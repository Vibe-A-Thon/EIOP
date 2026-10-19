"""RFC 8785 JSON Canonicalization Scheme (JCS) implementation (T-101 / REVA-WK-001)."""

from __future__ import annotations

import hashlib
import math
from typing import Any, Set


class CanonicalizationError(ValueError):
    """Raised when an object cannot be canonicalized under RFC 8785 rules."""


def _format_float(v: float) -> str:
    if math.isnan(v) or math.isinf(v):
        raise CanonicalizationError(f"NaN and Infinity are not allowed in JSON: {v}")
    if v == 0.0:
        return "0"

    # Use Python's repr which produces the shortest round-trippable IEEE 754 decimal
    s = repr(v)
    if "e" in s:
        mantissa, exp = s.split("e")
        exp_int = int(exp)
        exp_sign = "+" if exp_int >= 0 else "-"
        return f"{mantissa}e{exp_sign}{abs(exp_int)}"
    return s


def _escape_str(s: str) -> str:
    # Check for lone surrogates
    try:
        s.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise CanonicalizationError(f"String contains lone surrogates: {exc}") from exc

    out = ['"']
    for ch in s:
        cp = ord(ch)
        if cp == 0x22:
            out.append(r'\"')
        elif cp == 0x5C:
            out.append(r"\\")
        elif cp == 0x08:
            out.append(r"\b")
        elif cp == 0x0C:
            out.append(r"\f")
        elif cp == 0x0A:
            out.append(r"\n")
        elif cp == 0x0D:
            out.append(r"\r")
        elif cp == 0x09:
            out.append(r"\t")
        elif cp < 0x20:
            out.append(f"\\u{cp:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _serialize(v: Any, allow_float: bool, seen: Set[int]) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        if abs(v) > 9007199254740991:  # 2**53 - 1
            raise CanonicalizationError(
                f"Integer {v} outside IEEE-754 safe range (-2^53+1 to 2^53-1); encode as string"
            )
        return str(v)
    if isinstance(v, float):
        if not allow_float:
            raise CanonicalizationError("Floats are forbidden in hash-bearing structures (allow_float=False)")
        return _format_float(v)
    if isinstance(v, str):
        return _escape_str(v)
    if isinstance(v, (list, tuple)):
        obj_id = id(v)
        if obj_id in seen:
            raise CanonicalizationError("Circular reference detected in array")
        seen.add(obj_id)
        try:
            items = [_serialize(x, allow_float, seen) for x in v]
            return "[" + ",".join(items) + "]"
        finally:
            seen.remove(obj_id)
    if isinstance(v, dict):
        obj_id = id(v)
        if obj_id in seen:
            raise CanonicalizationError("Circular reference detected in dict")
        seen.add(obj_id)
        try:
            # Sort keys by UTF-16 code units per RFC 8785
            # Python str.encode("utf-16-be") produces exact UTF-16 code unit ordering
            sorted_keys = sorted(v.keys(), key=lambda k: k.encode("utf-16-be") if isinstance(k, str) else b"")
            parts = []
            for k in sorted_keys:
                if not isinstance(k, str):
                    raise CanonicalizationError(f"Dict key must be str, got {type(k).__name__}")
                key_str = _escape_str(k)
                val_str = _serialize(v[k], allow_float, seen)
                parts.append(f"{key_str}:{val_str}")
            return "{" + ",".join(parts) + "}"
        finally:
            seen.remove(obj_id)

    if hasattr(v, "model_dump") and callable(v.model_dump):
        return _serialize(v.model_dump(by_alias=True, mode="json"), allow_float, seen)
    raise CanonicalizationError(f"Unsupported type for canonical JSON: {type(v).__name__}")


def canonicalize(value: Any, *, allow_float: bool = False) -> bytes:
    """Serialize value to RFC 8785 Canonical JSON bytes (UTF-8)."""
    res = _serialize(value, allow_float=allow_float, seen=set())
    return res.encode("utf-8")


def canonical_digest(value: Any, *, allow_float: bool = False) -> str:
    """Return SHA-256 lowercase hex digest of RFC 8785 canonicalized value."""
    return hashlib.sha256(canonicalize(value, allow_float=allow_float)).hexdigest()
