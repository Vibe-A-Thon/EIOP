"""Built-in Compliance Pack skeletons (SR-GOV-001, §14.4).

Skeleton catalogs for GDPR, SOC 2, ISO/IEC 27001, HIPAA and India DPDP Act
2023. Each pack declares >= 10 controls mapped to real platform capabilities
(audit sink, authz decisions, egress manifests, provenance evidence,
validation gates, governed proposals, tenancy isolation, kill switch,
backup/ops bundles, policy exceptions, AI governance records). Mappings are
skeletons, not certifications — the platform supports customer compliance;
attestation is a separate program (§14.4 note).

Additional frameworks from the §14.4 mapping table (CCPA/CPRA, LGPD, PIPEDA,
NIST CSF, PCI DSS, ISO/IEC 42001, EU AI Act...) are ADR-gated pack additions:
the format here is data-driven, so new packs only need control data.
"""

from __future__ import annotations

from eoip.compliance.pack import (
    CompliancePack,
    Control,
    EvidenceQuerySpec,
)

# Platform capability names referenced by controls (SR-GOV-001 mapping).
CAP_AUDIT = "audit-sink"
CAP_AUTHZ = "authz-decisions"
CAP_EGRESS = "egress-manifests"
CAP_PROV = "provenance-evidence"
CAP_VALIDATION = "validation-gates"
CAP_PROPOSALS = "governed-proposals"
CAP_TENANCY = "tenancy-isolation"
CAP_KILL = "kill-switch"
CAP_BACKUP = "backup-restore"
CAP_EXCEPTIONS = "policy-exceptions"
CAP_AI_GOV = "ai-governance"
CAP_ROLES = "roles-registry"
CAP_BITEMPORAL = "bitemporal-audit"

# Common evidence specs reused across packs (each >= 10 controls per pack).
_EVIDENCE = {
    "audit_write": EvidenceQuerySpec(
        kind="audit_event", params={"event_type": "audit.event"},
        description="Audit events persisted to the audit sink",
    ),
    "audit_mutation": EvidenceQuerySpec(
        kind="audit_event", params={"action": "graph.mutate"},
        description="Graph mutations recorded in audit trail",
    ),
    "audit_authz_deny": EvidenceQuerySpec(
        kind="authz_decisions", params={"action": "authz.deny"},
        description="Denied authorization decisions auditable",
    ),
    "roles_admin_steward": EvidenceQuerySpec(
        kind="authz_roles", params={"roles": ["admin", "steward"]},
        description="Separation-of-duties roles registered",
    ),
    "role_auditor": EvidenceQuerySpec(
        kind="authz_roles", params={"roles": ["auditor"]},
        description="Read-only auditor role registered (SR-GOV-004)",
    ),
    "graph_entity": EvidenceQuerySpec(
        kind="graph_vertices", params={"label": "Person"},
        description="Canonical entities present in graph",
    ),
    "evidence_vertices": EvidenceQuerySpec(
        kind="evidence_vertices", params={"label": "Evidence"},
        description="Provenance evidence vertices linked to facts",
    ),
    "proposals": EvidenceQuerySpec(
        kind="proposals", description="Governed change proposals on record",
    ),
    "approved_proposals": EvidenceQuerySpec(
        kind="proposals", params={"status": "APPROVED"},
        description="Approval-gated changes with recorded approval",
    ),
    "validation_findings": EvidenceQuerySpec(
        kind="validation_findings",
        description="Validation gate findings tracked",
    ),
    "backup_manifest": EvidenceQuerySpec(
        kind="backup_manifest", params={"filenames": ["manifest.json"]},
        description="Backup/ops bundle manifest produced",
    ),
    "exceptions": EvidenceQuerySpec(
        kind="policy_exceptions",
        description="Active time-boxed policy exceptions visible (SR-GOV-005)",
    ),
    "model_cards": EvidenceQuerySpec(
        kind="ai_governance", params={"record": "model_cards"},
        description="AI model cards registered (SR-GOV-002)",
    ),
    "evaluations": EvidenceQuerySpec(
        kind="ai_governance", params={"record": "evaluations"},
        description="AI model evaluation records present (SR-GOV-002)",
    ),
}


def _control(
    framework: str,
    suffix: str,
    title: str,
    capabilities: list[str],
    evidence: list[EvidenceQuerySpec],
    description: str = "",
) -> Control:
    return Control(
        control_id=f"{framework}-{suffix}",
        framework=framework,
        title=title,
        description=description,
        platform_capabilities=capabilities,
        evidence=evidence,
        report_template="compliance-evidence",
    )


