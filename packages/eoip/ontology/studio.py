"""Visual Ontology Studio builder (GAP-NOCODE).

Drag-and-drop ontology builder for non-technical and technical users.
Supports three user experience modes:
- NOVICE: Simple business entities and links without technical types
- ANALYST: Attribute types, domain tags, basic cardinalities
- EXPERT: Full constraints, inverse relations, temporal properties, inheritance
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class StudioMode(str, Enum):
    NOVICE = "NOVICE"
    ANALYST = "ANALYST"
    EXPERT = "EXPERT"


@dataclass
class StudioProperty:
    name: str
    property_type: str = "TEXT"
    required: bool = False
    description: str = ""


@dataclass
class StudioClassNode:
    id: str
    label: str
    domain: str = "BUSINESS"
    description: str = ""
    properties: list[StudioProperty] = field(default_factory=list)
    position: dict[str, float] = field(default_factory=lambda: {"x": 100.0, "y": 100.0})


@dataclass
class StudioRelationEdge:
    id: str
    label: str
    source_class: str
    target_class: str
    cardinality: str = "1:N"  # 1:1, 1:N, N:M
    description: str = ""


class OntologyStudioProject:
    """A visual ontology studio canvas project (GAP-NOCODE)."""

    def __init__(self, name: str, mode: StudioMode = StudioMode.ANALYST) -> None:
        self.name = name
        self.mode = mode
        self.nodes: dict[str, StudioClassNode] = {}
        self.edges: dict[str, StudioRelationEdge] = {}

    def set_mode(self, mode: StudioMode) -> None:
        self.mode = mode

    def add_class(
        self,
        label: str,
        domain: str = "BUSINESS",
        description: str = "",
        x: float = 0.0,
        y: float = 0.0,
    ) -> StudioClassNode:
        node_id = f"class_{label.lower().replace(' ', '_')}"
        if node_id in self.nodes:
            raise ValueError(f"Class '{label}' already exists in studio canvas")

        node = StudioClassNode(
            id=node_id,
            label=label,
            domain=domain,
            description=description,
            position={"x": x, "y": y},
        )
        self.nodes[node_id] = node
        return node

    def add_property_to_class(
        self,
        class_label: str,
        property_name: str,
        property_type: str = "TEXT",
        required: bool = False,
    ) -> StudioProperty:
        node_id = f"class_{class_label.lower().replace(' ', '_')}"
        node = self.nodes.get(node_id)
        if not node:
            raise KeyError(f"Class '{class_label}' not found")

        # Novice mode defaults to TEXT automatically
        if self.mode == StudioMode.NOVICE:
            property_type = "TEXT"

        prop = StudioProperty(name=property_name, property_type=property_type, required=required)
        node.properties.append(prop)
        return prop

    def add_relationship(
        self,
        relationship_label: str,
        source_class: str,
        target_class: str,
        cardinality: str = "1:N",
    ) -> StudioRelationEdge:
        src_id = f"class_{source_class.lower().replace(' ', '_')}"
        tgt_id = f"class_{target_class.lower().replace(' ', '_')}"
        if src_id not in self.nodes:
            raise KeyError(f"Source class '{source_class}' not found")
        if tgt_id not in self.nodes:
            raise KeyError(f"Target class '{target_class}' not found")

        edge_id = f"edge_{source_class}_{relationship_label}_{target_class}"
        edge = StudioRelationEdge(
            id=edge_id,
            label=relationship_label,
            source_class=source_class,
            target_class=target_class,
            cardinality=cardinality,
        )
        self.edges[edge_id] = edge
        return edge

    def validate(self) -> dict[str, Any]:
        """Validates the studio canvas against ontology consistency rules."""
        errors: list[str] = []
        if not self.nodes:
            errors.append("Canvas requires at least one class node")

        for edge in self.edges.values():
            src_id = f"class_{edge.source_class.lower().replace(' ', '_')}"
            tgt_id = f"class_{edge.target_class.lower().replace(' ', '_')}"
            if src_id not in self.nodes or tgt_id not in self.nodes:
                errors.append(f"Edge {edge.label} references nonexistent classes")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "class_count": len(self.nodes),
            "relationship_count": len(self.edges),
            "mode": self.mode.value,
        }

    def export_schema(self) -> dict[str, Any]:
        """Exports studio project into standard ontology schema format."""
        validation = self.validate()
        if not validation["valid"]:
            raise ValueError(f"Cannot export invalid studio project: {validation['errors']}")

        classes_export: dict[str, Any] = {}
        for node in self.nodes.values():
            classes_export[node.label] = {
                "domain": node.domain,
                "description": node.description,
                "properties": {p.name: p.property_type for p in node.properties},
            }

        relationships_export: dict[str, Any] = {}
        for edge in self.edges.values():
            relationships_export[edge.label] = {
                "source": edge.source_class,
                "target": edge.target_class,
                "cardinality": edge.cardinality,
            }

        return {
            "name": self.name,
            "mode": self.mode.value,
            "classes": classes_export,
            "relationships": relationships_export,
        }
