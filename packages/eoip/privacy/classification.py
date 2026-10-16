"""Privacy classification engine at ingest (SR-PRV-001).

Labels payloads with sensitivity classes — PII, PHI, PCI, SECRET,
IP, LEGAL_PRIVILEGED, EXPORT_CONTROLLED — using three detector
families:

* **pattern** detectors: regular expressions (emails, card numbers,
  national IDs, API keys, ...);
* **dictionary** detectors: customer-supplied word lists (e.g. diagnosis
  names, project codenames);
* **entropy** detectors: high-entropy token-like strings that look like
  secrets without matching a known pattern.

Customers can register additional rules on top of the built-in set
(customer-extensible, SR-PRV-001). NER/ML detectors are ADR-gated:
they need a model-runtime dependency that the base package deliberately
does not carry.

Labels propagate to derived records: anything derived from classified
source data inherits the source's labels (union), so embeddings, search
documents and summaries stay tagged for downstream policy enforcement.
"""

from __future__ import annotations

import math
import re
from enum import Enum
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SensitivityLabel(str, Enum):
    PII = "PII"
    PHI = "PHI"
    PCI = "PCI"
    SECRET = "SECRET"
    IP = "IP"
    LEGAL_PRIVILEGED = "LEGAL_PRIVILEGED"
    EXPORT_CONTROLLED = "EXPORT_CONTROLLED"


class DetectorKind(str, Enum):
    PATTERN = "pattern"
    DICTIONARY = "dictionary"
    ENTROPY = "entropy"


