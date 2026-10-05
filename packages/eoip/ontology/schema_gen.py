"""Generate JSON Schema, OpenAPI schemas and form specs from the ontology (GAP-STUDIO-011).

Reads VERTEX_LABELS and EDGE_LABELS from ``eoip.ontology.manifest`` and
produces machine-readable schema definitions for vertex labels. These drive
form generation, API payload validation and Studio UI rendering.
"""

from __future__ import annotations

from typing import Any

from eoip.ontology.manifest import EDGE_LABELS, PROPERTY_KEYS, VERTEX_LABELS

# Map HugeGraph property types to JSON Schema types
_HUGEGRAPH_TO_JSON_SCHEMA: dict[str, dict[str, Any]] = {
    "TEXT": {"type": "string"},
    "INT": {"type": "integer"},
    "LONG": {"type": "integer"},
    "DOUBLE": {"type": "number"},
    "BOOLEAN": {"type": "boolean"},
    "DATE": {"type": "string", "format": "date-time"},
}


def _property_schema(prop_name: str) -> dict[str, Any]:
    """Return a JSON Schema snippet for a single property key."""
    hugegraph_type = PROPERTY_KEYS.get(prop_name, "TEXT")
    schema = dict(_HUGEGRAPH_TO_JSON_SCHEMA.get(hugegraph_type, {"type": "string"}))
    schema["description"] = f"Property '{prop_name}' ({hugegraph_type})"
    return schema


def generate_json_schema(label: str) -> dict[str, Any]:
    """Generate a JSON Schema for a vertex label's properties.

    Uses the ``(domain, required_props, optional_props)`` tuple structure
    from ``VERTEX_LABELS``. Returns a valid JSON Schema dict with ``type``,
    ``properties`` and ``required``.

    Raises ``KeyError`` if the label is not declared in the ontology.
    """
    if label not in VERTEX_LABELS:
        raise KeyError(f"Unknown vertex label: {label}")

    domain, required_props, optional_props = VERTEX_LABELS[label]
    all_props = required_props + optional_props
    properties: dict[str, Any] = {}
    for prop_name in all_props:
        properties[prop_name] = _property_schema(prop_name)

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": label,
        "description": f"Schema for {label} vertex (domain: {domain})",
        "type": "object",
        "properties": properties,
        "required": list(required_props),
        "additionalProperties": False,
    }


def generate_openapi_schemas() -> dict[str, Any]:
    """Generate OpenAPI-style component schemas for all vertex labels.

    Returns a dict suitable for embedding in an OpenAPI ``components.schemas``
    section. Each key is a vertex label, each value is a schema object.
    """
    schemas: dict[str, Any] = {}
    for label in VERTEX_LABELS:
        domain, required_props, optional_props = VERTEX_LABELS[label]
        all_props = required_props + optional_props
        properties: dict[str, Any] = {}
        for prop_name in all_props:
            properties[prop_name] = _property_schema(prop_name)

        schemas[label] = {
            "type": "object",
            "description": f"{label} vertex (domain: {domain})",
            "properties": properties,
            "required": list(required_props),
        }
    return {"schemas": schemas}


# Map HugeGraph types to form field types
_HUGEGRAPH_TO_FORM_TYPE: dict[str, str] = {
    "TEXT": "text",
    "INT": "number",
    "LONG": "number",
    "DOUBLE": "number",
    "BOOLEAN": "checkbox",
    "DATE": "datetime",
}


def generate_form_spec(label: str) -> dict[str, Any]:
    """Generate a form specification for a vertex label.

    Returns a dict with ``label``, ``domain`` and ``fields`` — a list of
    field descriptors containing ``name``, ``type``, ``required`` and
    ``hugegraph_type``.

    Raises ``KeyError`` if the label is not declared in the ontology.
    """
    if label not in VERTEX_LABELS:
        raise KeyError(f"Unknown vertex label: {label}")

    domain, required_props, optional_props = VERTEX_LABELS[label]
    required_set = set(required_props)
    all_props = required_props + optional_props
    fields: list[dict[str, Any]] = []
    for prop_name in all_props:
        hugegraph_type = PROPERTY_KEYS.get(prop_name, "TEXT")
        fields.append(
            {
                "name": prop_name,
                "type": _HUGEGRAPH_TO_FORM_TYPE.get(hugegraph_type, "text"),
                "required": prop_name in required_set,
                "hugegraph_type": hugegraph_type,
            }
        )

    return {
        "label": label,
        "domain": domain,
        "fields": fields,
    }
