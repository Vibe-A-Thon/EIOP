"""Relation Extraction & Triple Generation Engine (AI-003).

Automates Subject-Predicate-Object triple generation from unstructured text:
- Pattern-based relation extraction with configurable rules
- Triple validation against ontology constraints
- Deduplication and entity normalization
- Feeds Knowledge Graph construction pipeline (AGENT-002)
"""

from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any

logger = logging.getLogger("eoip.extraction.relation_extractor")


@dataclass
class RelationPattern:
    """Configurable extraction pattern for subject-predicate-object triples."""

    predicate: str
    pattern: str  # Regex with (?P<subja>...) and (?P<obj>...) groups
    subject_type: str = "Entity"
    object_type: str = "Entity"
    confidence: float = 0.85


@dataclass
class ExtractedTriple:
    """A verified (subject, predicate, object) knowledge triple."""

    subject: str
    predicate: str
    object: str
    subject_type: str = "Entity"
    object_type: str = "Entity"
    confidence: float = 0.85
    evidence_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def canonical_key(self) -> str:
        s = re.sub(r"\W+", "_", self.subject.strip().lower())
        p = re.sub(r"\W+", "_", self.predicate.strip().lower())
        o = re.sub(r"\W+", "_", self.object.strip().lower())
        return f"{s}:{p}:{o}"


class TripleValidator:
    """Validates extracted triples against schema and sanity rules."""

    def __init__(self, allowed_predicates: set[str] | None = None) -> None:
        self.allowed_predicates = allowed_predicates

    def is_valid(self, triple: ExtractedTriple) -> bool:
        if not triple.subject or not triple.predicate or not triple.object:
            return False
        if len(triple.subject.strip()) < 2 or len(triple.object.strip()) < 2:
            return False
        if triple.subject.strip().lower() == triple.object.strip().lower():
            return False  # Avoid self-loops by default
        if self.allowed_predicates and triple.predicate.lower() not in self.allowed_predicates:
            return False
        return True


class TripleDeduplicator:
    """Merges and deduplicates near-identical triples, keeping highest confidence."""

    def deduplicate(self, triples: list[ExtractedTriple]) -> list[ExtractedTriple]:
        unique: dict[str, ExtractedTriple] = {}
        for t in triples:
            key = t.canonical_key
            if key not in unique or t.confidence > unique[key].confidence:
                unique[key] = t
        return list(unique.values())


class RelationExtractor:
    """Extracts typed knowledge graph triples from raw sentences."""

    def __init__(self, custom_patterns: list[RelationPattern] | None = None) -> None:
        self.validator = TripleValidator()
        self.deduplicator = TripleDeduplicator()
        self.patterns = custom_patterns or self._default_patterns()

    def _default_patterns(self) -> list[RelationPattern]:
        return [
            # "X depends on Y"
            RelationPattern(
                predicate="DEPENDS_ON",
                pattern=r"(?P<sub>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)\s+(?:depends on|relies on|requires)\s+(?P<obj>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)",
                confidence=0.92,
            ),
            # "X is a part of Y"
            RelationPattern(
                predicate="PART_OF",
                pattern=r"(?P<sub>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)\s+is\s+(?:a\s+)?part\s+of\s+(?P<obj>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)",
                confidence=0.88,
            ),
            # "X owns Y"
            RelationPattern(
                predicate="OWNS",
                pattern=r"(?P<sub>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)\s+(?:owns|manages|maintains)\s+(?P<obj>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)",
                confidence=0.89,
            ),
            # "X communicates with Y" / "calls"
            RelationPattern(
                predicate="CALLS",
                pattern=r"(?P<sub>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)\s+(?:calls|invokes|queries)\s+(?P<obj>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)",
                confidence=0.91,
            ),
            # General "X is a Y"
            RelationPattern(
                predicate="IS_A",
                pattern=r"(?P<sub>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)\s+is\s+(?:an?|the)\s+(?P<obj>[A-Z][\w\.\-]+(?:\s+[A-Z][\w\.\-]+)*)",
                confidence=0.82,
            ),
        ]

    def extract_triples(self, text: str) -> list[ExtractedTriple]:
        """Extract subject-predicate-object triples from text."""
        raw_triples: list[ExtractedTriple] = []
        sentences = [s.strip() for s in re.split(r"[.\n;]+", text) if len(s.strip()) > 5]

        for sentence in sentences:
            for pat in self.patterns:
                for match in re.finditer(pat.pattern, sentence, re.IGNORECASE):
                    sub = match.group("sub").strip()
                    obj = match.group("obj").strip()
                    triple = ExtractedTriple(
                        subject=sub,
                        predicate=pat.predicate,
                        object=obj,
                        subject_type=pat.subject_type,
                        object_type=pat.object_type,
                        confidence=pat.confidence,
                        evidence_text=sentence,
                    )
                    if self.validator.is_valid(triple):
                        raw_triples.append(triple)

        return self.deduplicator.deduplicate(raw_triples)
