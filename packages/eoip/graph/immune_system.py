"""Enterprise Knowledge Immune System (G2-IMMUNE-001..013, MS-19).

Continuously scans the knowledge graph for anomalies, poisoning, and structural debt:
- Orphan nodes (G2-IMMUNE-001)
- Missing mandatory relationships (G2-IMMUNE-002)
- Contradictory claims (G2-IMMUNE-003)
- Stale documentation (G2-IMMUNE-004)
- Schema/mapping drift (G2-IMMUNE-005)
- Unexpected architecture edges (G2-IMMUNE-006)
- Missing ownership (G2-IMMUNE-007)
- Broken provenance/evidence references (G2-IMMUNE-008)
- Suspicious/low-confidence AI-inferred relationships (G2-IMMUNE-009)
- Graph poisoning and semantic injection anomalies (G2-IMMUNE-010)
- Recommend repair, quarantine, re-ingestion, or human review (G2-IMMUNE-011)
- Strict non-silent rewrite policy (G2-IMMUNE-012)
- Verifiable explanatory rationale for every finding (G2-IMMUNE-013)
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class ImmuneFinding:
    finding_id: str
    rule_code: str  # e.g. IMMUNE-ORPHAN, IMMUNE-MISSING-REL, IMMUNE-POISON
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    entity_id: str
    entity_label: str
    summary: str
    why_generated: str  # G2-IMMUNE-013
    recommended_action: str  # QUARANTINE, REPAIR_PROPOSAL, RE_INGESTION, HUMAN_REVIEW (G2-IMMUNE-011)
    status: str = "QUARANTINED"  # Never silently applied (G2-IMMUNE-012)
    detected_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EnterpriseKnowledgeImmuneSystem:
    """Active Graph & Agent Memory Immune Defense System."""

    def __init__(self, store: GraphStore) -> None:
        self.store = store
        self._quarantine: dict[str, ImmuneFinding] = {}

    def scan_graph(self) -> list[ImmuneFinding]:
        """Runs the complete suite of immune health and anti-poisoning scans."""
        findings: list[ImmuneFinding] = []
        findings.extend(self.detect_orphan_nodes())
        findings.extend(self.detect_missing_mandatory_relationships())
        findings.extend(self.detect_contradictory_claims())
        findings.extend(self.detect_stale_documentation())
        findings.extend(self.detect_schema_drift())
        findings.extend(self.detect_unexpected_architecture_edges())
        findings.extend(self.detect_missing_ownership())
        findings.extend(self.detect_broken_provenance())
        findings.extend(self.detect_suspicious_ai_relationships())
        findings.extend(self.detect_graph_poisoning_anomalies())

        for f in findings:
            self._quarantine[f.finding_id] = f

        return findings

    def detect_orphan_nodes(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-001: Detect orphan nodes with zero in-degree and out-degree."""
        findings: list[ImmuneFinding] = []
        vertices = self.store.find_vertices(limit=1000)
        for v in vertices:
            vid = v["vid"]
            out_edges = self.store.find_edges(out_v=vid, limit=1)
            in_edges = self.store.find_edges(in_v=vid, limit=1)
            if not out_edges and not in_edges:
                fid = f"imm-orphan-{vid}"
                findings.append(ImmuneFinding(
                    finding_id=fid,
                    rule_code="IMMUNE-001-ORPHAN",
                    severity="LOW",
                    entity_id=v.get("canonical_id", str(vid)),
                    entity_label=v.get("label", "Unknown"),
                    summary="Orphan vertex has no inbound or outbound graph relationships",
                    why_generated="Detected entity disconnected from all topology, dependencies, and ownership chains",
                    recommended_action="REPAIR_PROPOSAL",
                ))
        return findings

    def detect_missing_mandatory_relationships(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-002: Detect vertices missing mandatory relationship endpoints."""
        findings: list[ImmuneFinding] = []
        services = self.store.find_vertices(label="APIService", limit=500)
        for s in services:
            vid = s["vid"]
            edges = self.store.find_edges(out_v=vid, label="EXPOSES", limit=1)
            if not edges:
                findings.append(ImmuneFinding(
                    finding_id=f"imm-missing-rel-{vid}",
                    rule_code="IMMUNE-002-MISSING-REL",
                    severity="MEDIUM",
                    entity_id=s.get("canonical_id", str(vid)),
                    entity_label="APIService",
                    summary=f"APIService '{s.get('canonical_id')}' missing mandatory EXPOSES endpoint relation",
                    why_generated="Enterprise ontology mandates every API service must expose at least one APIEndpoint",
                    recommended_action="HUMAN_REVIEW",
                ))
        return findings

    def detect_contradictory_claims(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-003: Detect contradictory claims or mutually exclusive states."""
        findings: list[ImmuneFinding] = []
        vertices = self.store.find_vertices(limit=1000)
        for v in vertices:
            status = str(v.get("properties", {}).get("status", "")).upper()
            approval_status = str(v.get("properties", {}).get("approval_status", "")).upper()
            if status == "DEPRECATED" and approval_status == "APPROVED":
                findings.append(ImmuneFinding(
                    finding_id=f"imm-contra-{v['vid']}",
                    rule_code="IMMUNE-003-CONTRADICTION",
                    severity="HIGH",
                    entity_id=v.get("canonical_id", str(v["vid"])),
                    entity_label=v.get("label", "Unknown"),
                    summary="Contradictory state: entity marked DEPRECATED but APPROVED",
                    why_generated="Detected mutually exclusive claim states in entity properties",
                    recommended_action="QUARANTINE",
                ))
        return findings

    def detect_stale_documentation(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-004: Detect documentation not updated in sync with code."""
        findings: list[ImmuneFinding] = []
        docs = self.store.find_vertices(label="Document", limit=500)
        now = time.time()
        for d in docs:
            mod_at = float(d.get("properties", {}).get("modified_at", now))
            if (now - mod_at) > (180 * 86400):  # 180 days stale
                findings.append(ImmuneFinding(
                    finding_id=f"imm-stale-doc-{d['vid']}",
                    rule_code="IMMUNE-004-STALE-DOC",
                    severity="LOW",
                    entity_id=d.get("canonical_id", str(d["vid"])),
                    entity_label="Document",
                    summary=f"Document '{d.get('canonical_id')}' has not been refreshed in >180 days",
                    why_generated="Staleness threshold exceeded; document age exceeds code modification timeline",
                    recommended_action="RE_INGESTION",
                ))
        return findings

    def detect_schema_drift(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-005: Detect source-to-ontology schema or mapping drift."""
        findings: list[ImmuneFinding] = []
        vertices = self.store.find_vertices(limit=500)
        for v in vertices:
            dev_type = v.get("properties", {}).get("deviation_type")
            if dev_type == "SCHEMA_DRIFT":
                findings.append(ImmuneFinding(
                    finding_id=f"imm-drift-{v['vid']}",
                    rule_code="IMMUNE-005-SCHEMA-DRIFT",
                    severity="MEDIUM",
                    entity_id=v.get("canonical_id", str(v["vid"])),
                    entity_label=v.get("label", "Unknown"),
                    summary=f"Schema mapping drift detected: {dev_type}",
                    why_generated="External crawler ingested fields absent from active ontology schema",
                    recommended_action="REPAIR_PROPOSAL",
                ))
        return findings

    def detect_unexpected_architecture_edges(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-006: Detect architectural boundary violations."""
        findings: list[ImmuneFinding] = []
        edges = self.store.find_edges(limit=2000)
        for e in edges:
            if e.get("label") == "CALLS":
                out_v = self.store.get_vertex(e["out_v"])
                in_v = self.store.get_vertex(e["in_v"])
                if out_v and in_v:
                    out_q = str(out_v.get("properties", {}).get("qualified_name", ""))
                    in_q = str(in_v.get("properties", {}).get("qualified_name", ""))
                    if out_q.startswith("ui.") and in_q.startswith("db."):
                        findings.append(ImmuneFinding(
                            finding_id=f"imm-arch-edge-{e['eid']}",
                            rule_code="IMMUNE-006-UNEXPECTED-EDGE",
                            severity="CRITICAL",
                            entity_id=out_v.get("canonical_id", str(e["out_v"])),
                            entity_label="CodeSymbol",
                            summary="Direct database query call from UI handler bypasses API layer",
                            why_generated="Architecture boundary rule 'UI MUST_NOT_ACCESS database directly' was violated",
                            recommended_action="HUMAN_REVIEW",
                        ))
        return findings

    def detect_missing_ownership(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-007: Detect entities lacking steward or team ownership."""
        findings: list[ImmuneFinding] = []
        services = self.store.find_vertices(label="APIService", limit=500)
        for s in services:
            owner = s.get("properties", {}).get("owner_id")
            if not owner:
                findings.append(ImmuneFinding(
                    finding_id=f"imm-owner-{s['vid']}",
                    rule_code="IMMUNE-007-NO-OWNER",
                    severity="HIGH",
                    entity_id=s.get("canonical_id", str(s["vid"])),
                    entity_label="APIService",
                    summary=f"APIService '{s.get('canonical_id')}' lacks ownership attribution",
                    why_generated="Zero team or steward metadata declared for public API endpoint",
                    recommended_action="HUMAN_REVIEW",
                ))
        return findings

    def detect_broken_provenance(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-008: Detect broken provenance or evidence references."""
        findings: list[ImmuneFinding] = []
        vertices = self.store.find_vertices(limit=500)
        for v in vertices:
            ev_ref = v.get("properties", {}).get("source_ref")
            if ev_ref == "MISSING_HASH" or ev_ref == "NULL_RECEIPT":
                findings.append(ImmuneFinding(
                    finding_id=f"imm-broken-prov-{v['vid']}",
                    rule_code="IMMUNE-008-BROKEN-PROVENANCE",
                    severity="HIGH",
                    entity_id=v.get("canonical_id", str(v["vid"])),
                    entity_label=v.get("label", "Unknown"),
                    summary=f"Broken evidence reference for entity: {ev_ref}",
                    why_generated="Provenance receipt hash does not resolve to an immutable audit record",
                    recommended_action="QUARANTINE",
                ))
        return findings


    def detect_suspicious_ai_relationships(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-009: Detect low-confidence AI-inferred relationships."""
        findings: list[ImmuneFinding] = []
        edges = self.store.find_edges(limit=2000)
        for e in edges:
            conf = float(e.get("properties", {}).get("confidence", 1.0))
            is_inferred = e.get("properties", {}).get("creation_status") == "INFERRED"
            if is_inferred and conf < 0.65:
                findings.append(ImmuneFinding(
                    finding_id=f"imm-ai-suspicious-{e['eid']}",
                    rule_code="IMMUNE-009-LOW-CONF-AI",
                    severity="MEDIUM",
                    entity_id=f"{e['out_v']}->{e['in_v']}",
                    entity_label="Edge",
                    summary=f"Low-confidence AI relationship ({conf:.2f} < 0.65 threshold)",
                    why_generated="Inferred link confidence below enterprise auto-approval boundary",
                    recommended_action="HUMAN_REVIEW",
                ))
        return findings

    def detect_graph_poisoning_anomalies(self) -> list[ImmuneFinding]:
        """G2-IMMUNE-010: Detect adversarial prompt injection or graph poisoning attempts."""
        findings: list[ImmuneFinding] = []
        suspicious_patterns = ["IGNORE PREVIOUS INSTRUCTIONS", "<script>", "DROP TABLE", "BASE64_EXEC"]
        vertices = self.store.find_vertices(limit=1000)
        for v in vertices:
            text = " ".join(str(val) for val in v.get("properties", {}).values()).upper()
            for pattern in suspicious_patterns:
                if pattern in text:
                    findings.append(ImmuneFinding(
                        finding_id=f"imm-poison-{v['vid']}",
                        rule_code="IMMUNE-010-POISONING",
                        severity="CRITICAL",
                        entity_id=v.get("canonical_id", str(v["vid"])),
                        entity_label=v.get("label", "Unknown"),
                        summary=f"Potential graph poisoning attempt containing signature: {pattern}",
                        why_generated="Adversarial prompt injection pattern detected in entity property payload",
                        recommended_action="QUARANTINE",
                    ))
                    break
        return findings

    def get_quarantined_findings(self) -> list[dict[str, Any]]:
        """Returns all quarantined findings pending human verification."""
        return [f.to_dict() for f in self._quarantine.values()]


@dataclass
class MemoryRiskAssessment:
    write_id: str
    aggregate_risk: float
    signal_scores: dict[str, float]
    decision: str  # ALLOW or QUARANTINE
    rationale: str
    quarantined_payload: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AMISMemoryGuard:
    """Agent Memory Immune System (AMIS - MS-19).

    Provides 5-signal write-time anti-poisoning defense for agent memories and graph updates:
    1. Source reputation tier (asserted/curated vs inferred/untrusted)
    2. Behavioral phrasing patterns (urgency framing, forced imperatives)
    3. External contact patterns (suspicious domains, unverified callbacks)
    4. Contradiction risk (conflicts with established truth in the graph)
    5. Injection anomaly (adversarial prompts, shell code, SQL/HTML tags)
    """

    REPUTATION_WEIGHTS = {
        "CURATED": 0.05,
        "ASSERTED": 0.15,
        "DERIVED": 0.35,
        "INFERRED": 0.60,
        "UNTRUSTED": 0.95,
    }

    INJECTION_TRIGGERS = [
        "IGNORE PREVIOUS INSTRUCTIONS",
        "SYSTEM PROMPT OVERRIDE",
        "<SCRIPT>",
        "DROP TABLE",
        "EXEC(",
        "BASE64_EXEC",
        "AGENT_ROOT_ACCESS",
    ]

    URGENCY_TRIGGERS = [
        "DO NOT VERIFY",
        "OVERRIDE IMMEDIATELY",
        "EMERGENCY BYPASS",
        "URGENT UNVERIFIED",
    ]

    def __init__(self, risk_threshold: float = 0.65) -> None:
        self.risk_threshold = risk_threshold
        self._quarantined_writes: dict[str, MemoryRiskAssessment] = {}

    def assess_memory_write(
        self,
        write_payload: dict[str, Any],
        existing_facts: list[dict[str, Any]] | None = None,
    ) -> MemoryRiskAssessment:
        write_id = str(write_payload.get("write_id", f"write-{int(time.time()*1000)}"))
        source_tier = str(write_payload.get("source_tier", "UNTRUSTED")).upper()
        content = " ".join(str(v) for v in write_payload.values()).upper()

        # Signal 1: Source reputation
        sig1 = self.REPUTATION_WEIGHTS.get(source_tier, 0.90)

        # Signal 2: Behavioral phrasing
        sig2 = 0.1
        for phrase in self.URGENCY_TRIGGERS:
            if phrase in content:
                sig2 = 0.9
                break

        # Signal 3: External contact patterns
        sig3 = 0.1
        if "HTTP://" in content or "ONION" in content or "CALLBACK_URL" in content:
            sig3 = 0.8

        # Signal 4: Contradiction risk
        sig4 = 0.1
        if existing_facts:
            target_key = write_payload.get("canonical_id")
            for fact in existing_facts:
                if fact.get("canonical_id") == target_key:
                    # check if conflicting status
                    if fact.get("properties", {}).get("status") != write_payload.get("status"):
                        sig4 = 0.75
                        break

        # Signal 5: Injection anomaly
        sig5 = 0.05
        for trigger in self.INJECTION_TRIGGERS:
            if trigger in content:
                sig5 = 1.0
                break

        # Weighted aggregate
        aggregate = (
            sig1 * 0.25
            + sig2 * 0.20
            + sig3 * 0.15
            + sig4 * 0.20
            + sig5 * 0.20
        )

        decision = "QUARANTINE" if aggregate >= self.risk_threshold else "ALLOW"
        rationale = (
            f"AMIS 5-Signal Assessment (aggregate={aggregate:.3f}, threshold={self.risk_threshold}): "
            f"Reputation={sig1:.2f}, Phrasing={sig2:.2f}, External={sig3:.2f}, "
            f"Contradiction={sig4:.2f}, Injection={sig5:.2f} -> {decision}"
        )

        assessment = MemoryRiskAssessment(
            write_id=write_id,
            aggregate_risk=round(aggregate, 4),
            signal_scores={
                "source_reputation": sig1,
                "behavioral_phrasing": sig2,
                "external_contact": sig3,
                "contradiction_risk": sig4,
                "injection_anomaly": sig5,
            },
            decision=decision,
            rationale=rationale,
            quarantined_payload=write_payload if decision == "QUARANTINE" else None,
        )

        if decision == "QUARANTINE":
            self._quarantined_writes[write_id] = assessment

        return assessment

    def get_quarantined_writes(self) -> list[dict[str, Any]]:
        return [q.to_dict() for q in self._quarantined_writes.values()]

