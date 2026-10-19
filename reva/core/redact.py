"""Redaction utilities for HTTP headers, query parameters and sensitive tokens (REVA-AS-003 / REVA-SEC-005)."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Union
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "proxy-authorization",
    "x-auth-token",
    "api-key",
}

SENSITIVE_KEY_PATTERN = re.compile(
    r"(?i)(password|secret|token|api_?key|access_?token|refresh_?token|private_?key|auth|credential)"
)


def redact_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """Redact sensitive HTTP header values."""
    out = {}
    for k, v in headers.items():
        if k.lower() in SENSITIVE_HEADERS or SENSITIVE_KEY_PATTERN.search(k):
            out[k] = "[REDACTED]"
        else:
            out[k] = v
    return out


def redact_url(url_str: str) -> str:
    """Redact credentials and sensitive query parameters from a URL."""
    try:
        parts = urlsplit(url_str)
        # Strip user:pass from netloc
        netloc = parts.netloc
        if "@" in netloc:
            _, host = netloc.rsplit("@", 1)
            netloc = f"[REDACTED]@{host}"

        # Redact query params
        query_pairs = parse_qsl(parts.query, keep_blank_values=True)
        redacted_pairs = []
        for qk, qv in query_pairs:
            if SENSITIVE_KEY_PATTERN.search(qk):
                redacted_pairs.append((qk, "[REDACTED]"))
            else:
                redacted_pairs.append((qk, qv))

        new_query = urlencode(redacted_pairs)
        return urlunsplit((parts.scheme, netloc, parts.path, new_query, parts.fragment))
    except Exception:
        return url_str


def redact_data(obj: Any) -> Any:
    """Recursively redact sensitive keys in nested dictionaries and lists."""
    if isinstance(obj, dict):
        res = {}
        for k, v in obj.items():
            if isinstance(k, str) and SENSITIVE_KEY_PATTERN.search(k):
                res[k] = "[REDACTED]"
            else:
                res[k] = redact_data(v)
        return res
    if isinstance(obj, list):
        return [redact_data(x) for x in obj]
    return obj
