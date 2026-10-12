"""Semantic Telemetry Adapter & Runtime Fact Manager (G2-TEL-002..008).

Implements bounded semantic telemetry storage:
- Telemetry-derived edges with explicit observation windows (G2-TEL-002)
- Source and evidence references on all derived edges (G2-TEL-003)
- Pattern fingerprinting for high-volume logs (G2-TEL-004)
- Bounded exemplar trace IDs preservation (G2-TEL-005)
- Configurable retention and TTL fact expiration (G2-TEL-006, G2-TEL-007)
- Explicit distinction between "not observed" vs "does not exist" with coverage status (G2-TEL-008).
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class TelemetryDerivedEdge:
    edge_key: str
    label: str
    out_cid: str
    in_cid: str
    window_start: float
    window_end: float
    source_ref: str
    evidence_key: str
    exemplar_trace_ids: list[str]
    call_count: int
    confidence: float
    coverage_status: str  # OBSERVED, NOT_OBSERVED_IN_WINDOW
    created_at: float = field(default_factory=time.time)

    def is_expired(self, current_time: float, ttl_seconds: float = 86400.0) -> bool:
        """G2-TEL-007: Runtime edge expires when observation window exceeds TTL."""
        return (current_time - self.window_end) > ttl_seconds

    def to_properties(self) -> dict[str, Any]:
        return {
            "edge_key": self.edge_key,
            "source_ref": self.source_ref,
            "evidence_key": self.evidence_key,
            "confidence": self.confidence,
            "creation_status": "DERIVED",
        }


class SemanticTelemetryAdapter:
    """Aggregates high-volume telemetry events into bounded semantic graph facts."""

    def __init__(self, store: GraphStore | None = None, retention_days: int = 30) -> None:
        self.store = store
        self.retention_days = retention_days
        self._derived_edges: dict[str, TelemetryDerivedEdge] = {}
        self._log_patterns: dict[str, int] = {}

    def compute_log_fingerprint(self, raw_message: str) -> str:
        """G2-TEL-004: Fingerprint repeated log message patterns by normalizing variable tokens."""
        import re
        normalized = re.sub(r"\b\d+\b", "<NUM>", raw_message)
        normalized = re.sub(r"[a-f0-9]{8,}", "<HEX>", normalized)
        fp = hashlib.sha256(normalized.encode()).hexdigest()[:16]
        self._log_patterns[fp] = self._log_patterns.get(fp, 0) + 1
        return fp

    def aggregate_service_interaction(
        self,
        caller_cid: str,
        callee_cid: str,
        window_start: float,
        window_end: float,
        trace_ids: list[str],
        source_ref: str = "otel:collector-west",
        confidence: float = 0.98,
    ) -> TelemetryDerivedEdge:
        """G2-TEL-002, 003, 005, 008: Aggregate raw telemetry into semantic edge."""
        edge_key = f"tel:{caller_cid}->{callee_cid}:{int(window_start)}"
        # Preserve bounded exemplars (max 5)
        bounded_traces = trace_ids[:5]

        edge = TelemetryDerivedEdge(
            edge_key=edge_key,
            label="DEPENDS_ON",
            out_cid=caller_cid,
            in_cid=callee_cid,
            window_start=window_start,
            window_end=window_end,
            source_ref=source_ref,
            evidence_key=f"urn:evidence:trace:{bounded_traces[0] if bounded_traces else 'none'}",
            exemplar_trace_ids=bounded_traces,
            call_count=len(trace_ids),
            confidence=confidence,
            coverage_status="OBSERVED" if trace_ids else "NOT_OBSERVED_IN_WINDOW",
        )
        self._derived_edges[edge_key] = edge
        return edge

    def purge_expired_runtime_edges(self, current_time: float, ttl_seconds: float = 86400.0) -> list[str]:
        """G2-TEL-006, G2-TEL-007: Expirations under configured retention and TTL."""
        expired = []
        for k, edge in list(self._derived_edges.items()):
            if edge.is_expired(current_time, ttl_seconds):
                expired.append(k)
                del self._derived_edges[k]
        return expired

    def get_edge_coverage(self, caller_cid: str, callee_cid: str) -> dict[str, Any]:
        """G2-TEL-008: Explicit coverage query distinguishing unobserved vs nonexistent."""
        for edge in self._derived_edges.values():
            if edge.out_cid == caller_cid and edge.in_cid == callee_cid:
                return {
                    "exists": True,
                    "coverage_status": edge.coverage_status,
                    "confidence": edge.confidence,
                    "exemplars": edge.exemplar_trace_ids,
                }
        return {
            "exists": False,
            "coverage_status": "NOT_OBSERVED_IN_WINDOW",
            "confidence": 0.0,
            "exemplars": [],
        }
