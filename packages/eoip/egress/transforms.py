"""Payload transforms down to a permitted sharing level (SR-LLM-011, SR-LLM-015).

Implements the §10.2 Dimension-B ladder:

* S1 schema-strip  — ontology/type names and field names, no values.
* S2 aggregate     — counts/statistics with k-anonymity small-cell suppression.
* S3 synthetic     — shape-preserving generated stand-ins (configured template
                     transform; generative synthetic data is ADR-gated).
* S4 tokenize      — reversible vault tokens (SR-LLM-015).
* S5 redact        — DLP-masked minimal passages via the regex scanner.
* S6 exact preview — payload passes through unchanged but requires a recorded
                     per-request human approval (SR-LLM-012).
* S7 full          — pass-through (only for tenant-designated shareable data).
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from eoip.egress.dlp import DlpScanner
from eoip.egress.policy import SharingLevel
from eoip.egress.vault import TokenVault

K_ANONYMITY_DEFAULT = 5  # small-cell suppression threshold for S2


class TransformError(Exception):
    """Raised when a payload cannot be brought to the required level."""


def _schema_of(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "string"


def schema_strip(payload: dict) -> dict:
    """S1: field names + type names only, no values."""
    return {key: {"type": _schema_of(value)} for key, value in payload.items()}


def aggregate(payload: dict, *, k: int = K_ANONYMITY_DEFAULT) -> dict:
    """S2: counts/statistics per field with small-cell suppression.

    Scalars become presence counts of their class; lists become element
    frequency counts (cells below ``k`` suppressed); dicts aggregate to
    their number of keys.
    """
    out: dict[str, Any] = {}
    for key, value in payload.items():
        if isinstance(value, list):
            counts: dict[str, int] = {}
            for item in value:
                label = _schema_of(item) if not isinstance(item, (str, int, float, bool)) else str(item)
                counts[label] = counts.get(label, 0) + 1
            out[key] = {
                "count": len(value),
                "distinct": sum(1 for c in counts.values() if c >= k),
                "suppressed_cells": sum(1 for c in counts.values() if c < k),
                "k": k,
            }
        elif isinstance(value, dict):
            out[key] = {"type": "object", "keys": len(value)}
        else:
            out[key] = {"type": _schema_of(value), "count": 1}
    return out


def synthetic(payload: dict, *, seed: str = "eoip") -> dict:
    """S3: shape-preserving synthetic stand-ins, never derived 1:1 from records.

    Uses deterministic type-shaped placeholders hashed with a local seed.
    ADR-gated: real generative synthetic data (shape-preserving models)
    replaces these placeholders when that capability lands.
    """
    def gen(value: Any, path: str) -> Any:
        digest = hashlib.sha256(f"{seed}:{path}".encode()).hexdigest()
        if isinstance(value, bool):
            return bool(int(digest[0], 16) % 2)
        if isinstance(value, int):
            return int(digest[:8], 16)
        if isinstance(value, float):
            return int(digest[:8], 16) / 1e6
        if isinstance(value, list):
            return [gen(v, f"{path}[{i}]") for i, v in enumerate(value)]
        if isinstance(value, dict):
            return {k2: gen(v2, f"{path}.{k2}") for k2, v2 in value.items()}
        return f"syn_{digest[:12]}"
    return {key: gen(value, key) for key, value in payload.items()}


def tokenize(payload: dict, vault: TokenVault) -> dict:
    """S4: replace every string leaf with a reversible vault token."""

    def tok(value: Any, path: str) -> Any:
        if isinstance(value, str):
            return vault.tokenize(value, field=path)
        if isinstance(value, list):
            return [tok(v, f"{path}[{i}]") for i, v in enumerate(value)]
        if isinstance(value, dict):
            return {k2: tok(v2, f"{path}.{k2}") for k2, v2 in value.items()}
        return value

    return {key: tok(value, key) for key, value in payload.items()}


_REDACTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[EMAIL]"),
    (re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b"), "[PHONE]"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
    (re.compile(r"\b(?:\d[ -]*?){13,19}\b"), "[CARD]"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|password|token|private[_-]?key)\b\s*[:=]\s*\S+"),
     lambda m: m.group(1) + "=[REDACTED]"),  # type: ignore[dict-item]
]


def redact(payload: dict, scanner: DlpScanner | None = None) -> dict:
    """S5: DLP-mask every sensitive leaf, keeping structure."""

    def redact_str(value: str) -> str:
        for pattern, replacement in _REDACTION_PATTERNS:
            value = pattern.sub(replacement, value)  # type: ignore[arg-type]
        return value

    def rec(value: Any) -> Any:
        if isinstance(value, str):
            return redact_str(value)
        if isinstance(value, list):
            return [rec(v) for v in value]
        if isinstance(value, dict):
            return {k2: rec(v2) for k2, v2 in value.items()}
        return value

    return {key: rec(value) for key, value in payload.items()}


def transform(payload: dict, level: SharingLevel, *,
              vault: TokenVault | None = None,
              k: int = K_ANONYMITY_DEFAULT) -> dict:
    """Apply the transform for ``level`` to ``payload`` (SR-LLM-011).

    S0 raises (nothing may leave); S6/S7 pass through unchanged (S6's
    protection is the recorded approval, not a transform).
    """
    if level == SharingLevel.S0:
        raise TransformError("S0: nothing may leave the boundary")
    if level in (SharingLevel.S6, SharingLevel.S7):
        return payload
    if level == SharingLevel.S1:
        return schema_strip(payload)
    if level == SharingLevel.S2:
        return aggregate(payload, k=k)
    if level == SharingLevel.S3:
        return synthetic(payload)
    if level == SharingLevel.S4:
        if vault is None:
            raise TransformError("S4 tokenization requires a token vault")
        return tokenize(payload, vault)
    if level == SharingLevel.S5:
        return redact(payload)
    raise TransformError(f"unsupported level {level}")
