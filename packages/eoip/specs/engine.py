"""Spec Engineering engine — declarative entity specs → auto-generated
JSON Schema, Pydantic code, validation rules, and versioning with
diff/migration detection."""

from __future__ import annotations

import hashlib
import json
import re
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FieldType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    LIST = "list"
    MAP = "map"
    REFERENCE = "reference"
    ENUM = "enum"
    TEXT = "text"


@dataclass
class FieldConstraint:
    min_length: int | None = None
    max_length: int | None = None
    min_value: float | None = None
    max_value: float | None = None
    pattern: str | None = None
    allowed_values: list[str] | None = None
    unique: bool = False
    indexed: bool = False
    reference_type: str | None = None


@dataclass
class FieldSpec:
    name: str
    field_type: FieldType
    required: bool = True
    default: Any = None
    description: str = ""
    constraint: FieldConstraint | None = None

    def to_json_schema(self) -> dict[str, Any]:
        type_map = {
            FieldType.STRING: "string", FieldType.TEXT: "string",
            FieldType.INTEGER: "integer", FieldType.FLOAT: "number",
            FieldType.BOOLEAN: "boolean", FieldType.DATETIME: "string",
            FieldType.LIST: "array", FieldType.MAP: "object",
            FieldType.REFERENCE: "string", FieldType.ENUM: "string",
        }
        schema: dict[str, Any] = {"type": type_map.get(self.field_type, "string")}
        if self.description:
            schema["description"] = self.description
        if self.default is not None:
            schema["default"] = self.default
        if self.constraint:
            c = self.constraint
            if c.min_length is not None:
                schema["minLength"] = c.min_length
            if c.max_length is not None:
                schema["maxLength"] = c.max_length
            if c.min_value is not None:
                schema["minimum"] = c.min_value
            if c.max_value is not None:
                schema["maximum"] = c.max_value
            if c.pattern:
                schema["pattern"] = c.pattern
            if c.allowed_values:
                schema["enum"] = c.allowed_values
        if self.field_type == FieldType.DATETIME:
            schema["format"] = "date-time"
        return schema


