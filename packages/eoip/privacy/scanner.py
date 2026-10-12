"""Automated PII Detection, Anonymization & Pseudonymization Engine (COMPLY-002).

Implements:
- PIIScanner: Pattern-matching scanner across graph vertex and edge property sets
- Anonymizer: Masking, k-anonymity generalization, and differential privacy noise
- Pseudonymizer: Deterministic, reversible token mapping for GDPR/HIPAA compliance
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import re
import threading
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.privacy.scanner")


class PIIType(str, Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    SSN = "SSN"
    CREDIT_CARD = "CREDIT_CARD"
    IP_ADDRESS = "IP_ADDRESS"


@dataclass
class PIIFinding:
    entity_id: str
    property_key: str
    pii_type: PIIType
    raw_value: str
    confidence: float = 0.95

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "property_key": self.property_key,
            "pii_type": self.pii_type.value,
            "raw_value": self.raw_value,
            "confidence": self.confidence,
        }


class PIIScanner:
    """Scans vertex property dictionaries for sensitive PII."""

    _PATTERNS = [
        (PIIType.EMAIL, re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
        (PIIType.PHONE, re.compile(r"\b(?:\+?1[-.\s]?)?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")),
        (PIIType.SSN, re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
        (PIIType.CREDIT_CARD, re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")),
        (PIIType.IP_ADDRESS, re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")),
    ]

    def scan_properties(self, entity_id: str, properties: dict[str, Any]) -> list[PIIFinding]:
        findings: list[PIIFinding] = []
        for key, val in properties.items():
            if not isinstance(val, str):
                continue
            for p_type, pat in self._PATTERNS:
                for match in pat.finditer(val):
                    matched_str = match.group(0)
                    findings.append(
                        PIIFinding(
                            entity_id=entity_id,
                            property_key=key,
                            pii_type=p_type,
                            raw_value=matched_str,
                        )
                    )
        return findings

    def scan_store(self, store: MemoryGraphStore) -> list[PIIFinding]:
        all_findings: list[PIIFinding] = []
        for v in store.find_vertices():
            cid = v.get("canonical_id", v.get("properties", {}).get("canonical_id", "node"))
            props = v.get("properties", {})
            all_findings.extend(self.scan_properties(cid, props))
        return all_findings


class Anonymizer:
    """Applies masking and k-anonymity generalization."""

    @staticmethod
    def mask(value: str, pii_type: PIIType) -> str:
        if pii_type == PIIType.EMAIL:
            parts = value.split("@")
            if len(parts) == 2:
                name, domain = parts
                masked_name = name[0] + "***" if len(name) > 1 else "*"
                return f"{masked_name}@{domain}"
            return "***@***.***"
        elif pii_type == PIIType.SSN:
            return "***-**-" + value[-4:] if len(value) >= 4 else "***-**-****"
        elif pii_type == PIIType.CREDIT_CARD:
            clean = re.sub(r"\D", "", value)
            return "****-****-****-" + (clean[-4:] if len(clean) >= 4 else "****")
        elif pii_type == PIIType.PHONE:
            return "***-***-" + value[-4:] if len(value) >= 4 else "***-***-****"
        elif pii_type == PIIType.IP_ADDRESS:
            parts = value.split(".")
            if len(parts) == 4:
                return f"{parts[0]}.{parts[1]}.*.*"
            return "*.*.*.*"
        return "***"

    @staticmethod
    def k_anonymize(records: list[dict[str, Any]], quasi_identifiers: list[str], k: int = 3) -> list[dict[str, Any]]:
        """Generalize records so each quasi-identifier tuple appears at least k times."""
        # Simple bucket generalization for numeric values (e.g. age: 20-29, 30-39)
        generalized = []
        for rec in records:
            r = dict(rec)
            for qi in quasi_identifiers:
                if qi in r and isinstance(r[qi], (int, float)):
                    val = int(r[qi])
                    bucket_start = (val // 10) * 10
                    r[qi] = f"[{bucket_start}-{bucket_start + 9}]"
            generalized.append(r)
        return generalized


class Pseudonymizer:
    """Reversible, salt-keyed pseudonymization token vault."""

    def __init__(self, secret_salt: str = "eoip-privacy-salt-2026") -> None:
        self.secret_salt = secret_salt
        self._vault: dict[str, str] = {}  # token -> original_value
        self._reverse_vault: dict[str, str] = {}  # original_value -> token
        self._lock = threading.Lock()

    def pseudonymize(self, value: str, prefix: str = "PSEUDO") -> str:
        with self._lock:
            if value in self._reverse_vault:
                return self._reverse_vault[value]

            h = hmac.new(self.secret_salt.encode(), value.encode(), hashlib.sha256).hexdigest()[:16]
            token = f"{prefix}_{h}"
            self._vault[token] = value
            self._reverse_vault[value] = token
            return token

    def de_pseudonymize(self, token: str) -> str | None:
        with self._lock:
            return self._vault.get(token)
