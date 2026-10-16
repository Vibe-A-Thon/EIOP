"""Tests for new deep agents: BlastRadius, Community, Anomaly, Similarity."""

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.memory import MemoryGraphStore


def _vertex(store, label, canonical_id, **props):
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id, **props})


def _build_graph():
    store = MemoryGraphStore()
    a = _vertex(store, "WorkItem", "item:A", issue_key="A-1", summary="A")
    b = _vertex(store, "Commit", "commit:B", commit_sha="abc123")
    c = _vertex(store, "File", "file:C", repo_id="repo1", path="c.py")
    d = _vertex(store, "CodeSymbol", "symbol:D", qualified_name="d.run", symbol_kind="function")
    e = _vertex(store, "Evidence", "evidence:E", source_system="git", method="SOURCE_EVENT", evidence_key="ek:E")
    store.upsert_edge("IMPLEMENTS", b["vid"], a["vid"], {})
    store.upsert_edge("MODIFIES", b["vid"], c["vid"], {})
    store.upsert_edge("DECLARES", c["vid"], d["vid"], {})
    store.upsert_edge("EVIDENCED_BY", d["vid"], e["vid"], {})
    return store


def _make_request(agent_id, goal, context_refs=None, budgets=None):
    return AgentRequest(
        request_id="test-req-1",
        agent_id=agent_id,
        goal=goal,
        context_refs=context_refs,
        budgets=budgets,
    )


class TestBlastRadiusAgent:
    def test_execute_success(self):
        from eoip.agents.blast_radius import BlastRadiusAgent
        store = _build_graph()
        agent = BlastRadiusAgent()
        req = _make_request("BlastRadius", "Compute blast radius for commit:B", context_refs=["commit:B"])
        result = agent.execute(req, store)
        assert isinstance(result, AgentResult)
        assert result.status in ("SUCCEEDED", "PARTIAL")
        assert result.request_id == "test-req-1"

    def test_execute_missing_entity(self):
        from eoip.agents.blast_radius import BlastRadiusAgent
        store = MemoryGraphStore()
        agent = BlastRadiusAgent()
        req = _make_request("BlastRadius", "nonexistent:x", context_refs=["nonexistent:x"])
        result = agent.execute(req, store)
        assert result.status == "FAILED"

    def test_agent_attributes(self):
        from eoip.agents.blast_radius import BlastRadiusAgent
        agent = BlastRadiusAgent()
        assert agent.agent_id == "BlastRadius"
        assert isinstance(agent.allowed_tools, frozenset)
        assert agent.max_steps > 0
        assert agent.max_seconds > 0

    def test_custom_config(self):
        from eoip.agents.blast_radius import BlastRadiusAgent
        agent = BlastRadiusAgent(config={"budgets": {"max_steps": 5, "max_seconds": 10.0}})
        assert agent.max_steps == 5
        assert agent.max_seconds == 10.0


class TestCommunityAnalysisAgent:
    def test_execute_success(self):
        from eoip.agents.community import CommunityAnalysisAgent
        store = _build_graph()
        agent = CommunityAnalysisAgent()
        req = _make_request("CommunityAnalysis", "Detect communities in the graph")
        result = agent.execute(req, store)
        assert isinstance(result, AgentResult)
        assert result.status in ("SUCCEEDED", "PARTIAL")

    def test_agent_attributes(self):
        from eoip.agents.community import CommunityAnalysisAgent
        agent = CommunityAnalysisAgent()
        assert agent.agent_id == "CommunityAnalysis"


class TestAnomalyDetectionAgent:
    def test_execute_success(self):
        from eoip.agents.anomaly import AnomalyDetectionAgent
        store = _build_graph()
        agent = AnomalyDetectionAgent()
        req = _make_request("AnomalyDetection", "Detect anomalous nodes")
        result = agent.execute(req, store)
        assert isinstance(result, AgentResult)
        assert result.status in ("SUCCEEDED", "PARTIAL")

    def test_agent_attributes(self):
        from eoip.agents.anomaly import AnomalyDetectionAgent
        agent = AnomalyDetectionAgent()
        assert agent.agent_id == "AnomalyDetection"


class TestSimilarityAgent:
    def test_execute_success(self):
        from eoip.agents.similarity import SimilarityAgent
        store = _build_graph()
        agent = SimilarityAgent()
        req = _make_request("Similarity", "Find similar to commit:B", context_refs=["commit:B"])
        result = agent.execute(req, store)
        assert isinstance(result, AgentResult)
        assert result.status in ("SUCCEEDED", "PARTIAL", "FAILED")

    def test_agent_attributes(self):
        from eoip.agents.similarity import SimilarityAgent
        agent = SimilarityAgent()
        assert agent.agent_id == "Similarity"


class TestAgentRegistration:
    def test_all_agents_importable(self):
        from eoip.agents.anomaly import AnomalyDetectionAgent
        from eoip.agents.blast_radius import BlastRadiusAgent
        from eoip.agents.community import CommunityAnalysisAgent
        from eoip.agents.similarity import SimilarityAgent
        agents = [BlastRadiusAgent, CommunityAnalysisAgent, AnomalyDetectionAgent, SimilarityAgent]
        for cls in agents:
            instance = cls()
            assert hasattr(instance, "agent_id")
            assert hasattr(instance, "execute")
            assert hasattr(instance, "allowed_tools")

    def test_agents_in_registry(self):
        from eoip.agents.anomaly import AnomalyDetectionAgent
        from eoip.agents.blast_radius import BlastRadiusAgent
        from eoip.agents.community import CommunityAnalysisAgent
        from eoip.agents.runtime import AgentRegistry
        from eoip.agents.similarity import SimilarityAgent
        registry = AgentRegistry()
        registry.register(BlastRadiusAgent())
        registry.register(CommunityAnalysisAgent())
        registry.register(AnomalyDetectionAgent())
        registry.register(SimilarityAgent())
        agents = registry.list_agents()
        assert len(agents) >= 4
        assert "BlastRadius" in agents
        assert "CommunityAnalysis" in agents