@dataclass
class EntitySpec:
    name: str
    fields: list[FieldSpec]
    description: str = ""
    version: int = 1

    def to_json_schema(self) -> dict[str, Any]:
        properties = {f.name: f.to_json_schema() for f in self.fields}
        required = [f.name for f in self.fields if f.required]
        schema: dict[str, Any] = {
            "type": "object",
            "title": self.name,
            "properties": properties,
        }
        if required:
            schema["required"] = required
        if self.description:
            schema["description"] = self.description
        return schema

    def to_pydantic_code(self) -> str:
        type_map = {
            FieldType.STRING: "str", FieldType.TEXT: "str",
            FieldType.INTEGER: "int", FieldType.FLOAT: "float",
            FieldType.BOOLEAN: "bool", FieldType.DATETIME: "str",
            FieldType.LIST: "list", FieldType.MAP: "dict",
            FieldType.REFERENCE: "str", FieldType.ENUM: "str",
        }
        lines = [
            "from pydantic import BaseModel, Field",
            "",
            f"class {self.name}(BaseModel):",
        ]
        if self.description:
            lines.append(f'    """{self.description}"""')
        for f in self.fields:
            py_type = type_map.get(f.field_type, "str")
            if not f.required:
                py_type = f"{py_type} | None"
            default = f" = {repr(f.default)}" if f.default is not None else ""
            if not f.required and f.default is None:
                default = " = None"
            lines.append(f"    {f.name}: {py_type}{default}")
        return "\n".join(lines)

    def validate_instance(self, data: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        for f in self.fields:
            if f.required and f.name not in data:
                errors.append(f"Missing required field: {f.name}")
            if f.name in data and f.constraint:
                val = data[f.name]
                c = f.constraint
                if isinstance(val, str):
                    if c.min_length and len(val) < c.min_length:
                        errors.append(f"{f.name}: too short (min {c.min_length})")
                    if c.max_length and len(val) > c.max_length:
                        errors.append(f"{f.name}: too long (max {c.max_length})")
                    if c.pattern and not re.match(c.pattern, val):
                        errors.append(f"{f.name}: doesn't match pattern {c.pattern}")
                    if c.allowed_values and val not in c.allowed_values:
                        errors.append(f"{f.name}: not in allowed values")
                if isinstance(val, (int, float)):
                    if c.min_value is not None and val < c.min_value:
                        errors.append(f"{f.name}: below minimum {c.min_value}")
                    if c.max_value is not None and val > c.max_value:
                        errors.append(f"{f.name}: above maximum {c.max_value}")
        return errors

    def fingerprint(self) -> str:
        data = json.dumps(self.to_json_schema(), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def required_field_names(self) -> list[str]:
        return [f.name for f in self.fields if f.required]

    def field_map(self) -> dict[str, FieldSpec]:
        return {f.name: f for f in self.fields}


@dataclass
class RelationshipSpec:
    name: str
    source_type: str
    target_type: str
    cardinality: str = "many-to-many"
    bidirectional: bool = False
    description: str = ""


@dataclass
class SpecVersion:
    spec_name: str
    version: int
    spec: EntitySpec
    created_at: float = field(default_factory=time.time)


@dataclass
class SpecMigration:
    from_version: int
    to_version: int
    added_fields: list[str]
    removed_fields: list[str]
    modified_fields: list[str]
    breaking: bool = False


@dataclass
class SpecValidationResult:
    valid: bool
    errors: list[str]
    spec_name: str
    version: int


class SpecRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._specs: dict[str, list[SpecVersion]] = defaultdict(list)
        self._relationships: dict[str, RelationshipSpec] = {}

    def register(self, spec: EntitySpec) -> SpecVersion:
        with self._lock:
            versions = self._specs[spec.name]
            v = SpecVersion(spec.name, len(versions) + 1, spec)
            versions.append(v)
            spec.version = v.version
            return v

    def get(self, name: str, version: int | None = None) -> EntitySpec | None:
        with self._lock:
            versions = self._specs.get(name, [])
            if not versions:
                return None
            if version is None:
                return versions[-1].spec
            for v in versions:
                if v.version == version:
                    return v.spec
            return None

    def diff(self, name: str, v1: int, v2: int) -> SpecMigration | None:
        s1 = self.get(name, v1)
        s2 = self.get(name, v2)
        if not s1 or not s2:
            return None
        f1 = {f.name for f in s1.fields}
        f2 = {f.name for f in s2.fields}
        added = sorted(f2 - f1)
        removed = sorted(f1 - f2)
        common = f1 & f2
        m1 = s1.field_map()
        m2 = s2.field_map()
        modified = sorted(n for n in common if m1[n].field_type != m2[n].field_type)
        breaking = bool(removed) or bool(modified)
        return SpecMigration(v1, v2, added, removed, modified, breaking)

    def validate(self, name: str, data: dict[str, Any]) -> SpecValidationResult:
        spec = self.get(name)
        if not spec:
            return SpecValidationResult(False, [f"Spec '{name}' not found"], name, 0)
        errors = spec.validate_instance(data)
        return SpecValidationResult(not errors, errors, name, spec.version)

    def add_relationship(self, rel: RelationshipSpec) -> None:
        self._relationships[rel.name] = rel

    def generate_openapi_schemas(self) -> dict[str, Any]:
        schemas: dict[str, Any] = {}
        for name in self._specs:
            spec = self.get(name)
            if spec:
                schemas[name] = spec.to_json_schema()
        return schemas

    def stats(self) -> dict[str, Any]:
        return {
            "specs": len(self._specs),
            "total_versions": sum(len(v) for v in self._specs.values()),
            "relationships": len(self._relationships),
        }


class SpecEngine:
    """Top-level Spec Engineering orchestrator."""

    def __init__(self) -> None:
        self._registry = SpecRegistry()

    @property
    def registry(self) -> SpecRegistry:
        return self._registry

    def define_entity(self, name: str, fields_dict: dict[str, dict[str, Any]],
                      description: str = "") -> EntitySpec:
        fields: list[FieldSpec] = []
        for field_name, config in fields_dict.items():
            ft = FieldType(config.get("type", "string"))
            constraint = None
            if any(k in config for k in ("min_length", "max_length", "min_value", "max_value", "pattern", "allowed_values")):
                constraint = FieldConstraint(
                    min_length=config.get("min_length"),
                    max_length=config.get("max_length"),
                    min_value=config.get("min_value"),
                    max_value=config.get("max_value"),
                    pattern=config.get("pattern"),
                    allowed_values=config.get("allowed_values"),
                )
            fields.append(FieldSpec(
                name=field_name, field_type=ft,
                required=config.get("required", True),
                default=config.get("default"),
                description=config.get("description", ""),
                constraint=constraint,
            ))
        spec = EntitySpec(name=name, fields=fields, description=description)
        self._registry.register(spec)
        return spec

    def define_relationship(self, name: str, source: str, target: str,
                            cardinality: str = "many-to-many",
                            bidirectional: bool = False) -> RelationshipSpec:
        rel = RelationshipSpec(name, source, target, cardinality, bidirectional)
        self._registry.add_relationship(rel)
        return rel

    def validate(self, name: str, data: dict[str, Any]) -> SpecValidationResult:
        return self._registry.validate(name, data)

    def generate_json_schema(self, name: str) -> dict[str, Any] | None:
        spec = self._registry.get(name)
        return spec.to_json_schema() if spec else None

    def generate_pydantic(self, name: str) -> str | None:
        spec = self._registry.get(name)
        return spec.to_pydantic_code() if spec else None

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "spec_engineering",
            **self._registry.stats(),
        }


_instance: SpecEngine | None = None
_lock = threading.Lock()


def get_spec_engine() -> SpecEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = SpecEngine()
    return _instance
