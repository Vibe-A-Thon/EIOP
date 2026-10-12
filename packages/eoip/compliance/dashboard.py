"""Continuous Compliance Monitoring Dashboard Engine (COMPLY-003).

Provides real-time compliance posture tracking:
- Per-framework compliance scores (GDPR, SOX, HIPAA, SOC2, NIST AI RMF, EU AI Act)
- Automated evidence collection with graph references & provenance
- Attestation workflows with digital reviewer signatures
- Audit-ready report export (JSON/CSV) for regulatory examiners
"""

from __future__ import annotations

import csv
import io
import json
import logging
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.compliance.constraints import (
    ComplianceFramework,
    ComplianceSeverity,
    ContinuousMonitor,
    ViolationReport,
)
from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.compliance.dashboard")


class ReadinessTier(str, Enum):
    AUDIT_READY = "AUDIT_READY"
    SUBSTANTIAL_COMPLIANCE = "SUBSTANTIAL_COMPLIANCE"
    NEEDS_ATTENTION = "NEEDS_ATTENTION"
    CRITICAL_GAP = "CRITICAL_GAP"


class AttestationStatus(str, Enum):
    PENDING = "PENDING"
    ATTESTED = "ATTESTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


@dataclass
class FrameworkScore:
    framework: str
    total_controls: int
    passed_controls: int
    failed_controls: int
    score_percentage: float
    readiness_tier: ReadinessTier
    last_evaluated_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "framework": self.framework,
            "total_controls": self.total_controls,
            "passed_controls": self.passed_controls,
            "failed_controls": self.failed_controls,
            "score_percentage": round(self.score_percentage, 2),
            "readiness_tier": self.readiness_tier.value,
            "last_evaluated_at": self.last_evaluated_at,
        }


@dataclass
class EvidenceArtifact:
    evidence_id: str
    control_id: str
    framework: str
    graph_entity_id: str
    entity_label: str
    provenance_hash: str
    collected_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AttestationRecord:
    attestation_id: str
    framework: str
    scope_period: str
    attester_id: str
    reviewer_signature: str
    status: AttestationStatus
    evidence_ids: list[str] = field(default_factory=list)
    comments: str = ""
    created_at: float = field(default_factory=time.time)
    expires_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


class EvidenceCollector:
    """Automates evidence gathering from graph entities with tamper-evident cryptographic hash-chaining."""

    def __init__(self) -> None:
        self._artifacts: dict[str, EvidenceArtifact] = {}
        self._previous_hash = "0" * 64
        self._lock = threading.Lock()

    def collect_from_graph(
        self,
        store: MemoryGraphStore,
        control_id: str,
        framework: str,
    ) -> list[EvidenceArtifact]:
        collected = []
        import hashlib

        with self._lock:
            for v in store.find_vertices():
                props = v.get("properties", {})
                cid = props.get("canonical_id", v.get("canonical_id", "unknown"))
                lbl = v.get("label", "Unknown")
                raw_data = f"{cid}:{lbl}:{props.get('modified_at', '')}:{self._previous_hash}"
                prov_hash = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()
                self._previous_hash = prov_hash

                ev_id = f"EV-{control_id}-{cid}"
                artifact = EvidenceArtifact(
                    evidence_id=ev_id,
                    control_id=control_id,
                    framework=framework,
                    graph_entity_id=cid,
                    entity_label=lbl,
                    provenance_hash=prov_hash,
                    metadata={"properties_count": len(props), "previous_hash": self._previous_hash},
                )
                self._artifacts[ev_id] = artifact
                collected.append(artifact)
        return collected

    def get_artifact(self, evidence_id: str) -> EvidenceArtifact | None:
        with self._lock:
            return self._artifacts.get(evidence_id)

    def list_artifacts(self, framework: str | None = None) -> list[EvidenceArtifact]:
        with self._lock:
            if not framework:
                return list(self._artifacts.values())
            return [a for a in self._artifacts.values() if a.framework == framework]


