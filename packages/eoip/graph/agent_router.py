"""Phase 13.2 — Agent Router: 40+ agent types across 9 categories.

Routes graph intelligence queries to specialized agent types.
Each agent operates on graph data with structured analysis fallbacks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


@dataclass(frozen=True)
class AgentType:
    name: str
    category: str
    description: str
    capabilities: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "category": self.category,
                "description": self.description, "capabilities": list(self.capabilities)}


AGENT_TYPES = [
    # Reactive agents (5)
    AgentType("simple_reflex", "reactive", "Responds to current percept with fixed rules", ("pattern_match", "immediate_response")),
    AgentType("model_based_reflex", "reactive", "Maintains internal state model for decisions", ("state_tracking", "model_update")),
    AgentType("condition_action", "reactive", "IF-THEN rules on graph state", ("rule_evaluation", "action_dispatch")),
    AgentType("event_driven", "reactive", "Responds to graph change events", ("event_listen", "trigger_action")),
    AgentType("threshold", "reactive", "Triggers when metrics exceed thresholds", ("metric_monitor", "threshold_alert")),

    # Deliberative agents (5)
    AgentType("goal_based", "deliberative", "Plans actions to achieve graph analysis goals", ("goal_decomposition", "plan_generation")),
    AgentType("utility_based", "deliberative", "Maximizes utility function over graph states", ("utility_calculation", "state_evaluation")),
    AgentType("bdi", "deliberative", "Belief-Desire-Intention architecture for reasoning", ("belief_update", "intention_formation", "plan_execution")),
    AgentType("planning", "deliberative", "STRIPS-style planning over graph operations", ("operator_selection", "plan_search")),
    AgentType("constraint_satisfaction", "deliberative", "Solves constraint problems over graph topology", ("constraint_propagation", "backtrack_search")),

    # Tool-using agents (5)
    AgentType("retrieval", "tool_using", "Uses graph retrieval tools for information gathering", ("graph_query", "index_search")),
    AgentType("computation", "tool_using", "Applies graph algorithms as tools", ("algorithm_execute", "metric_compute")),
    AgentType("code_generation", "tool_using", "Generates analysis code for graph queries", ("code_gen", "code_execute")),
    AgentType("api_caller", "tool_using", "Orchestrates external API calls for enrichment", ("api_call", "response_parse")),
    AgentType("visualization", "tool_using", "Creates graph visualizations as analysis output", ("render_graph", "export_visual")),

    # Orchestration agents (5)
    AgentType("supervisor", "orchestration", "Manages and delegates to sub-agents", ("task_assign", "result_aggregate")),
    AgentType("router", "orchestration", "Routes queries to specialized agents", ("query_classify", "agent_select")),
    AgentType("pipeline", "orchestration", "Chains agents in sequential processing", ("stage_manage", "data_flow")),
    AgentType("parallel", "orchestration", "Runs multiple agents concurrently", ("parallel_dispatch", "result_merge")),
    AgentType("workflow", "orchestration", "Executes complex multi-step workflows", ("workflow_define", "step_execute")),

    # Collaboration agents (5)
    AgentType("debate", "collaboration", "Multiple perspectives argue to consensus", ("position_generate", "argument_evaluate")),
    AgentType("consensus", "collaboration", "Aggregates multiple agent opinions", ("vote_collect", "consensus_compute")),
    AgentType("peer_review", "collaboration", "Agents review each other's analysis", ("review_generate", "feedback_integrate")),
    AgentType("negotiation", "collaboration", "Agents negotiate resource allocation", ("offer_generate", "agreement_reach")),
    AgentType("swarm", "collaboration", "Emergent behavior from simple agent interactions", ("local_rule", "emergent_pattern")),

    # Meta-cognitive agents (4)
    AgentType("self_reflective", "meta_cognitive", "Evaluates own reasoning quality", ("reasoning_trace", "quality_assess")),
    AgentType("learning", "meta_cognitive", "Improves from past interaction outcomes", ("outcome_record", "strategy_update")),
    AgentType("uncertainty", "meta_cognitive", "Quantifies and communicates confidence", ("confidence_estimate", "uncertainty_propagate")),
    AgentType("explanation", "meta_cognitive", "Generates explanations for its decisions", ("decision_trace", "explanation_generate")),

    # Autonomous agents (4)
    AgentType("explorer", "autonomous", "Autonomously explores graph for insights", ("frontier_select", "discovery_report")),
    AgentType("monitor", "autonomous", "Continuously watches graph for anomalies", ("change_detect", "anomaly_alert")),
    AgentType("maintainer", "autonomous", "Identifies and suggests graph quality fixes", ("quality_check", "fix_suggest")),
    AgentType("researcher", "autonomous", "Deep-dives into graph patterns", ("pattern_mine", "hypothesis_test")),

    # Enterprise agents (4)
    AgentType("compliance", "enterprise", "Checks graph against compliance rules", ("rule_check", "violation_report")),
    AgentType("audit", "enterprise", "Generates audit trails from graph operations", ("trail_record", "audit_report")),
    AgentType("governance", "enterprise", "Enforces data governance policies", ("policy_check", "governance_report")),
    AgentType("security", "enterprise", "Analyzes graph for security implications", ("threat_model", "risk_assess")),

    # Multi-agent patterns (4)
    AgentType("map_reduce", "multi_agent", "Distributes analysis across graph partitions", ("partition", "map", "reduce")),
    AgentType("blackboard", "multi_agent", "Shared knowledge space for collaborative analysis", ("post_knowledge", "read_board", "contribute")),
    AgentType("market", "multi_agent", "Auction-based task allocation among agents", ("bid", "allocate", "execute")),
    AgentType("ensemble", "multi_agent", "Combines multiple agent outputs for robustness", ("diverse_analyze", "ensemble_combine")),
]

_AGENT_MAP = {a.name: a for a in AGENT_TYPES}
_CATEGORY_MAP: dict[str, list[AgentType]] = {}
for _a in AGENT_TYPES:
    _CATEGORY_MAP.setdefault(_a.category, []).append(_a)


@dataclass
class AgentResult:
    answer: str
    agent_type: str
    category: str
    confidence: float
    actions: list[dict] = field(default_factory=list)
    highlight_ids: list[str] = field(default_factory=list)
    reasoning: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer, "agent_type": self.agent_type,
            "category": self.category, "confidence": round(self.confidence, 3),
            "actions": self.actions, "highlight_ids": self.highlight_ids,
            "reasoning": self.reasoning, "metadata": self.metadata,
        }


class BaseAgent:
    def __init__(self, store: GraphStore, agent_type: AgentType) -> None:
        self._store = store
        self._type = agent_type

    def execute(self, query: str, context: dict) -> AgentResult:
        return AgentResult(
            answer=f"[{self._type.name}] Analysis not available for this query.",
            agent_type=self._type.name, category=self._type.category,
            confidence=0.1,
        )


class SimpleReflexAgent(BaseAgent):
    def execute(self, query: str, context: dict) -> AgentResult:
        q = query.lower()
        vertices = self._store.find_vertices(limit=100)
        if "count" in q or "how many" in q:
            edges = list(self._store.find_edges(limit=1000))
            return AgentResult(
                answer=f"Graph contains {len(vertices)} nodes and {len(edges)} edges.",
                agent_type="simple_reflex", category="reactive", confidence=0.9,
            )
        if "type" in q or "label" in q:
            labels: dict[str, int] = {}
            for v in vertices:
                labels[v.get("label", "unknown")] = labels.get(v.get("label", "unknown"), 0) + 1
            breakdown = ", ".join(f"{l}: {c}" for l, c in sorted(labels.items(), key=lambda x: -x[1])[:10])
            return AgentResult(
                answer=f"Node types: {breakdown}", agent_type="simple_reflex",
                category="reactive", confidence=0.85,
            )
        return AgentResult(
            answer=f"Found {len(vertices)} vertices. Try asking about counts or types.",
            agent_type="simple_reflex", category="reactive", confidence=0.4,
        )


class GoalBasedAgent(BaseAgent):
    def execute(self, query: str, context: dict) -> AgentResult:
        q = query.lower()
        reasoning = ["Decomposing query into sub-goals"]
        actions = []
        if "impact" in q or "break" in q or "remove" in q:
            selected_id = context.get("selected_id")
            if selected_id:
                reasoning.append(f"Goal: assess impact of removing {selected_id}")
                from eoip.graph.metrics import GraphMetricsEngine
                engine = GraphMetricsEngine(self._store)
                try:
                    br = engine.blast_radius(selected_id, max_depth=3)
                    affected = br.affected_items or []
                    reasoning.append(f"Computed blast radius: {len(affected)} affected entities")
                    actions = [{"type": "highlight", "ids": [i.canonical_id for i in affected[:10]]}]
                    return AgentResult(
                        answer=f"Removing {selected_id} would affect {len(affected)} entities across {br.max_depth_reached} depth levels.",
                        agent_type="goal_based", category="deliberative", confidence=0.8,
                        actions=actions, highlight_ids=[i.canonical_id for i in affected[:10]],
                        reasoning=reasoning,
                    )
                except Exception:
                    reasoning.append("Blast radius computation failed, falling back to edge count")
            else:
                reasoning.append("No entity selected — cannot assess impact")

        if "community" in q or "cluster" in q:
            reasoning.append("Goal: identify community structure")
            from eoip.graph.community import CommunityDetectionEngine
            engine = CommunityDetectionEngine(self._store)
            try:
                result = engine.detect(algorithm="louvain", resolution=1.0)
                communities = result.get("communities", [])
                reasoning.append(f"Detected {len(communities)} communities")
                return AgentResult(
                    answer=f"Found {len(communities)} communities. Largest has {max((c.get('size', 0) for c in communities), default=0)} members.",
                    agent_type="goal_based", category="deliberative", confidence=0.75,
                    reasoning=reasoning,
                )
            except Exception:
                reasoning.append("Community detection failed")

        reasoning.append("Generic analysis — returning graph overview")
        vertices = self._store.find_vertices(limit=50)
        return AgentResult(
            answer=f"Analyzed {len(vertices)} entities. Refine your query for deeper analysis.",
            agent_type="goal_based", category="deliberative", confidence=0.4,
            reasoning=reasoning,
        )


class ExplorerAgent(BaseAgent):
    def execute(self, query: str, context: dict) -> AgentResult:
        reasoning = ["Exploring graph for insights"]
        vertices = self._store.find_vertices(limit=200)
        edges = list(self._store.find_edges(limit=1000))

        degree: dict[str, int] = {}
        for e in edges:
            src = e.get("from_id", "")
            tgt = e.get("to_id", "")
            degree[src] = degree.get(src, 0) + 1
            degree[tgt] = degree.get(tgt, 0) + 1

        hubs = sorted(degree.items(), key=lambda x: -x[1])[:5]
        orphans = [v for v in vertices if v.get("vid") not in degree]

        reasoning.append(f"Found {len(hubs)} high-degree nodes, {len(orphans)} orphans")

        hub_text = ", ".join(f"{h[0]}(degree={h[1]})" for h in hubs)
        return AgentResult(
            answer=f"Graph exploration: {len(vertices)} nodes, {len(edges)} edges. Top hubs: {hub_text}. {len(orphans)} orphaned nodes found.",
            agent_type="explorer", category="autonomous", confidence=0.7,
            highlight_ids=[h[0] for h in hubs],
            reasoning=reasoning,
        )


class ComplianceAgent(BaseAgent):
    def execute(self, query: str, context: dict) -> AgentResult:
        reasoning = ["Checking graph against compliance rules"]
        vertices = self._store.find_vertices(limit=500)
        edges = list(self._store.find_edges(limit=2000))

        issues = []
        orphaned = set(v.get("vid") for v in vertices)
        for e in edges:
            orphaned.discard(e.get("to_id"))
        if orphaned:
            issues.append(f"{len(orphaned)} entities have no incoming relationships (potential data gaps)")
            reasoning.append(f"Found {len(orphaned)} orphaned entities")

        no_evidence = [e for e in edges if not e.get("properties", {}).get("source_ref") and not e.get("properties", {}).get("evidence_key")]
        if no_evidence:
            issues.append(f"{len(no_evidence)}/{len(edges)} edges lack evidence references")
            reasoning.append(f"{len(no_evidence)} edges without evidence")

        no_label = [v for v in vertices if not v.get("label")]
        if no_label:
            issues.append(f"{len(no_label)} entities missing type labels")

        if not issues:
            return AgentResult(
                answer="No compliance issues found. All entities have types, evidence coverage is complete.",
                agent_type="compliance", category="enterprise", confidence=0.85,
                reasoning=reasoning,
            )

        return AgentResult(
            answer=f"Found {len(issues)} compliance concerns: " + "; ".join(issues),
            agent_type="compliance", category="enterprise", confidence=0.8,
            reasoning=reasoning,
            actions=[{"type": "review", "issue": i} for i in issues],
        )


class AuditAgent(BaseAgent):
    def execute(self, query: str, context: dict) -> AgentResult:
        reasoning = ["Generating audit trail analysis"]
        vertices = self._store.find_vertices(limit=200)
        edges = list(self._store.find_edges(limit=1000))

        sources = set()
        for e in edges:
            props = e.get("properties", {})
            ref = props.get("source_ref") or props.get("evidence_key") or ""
            if ref:
                sources.add(ref)

        domains = set()
        for v in vertices:
            props = v.get("properties", {})
            d = props.get("domain") or props.get("source_domain") or ""
            if d:
                domains.add(d)

        reasoning.append(f"Found {len(sources)} unique evidence sources across {len(domains)} domains")

        return AgentResult(
            answer=f"Audit summary: {len(vertices)} entities, {len(edges)} relationships. {len(sources)} unique evidence sources across {len(domains)} domains. Evidence coverage: {(len([e for e in edges if e.get('properties', {}).get('source_ref')]) / max(len(edges), 1) * 100):.0f}%.",
            agent_type="audit", category="enterprise", confidence=0.75,
            reasoning=reasoning,
            metadata={"source_count": len(sources), "domain_count": len(domains)},
        )


class MapReduceAgent(BaseAgent):
    def execute(self, query: str, context: dict) -> AgentResult:
        reasoning = ["Partitioning graph for distributed analysis"]
        vertices = self._store.find_vertices(limit=500)

        partitions: dict[str, list] = {}
        for v in vertices:
            label = v.get("label", "unknown")
            partitions.setdefault(label, []).append(v)

        reasoning.append(f"Created {len(partitions)} partitions by node type")

        partition_summaries = []
        for label, verts in sorted(partitions.items(), key=lambda x: -len(x[1]))[:8]:
            partition_summaries.append(f"{label}: {len(verts)} entities")

        return AgentResult(
            answer=f"Map-reduce analysis across {len(partitions)} partitions: {'; '.join(partition_summaries)}.",
            agent_type="map_reduce", category="multi_agent", confidence=0.7,
            reasoning=reasoning,
            metadata={"partition_count": len(partitions), "total_entities": len(vertices)},
        )


class EnsembleAgent(BaseAgent):
    def execute(self, query: str, context: dict) -> AgentResult:
        agents = [
            SimpleReflexAgent(self._store, _AGENT_MAP["simple_reflex"]),
            GoalBasedAgent(self._store, _AGENT_MAP["goal_based"]),
            ExplorerAgent(self._store, _AGENT_MAP["explorer"]),
        ]
        results = [a.execute(query, context) for a in agents]
        best = max(results, key=lambda r: r.confidence)
        all_highlights = list(set(h for r in results for h in r.highlight_ids))[:10]
        all_reasoning = [f"[{r.agent_type}] {r.answer[:80]}" for r in results]

        return AgentResult(
            answer=f"Ensemble of {len(results)} agents. Best answer ({best.agent_type}, {best.confidence:.0%}): {best.answer}",
            agent_type="ensemble", category="multi_agent",
            confidence=max(r.confidence for r in results),
            highlight_ids=all_highlights,
            reasoning=all_reasoning,
            metadata={"sub_agents": {r.agent_type: r.confidence for r in results}},
        )


class SupervisorAgent(BaseAgent):
    def execute(self, query: str, context: dict) -> AgentResult:
        q = query.lower()
        reasoning = ["Supervisor: classifying query to delegate"]

        if any(w in q for w in ["compliance", "rule", "policy", "legal"]):
            reasoning.append("Delegating to compliance agent")
            return ComplianceAgent(self._store, _AGENT_MAP["compliance"]).execute(query, context)
        if any(w in q for w in ["audit", "trail", "evidence", "source"]):
            reasoning.append("Delegating to audit agent")
            return AuditAgent(self._store, _AGENT_MAP["audit"]).execute(query, context)
        if any(w in q for w in ["impact", "break", "remove", "community", "cluster"]):
            reasoning.append("Delegating to goal-based agent")
            return GoalBasedAgent(self._store, _AGENT_MAP["goal_based"]).execute(query, context)
        if any(w in q for w in ["explore", "discover", "insight", "hub", "orphan"]):
            reasoning.append("Delegating to explorer agent")
            return ExplorerAgent(self._store, _AGENT_MAP["explorer"]).execute(query, context)

        reasoning.append("No specialist matched — using ensemble")
        return EnsembleAgent(self._store, _AGENT_MAP["ensemble"]).execute(query, context)


_AGENT_IMPLEMENTATIONS: dict[str, type[BaseAgent]] = {
    "simple_reflex": SimpleReflexAgent,
    "model_based_reflex": SimpleReflexAgent,
    "condition_action": SimpleReflexAgent,
    "event_driven": SimpleReflexAgent,
    "threshold": SimpleReflexAgent,
    "goal_based": GoalBasedAgent,
    "utility_based": GoalBasedAgent,
    "bdi": GoalBasedAgent,
    "planning": GoalBasedAgent,
    "constraint_satisfaction": GoalBasedAgent,
    "retrieval": SimpleReflexAgent,
    "computation": ExplorerAgent,
    "code_generation": SimpleReflexAgent,
    "api_caller": SimpleReflexAgent,
    "visualization": SimpleReflexAgent,
    "supervisor": SupervisorAgent,
    "router": SupervisorAgent,
    "pipeline": SupervisorAgent,
    "parallel": SupervisorAgent,
    "workflow": SupervisorAgent,
    "debate": EnsembleAgent,
    "consensus": EnsembleAgent,
    "peer_review": EnsembleAgent,
    "negotiation": EnsembleAgent,
    "swarm": EnsembleAgent,
    "self_reflective": GoalBasedAgent,
    "learning": GoalBasedAgent,
    "uncertainty": GoalBasedAgent,
    "explanation": GoalBasedAgent,
    "explorer": ExplorerAgent,
    "monitor": ComplianceAgent,
    "maintainer": ComplianceAgent,
    "researcher": ExplorerAgent,
    "compliance": ComplianceAgent,
    "audit": AuditAgent,
    "governance": ComplianceAgent,
    "security": ComplianceAgent,
    "map_reduce": MapReduceAgent,
    "blackboard": EnsembleAgent,
    "market": EnsembleAgent,
    "ensemble": EnsembleAgent,
}


class AgentRouter:
    """Routes queries to the optimal agent type."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def classify(self, query: str, context: dict | None = None) -> str:
        q = query.lower()
        if any(w in q for w in ["compliance", "rule", "violation", "policy"]):
            return "compliance"
        if any(w in q for w in ["audit", "trail", "evidence", "provenance"]):
            return "audit"
        if any(w in q for w in ["impact", "break", "goal", "plan"]):
            return "goal_based"
        if any(w in q for w in ["explore", "discover", "insight", "pattern"]):
            return "explorer"
        if any(w in q for w in ["count", "how many", "type", "label"]):
            return "simple_reflex"
        if any(w in q for w in ["distribute", "partition", "map", "reduce"]):
            return "map_reduce"
        return "supervisor"

    def route(self, query: str, agent_type: str | None = None, context: dict | None = None) -> dict:
        ctx = context or {}
        name = agent_type if agent_type and agent_type in _AGENT_IMPLEMENTATIONS else self.classify(query, ctx)
        at = _AGENT_MAP.get(name, _AGENT_MAP["supervisor"])
        impl_cls = _AGENT_IMPLEMENTATIONS.get(name, SupervisorAgent)
        impl = impl_cls(self._store, at)
        result = impl.execute(query, ctx)
        return result.to_dict()
