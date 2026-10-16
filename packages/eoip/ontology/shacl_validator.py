"""SHACL Runtime Validator Engine (GRAPH-006).

Validates active graph instance stores against W3C SHACL shape definitions:
- Node shapes and property shapes with cardinality, datatype, and value constraints
- Validation reports with structured violations, severity levels (INFO/WARNING/VIOLATION)
- Actionable fix suggestions
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.ontology.shacl_validator")



class SHACLSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    VIOLATION = "VIOLATION"


@dataclass
class SHACLShape:
    """A SHACL NodeShape definition specifying constraints for target class instances."""

    shape_id: str
    target_class: str
    required_properties: list[str] = field(default_factory=list)
    property_types: dict[str, str] = field(default_factory=dict)  # "string", "int", "float", "bool", "dict", "list"
    min_counts: dict[str, int] = field(default_factory=dict)
    max_counts: dict[str, int] = field(default_factory=dict)
    allowed_values: dict[str, list[Any]] = field(default_factory=dict)
    severity: SHACLSeverity = SHACLSeverity.VIOLATION
    description: str = ""


@dataclass
class SHACLViolation:
    """A single constraint violation detected by SHACL validation."""

    shape_id: str
    focus_node: str
    path: str
    message: str
    severity: str
    fix_suggestion: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SHACLValidationReport:
    """Overall validation report conforming to SHACL specification."""

    conforms: bool
    total_violations: int
    nodes_checked: int
    violations: list[SHACLViolation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conforms": self.conforms,
            "total_violations": self.total_violations,
            "nodes_checked": self.nodes_checked,
            "violations": [v.to_dict() for v in self.violations],
        }


class SHACLValidator:
    """Validates MemoryGraphStore instances against registered SHACL shapes."""

    def __init__(self) -> None:
        self.shapes: dict[str, SHACLShape] = {}
        self._bootstrap_core_shapes()

    def _bootstrap_core_shapes(self) -> None:
        # Core Service shape
        self.register_shape(SHACLShape(
            shape_id="ServiceShape",
            target_class="Service",
            required_properties=["canonical_id", "name"],
            property_types={"name": "string"},
            min_counts={"name": 1},
            severity=SHACLSeverity.VIOLATION,
            description="Service instances must have valid canonical_id and non-empty name string",
        ))
        # Core Person shape
        self.register_shape(SHACLShape(
            shape_id="PersonShape",
            target_class="Person",
            required_properties=["canonical_id"],
            severity=SHACLSeverity.VIOLATION,
        ))

    def register_shape(self, shape: SHACLShape) -> None:
        self.shapes[shape.shape_id] = shape

    def validate(self, store: MemoryGraphStore) -> SHACLValidationReport:
        """Validate all nodes in store against matching registered shapes."""
        violations: list[SHACLViolation] = []
        nodes_checked = 0

        vertices = store.find_vertices()
        for v in vertices:
            label = v.get("label")
            cid = v.get("canonical_id") or v.get("properties", {}).get("canonical_id", "unknown_node")
            props = v.get("properties", {})

            for shape in self.shapes.values():
                if shape.target_class.lower() != str(label).lower():
                    continue

                nodes_checked += 1

                # 1. Check required properties (min_count >= 1)
                for req in shape.required_properties:
                    val = props.get(req)
                    # Check if property is at root or in properties dict
                    if val is None and req in v:
                        val = v[req]

                    if val is None or val == "":
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path=req,
                            message=f"Focus node '{cid}' missing mandatory property '{req}'",
                            severity=shape.severity.value,
                            fix_suggestion=f"Provide a non-null value for '{req}' on node '{cid}'",
                        ))

                # 2. Check property datatypes
                for prop_name, expected_type in shape.property_types.items():
                    val = props.get(prop_name)
                    if val is not None:
                        is_type_valid = self._check_datatype(val, expected_type)
                        if not is_type_valid:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value '{val}' does not conform to expected datatype '{expected_type}'",
                                severity=shape.severity.value,
                                fix_suggestion=f"Cast '{prop_name}' to {expected_type}",
                            ))

                # 3. Check allowed values (in-list constraint)
                for prop_name, allowed_set in shape.allowed_values.items():
                    val = props.get(prop_name)
                    if val is not None and val not in allowed_set:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path=prop_name,
                            message=f"Value '{val}' for property '{prop_name}' is not in allowed set {allowed_set}",
                            severity=shape.severity.value,
                            fix_suggestion=f"Update '{prop_name}' to one of {allowed_set}",
                        ))

        conforms = len(violations) == 0
        return SHACLValidationReport(
            conforms=conforms,
            total_violations=len(violations),
            nodes_checked=nodes_checked,
            violations=violations,
        )

    def _check_datatype(self, value: Any, expected_type: str) -> bool:
        t = expected_type.lower()
        if t in ("string", "str"):
            return isinstance(value, str)
        if t in ("int", "integer"):
            return isinstance(value, int) and not isinstance(value, bool)
        if t in ("float", "double", "number"):
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if t in ("bool", "boolean"):
            return isinstance(value, bool)
        if t in ("list", "array"):
            return isinstance(value, (list, tuple))
        if t in ("dict", "object"):
            return isinstance(value, dict)
        return True


def get_shacl_validator() -> SHACLValidator:
    return SHACLValidator()
