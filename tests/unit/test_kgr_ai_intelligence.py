"""Phase 13 — AI-Assisted Graph Intelligence: tests for RAG, Agents, Engineering."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from packages.eoip.graph.store import MemoryGraphStore
from packages.eoip.graph.rag_router import RAGRouter, RAG_PATTERNS, RAGPattern, RAGResult
from packages.eoip.graph.agent_router import AgentRouter, AGENT_TYPES, AgentType, AgentResult
from packages.eoip.graph.engineering import EngineeringRouter, ENGINEERING_DISCIPLINES, EngineeringDiscipline, EngineeringResult


def _make_store():
    """Create a store with test graph data."""
    store = MemoryGraphStore()
    nodes = [
        ("v1", "Module", {"canonical_id": "v1", "name": "auth_module", "domain": "security"}),
        ("v2", "Module", {"canonical_id": "v2", "name": "api_gateway", "domain": "infra"}),
        ("v3", "Service", {"canonical_id": "v3", "name": "user_service", "domain": "core"}),
        ("v4", "Database", {"canonical_id": "v4", "name": "postgres_main", "domain": "data"}),
        ("v5", "Config", {"canonical_id": "v5", "name": "env_config", "domain": "infra"}),
        ("v6", "Test", {"canonical_id": "v6", "name": "test_auth", "domain": "testing"}),
        ("v7", "Module", {"canonical_id": "v7", "name": "logger", "domain": "infra"}),
        ("v8", "Service", {"canonical_id": "v8", "name": "notification_service", "domain": "core"}),
    ]
    for vid, label, props in nodes:
        store.add_vertex(vid, label, props)
    edges = [
        ("v1", "DEPENDS_ON", "v2", {"source_ref": "code_scan_1"}),
        ("v2", "CONNECTS_TO", "v3", {"source_ref": "arch_doc"}),
        ("v3", "READS_FROM", "v4", {"source_ref": "schema_def"}),
        ("v1", "TESTED_BY", "v6", {}),
        ("v5", "CONFIGURES", "v2", {"evidence_key": "config_audit"}),
        ("v3", "USES", "v7", {}),
        ("v8", "DEPENDS_ON", "v3", {"source_ref": "service_map"}),
        ("v7", "WRITES_TO", "v4", {}),
    ]
    for src, label, tgt, props in edges:
        store.add_edge(src, label, tgt, props)
    return store


# ===== RAG Router Tests (Phase 13.1) =====

def test_rag_patterns_count():
    """Should have exactly 17 RAG patterns."""
    assert len(RAG_PATTERNS) == 17


def test_rag_patterns_unique_names():
    """All RAG pattern names should be unique."""
    names = [p.name for p in RAG_PATTERNS]
    assert len(names) == len(set(names))


def test_rag_pattern_dataclass():
    """RAGPattern should serialize to dict."""
    p = RAG_PATTERNS[0]
    d = p.to_dict()
    assert "name" in d
    assert "description" in d
    assert "retrieval_strategy" in d
    assert "when_to_use" in d


def test_rag_router_classify_simple():
    """Short queries should classify as simple."""
    store = _make_store()
    router = RAGRouter(store)
    assert router.classify("find auth") == "simple"


def test_rag_router_classify_graph():
    """Community-related queries should classify as graph."""
    store = _make_store()
    router = RAGRouter(store)
    assert router.classify("show me the community overview of this graph") == "graph"


def test_rag_router_classify_multihop():
    """Impact queries with selected_id should classify as multihop."""
    store = _make_store()
    router = RAGRouter(store)
    assert router.classify("what would break if removed", {"selected_id": "v1"}) == "multihop"


def test_rag_router_classify_multistep():
    """Multi-question queries should classify as multistep."""
    store = _make_store()
    router = RAGRouter(store)
    assert router.classify("what is v1? what connects to v2?") == "multistep"


def test_rag_router_route_simple():
    """Routing a simple query should return results with rag_pattern."""
    store = _make_store()
    router = RAGRouter(store)
    result = router.route("find auth module")
    assert "rag_pattern" in result
    assert "answer" in result
    assert "confidence" in result
    assert isinstance(result["confidence"], float)


def test_rag_router_route_with_explicit_pattern():
    """Explicit pattern should override classification."""
    store = _make_store()
    router = RAGRouter(store)
    result = router.route("anything", pattern="graph")
    assert result["rag_pattern"] in ("graph", "simple")


def test_rag_router_route_hybrid():
    """Hybrid RAG should merge keyword and community results."""
    store = _make_store()
    router = RAGRouter(store)
    result = router.route("surprising auth gateway connections", pattern="hybrid")
    assert "answer" in result


def test_rag_result_to_dict():
    """RAGResult should serialize correctly."""
    r = RAGResult(answer="test", pattern="simple", confidence=0.75,
                  sources=["v1"], highlight_ids=["v1"])
    d = r.to_dict()
    assert d["rag_pattern"] == "simple"
    assert d["confidence"] == 0.75
    assert d["sources"] == ["v1"]


# ===== Agent Router Tests (Phase 13.2) =====

def test_agent_types_count():
    """Should have 41 agent types across 9 categories."""
    assert len(AGENT_TYPES) == 41


def test_agent_types_nine_categories():
    """Should have exactly 9 categories."""
    categories = set(a.category for a in AGENT_TYPES)
    assert len(categories) == 9
    expected = {"reactive", "deliberative", "tool_using", "orchestration",
                "collaboration", "meta_cognitive", "autonomous", "enterprise", "multi_agent"}
    assert categories == expected


def test_agent_types_unique_names():
    """All agent type names should be unique."""
    names = [a.name for a in AGENT_TYPES]
    assert len(names) == len(set(names))


def test_agent_type_dataclass():
    """AgentType should serialize to dict."""
    a = AGENT_TYPES[0]
    d = a.to_dict()
    assert "name" in d
    assert "category" in d
    assert "capabilities" in d
    assert isinstance(d["capabilities"], list)


def test_agent_router_classify_compliance():
    """Compliance-related queries should route to compliance agent."""
    store = _make_store()
    router = AgentRouter(store)
    assert router.classify("check compliance rules") == "compliance"


def test_agent_router_classify_audit():
    """Audit-related queries should route to audit agent."""
    store = _make_store()
    router = AgentRouter(store)
    assert router.classify("generate audit trail") == "audit"


def test_agent_router_classify_explorer():
    """Discovery queries should route to explorer agent."""
    store = _make_store()
    router = AgentRouter(store)
    assert router.classify("explore and discover patterns") == "explorer"


def test_agent_router_route_simple_reflex():
    """Simple reflex agent should answer count queries."""
    store = _make_store()
    router = AgentRouter(store)
    result = router.route("how many nodes", agent_type="simple_reflex")
    assert "answer" in result
    assert "agent_type" in result
    assert result["agent_type"] == "simple_reflex"
    assert "8" in result["answer"] or "nodes" in result["answer"].lower()


def test_agent_router_route_compliance():
    """Compliance agent should find issues."""
    store = _make_store()
    router = AgentRouter(store)
    result = router.route("check compliance", agent_type="compliance")
    assert "answer" in result
    assert result["category"] == "enterprise"


def test_agent_router_route_ensemble():
    """Ensemble agent should combine multiple sub-agents."""
    store = _make_store()
    router = AgentRouter(store)
    result = router.route("analyze everything", agent_type="ensemble")
    assert result["agent_type"] == "ensemble"
    assert "metadata" in result
    assert "sub_agents" in result.get("metadata", {})


def test_agent_result_to_dict():
    """AgentResult should serialize correctly."""
    r = AgentResult(answer="test", agent_type="explorer", category="autonomous",
                    confidence=0.8, reasoning=["step1"])
    d = r.to_dict()
    assert d["agent_type"] == "explorer"
    assert d["confidence"] == 0.8
    assert d["reasoning"] == ["step1"]


# ===== Engineering Router Tests (Phase 13.3) =====

def test_engineering_disciplines_count():
    """Should have exactly 8 engineering disciplines."""
    assert len(ENGINEERING_DISCIPLINES) == 8


def test_engineering_disciplines_unique_names():
    """All discipline names should be unique."""
    names = [d.name for d in ENGINEERING_DISCIPLINES]
    assert len(names) == len(set(names))


def test_engineering_discipline_dataclass():
    """EngineeringDiscipline should serialize to dict."""
    d = ENGINEERING_DISCIPLINES[0]
    dd = d.to_dict()
    assert "name" in dd
    assert "pattern" in dd
    assert "use_cases" in dd
    assert isinstance(dd["use_cases"], list)


def test_engineering_router_loop():
    """Loop discipline should iterate and converge."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("loop", "analyze convergence")
    assert result["discipline"] == "loop"
    assert "iterations" in result.get("metrics", {})
    assert len(result.get("steps", [])) > 0


