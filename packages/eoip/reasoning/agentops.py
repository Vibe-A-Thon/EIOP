"""AgentOps — §7 Reasoning & Orchestration: agent operations (observability).

Run tracing, cost/latency accounting, deployment descriptors, incident
records, and SLA tracking. This *extends* ``eoip.observability`` (Prometheus
registry, OTel helpers) rather than duplicating it: traces and costs are kept
in JSONL files under a caller-supplied root (matching the ``eoip.jobs``
convention) and may be exported to the shared metrics registry by the wiring
step. Everything is deterministic and works without a live collector —
*External gate* for OTLP export.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from eoip.contracts.source_event import utc_now_iso
from eoip.jobs import write_json


def _urn(kind: str, seed: str) -> str:
    return "urn:eoip:reasoning:agentops:" + kind + ":" + hashlib.sha256(seed.encode()).hexdigest()[:20]


# ---------------------------------------------------------------------------
# Run tracing (§7)
# ---------------------------------------------------------------------------

class Span(BaseModel):
    model_config = ConfigDict(extra="forbid")

    span_id: str
    name: str
    started_at: str
    ended_at: str | None = None
    status: str = "OK"  # OK | ERROR
    attributes: dict[str, str] = Field(default_factory=dict)


class RunTrace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trace_id: str
    run_id: str
    agent_id: str
    started_at: str
    ended_at: str | None = None
    spans: list[Span] = Field(default_factory=list)
    tokens_used: int = 0
    estimated_cost: float = 0.0


class RunTracer:
    """Append-only run/span tracer persisted as JSONL under ``root``."""

    def __init__(self, root: str | Path | None = None):
        self.root = Path(root) / "agentops" / "traces" if root else None
        if self.root:
            self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._seq = 0

    def _next_id(self, seed: str) -> str:
        self._seq += 1
        return _urn("span", f"{seed}:{self._seq}:{os.getpid()}")

    def start_run(self, run_id: str, agent_id: str) -> RunTrace:
        trace = RunTrace(trace_id=_urn("trace", f"{run_id}:{utc_now_iso()}"), run_id=run_id,
                         agent_id=agent_id, started_at=utc_now_iso())
        self._persist(trace)
        return trace

    def start_span(self, trace: RunTrace, name: str, **attributes: str) -> Span:
        with self._lock:
            span = Span(span_id=self._next_id(name), name=name, started_at=utc_now_iso(),
                        attributes={k: str(v) for k, v in attributes.items()})
            trace.spans.append(span)
            return span

    def end_span(self, trace: RunTrace, span: Span, *, status: str = "OK") -> None:
        with self._lock:
            span.ended_at = utc_now_iso()
            span.status = status
            self._persist(trace)

    def end_run(self, trace: RunTrace, *, tokens_used: int = 0, estimated_cost: float = 0.0) -> RunTrace:
        with self._lock:
            trace.ended_at = utc_now_iso()
            trace.tokens_used = tokens_used
            trace.estimated_cost = estimated_cost
            self._persist(trace)
            return trace

    def _persist(self, trace: RunTrace) -> None:
        if not self.root:
            return
        with self._lock:
            path = self.root / f"{trace.trace_id.split(':')[-1]}.jsonl"
            path.write_text("\n".join(trace.model_dump_json() for _ in (0,)) + "\n", encoding="utf-8")

    def read(self, trace_id: str) -> RunTrace | None:
        if not self.root:
            return None
        for path in self.root.glob("*.jsonl"):
            last_line = path.read_text(encoding="utf-8").strip().splitlines()[-1]
            trace = RunTrace.model_validate(json.loads(last_line))
            if trace.trace_id == trace_id:
                return trace
        return None


# ---------------------------------------------------------------------------
# Cost / latency accounting (§7)
# ---------------------------------------------------------------------------

COST_MANIFEST = {
    "capability": "llm-cost-quoting",
    "external_gate": True,
    "note": "Real per-token pricing comes from a provider pricing API at wiring "
            "time; CostLedger accepts explicit rates and never guesses live prices.",
}


class CostLedger:
    """Token/cost accounting per run and model. Rates are caller-supplied;
    without a rate the ledger counts tokens only."""

    def __init__(self) -> None:
        self._entries: list[dict] = []
        self._lock = threading.RLock()
        self.rates: dict[str, float] = {}  # model -> cost per 1k tokens

    def set_rate(self, model: str, cost_per_1k_tokens: float) -> None:
        if cost_per_1k_tokens < 0:
            raise ValueError("rate must be non-negative")
        self.rates[model] = cost_per_1k_tokens

    def record(self, run_id: str, model: str, prompt_tokens: int, completion_tokens: int,
               latency_seconds: float) -> dict:
        if prompt_tokens < 0 or completion_tokens < 0:
            raise ValueError("token counts must be non-negative")
        total = prompt_tokens + completion_tokens
        with self._lock:
            entry = {
                "entry_id": _urn("cost", f"{run_id}:{len(self._entries)}"),
                "run_id": run_id,
                "model": model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total,
                "cost": round(total / 1000.0 * self.rates.get(model, 0.0), 6),
                "latency_seconds": round(latency_seconds, 4),
                "recorded_at": utc_now_iso(),
            }
            self._entries.append(entry)
            return entry

    def totals(self, *, run_id: str | None = None) -> dict:
        with self._lock:
            entries = [e for e in self._entries if run_id is None or e["run_id"] == run_id]
        return {
            "runs": len({e["run_id"] for e in entries}),
            "total_tokens": sum(e["total_tokens"] for e in entries),
            "total_cost": round(sum(e["cost"] for e in entries), 6),
            "mean_latency_seconds": round(
                sum(e["latency_seconds"] for e in entries) / len(entries), 4) if entries else 0.0,
        }


# ---------------------------------------------------------------------------
# Deployment descriptors (§7)
# ---------------------------------------------------------------------------

class DeploymentDescriptor(BaseModel):
    """Declarative agent deployment descriptor (§7 AgentOps)."""

    model_config = ConfigDict(extra="forbid")

    deployment_id: str
    agent_id: str
    version: str
    environment: str = "staging"  # staging | canary | production
    canary_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    min_eval_pass_rate: float = Field(default=0.9, ge=0.0, le=1.0)
    max_cost_per_task: float = Field(default=0.0, ge=0.0)  # 0 = unbounded
    rollback_on_sla_breach: bool = True


def validate_deployment(descriptor: DeploymentDescriptor) -> list[str]:
    """Deterministic deployment-gate checks; returns violation messages."""
    violations: list[str] = []
    if descriptor.environment == "production" and descriptor.canary_percentage == 0.0:
        violations.append("production deployment must start as a canary (canary_percentage > 0)")
    if descriptor.canary_percentage > 0.0 and descriptor.canary_percentage < 1.0:
        violations.append("canary_percentage below 1% is not a meaningful canary")
    if not descriptor.version:
        violations.append("version is required")
    return violations


# ---------------------------------------------------------------------------
# Incident record model (§7)
# ---------------------------------------------------------------------------

class IncidentRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incident_id: str
    deployment_id: str
    severity: str = "SEV3"  # SEV1 | SEV2 | SEV3 | SEV4
    title: str
    description: str = ""
    status: str = "OPEN"  # OPEN | MITIGATED | RESOLVED
    opened_at: str = ""
    resolved_at: str | None = None
    trace_id: str | None = None

    @property
    def resolution_seconds(self) -> float | None:
        if not self.resolved_at or not self.opened_at:
            return None
        from datetime import datetime
        try:
            start = datetime.fromisoformat(self.opened_at)
            end = datetime.fromisoformat(self.resolved_at)
            return (end - start).total_seconds()
        except ValueError:
            return None


class IncidentStore:
    """Filesystem-backed incident records under ``root``."""

    SEVERITIES = ("SEV1", "SEV2", "SEV3", "SEV4")

    def __init__(self, root: str | Path | None = None):
        self.root = Path(root) / "agentops" / "incidents" if root else None
        if self.root:
            self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._seq = 0

    def open(self, deployment_id: str, severity: str, title: str, *,
             description: str = "", trace_id: str | None = None) -> IncidentRecord:
        if severity not in self.SEVERITIES:
            raise ValueError(f"severity must be one of {self.SEVERITIES}")
        with self._lock:
            self._seq += 1
            incident = IncidentRecord(
                incident_id=_urn("incident", str(self._seq)),
                deployment_id=deployment_id, severity=severity, title=title,
                description=description, opened_at=utc_now_iso(), trace_id=trace_id,
            )
            self._persist(incident)
            return incident

    def update_status(self, incident: IncidentRecord, status: str) -> IncidentRecord:
        if status not in {"OPEN", "MITIGATED", "RESOLVED"}:
            raise ValueError("status must be OPEN, MITIGATED, or RESOLVED")
        with self._lock:
            incident.status = status
            if status == "RESOLVED" and incident.resolved_at is None:
                incident.resolved_at = utc_now_iso()
            self._persist(incident)
            return incident

    def _persist(self, incident: IncidentRecord) -> None:
        if self.root:
            write_json(self.root / f"{incident.incident_id.split(':')[-1]}.json",
                       json.loads(incident.model_dump_json()))

    def list(self, *, status: str | None = None, deployment_id: str | None = None) -> list[IncidentRecord]:
        if not self.root:
            return []
        out = []
        for path in sorted(self.root.glob("*.json")):
            record = IncidentRecord.model_validate(json.loads(path.read_text(encoding="utf-8")))
            if status and record.status != status:
                continue
            if deployment_id and record.deployment_id != deployment_id:
                continue
            out.append(record)
        return out


# ---------------------------------------------------------------------------
# SLA tracking (§7)
# ---------------------------------------------------------------------------

class SLAPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_id: str
    agent_id: str
    slo_target: float = Field(ge=0.0, le=1.0)  # e.g. 0.99 success rate
    window_records: int = Field(default=100, ge=1)  # rolling window size
    error_budget: float = Field(default=0.01, gt=0.0, le=1.0)  # allowed failure fraction


class SLATracker:
    """Rolling-window SLA tracker with error-budget burn rate."""

    def __init__(self, policy: SLAPolicy):
        self.policy = policy
        self._outcomes: list[bool] = []  # True = success
        self._lock = threading.RLock()

    def record(self, success: bool) -> None:
        with self._lock:
            self._outcomes.append(bool(success))
            if len(self._outcomes) > self.policy.window_records:
                self._outcomes.pop(0)

    def status(self) -> dict:
        with self._lock:
            outcomes = list(self._outcomes)
        window = len(outcomes)
        successes = sum(outcomes)
        observed = successes / window if window else 0.0
        allowed_failures = self.policy.error_budget * max(window, 1)
        actual_failures = window - successes
        remaining_budget = max(0.0, 1.0 - (actual_failures / allowed_failures)) if allowed_failures else 0.0
        return {
            "policy_id": self.policy.policy_id,
            "window_records": window,
            "success_rate": round(observed, 4),
            "slo_target": self.policy.slo_target,
            "slo_met": window > 0 and observed >= self.policy.slo_target,
            "error_budget_remaining": round(remaining_budget, 4),
            "breach": window > 0 and observed < (1.0 - self.policy.error_budget),
        }
