"""Deterministic specialist agents for knowledge, operations, and governance."""

from __future__ import annotations

from collections import Counter
from uuid import uuid4

from eoip.agents.incident_correlation import IncidentCorrelationAgent
from eoip.agents.trace_impact import TraceImpactAgent
from eoip.contracts.agent import (
    AgentRequest,
    AgentResult,
    ChangeProposal,
    ConfidenceInput,
    ExplanationEnvelope,
    RuleDecision,
)
from eoip.contracts.source_event import utc_now_iso
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS
from eoip.retrieval.service import retrieve


class _ConfiguredAgent:
    allowed_tools = frozenset({"search", "entity", "evidence"})
    max_steps = 10
    max_seconds = 30.0

    def __init__(self, config: dict | None = None) -> None:
        if not config:
            return
        budgets = config.get("budgets", {})
        self.max_steps = budgets.get("max_steps", self.max_steps)
        self.max_seconds = budgets.get("max_seconds", self.max_seconds)
        if config.get("allowed_tools"):
            self.allowed_tools = frozenset(config["allowed_tools"])


class DataQualityAgent(_ConfiguredAgent):
    """Find graph records with missing identity or provenance."""

    agent_id = "DataQuality"
    allowed_tools = frozenset({"search", "entity", "quality", "evidence"})

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        limit = min(int((request.budgets or {}).get("max_context_items", 100)), 5000)
        vertices = store.find_vertices(limit=limit)
        issues: list[str] = []
        for vertex in vertices:
            properties = vertex.get("properties", {})
            canonical_id = properties.get("canonical_id") or vertex.get("canonical_id")
            if not canonical_id:
                issues.append(f"vid:{vertex.get('vid')}:missing-canonical-id")
                continue
            incoming = store.edges_to(vertex["vid"], limit=25)
            if vertex["label"] not in {"Evidence", "IngestionRun", "AgentRun"} and not any(
                edge["label"] in {"EVIDENCED_BY", "INGESTED_IN"} for edge in incoming
            ):
                issues.append(canonical_id)
        status = "SUCCEEDED" if not issues else "PARTIAL"
        return AgentResult(
            request_id=request.request_id,
            status=status,
            summary=(
                f"Checked {len(vertices)} graph entities; found {len(issues)} identity or provenance gap(s)."
            ),
            evidence_refs=issues[:100],
            tool_calls=[{"tool": "quality", "input": {"limit": limit}}],
            warnings=["Quality findings require human review before remediation"] if issues else None,
        )


class OntologyReviewAgent(_ConfiguredAgent):
    """Review stored labels and edge endpoints against the ontology manifest."""

    agent_id = "OntologyReview"
    allowed_tools = frozenset({"search", "entity", "ontology", "evidence"})

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        vertices = store.find_vertices(limit=2000)
        edges = store.find_edges(limit=5000)
        findings: list[str] = []
        by_vid = {item["vid"]: item for item in vertices}
        for vertex in vertices:
            if vertex["label"] not in VERTEX_LABELS:
                findings.append(f"unknown-vertex-label:{vertex['label']}:{vertex['vid']}")
        for edge in edges:
            definition = EDGE_LABELS.get(edge["label"])
            if definition is None:
                findings.append(f"unknown-edge-label:{edge['label']}:{edge['eid']}")
                continue
            out_labels, in_labels, _ = definition
            source, target = by_vid.get(edge["out_v"]), by_vid.get(edge["in_v"])
            if source and source["label"] not in out_labels:
                findings.append(f"invalid-source:{edge['eid']}")
            if target and target["label"] not in in_labels:
                findings.append(f"invalid-target:{edge['eid']}")
        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED" if not findings else "PARTIAL",
            summary=f"Reviewed {len(vertices)} vertices and {len(edges)} edges; found {len(findings)} ontology issue(s).",
            evidence_refs=findings[:100],
            tool_calls=[{"tool": "ontology", "input": {"mode": "conformance"}}],
        )


