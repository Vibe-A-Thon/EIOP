"""Outbound DLP scanning and canary registry (SR-LLM-014).

Every payload that would leave the boundary is scanned for PII/secret/PHI
patterns, high-entropy candidate secrets, and customer-defined dictionary
terms. A canary registry holds planted canary values (CI plants them in
test tenants): if a canary value would egress below its allowed level the
scan fails — CI fails the build on any such finding.

External gate: richer detectors (NER models, presidio-style analyzers)
are ADR-gated; this module is stdlib regex + Shannon entropy only.
"""

from __future__ import annotations

import math
import re
import time
import uuid
from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Detectors
# ---------------------------------------------------------------------------

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("PHONE", re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")),
    ("CREDIT_CARD",
     re.compile(r"\b(?:\d[ -]*?){13,19}\b")),
    ("SECRET_ASSIGNMENT",
     re.compile(r"(?i)\b(api[_-]?key|secret|password|token|key|private[_-]?key)\b\s*[:=]\s*\S+")),
    ("AWS_ACCESS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")),
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("IP_ADDRESS", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
]

_ENTROY_MIN_LEN = 20
_ENTROPY_THRESHOLD = 4.2  # Shannon bits/char; classic secret-detector cut-off


def _shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts: dict[str, int] = {}
    for ch in value:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(value)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


@dataclass
class DlpFinding:
    detector: str
    matched: str
    # Byte offsets within the serialized payload (approximate; regex-based).
    start: int
    end: int


@dataclass
class DlpReport:
    clean: bool
    findings: list[DlpFinding] = field(default_factory=list)
    canary_hits: list[str] = field(default_factory=list)


class DlpScanner:
    """Regex + entropy + dictionary scanner over the exact egress payload."""

    def __init__(self, dictionary_terms: list[str] | None = None) -> None:
        self.dictionary_terms = [t for t in (dictionary_terms or []) if t]

    def scan_text(self, text: str) -> list[DlpFinding]:
        findings: list[DlpFinding] = []
        for name, pattern in _PATTERNS:
            for m in pattern.finditer(text):
                findings.append(DlpFinding(name, m.group(0), m.start(), m.end()))
        # Entropy pass on long tokens that weren't already pattern-matched.
        for m in re.finditer(r"[A-Za-z0-9+/=_-]{%d,}" % _ENTROY_MIN_LEN, text):
            if _shannon_entropy(m.group(0)) >= _ENTROPY_THRESHOLD:
                if not any(f.start <= m.start() < f.end for f in findings):
                    findings.append(DlpFinding("HIGH_ENTROPY", m.group(0), m.start(), m.end()))
        for term in self.dictionary_terms:
            start = 0
            while (idx := text.find(term, start)) >= 0:
                findings.append(DlpFinding("DICTIONARY", term, idx, idx + len(term)))
                start = idx + 1
        return findings

    def scan(self, payload: dict) -> DlpReport:
        text = _serialize(payload)
        findings = self.scan_text(text)
        return DlpReport(clean=not findings, findings=findings)


def _serialize(payload: dict) -> str:
    import json

    return json.dumps(payload, sort_keys=True, default=str)


# ---------------------------------------------------------------------------
# Canary registry
# ---------------------------------------------------------------------------


class CanaryRecord(BaseModel):
    """A planted canary value and the minimum level at which it may egress."""

    model_config = ConfigDict(extra="forbid")

    canary_id: str
    value: str
    min_level: int = 8  # default: canaries may never leave (S7 is the max level)
    planted_by: str = "ci"
    planted_at: float = Field(default_factory=time.time)


class CanaryRegistry:
    """Planted canary values; block egress that would leak them (SR-LLM-014)."""

    def __init__(self) -> None:
        self._canaries: dict[str, CanaryRecord] = {}

    def plant(self, value: str, *, min_level: int = 8,
              planted_by: str = "ci", canary_id: str | None = None) -> CanaryRecord:
        record = CanaryRecord(
            canary_id=canary_id or f"urn:eoip:egress:canary:{uuid.uuid4().hex[:12]}",
            value=value,
            min_level=min_level,
            planted_by=planted_by,
        )
        self._canaries[record.canary_id] = record
        return record

    def check(self, payload: dict, egress_level: int) -> list[CanaryRecord]:
        """Return canaries that would egress at a level below their minimum."""
        text = _serialize(payload)
        hits = [
            record for record in self._canaries.values()
            if egress_level < record.min_level and record.value in text
        ]
        return hits

    def remove(self, canary_id: str) -> None:
        self._canaries.pop(canary_id, None)

    def __len__(self) -> int:
        return len(self._canaries)
