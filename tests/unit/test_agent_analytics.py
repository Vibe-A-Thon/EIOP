"""Tests for GraphAnalyticsAgent and SemanticIndexAgent."""

from eoip.agents.graph_analytics import ALGORITHM_REGISTRY, GraphAnalyticsAgent
from eoip.agents.semantic_index import SemanticIndexAgent
from eoip.contracts.agent import AgentRequest
from eoip.graph.memory import MemoryGraphStore


def _vertex(store, label, canonical_id, **props):
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id, **props})


def _build_store():
    store = MemoryGraphStore()
    a = _vertex(store, "WorkItem", "item:A", issue_key="A-1")
    b = _vertex(store, "WorkItem", "item:B", issue_key="B-1")
    c = _vertex(store, "Commit", "commit:C", commit_sha="abc123")
    d = _vertex(store, "File", "file:D", repo_id="repo1", path="d.py")
    e = _vertex(store, "File", "file:E", repo_id="repo1", path="e.py")
    f = _vertex(store, "CodeSymbol", "symbol:F", qualified_name="f.run", symbol_kind="function")
    store.upsert_edge("IMPLEMENTS", c["vid"], a["vid"], {})
    store.upsert_edge("IMPLEMENTS", c["vid"], b["vid"], {})
    store.upsert_edge("MODIFIES", c["vid"], d["vid"], {})
    store.upsert_edge("MODIFIES", c["vid"], e["vid"], {})
    store.upsert_edge("DECLARES", d["vid"], f["vid"], {})
    store.upsert_edge("DECLARES", e["vid"], f["vid"], {})
    return store


# --- GraphAnalyticsAgent ---

def test_analytics_agent_single_algorithm():
    store = _build_store()
    agent = GraphAnalyticsAgent()
    request = AgentRequest(
        request_id="test-1",
        agent_id="GraphAnalytics",
        goal="ring_detection",
        context_refs=["item:A"],
    )
    result = agent.execute(request, store)
    assert result.status in ("SUCCEEDED", "PARTIAL")
    assert result.request_id == "test-1"


def test_analytics_agent_unknown_algorithm():
    store = _build_store()
    agent = GraphAnalyticsAgent()
    request = AgentRequest(
        request_id="test-unknown",
        agent_id="GraphAnalytics",
        goal="nonexistent_algorithm",
    )
    result = agent.execute(request, store)
    assert result.status == "FAILED"
    assert "Unknown algorithm" in result.summary


def test_analytics_agent_swarm():
    store = _build_store()
    agent = GraphAnalyticsAgent()
    request = AgentRequest(
        request_id="test-swarm",
        agent_id="GraphAnalytics",
        goal="swarm",
        context_refs=["commit:C"],
    )
    result = agent.execute(request, store)
    assert result.status in ("SUCCEEDED", "PARTIAL")
    assert result.data is not None
    assert "results" in result.data


def test_analytics_agent_swarm_no_cid():
    store = _build_store()
    agent = GraphAnalyticsAgent()
    request = AgentRequest(
        request_id="test-swarm-base",
        agent_id="GraphAnalytics",
        goal="all",
    )
    result = agent.execute(request, store)
    assert result.status in ("SUCCEEDED", "PARTIAL")


def test_analytics_agent_k_step():
    store = _build_store()
    agent = GraphAnalyticsAgent()
    request = AgentRequest(
        request_id="test-kstep",
        agent_id="GraphAnalytics",
        goal="k_step_neighbors",
        context_refs=["commit:C"],
    )
    result = agent.execute(request, store)
    assert result.status == "SUCCEEDED"


def test_analytics_agent_pagerank():
    store = _build_store()
    agent = GraphAnalyticsAgent()
    request = AgentRequest(
        request_id="test-pr",
        agent_id="GraphAnalytics",
        goal="pagerank",
        context_refs=["commit:C"],
    )
    result = agent.execute(request, store)
    assert result.status == "SUCCEEDED"


def test_analytics_agent_explanation():
    store = _build_store()
    agent = GraphAnalyticsAgent()
    request = AgentRequest(
        request_id="test-explain",
        agent_id="GraphAnalytics",
        goal="ring_detection",
    )
    result = agent.execute(request, store)
    assert result.explanation is not None
    assert result.explanation.decision_summary


def test_analytics_agent_custom_budgets():
    agent = GraphAnalyticsAgent(config={"budgets": {"max_steps": 5, "max_seconds": 30.0}})
    assert agent.max_steps == 5
    assert agent.max_seconds == 30.0


def test_algorithm_registry_completeness():
    assert len(ALGORITHM_REGISTRY) >= 28


# --- SemanticIndexAgent ---

def test_semantic_agent_full_pipeline():
    store = _build_store()
    agent = SemanticIndexAgent()
    request = AgentRequest(
        request_id="test-sem-1",
        agent_id="SemanticIndex",
        goal="full",
    )
    result = agent.execute(request, store)
    assert result.status in ("SUCCEEDED", "PARTIAL")
    assert result.data is not None
    assert "stages" in result.data


def test_semantic_agent_specific_stages():
    store = _build_store()
    agent = SemanticIndexAgent()
    request = AgentRequest(
        request_id="test-sem-stages",
        agent_id="SemanticIndex",
        goal="domain:WORK",
        context_refs=["search_index", "analytics"],
    )
    result = agent.execute(request, store)
    assert result.status in ("SUCCEEDED", "PARTIAL")
    stage_names = [s["stage"] for s in result.data["stages"]]
    assert "search_index" in stage_names
    assert "analytics" in stage_names


def test_semantic_agent_explanation():
    store = _build_store()
    agent = SemanticIndexAgent()
    request = AgentRequest(
        request_id="test-sem-explain",
        agent_id="SemanticIndex",
        goal="full",
    )
    result = agent.execute(request, store)
    assert result.explanation is not None
    assert result.explanation.decision_summary


def test_semantic_agent_custom_budgets():
    agent = SemanticIndexAgent(config={"budgets": {"max_steps": 10, "max_seconds": 60.0}})
    assert agent.max_steps == 10
    assert agent.max_seconds == 60.0


def test_semantic_agent_invalid_stages_fallback():
    store = _build_store()
    agent = SemanticIndexAgent()
    request = AgentRequest(
        request_id="test-sem-invalid",
        agent_id="SemanticIndex",
        goal="full",
        context_refs=["not_a_real_stage"],
    )
    result = agent.execute(request, store)
    assert result.status in ("SUCCEEDED", "PARTIAL")
    assert len(result.data["stages"]) == 6
