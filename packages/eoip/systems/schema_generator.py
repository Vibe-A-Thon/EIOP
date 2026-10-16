"""Auto-Schema Generator — generates graph schemas from raw JSON data files.

When a new system connects and provides sample data (raw JSON), this module:
1. Profiles the data structure (types, keys, nullability, cardinality)
2. Detects entity types and relationship candidates
3. Generates an ontology-compatible schema with vertex/edge labels
4. Produces field mappings, GraphQL SDL, and JSON Schema
5. Creates validation rules and golden queries
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class FieldSpec:
    name: str
    inferred_type: str
    is_nullable: bool
    is_key: bool
    is_foreign_key: bool
    foreign_key_target: str | None = None
    format_hint: str | None = None
    sample_values: list[Any] = field(default_factory=list)


@dataclass
class EntitySchema:
    label: str
    source_name: str
    key_field: str
    fields: list[FieldSpec]
    record_count: int = 0


@dataclass
class RelationshipSchema:
    edge_label: str
    from_entity: str
    to_entity: str
    foreign_key_field: str
    cardinality: str = "MANY_TO_ONE"


@dataclass
class GeneratedSchema:
    system_id: str
    system_type: str
    entities: list[EntitySchema]
    relationships: list[RelationshipSchema]
    graphql_sdl: str
    json_schema: dict[str, Any]
    field_mappings: dict[str, dict[str, str]]
    ontology_labels: dict[str, list[str]]
    golden_queries: list[str]
    validation_rules: list[dict[str, Any]]
    generated_at: str
    data_fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AutoSchemaGenerator:
    """Generates complete graph schemas from raw JSON data samples."""

    # Type inference
    _DATE_PATTERNS = [
        re.compile(r"^\d{4}-\d{2}-\d{2}"),
        re.compile(r"^\d{2}/\d{2}/\d{4}"),
    ]
    _EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _URL_PATTERN = re.compile(r"^https?://")
    _UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
    _ID_PATTERN = re.compile(r"^(?:.+_)?(?:id|key|uuid|guid|code|number|num)$", re.I)
    _FK_PATTERN = re.compile(r"^(.+?)_(?:id|key|uuid|ref|code)$", re.I)

    def generate_from_json(
        self,
        system_id: str,
        system_type: str,
        data: list[dict[str, Any]] | dict[str, Any],
        dataset_name: str | None = None,
    ) -> GeneratedSchema:
        """Generate schema from raw JSON data (array of records or nested object)."""
        datasets: dict[str, list[dict[str, Any]]] = {}

        if isinstance(data, list) and data and isinstance(data[0], dict):
            name = dataset_name or self._infer_dataset_name(system_type)
            datasets[name] = data
        elif isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, list) and val and isinstance(val[0], dict):
                    datasets[key] = val
                elif isinstance(val, dict):
                    datasets[key] = [val]
            if not datasets:
                name = dataset_name or self._infer_dataset_name(system_type)
                datasets[name] = [data]

        entities: list[EntitySchema] = []
        relationships: list[RelationshipSchema] = []

        for ds_name, records in datasets.items():
            entity = self._profile_entity(ds_name, records)
            entities.append(entity)

        # Relationship discovery across entities
        entity_labels = {e.label for e in entities}
        for entity in entities:
            for f in entity.fields:
                if f.is_foreign_key and f.foreign_key_target:
                    target_label = self._to_pascal_case(f.foreign_key_target)
                    if target_label in entity_labels or True:
                        relationships.append(RelationshipSchema(
                            edge_label=f"REL_{f.foreign_key_target.upper()}",
                            from_entity=entity.label,
                            to_entity=target_label,
                            foreign_key_field=f.name,
                        ))

        # Nested object relationships
        for entity in entities:
            for f in entity.fields:
                if f.inferred_type == "object":
                    child_label = self._to_pascal_case(f.name)
                    relationships.append(RelationshipSchema(
                        edge_label=f"HAS_{f.name.upper()}",
                        from_entity=entity.label,
                        to_entity=child_label,
                        foreign_key_field=f.name,
                        cardinality="ONE_TO_ONE",
                    ))
                elif f.inferred_type == "array_of_objects":
                    child_label = self._to_pascal_case(f.name)
                    relationships.append(RelationshipSchema(
                        edge_label=f"HAS_{f.name.upper()}",
                        from_entity=entity.label,
                        to_entity=child_label,
                        foreign_key_field=f.name,
                        cardinality="ONE_TO_MANY",
                    ))

        graphql_sdl = self._generate_graphql(entities, relationships)
        json_schema = self._generate_json_schema(entities)
        field_mappings = self._generate_field_mappings(entities)
        ontology_labels = {
            "vertex_labels": [e.label for e in entities],
            "edge_labels": [r.edge_label for r in relationships],
        }
        golden_queries = self._generate_golden_queries(entities, relationships)
        validation_rules = self._generate_validation_rules(entities)
        fingerprint = hashlib.sha256(
            json.dumps(datasets, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]

        return GeneratedSchema(
            system_id=system_id,
            system_type=system_type,
            entities=entities,
            relationships=relationships,
            graphql_sdl=graphql_sdl,
            json_schema=json_schema,
            field_mappings=field_mappings,
            ontology_labels=ontology_labels,
            golden_queries=golden_queries,
            validation_rules=validation_rules,
            generated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            data_fingerprint=fingerprint,
        )

    def generate_from_file(
        self, system_id: str, system_type: str, file_path: str,
        dataset_name: str | None = None,
    ) -> GeneratedSchema:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.generate_from_json(system_id, system_type, data, dataset_name)

    def _infer_dataset_name(self, system_type: str) -> str:
        return system_type.replace("-", "_").replace(" ", "_")

    def _to_pascal_case(self, name: str) -> str:
        parts = re.split(r"[_\-\s]+", name)
        return "".join(p.capitalize() for p in parts if p)

    def _to_graphql_type(self, t: str) -> str:
        mapping = {
            "string": "String", "int": "Int", "float": "Float",
            "boolean": "Boolean", "datetime": "String",
            "email": "String", "url": "String", "uuid": "ID",
            "list": "[String]", "object": "JSON",
            "array_of_objects": "[JSON]", "array_of_strings": "[String]",
            "array_of_ints": "[Int]",
        }
        return mapping.get(t, "String")

    def _infer_field_type(self, values: list[Any]) -> tuple[str, str | None]:
        non_null = [v for v in values if v is not None]
        if not non_null:
            return "string", None

        sample = non_null[0]
        if isinstance(sample, bool):
            return "boolean", None
        if isinstance(sample, int):
            return "int", None
        if isinstance(sample, float):
            return "float", None
        if isinstance(sample, list):
            if sample and isinstance(sample[0], dict):
                return "array_of_objects", None
            if sample and isinstance(sample[0], str):
                return "array_of_strings", None
            if sample and isinstance(sample[0], int):
                return "array_of_ints", None
            return "list", None
        if isinstance(sample, dict):
            return "object", None

        s = str(sample)
        if self._UUID_PATTERN.match(s):
            return "string", "uuid"
        if self._EMAIL_PATTERN.match(s):
            return "string", "email"
        if self._URL_PATTERN.match(s):
            return "string", "url"
        for dp in self._DATE_PATTERNS:
            if dp.match(s):
                return "datetime", "iso_datetime"
        return "string", None

    def _profile_entity(self, name: str, records: list[dict[str, Any]]) -> EntitySchema:
        label = self._to_pascal_case(name)
        field_values: dict[str, list[Any]] = {}
        for rec in records:
            for k, v in rec.items():
                field_values.setdefault(k, []).append(v)

        fields: list[FieldSpec] = []
        key_field = "id"
        key_score: dict[str, float] = {}

        for fname, values in field_values.items():
            inferred_type, format_hint = self._infer_field_type(values)
            is_nullable = any(v is None for v in values)
            non_null = [v for v in values if v is not None]
            unique_count = len(set(str(v) for v in non_null))
            is_unique = unique_count == len(non_null) and len(non_null) > 1

            is_id_like = bool(self._ID_PATTERN.match(fname))
            fk_match = self._FK_PATTERN.match(fname)
            is_fk = bool(fk_match) and fname != "id"
            fk_target = fk_match.group(1) if fk_match else None

            # Key candidate scoring
            score = 0.0
            if fname == "id":
                score = 1.0
            elif is_id_like and is_unique:
                score = 0.9
            elif is_unique and not is_nullable:
                score = 0.7
            key_score[fname] = score

            fields.append(FieldSpec(
                name=fname,
                inferred_type=inferred_type,
                is_nullable=is_nullable,
                is_key=False,
                is_foreign_key=is_fk,
                foreign_key_target=fk_target,
                format_hint=format_hint,
                sample_values=[str(v)[:50] for v in non_null[:3]],
            ))

        if key_score:
            best_key = max(key_score, key=lambda k: key_score[k])
            key_field = best_key
            for f in fields:
                if f.name == best_key:
                    f.is_key = True
                    break

        return EntitySchema(
            label=label,
            source_name=name,
            key_field=key_field,
            fields=fields,
            record_count=len(records),
        )

    def _generate_graphql(self, entities: list[EntitySchema],
                          relationships: list[RelationshipSchema]) -> str:
        lines: list[str] = []
        for e in entities:
            lines.append(f"type {e.label} {{")
            for f in e.fields:
                gql_type = self._to_graphql_type(f.inferred_type)
                nullable = "" if f.is_nullable else "!"
                key_marker = " @key" if f.is_key else ""
                lines.append(f"  {f.name}: {gql_type}{nullable}{key_marker}")
            # Add relationship fields
            for r in relationships:
                if r.from_entity == e.label:
                    card = f"[{r.to_entity}]" if "MANY" in r.cardinality else r.to_entity
                    lines.append(f"  {r.to_entity.lower()}: {card}")
            lines.append("}")
            lines.append("")
        return "\n".join(lines)

    def _generate_json_schema(self, entities: list[EntitySchema]) -> dict[str, Any]:
        definitions: dict[str, Any] = {}
        for e in entities:
            props: dict[str, Any] = {}
            required: list[str] = []
            for f in e.fields:
                type_map = {
                    "string": {"type": "string"}, "int": {"type": "integer"},
                    "float": {"type": "number"}, "boolean": {"type": "boolean"},
                    "datetime": {"type": "string", "format": "date-time"},
                    "object": {"type": "object"}, "list": {"type": "array"},
                    "array_of_objects": {"type": "array", "items": {"type": "object"}},
                    "array_of_strings": {"type": "array", "items": {"type": "string"}},
                    "array_of_ints": {"type": "array", "items": {"type": "integer"}},
                }
                props[f.name] = type_map.get(f.inferred_type, {"type": "string"})
                if f.format_hint:
                    props[f.name]["format"] = f.format_hint
                if not f.is_nullable:
                    required.append(f.name)
            definitions[e.label] = {
                "type": "object",
                "properties": props,
                "required": required,
            }
        return {"$schema": "https://json-schema.org/draft/2020-12/schema", "definitions": definitions}

    def _generate_field_mappings(self, entities: list[EntitySchema]) -> dict[str, dict[str, str]]:
        mappings: dict[str, dict[str, str]] = {}
        for e in entities:
            entity_map: dict[str, str] = {}
            for f in e.fields:
                if f.is_key:
                    entity_map[f.name] = "canonical_id"
                elif f.inferred_type == "datetime":
                    entity_map[f.name] = f"properties.{f.name}"
                else:
                    entity_map[f.name] = f"properties.{f.name}"
            mappings[e.label] = entity_map
        return mappings

    def _generate_golden_queries(self, entities: list[EntitySchema],
                                  relationships: list[RelationshipSchema]) -> list[str]:
        queries: list[str] = []
        for e in entities:
            queries.append(f"MATCH (n:{e.label}) RETURN n LIMIT 25")
            queries.append(f"MATCH (n:{e.label}) RETURN count(n) AS total")
        for r in relationships:
            queries.append(
                f"MATCH (a:{r.from_entity})-[:{r.edge_label}]->(b:{r.to_entity}) RETURN a, b LIMIT 25"
            )
        return queries

    def _generate_validation_rules(self, entities: list[EntitySchema]) -> list[dict[str, Any]]:
        rules: list[dict[str, Any]] = []
        for e in entities:
            for f in e.fields:
                if f.is_key:
                    rules.append({
                        "entity": e.label, "field": f.name,
                        "rule": "NOT_NULL", "severity": "ERROR",
                    })
                    rules.append({
                        "entity": e.label, "field": f.name,
                        "rule": "UNIQUE", "severity": "ERROR",
                    })
                if not f.is_nullable and not f.is_key:
                    rules.append({
                        "entity": e.label, "field": f.name,
                        "rule": "NOT_NULL", "severity": "WARNING",
                    })
        return rules
