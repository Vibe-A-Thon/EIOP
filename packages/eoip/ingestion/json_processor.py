"""JSON file processor: ingests arbitrary JSON files into the knowledge graph.

Handles multiple JSON formats:
- Array of entity objects
- Nested objects with entity/relationship sections
- Single entity documents
- EOIP NormalizedEntity/NormalizedRelationship envelopes

Builds vertices, edges, metadata graphs, and relationship graphs from JSON.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime
from typing import Any

from eoip.contracts.graph_mutation import GraphMutation
from eoip.contracts.normalized import NormalizedEntity
from eoip.graph.store import GraphStore
from eoip.ingestion.code_graph_json import normalize_code_export
from eoip.ingestion.pipeline import apply_graph_mutation
from eoip.ontology.manifest import VERTEX_LABELS
from eoip.validation.gate import MutationBlocked


class ProcessingResult:
    """Result of processing one or more JSON files."""

    def __init__(self) -> None:
        self.files_processed: int = 0
        self.entities_created: int = 0
        self.relationships_created: int = 0
        self.errors: list[dict[str, Any]] = []
        self.log: list[str] = []
        self.metadata_vertices: int = 0
        self.formats_generated: list[str] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "files_processed": self.files_processed,
            "entities_created": self.entities_created,
            "relationships_created": self.relationships_created,
            "metadata_vertices": self.metadata_vertices,
            "formats_generated": self.formats_generated,
            "error_count": len(self.errors),
            "errors": self.errors[:50],
            "log": self.log[-100:],
        }


def _generate_canonical_id(entity_type: str, data: dict) -> str:
    name = data.get("name") or data.get("id") or data.get("key") or data.get("canonical_id", "")
    if name:
        return f"{entity_type}:{name}"
    content = json.dumps(data, sort_keys=True)
    return f"{entity_type}:{hashlib.sha256(content.encode()).hexdigest()[:16]}"


def _infer_entity_type(data: dict) -> str:
    if "entity_type" in data:
        return data["entity_type"]
    if "type" in data:
        raw = data["type"]
        mapped = {
            "issue": "Issue", "bug": "Issue", "story": "Issue", "task": "Issue",
            "commit": "Commit", "file": "CodeFile", "symbol": "CodeSymbol",
            "pipeline": "Pipeline", "build": "BuildRecord", "test": "TestCase",
            "document": "Document", "page": "Document", "article": "Document",
            "person": "Person", "user": "Person", "author": "Person",
            "service": "Service", "api": "Service", "endpoint": "Service",
            "requirement": "Requirement", "spec": "Requirement",
            "deployment": "Deployment", "release": "Release",
        }
        normalized = str(raw).lower().strip()
        return mapped.get(normalized, raw if raw in VERTEX_LABELS else "GenericEntity")
    return "GenericEntity"


def _infer_domain(entity_type: str) -> str:
    domain_map = VERTEX_LABELS
    if entity_type in domain_map:
        return domain_map[entity_type][0]
    return "INTEGRATION"


def _extract_relationships(data: dict, source_cid: str) -> list[dict]:
    rels = []
    for key in ("relationships", "relations", "edges", "links", "connections"):
        items = data.get(key, [])
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    target = item.get("to_id") or item.get("target") or item.get("to") or ""
                    rel_type = item.get("type") or item.get("relationship_type") or "RELATED_TO"
                    if target:
                        rels.append({
                            "from_id": source_cid,
                            "to_id": target,
                            "type": rel_type,
                            "properties": {
                                k: v for k, v in item.items()
                                if k not in ("to_id", "target", "to", "type", "relationship_type")
                            },
                        })
    for key in ("parent", "parent_id"):
        if data.get(key):
            rels.append({"from_id": source_cid, "to_id": data[key], "type": "CHILD_OF", "properties": {}})
    for key in ("depends_on", "dependencies"):
        deps = data.get(key, [])
        if isinstance(deps, list):
            for dep in deps:
                if isinstance(dep, str):
                    rels.append({"from_id": source_cid, "to_id": dep, "type": "DEPENDS_ON", "properties": {}})
    return rels


class JsonProcessor:
    """Processes JSON files into the EOIP knowledge graph."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def process_json_data(
        self,
        data: Any,
        *,
        source_label: str = "json_upload",
        pipeline_id: str = "manual",
    ) -> ProcessingResult:
        result = ProcessingResult()
        now = datetime.now(UTC).isoformat()
        pending_relationships: list[dict] = []

        if isinstance(data, dict) and all(key in data for key in ("repository", "files", "symbols")):
            try:
                data = normalize_code_export(data)
            except ValueError as exc:
                result.errors.append({"source_label": source_label, "error": str(exc)})
                result.log.append(f"[ERR] Code export {source_label}: {exc}")
                result.files_processed = 1
                return result

        if isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    pending_relationships.extend(self._process_entity(item, result, source_label, pipeline_id, now))
                else:
                    result.errors.append({"index": i, "error": "Expected object in array"})
        elif isinstance(data, dict):
            if "entities" in data or "nodes" in data:
                entities = data.get("entities") or data.get("nodes") or []
                for item in entities:
                    if isinstance(item, dict):
                        pending_relationships.extend(self._process_entity(item, result, source_label, pipeline_id, now))
                relationships = data.get("relationships") or data.get("edges") or []
                for rel in relationships:
                    if isinstance(rel, dict):
                        pending_relationships.append(rel)
            else:
                pending_relationships.extend(self._process_entity(data, result, source_label, pipeline_id, now))
        else:
            result.errors.append({"error": "JSON root must be an object or array"})

        for rel in pending_relationships:
            self._process_relationship(rel, result, now)
        self._create_metadata_vertex(result, source_label, pipeline_id, now)
        result.files_processed = 1
        result.log.append(f"[{now}] Processing complete: {result.entities_created} entities, {result.relationships_created} relationships")
        return result

    def process_json_file(
        self,
        file_path: str,
        *,
        source_label: str = "",
        pipeline_id: str = "manual",
    ) -> ProcessingResult:
        if not source_label:
            source_label = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.process_json_data(data, source_label=source_label, pipeline_id=pipeline_id)

    def process_json_directory(
        self,
        dir_path: str,
        *,
        pipeline_id: str = "batch",
    ) -> ProcessingResult:
        combined = ProcessingResult()
        for name in sorted(os.listdir(dir_path)):
            if not name.lower().endswith(".json"):
                continue
            path = os.path.join(dir_path, name)
            if not os.path.isfile(path):
                continue
            try:
                result = self.process_json_file(path, source_label=name, pipeline_id=pipeline_id)
                combined.entities_created += result.entities_created
                combined.relationships_created += result.relationships_created
                combined.metadata_vertices += result.metadata_vertices
                combined.errors.extend(result.errors)
                combined.log.extend(result.log)
                combined.files_processed += 1
            except Exception as exc:  # noqa: BLE001 - one bad file must not abort the batch
                combined.errors.append({"file": name, "error": str(exc)})
                combined.log.append(f"[ERROR] Failed to process {name}: {exc}")
        return combined

    def _process_entity(
        self, data: dict, result: ProcessingResult,
        source_label: str, pipeline_id: str, now: str,
    ) -> list[dict]:
        entity_type = _infer_entity_type(data)
        domain = _infer_domain(entity_type)
        cid = data.get("canonical_id") or _generate_canonical_id(entity_type, data)

        from eoip.ontology.manifest import PROPERTY_KEYS
        reserved = {"entity_type", "type", "canonical_id", "graph_domain",
                     "relationships", "relations", "edges", "links", "connections",
                     "parent", "parent_id", "depends_on", "dependencies"}
        properties = {k: v for k, v in data.items() if k not in reserved and isinstance(v, (str, int, float, bool)) and k in PROPERTY_KEYS}
        properties["canonical_id"] = cid
        if "name" not in properties:
            properties["name"] = data.get("name") or data.get("key") or data.get("title") or data.get("id") or cid
        properties["source_connector"] = source_label
        properties["pipeline_id"] = pipeline_id
        properties["last_ingestion_run"] = now

        if entity_type not in VERTEX_LABELS:
            entity_type = "GenericEntity"
            domain = "INTEGRATION"

        try:
            entity = NormalizedEntity(
                canonical_id=cid,
                entity_type=entity_type,
                graph_domain=domain,
                source_refs=[f"json:{source_label}"],
                creation_status="DETERMINISTIC",
                confidence=1.0,
                properties=properties,
            )
            mutation = GraphMutation(
                mutation_id=f"json-{cid}-{now}",
                ingestion_run_id=f"json:{pipeline_id}:{now}",
                target_kind="VERTEX",
                operation="UPSERT",
                payload=entity.model_dump(),
            )
            apply_graph_mutation(self._store, mutation)
            result.entities_created += 1
            result.log.append(f"[OK] Entity: {entity_type}:{cid}")
        except MutationBlocked as exc:
            result.errors.append({"canonical_id": cid, "entity_type": entity_type, "error": str(exc)})
            result.log.append(f"[ERR] Entity {cid}: {exc}")
        except Exception as exc:  # noqa: BLE001 - record and continue per entity
            result.errors.append({"canonical_id": cid, "entity_type": entity_type, "error": str(exc)})
            result.log.append(f"[ERR] Entity {cid}: {exc}")

        return _extract_relationships(data, cid)

    def _process_relationship(self, rel: dict, result: ProcessingResult, now: str) -> None:
        from_id = rel.get("from_id") or rel.get("source") or rel.get("from") or ""
        to_id = rel.get("to_id") or rel.get("target") or rel.get("to") or ""
        rel_type = rel.get("type") or rel.get("relationship_type") or "RELATED_TO"
        if not from_id or not to_id:
            result.errors.append({"relationship": rel_type, "error": "Missing from_id or to_id"})
            return

        source_v = self._store.get_vertex_by_canonical_id(from_id)
        target_v = self._store.get_vertex_by_canonical_id(to_id)
        if not source_v or not target_v:
            result.errors.append({
                "relationship": rel_type, "from_id": from_id, "to_id": to_id,
                "error": f"Endpoint not found: {'from' if not source_v else 'to'}",
            })
            return

        props = rel.get("properties", {})
        if isinstance(props, dict):
            props = {k: v for k, v in props.items() if isinstance(v, (str, int, float, bool))}
        else:
            props = {}
        props["creation_status"] = rel.get("creation_status", "DETERMINISTIC")
        props["last_ingestion_run"] = now

        try:
            self._store.upsert_edge(rel_type, source_v["vid"], target_v["vid"], props)
            result.relationships_created += 1
            result.log.append(f"[OK] Edge: {from_id} --{rel_type}--> {to_id}")
        except Exception as exc:  # noqa: BLE001 - record and continue per relationship
            result.errors.append({"relationship": rel_type, "from_id": from_id, "to_id": to_id, "error": str(exc)})
            result.log.append(f"[ERR] Edge {from_id}->{to_id}: {exc}")

    def _create_metadata_vertex(
        self, result: ProcessingResult,
        source_label: str, pipeline_id: str, now: str,
    ) -> None:
        if result.entities_created == 0:
            return
        meta_cid = f"IngestionRun:json:{pipeline_id}:{now}"
        try:
            self._store.upsert_vertex("IngestionRun", {
                "canonical_id": meta_cid,
                "run_kind": "json_ingestion",
                "source_connector": source_label,
                "pipeline_id": pipeline_id,
                "run_status": "SUCCEEDED" if not result.errors else "PARTIAL",
                "started_at": now,
                "completed_at": datetime.now(UTC).isoformat(),
                "records_accepted": result.entities_created,
                "records_rejected": len(result.errors),
            })
            result.metadata_vertices = 1
            result.log.append(f"[OK] Metadata: {meta_cid}")
        except Exception as exc:  # noqa: BLE001 - metadata failure must not fail ingested entities
            result.log.append(f"[WARN] Metadata vertex skipped: {exc}")