def test_engineering_router_graph():
    """Graph discipline should analyze topology."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("graph", "topology analysis")
    assert result["discipline"] == "graph"
    assert "components" in result.get("metrics", {})
    assert "density" in result.get("metrics", {})


def test_engineering_router_harness():
    """Harness discipline should execute pipeline stages."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("harness", "run pipeline")
    assert result["discipline"] == "harness"
    assert result.get("metrics", {}).get("stages_executed", 0) >= 4


def test_engineering_router_memory():
    """Memory discipline should analyze state patterns."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("memory", "state analysis")
    assert result["discipline"] == "memory"
    assert "entities" in result.get("metrics", {})


def test_engineering_router_context():
    """Context discipline should optimize context window."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("context", "auth module analysis")
    assert result["discipline"] == "context"
    assert "selected" in result.get("metrics", {})
    assert "estimated_tokens" in result.get("metrics", {})


def test_engineering_router_prompt():
    """Prompt discipline should construct prompt chain."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("prompt", "build analysis chain")
    assert result["discipline"] == "prompt"
    assert result.get("metrics", {}).get("chain_length", 0) >= 4


def test_engineering_router_graph_over_loop():
    """Graph-over-Loop should use topology for iteration order."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("graph_over_loop", "traverse")
    assert result["discipline"] == "graph_over_loop"
    assert "roots" in result.get("metrics", {})
    assert "processed" in result.get("metrics", {})


