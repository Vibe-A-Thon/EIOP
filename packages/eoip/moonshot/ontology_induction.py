"""KGR-G-015: LLM-Assisted Dynamic Ontology Induction.

AutoSchemaKG-pattern joint extraction + schema induction from
unstructured text with SHACL anti-drift guards.  Uses a local LLM
(air-gap compatible) to propose entity types, relationship types, and
property shapes from raw text corpora.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol
from collections.abc import Callable

log = logging.getLogger("eoip.moonshot.ontology_induction")


class InductionStrategy(str, Enum):
    JOINT_EXTRACTION = "JOINT_EXTRACTION"
    SCHEMA_FIRST = "SCHEMA_FIRST"
    INSTANCE_DRIVEN = "INSTANCE_DRIVEN"
    HYBRID = "HYBRID"


@dataclass
class EntityTypeProposal:
    name: str
    description: str
    properties: list[PropertyProposal]
    parent_type: str | None = None
    confidence: float = 0.0
    evidence_count: int = 0
    source_spans: list[str] = field(default_factory=list)

    @property
    def canonical_id(self) -> str:
        return f"entity_type:{self.name.lower()}"


@dataclass
class PropertyProposal:
    name: str
    data_type: str  # string, integer, float, boolean, datetime, uri
    description: str
    required: bool = False
    cardinality: str = "single"  # single, list, set
    confidence: float = 0.0


@dataclass
class RelationshipTypeProposal:
    name: str
    source_type: str
    target_type: str
    description: str
    cardinality: str = "many-to-many"
    confidence: float = 0.0
    evidence_count: int = 0


@dataclass
class SHACLShape:
    """A SHACL node shape for validating induced ontology elements."""
    target_class: str
    properties: list[SHACLPropertyShape]
    closed: bool = False

    def to_turtle(self) -> str:
        lines = [
            f"eoip:{self.target_class}Shape",
            "    a sh:NodeShape ;",
            f"    sh:targetClass eoip:{self.target_class} ;",
        ]
        if self.closed:
            lines.append("    sh:closed true ;")
        for prop in self.properties:
            lines.append("    sh:property [")
            lines.append(f"        sh:path eoip:{prop.path} ;")
            if prop.datatype:
                lines.append(f"        sh:datatype xsd:{prop.datatype} ;")
            if prop.min_count is not None:
                lines.append(f"        sh:minCount {prop.min_count} ;")
            if prop.max_count is not None:
                lines.append(f"        sh:maxCount {prop.max_count} ;")
            lines.append("    ] ;")
        if lines[-1].endswith(";"):
            lines[-1] = lines[-1][:-1] + "."
        return "\n".join(lines)


@dataclass
class SHACLPropertyShape:
    path: str
    datatype: str | None = None
    min_count: int | None = None
    max_count: int | None = None
    pattern: str | None = None


@dataclass
class InductionResult:
    entity_types: list[EntityTypeProposal]
    relationship_types: list[RelationshipTypeProposal]
    shacl_shapes: list[SHACLShape]
    consolidated_types: int = 0
    drift_violations: list[str] = field(default_factory=list)
    processing_time_ms: int = 0


class LLMProvider(Protocol):
    """Interface for local LLM inference (Ollama, vLLM, llama.cpp)."""
    def generate(self, prompt: str, *, max_tokens: int = 2048, temperature: float = 0.1) -> str: ...


class LocalOllamaProvider:
    """Ollama-based local LLM provider."""

    def __init__(self, model: str = "llama3.1:8b", base_url: str = "http://localhost:11434") -> None:
        from urllib.parse import urlsplit
        if urlsplit(base_url).scheme not in ("http", "https"):
            raise ValueError(f"LLM provider URL scheme must be http or https: {base_url!r}")
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str, *, max_tokens: int = 2048, temperature: float = 0.1) -> str:
        import urllib.request
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": temperature},
        }).encode()
        req = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:  # nosec B310 - scheme restricted to http/https in __init__
            result = json.loads(resp.read())
        return result.get("response", "")


EXTRACTION_PROMPT = """Analyze the following text and extract a structured ontology schema.

TEXT:
{text}

