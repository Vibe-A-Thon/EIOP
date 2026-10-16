"""Knowledge Capsules (G2-CAP-001..006, Capsoryn).

A Knowledge Capsule is a bounded, portable graph context for a task, person or
agent. It reduces unnecessary context exposure: instead of handing an agent
the whole enterprise graph, a capsule carries only the declared roots, their
bounded traversal, the requested domains, an optional trust threshold, and the
evidence references behind every included relationship.

Reproducibility: the capsule id is a hash of the normalized definition plus a
fingerprint of the graph region it was built from, so the same definition over
the same graph state rebuilds to the same capsule. Manifests are persisted
under the data directory and are exportable as a local JSON package.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from eoip.graph.traversal import GraphTraversal

TRUST_ORDER = ("DETERMINISTIC", "INFERRED")


@dataclass(frozen=True)
class CapsuleDefinition:
    """Declarative capsule contract (G2-CAP-001)."""

    name: str
    root_entities: tuple[str, ...]
    max_depth: int = 2
    domains: tuple[str, ...] | None = None
    time_window: tuple[str, str] | None = None
    trust_threshold: str | None = None
    include_evidence: bool = True
    result_limit: int = 200

    def normalized(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "root_entities": sorted(self.root_entities),
            "max_depth": self.max_depth,
            "domains": sorted(self.domains) if self.domains else None,
            "time_window": list(self.time_window) if self.time_window else None,
            "trust_threshold": self.trust_threshold,
            "include_evidence": self.include_evidence,
            "result_limit": self.result_limit,
        }


@dataclass
class KnowledgeCapsule:
    capsule_id: str
    definition: dict[str, Any]
    entities: list[dict[str, Any]]
    relationships: list[dict[str, Any]]
    evidence_refs: list[str]
    graph_fingerprint: str
    truncated: bool = False
    manifest: dict[str, Any] = field(default_factory=dict)


def _content_hash(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _edge_trust(edge: dict) -> str:
    return str(edge["properties"].get("creation_status") or "DETERMINISTIC").upper()


def _passes_trust(edge: dict, threshold: str | None) -> bool:
    if threshold is None:
        return True
    threshold = threshold.upper()
    try:
        return TRUST_ORDER.index(_edge_trust(edge)) <= TRUST_ORDER.index(threshold)
    except ValueError:
        return True


class KnowledgeCapsuleService:
    """Builds and persists reproducible knowledge capsules."""

    def __init__(self, store, capsule_root: str | Path) -> None:
        self._store = store
        self._root = Path(capsule_root)
        self._root.mkdir(parents=True, exist_ok=True)

    def build(self, definition: CapsuleDefinition) -> KnowledgeCapsule:
        if not definition.root_entities:
            raise ValueError("capsule requires at least one root entity")
        if not 1 <= definition.max_depth <= 6:
            raise ValueError("capsule max_depth must be between 1 and 6")

        traversal = GraphTraversal(
            self._store, max_depth=definition.max_depth, max_results=definition.result_limit
        )
        entities: dict[str, dict[str, Any]] = {}
        relationships: dict[str, dict[str, Any]] = {}
        evidence_refs: set[str] = set()
        truncated = False

        for root_cid in definition.root_entities:
            result = traversal.impact(root_cid, max_depth=definition.max_depth)
            if result["source"] is None:
                raise ValueError(f"root entity not found: {root_cid}")
            candidates = [result["source"], *[item["vertex"] for item in result["impacted"]]]
            if result.get("truncated"):
                truncated = True
            for vertex in candidates:
                domain = vertex["properties"].get("graph_domain")
                if definition.domains and domain not in definition.domains:
                    continue
                entities.setdefault(
                    vertex["canonical_id"],
                    {
                        "canonical_id": vertex["canonical_id"],
                        "label": vertex["label"],
                        "domain": domain,
                        "name": (
                            vertex["properties"].get("issue_key")
                            or vertex["properties"].get("name")
                            or vertex["properties"].get("qualified_name")
                            or vertex["canonical_id"]
                        ),
                    },
                )
            for item in result["impacted"]:
                for edge in item["path"]["edges"]:
                    if not _passes_trust(edge, definition.trust_threshold):
                        continue
                    source_ref = edge["properties"].get("source_ref")
                    if definition.include_evidence and source_ref:
                        evidence_refs.add(source_ref)
                    relationships.setdefault(
                        edge["eid"],
                        {
                            "edge_id": edge["eid"],
                            "type": edge["label"],
                            "from_id": edge.get("out_cid"),
                            "to_id": edge.get("in_cid"),
                            "trust": _edge_trust(edge),
                            "source_ref": source_ref,
                        },
                    )

        # Only keep relationships whose endpoints are both inside the capsule.
        entities = {
            cid: entity
            for cid, entity in entities.items()
            if any(
                relationship["from_id"] == cid or relationship["to_id"] == cid
                for relationship in relationships.values()
            ) or cid in definition.root_entities
        }
        relationships = {
            eid: relationship
            for eid, relationship in relationships.items()
            if relationship["from_id"] in entities and relationship["to_id"] in entities
        }

        fingerprint_payload = {
            "vertices": len(entities),
            "edges": len(relationships),
            "roots": sorted(definition.root_entities),
        }
        graph_fingerprint = _content_hash(fingerprint_payload)
        capsule_id = _content_hash(
            {"definition": definition.normalized(), "graph": graph_fingerprint}
        )
        manifest = {
            "capsule_id": capsule_id,
            "created_with": "eoip-capsules/1.0",
            "definition": definition.normalized(),
            "counts": {"entities": len(entities), "relationships": len(relationships)},
            "graph_fingerprint": graph_fingerprint,
            "evidence_refs": sorted(evidence_refs),
        }
        capsule = KnowledgeCapsule(
            capsule_id=capsule_id,
            definition=definition.normalized(),
            entities=sorted(entities.values(), key=lambda item: item["canonical_id"]),
            relationships=sorted(relationships.values(), key=lambda item: item["edge_id"]),
            evidence_refs=sorted(evidence_refs),
            graph_fingerprint=graph_fingerprint,
            truncated=truncated,
            manifest=manifest,
        )
        destination = self._root / f"{definition.name}--{capsule_id[:16]}.json"
        destination.write_text(
            json.dumps(
                {
                    "manifest": manifest,
                    "entities": capsule.entities,
                    "relationships": capsule.relationships,
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return capsule

    def list_manifests(self) -> list[dict[str, Any]]:
        manifests = []
        for path in sorted(self._root.glob("*.json")):
            try:
                document = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            manifests.append(document.get("manifest", {}))
        return manifests

    def get_manifest(self, name: str) -> dict[str, Any] | None:
        matches = sorted(self._root.glob(f"{name}--*.json"))
        if not matches:
            return None
        document = json.loads(matches[-1].read_text(encoding="utf-8"))
        return document

    def export_package(self, name: str, output_path: str | Path | None = None) -> Path:
        """Exports capsule into an approved local package format (G2-CAP-006)."""
        matches = sorted(self._root.glob(f"{name}--*.json"))
        if not matches:
            raise FileNotFoundError(f"Capsule package not found for {name}")
        source_path = matches[-1]
        raw = json.loads(source_path.read_text(encoding="utf-8"))

        package_payload = {
            "package_format": "eoip-capsule-package/1.0",
            "capsule_id": raw.get("manifest", {}).get("capsule_id"),
            "manifest": raw.get("manifest", {}),
            "payload": {
                "entities": raw.get("entities", []),
                "relationships": raw.get("relationships", []),
            },
        }

        if output_path is None:
            dest = self._root / f"{name}.capsule.json"
        else:
            dest = Path(output_path)
            dest.parent.mkdir(parents=True, exist_ok=True)

        dest.write_text(json.dumps(package_payload, indent=2, sort_keys=True), encoding="utf-8")
        return dest


EXAMPLE_CAPSULE_TYPES: tuple[str, ...] = (
    "release",
    "incident",
    "service",
    "application",
    "change_request",
    "architecture_review",
    "audit_evidence",
)


def create_example_capsule_definition(
    capsule_type: str,
    root_entities: tuple[str, ...],
    max_depth: int = 2,
    **kwargs: Any,
) -> CapsuleDefinition:
    """Creates a standard capsule definition for supported example types (G2-CAP-005)."""
    norm_type = capsule_type.lower().replace("-", "_").replace(" ", "_")
    if norm_type not in EXAMPLE_CAPSULE_TYPES:
        raise ValueError(
            f"Unsupported example capsule type: {capsule_type}. Must be one of {EXAMPLE_CAPSULE_TYPES}"
        )
    return CapsuleDefinition(
        name=norm_type,
        root_entities=root_entities,
        max_depth=max_depth,
        **kwargs,
    )
