"""LLM guardrails behind the Model Provider Port (SR-LLM-009).

* Input scanners: prompt-injection / jailbreak patterns and secrets block the call; PII is redacted
  from the prompt unless the tenant policy allows raw PII.
* Output scanners: PII and secrets in model output are redacted before display; active content
  (script/html event handlers) is neutralised (OWASP LLM05 improper output handling).
* Tool allowlists per tenant: a request asking for a tool outside the allowlist is blocked
  (OWASP LLM06 excessive agency).
* Output schema validation is enforced by ``ModelPort`` when the request carries a JSON Schema.
* ``tests/fixtures/llm_guardrail_corpus.json`` is the jailbreak/prompt-injection corpus, tagged with
  OWASP LLM Top-10 (2025) categories, run in CI by ``tests/unit/test_model_port.py``.
"""

from __future__ import annotations

import json
import re
from typing import Any

from eoip.ai.graphrag import PromptInjectionFence
from eoip.egress.dlp import DlpScanner

SECRET_DETECTORS = frozenset({"SECRET_ASSIGNMENT", "AWS_ACCESS_KEY", "JWT"})

INJECTION_PATTERNS = [*PromptInjectionFence.FORBIDDEN_INJECTION_PATTERNS, *[re.compile(p, re.IGNORECASE) for p in (
    r"(ignore|disregard|forget)\s+(all\s+|any\s+)?(prior|previous|above|earlier)\s+(instructions|rules|directions)",
    r"\bDAN\b|do\s+anything\s+now",
    r"(reveal|print|show|repeat|output)\s+(me\s+)?(your|the)\s+(system\s+prompt|hidden\s+instructions|initial\s+prompt)",
    r"pretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(unrestricted|unfiltered|jailbroken)",
    r"you\s+(have|now\s+have)\s+no\s+(restrictions|rules|guidelines)",
    r"</?\s*(system|assistant)\s*>",
    r"act\s+as\s+(my\s+)?(root|admin|sudo)",
)]]
_ACTIVE_CONTENT = re.compile(r"<\s*script\b[^>]*>.*?<\s*/\s*script\s*>|\bon\w+\s*=\s*\"[^\"]*\"|javascript:",
                             re.IGNORECASE | re.DOTALL)


class GuardrailBlocked(PermissionError):
    def __init__(self, reason: str, triggers: list[str]) -> None:
        super().__init__(reason)
        self.triggers = triggers


class Guardrails:
    def __init__(self, *, scanner: DlpScanner | None = None, allow_raw_pii: set[str] | None = None,
                 redact_pii: bool = True) -> None:
        self.scanner = scanner or DlpScanner()
        # False for local-only deployments: PII stays inside the tenant, secrets/injection still blocked
        self.redact_pii = redact_pii
        self.tool_allowlists: dict[str, set[str]] = {}
        self.allow_raw_pii = allow_raw_pii or set()  # tenants whose policy allows raw PII in prompts

    def set_tool_allowlist(self, tenant_id: str, tools: set[str]) -> None:
        self.tool_allowlists[tenant_id] = set(tools)

    @staticmethod
    def _text(value: Any) -> str:
        return value if isinstance(value, str) else json.dumps(value, sort_keys=True, default=str)

    def injection_hits(self, text: str) -> list[str]:
        return [p.pattern for p in INJECTION_PATTERNS if p.search(text)]

    def check_input(self, request: Any) -> list[str]:
        text = self._text(request.input)
        triggers: list[str] = []
        if self.injection_hits(text):
            raise GuardrailBlocked("prompt injection / jailbreak pattern in input", ["input:injection"])
        findings = self.scanner.scan_text(text)
        secrets = sorted({f.detector for f in findings if f.detector in SECRET_DETECTORS})
        if secrets:
            raise GuardrailBlocked("secret material in model input", [f"input:secret:{d}" for d in secrets])
        pii = sorted({f.detector for f in findings} - SECRET_DETECTORS)
        if pii and self.redact_pii and request.tenant_id not in self.allow_raw_pii:
            request.input = self._redact(request.input)
            triggers += [f"input:pii_redacted:{d}" for d in pii]
        allowed = self.tool_allowlists.get(request.tenant_id, set())
        denied = sorted(set(request.tools) - allowed)
        if denied:
            raise GuardrailBlocked(f"tools not on the tenant allowlist: {denied}", [f"tool:denied:{t}" for t in denied])
        return triggers

    def check_output(self, output: Any) -> tuple[Any, list[str]]:
        triggers: list[str] = []
        detectors = sorted({f.detector for f in self.scanner.scan_text(self._text(output))
                            if self.redact_pii or f.detector in SECRET_DETECTORS})
        if detectors:
            output = self._redact(output)
            triggers += [f"output:redacted:{d}" for d in detectors]
        if _ACTIVE_CONTENT.search(self._text(output)):
            output = self._neutralise(output)
            triggers.append("output:active_content")
        return output, triggers

    def _map(self, value: Any, fn) -> Any:
        if isinstance(value, str):
            return fn(value)
        if isinstance(value, list):
            return [self._map(v, fn) for v in value]
        if isinstance(value, dict):
            return {k: self._map(v, fn) for k, v in value.items()}
        return value

    def _redact(self, value: Any) -> Any:
        def red(s: str) -> str:
            found = [f for f in self.scanner.scan_text(s) if self.redact_pii or f.detector in SECRET_DETECTORS]
            for f in sorted(found, key=lambda f: -len(f.matched)):
                s = s.replace(f.matched, f"[REDACTED:{f.detector}]")
            return s
        return self._map(value, red)

    def _neutralise(self, value: Any) -> Any:
        return self._map(value, lambda s: _ACTIVE_CONTENT.sub("[ACTIVE_CONTENT_REMOVED]", s))
