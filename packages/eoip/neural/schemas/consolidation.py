"""
Unstructured Stream Schema Induction & Episodic-to-Semantic Consolidation (NS-P3, T-NS-006).
Induces candidate Neural Schemas from observation streams and synthesizes SHACL shape constraints.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from packages.eoip.neural.schemas.models import NeuralSchema, SlotConstraint


@dataclass
class SHACLShape:
    target_class: str
    property_shapes: List[Dict[str, Any]] = field(default_factory=list)

    def to_shacl_turtle(self) -> str:
        lines = [f":{self.target_class}Shape a sh:NodeShape ;", f"  sh:targetClass :{self.target_class} ;"]
        for p in self.property_shapes:
            lines.append("  sh:property [")
            lines.append(f"    sh:path :{p['path']} ;")
            lines.append(f"    sh:datatype xsd:{p.get('datatype', 'string')} ;")
            if p.get("minCount", 0) > 0:
                lines.append(f"    sh:minCount {p['minCount']} ;")
            lines.append("  ] ;")
        lines.append("  .")
        return "\n".join(lines)


class SchemaInductionEngine:
    """
    Consolidates episodic instance streams into semantic schema archetypes.
    """

    def __init__(self, min_support_ratio: float = 0.70) -> None:
        self.min_support_ratio = min_support_ratio

    def induce_schema_from_instances(
        self,
        schema_name: str,
        domain: str,
        instances: List[Dict[str, Any]],
    ) -> NeuralSchema:
        """
        Analyzes a batch of observation instances to infer slot constraints and types.
        """
        if not instances:
            return NeuralSchema.create(name=schema_name, domain=domain, slots={})

        total = len(instances)
        property_counts: Dict[str, int] = {}
        property_types: Dict[str, Set[str]] = {}

        for inst in instances:
            for k, v in inst.items():
                property_counts[k] = property_counts.get(k, 0) + 1
                py_type = type(v).__name__
                property_types.setdefault(k, set()).add(py_type)

        slots: Dict[str, SlotConstraint] = {}
        for prop, count in property_counts.items():
            support = count / total
            is_required = support >= self.min_support_ratio
            allowed = sorted(list(property_types.get(prop, {"str"})))
            slots[prop] = SlotConstraint(
                name=prop,
                required=is_required,
                allowed_types=allowed,
                epistemic_default="inferred",
            )

        return NeuralSchema.create(
            name=schema_name,
            domain=domain,
            slots=slots,
        )

    def synthesize_shacl_shape(self, schema: NeuralSchema) -> SHACLShape:
        """
        Translates a NeuralSchema into standard W3C SHACL shape constraints.
        """
        props = []
        for name, constraint in schema.slots.items():
            shacl_type = "string"
            if "int" in constraint.allowed_types:
                shacl_type = "integer"
            elif "float" in constraint.allowed_types:
                shacl_type = "decimal"
            elif "bool" in constraint.allowed_types:
                shacl_type = "boolean"

            props.append({
                "path": name,
                "datatype": shacl_type,
                "minCount": 1 if constraint.required else 0,
            })

        return SHACLShape(target_class=schema.name, property_shapes=props)