_GDPR_CONTROLS = [
    _control("GDPR", "ART-05", "Principles: lawfulness and accountability",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("GDPR", "ART-06", "Lawfulness of processing recorded",
             [CAP_AUDIT, CAP_PROV], [_EVIDENCE["audit_write"], _EVIDENCE["evidence_vertices"]]),
    _control("GDPR", "ART-15", "Right of access: data discoverable in graph",
             [CAP_PROV], [_EVIDENCE["graph_entity"], _EVIDENCE["evidence_vertices"]]),
    _control("GDPR", "ART-17", "Right to erasure: tombstone + audit",
             [CAP_AUDIT], [_EVIDENCE["audit_mutation"]]),
    _control("GDPR", "ART-25", "Data protection by design: validation gates",
             [CAP_VALIDATION], [_EVIDENCE["validation_findings"]]),
    _control("GDPR", "ART-30", "Records of processing: provenance trail",
             [CAP_PROV, CAP_AUDIT], [_EVIDENCE["evidence_vertices"], _EVIDENCE["audit_write"]]),
    _control("GDPR", "ART-32", "Security of processing: authz + tenancy",
             [CAP_AUTHZ, CAP_TENANCY], [_EVIDENCE["roles_admin_steward"], _EVIDENCE["audit_authz_deny"]]),
    _control("GDPR", "ART-33", "Breach notification readiness",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("GDPR", "ART-35", "DPIA: impact assessment report template",
             ["report-templates"], [_EVIDENCE["audit_write"]]),
    _control("GDPR", "ART-39", "Compliance monitoring: auditor role",
             [CAP_ROLES], [_EVIDENCE["role_auditor"]]),
    _control("GDPR", "ART-44+", "Transfers: egress manifests",
             [CAP_EGRESS, CAP_AUDIT], [_EVIDENCE["audit_write"]]),
]

_SOC2_CONTROLS = [
    _control("SOC2", "CC-01", "Change management: governed proposals",
             [CAP_PROPOSALS], [_EVIDENCE["proposals"], _EVIDENCE["approved_proposals"]]),
    _control("SOC2", "CC-02", "Rollback capability: proposal rollback states",
             [CAP_PROPOSALS, CAP_BACKUP], [_EVIDENCE["proposals"]]),
    _control("SOC2", "CC-03", "Incident response: audit + reports",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("SOC2", "CC-04", "Backup and recovery: ops bundles",
             [CAP_BACKUP], [_EVIDENCE["backup_manifest"]]),
    _control("SOC2", "CC-05", "Logical access: RBAC + separation of duties",
             [CAP_AUTHZ, CAP_ROLES], [_EVIDENCE["roles_admin_steward"]]),
    _control("SOC2", "CC-06", "Access denial auditable",
             [CAP_AUTHZ, CAP_AUDIT], [_EVIDENCE["audit_authz_deny"]]),
    _control("SOC2", "CC-07", "System monitoring: audit sink",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("SOC2", "CC-08", "Vendor/AI change governance: model cards",
             [CAP_AI_GOV], [_EVIDENCE["model_cards"]]),
    _control("SOC2", "CC-09", "Data quality: validation gates",
             [CAP_VALIDATION], [_EVIDENCE["validation_findings"]]),
    _control("SOC2", "A-01", "Availability: kill switch + backup drill evidence",
             [CAP_KILL, CAP_BACKUP], [_EVIDENCE["backup_manifest"]]),
]

_ISO_CONTROLS = [
    _control("ISO27001", "A-5.15", "Access control: RBAC registry",
             [CAP_AUTHZ, CAP_ROLES], [_EVIDENCE["roles_admin_steward"]]),
    _control("ISO27001", "A-5.16", "Identity management: authn + roles",
             [CAP_ROLES], [_EVIDENCE["roles_admin_steward"]]),
    _control("ISO27001", "A-5.17", "Authentication information: secret redaction",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("ISO27001", "A-5.24", "Incident management: audit trail + RCA template",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("ISO27001", "A-5.29", "Continuity: backup manifests",
             [CAP_BACKUP], [_EVIDENCE["backup_manifest"]]),
    _control("ISO27001", "A-5.31", "Legal requirements: compliance packs",
             ["compliance-packs"], [_EVIDENCE["audit_write"]]),
    _control("ISO27001", "A-5.34", "Privacy: GDPR pack linkage",
             ["compliance-packs"], [_EVIDENCE["role_auditor"]]),
    _control("ISO27001", "A-8.15", "Logging: audit sink",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("ISO27001", "A-8.16", "Monitoring activities: authz decisions",
             [CAP_AUTHZ, CAP_AUDIT], [_EVIDENCE["audit_authz_deny"]]),
    _control("ISO27001", "A-8.32", "Change management: governed proposals",
             [CAP_PROPOSALS], [_EVIDENCE["approved_proposals"]]),
]

_HIPAA_CONTROLS = [
    _control("HIPAA", "164.308-a-1", "Security management: audit + validation",
             [CAP_AUDIT, CAP_VALIDATION], [_EVIDENCE["audit_write"], _EVIDENCE["validation_findings"]]),
    _control("HIPAA", "164.308-a-3", "Workforce security: roles registry",
             [CAP_ROLES], [_EVIDENCE["roles_admin_steward"]]),
    _control("HIPAA", "164.308-a-6", "Security incident procedures",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("HIPAA", "164.312-a-1", "Access control: default-deny authz",
             [CAP_AUTHZ], [_EVIDENCE["audit_authz_deny"]]),
    _control("HIPAA", "164.312-b", "Audit controls: persistent audit sink",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("HIPAA", "164.312-c-1", "Integrity: hard validation gates",
             [CAP_VALIDATION], [_EVIDENCE["validation_findings"]]),
    _control("HIPAA", "164.312-e-1", "Transmission security: egress manifests",
             [CAP_EGRESS], [_EVIDENCE["audit_write"]]),
    _control("HIPAA", "164.310-d-2", "Accountability: auditable authz decisions",
             [CAP_AUTHZ, CAP_AUDIT], [_EVIDENCE["audit_authz_deny"]]),
    _control("HIPAA", "164.308-a-7", "Contingency plan: backup/restore",
             [CAP_BACKUP], [_EVIDENCE["backup_manifest"]]),
    _control("HIPAA", "164.316", "Documentation: bitemporal audit history",
             [CAP_AUDIT, CAP_BITEMPORAL], [_EVIDENCE["audit_write"]]),
]

_DPDP_CONTROLS = [
    _control("DPDP", "S-4", "Consent management: provenance of processing basis",
             [CAP_PROV, CAP_AUDIT], [_EVIDENCE["evidence_vertices"], _EVIDENCE["audit_write"]]),
    _control("DPDP", "S-5", "Notice: data discoverable and explainable",
             [CAP_PROV], [_EVIDENCE["graph_entity"]]),
    _control("DPDP", "S-6", "Rights of data principals: access via graph",
             [CAP_PROV], [_EVIDENCE["graph_entity"], _EVIDENCE["evidence_vertices"]]),
    _control("DPDP", "S-8", "Obligations of data fiduciary: security safeguards",
             [CAP_AUTHZ, CAP_TENANCY], [_EVIDENCE["roles_admin_steward"]]),
    _control("DPDP", "S-9", "Significant data fiduciary: audits and AI duties",
             [CAP_AUDIT, CAP_AI_GOV], [_EVIDENCE["audit_write"], _EVIDENCE["model_cards"]]),
    _control("DPDP", "S-10", "Processing outside India: egress control",
             [CAP_EGRESS], [_EVIDENCE["audit_write"]]),
    _control("DPDP", "S-11", "Data breach notification: audit trail",
             [CAP_AUDIT], [_EVIDENCE["audit_write"]]),
    _control("DPDP", "S-12", "Children's data: validation rules",
             [CAP_VALIDATION], [_EVIDENCE["validation_findings"]]),
    _control("DPDP", "S-13", "Exemptions: time-boxed policy exceptions",
             [CAP_EXCEPTIONS], [_EVIDENCE["exceptions"]]),
    _control("DPDP", "S-22", "Penalties avoidance: compliance evidence reports",
             ["report-templates"], [_EVIDENCE["audit_write"]]),
]


def builtin_packs() -> list[CompliancePack]:
    """Return skeleton packs for the five built-in frameworks."""
    return [
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:gdpr",
            framework="GDPR",
            version="2023.1",
            description="EU/UK GDPR skeleton pack (SR-GOV-001, §14.4 Privacy).",
            controls=_GDPR_CONTROLS,
            report_templates=["compliance-evidence", "executive-brief"],
        ),
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:soc2",
            framework="SOC2",
            version="2023.1",
            description="SOC 2 Trust Services criteria skeleton pack.",
            controls=_SOC2_CONTROLS,
            report_templates=["compliance-evidence", "incident-rca", "executive-brief"],
        ),
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:iso27001",
            framework="ISO27001",
            version="2022.1",
            description="ISO/IEC 27001:2022 Annex A skeleton pack.",
            controls=_ISO_CONTROLS,
            report_templates=["compliance-evidence", "executive-brief"],
        ),
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:hipaa",
            framework="HIPAA",
            version="2023.1",
            description="HIPAA Security Rule skeleton pack (45 CFR 164).",
            controls=_HIPAA_CONTROLS,
            report_templates=["compliance-evidence", "incident-rca"],
        ),
        CompliancePack(
            pack_id="urn:eoip:compliance:pack:dpdp-2023",
            framework="DPDP-2023",
            version="2023.1",
            description="India Digital Personal Data Protection Act 2023 skeleton pack.",
            controls=_DPDP_CONTROLS,
            report_templates=["compliance-evidence", "executive-brief"],
        ),
    ]


def pack_by_framework(framework: str) -> CompliancePack | None:
    for pack in builtin_packs():
        if pack.framework.lower() == framework.lower():
            return pack
    return None