def test_engineering_router_loop_over_graph():
    """Loop-over-Graph should iteratively refine the graph."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("loop_over_graph", "refine graph")
    assert result["discipline"] == "loop_over_graph"
    assert result.get("metrics", {}).get("rounds", 0) >= 3


def test_engineering_router_unknown_discipline_defaults():
    """Unknown discipline should default to graph."""
    store = _make_store()
    router = EngineeringRouter(store)
    result = router.execute("nonexistent", "query")
    assert result["discipline"] == "graph"


def test_engineering_result_to_dict():
    """EngineeringResult should serialize correctly."""
    r = EngineeringResult(output="test", discipline="loop", pattern="iterative",
                          steps=["s1"], metrics={"k": 1})
    d = r.to_dict()
    assert d["discipline"] == "loop"
    assert d["steps"] == ["s1"]
    assert d["metrics"] == {"k": 1}


# ===== API Endpoints Tests (Phase 13.4) =====

def test_api_has_rag_endpoints():
    """app.py should have RAG query and patterns endpoints."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api", "app.py")
    content = open(path, encoding="utf-8").read()
    assert "/api/v1/rag/query" in content
    assert "/api/v1/rag/patterns" in content
    assert "RAGRouter" in content


def test_api_has_agent_endpoints():
    """app.py should have agent query and types endpoints."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api", "app.py")
    content = open(path, encoding="utf-8").read()
    assert "/api/v1/agents/query" in content
    assert "/api/v1/agents/types" in content
    assert "AgentRouter" in content


def test_api_has_engineering_endpoint():
    """app.py should have engineering discipline endpoint."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api", "app.py")
    content = open(path, encoding="utf-8").read()
    assert "/api/v1/engineering/" in content
    assert "EngineeringRouter" in content
