"""Deterministic replay of captured raw SourceEvents (FR-CONN-006).

Replay re-runs events previously captured under ``<data>/raw/<source_system>``
through the same capture-first ingestion services used at baseline time. The
pipeline is idempotent: capture deduplicates by event id + payload hash and
graph upserts are keyed by canonical ids, so replay repairs missed or failed
mutations without creating duplicates.

Scope: sources with file-captured SourceEvents (jira, gitlab). Other sources
raise a stable error instead of silently no-oping.
"""

from __future__ import annotations

import json
from pathlib import Path

from eoip.codegraph.parser import CodeParser
from eoip.connectors.gitlab_json import GitLabJsonConnector
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.connectors.local_code import LocalCodeConnector
from eoip.contracts.source_event import SourceEvent
from eoip.ingestion.code import CodeIngestionService
from eoip.ingestion.gitlab import GitLabIngestionService
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService

SUPPORTED_SOURCES = frozenset({"jira", "gitlab", "git"})
_VOLATILE_VERTEX_LABELS = frozenset({"IngestionRun", "ValidationRun", "ValidationFinding"})
_VOLATILE_EDGE_LABELS = frozenset({"INGESTED_IN", "VALIDATED_BY"})
_VOLATILE_PROPERTIES = frozenset(
    {
        "ingestion_run_id",
        "run_id",
        "started_at",
        "finished_at",
    }
)


def replay_captured_events(
    store,
    data_root,
    *,
    source_system: str,
    event_ids: list[str] | None = None,
    dry_run: bool = False,
    mapping_path: str = "config/mappings/jira-mvp.yaml",
    repository_id: str = "demo",
) -> dict:
    """Replay captured raw events for a source through its ingestion service."""
    if source_system not in SUPPORTED_SOURCES:
        raise ValueError(
            f"replay is not supported for source '{source_system}'; "
            f"supported: {sorted(SUPPORTED_SOURCES)}"
        )
    root = Path(data_root)
    before = logical_graph_output(store)
    raw_dir = root / "raw" / source_system
    if not raw_dir.exists():
        return {
            "run_status": "SUCCEEDED",
            "records_seen": 0,
            "records_replayed": 0,
            "source_system": source_system,
            "detail": "no captured events for source",
            "logical_diff": logical_output_diff(before, before),
        }

    wanted = set(event_ids) if event_ids else None
    events: list[SourceEvent] = []
    available = {p.stem for p in raw_dir.glob("*.json")}
    if wanted is not None:
        not_found = sorted(wanted - available)
        if not_found:
            raise ValueError(f"captured events not found: {not_found}")
    for path in sorted(raw_dir.glob("*.json")):
        if wanted is not None and path.stem not in wanted:
            continue
        event = SourceEvent.model_validate_json(path.read_text(encoding="utf-8"))
        if event.event_id != path.stem:
            raise ValueError(f"captured event id mismatch: {path.name}")
        if event.source_system != source_system:
            raise ValueError(f"captured event source mismatch: {path.name}")
        events.append(event)

    capture = FileEventCapture(root / "raw")
    if source_system == "jira":
        service = JiraIngestionService(
            store,
            JiraJsonConnector.from_yaml(mapping_path),
            capture,
            root / "dlq",
        )
        result = service.ingest_events(events, dry_run=dry_run)
    elif source_system == "gitlab":
        service = GitLabIngestionService(
            store,
            repository_id,
            GitLabJsonConnector(),
            capture,
            root / "dlq",
        )
        result = service.ingest_events(events, dry_run=dry_run)
    else:
        repo_ids = {event.payload.get("repo_id") for event in events}
        if len(repo_ids) > 1 or None in repo_ids:
            raise ValueError("captured code events must belong to one repository")
        captured_repo_id = next(iter(repo_ids), repository_id)
        service = CodeIngestionService(
            store,
            LocalCodeConnector(),
            CodeParser(),
            capture,
            root / "dlq",
        )
        result = service.ingest_events(
            events,
            captured_repo_id,
            repository_name=captured_repo_id,
            dry_run=dry_run,
        )
    result["source_system"] = source_system
    result["records_replayed"] = result.get("records_accepted", 0)
    result["logical_diff"] = logical_output_diff(before, logical_graph_output(store))
    return result


def replay_summary(result: dict) -> str:
    return json.dumps(result, sort_keys=True)[:500]


def logical_graph_output(store, *, limit: int = 100_000) -> dict:
    """Return a stable graph projection suitable for replay golden comparisons."""
    vertices = store.find_vertices(limit=limit, include_deleted=True)
    stable_vertices = {}
    for vertex in vertices:
        if vertex["label"] in _VOLATILE_VERTEX_LABELS:
            continue
        stable_vertices[vertex["canonical_id"]] = {
            "label": vertex["label"],
            "properties": {
                key: value
                for key, value in sorted(vertex["properties"].items())
                if key not in _VOLATILE_PROPERTIES
            },
        }

    stable_edges = {}
    for edge in store.find_edges(limit=limit, include_historical=True):
        if edge["label"] in _VOLATILE_EDGE_LABELS:
            continue
        out_cid = edge.get("out_cid") or _canonical_id(store, edge["out_v"])
        in_cid = edge.get("in_cid") or _canonical_id(store, edge["in_v"])
        if out_cid not in stable_vertices or in_cid not in stable_vertices:
            continue
        properties = {
            key: value
            for key, value in sorted(edge["properties"].items())
            if key not in _VOLATILE_PROPERTIES
        }
        identity = properties.get("edge_key") or "|".join(
            (edge["label"], out_cid, in_cid, str(properties.get("fact_key", "")))
        )
        stable_edges[identity] = {
            "label": edge["label"],
            "out": out_cid,
            "in": in_cid,
            "properties": properties,
        }
    return {"vertices": stable_vertices, "edges": stable_edges}


def logical_output_diff(expected: dict, actual: dict) -> dict:
    """Describe stable logical additions, removals, and mutations."""
    result = {}
    for collection in ("vertices", "edges"):
        expected_items = expected.get(collection, {})
        actual_items = actual.get(collection, {})
        expected_keys = set(expected_items)
        actual_keys = set(actual_items)
        result[collection] = {
            "added": sorted(actual_keys - expected_keys),
            "removed": sorted(expected_keys - actual_keys),
            "changed": sorted(
                key
                for key in expected_keys & actual_keys
                if expected_items[key] != actual_items[key]
            ),
        }
    result["equivalent"] = all(
        not result[collection][change]
        for collection in ("vertices", "edges")
        for change in ("added", "removed", "changed")
    )
    return result


def _canonical_id(store, vid: str) -> str:
    vertex = store.get_vertex(vid)
    return vertex["canonical_id"] if vertex else f"missing:{vid}"
