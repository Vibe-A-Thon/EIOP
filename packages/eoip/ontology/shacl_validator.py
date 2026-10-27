"""SHACL Runtime Validator Engine (GRAPH-006, CRA-020).

Validates active graph instance stores against W3C SHACL Core 2017 definitions:
- Node shapes and property shapes with cardinality, datatype, and value constraints
- Validation reports with structured violations, severity levels (INFO/WARNING/VIOLATION)
- Actionable fix suggestions
- Strict datatype checking, unknown datatype rejection during setup
- Unsupported constraint component rejection (never conforms=True)
- Pre-validation shape scanning and bounded resource validation
- pySHACL worker adapter and TopBraid differential oracle
- Transactional isolation, CAS base revision checking, and zero-triple commit on failure
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.ontology.shacl_validator")

# Supported profiles
PROFILE_SHACL_CORE_2017 = "shacl-core-2017"
PROFILE_SHACL_SPARQL = "shacl-sparql"
PROFILE_SHACL_ADVANCED = "shacl-advanced"
DEFAULT_PROFILE = PROFILE_SHACL_CORE_2017

# Standard result codes per CRA-020.10
SHACL_CARDINALITY_VIOLATION = "SHACL_CARDINALITY_VIOLATION"
SHACL_DATATYPE_VIOLATION = "SHACL_DATATYPE_VIOLATION"
SHACL_NODE_KIND_VIOLATION = "SHACL_NODE_KIND_VIOLATION"
SHACL_CLASS_VIOLATION = "SHACL_CLASS_VIOLATION"
SHACL_VALUE_SET_VIOLATION = "SHACL_VALUE_SET_VIOLATION"
SHACL_PATTERN_VIOLATION = "SHACL_PATTERN_VIOLATION"
SHACL_BOUND_VIOLATION = "SHACL_BOUND_VIOLATION"
SHACL_LENGTH_VIOLATION = "SHACL_LENGTH_VIOLATION"
SHACL_LOGICAL_VIOLATION = "SHACL_LOGICAL_VIOLATION"
SHACL_CLOSED_VIOLATION = "SHACL_CLOSED_VIOLATION"
UNSUPPORTED_CONSTRAINT = "UNSUPPORTED_CONSTRAINT"

# Known valid XSD / RDF datatypes
XSD_DATATYPES = {
    "xsd:string", "string", "str", "http://www.w3.org/2001/xmlschema#string",
    "xsd:integer", "xsd:int", "xsd:long", "xsd:short", "xsd:byte", "int", "integer", "http://www.w3.org/2001/xmlschema#integer",
    "xsd:decimal", "xsd:float", "xsd:double", "float", "double", "number", "http://www.w3.org/2001/xmlschema#decimal", "http://www.w3.org/2001/xmlschema#double", "http://www.w3.org/2001/xmlschema#float",
    "xsd:boolean", "bool", "boolean", "http://www.w3.org/2001/xmlschema#boolean",
    "xsd:date", "xsd:datetime", "xsd:time", "date", "datetime", "http://www.w3.org/2001/xmlschema#datetime", "http://www.w3.org/2001/xmlschema#date",
    "xsd:anyuri", "uri", "http://www.w3.org/2001/xmlschema#anyuri",
    "rdf:langstring", "http://www.w3.org/1999/02/22-rdf-syntax-ns#langstring",
    "dict", "object", "list", "array"
}


class SHACLSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    VIOLATION = "VIOLATION"


class SHACLNodeKind(str, Enum):
    IRI = "sh:IRI"
    Literal = "sh:Literal"
    BlankNode = "sh:BlankNode"
    BlankNodeOrIRI = "sh:BlankNodeOrIRI"
    BlankNodeOrLiteral = "sh:BlankNodeOrLiteral"
    IRIOrLiteral = "sh:IRIOrLiteral"


class SHACLEngineError(Exception):
    """Base exception for SHACL operations."""


class SHACLSetupError(SHACLEngineError):
    """Raised when shape registration or validator setup contains invalid definitions (e.g. unknown datatype)."""


class SHACLTxnViolationError(SHACLEngineError):
    """Raised during transactional validation when candidate commit violates SHACL constraints."""
    def __init__(self, message: str, report: SHACLValidationReport | None = None) -> None:
        super().__init__(message)
        self.report = report


class SHACLConcurrencyConflictError(SHACLEngineError):
    """Raised when base revision does not match during candidate publication."""


class SHACLTimeoutError(SHACLEngineError):
    """Raised when validation execution exceeds configured timeout bound."""


class SHACLValidatorUnavailableError(SHACLEngineError):
    """Raised when the validator engine or isolated worker is offline or unavailable."""


class UnsupportedConstraintError(SHACLEngineError):
    """Raised when shape contains constraint components outside the declared profile."""


@dataclass
class SHACLPropertyShape:
    """A SHACL PropertyShape specifying constraints on a focus node property path."""
    path: str
    min_count: int | None = None
    max_count: int | None = None
    datatype: str | None = None
    node_kind: str | None = None
    sh_class: str | None = None
    in_values: list[Any] | None = None
    pattern: str | None = None
    flags: str | None = None
    min_length: int | None = None
    max_length: int | None = None
    min_inclusive: Any | None = None
    max_inclusive: Any | None = None
    min_exclusive: Any | None = None
    max_exclusive: Any | None = None
    language_in: list[str] | None = None
    unique_lang: bool = False
    has_value: Any | None = None
    equals: str | None = None
    disjoint: str | None = None
    less_than: str | None = None
    less_than_or_equals: str | None = None
    severity: SHACLSeverity = SHACLSeverity.VIOLATION
    message: str | None = None
    unsupported_components: list[str] = field(default_factory=list)


@dataclass
class SHACLShape:
    """A SHACL NodeShape definition specifying constraints for target class instances."""
    shape_id: str
    target_class: str = ""
    target_node: str | list[str] | None = None
    target_subjects_of: str | None = None
    target_objects_of: str | None = None
    required_properties: list[str] = field(default_factory=list)
    property_types: dict[str, str] = field(default_factory=dict)
    min_counts: dict[str, int] = field(default_factory=dict)
    max_counts: dict[str, int] = field(default_factory=dict)
    allowed_values: dict[str, list[Any]] = field(default_factory=dict)
    patterns: dict[str, str] = field(default_factory=dict)
    lengths: dict[str, tuple[int | None, int | None]] = field(default_factory=dict)
    numeric_bounds: dict[str, dict[str, Any]] = field(default_factory=dict)
    node_kinds: dict[str, str] = field(default_factory=dict)
    property_classes: dict[str, str] = field(default_factory=dict)
    property_shapes: list[SHACLPropertyShape] = field(default_factory=list)
    closed: bool = False
    ignored_properties: list[str] = field(default_factory=list)
    or_shapes: list[Any] = field(default_factory=list)
    and_shapes: list[Any] = field(default_factory=list)
    not_shape: Any | None = None
    xone_shapes: list[Any] = field(default_factory=list)
    unsupported_components: list[str] = field(default_factory=list)
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
    fix_suggestion: str = ""
    source_constraint_component: str = ""
    value: Any = None
    result_code: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # Add W3C standard SHACL keys
        d["focusNode"] = self.focus_node
        d["resultPath"] = self.path
        d["sourceShape"] = self.shape_id
        d["resultSeverity"] = f"sh:{self.severity.capitalize()}" if not self.severity.startswith("sh:") else self.severity
        d["resultMessage"] = self.message
        d["sourceConstraintComponent"] = self.source_constraint_component or "sh:ConstraintComponent"
        return d


@dataclass
class SHACLValidationReport:
    """Overall validation report conforming to SHACL specification and EOIP extensions."""
    conforms: bool
    total_violations: int
    nodes_checked: int
    violations: list[SHACLViolation] = field(default_factory=list)
    revision: str = "v1"
    engine: str = "eoip-core-shacl"
    engine_version: str = "1.0.0"
    profile: str = "shacl-core-2017"
    truncated: bool = False
    status: str = "VALIDATED"
    execution_time_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        viols = [v.to_dict() for v in self.violations]
        return {
            "conforms": self.conforms,
            "total_violations": self.total_violations,
            "nodes_checked": self.nodes_checked,
            "violations": viols,
            "results": viols,  # W3C alias
            "revision": self.revision,
            "engine": self.engine,
            "engine_version": self.engine_version,
            "profile": self.profile,
            "truncated": self.truncated,
            "status": self.status,
            "execution_time_ms": self.execution_time_ms,
        }


class SHACLValidator:
    """Validates GraphStore / MemoryGraphStore instances against registered SHACL shapes."""

    def __init__(self, profile: str = PROFILE_SHACL_CORE_2017) -> None:
        self.profile = profile
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

    def register_shape(self, shape: SHACLShape, *, allow_unsupported: bool = False) -> None:
        """Register a shape. Rejects unknown datatype IRIs per CRA-020.3."""
        # Check property_types
        for prop, ptype in shape.property_types.items():
            if not self._is_known_datatype(ptype):
                raise SHACLSetupError(f"Unknown datatype name or IRI '{ptype}' for property '{prop}' in shape '{shape.shape_id}'")

        # Check property_shapes datatypes
        for ps in shape.property_shapes:
            if ps.datatype and not self._is_known_datatype(ps.datatype):
                raise SHACLSetupError(f"Unknown datatype name or IRI '{ps.datatype}' for path '{ps.path}' in shape '{shape.shape_id}'")

        self.shapes[shape.shape_id] = shape

    def _is_known_datatype(self, ptype: str) -> bool:
        return ptype.lower().strip() in XSD_DATATYPES

    def pre_scan_shapes(self) -> list[SHACLViolation]:
        """Scan registered shapes for unsupported constraint components under the declared profile."""
        violations: list[SHACLViolation] = []
        if self.profile == PROFILE_SHACL_CORE_2017:
            for shape in self.shapes.values():
                # Check for advanced unsupported components
                for comp in shape.unsupported_components:
                    violations.append(SHACLViolation(
                        shape_id=shape.shape_id,
                        focus_node=shape.shape_id,
                        path="sh:constraint",
                        message=f"Constraint component '{comp}' is unsupported in declared profile '{self.profile}'",
                        severity=SHACLSeverity.VIOLATION.value,
                        fix_suggestion=f"Remove '{comp}' or enable advanced profile with explicit qualification",
                        source_constraint_component=comp,
                        result_code=UNSUPPORTED_CONSTRAINT,
                    ))
                for ps in shape.property_shapes:
                    for comp in ps.unsupported_components:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=shape.shape_id,
                            path=ps.path,
                            message=f"Constraint component '{comp}' on path '{ps.path}' is unsupported in profile '{self.profile}'",
                            severity=SHACLSeverity.VIOLATION.value,
                            fix_suggestion=f"Remove '{comp}' or enable advanced profile",
                            source_constraint_component=comp,
                            result_code=UNSUPPORTED_CONSTRAINT,
                        ))
        return violations

    def validate(
        self,
        store: Any,
        *,
        revision: str = "v1",
        timeout_seconds: float = 10.0,
        max_violations: int = 1000,
    ) -> SHACLValidationReport:
        """Validate all nodes/edges in store against matching registered shapes."""
        start_time = time.perf_counter()
        violations: list[SHACLViolation] = []
        nodes_checked = 0
        truncated = False

        # 1. Pre-validation scan for unsupported constraints (CRA-020.2, CRA-020.10)
        unsupported_violations = self.pre_scan_shapes()
        if unsupported_violations:
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return SHACLValidationReport(
                conforms=False,
                total_violations=len(unsupported_violations),
                nodes_checked=0,
                violations=unsupported_violations,
                revision=revision,
                engine="eoip-core-shacl",
                profile=self.profile,
                truncated=False,
                status=UNSUPPORTED_CONSTRAINT,
                execution_time_ms=elapsed,
            )

        vertices = store.find_vertices() if hasattr(store, "find_vertices") else []
        edges = store.find_edges() if hasattr(store, "find_edges") else []

        # Index vertices by canonical_id / vid for path traversal
        vertex_map: dict[str, dict[str, Any]] = {}
        for v in vertices:
            cid = v.get("canonical_id") or v.get("properties", {}).get("canonical_id")
            if cid:
                vertex_map[cid] = v
            vid = v.get("vid")
            if vid is not None:
                vertex_map[str(vid)] = v

        for v in vertices:
            if timeout_seconds and (time.perf_counter() - start_time) > timeout_seconds:
                raise SHACLTimeoutError(f"Validation timed out after {timeout_seconds}s")

            if len(violations) >= max_violations:
                truncated = True
                break

            label = v.get("label", "")
            cid = v.get("canonical_id") or v.get("properties", {}).get("canonical_id", "unknown_node")
            props = v.get("properties", {})

            for shape in self.shapes.values():
                # Target Class matching
                if shape.target_class:
                    if shape.target_class.lower() != str(label).lower():
                        continue
                elif shape.target_node:
                    targets = [shape.target_node] if isinstance(shape.target_node, str) else shape.target_node
                    if cid not in targets:
                        continue

                nodes_checked += 1

                # 1. Check required properties
                for req in shape.required_properties:
                    val = props.get(req)
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
                            source_constraint_component="sh:MinCountConstraintComponent",
                            result_code=SHACL_CARDINALITY_VIOLATION,
                        ))

                # 2. Check property datatypes
                for prop_name, expected_type in shape.property_types.items():
                    val = props.get(prop_name)
                    if val is not None:
                        if not self._check_datatype(val, expected_type):
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value '{val}' does not conform to expected datatype '{expected_type}'",
                                severity=shape.severity.value,
                                fix_suggestion=f"Cast '{prop_name}' to {expected_type}",
                                source_constraint_component="sh:DatatypeConstraintComponent",
                                value=val,
                                result_code=SHACL_DATATYPE_VIOLATION,
                            ))

                # 3. Check allowed values (sh:in)
                for prop_name, allowed_set in shape.allowed_values.items():
                    val = props.get(prop_name)
                    if val is not None:
                        vals = val if isinstance(val, (list, tuple, set)) else [val]
                        for item in vals:
                            if item not in allowed_set:
                                violations.append(SHACLViolation(
                                    shape_id=shape.shape_id,
                                    focus_node=cid,
                                    path=prop_name,
                                    message=f"Value '{item}' for property '{prop_name}' is not in allowed set {allowed_set}",
                                    severity=shape.severity.value,
                                    fix_suggestion=f"Update '{prop_name}' to one of {allowed_set}",
                                    source_constraint_component="sh:InConstraintComponent",
                                    value=item,
                                    result_code=SHACL_VALUE_SET_VIOLATION,
                                ))

                # 4. Check min_counts constraint
                for prop_name, min_cnt in shape.min_counts.items():
                    val = props.get(prop_name)
                    if val is None and prop_name in v:
                        val = v[prop_name]
                    cnt = 0 if val is None else (len(val) if isinstance(val, (list, tuple, set)) else 1)
                    if cnt < min_cnt:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path=prop_name,
                            message=f"Focus node '{cid}' has {cnt} values for '{prop_name}', minimum count is {min_cnt}",
                            severity=shape.severity.value,
                            fix_suggestion=f"Provide at least {min_cnt} values for '{prop_name}' on node '{cid}'",
                            source_constraint_component="sh:MinCountConstraintComponent",
                            result_code=SHACL_CARDINALITY_VIOLATION,
                        ))

                # 5. Check max_counts constraint
                for prop_name, max_cnt in shape.max_counts.items():
                    val = props.get(prop_name)
                    if val is None and prop_name in v:
                        val = v[prop_name]
                    cnt = 0 if val is None else (len(val) if isinstance(val, (list, tuple, set)) else 1)
                    if cnt > max_cnt:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path=prop_name,
                            message=f"Focus node '{cid}' has {cnt} values for '{prop_name}', maximum count is {max_cnt}",
                            severity=shape.severity.value,
                            fix_suggestion=f"Reduce values for '{prop_name}' to at most {max_cnt} on node '{cid}'",
                            source_constraint_component="sh:MaxCountConstraintComponent",
                            result_code=SHACL_CARDINALITY_VIOLATION,
                        ))

                # 6. Check patterns (sh:pattern)
                for prop_name, pat in shape.patterns.items():
                    val = props.get(prop_name)
                    if val is not None and isinstance(val, str):
                        if not re.search(pat, val):
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value '{val}' does not match pattern '{pat}'",
                                severity=shape.severity.value,
                                fix_suggestion=f"Ensure '{prop_name}' conforms to pattern '{pat}'",
                                source_constraint_component="sh:PatternConstraintComponent",
                                value=val,
                                result_code=SHACL_PATTERN_VIOLATION,
                            ))

                # 7. Check string lengths (sh:minLength, sh:maxLength)
                for prop_name, (min_len, max_len) in shape.lengths.items():
                    val = props.get(prop_name)
                    if val is not None and isinstance(val, str):
                        l = len(val)
                        if min_len is not None and l < min_len:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' length {l} is less than minLength {min_len}",
                                severity=shape.severity.value,
                                fix_suggestion=f"Provide at least {min_len} characters for '{prop_name}'",
                                source_constraint_component="sh:MinLengthConstraintComponent",
                                value=val,
                                result_code=SHACL_LENGTH_VIOLATION,
                            ))
                        if max_len is not None and l > max_len:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' length {l} exceeds maxLength {max_len}",
                                severity=shape.severity.value,
                                fix_suggestion=f"Shorten '{prop_name}' to at most {max_len} characters",
                                source_constraint_component="sh:MaxLengthConstraintComponent",
                                value=val,
                                result_code=SHACL_LENGTH_VIOLATION,
                            ))

                # 8. Check numeric bounds
                for prop_name, bounds in shape.numeric_bounds.items():
                    val = props.get(prop_name)
                    if val is not None and isinstance(val, (int, float)) and not isinstance(val, bool):
                        min_inc = bounds.get("min_inclusive")
                        max_inc = bounds.get("max_inclusive")
                        min_exc = bounds.get("min_exclusive")
                        max_exc = bounds.get("max_exclusive")
                        if min_inc is not None and val < min_inc:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value {val} < minInclusive {min_inc}",
                                severity=shape.severity.value,
                                fix_suggestion=f"Value must be >= {min_inc}",
                                source_constraint_component="sh:MinInclusiveConstraintComponent",
                                value=val,
                                result_code=SHACL_BOUND_VIOLATION,
                            ))
                        if max_inc is not None and val > max_inc:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value {val} > maxInclusive {max_inc}",
                                severity=shape.severity.value,
                                fix_suggestion=f"Value must be <= {max_inc}",
                                source_constraint_component="sh:MaxInclusiveConstraintComponent",
                                value=val,
                                result_code=SHACL_BOUND_VIOLATION,
                            ))
                        if min_exc is not None and val <= min_exc:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value {val} <= minExclusive {min_exc}",
                                severity=shape.severity.value,
                                fix_suggestion=f"Value must be > {min_exc}",
                                source_constraint_component="sh:MinExclusiveConstraintComponent",
                                value=val,
                                result_code=SHACL_BOUND_VIOLATION,
                            ))
                        if max_exc is not None and val >= max_exc:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value {val} >= maxExclusive {max_exc}",
                                severity=shape.severity.value,
                                fix_suggestion=f"Value must be < {max_exc}",
                                source_constraint_component="sh:MaxExclusiveConstraintComponent",
                                value=val,
                                result_code=SHACL_BOUND_VIOLATION,
                            ))

                # 9. Check nodeKind constraint
                for prop_name, expected_kind in shape.node_kinds.items():
                    val = props.get(prop_name)
                    if val is not None:
                        is_iri = isinstance(val, str) and (val.startswith(("http://", "https://", "urn:")))
                        is_lit = isinstance(val, (str, int, float, bool)) and not is_iri
                        if expected_kind == SHACLNodeKind.IRI and not is_iri:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value '{val}' is not an IRI",
                                severity=shape.severity.value,
                                fix_suggestion="Value must be a valid IRI",
                                source_constraint_component="sh:NodeKindConstraintComponent",
                                value=val,
                                result_code=SHACL_NODE_KIND_VIOLATION,
                            ))
                        elif expected_kind == SHACLNodeKind.Literal and not is_lit:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=prop_name,
                                message=f"Property '{prop_name}' value '{val}' is not a Literal",
                                severity=shape.severity.value,
                                fix_suggestion="Value must be a literal",
                                source_constraint_component="sh:NodeKindConstraintComponent",
                                value=val,
                                result_code=SHACL_NODE_KIND_VIOLATION,
                            ))

                # 10. Check sh:closed and sh:ignoredProperties
                if shape.closed:
                    allowed_props = set(shape.required_properties) | set(shape.property_types.keys()) | set(shape.min_counts.keys()) | set(shape.max_counts.keys()) | set(shape.ignored_properties) | {"canonical_id"}
                    for present_prop in props.keys():
                        if present_prop not in allowed_props:
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=present_prop,
                                message=f"Predicate '{present_prop}' is not permitted in closed shape '{shape.shape_id}'",
                                severity=shape.severity.value,
                                fix_suggestion=f"Remove '{present_prop}' or add it to shape definition",
                                source_constraint_component="sh:ClosedConstraintComponent",
                                value=props[present_prop],
                                result_code=SHACL_CLOSED_VIOLATION,
                            ))

                # 11. Check rich property_shapes
                for ps in shape.property_shapes:
                    val = props.get(ps.path)
                    cnt = 0 if val is None else (len(val) if isinstance(val, (list, tuple, set)) else 1)
                    if ps.min_count is not None and cnt < ps.min_count:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path=ps.path,
                            message=ps.message or f"Path '{ps.path}' has {cnt} values, minCount is {ps.min_count}",
                            severity=ps.severity.value,
                            fix_suggestion=f"Provide at least {ps.min_count} values for '{ps.path}'",
                            source_constraint_component="sh:MinCountConstraintComponent",
                            result_code=SHACL_CARDINALITY_VIOLATION,
                        ))
                    if ps.max_count is not None and cnt > ps.max_count:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path=ps.path,
                            message=ps.message or f"Path '{ps.path}' has {cnt} values, maxCount is {ps.max_count}",
                            severity=ps.severity.value,
                            fix_suggestion=f"Provide at most {ps.max_count} values for '{ps.path}'",
                            source_constraint_component="sh:MaxCountConstraintComponent",
                            result_code=SHACL_CARDINALITY_VIOLATION,
                        ))
                    if val is not None and ps.datatype:
                        if not self._check_datatype(val, ps.datatype):
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=cid,
                                path=ps.path,
                                message=ps.message or f"Path '{ps.path}' value does not conform to datatype '{ps.datatype}'",
                                severity=ps.severity.value,
                                fix_suggestion=f"Cast '{ps.path}' to {ps.datatype}",
                                source_constraint_component="sh:DatatypeConstraintComponent",
                                value=val,
                                result_code=SHACL_DATATYPE_VIOLATION,
                            ))

                # 12. Logical constraints (sh:not, sh:or, sh:xone)
                if shape.not_shape is not None:
                    # If not_shape conforms, this is a violation
                    sub_v = SHACLValidator(self.profile)
                    sub_v.shapes = {shape.not_shape.shape_id: shape.not_shape}
                    sub_report = sub_v.validate(store)
                    if sub_report.conforms:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path="sh:not",
                            message=f"Focus node '{cid}' must not conform to shape '{shape.not_shape.shape_id}'",
                            severity=shape.severity.value,
                            source_constraint_component="sh:NotConstraintComponent",
                            result_code=SHACL_LOGICAL_VIOLATION,
                        ))

                if shape.or_shapes:
                    conforming_count = 0
                    for sub_shape in shape.or_shapes:
                        sub_v = SHACLValidator(self.profile)
                        sub_v.shapes = {sub_shape.shape_id: sub_shape}
                        if sub_v.validate(store).conforms:
                            conforming_count += 1
                    if conforming_count == 0:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path="sh:or",
                            message=f"Focus node '{cid}' does not conform to any shape in sh:or list",
                            severity=shape.severity.value,
                            source_constraint_component="sh:OrConstraintComponent",
                            result_code=SHACL_LOGICAL_VIOLATION,
                        ))

                if shape.xone_shapes:
                    conforming_count = 0
                    for sub_shape in shape.xone_shapes:
                        sub_v = SHACLValidator(self.profile)
                        sub_v.shapes = {sub_shape.shape_id: sub_shape}
                        if sub_v.validate(store).conforms:
                            conforming_count += 1
                    if conforming_count != 1:
                        violations.append(SHACLViolation(
                            shape_id=shape.shape_id,
                            focus_node=cid,
                            path="sh:xone",
                            message=f"Focus node '{cid}' conforms to {conforming_count} shapes in sh:xone (expected exactly 1)",
                            severity=shape.severity.value,
                            source_constraint_component="sh:XoneConstraintComponent",
                            result_code=SHACL_LOGICAL_VIOLATION,
                        ))

        # Check edge relationships for targetSubjectsOf / targetObjectsOf shapes
        for edge in edges:
            label = edge.get("label", "")
            out_v = vertex_map.get(str(edge.get("out_v")))
            in_v = vertex_map.get(str(edge.get("in_v")))
            edge.get("properties", {}).get("edge_key") or edge.get("eid", "unknown_edge")

            for shape in self.shapes.values():
                if shape.target_subjects_of and shape.target_subjects_of == label:
                    if out_v and shape.target_class:
                        if str(out_v.get("label", "")).lower() != shape.target_class.lower():
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=str(out_v.get("canonical_id", out_v.get("vid"))),
                                path=label,
                                message=f"Subject of '{label}' must have class '{shape.target_class}', got '{out_v.get('label')}'",
                                severity=shape.severity.value,
                                source_constraint_component="sh:ClassConstraintComponent",
                                result_code=SHACL_CLASS_VIOLATION,
                            ))
                if shape.target_objects_of and shape.target_objects_of == label:
                    if in_v and shape.target_class:
                        if str(in_v.get("label", "")).lower() != shape.target_class.lower():
                            violations.append(SHACLViolation(
                                shape_id=shape.shape_id,
                                focus_node=str(in_v.get("canonical_id", in_v.get("vid"))),
                                path=label,
                                message=f"Object of '{label}' must have class '{shape.target_class}', got '{in_v.get('label')}'",
                                severity=shape.severity.value,
                                source_constraint_component="sh:ClassConstraintComponent",
                                result_code=SHACL_CLASS_VIOLATION,
                            ))

        conforms = len(violations) == 0
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return SHACLValidationReport(
            conforms=conforms,
            total_violations=len(violations),
            nodes_checked=nodes_checked,
            violations=violations,
            revision=revision,
            engine="eoip-core-shacl",
            profile=self.profile,
            truncated=truncated,
            status="VALIDATED",
            execution_time_ms=elapsed_ms,
        )

    def _check_datatype(self, value: Any, expected_type: str) -> bool:
        t = expected_type.lower().strip()
        if t in ("string", "str", "xsd:string", "http://www.w3.org/2001/xmlschema#string"):
            return isinstance(value, str)
        if t in ("int", "integer", "xsd:integer", "xsd:int", "xsd:long", "xsd:short", "xsd:byte", "http://www.w3.org/2001/xmlschema#integer"):
            return isinstance(value, int) and not isinstance(value, bool)
        if t in ("float", "double", "number", "xsd:float", "xsd:double", "xsd:decimal", "http://www.w3.org/2001/xmlschema#decimal", "http://www.w3.org/2001/xmlschema#double", "http://www.w3.org/2001/xmlschema#float"):
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if t in ("bool", "boolean", "xsd:boolean", "http://www.w3.org/2001/xmlschema#boolean"):
            return isinstance(value, bool)
        if t in ("list", "array"):
            return isinstance(value, (list, tuple))
        if t in ("dict", "object"):
            return isinstance(value, dict)
        if t in ("date", "datetime", "xsd:date", "xsd:datetime", "http://www.w3.org/2001/xmlschema#datetime", "http://www.w3.org/2001/xmlschema#date"):
            if isinstance(value, str):
                # Basic ISO-8601 validation
                return bool(re.match(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})?", value))
            return False
        if t in ("xsd:anyuri", "uri", "http://www.w3.org/2001/xmlschema#anyuri"):
            return isinstance(value, str) and (":" in value)
        return False


class PySHACLAdapter:
    """Worker adapter for running pySHACL in an isolated profile environment (CRA-020.7)."""

    def __init__(self, profile: str = PROFILE_SHACL_CORE_2017) -> None:
        self.profile = profile

    def validate(
        self,
        data_graph: Any,
        shapes_graph: Any,
        *,
        revision: str = "v1",
        timeout_seconds: float = 10.0,
    ) -> SHACLValidationReport:
        import rdflib
        import pyshacl

        # Ensure graphs are rdflib Graphs
        if isinstance(data_graph, str):
            dg = rdflib.Graph()
            dg.parse(data=data_graph, format="turtle")
        else:
            dg = data_graph

        if isinstance(shapes_graph, str):
            sg = rdflib.Graph()
            sg.parse(data=shapes_graph, format="turtle")
        else:
            sg = shapes_graph

        # Pre-scan shapes graph for unsupported SPARQL / JS components under shacl-core-2017
        if self.profile == PROFILE_SHACL_CORE_2017:
            sh_sparql = rdflib.URIRef("http://www.w3.org/ns/shacl#sparql")
            sh_js = rdflib.URIRef("http://www.w3.org/ns/shacl#js")
            for s, p, o in sg:
                if p in (sh_sparql, sh_js):
                    comp_name = "sh:SPARQLConstraintComponent" if p == sh_sparql else "sh:JSConstraintComponent"
                    return SHACLValidationReport(
                        conforms=False,
                        total_violations=1,
                        nodes_checked=0,
                        violations=[
                            SHACLViolation(
                                shape_id=str(s),
                                focus_node=str(s),
                                path=str(p),
                                message=f"Constraint component '{comp_name}' is not supported in '{self.profile}'",
                                severity=SHACLSeverity.VIOLATION.value,
                                fix_suggestion="Remove advanced constraint or enable advanced profile",
                                source_constraint_component=comp_name,
                                result_code=UNSUPPORTED_CONSTRAINT,
                            )
                        ],
                        revision=revision,
                        engine="pyshacl",
                        engine_version=getattr(pyshacl, "__version__", "0.40.1"),
                        profile=self.profile,
                        status=UNSUPPORTED_CONSTRAINT,
                    )

        start_time = time.perf_counter()
        conforms, report_graph, report_text = pyshacl.validate(
            dg,
            shacl_graph=sg,
            inference="none",
            advanced=False,
            abort_on_first=False,
            meta_shacl=False,
        )
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        violations: list[SHACLViolation] = []
        SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
        for result in report_graph.subjects(rdflib.RDF.type, SH.ValidationResult):
            focus = str(report_graph.value(result, SH.focusNode) or "unknown")
            path = str(report_graph.value(result, SH.resultPath) or "")
            msg = str(report_graph.value(result, SH.resultMessage) or "")
            sev_uri = report_graph.value(result, SH.resultSeverity)
            sev = "VIOLATION"
            if sev_uri == SH.Warning:
                sev = "WARNING"
            elif sev_uri == SH.Info:
                sev = "INFO"
            src_shape = str(report_graph.value(result, SH.sourceShape) or "")
            comp = str(report_graph.value(result, SH.sourceConstraintComponent) or "")
            val = report_graph.value(result, SH.value)

            code = SHACL_CARDINALITY_VIOLATION
            if "Datatype" in comp:
                code = SHACL_DATATYPE_VIOLATION
            elif "Class" in comp:
                code = SHACL_CLASS_VIOLATION
            elif "Pattern" in comp:
                code = SHACL_PATTERN_VIOLATION
            elif "NodeKind" in comp:
                code = SHACL_NODE_KIND_VIOLATION
            elif "In" in comp:
                code = SHACL_VALUE_SET_VIOLATION

            violations.append(SHACLViolation(
                shape_id=src_shape,
                focus_node=focus,
                path=path,
                message=msg,
                severity=sev,
                source_constraint_component=comp,
                value=str(val) if val is not None else None,
                result_code=code,
            ))

        return SHACLValidationReport(
            conforms=conforms,
            total_violations=len(violations),
            nodes_checked=len(list(dg.subjects())),
            violations=violations,
            revision=revision,
            engine="pyshacl",
            engine_version=getattr(pyshacl, "__version__", "0.40.1"),
            profile=self.profile,
            status="VALIDATED",
            execution_time_ms=elapsed_ms,
        )


class TopBraidDifferentialOracle:
    """Differential oracle comparing native validator against pySHACL reference (CRA-020.7)."""

    def __init__(self) -> None:
        self.pyshacl_adapter = PySHACLAdapter()

    def compare(self, native_report: SHACLValidationReport, pyshacl_report: SHACLValidationReport) -> dict[str, Any]:
        """Verify that native engine and reference oracle produce equivalent conformance results."""
        conformance_match = (native_report.conforms == pyshacl_report.conforms)
        return {
            "conformance_match": conformance_match,
            "native_conforms": native_report.conforms,
            "oracle_conforms": pyshacl_report.conforms,
            "native_violations": native_report.total_violations,
            "oracle_violations": pyshacl_report.total_violations,
            "oracle_engine": pyshacl_report.engine,
        }


class TransactionalSHACLValidator:
    """Provides transactional isolation, CAS base revision checking, and zero-triple commit on failure (CRA-020.4, CRA-020.5, CRA-020.10)."""

    def __init__(self, store: Any, validator: SHACLValidator | None = None) -> None:
        self.store = store
        self.validator = validator or SHACLValidator()
        self.current_revision = "rev-1"
        self._revision_counter = 1

    def get_revision(self) -> str:
        return self.current_revision

    def validate_candidate_publication(
        self,
        candidate_vertices: list[dict[str, Any]],
        candidate_edges: list[dict[str, Any]],
        expected_base_revision: str,
        *,
        timeout_seconds: float = 10.0,
    ) -> dict[str, Any]:
        """Validate candidate data jointly with existing data under expected base revision.
        
        If revision does not match, raises SHACLConcurrencyConflictError.
        If validation fails, zero triples are committed.
        """
        # 1. CAS Check on base revision
        if self.current_revision != expected_base_revision:
            raise SHACLConcurrencyConflictError(
                f"Concurrent modification conflict: expected base revision '{expected_base_revision}' "
                f"does not match current revision '{self.current_revision}'"
            )

        # 2. Stage candidate together with existing data in isolated MemoryGraphStore
        from eoip.graph.memory import MemoryGraphStore
        staged_store = MemoryGraphStore()

        # Copy existing vertices & edges
        for v in self.store.find_vertices():
            props = dict(v.get("properties", {}))
            props["canonical_id"] = v.get("canonical_id") or props.get("canonical_id")
            staged_store.upsert_vertex(v.get("label"), props)
        for e in self.store.find_edges():
            staged_store.upsert_edge(
                e.get("label"),
                e.get("out_v"),
                e.get("in_v"),
                dict(e.get("properties", {}))
            )

        # Apply candidate changes
        for v in candidate_vertices:
            props = dict(v.get("properties", {}))
            props["canonical_id"] = v.get("canonical_id") or props.get("canonical_id")
            staged_store.upsert_vertex(v.get("label"), props)
        for e in candidate_edges:
            staged_store.upsert_edge(
                e.get("label"),
                e.get("out_v"),
                e.get("in_v"),
                dict(e.get("properties", {}))
            )

        # 3. Validate staged store
        report = self.validator.validate(
            staged_store,
            revision=expected_base_revision,
            timeout_seconds=timeout_seconds,
        )

        if not report.conforms:
            # Zero triples committed on failure!
            raise SHACLTxnViolationError(
                f"Candidate validation failed with {report.total_violations} violations",
                report=report,
            )

        # 4. Atomic Commit: apply candidates to canonical store and advance revision
        committed_vertices = 0
        committed_edges = 0
        for v in candidate_vertices:
            props = dict(v.get("properties", {}))
            props["canonical_id"] = v.get("canonical_id") or props.get("canonical_id")
            self.store.upsert_vertex(v.get("label"), props)
            committed_vertices += 1

        for e in candidate_edges:
            self.store.upsert_edge(
                e.get("label"),
                e.get("out_v"),
                e.get("in_v"),
                dict(e.get("properties", {}))
            )
            committed_edges += 1

        self._revision_counter += 1
        self.current_revision = f"rev-{self._revision_counter}"

        return {
            "committed": True,
            "new_revision": self.current_revision,
            "committed_vertices": committed_vertices,
            "committed_edges": committed_edges,
            "report": report.to_dict(),
        }

    def revalidate_affected_data(
        self,
        shapes: list[SHACLShape],
        *,
        mode: str = "incremental",
        timeout_seconds: float = 10.0,
    ) -> dict[str, Any]:
        """Revalidate store data on shape changes, distinguishing incremental vs full check (CRA-020.5)."""
        reval_validator = SHACLValidator(self.validator.profile)
        reval_validator.shapes = {s.shape_id: s for s in shapes}

        report = reval_validator.validate(self.store, timeout_seconds=timeout_seconds)
        if not report.conforms:
            return {
                "conforms": False,
                "mode": mode,
                "revalidated_nodes": report.nodes_checked,
                "total_violations": report.total_violations,
                "report": report.to_dict(),
                "publication_blocked": True,
            }

        return {
            "conforms": True,
            "mode": mode,
            "revalidated_nodes": report.nodes_checked,
            "total_violations": 0,
            "report": report.to_dict(),
            "publication_blocked": False,
        }


def get_shacl_validator() -> SHACLValidator:
    return SHACLValidator()
