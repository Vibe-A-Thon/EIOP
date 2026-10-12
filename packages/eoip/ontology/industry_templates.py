"""Packaged industry templates service (GAP-TEMPLATE, GAP-MKT-003, GAP-MKT-006).

Provides ready-to-deploy domain templates for:
- ENGINEERING: Services, repositories, deployments, PRs, symbols
- AUDIT: Evidence records, audit logs, signoffs, immutable provenance
- RISK: Risk registers, threat models, vulnerabilities, mitigating controls
- INCIDENT: Outages, root-cause analyses, post-mortems, on-call escalations
- ARCHITECTURE: ADRs, capabilities, technology standards, boundaries
- COMPLIANCE: SOC2/ISO controls, policies, attestations, review cycles
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class IndustryTemplate:
    template_id: str
    name: str
    category: str
    description: str
    classes: list[dict[str, Any]]
    relationships: list[dict[str, Any]]
    recommended_queries: list[str] = field(default_factory=list)


INDUSTRY_TEMPLATES: dict[str, IndustryTemplate] = {
    "engineering": IndustryTemplate(
        template_id="template:engineering",
        name="Software Engineering Excellence",
        category="engineering",
        description="Core SDLC ontology: services, repos, commits, PRs, and CI/CD pipelines.",
        classes=[
            {"label": "Service", "domain": "ENGINEERING", "properties": ["name", "service_id", "tier"]},
            {"label": "Repository", "domain": "ENGINEERING", "properties": ["name", "url", "default_branch"]},
            {"label": "Commit", "domain": "ENGINEERING", "properties": ["commit_sha", "message", "author"]},
        ],
        relationships=[
            {"label": "DECLARES", "source": "Repository", "target": "Service"},
            {"label": "CONTAINS", "source": "Repository", "target": "Commit"},
        ],
        recommended_queries=["MATCH (r:Repository)-[:DECLARES]->(s:Service) RETURN r, s"],
    ),
    "audit": IndustryTemplate(
        template_id="template:audit",
        name="Enterprise Audit & Provenance",
        category="audit",
        description="Immutable audit trail and evidence linking for internal and external auditors.",
        classes=[
            {"label": "AuditEvent", "domain": "GOVERNANCE", "properties": ["event_id", "actor", "timestamp", "action"]},
            {"label": "AuditEvidence", "domain": "GOVERNANCE", "properties": ["evidence_id", "hash", "source_system"]},
        ],
        relationships=[
            {"label": "EVIDENCED_BY", "source": "AuditEvent", "target": "AuditEvidence"},
        ],
        recommended_queries=["MATCH (a:AuditEvent)-[:EVIDENCED_BY]->(e:AuditEvidence) RETURN a, e"],
    ),
    "risk": IndustryTemplate(
        template_id="template:risk",
        name="Enterprise Risk & Threat Modeling",
        category="risk",
        description="Risk registers, threat scenarios, likelihood/impact scoring, and mitigating controls.",
        classes=[
            {"label": "RiskItem", "domain": "RISK", "properties": ["risk_id", "severity", "likelihood", "impact"]},
            {"label": "MitigationControl", "domain": "RISK", "properties": ["control_id", "status", "owner"]},
        ],
        relationships=[
            {"label": "MITIGATES", "source": "MitigationControl", "target": "RiskItem"},
        ],
        recommended_queries=["MATCH (c:MitigationControl)-[:MITIGATES]->(r:RiskItem) RETURN c, r"],
    ),
    "incident": IndustryTemplate(
        template_id="template:incident",
        name="Incident Response & Post-Mortem",
        category="incident",
        description="Incident tracking, blast radius, timeline events, and post-mortem remediation tasks.",
        classes=[
            {"label": "Incident", "domain": "OPERATIONS", "properties": ["incident_id", "severity", "status"]},
            {"label": "PostMortem", "domain": "OPERATIONS", "properties": ["document_id", "root_cause", "actions"]},
        ],
        relationships=[
            {"label": "DOCUMENTED_IN", "source": "Incident", "target": "PostMortem"},
        ],
        recommended_queries=["MATCH (i:Incident)-[:DOCUMENTED_IN]->(p:PostMortem) RETURN i, p"],
    ),
    "architecture": IndustryTemplate(
        template_id="template:architecture",
        name="Enterprise Architecture & ADRs",
        category="architecture",
        description="Architectural decision records, capabilities, components, and boundary contexts.",
        classes=[
            {"label": "ArchitectureDecision", "domain": "ARCHITECTURE", "properties": ["adr_id", "status", "rationale"]},
            {"label": "Component", "domain": "ARCHITECTURE", "properties": ["name", "boundary_context"]},
        ],
        relationships=[
            {"label": "DECIDES", "source": "ArchitectureDecision", "target": "Component"},
        ],
        recommended_queries=["MATCH (d:ArchitectureDecision)-[:DECIDES]->(c:Component) RETURN d, c"],
    ),
    "compliance": IndustryTemplate(
        template_id="template:compliance",
        name="Regulatory Compliance & Controls",
        category="compliance",
        description="SOC2, ISO27001, and HIPAA compliance requirements and automated verification evidence.",
        classes=[
            {"label": "ComplianceStandard", "domain": "COMPLIANCE", "properties": ["standard_id", "framework"]},
            {"label": "PolicyRequirement", "domain": "COMPLIANCE", "properties": ["rule_id", "frequency"]},
        ],
        relationships=[
            {"label": "MANDATES", "source": "ComplianceStandard", "target": "PolicyRequirement"},
        ],
        recommended_queries=["MATCH (s:ComplianceStandard)-[:MANDATES]->(p:PolicyRequirement) RETURN s, p"],
    ),
}


def list_industry_templates() -> list[dict[str, Any]]:
    """Lists all available industry templates (GAP-TEMPLATE)."""
    return [
        {
            "template_id": t.template_id,
            "name": t.name,
            "category": t.category,
            "description": t.description,
            "class_count": len(t.classes),
            "relationship_count": len(t.relationships),
        }
        for t in INDUSTRY_TEMPLATES.values()
    ]


def get_industry_template(template_id_or_category: str) -> IndustryTemplate:
    """Retrieves an industry template by id or category name."""
    key = template_id_or_category.lower().replace("template:", "").strip()
    if key not in INDUSTRY_TEMPLATES:
        raise KeyError(f"Template '{template_id_or_category}' not found. Available: {list(INDUSTRY_TEMPLATES.keys())}")
    return INDUSTRY_TEMPLATES[key]
