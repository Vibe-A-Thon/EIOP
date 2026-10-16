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


# ── Cognitive Boundary Telemetry (AGENT-001) ─────────────────────────

from enum import Enum


class BoundarySignal(str, Enum):
    CONFIDENCE_DROP = "confidence_drop"
    HALLUCINATION_PROBABILITY = "hallucination_probability"
    CONTEXT_OVERFLOW = "context_overflow"
    TOOL_FAILURE_STREAK = "tool_failure_streak"
    REASONING_LOOP_DETECTED = "reasoning_loop_detected"
    LATENCY_SPIKE = "latency_spike"
    COST_OVERRUN = "cost_overrun"


class HandoffTarget(str, Enum):
    HUMAN = "HUMAN_IN_THE_LOOP"
    HIGHER_AUTONOMY_LOOP = "HIGHER_AUTONOMY_LOOP"
    FALLBACK_AGENT = "FALLBACK_AGENT"
    NONE = "NONE"


@dataclass
class BoundaryEvaluation:
    signal: BoundarySignal
    value: float
    threshold: float
    breached: bool
    description: str


@dataclass
class HandoffDecision:
    triggered: bool
    target: HandoffTarget
    escalated_loop: str
    breached_signals: list[BoundaryEvaluation]
    recommended_action: str
    agent_id: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "triggered": self.triggered,
            "target": self.target.value,
            "escalated_loop": self.escalated_loop,
            "breached_signals": [
                {
                    "signal": s.signal.value,
                    "value": s.value,
                    "threshold": s.threshold,
                    "description": s.description,
                }
                for s in self.breached_signals
            ],
            "recommended_action": self.recommended_action,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
        }


