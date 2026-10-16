"""Moonshot 9: Enterprise Governance & Autonomous Compliance Twin.

Provides:
- Machine-readable AI Bill of Materials (AI-BOM) tracking model lineage, prompts, and training data.
- Autonomous Compliance Twin continuously auditing controls against EU AI Act, SOC 2, ISO 42001, and HIPAA/GDPR.
- Cryptographically sealed auditor evidence export bundles.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AIBOMComponent:
    component_id: str
    name: str
    version: str
    component_type: str  # MODEL, PROMPT_TEMPLATE, EMBEDDING, DATASET
    sha256_hash: str
    license_type: str
    supplier: str


@dataclass
class AIBillOfMaterials:
    bom_id: str
    created_at: float
    platform_version: str
    components: list[AIBOMComponent]
    cryptographic_seal: str = ""

    def __post_init__(self) -> None:
        if not self.cryptographic_seal:
            serialized = json.dumps([asdict(c) for c in self.components], sort_keys=True)
            self.cryptographic_seal = hashlib.sha256(serialized.encode()).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ControlEvaluation:
    control_id: str
    framework: str
    title: str
    passed: bool
    evidence_summary: str
    remediation_hint: str = ""


class AutonomousComplianceTwin:
    """Continuous enterprise compliance monitor for AI regulation and cybersecurity standards."""

    def __init__(self, tenant_id: str = "default") -> None:
        self.tenant_id = tenant_id

    def generate_ai_bom(self, active_models: list[dict[str, Any]]) -> AIBillOfMaterials:
        components: list[AIBOMComponent] = []
        for m in active_models:
            comp_id = m.get("id", "model-default")
            name = m.get("name", "local-ollama")
            version = m.get("version", "1.0.0")
            h = hashlib.sha256(f"{comp_id}:{name}:{version}".encode()).hexdigest()
            components.append(
                AIBOMComponent(
                    component_id=comp_id,
                    name=name,
                    version=version,
                    component_type="MODEL",
                    sha256_hash=h,
                    license_type=m.get("license", "Apache-2.0"),
                    supplier=m.get("supplier", "local-organization"),
                )
            )

        return AIBillOfMaterials(
            bom_id=f"aibom_{self.tenant_id}_{int(time.time())}",
            created_at=time.time(),
            platform_version="2.0.0",
            components=components,
        )

    def _check_control(self, control_id: str, system_stats: dict[str, Any]) -> tuple[bool, str]:
        """Evaluate a single control by inspecting actual system state.

        Returns (passed, evidence_summary). A control fails when the required
        system_stats key is missing or explicitly False — never defaults to True.
        """
        checks: dict[str, tuple[str, str, str]] = {
            "EU-AI-ACT-ART-12": (
                "audit_logging_enabled",
                "Audit logging active on all agent and query pipelines.",
                "Audit logging is DISABLED or not configured.",
            ),
            "EU-AI-ACT-ART-14": (
                "hitl_approval_required",
                "Human approval boundary enforced on R3/R4 operations.",
                "HITL gating is DISABLED — high-risk actions can execute without approval.",
            ),
            "EU-AI-ACT-ART-15": (
                "no_egress_default",
                "Air-gapped local model processing by default.",
                "Egress controls are not enforced — data may leave the enclave.",
            ),
            "EU-AI-ACT-ART-13": (
                "model_transparency_docs",
                "Model documentation and AI-BOM registered for all deployed models.",
                "Missing model transparency documentation or AI-BOM.",
            ),
            "SOC2-CC6.1": (
                "tenant_isolation_active",
                "Strict tenant namespace and principal checking enabled.",
                "Tenant isolation is DISABLED or misconfigured.",
            ),
            "SOC2-CC7.1": (
                "drift_monitoring_active",
                "Continuous architecture drift scanning operational.",
                "Drift monitoring is INACTIVE — architecture violations may go undetected.",
            ),
            "SOC2-CC7.2": (
                "vulnerability_scan_age_days",
                "Vulnerability scan completed within the last 7 days.",
                "Last vulnerability scan is older than 7 days or has never run.",
            ),
            "SOC2-CC8.1": (
                "change_management_active",
                "Change management with approval workflow is operational.",
                "Change management workflow is DISABLED.",
            ),
            "ISO42001-5.2": (
                "ai_risk_assessment_complete",
                "AI risk assessment completed and documented.",
                "AI risk assessment not completed or documentation missing.",
            ),
            "HIPAA-164.312a": (
                "encryption_at_rest",
                "Data encrypted at rest with AES-256 or equivalent.",
                "Encryption at rest is NOT enabled.",
            ),
            "GDPR-ART-25": (
                "data_minimization_enforced",
                "Data minimization controls active on PII processing pipelines.",
                "Data minimization is NOT enforced on PII processing.",
            ),
            "GOV-GEN-01": (
                "provenance_active",
                "Evidence manifests attached to all knowledge responses.",
                "Provenance tracking is INACTIVE.",
            ),
            "GOV-GEN-02": (
                "rbac_enforced",
                "Role-based access control enforced on all API endpoints.",
                "RBAC is NOT enforced — open access on API endpoints.",
            ),
        }

        spec = checks.get(control_id)
        if not spec:
            return False, f"Unknown control {control_id}"

        stat_key, pass_evidence, fail_evidence = spec

        if stat_key == "vulnerability_scan_age_days":
            val = system_stats.get(stat_key)
            if val is None or not isinstance(val, (int, float)) or val > 7:
                return False, fail_evidence
            return True, pass_evidence

        val = system_stats.get(stat_key)
        if val is None:
            return False, f"{fail_evidence} (key '{stat_key}' not present in system stats)"
        if not bool(val):
            return False, fail_evidence
        return True, pass_evidence

    def evaluate_compliance(
        self,
        framework: str,
        system_stats: dict[str, Any],
    ) -> dict[str, Any]:
        """Evaluate continuous compliance posture against regulatory framework standards.

        Controls are checked against actual system_stats values. Missing keys cause
        controls to FAIL rather than defaulting to pass.
        """
        framework_upper = framework.upper()
        evaluations: list[ControlEvaluation] = []

        if "EU_AI" in framework_upper or "EU" in framework_upper:
            for cid, title in [
                ("EU-AI-ACT-ART-12", "Record-Keeping and Continuous Logging"),
                ("EU-AI-ACT-ART-13", "Model Transparency and AI-BOM"),
                ("EU-AI-ACT-ART-14", "Human-in-the-Loop Oversight for High-Risk Actions"),
                ("EU-AI-ACT-ART-15", "Robustness, Cybersecurity and Egress Control"),
            ]:
                passed, evidence = self._check_control(cid, system_stats)
                evaluations.append(ControlEvaluation(
                    control_id=cid, framework="EU AI Act", title=title,
                    passed=passed, evidence_summary=evidence,
                    remediation_hint="" if passed else f"Configure {cid} requirements.",
                ))

        elif "SOC2" in framework_upper:
            for cid, title in [
                ("SOC2-CC6.1", "Logical Access and Least Privilege"),
                ("SOC2-CC7.1", "System Vulnerability and Drift Monitoring"),
                ("SOC2-CC7.2", "Vulnerability Scanning Timeliness"),
                ("SOC2-CC8.1", "Change Management"),
            ]:
                passed, evidence = self._check_control(cid, system_stats)
                evaluations.append(ControlEvaluation(
                    control_id=cid, framework="SOC 2 Type II", title=title,
                    passed=passed, evidence_summary=evidence,
                    remediation_hint="" if passed else f"Address {cid} requirement.",
                ))

        elif "ISO" in framework_upper and "42001" in framework_upper:
            passed, evidence = self._check_control("ISO42001-5.2", system_stats)
            evaluations.append(ControlEvaluation(
                control_id="ISO42001-5.2", framework="ISO 42001",
                title="AI Risk Assessment",
                passed=passed, evidence_summary=evidence,
            ))

        elif "HIPAA" in framework_upper:
            passed, evidence = self._check_control("HIPAA-164.312a", system_stats)
            evaluations.append(ControlEvaluation(
                control_id="HIPAA-164.312a", framework="HIPAA",
                title="Encryption at Rest",
                passed=passed, evidence_summary=evidence,
            ))

        elif "GDPR" in framework_upper:
            passed, evidence = self._check_control("GDPR-ART-25", system_stats)
            evaluations.append(ControlEvaluation(
                control_id="GDPR-ART-25", framework="GDPR",
                title="Data Protection by Design and Default",
                passed=passed, evidence_summary=evidence,
            ))

        else:
            for cid, title in [
                ("GOV-GEN-01", "Data Integrity and Provenance Tracking"),
                ("GOV-GEN-02", "Role-Based Access Control"),
            ]:
                passed, evidence = self._check_control(cid, system_stats)
                evaluations.append(ControlEvaluation(
                    control_id=cid, framework=framework, title=title,
                    passed=passed, evidence_summary=evidence,
                ))

        passed_count = sum(1 for e in evaluations if e.passed)
        score_pct = round((passed_count / max(1, len(evaluations))) * 100, 1)

        serialized = json.dumps([asdict(e) for e in evaluations], sort_keys=True)
        evidence_seal = hashlib.sha256(serialized.encode()).hexdigest()

        return {
            "framework": framework,
            "tenant_id": self.tenant_id,
            "compliance_score_percent": score_pct,
            "controls_passed": passed_count,
            "controls_total": len(evaluations),
            "evaluations": [asdict(e) for e in evaluations],
            "evidence_package_seal": evidence_seal,
            "timestamp": time.time(),
        }
