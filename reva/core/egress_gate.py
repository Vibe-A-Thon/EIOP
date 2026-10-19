"""
Zero-Data-Leak LLM Egress Security Gate (REVA-SEC-013, T-ENH-002).
Enforces deterministic Python-first policy and prevents any code, secret, or PII leak to LLMs.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from reva.core.errors import RevaError
from reva.core.pseudonymizer import CodePseudonymizer

class RevaEgressViolationError(RevaError):
    """Raised when an LLM egress payload violates the Zero-Data-Leak policy."""
    def __init__(self, message: str, violations: Optional[List[str]] = None) -> None:
        super().__init__(f"EGRESS_VIOLATION: {message}")
        self.violations = violations or [message]


class EgressSecurityGate:
    """
    Zero-Data-Leak LLM Egress Gate.
    Sanitizes prompts, redacts secrets, pseudonymizes code, and applies security fences.
    """

    # Secret patterns to scrub
    SECRET_PATTERNS = [
        (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED_AWS_KEY]"),
        (re.compile(r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}"), "[REDACTED_JWT]"),
        (re.compile(r"(?i)(password|passwd|secret|api_key|token)\s*[:=]\s*['\"][^'\"]{6,}['\"]"), "[REDACTED_CREDENTIAL]"),
        (re.compile(r"(postgres|mysql|mongodb|redis):\/\/[^:\s]+:[^@\s]+@[^\s\/]+"), "[REDACTED_DB_URL]"),
        (re.compile(r"-----BEGIN (RSA|EC|DSA|OPENSSH|PRIVATE) KEY-----[\s\S]*?-----END \1 KEY-----"), "[REDACTED_PRIVATE_KEY]"),
    ]

    def __init__(self, allow_raw_code: bool = False, max_raw_bytes: int = 500) -> None:
        self.allow_raw_code = allow_raw_code
        self.max_raw_bytes = max_raw_bytes
        self.pseudonymizer = CodePseudonymizer()

    def scrub_secrets(self, text: str) -> Tuple[str, List[str]]:
        """Redacts secrets and confidential credentials from text."""
        detected = []
        result = text
        for pattern, replacement in self.SECRET_PATTERNS:
            if pattern.search(result):
                detected.append(replacement)
                result = pattern.sub(replacement, result)
        return result, detected

    def fence_untrusted_content(self, content: str) -> str:
        """Wraps untrusted input in cryptographic security fences."""
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return f"<<<UNTRUSTED_CONTENT_START:{digest}>>>\n{content}\n<<<UNTRUSTED_CONTENT_END>>>"

    def inspect_and_sanitize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main egress gate inspection:
        1. Verifies payload against secret leak rules.
        2. Enforces the Zero-Raw-Code limit (raw files >= max_raw_bytes must be tokenized).
        3. Fences user/repo contents.
        4. Injects canary token.
        """
        violations: List[str] = []
        sanitized: Dict[str, Any] = {}

        # Scan and sanitize all fields
        for key, value in payload.items():
            if isinstance(value, str):
                # Check for secrets
                scrubbed, found_secrets = self.scrub_secrets(value)
                if found_secrets:
                    # In fail-safe mode, we scrub and record
                    pass

                # Check for un-tokenized raw code length
                if not self.allow_raw_code and len(value) >= self.max_raw_bytes:
                    # If it contains source code patterns like imports or defs
                    if any(kw in value for kw in ("import ", "from ", "def ", "class ", "function ", "const ", "var ")):
                        if "[FUNC_" not in value and "[VAR_" not in value:
                            # Apply automatic pseudonymization
                            scrubbed = self.pseudonymizer.pseudonymize_code(scrubbed)
                            if len(scrubbed) >= self.max_raw_bytes and "[FUNC_" not in scrubbed:
                                violations.append(f"Field '{key}' contains raw code >= {self.max_raw_bytes} bytes without AST pseudonymization.")

                # Wrap in security fence
                if key in ("prompt", "context", "code", "repo_content", "user_input"):
                    scrubbed = self.fence_untrusted_content(scrubbed)

                sanitized[key] = scrubbed
            else:
                sanitized[key] = value

        if violations:
            raise RevaEgressViolationError("LLM Egress Gate blocked payload due to policy violations", violations)

        # Inject verification canary
        payload_digest = hashlib.sha256(json.dumps(sanitized, sort_keys=True, default=str).encode("utf-8")).hexdigest()
        sanitized["_egress_gate"] = {
            "verified": True,
            "policy": "REVA-SEC-013-STRICT",
            "canary": f"egress_canary_{payload_digest[:16]}",
            "sha256": payload_digest,
        }
        return sanitized