Return a JSON object with this exact structure:
{{
  "entity_types": [
    {{
      "name": "TypeName",
      "description": "what this entity represents",
      "properties": [
        {{"name": "prop_name", "data_type": "string|integer|float|boolean|datetime|uri", "required": true|false}}
      ],
      "parent_type": null
    }}
  ],
  "relationship_types": [
    {{
      "name": "RELATIONSHIP_NAME",
      "source_type": "SourceType",
      "target_type": "TargetType",
      "description": "what this relationship means",
      "cardinality": "one-to-one|one-to-many|many-to-many"
    }}
  ]
}}

Rules:
- Use PascalCase for entity type names
- Use UPPER_SNAKE_CASE for relationship names
- Only include types with clear evidence in the text
- Include at least one descriptive property per entity type
- Return valid JSON only, no markdown formatting"""


class CorpusOntologyInducer:
    """Induces ontology schemas from unstructured text corpora using a local LLM."""

    def __init__(
        self,
        llm: LLMProvider,
        *,
        strategy: InductionStrategy = InductionStrategy.JOINT_EXTRACTION,
        min_confidence: float = 0.3,
        max_chunk_chars: int = 4000,
    ) -> None:
        self.llm = llm
        self.strategy = strategy
        self.min_confidence = min_confidence
        self.max_chunk_chars = max_chunk_chars

    def induce(self, texts: list[str]) -> InductionResult:
        started = time.monotonic()
        all_entities: list[EntityTypeProposal] = []
        all_relationships: list[RelationshipTypeProposal] = []

        for text in texts:
            chunks = self._chunk_text(text)
            for chunk in chunks:
                entities, rels = self._extract_from_chunk(chunk)
                all_entities.extend(entities)
                all_relationships.extend(rels)

        consolidated_entities = TypeConsolidationGuard.consolidate_entity_types(all_entities)
        consolidated_rels = TypeConsolidationGuard.consolidate_relationship_types(all_relationships)

        shapes = self._generate_shacl_shapes(consolidated_entities)

        elapsed = int((time.monotonic() - started) * 1000)
        return InductionResult(
            entity_types=consolidated_entities,
            relationship_types=consolidated_rels,
            shacl_shapes=shapes,
            consolidated_types=len(all_entities) - len(consolidated_entities),
            processing_time_ms=elapsed,
        )

    def _chunk_text(self, text: str) -> list[str]:
        if len(text) <= self.max_chunk_chars:
            return [text] if text.strip() else []
        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = min(start + self.max_chunk_chars, len(text))
            if end < len(text):
                break_at = text.rfind("\n\n", start, end)
                if break_at > start + self.max_chunk_chars // 2:
                    end = break_at
            chunks.append(text[start:end])
            start = end
        return chunks

    def _extract_from_chunk(self, text: str) -> tuple[list[EntityTypeProposal], list[RelationshipTypeProposal]]:
        prompt = EXTRACTION_PROMPT.format(text=text[:self.max_chunk_chars])
        response = self.llm.generate(prompt, max_tokens=2048, temperature=0.1)

        entities: list[EntityTypeProposal] = []
        relationships: list[RelationshipTypeProposal] = []

        try:
            json_match = re.search(r"\{[\s\S]*\}", response)
            if not json_match:
                return entities, relationships
            data = json.loads(json_match.group())
        except (json.JSONDecodeError, ValueError):
            log.warning("Failed to parse LLM response as JSON")
            return entities, relationships

        for et in data.get("entity_types", []):
            props = [
                PropertyProposal(
                    name=p.get("name", ""),
                    data_type=p.get("data_type", "string"),
                    description=p.get("description", ""),
                    required=p.get("required", False),
                    confidence=0.7,
                )
                for p in et.get("properties", [])
                if p.get("name")
            ]
            entities.append(EntityTypeProposal(
                name=et.get("name", "Unknown"),
                description=et.get("description", ""),
                properties=props,
                parent_type=et.get("parent_type"),
                confidence=0.7,
                evidence_count=1,
                source_spans=[text[:200]],
            ))

        for rt in data.get("relationship_types", []):
            relationships.append(RelationshipTypeProposal(
                name=rt.get("name", "RELATED_TO"),
                source_type=rt.get("source_type", ""),
                target_type=rt.get("target_type", ""),
                description=rt.get("description", ""),
                cardinality=rt.get("cardinality", "many-to-many"),
                confidence=0.7,
                evidence_count=1,
            ))

        return entities, relationships

    def _generate_shacl_shapes(self, entity_types: list[EntityTypeProposal]) -> list[SHACLShape]:
        shapes: list[SHACLShape] = []
        for et in entity_types:
            prop_shapes = [
                SHACLPropertyShape(
                    path=p.name,
                    datatype=self._xsd_type(p.data_type),
                    min_count=1 if p.required else None,
                    max_count=1 if p.cardinality == "single" else None,
                )
                for p in et.properties
            ]
            shapes.append(SHACLShape(
                target_class=et.name,
                properties=prop_shapes,
            ))
        return shapes

    @staticmethod
    def _xsd_type(dt: str) -> str:
        return {
            "string": "string",
            "integer": "integer",
            "float": "decimal",
            "boolean": "boolean",
            "datetime": "dateTime",
            "uri": "anyURI",
        }.get(dt, "string")


class TypeConsolidationGuard:
    """Merges duplicate or near-duplicate type proposals."""

    @staticmethod
    def consolidate_entity_types(proposals: list[EntityTypeProposal]) -> list[EntityTypeProposal]:
        by_name: dict[str, list[EntityTypeProposal]] = {}
        for p in proposals:
            key = p.name.lower().replace("_", "").replace("-", "")
            by_name.setdefault(key, []).append(p)

        result: list[EntityTypeProposal] = []
        for group in by_name.values():
            if len(group) == 1:
                result.append(group[0])
                continue
            merged = group[0]
            for other in group[1:]:
                merged = TypeConsolidationGuard._merge_entity(merged, other)
            result.append(merged)
        return result

    @staticmethod
    def consolidate_relationship_types(proposals: list[RelationshipTypeProposal]) -> list[RelationshipTypeProposal]:
        by_key: dict[str, list[RelationshipTypeProposal]] = {}
        for p in proposals:
            key = f"{p.source_type}:{p.name}:{p.target_type}".lower()
            by_key.setdefault(key, []).append(p)

        result: list[RelationshipTypeProposal] = []
        for group in by_key.values():
            best = max(group, key=lambda x: x.confidence)
            best.evidence_count = sum(g.evidence_count for g in group)
            result.append(best)
        return result

    @staticmethod
    def _merge_entity(a: EntityTypeProposal, b: EntityTypeProposal) -> EntityTypeProposal:
        all_props: dict[str, PropertyProposal] = {}
        for p in a.properties + b.properties:
            key = p.name.lower()
            existing = all_props.get(key)
            if existing is None or p.confidence > existing.confidence:
                all_props[key] = p
        return EntityTypeProposal(
            name=a.name,
            description=a.description or b.description,
            properties=list(all_props.values()),
            parent_type=a.parent_type or b.parent_type,
            confidence=max(a.confidence, b.confidence),
            evidence_count=a.evidence_count + b.evidence_count,
            source_spans=a.source_spans + b.source_spans,
        )


class InductionSHACLValidator:
    """Validates induced ontology elements against SHACL shape constraints
    to prevent ontology drift."""

    def __init__(self, baseline_shapes: list[SHACLShape] | None = None) -> None:
        self._baseline: dict[str, SHACLShape] = {}
        if baseline_shapes:
            for s in baseline_shapes:
                self._baseline[s.target_class] = s

    def set_baseline(self, shapes: list[SHACLShape]) -> None:
        self._baseline = {s.target_class: s for s in shapes}

    def validate(self, proposed: list[EntityTypeProposal]) -> list[str]:
        """Validate proposed types against baseline, returning drift violations."""
        violations: list[str] = []
        for entity in proposed:
            baseline = self._baseline.get(entity.name)
            if baseline is None:
                continue
            baseline_props = {p.path for p in baseline.properties}
            proposed_props = {p.name for p in entity.properties}
            removed = baseline_props - proposed_props
            if removed:
                violations.append(
                    f"DRIFT: Entity '{entity.name}' would remove baseline properties: {removed}"
                )
            for prop in entity.properties:
                for bp in baseline.properties:
                    if bp.path == prop.name and bp.datatype:
                        expected_xsd = CorpusOntologyInducer._xsd_type(prop.data_type)
                        if expected_xsd != bp.datatype:
                            violations.append(
                                f"DRIFT: Property '{entity.name}.{prop.name}' type changed "
                                f"from '{bp.datatype}' to '{expected_xsd}'"
                            )
        return violations
