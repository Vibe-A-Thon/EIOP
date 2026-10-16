"""Extended Compliance Packs — CCPA, PCI DSS, NIST CSF, ISO 42001.

Adds four additional compliance frameworks to the existing pack system.
Uses the same CompliancePack/Control data model from compliance.pack.
"""

from __future__ import annotations

from eoip.compliance.pack import (
    CompliancePack,
    Control,
    EvidenceQuerySpec,
)

CAP_AUDIT = "audit-sink"
CAP_AUTHZ = "authz-decisions"
CAP_EGRESS = "egress-manifests"
CAP_PROV = "provenance-evidence"
CAP_VALIDATION = "validation-gates"
CAP_BACKUP = "backup-restore"
CAP_AI_GOV = "ai-governance"
CAP_ROLES = "roles-registry"
CAP_TENANCY = "tenancy-isolation"
CAP_KILL = "kill-switch"

_EVIDENCE = {
    "audit_write": EvidenceQuerySpec(
        kind="audit_event", params={"event_type": "audit.event"},
        description="Audit events persisted to the audit sink",
    ),
    "audit_authz_deny": EvidenceQuerySpec(
        kind="authz_decisions", params={"action": "authz.deny"},
        description="Denied authorization decisions auditable",
    ),
    "roles": EvidenceQuerySpec(
        kind="authz_roles", params={"roles": ["admin", "steward"]},
        description="Separation-of-duties roles registered",
    ),
    "graph_entity": EvidenceQuerySpec(
        kind="graph_vertices", params={"label": "Entity"},
        description="Canonical entities present in graph",
    ),
    "evidence_vertices": EvidenceQuerySpec(
        kind="evidence_vertices", params={"label": "Evidence"},
        description="Provenance evidence vertices linked to facts",
    ),
    "validation_findings": EvidenceQuerySpec(
        kind="validation_findings",
        description="Validation gate findings tracked",
    ),
    "backup_manifest": EvidenceQuerySpec(
        kind="backup_manifest", params={"filenames": ["manifest.json"]},
        description="Backup/ops bundle manifest produced",
    ),
    "model_cards": EvidenceQuerySpec(
        kind="ai_governance", params={"record": "model_cards"},
        description="AI model cards registered",
    ),
    "evaluations": EvidenceQuerySpec(
        kind="ai_governance", params={"record": "evaluations"},
        description="AI model evaluation records present",
    ),
}


def _c(framework: str, suffix: str, title: str,
       capabilities: list[str], evidence: list[EvidenceQuerySpec],
       description: str = "") -> Control:
    return Control(
        control_id=f"{framework}-{suffix}",
        framework=framework,
        title=title,
        description=description,
        platform_capabilities=capabilities,
        evidence=evidence,
        report_template="compliance-evidence",
    )


