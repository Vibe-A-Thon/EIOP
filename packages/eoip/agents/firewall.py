"""Knowledge firewall for untrusted source content entering agent context.

Implements:
- GAP-KFW-001: inspect context crossing a knowledge boundary.
- GAP-KFW-002: detect secrets, PII, credentials, regulated data, and restricted classifications.
- GAP-KFW-003: block or redact based on policy.
- GAP-KFW-004: prevent source text from becoming executable agent instructions.
- GAP-KFW-005: tag untrusted/externally sourced graph content.
- GAP-KFW-006: defend against semantic prompt injection.
- GAP-KFW-007: maintain security provenance.
- GAP-KFW-008: explain why content was blocked or redacted.
- GAP-AGOV-006: prompt-injection detection.
- GAP-AGOV-007: tool-output sanitization.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from eoip.contracts.agent import RuleDecision
from eoip.contracts.source_event import utc_now_iso

_SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
)
_PII_PATTERNS = (
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
)
_RESTRICTED_PATTERNS = (
    re.compile(r"(?i)\b(export\s+controlled|itar|hipaa|pci|restricted|confidential)\b"),
)
_INJECTION_PATTERNS = (
    re.compile(r"(?i)ignore\s+(all\s+)?previous\s+instructions"),
    re.compile(r"(?i)system\s+prompt"),
    re.compile(r"(?i)(execute|run)\s+(this\s+)?(command|tool|script)"),
    re.compile(r"(?i)\b(exfiltrate|leak|dump)\b.*\b(secret|token|credential|prompt)\b"),
)


@dataclass(frozen=True)
class FirewallResult:
    content: str
    decisions: list[RuleDecision]
    untrusted: bool = True
    blocked: bool = False
    classifications: tuple[str, ...] = ()
    boundary: str = "agent_context"
    provenance: dict | None = None


class KnowledgeFirewall:
    """Labels source content as data, redacts secrets, and flags injection text."""

    def inspect(
        self,
        content: str,
        *,
        boundary: str = "agent_context",
        source_ref: str | None = None,
        block_on_restricted: bool = False,
    ) -> FirewallResult:
        redacted = content
        decisions: list[RuleDecision] = []
        classifications: set[str] = set()
        for pattern in _SECRET_PATTERNS:
            if pattern.search(redacted):
                redacted = pattern.sub("[REDACTED]", redacted)
                classifications.add("secret")
                decisions.append(RuleDecision(
                    rule_id="KFW-SECRET-REDACTION",
                    outcome="REDACT",
                    summary="Secret-like source content was removed before agent use.",
                ))
        for pattern in _PII_PATTERNS:
            if pattern.search(redacted):
                redacted = pattern.sub("[REDACTED-PII]", redacted)
                classifications.add("pii")
                decisions.append(RuleDecision(
                    rule_id="KFW-PII-REDACTION",
                    outcome="REDACT",
                    summary="PII-like source content was removed before boundary crossing.",
                ))
        restricted = any(pattern.search(redacted) for pattern in _RESTRICTED_PATTERNS)
        if restricted:
            classifications.add("restricted")
            decisions.append(RuleDecision(
                rule_id="KFW-RESTRICTED-DATA",
                outcome="BLOCK" if block_on_restricted else "WARN",
                summary=(
                    "Restricted-classification source content was blocked by policy."
                    if block_on_restricted
                    else "Restricted-classification source content was tagged for policy review."
                ),
            ))
        if any(pattern.search(redacted) for pattern in _INJECTION_PATTERNS):
            classifications.add("prompt_injection")
            decisions.append(RuleDecision(
                rule_id="KFW-PROMPT-INJECTION",
                outcome="WARN",
                summary="Instruction-like source text was treated only as untrusted data.",
            ))
        if not decisions:
            decisions.append(RuleDecision(
                rule_id="KFW-UNTRUSTED-DATA",
                outcome="ALLOW",
                summary="Source content was admitted as untrusted evidence, not instructions.",
            ))
        blocked = any(decision.outcome == "BLOCK" for decision in decisions)
        return FirewallResult(
            content="" if blocked else redacted,
            decisions=decisions,
            blocked=blocked,
            classifications=tuple(sorted(classifications or {"unclassified"})),
            boundary=boundary,
            provenance={
                "boundary": boundary,
                "source_ref": source_ref,
                "inspected_at": utc_now_iso(),
                "untrusted": True,
            },
        )
