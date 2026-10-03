"""Validated, idempotent loader for the cross-domain enterprise demo pack."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from eoip.contracts.source_event import SourceEvent, utc_now_iso
from eoip.graph.meta import link_domains
from eoip.graph.store import GraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.pipeline import IngestionGraphStore
from eoip.ontology.manifest import edge_endpoints_valid
from eoip.validation.gate import MutationBlocked, check_edge, check_vertex
from jsonschema import Draft202012Validator

DEFAULT_PACK = Path("examples/demo-enterprise/scenario-pack.json")
DEFAULT_SCHEMA = Path("schemas/demo_scenario_pack.schema.json")


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_demo_scenario_pack(project_root: str | Path | None = None) -> dict:
    """Return the checked-in scenario catalog used by the API and presenter guide."""
    root = Path(project_root or Path(__file__).resolve().parents[2])
    return _read_json(root / DEFAULT_PACK)


def validate_demo_scenario_pack(pack: dict, schema: dict) -> None:
    """Validate JSON shape plus ontology labels, properties, endpoints and scenario paths."""
    Draft202012Validator(schema).validate(pack)
    vertices = {}
    for item in pack["vertices"]:
        label = item["label"]
        properties = item["properties"]
        check_vertex(label, properties)
        canonical_id = properties["canonical_id"]
        if canonical_id in vertices:
            raise MutationBlocked(f"duplicate demo vertex: {canonical_id}", label=label)
        vertices[canonical_id] = label

    seen_scenarios = set()
    for scenario in pack["scenarios"]:
        if scenario["id"] in seen_scenarios:
            raise ValueError(f"duplicate demo scenario: {scenario['id']}")
        seen_scenarios.add(scenario["id"])
        if scenario["entrypoint"] not in vertices:
            raise ValueError(f"scenario entrypoint is not a fixture vertex: {scenario['entrypoint']}")
        missing = [canonical_id for canonical_id in scenario["expected_path"] if canonical_id not in vertices]
        if missing:
            raise ValueError(f"scenario path references missing fixture vertices: {missing}")

    for item in pack["edges"]:
        source = item["from"]
        target = item["to"]
        if source not in vertices or target not in vertices:
            raise MutationBlocked(f"demo edge references missing endpoint: {source} -> {target}")
        properties = item.get("properties", {})
        check_edge(item["label"], vertices[source], vertices[target], properties)
        if not edge_endpoints_valid(item["label"], vertices[source], vertices[target]):
            raise MutationBlocked(
                f"invalid demo edge endpoints: {vertices[source]} -[{item['label']}]-> {vertices[target]}"
            )


def load_demo_scenario_pack(
    store: GraphStore,
    data_dir: str | Path,
    *,
    project_root: str | Path | None = None,
    pack_path: str | Path | None = None,
) -> dict:
    """Capture and load the enterprise pack through the canonical mutation boundary."""
    package_root = Path(__file__).resolve().parents[2]
    root = Path(project_root or package_root)
    source = Path(pack_path) if pack_path else root / DEFAULT_PACK
    if not source.is_file() and pack_path is None:
        source = package_root / DEFAULT_PACK
    schema_path = root / DEFAULT_SCHEMA
    if not schema_path.is_file():
        schema_path = package_root / DEFAULT_SCHEMA
    pack = _read_json(source)
    validate_demo_scenario_pack(pack, _read_json(schema_path))

    serialized = json.dumps(pack, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    event_id = f"{pack['dataset_id']}-{pack['version']}"
    event = SourceEvent(
        event_id=event_id,
        source_system="demo_enterprise",
        source_record_id=source.name,
        source_version=pack["version"],
        payload_hash=digest,
        payload=pack,
        metadata={"fixture_path": str(DEFAULT_PACK).replace("\\", "/")},
    )
    FileEventCapture(Path(data_dir) / "raw").capture(event)

    run_id = f"demo-enterprise-{pack['version']}"
    graph = IngestionGraphStore(store)
    graph.begin_run(run_id)
    observed_at = utc_now_iso()
    loaded = []
    for item in pack["vertices"]:
        properties = {
            **item["properties"],
            "source_system": item["properties"].get("source_system", "demo_enterprise"),
            "ingestion_run_id": run_id,
            "last_seen": observed_at,
        }
        loaded.append(graph.upsert_vertex(item["label"], properties))

    for index, item in enumerate(pack["edges"]):
        properties = {
            **item.get("properties", {}),
            "fact_key": item.get("properties", {}).get(
                "fact_key", f"demo:{pack['version']}:{index}:{item['label']}"
            ),
            "source_system": "demo_enterprise",
            "source_ref": f"fixture://{DEFAULT_PACK.as_posix()}",
            "evidence_key": event_id,
            "ingestion_run_id": run_id,
            "creation_status": item.get("properties", {}).get("creation_status", "DETERMINISTIC"),
        }
        graph.upsert_edge(item["label"], item["from"], item["to"], properties)

    run = graph.upsert_vertex(
        "IngestionRun",
        {
            "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}",
            "ingestion_run_id": run_id,
            "run_kind": "ENTERPRISE_DEMO_FIXTURE",
            "run_status": "SUCCEEDED",
            "counts": json.dumps({"vertices": len(loaded), "edges": len(pack["edges"])}),
            "started_at": event.captured_at,
            "finished_at": observed_at,
            "source_system": "demo_enterprise",
        },
    )
    ingestion_links = 0
    for vertex in loaded:
        if edge_endpoints_valid("INGESTED_IN", vertex["label"], "IngestionRun"):
            graph.upsert_edge(
                "INGESTED_IN",
                vertex["canonical_id"],
                run["canonical_id"],
                {
                    "fact_key": f"demo-run:{vertex['canonical_id']}",
                    "source_system": "demo_enterprise",
                    "source_ref": f"fixture://{DEFAULT_PACK.as_posix()}",
                    "evidence_key": event_id,
                    "ingestion_run_id": run_id,
                },
            )
            ingestion_links += 1
    domain_links = link_domains(graph, loaded)
    return {
        "run_id": run_id,
        "run_status": "SUCCEEDED",
        "dataset_id": pack["dataset_id"],
        "version": pack["version"],
        "vertices": len(loaded),
        "edges": len(pack["edges"]),
        "ingestion_links": ingestion_links,
        "domain_links": domain_links,
        "scenarios": [
            {"id": item["id"], "title": item["title"], "entrypoint": item["entrypoint"]}
            for item in pack["scenarios"]
        ],
    }
