"""Data Preparation and Stream Transformation Backend for DPU (PUR-DPU-001..005).

Provides:
1. Streaming batch preparation with backpressure.
2. SHA-256 checksum verification.
3. Gzip compression and decompression with bomb protection.
4. Recursive classification and secret redaction.
5. Deduplication and SourceEvent v2 envelope generation.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
from typing import Any, Dict, List, Optional, Tuple
from collections.abc import Generator, Iterable


def calculate_checksum(data: bytes) -> str:
    """Calculate SHA-256 hex digest of byte payload (PUR-DPU-002)."""
    return hashlib.sha256(data).hexdigest()


def compress_payload(data: bytes, level: int = 6) -> bytes:
    """Compress payload using standard gzip."""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=level) as gz:
        gz.write(data)
    return buf.getvalue()


def decompress_payload(
    compressed_data: bytes,
    max_decompressed_bytes: int = 64 * 1024 * 1024,
    max_ratio: float = 100.0,
) -> bytes:
    """Decompress gzip payload with zip-bomb protection (PUR-DPU-002)."""
    compressed_len = len(compressed_data)
    buf = io.BytesIO(compressed_data)
    out = io.BytesIO()

    total_read = 0
    with gzip.GzipFile(fileobj=buf, mode="rb") as gz:
        while True:
            chunk = gz.read(64 * 1024)
            if not chunk:
                break
            total_read += len(chunk)
            if total_read > max_decompressed_bytes:
                raise ValueError(
                    f"Decompression bomb rejected: exceeded max size of {max_decompressed_bytes} bytes"
                )
            if compressed_len > 0 and (total_read / compressed_len) > max_ratio:
                raise ValueError(
                    f"Decompression bomb rejected: expansion ratio {total_read / compressed_len:.1f}x exceeds limit {max_ratio}x"
                )
            out.write(chunk)

    return out.getvalue()


def prepare_batches(
    records: Iterable[Dict[str, Any]],
    batch_size: int = 100,
    max_batch_bytes: int = 1024 * 1024,
) -> Generator[Dict[str, Any], None, None]:
    """Batch records with count and byte size limits (PUR-DPU-001)."""
    current_batch: List[Dict[str, Any]] = []
    current_bytes = 0
    batch_index = 0

    for rec in records:
        rec_bytes = len(json.dumps(rec, ensure_ascii=False).encode("utf-8"))
        if current_batch and (len(current_batch) >= batch_size or (current_bytes + rec_bytes) > max_batch_bytes):
            yield {
                "batch_index": batch_index,
                "record_count": len(current_batch),
                "byte_length": current_bytes,
                "records": current_batch,
            }
            batch_index += 1
            current_batch = []
            current_bytes = 0

        current_batch.append(rec)
        current_bytes += rec_bytes

    if current_batch:
        yield {
            "batch_index": batch_index,
            "record_count": len(current_batch),
            "byte_length": current_bytes,
            "records": current_batch,
        }


def redact_sensitive_data(
    data: Any,
    secret_patterns: Optional[List[re.Pattern]] = None,
) -> Tuple[Any, int]:
    """Recursively redact secrets and PII from nested structures (PUR-DPU-003)."""
    if secret_patterns is None:
        secret_patterns = [
            re.compile(r"(?i)(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*['\"]?([^'\"\s]+)"),
            re.compile(r"sk-[a-zA-Z0-9]{32,}"),
            re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN
            re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b"),  # Credit card
        ]

    redactions_count = 0

    def _walk(item: Any) -> Any:
        nonlocal redactions_count
        if isinstance(item, str):
            res = item
            for pat in secret_patterns:
                matches = list(pat.finditer(res))
                if matches:
                    redactions_count += len(matches)
                    res = pat.sub("[REDACTED]", res)
            return res
        elif isinstance(item, dict):
            new_dict = {}
            for k, v in item.items():
                if any(sec_term in str(k).lower() for sec_term in ("secret", "password", "token", "apikey")):
                    redactions_count += 1
                    new_dict[k] = "[REDACTED]"
                else:
                    new_dict[k] = _walk(v)
            return new_dict
        elif isinstance(item, list):
            return [_walk(v) for v in item]
        return item

    cleaned = _walk(data)
    return cleaned, redactions_count


def deduplicate_records(
    records: List[Dict[str, Any]],
    key_fields: List[str],
) -> Dict[str, Any]:
    """Deduplicate records based on composite key fields (PUR-DPU-004)."""
    seen_keys = set()
    survivors = []
    duplicate_count = 0

    for rec in records:
        key_vals = tuple(rec.get(k) for k in key_fields)
        if key_vals in seen_keys:
            duplicate_count += 1
        else:
            seen_keys.add(key_vals)
            survivors.append(rec)

    return {
        "original_count": len(records),
        "unique_count": len(survivors),
        "duplicate_count": duplicate_count,
        "duplicates_removed": duplicate_count,
        "survivors": survivors,
        "records": survivors,
    }



def create_ingestion_envelope(
    source_name: str,
    records: List[Dict[str, Any]],
    tenant_id: str = "default",
) -> Dict[str, Any]:
    """Wrap records in SourceEvent v2 ingestion envelope (PUR-DPU-005)."""
    raw_bytes = json.dumps(records).encode("utf-8")
    digest = calculate_checksum(raw_bytes)

    return {
        "event_version": "v2",
        "source": source_name,
        "tenant_id": tenant_id,
        "content_sha256": digest,
        "record_count": len(records),
        "payload": records,
    }
