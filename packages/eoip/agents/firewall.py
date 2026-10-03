"""Knowledge firewall for untrusted source content entering agent context."""

from __future__ import annotations

import re
from dataclasses import dataclass

from eoip.contracts.agent import RuleDecision

_SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
)
_INJECTION_PATTERNS = (
    re.compile(r"(?i)ignore\s+(all\s+)?previous\s+instructions"),
    re.compile(r"(?i)system\s+prompt"),
    re.compile(r"(?i)(execute|run)\s+(this\s+)?(command|tool|script)"),
)


@dataclass(frozen=True)
class FirewallResult:
    content: str
    decisions: list[RuleDecision]
    untrusted: bool = True


class KnowledgeFirewall:
    """Labels source content as data, redacts secrets, and flags injection text."""

    def inspect(self, content: str) -> FirewallResult:
        redacted = content
        decisions: list[RuleDecision] = []
        for pattern in _SECRET_PATTERNS:
            if pattern.search(redacted):
                redacted = pattern.sub("[REDACTED]", redacted)
                decisions.append(RuleDecision(
                    rule_id="KFW-SECRET-REDACTION",
                    outcome="REDACT",
                    summary="Secret-like source content was removed before agent use.",
                ))
        if any(pattern.search(redacted) for pattern in _INJECTION_PATTERNS):
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
        return FirewallResult(content=redacted, decisions=decisions)