_CCPA_CONTROLS = [
    _c("CCPA", "1798.100", "Right to Know",
       [CAP_PROV], [_EVIDENCE["graph_entity"], _EVIDENCE["evidence_vertices"]],
       "Consumers can request categories and specific pieces of personal information collected."),
    _c("CCPA", "1798.105", "Right to Delete",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Consumers can request deletion of personal information."),
    _c("CCPA", "1798.110", "Data Categories Disclosure",
       [CAP_PROV], [_EVIDENCE["graph_entity"]],
       "Disclose categories of personal information collected and purposes."),
    _c("CCPA", "1798.115", "Right to Know — Sold/Disclosed",
       [CAP_EGRESS, CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Disclose categories sold or disclosed for business purposes."),
    _c("CCPA", "1798.120", "Right to Opt-Out of Sale",
       [CAP_AUDIT, CAP_AUTHZ], [_EVIDENCE["audit_write"], _EVIDENCE["audit_authz_deny"]],
       "Consumers can opt out of sale of personal information."),
    _c("CCPA", "1798.121", "Right to Limit Sensitive Info",
       [CAP_AUTHZ], [_EVIDENCE["roles"]],
       "Limit use and disclosure of sensitive personal information."),
    _c("CCPA", "1798.125", "Non-Discrimination",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Cannot discriminate against consumers exercising CCPA rights."),
    _c("CCPA", "1798.130", "Notice at Collection",
       [CAP_PROV], [_EVIDENCE["evidence_vertices"]],
       "Provide notice at or before the point of collection."),
    _c("CCPA", "1798.135", "Opt-Out Link",
       [CAP_AUTHZ], [_EVIDENCE["audit_authz_deny"]],
       "Clear and conspicuous opt-out link required."),
    _c("CCPA", "1798.140", "Definition Compliance",
       [CAP_VALIDATION], [_EVIDENCE["validation_findings"]],
       "Classification of personal information per CCPA definitions."),
]

_PCI_DSS_CONTROLS = [
    _c("PCI-DSS", "1.1", "Network Security Controls",
       [CAP_TENANCY], [_EVIDENCE["audit_write"]],
       "Install and maintain network security controls."),
    _c("PCI-DSS", "2.1", "Secure System Configuration",
       [CAP_VALIDATION], [_EVIDENCE["validation_findings"]],
       "Apply secure configurations to all system components."),
    _c("PCI-DSS", "3.1", "Stored Data Protection",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Protect stored account data with encryption."),
    _c("PCI-DSS", "4.1", "Transmission Encryption",
       [CAP_EGRESS], [_EVIDENCE["audit_write"]],
       "Strong cryptography for cardholder data over open networks."),
    _c("PCI-DSS", "5.1", "Malware Protection",
       [CAP_VALIDATION], [_EVIDENCE["validation_findings"]],
       "Protect all systems against malware."),
    _c("PCI-DSS", "6.1", "Secure Development",
       [CAP_VALIDATION], [_EVIDENCE["validation_findings"]],
       "Develop and maintain secure systems and software."),
    _c("PCI-DSS", "7.1", "Restrict Access by Business Need",
       [CAP_AUTHZ, CAP_ROLES], [_EVIDENCE["roles"], _EVIDENCE["audit_authz_deny"]],
       "Restrict access to system components by business need to know."),
    _c("PCI-DSS", "8.1", "Identify and Authenticate",
       [CAP_AUTHZ], [_EVIDENCE["audit_authz_deny"]],
       "Identify users and authenticate access to system components."),
    _c("PCI-DSS", "10.1", "Logging and Monitoring",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Log and monitor all access to system components."),
    _c("PCI-DSS", "12.1", "Security Policy",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Maintain information security policy for all personnel."),
]

_NIST_CSF_CONTROLS = [
    _c("NIST-CSF", "ID.AM", "Asset Management",
       [CAP_PROV], [_EVIDENCE["graph_entity"]],
       "Identify and manage data, personnel, devices, and systems."),
    _c("NIST-CSF", "ID.BE", "Business Environment",
       [CAP_PROV], [_EVIDENCE["graph_entity"]],
       "Understand mission, objectives, stakeholders and activities."),
    _c("NIST-CSF", "ID.GV", "Governance",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Policies, procedures, and processes to manage cybersecurity risk."),
    _c("NIST-CSF", "ID.RA", "Risk Assessment",
       [CAP_VALIDATION], [_EVIDENCE["validation_findings"]],
       "Understand cybersecurity risk to operations and assets."),
    _c("NIST-CSF", "PR.AC", "Access Control",
       [CAP_AUTHZ, CAP_ROLES], [_EVIDENCE["roles"], _EVIDENCE["audit_authz_deny"]],
       "Manage access to assets and associated facilities."),
    _c("NIST-CSF", "PR.DS", "Data Security",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Manage data consistent with risk strategy."),
    _c("NIST-CSF", "PR.AT", "Awareness and Training",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Educate personnel about cybersecurity."),
    _c("NIST-CSF", "DE.CM", "Continuous Monitoring",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Monitor information systems for cybersecurity events."),
    _c("NIST-CSF", "RS.RP", "Response Planning",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Execute response processes during and after incidents."),
    _c("NIST-CSF", "RC.RP", "Recovery Planning",
       [CAP_BACKUP], [_EVIDENCE["backup_manifest"]],
       "Execute recovery processes to restore impaired systems."),
]

_ISO42001_CONTROLS = [
    _c("ISO42001", "5.1", "AI Leadership and Commitment",
       [CAP_AI_GOV], [_EVIDENCE["model_cards"]],
       "Top management commitment to AI management system."),
    _c("ISO42001", "5.2", "AI Policy",
       [CAP_AI_GOV], [_EVIDENCE["model_cards"]],
       "Establish AI policy appropriate to purpose of the organization."),
    _c("ISO42001", "6.1", "AI Risk Assessment",
       [CAP_VALIDATION, CAP_AI_GOV], [_EVIDENCE["validation_findings"], _EVIDENCE["evaluations"]],
       "Assess risks and opportunities for the AI management system."),
    _c("ISO42001", "7.1", "AI Resources",
       [CAP_AI_GOV], [_EVIDENCE["model_cards"]],
       "Determine and provide resources for AI management."),
    _c("ISO42001", "8.1", "AI Operational Planning",
       [CAP_AI_GOV], [_EVIDENCE["model_cards"], _EVIDENCE["evaluations"]],
       "Plan, implement and control AI processes."),
    _c("ISO42001", "8.2", "AI System Lifecycle",
       [CAP_AI_GOV, CAP_AUDIT], [_EVIDENCE["model_cards"], _EVIDENCE["audit_write"]],
       "Manage AI system lifecycle from design to decommission."),
    _c("ISO42001", "8.4", "AI Impact Assessment",
       [CAP_AI_GOV, CAP_VALIDATION], [_EVIDENCE["evaluations"]],
       "Conduct impact assessments for AI systems."),
    _c("ISO42001", "9.1", "AI Performance Monitoring",
       [CAP_AI_GOV, CAP_AUDIT], [_EVIDENCE["evaluations"], _EVIDENCE["audit_write"]],
       "Monitor, measure and evaluate AI system performance."),
    _c("ISO42001", "9.2", "AI Internal Audit",
       [CAP_AUDIT], [_EVIDENCE["audit_write"]],
       "Conduct internal audits of AI management system."),
    _c("ISO42001", "10.1", "AI Continual Improvement",
       [CAP_AI_GOV], [_EVIDENCE["evaluations"]],
       "Continually improve AI management system effectiveness."),
]


def extended_packs() -> list[CompliancePack]:
    """Return the four extended compliance framework packs."""
    return [
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:ccpa",
            framework="CCPA",
            version="2024.1",
            description="California Consumer Privacy Act / CPRA compliance pack.",
            controls=_CCPA_CONTROLS,
            report_templates=["compliance-evidence", "executive-brief"],
        ),
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:pci-dss",
            framework="PCI-DSS",
            version="4.0",
            description="Payment Card Industry Data Security Standard v4.0 pack.",
            controls=_PCI_DSS_CONTROLS,
            report_templates=["compliance-evidence", "executive-brief"],
        ),
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:nist-csf",
            framework="NIST-CSF",
            version="2.0",
            description="NIST Cybersecurity Framework v2.0 pack.",
            controls=_NIST_CSF_CONTROLS,
            report_templates=["compliance-evidence", "executive-brief"],
        ),
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:iso42001",
            framework="ISO42001",
            version="2023.1",
            description="ISO/IEC 42001:2023 AI Management System pack.",
            controls=_ISO42001_CONTROLS,
            report_templates=["compliance-evidence", "executive-brief"],
        ),
    ]


def extended_pack_by_framework(framework: str) -> CompliancePack | None:
    for pack in extended_packs():
        if pack.framework.lower() == framework.lower():
            return pack
    return None
