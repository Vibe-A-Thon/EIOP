"""Connector Mapping Language (CML) YAML parser and compiler (CRA-017.6, CRA-017.7).

Enforces:
1. Strict declarative YAML schema: source, version, subject_map, property_maps, relation_maps, provenance, governance.
2. Whitelisted template functions: lower, upper, trim, concat, split, date_parse, iri_safe.
3. Parse-time rejection of code injection attempts: __import__, {0.__class__}, eval, exec.
4. Compiles CML into engine-neutral MappingIR.
"""

from __future__ import annotations

import re
from urllib.parse import quote
from typing import Any

import yaml

from eoip.mapping.ir import (
    MappingIR,
    PropertyMapIR,
    ProvenanceConfigIR,
    RelationMapIR,
    SubjectMapIR,
)

# Allowed template function identifiers (CRA-017.6, CRA-017.11 default)
ALLOWED_FUNCTIONS = frozenset({
    "lower",
    "upper",
    "trim",
    "concat",
    "split",
    "date_parse",
    "iri_safe",
})

# Injection / dangerous patterns in templates or paths (CRA-017.A)
_FORBIDDEN_PATTERNS = [
    re.compile(r"__import__", re.IGNORECASE),
    re.compile(r"__class__", re.IGNORECASE),
    re.compile(r"__builtins__", re.IGNORECASE),
    re.compile(r"\b(eval|exec|compile|open|getattr|setattr)\s*\(", re.IGNORECASE),
    re.compile(r"\{0\.", re.IGNORECASE),
]


class CMLParseError(ValueError):
    """Raised when CML YAML syntax or template safety validation fails."""


def validate_template_safety(template_str: str) -> None:
    """Ensure template does not contain code execution attempts or unapproved expressions."""
    for pat in _FORBIDDEN_PATTERNS:
        if pat.search(template_str):
            raise CMLParseError(
                f"CML template '{template_str}' contains forbidden code or object traversal expression"
            )


def _eval_template_expr(expr: str, record: dict[str, Any]) -> str:
    expr = expr.strip()
    fn_match = re.match(r"^([a-zA-Z_]+)\((.*)\)$", expr)
    if fn_match:
        fn_name = fn_match.group(1).lower()
        inner_arg = fn_match.group(2).strip()
        if fn_name not in ALLOWED_FUNCTIONS:
            raise CMLParseError(f"Unauthorized template function '{fn_name}'; allowed: {ALLOWED_FUNCTIONS}")
        raw_val = _eval_template_expr(inner_arg, record)
        if fn_name == "lower":
            return raw_val.lower()
        elif fn_name == "upper":
            return raw_val.upper()
        elif fn_name == "trim":
            return raw_val.strip()
        elif fn_name == "iri_safe":
            return quote(raw_val, safe="")
        elif fn_name == "date_parse":
            return raw_val.split("T")[0]
        elif fn_name == "split":
            return raw_val.split(",")[0].strip()
        elif fn_name == "concat":
            return raw_val
        return raw_val

    val = record.get(expr, "")
    return str(val) if val is not None else ""


def safe_apply_template(template_str: str, record: dict[str, Any]) -> str:
    """Apply safe {field} or {func(field)} substitutions."""
    validate_template_safety(template_str)

    def _replace_var(match: re.Match) -> str:
        var_expr = match.group(1).strip()
        return _eval_template_expr(var_expr, record)

    return re.sub(r"\{([^}]+)\}", _replace_var, template_str)


def parse_and_compile_cml(cml_yaml: str) -> MappingIR:
    """Parse CML YAML document and compile into engine-neutral MappingIR."""
    try:
        data = yaml.safe_load(cml_yaml)
    except Exception as e:
        raise CMLParseError(f"YAML parse error: {e}")

    if not isinstance(data, dict):
        raise CMLParseError("CML root must be a YAML mapping")

    source = data.get("source")
    if not source:
        raise CMLParseError("Missing required 'source' in CML mapping")

    version = str(data.get("version", "1.0.0"))
    mapping_id = data.get("id", f"cml_{source}_{version}")

    # Subject Map
    subj_data = data.get("subject_map")
    if not subj_data or "template" not in subj_data or "class" not in subj_data:
        raise CMLParseError("CML 'subject_map' requires 'template' and 'class'")
    validate_template_safety(subj_data["template"])
    subj_ir = SubjectMapIR(
        template=subj_data["template"],
        target_class_iri=subj_data["class"],
        graph_iri_template=subj_data.get("graph"),
    )

    # Governance
    gov = data.get("governance", {})
    classification = gov.get("classification", "INTERNAL")
    pii_fields = list(gov.get("pii_fields", []))

    # Property Maps
    prop_maps_ir: list[PropertyMapIR] = []
    for pm in data.get("property_maps", []):
        path = pm.get("path")
        pred = pm.get("predicate")
        if not path or not pred:
            raise CMLParseError(f"property_map requires 'path' and 'predicate': {pm}")
        validate_template_safety(path)
        is_pii = (path in pii_fields) or bool(pm.get("pii", False))
        prop_maps_ir.append(
            PropertyMapIR(
                source_path=path,
                predicate_iri=pred,
                datatype_iri=pm.get("datatype", "http://www.w3.org/2001/XMLSchema#string"),
                required=bool(pm.get("required", False)),
                language=pm.get("language"),
                is_pii=is_pii,
                classification=pm.get("classification", classification),
            )
        )

    # Relation Maps
    rel_maps_ir: list[RelationMapIR] = []
    for rm in data.get("relation_maps", []):
        path = rm.get("path")
        pred = rm.get("predicate")
        obj_tmpl = rm.get("object_template")
        obj_cls = rm.get("object_class")
        if not path or not pred or not obj_tmpl or not obj_cls:
            raise CMLParseError(f"relation_map requires path, predicate, object_template, and object_class: {rm}")
        validate_template_safety(obj_tmpl)
        rel_maps_ir.append(
            RelationMapIR(
                source_path=path,
                predicate_iri=pred,
                object_template=obj_tmpl,
                object_class_iri=obj_cls,
                edge_properties=rm.get("properties", {}),
            )
        )

    # Provenance
    prov_data = data.get("provenance", {})
    prov_ir = ProvenanceConfigIR(
        emit_prov_o=bool(prov_data.get("emit", True)),
        confidence_default=float(prov_data.get("confidence", 1.0)),
        connector_agent_iri=prov_data.get("agent", "urn:eoip:agent:connector"),
    )

    return MappingIR(
        mapping_id=mapping_id,
        version=version,
        source_type=source,
        subject_map=subj_ir,
        property_maps=prop_maps_ir,
        relation_maps=rel_maps_ir,
        provenance=prov_ir,
        classification=classification,
        pii_fields=pii_fields,
    )
