"""Validation engine (FR-VALID-001, FR-VALID-002).

Hard rules prevent/quarantine invalid edges. Soft rules detect anomalies.
Findings are persisted with the validation run.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from uuid import uuid4

from eoip.contracts.source_event import utc_now_iso
from eoip.graph.documentation import document_reference_findings
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS, edge_endpoints_valid
from eoip.validation.quality import QualityMetrics

log = logging.getLogger(__name__)


class ValidationEngine:
    def __init__(self, store: GraphStore, *, vertex_limit: int = 10_001, edge_limit: int = 10_001) -> None:
        self._store = store
        self._vertex_limit = vertex_limit
        self._edge_limit = edge_limit

    def run(self) -> dict:
        run_id = str(uuid4())
        started_at = utc_now_iso()
        findings: list[dict] = []

        all_vertices = self._store.find_vertices(
            limit=self._vertex_limit,
            include_deleted=True,
        )
        vertices = [item for item in all_vertices if not item["properties"].get("deleted_at")]
        deleted_vertices = [item for item in all_vertices if item["properties"].get("deleted_at")]
        edges = self._store.find_edges(limit=self._edge_limit)
        vertices_by_id: dict[str, dict | None] = {item["vid"]: item for item in all_vertices}

        def get_vertex(vid: str) -> dict | None:
            if vid not in vertices_by_id:
                vertices_by_id[vid] = self._store.get_vertex(vid)
            return vertices_by_id[vid]

        for vertex in vertices:
            findings.extend(self._check_vertex(vertex))

        for edge in edges:
            findings.extend(self._check_edge(edge, get_vertex))

        findings.extend(self._check_orphans(vertices, edges))
        findings.extend(self._check_deletion_conflicts(deleted_vertices, edges))
        findings.extend(document_reference_findings(self._store, edges, get_vertex=get_vertex))

        quality = QualityMetrics.compute(vertices, edges, findings)

        result = {
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": utc_now_iso(),
            "findings": findings,
            "valid": not any(f["severity"] == "ERROR" for f in findings),
            "partial": len(all_vertices) >= self._vertex_limit or len(edges) >= self._edge_limit,
            "vertices_checked": len(all_vertices),
            "edges_checked": len(edges),
            "quality": quality.as_dict(),
        }

        self._persist_run(result)
        return result

    def _check_vertex(self, vertex: dict) -> list[dict]:
        findings = []
        label = vertex["label"]
        if label not in VERTEX_LABELS:
            findings.append(
                {
                    "canonical_id": vertex["canonical_id"],
                    "rule": "unknown_vertex_label",
                    "severity": "ERROR",
                    "detail": f"Unknown vertex label: {label}",
                }
            )
            return findings

        _domain, required, _optional = VERTEX_LABELS[label]
        missing = [key for key in required if vertex["properties"].get(key) is None]
        if missing:
            findings.append(
                {
                    "canonical_id": vertex["canonical_id"],
                    "rule": "required_properties",
                    "severity": "ERROR",
                    "missing": missing,
                    "detail": f"Missing required properties: {missing}",
                }
            )
        if not vertex.get("canonical_id"):
            findings.append(
                {
                    "canonical_id": vertex.get("canonical_id", "UNKNOWN"),
                    "rule": "missing_canonical_id",
                    "severity": "ERROR",
                    "detail": "Vertex has no canonical_id",
                }
            )

        cs = vertex["properties"].get("creation_status")
        if cs == "AMBIGUOUS":
            findings.append(
                {
                    "canonical_id": vertex["canonical_id"],
                    "rule": "ambiguous_needs_review",
                    "severity": "WARNING",
                    "detail": f"Vertex {label} has AMBIGUOUS creation_status and needs human review",
                }
            )

        return findings

    @staticmethod
    def _check_deletion_conflicts(vertices: list[dict], edges: list[dict]) -> list[dict]:
        active_edge_vertices = {
            endpoint
            for edge in edges
            if edge["properties"].get("is_current") is not False
            for endpoint in (edge["out_v"], edge["in_v"])
        }
        return [
            {
                "canonical_id": vertex["canonical_id"],
                "rule": "deletion_conflict",
                "severity": "WARNING",
                "detail": "Tombstoned entity is still referenced by an active relationship",
            }
            for vertex in vertices
            if vertex["vid"] in active_edge_vertices
        ]

    def _check_edge(self, edge: dict, get_vertex: Callable[[str], dict | None]) -> list[dict]:
        findings = []
        out_node = get_vertex(edge["out_v"])
        in_node = get_vertex(edge["in_v"])

        if out_node is None or in_node is None:
            findings.append(
                {
                    "edge_id": edge["eid"],
                    "rule": "dangling_endpoint",
                    "severity": "ERROR",
                    "detail": "Edge references a missing vertex",
                }
            )
            return findings

        if edge["label"] not in EDGE_LABELS:
            findings.append(
                {
                    "edge_id": edge["eid"],
                    "rule": "unknown_edge_label",
                    "severity": "ERROR",
                    "detail": f"Unknown edge label: {edge['label']}",
                }
            )
        elif not edge_endpoints_valid(edge["label"], out_node["label"], in_node["label"]):
            findings.append(
                {
                    "edge_id": edge["eid"],
                    "rule": "endpoint_types",
                    "severity": "ERROR",
                    "detail": f"{out_node['label']} -[{edge['label']}]-> {in_node['label']} violates ontology constraints",
                }
            )

        evidence_required = {"IMPLEMENTS", "REFERENCES", "DOCUMENTS", "MODIFIES", "DECLARES"}
        if edge["label"] in evidence_required and not edge["properties"].get("evidence_key"):
            findings.append(
                {
                    "edge_id": edge["eid"],
                    "rule": "missing_evidence",
                    "severity": "WARNING",
                    "detail": f"{edge['label']} edge missing evidence_key",
                }
            )

        VALID_CREATION_STATUSES = {"DETERMINISTIC", "INFERRED", "AMBIGUOUS", "MANUAL", "HUMAN_CONFIRMED"}
        cs = edge["properties"].get("creation_status")
        if not cs:
            findings.append(
                {
                    "edge_id": edge["eid"],
                    "rule": "missing_creation_status",
                    "severity": "WARNING",
                    "detail": "Edge missing creation_status",
                }
            )
        elif cs not in VALID_CREATION_STATUSES:
            findings.append(
                {
                    "edge_id": edge["eid"],
                    "rule": "invalid_creation_status",
                    "severity": "ERROR",
                    "detail": f"Invalid creation_status: {cs}",
                }
            )
        elif cs == "AMBIGUOUS":
            findings.append(
                {
                    "edge_id": edge["eid"],
                    "rule": "ambiguous_needs_review",
                    "severity": "WARNING",
                    "detail": "Edge has AMBIGUOUS creation_status and needs human review",
                }
            )

        return findings

    def _check_orphans(self, vertices: list[dict], edges: list[dict]) -> list[dict]:
        findings = []
        referenced_vids = set()
        for edge in edges:
            referenced_vids.add(edge["out_v"])
            referenced_vids.add(edge["in_v"])

        for vertex in vertices:
            definition = VERTEX_LABELS.get(vertex["label"])
            is_meta = definition is not None and definition[0] == "META"
            if not is_meta and vertex["vid"] not in referenced_vids:
                findings.append(
                    {
                        "canonical_id": vertex["canonical_id"],
                        "rule": "orphan_vertex",
                        "severity": "WARNING",
                        "detail": f"Vertex {vertex['label']} has no edges",
                    }
                )
        return findings

    def _persist_run(self, result: dict) -> None:
        try:
            run_cid = f"urn:eoip:meta:validation-run:{result['run_id']}"
            run_vertex = self._store.upsert_vertex(
                "ValidationRun",
                {
                    "canonical_id": run_cid,
                    "run_status": "PASSED" if result["valid"] else "FINDINGS",
                    "started_at": result["started_at"],
                    "finished_at": result["finished_at"],
                    "counts": str(len(result["findings"])),
                },
            )
            for i, finding in enumerate(result["findings"]):
                finding_cid = f"urn:eoip:meta:validation-finding:{result['run_id']}:{i}"
                self._store.upsert_vertex(
                    "ValidationFinding",
                    {
                        "canonical_id": finding_cid,
                        "severity": finding["severity"],
                        "rule_id": finding["rule"],
                        "description": finding.get("detail", ""),
                        "remediation": finding.get("remediation"),
                    },
                )
                entity_cid = finding.get("canonical_id")
                if entity_cid:
                    entity = self._store.get_vertex_by_canonical_id(entity_cid)
                    if entity and edge_endpoints_valid("VALIDATED_BY", entity["label"], "ValidationRun"):
                        self._store.upsert_edge(
                            "VALIDATED_BY",
                            entity["vid"],
                            run_vertex["vid"],
                            {"fact_key": f"validation:{result['run_id']}:{entity_cid}"},
                        )
        except Exception:
            log.exception(
                "validation.persistence_failed",
                extra={"event": "validation.persistence_failed", "run_id": result["run_id"]},
            )
            raise