class CognitiveBoundaryDetector:
    """Monitors agent runtime metrics for cognitive boundary breaches (AGENT-001)."""

    def __init__(
        self,
        min_confidence: float = 0.65,
        max_hallucination: float = 0.35,
        max_context_tokens: int = 8192,
        max_tool_failures: int = 3,
        max_repeated_thoughts: int = 2,
        max_latency_ms: float = 15000.0,
        max_cost_usd: float = 2.50,
    ) -> None:
        self.min_confidence = min_confidence
        self.max_hallucination = max_hallucination
        self.max_context_tokens = max_context_tokens
        self.max_tool_failures = max_tool_failures
        self.max_repeated_thoughts = max_repeated_thoughts
        self.max_latency_ms = max_latency_ms
        self.max_cost_usd = max_cost_usd
        self._telemetry_events: list[dict[str, Any]] = []

    def evaluate_metrics(self, agent_id: str, metrics: dict[str, Any]) -> HandoffDecision:
        """Evaluate 7 cognitive boundary signals against metrics and decide handoff."""
        breached: list[BoundaryEvaluation] = []

        # 1. confidence_drop
        conf = float(metrics.get("confidence", 1.0))
        if conf < self.min_confidence:
            breached.append(BoundaryEvaluation(
                signal=BoundarySignal.CONFIDENCE_DROP,
                value=conf,
                threshold=self.min_confidence,
                breached=True,
                description=f"Confidence dropped to {conf:.2f} (< {self.min_confidence:.2f})",
            ))

        # 2. hallucination_probability
        hallucination = float(metrics.get("hallucination_score", 0.0))
        if hallucination > self.max_hallucination:
            breached.append(BoundaryEvaluation(
                signal=BoundarySignal.HALLUCINATION_PROBABILITY,
                value=hallucination,
                threshold=self.max_hallucination,
                breached=True,
                description=f"Hallucination probability {hallucination:.2f} exceeded safety limit {self.max_hallucination:.2f}",
            ))

        # 3. context_overflow
        tokens = int(metrics.get("context_tokens", 0))
        if tokens > self.max_context_tokens:
            breached.append(BoundaryEvaluation(
                signal=BoundarySignal.CONTEXT_OVERFLOW,
                value=float(tokens),
                threshold=float(self.max_context_tokens),
                breached=True,
                description=f"Context tokens {tokens} exceeded max capacity {self.max_context_tokens}",
            ))

        # 4. tool_failure_streak
        tool_fails = int(metrics.get("consecutive_tool_failures", 0))
        if tool_fails >= self.max_tool_failures:
            breached.append(BoundaryEvaluation(
                signal=BoundarySignal.TOOL_FAILURE_STREAK,
                value=float(tool_fails),
                threshold=float(self.max_tool_failures),
                breached=True,
                description=f"Tool failure streak reached {tool_fails} (threshold: {self.max_tool_failures})",
            ))

        # 5. reasoning_loop_detected
        loop_repeats = int(metrics.get("repeated_reasoning_steps", 0))
        if loop_repeats >= self.max_repeated_thoughts:
            breached.append(BoundaryEvaluation(
                signal=BoundarySignal.REASONING_LOOP_DETECTED,
                value=float(loop_repeats),
                threshold=float(self.max_repeated_thoughts),
                breached=True,
                description=f"Reasoning loop detected: {loop_repeats} repeated thoughts",
            ))

        # 6. latency_spike
        lat = float(metrics.get("latency_ms", 0.0))
        if lat > self.max_latency_ms:
            breached.append(BoundaryEvaluation(
                signal=BoundarySignal.LATENCY_SPIKE,
                value=lat,
                threshold=self.max_latency_ms,
                breached=True,
                description=f"Latency {lat:.1f}ms spiked above limit {self.max_latency_ms:.1f}ms",
            ))

        # 7. cost_overrun
        cost = float(metrics.get("accumulated_cost_usd", 0.0))
        if cost > self.max_cost_usd:
            breached.append(BoundaryEvaluation(
                signal=BoundarySignal.COST_OVERRUN,
                value=cost,
                threshold=self.max_cost_usd,
                breached=True,
                description=f"Cost ${cost:.2f} exceeded budget limit ${self.max_cost_usd:.2f}",
            ))

        if not breached:
            return HandoffDecision(
                triggered=False,
                target=HandoffTarget.NONE,
                escalated_loop="CURRENT_LOOP",
                breached_signals=[],
                recommended_action="Continue autonomous execution in current loop",
                agent_id=agent_id,
            )

        # Decide escalation target based on severity
        critical_signals = {
            BoundarySignal.HALLUCINATION_PROBABILITY,
            BoundarySignal.TOOL_FAILURE_STREAK,
            BoundarySignal.REASONING_LOOP_DETECTED,
        }
        has_critical = any(b.signal in critical_signals for b in breached)

        if has_critical:
            target = HandoffTarget.HUMAN
            escalated_loop = "HITL"  # Escalate to human-in-the-loop
            action = f"Immediate human intervention requested: {breached[0].description}"
        elif any(b.signal == BoundarySignal.CONTEXT_OVERFLOW for b in breached):
            target = HandoffTarget.FALLBACK_AGENT
            escalated_loop = "HBTL"  # Human beside the loop or fallback summarizer agent
            action = "Dispatch fallback summarizer agent to compress context window"
        else:
            target = HandoffTarget.HIGHER_AUTONOMY_LOOP
            escalated_loop = "HOTL"  # Escalate to supervisory Human-on-the-loop
            action = f"Escalated to supervisory HOTL loop: {breached[0].description}"

        decision = HandoffDecision(
            triggered=True,
            target=target,
            escalated_loop=escalated_loop,
            breached_signals=breached,
            recommended_action=action,
            agent_id=agent_id,
        )

        self.emit_telemetry_event(decision)
        return decision

    def emit_telemetry_event(self, decision: HandoffDecision) -> dict[str, Any]:
        """Emit cognitive boundary breach event into telemetry history."""
        event = {
            "event_type": "COGNITIVE_BOUNDARY_BREACH",
            "agent_id": decision.agent_id,
            "target": decision.target.value,
            "escalated_loop": decision.escalated_loop,
            "signals_count": len(decision.breached_signals),
            "reasons": [s.description for s in decision.breached_signals],
            "timestamp": decision.timestamp,
        }
        self._telemetry_events.append(event)
        return event

    def get_events(self, limit: int = 50) -> list[dict[str, Any]]:
        return self._telemetry_events[-limit:]

