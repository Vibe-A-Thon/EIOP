"""Secret redaction for audit records (NFR-OPS-001).

Secrets are redacted before persistence. This covers tokens, passwords,
and internal reasoning that should not appear in audit logs.
"""

from __future__ import annotations

import re

_SECRET_KEYS = frozenset({
    "password", "token", "secret", "api_key", "apikey",
    "authorization", "auth_token", "access_token", "refresh_token",
    "private_key", "credential", "credentials",
})

_SECRET_PATTERN = re.compile(
    r"(bearer\s+|token[=:]\s*|password[=:]\s*|secret[=:]\s*)\S+",
    re.IGNORECASE,
)


def redact_secrets(record: dict) -> dict:
    result = {}
    for key, value in record.items():
        k_lower = key.lower()
        if k_lower in _SECRET_KEYS or any(s in k_lower for s in ("token", "secret", "password", "credential")):
            result[key] = "***REDACTED***"
        elif isinstance(value, str):
            result[key] = _SECRET_PATTERN.sub(r"\1***REDACTED***", value)
        elif isinstance(value, dict):
            result[key] = redact_secrets(value)
        elif isinstance(value, list):
            result[key] = [
                redact_secrets(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
    return result