class ConnectorDiagnosisAgent(_ConfiguredAgent):
    """Diagnose failed and partial ingestion runs without accessing source secrets."""

    agent_id = "ConnectorDiagnosis"
    allowed_tools = frozenset({"search", "entity", "connector_status", "evidence"})

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        runs = store.find_vertices(label="IngestionRun", limit=500)
        unhealthy = [
            run for run in runs
            if str(run["properties"].get("run_status", "")).upper() in {"FAILED", "PARTIAL", "CANCELLED"}
        ]
        counts = Counter(str(run["properties"].get("source_system", "unknown")) for run in unhealthy)
        breakdown = ", ".join(f"{source}: {count}" for source, count in sorted(counts.items()))
        refs = [run["properties"].get("canonical_id", run["vid"]) for run in unhealthy]
        summary = f"Inspected {len(runs)} ingestion runs; {len(unhealthy)} require attention."
        if breakdown:
            summary += f" By source: {breakdown}."
        return AgentResult(
            request_id=request.request_id,
            status="PARTIAL" if unhealthy else "SUCCEEDED",
            summary=summary,
            evidence_refs=refs,
            tool_calls=[{"tool": "connector_status", "input": {"limit": 500}}],
        )


class DocumentationFreshnessAgent(_ConfiguredAgent):
    """Identify documents without content hashes or documented targets."""

    agent_id = "DocumentationFreshness"

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        documents = store.find_vertices(label="Document", limit=1000)
        stale: list[str] = []
        for document in documents:
            props = document["properties"]
            has_target = any(edge["label"] == "DOCUMENTS" for edge in store.edges_from(document["vid"]))
            if not props.get("content_hash") or not has_target:
                stale.append(props["canonical_id"])
        return AgentResult(
            request_id=request.request_id,
            status="PARTIAL" if stale else "SUCCEEDED",
            summary=f"Checked {len(documents)} documents; {len(stale)} freshness or coverage gap(s) found.",
            evidence_refs=stale,
            tool_calls=[{"tool": "search", "input": {"label": "Document"}}],
        )


class EvidenceVerificationAgent(_ConfiguredAgent):
    """Verify that graph facts carry source or evidence references."""

    agent_id = "EvidenceVerification"

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        edges = store.find_edges(limit=5000)
        unsupported = [
            edge for edge in edges
            if edge["label"] not in {"EVIDENCED_BY", "INGESTED_IN"}
            and not edge["properties"].get("source_ref")
            and not edge["properties"].get("evidence_key")
        ]
        refs = [edge.get("eid", f"{edge['out_v']}:{edge['label']}:{edge['in_v']}") for edge in unsupported]
        return AgentResult(
            request_id=request.request_id,
            status="PARTIAL" if unsupported else "SUCCEEDED",
            summary=f"Verified {len(edges)} graph facts; {len(unsupported)} lack direct provenance.",
            evidence_refs=refs[:100],
            tool_calls=[{"tool": "evidence", "input": {"scope": "edges"}}],
        )


class ArchitectureConformanceAgent(_ConfiguredAgent):
    """Detect dependency records that lack graph ownership or evidence."""

    agent_id = "ArchitectureConformance"

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        dependencies = store.find_vertices(label="Dependency", limit=2000)
        gaps = []
        for dependency in dependencies:
            incident_edges = store.edges_from(dependency["vid"]) + store.edges_to(dependency["vid"])
            labels = {edge["label"] for edge in incident_edges}
            if not labels.intersection({"DEPENDS_ON", "EVIDENCED_BY", "BELONGS_TO_DOMAIN"}):
                gaps.append(dependency["properties"]["canonical_id"])
        return AgentResult(
            request_id=request.request_id,
            status="PARTIAL" if gaps else "SUCCEEDED",
            summary=f"Reviewed {len(dependencies)} dependencies; found {len(gaps)} architecture conformance gap(s).",
            evidence_refs=gaps,
            tool_calls=[{"tool": "search", "input": {"label": "Dependency"}}],
        )