class AttestationWorkflow:
    """Manages compliance sign-offs and auditor attestations."""

    def __init__(self) -> None:
        self._records: dict[str, AttestationRecord] = {}
        self._lock = threading.Lock()

    def submit_attestation(
        self,
        framework: str,
        scope_period: str,
        attester_id: str,
        evidence_ids: list[str],
        validity_days: int = 90,
    ) -> AttestationRecord:
        import uuid
        now = time.time()
        aid = f"ATT-{uuid.uuid4().hex[:8].upper()}"
        record = AttestationRecord(
            attestation_id=aid,
            framework=framework,
            scope_period=scope_period,
            attester_id=attester_id,
            reviewer_signature="",
            status=AttestationStatus.PENDING,
            evidence_ids=evidence_ids,
            created_at=now,
            expires_at=now + (validity_days * 86400),
        )
        with self._lock:
            self._records[aid] = record
        return record

    def sign_attestation(
        self,
        attestation_id: str,
        reviewer_signature: str,
        comments: str = "",
    ) -> AttestationRecord:
        with self._lock:
            rec = self._records.get(attestation_id)
            if not rec:
                raise KeyError(f"Attestation not found: {attestation_id}")
            rec.reviewer_signature = reviewer_signature
            rec.comments = comments
            rec.status = AttestationStatus.ATTESTED
            return rec

    def reject_attestation(self, attestation_id: str, reason: str) -> AttestationRecord:
        with self._lock:
            rec = self._records.get(attestation_id)
            if not rec:
                raise KeyError(f"Attestation not found: {attestation_id}")
            rec.comments = reason
            rec.status = AttestationStatus.REJECTED
            return rec

    def get_record(self, attestation_id: str) -> AttestationRecord | None:
        with self._lock:
            return self._records.get(attestation_id)


class ContinuousComplianceDashboard:
    """Real-time enterprise compliance posture coordinator."""

    def __init__(self, continuous_monitor: ContinuousMonitor | None = None) -> None:
        self.monitor = continuous_monitor or ContinuousMonitor()
        self.evidence_collector = EvidenceCollector()
        self.attestation_workflow = AttestationWorkflow()
        self._lock = threading.Lock()

    def compute_framework_scores(self, store: MemoryGraphStore) -> dict[str, FrameworkScore]:
        report = self.monitor.evaluate_compliance(store)
        violations_by_fw: dict[str, int] = {}
        for v in report.violations:
            fw = v.framework.value if hasattr(v.framework, "value") else str(v.framework)
            violations_by_fw[fw] = violations_by_fw.get(fw, 0) + 1

        all_frameworks = ["GDPR", "SOX", "HIPAA", "SOC2", "ISO_27001", "ISO_42001", "NIST_AI_RMF", "EU_AI_ACT"]
        # Baseline controls count per standard
        framework_controls_count = {
            "GDPR": 10,
            "SOX": 8,
            "HIPAA": 12,
            "SOC2": 15,
            "ISO_27001": 14,
            "ISO_42001": 10,
            "NIST_AI_RMF": 10,
            "EU_AI_ACT": 10,
        }

        scores: dict[str, FrameworkScore] = {}
        for fw in all_frameworks:
            total = framework_controls_count.get(fw, 10)
            failed = violations_by_fw.get(fw, 0)
            passed = max(0, total - failed)
            pct = max(0.0, (passed / total) * 100.0)

            if pct >= 95.0 and failed == 0:
                tier = ReadinessTier.AUDIT_READY
            elif pct >= 80.0:
                tier = ReadinessTier.SUBSTANTIAL_COMPLIANCE
            elif pct >= 50.0:
                tier = ReadinessTier.NEEDS_ATTENTION
            else:
                tier = ReadinessTier.CRITICAL_GAP

            scores[fw] = FrameworkScore(
                framework=fw,
                total_controls=total,
                passed_controls=passed,
                failed_controls=failed,
                score_percentage=pct,
                readiness_tier=tier,
            )
        return scores

    def export_audit_package_json(self, store: MemoryGraphStore) -> str:
        scores = self.compute_framework_scores(store)
        evidence = self.evidence_collector.list_artifacts()
        payload = {
            "generated_at": time.time(),
            "framework_scores": {k: v.to_dict() for k, v in scores.items()},
            "evidence_count": len(evidence),
            "evidence_artifacts": [e.to_dict() for e in evidence],
        }
        return json.dumps(payload, indent=2)

    def export_audit_package_csv(self, store: MemoryGraphStore) -> str:
        scores = self.compute_framework_scores(store)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Framework", "Total Controls", "Passed Controls", "Failed Controls", "Score (%)", "Readiness Tier"])
        for s in scores.values():
            writer.writerow([
                s.framework,
                s.total_controls,
                s.passed_controls,
                s.failed_controls,
                f"{s.score_percentage:.1f}%",
                s.readiness_tier.value,
            ])
        return output.getvalue()


_dashboard_singleton: ContinuousComplianceDashboard | None = None
_dashboard_lock = threading.Lock()


def get_compliance_dashboard() -> ContinuousComplianceDashboard:
    """Thread-safe singleton accessor for ContinuousComplianceDashboard."""
    global _dashboard_singleton
    if _dashboard_singleton is None:
        with _dashboard_lock:
            if _dashboard_singleton is None:
                _dashboard_singleton = ContinuousComplianceDashboard()
    return _dashboard_singleton
