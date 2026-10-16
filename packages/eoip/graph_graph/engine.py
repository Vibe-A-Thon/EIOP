"""Graph-over-Graph Engineering (CORE-004).

Meta-graph operations that layer graphs:
- Ontology graph over instance graph
- Temporal graph over current graph
- Compliance graph over data graph
- Knowledge graph over schema graph
- Security/provenance graph over entity graph
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.graph_graph.engine")


class LayerType(str, Enum):
    ONTOLOGY = "ONTOLOGY"
    INSTANCE = "INSTANCE"
    TEMPORAL = "TEMPORAL"
    COMPLIANCE = "COMPLIANCE"
    SCHEMA = "SCHEMA"
    PROVENANCE = "PROVENANCE"
    SECURITY = "SECURITY"


class RelationKind(str, Enum):
    MAPS_TO = "maps_to"
    CONSTRAINS = "constrains"
    EXTENDS = "extends"
    OVERRIDES = "overrides"
    VALIDATES = "validates"


@dataclass
class GraphLayer:
    """A distinct layer in the meta-graph hierarchy."""

    name: str
    layer_type: LayerType
    priority: int = 10
    schema: dict[str, Any] = field(default_factory=dict)
    store: MemoryGraphStore = field(default_factory=MemoryGraphStore)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "layer_type": self.layer_type.value,
            "priority": self.priority,
            "vertex_count": self.store.count_vertices(),
            "edge_count": self.store.count_edges(),
            "schema": self.schema,
            "metadata": self.metadata,
        }


@dataclass
class LayerRelation:
    """A directed relationship bridging two distinct graph layers."""

    relation_type: str  # "maps_to", "constrains", "extends", "overrides", "validates"
    source_layer: str
    source_id: str
    target_layer: str
    target_id: str
    properties: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)



class GraphOverGraphEngine:
    """Engine orchestrating cross-layer meta-graph execution and multi-layer queries."""

    _instance: GraphOverGraphEngine | None = None

    def __init__(self) -> None:
        self.layers: dict[str, GraphLayer] = {}
        self.cross_layer_relations: list[LayerRelation] = []
        self._bootstrap_default_layers()

    @classmethod
    def get_instance(cls) -> GraphOverGraphEngine:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _bootstrap_default_layers(self) -> None:
        for lt in LayerType:
            layer = GraphLayer(name=lt.value.lower(), layer_type=lt, priority=self._default_priority(lt))
            self.register_layer(layer)

    def _default_priority(self, lt: LayerType) -> int:
        priorities = {
            LayerType.SECURITY: 1,
            LayerType.COMPLIANCE: 2,
            LayerType.ONTOLOGY: 3,
            LayerType.SCHEMA: 4,
            LayerType.PROVENANCE: 5,
            LayerType.INSTANCE: 10,
            LayerType.TEMPORAL: 15,
        }
        return priorities.get(lt, 10)

    def register_layer(self, layer: GraphLayer) -> None:
        self.layers[layer.name.lower()] = layer

    def get_layer(self, name: str) -> GraphLayer | None:
        return self.layers.get(name.lower())

    def get_or_create_layer(
        self,
        name: str,
        layer_type: LayerType = LayerType.INSTANCE,
        priority: int = 10,
        schema: dict[str, Any] | None = None,
    ) -> GraphLayer:
        layer = self.get_layer(name)
        if not layer:
            layer = GraphLayer(name=name.lower(), layer_type=layer_type, priority=priority, schema=schema or {})
            self.register_layer(layer)
        return layer

    def add_cross_layer_relation(self, relation: LayerRelation) -> None:
        self.cross_layer_relations.append(relation)

    def add_cross_layer_edge(
        self,
        source_layer: str,
        source_vertex_id: str,
        target_layer: str,
        target_vertex_id: str,
        relation_kind: RelationKind | str = RelationKind.MAPS_TO,
        properties: dict[str, Any] | None = None,
    ) -> LayerRelation:
        rel_type = relation_kind.value if isinstance(relation_kind, RelationKind) else str(relation_kind)
        rel = LayerRelation(
            relation_type=rel_type,
            source_layer=source_layer,
            source_id=source_vertex_id,
            target_layer=target_layer,
            target_id=target_vertex_id,
            properties=properties or {},
        )
        self.add_cross_layer_relation(rel)
        return rel


    def cross_layer_query(
        self,
        source_layer_name: str,
        target_layer_name: str,
        relation_type: str | None = None,
        source_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Query relations spanning between two distinct layers."""
        src = source_layer_name.lower()
        tgt = target_layer_name.lower()
        results = []

        for rel in self.cross_layer_relations:
            if rel.source_layer.lower() != src or rel.target_layer.lower() != tgt:
                continue
            if relation_type and rel.relation_type != relation_type:
                continue
            if source_id and rel.source_id != source_id:
                continue

            # Fetch source and target vertex details if available
            s_layer = self.get_layer(src)
            t_layer = self.get_layer(tgt)

            s_v = s_layer.store.get_vertex_by_canonical_id(rel.source_id) if s_layer else None
            t_v = t_layer.store.get_vertex_by_canonical_id(rel.target_id) if t_layer else None

            results.append({
                "relation": rel.to_dict(),
                "source_vertex": s_v,
                "target_vertex": t_v,
            })
        return results

    def project(self, layer_names: list[str]) -> MemoryGraphStore:
        """Create a combined projection store spanning specified layers sorted by priority."""
        projected = MemoryGraphStore()
        selected = [self.layers[n.lower()] for n in layer_names if n.lower() in self.layers]
        selected.sort(key=lambda x: x.priority)

        for l in selected:
            # Copy vertices
            for v in l.store.find_vertices():
                v_copy = dict(v)
                v_copy["properties"] = dict(v_copy.get("properties", {}))
                v_copy["properties"]["_origin_layer"] = l.name
                projected.upsert_vertex(v_copy["label"], v_copy["properties"])

            # Copy edges
            for e in l.store.find_edges():
                e_copy = dict(e)
                e_props = dict(e_copy.get("properties", {}))
                e_props["_origin_layer"] = l.name
                projected.upsert_edge(e_copy["label"], e_copy["out_v"], e_copy["in_v"], e_props)

        return projected

    def diff_layers(self, layer_name_a: str, layer_name_b: str) -> dict[str, Any]:
        """Compute structural difference between two layers (added/removed/modified vertices)."""
        la = self.get_layer(layer_name_a)
        lb = self.get_layer(layer_name_b)
        if not la or not lb:
            raise KeyError(f"One or both layers not found: {layer_name_a}, {layer_name_b}")

        cids_a = {v["canonical_id"]: v for v in la.store.find_vertices()}
        cids_b = {v["canonical_id"]: v for v in lb.store.find_vertices()}

        only_in_a = [cids_a[k] for k in set(cids_a) - set(cids_b)]
        only_in_b = [cids_b[k] for k in set(cids_b) - set(cids_a)]

        modified = []
        for cid in set(cids_a).intersection(set(cids_b)):
            va = cids_a[cid]
            vb = cids_b[cid]
            if va.get("properties") != vb.get("properties"):
                modified.append({"canonical_id": cid, "before": va, "after": vb})

        return {
            "only_in_first": only_in_a,
            "only_in_second": only_in_b,
            "modified": modified,
            "count_a": len(cids_a),
            "count_b": len(cids_b),
        }

    def propagate_constraints(
        self,
        compliance_layer_name: str,
        instance_layer_name: str,
    ) -> list[dict[str, Any]]:
        """Evaluate constraint rules defined in compliance layer against instances."""
        comp = self.get_layer(compliance_layer_name)
        inst = self.get_layer(instance_layer_name)
        if not comp or not inst:
            return []

        violations = []
        # Find constraint vertices
        constraints = comp.store.find_vertices(label="ConstraintRule")
        instances = inst.store.find_vertices()

        for c in constraints:
            props = c.get("properties", {})
            req_prop = props.get("required_property")
            target_label = props.get("target_label")

            for item in instances:
                if target_label and item.get("label") != target_label:
                    continue
                item_props = item.get("properties", {})
                if req_prop and req_prop not in item_props:
                    violations.append({
                        "constraint_id": c.get("canonical_id"),
                        "instance_id": item.get("canonical_id"),
                        "violation": f"Missing required property '{req_prop}'",
                        "severity": props.get("severity", "HIGH"),
                    })

        return violations

    def plan_layer_query(self, query: str) -> list[str]:
        """Determine which layers should be activated for a query."""
        active = ["instance"]
        q_lower = query.lower()

        if any(w in q_lower for w in ["comply", "gdpr", "hipaa", "sox", "violation", "constraint"]):
            active.append("compliance")
        if any(w in q_lower for w in ["ontology", "concept", "hierarchy", "isa", "subclass"]):
            active.append("ontology")
        if any(w in q_lower for w in ["history", "temporal", "evolution", "was", "earlier", "since"]):
            active.append("temporal")
        if any(w in q_lower for w in ["security", "clearance", "acl", "permission"]):
            active.append("security")
        if any(w in q_lower for w in ["provenance", "lineage", "source"]):
            active.append("provenance")

        return active


def get_graph_graph_engine() -> GraphOverGraphEngine:
    return GraphOverGraphEngine.get_instance()