class QueryOptimizationAgent(_ConfiguredAgent):
    """Report high-cardinality graph areas that need bounded query plans."""

    agent_id = "QueryOptimization"

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        counts = {label: store.count_vertices(label) for label in VERTEX_LABELS}
        heavy = sorted(((count, label) for label, count in counts.items() if count), reverse=True)[:10]
        refs = [f"urn:eoip:ontology:vertex:{label}" for _, label in heavy]
        summary = "Largest vertex populations: " + ", ".join(
            f"{label}={count}" for count, label in heavy
        ) if heavy else "The graph is empty; no query optimization findings."
        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED",
            summary=summary,
            evidence_refs=refs,
            tool_calls=[{"tool": "search", "input": {"analysis": "cardinality"}}],
        )


class GraphInvestigatorAgent(_ConfiguredAgent):
    """Answer graph questions with optional local-model synthesis and grounded XAI."""

    agent_id = "GraphInvestigator"
    allowed_tools = frozenset({"search", "entity", "impact", "evidence"})
    max_seconds = 60.0

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        if not request.context_refs:
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary="GraphInvestigator requires a canonical entity context.",
                evidence_refs=[],
                warnings=["Select an entity or supply context_refs."],
            )
        canonical_id = request.context_refs[0]
        retrieval = retrieve(
            store,
            canonical_id,
            request.goal,
            synthesize=bool(request.metadata.get("synthesize", False)),
            model_timeout=min(float((request.budgets or {}).get("max_seconds", 30)), 30.0),
            max_model_tokens=min(int((request.budgets or {}).get("max_model_tokens", 512)), 2048),
        )
        graph_paths = [
            [vertex["properties"]["canonical_id"] for vertex in item["path"]["vertices"]]
            for item in retrieval.graph.get("impacted", [])
        ]
        evidence_ratio = min(1.0, len(retrieval.evidence_refs) / max(1, len(retrieval.contexts)))
        confidence = round(0.55 + (0.4 * evidence_ratio), 3)
        return AgentResult(
            request_id=request.request_id,
            status="PARTIAL" if retrieval.partial or retrieval.warnings else "SUCCEEDED",
            summary=retrieval.answer or "Grounded evidence was retrieved.",
            evidence_refs=retrieval.evidence_refs,
            tool_calls=[{
                "tool": "impact",
                "input": {"canonical_id": canonical_id, "strategy": retrieval.strategy},
            }],
            warnings=retrieval.warnings or None,
            explanation=ExplanationEnvelope(
                decision_summary=retrieval.answer or "Grounded evidence was retrieved.",
                observed_facts=[
                    f"Retrieved {retrieval.metrics.get('entities', 0)} graph entities.",
                    f"Generation mode: {retrieval.generation}.",
                ],
                evidence_refs=retrieval.evidence_refs,
                graph_paths=graph_paths,
                rule_decisions=[RuleDecision(
                    rule_id="AI-GROUNDED-CONTEXT-ONLY",
                    outcome="ALLOW",
                    summary="Synthesis was constrained to firewall-treated graph context.",
                )],
                confidence=confidence,
                confidence_inputs=[ConfidenceInput(
                    name="cited_context_ratio",
                    value=evidence_ratio,
                    evidence_refs=retrieval.evidence_refs,
                )],
                uncertainty=list(retrieval.warnings),
            ),
        )


class KnowledgeCuratorAgent(DataQualityAgent):
    """Produce approval-gated remediation proposals for knowledge quality gaps."""

    agent_id = "KnowledgeCurator"

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        result = super().execute(request, store)
        proposals = [
            ChangeProposal(
                proposal_id=str(uuid4()),
                run_id=request.request_id,
                proposed_by=self.agent_id,
                operation="REVIEW_PROVENANCE",
                target_ref=ref,
                patch={"action": "attach_verified_evidence"},
                rationale="The entity has no observed evidence or ingestion relationship.",
                evidence_refs=[ref],
                created_at=utc_now_iso(),
            )
            for ref in result.evidence_refs[:20]
        ]
        return result.model_copy(update={
            "summary": result.summary + f" Created {len(proposals)} inert remediation proposal(s).",
            "proposals": proposals,
        })


class ChangeImpactAgent(TraceImpactAgent):
    """Trace bounded change impact with graph-path evidence."""

    agent_id = "ChangeImpact"


class IncidentInvestigationAgent(IncidentCorrelationAgent):
    """Investigate incident correlations across changes, deployments, and evidence."""

    agent_id = "IncidentInvestigation"