class DetectorRule(BaseModel):
    """One customer-extensible detection rule (SR-PRV-001)."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    kind: DetectorKind
    labels: list[SensitivityLabel] = Field(min_length=1)
    pattern: str | None = None
    terms: list[str] = Field(default_factory=list)
    min_entropy: float = Field(default=0.0, ge=0.0, le=8.0)
    min_token_length: int = Field(default=16, ge=4)

    @model_validator(mode="after")
    def _check_shape(self) -> DetectorRule:
        self.compile()
        return self

    def compile(self) -> DetectorRule:
        if self.kind == DetectorKind.PATTERN:
            if not self.pattern:
                raise ValueError("pattern rule requires a pattern")
            try:
                re.compile(self.pattern)
            except re.error as exc:
                raise ValueError(f"invalid regex: {exc}") from exc
        if self.kind == DetectorKind.DICTIONARY and not self.terms:
            raise ValueError("dictionary rule requires terms")
        return self


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts: dict[str, int] = {}
    for ch in value:
        counts[ch] = counts.get(ch, 0) + 1
    length = len(value)
    return -sum((n / length) * math.log2(n / length) for n in counts.values())


class ClassifiedField(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_path: str
    labels: list[SensitivityLabel]
    matched_by: list[str] = Field(default_factory=list, description="Names of rules that matched")


class ClassificationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_ref: str
    tenant_id: str | None = None
    labels: list[SensitivityLabel] = Field(default_factory=list)
    fields: list[ClassifiedField] = Field(default_factory=list)

    def propagate(self) -> list[SensitivityLabel]:
        """Labels that derived records must inherit (SR-PRV-001 propagation)."""
        return sorted(set(self.labels), key=lambda l: l.value)


_BUILTIN_RULES: list[DetectorRule] = [
    DetectorRule(
        name="email",
        kind=DetectorKind.PATTERN,
        labels=[SensitivityLabel.PII],
        pattern=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    ),
    DetectorRule(
        name="credit_card_luhn_shape",
        kind=DetectorKind.PATTERN,
        labels=[SensitivityLabel.PCI],
        pattern=r"\b(?:\d[ -]*?){13,19}\b",
    ),
    DetectorRule(
        name="us_ssn",
        kind=DetectorKind.PATTERN,
        labels=[SensitivityLabel.PII],
        pattern=r"\b\d{3}-\d{2}-\d{4}\b",
    ),
    DetectorRule(
        name="api_key_assignment",
        kind=DetectorKind.PATTERN,
        labels=[SensitivityLabel.SECRET],
        pattern=r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"]?[^\s'\"]{8,}",
    ),
    DetectorRule(
        name="private_key_block",
        kind=DetectorKind.PATTERN,
        labels=[SensitivityLabel.SECRET],
        pattern=r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    ),
    DetectorRule(
        name="hipaa_medical_terms",
        kind=DetectorKind.DICTIONARY,
        labels=[SensitivityLabel.PHI],
        terms=["diagnosis", "prescription", "patient", "icd-10", "cpt code", "prognosis"],
    ),
    DetectorRule(
        name="ip_address",
        kind=DetectorKind.PATTERN,
        labels=[SensitivityLabel.IP],
        pattern=r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    ),
    DetectorRule(
        name="export_control_marker",
        kind=DetectorKind.DICTIONARY,
        labels=[SensitivityLabel.EXPORT_CONTROLLED],
        terms=["export controlled", "ear99", "itar", "eccn"],
    ),
    DetectorRule(
        name="attorney_client",
        kind=DetectorKind.DICTIONARY,
        labels=[SensitivityLabel.LEGAL_PRIVILEGED],
        terms=["attorney-client privilege", "privileged & confidential", "work product"],
    ),
    DetectorRule(
        name="high_entropy_token",
        kind=DetectorKind.ENTROPY,
        labels=[SensitivityLabel.SECRET],
        min_entropy=4.0,
        min_token_length=20,
    ),
]

_TOKEN_RE = re.compile(r"[A-Za-z0-9+/=_-]+")


def _iter_strings(value: Any, path: str = "") -> Any:
    """Yield (field_path, string_value) pairs from a nested payload."""
    if isinstance(value, str):
        yield path or "$", value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _iter_strings(item, f"{path}.{key}" if path else str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from _iter_strings(item, f"{path}[{index}]")


class ClassificationEngine:
    """Applies built-in + customer detector rules to ingest payloads (SR-PRV-001)."""

    def __init__(self, rules: list[DetectorRule] | None = None, include_builtin: bool = True):
        self._rules: list[DetectorRule] = []
        if include_builtin:
            for rule in _BUILTIN_RULES:
                self.register(rule)
        for rule in rules or []:
            self.register(rule)

    def register(self, rule: DetectorRule) -> None:
        """Register a customer-extensible rule (SR-PRV-001)."""
        self._rules.append(rule.compile())

    @property
    def rules(self) -> list[DetectorRule]:
        return list(self._rules)

    def _match(self, text: str) -> tuple[set[SensitivityLabel], list[str]]:
        labels: set[SensitivityLabel] = set()
        matched: list[str] = []
        lowered = text.lower()
        for rule in self._rules:
            hit = False
            if rule.kind == DetectorKind.PATTERN and rule.pattern:
                hit = re.search(rule.pattern, text) is not None
            elif rule.kind == DetectorKind.DICTIONARY:
                hit = any(term in lowered for term in rule.terms)
            elif rule.kind == DetectorKind.ENTROPY:
                hit = any(
                    len(tok) >= rule.min_token_length and shannon_entropy(tok) >= rule.min_entropy
                    for tok in _TOKEN_RE.findall(text)
                )
            if hit:
                labels.update(rule.labels)
                matched.append(rule.name)
        return labels, matched

    def classify(self, payload: dict, *, source_ref: str = "", tenant_id: str | None = None) -> ClassificationResult:
        """Classify an ingest payload; every string field is scanned."""
        all_labels: set[SensitivityLabel] = set()
        fields: list[ClassifiedField] = []
        for path, text in _iter_strings(payload):
            labels, matched = self._match(text)
            if labels:
                all_labels.update(labels)
                fields.append(ClassifiedField(field_path=path, labels=sorted(labels, key=lambda l: l.value), matched_by=matched))
        return ClassificationResult(
            source_ref=source_ref,
            tenant_id=tenant_id,
            labels=sorted(all_labels, key=lambda l: l.value),
            fields=fields,
        )


class DerivedRecord(Protocol):
    """Anything derived from classified source data (embeddings, summaries)."""

    source_ref: str


def propagate_labels(result: ClassificationResult, derived: list[dict]) -> list[dict]:
    """Return derived records tagged with the source's labels (SR-PRV-001).

    Each derived record dict gains a ``sensitivity_labels`` list (union of
    what it already had and the source's labels).
    """
    labels = [label.value for label in result.propagate()]
    out: list[dict] = []
    for record in derived:
        merged = {label for label in record.get("sensitivity_labels", [])}
        merged.update(labels)
        tagged = dict(record)
        tagged["sensitivity_labels"] = sorted(merged)
        out.append(tagged)
    return out
