"""Phase 13 — AI-Assisted Graph Intelligence: tests for RAG, Agents, Engineering."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from packages.eoip.graph.agent_router import AGENT_TYPES, AgentResult, AgentRouter
from packages.eoip.graph.engineering import ENGINEERING_DISCIPLINES, EngineeringResult, EngineeringRouter
from packages.eoip.graph.memory import MemoryGraphStore
from packages.eoip.graph.rag_router import RAG_PATTERNS, RAGResult, RAGRouter


def _make_store():
    """Create a store with valid ontology-compliant test data."""
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "svc-auth", "service_id": "svc-auth", "name": "auth_service"})
    store.upsert_vertex("Service", {"canonical_id": "svc-api", "service_id": "svc-api", "name": "api_gateway"})
    store.upsert_vertex("Service", {"canonical_id": "svc-user", "service_id": "svc-user", "name": "user_service"})
    store.upsert_vertex("Repository", {"canonical_id": "repo-main", "repo_id": "repo-main", "name": "main_repo"})
    store.upsert_vertex("File", {"canonical_id": "file-auth", "repo_id": "repo-main", "path": "src/auth.py"})
    store.upsert_vertex("File", {"canonical_id": "file-api", "repo_id": "repo-main", "path": "src/api.py"})
    store.upsert_vertex("CodeSymbol", {"canonical_id": "sym-login", "qualified_name": "auth.login", "symbol_kind": "function"})
    store.upsert_vertex("Document", {"canonical_id": "doc-arch", "name": "Architecture Doc", "path": "docs/arch.md"})

    store.upsert_edge("DEPENDS_ON", "svc-auth", "svc-api", {"source_ref": "code_scan_1"})
    store.upsert_edge("DEPENDS_ON", "svc-api", "svc-user", {"source_ref": "arch_doc"})
    store.upsert_edge("DECLARES", "file-auth", "sym-login", {})
    store.upsert_edge("DEPENDS_ON", "file-auth", "file-api", {"source_ref": "import_scan"})
    return store


# ===== RAG Router Tests (Phase 13.1) =====

def test_rag_patterns_count():
    """Should have exactly 17 RAG patterns."""
    assert len(RAG_PATTERNS) == 17


def test_rag_patterns_unique_names():
    """All RAG pattern names should be unique."""
    names = [p.name for p in RAG_PATTERNS]
    assert len(names) == len(set(names))


def test_rag_pattern_to_dict():
    """RAGPattern should serialize to dict."""
    d = RAG_PATTERNS[0].to_dict()
    assert "name" in d and "description" in d and "retrieval_strategy" in d and "when_to_use" in d


def test_rag_router_classify_simple():
    """Short queries should classify as simple."""
    router = RAGRouter(_make_store())
    assert router.classify("find auth") == "simple"


def test_rag_router_classify_graph():
    """Community-related queries should classify as graph."""
    router = RAGRouter(_make_store())
    assert router.classify("show me the community overview of this graph") == "graph"


def test_rag_router_classify_multihop():
    """Impact queries with selected_id should classify as multihop."""
    router = RAGRouter(_make_store())
    assert router.classify("what would break if removed", {"selected_id": "svc-auth"}) == "multihop"


def test_rag_router_classify_multistep():
    """Multi-question queries should classify as multistep."""
    router = RAGRouter(_make_store())
    assert router.classify("what is svc-auth? what connects to svc-api?") == "multistep"


def test_rag_router_route_simple():
    """Routing a simple query should return results with rag_pattern."""
    router = RAGRouter(_make_store())
    result = router.route("find auth service")
    assert "rag_pattern" in result
    assert "answer" in result
    assert "confidence" in result
    assert isinstance(result["confidence"], float)


def test_rag_router_route_with_explicit_pattern():
    """Explicit pattern should override classification."""
    router = RAGRouter(_make_store())
    result = router.route("anything", pattern="hybrid")
    assert result["rag_pattern"] in ("hybrid", "simple")


def test_rag_result_to_dict():
    """RAGResult should serialize correctly."""
    r = RAGResult(answer="test", pattern="simple", confidence=0.75,
                  sources=["svc-auth"], highlight_ids=["svc-auth"])
    d = r.to_dict()
    assert d["rag_pattern"] == "simple"
    assert d["confidence"] == 0.75
    assert d["sources"] == ["svc-auth"]


# ===== Agent Router Tests (Phase 13.2) =====

def test_agent_types_count():
    """Should have 41 agent types across 9 categories."""
    assert len(AGENT_TYPES) == 41


def test_agent_types_nine_categories():
    """Should have exactly 9 categories."""
    categories = {a.category for a in AGENT_TYPES}
    assert len(categories) == 9
    expected = {"reactive", "deliberative", "tool_using", "orchestration",
                "collaboration", "meta_cognitive", "autonomous", "enterprise", "multi_agent"}
    assert categories == expected


def test_agent_types_unique_names():
    """All agent type names should be unique."""
    names = [a.name for a in AGENT_TYPES]
    assert len(names) == len(set(names))


def test_agent_type_to_dict():
    """AgentType should serialize to dict."""
    d = AGENT_TYPES[0].to_dict()
    assert "name" in d and "category" in d and "capabilities" in d


def test_agent_router_classify_compliance():
    """Compliance-related queries should route to compliance agent."""
    router = AgentRouter(_make_store())
    assert router.classify("check compliance rules") == "compliance"


def test_agent_router_classify_audit():
    """Audit-related queries should route to audit agent."""
    router = AgentRouter(_make_store())
    assert router.classify("generate audit trail") == "audit"


def test_agent_router_classify_explorer():
    """Discovery queries should route to explorer agent."""
    router = AgentRouter(_make_store())
    assert router.classify("explore and discover patterns") == "explorer"


def test_agent_router_route_simple_reflex():
    """Simple reflex agent should answer count queries."""
    router = AgentRouter(_make_store())
    result = router.route("how many nodes", agent_type="simple_reflex")
    assert "answer" in result
    assert result["agent_type"] == "simple_reflex"


def test_agent_router_route_compliance():
    """Compliance agent should produce results."""
    router = AgentRouter(_make_store())
    result = router.route("check compliance", agent_type="compliance")
    assert "answer" in result
    assert result["category"] == "enterprise"


def test_agent_router_route_ensemble():
    """Ensemble agent should combine multiple sub-agents."""
    router = AgentRouter(_make_store())
    result = router.route("analyze everything", agent_type="ensemble")
    assert result["agent_type"] == "ensemble"
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


def test_engineering_discipline_to_dict():
    """EngineeringDiscipline should serialize to dict."""
    d = ENGINEERING_DISCIPLINES[0].to_dict()
    assert "name" in d and "pattern" in d and "use_cases" in d


def test_engineering_router_loop():
    """Loop discipline should iterate and converge."""
    router = EngineeringRouter(_make_store())
    result = router.execute("loop", "analyze convergence")
    assert result["discipline"] == "loop"
    assert "iterations" in result.get("metrics", {})
    assert len(result.get("steps", [])) > 0


def test_engineering_router_graph():
    """Graph discipline should analyze topology."""
    router = EngineeringRouter(_make_store())
    result = router.execute("graph", "topology analysis")
    assert result["discipline"] == "graph"
    assert "components" in result.get("metrics", {})
    assert "density" in result.get("metrics", {})


def test_engineering_router_harness():
    """Harness discipline should execute pipeline stages."""
    router = EngineeringRouter(_make_store())
    result = router.execute("harness", "run pipeline")
    assert result["discipline"] == "harness"
    assert result.get("metrics", {}).get("stages_executed", 0) >= 4


def test_engineering_router_memory():
    """Memory discipline should analyze state patterns."""
    router = EngineeringRouter(_make_store())
    result = router.execute("memory", "state analysis")
    assert result["discipline"] == "memory"
    assert "entities" in result.get("metrics", {})


def test_engineering_router_context():
    """Context discipline should optimize context window."""
    router = EngineeringRouter(_make_store())
    result = router.execute("context", "auth service analysis")
    assert result["discipline"] == "context"
    assert "selected" in result.get("metrics", {})


def test_engineering_router_prompt():
    """Prompt discipline should construct prompt chain."""
    router = EngineeringRouter(_make_store())
    result = router.execute("prompt", "build analysis chain")
    assert result["discipline"] == "prompt"
    assert result.get("metrics", {}).get("chain_length", 0) >= 4


def test_engineering_router_graph_over_loop():
    """Graph-over-Loop should use topology for iteration order."""
    router = EngineeringRouter(_make_store())
    result = router.execute("graph_over_loop", "traverse")
    assert result["discipline"] == "graph_over_loop"
    assert "roots" in result.get("metrics", {})


def test_engineering_router_loop_over_graph():
    """Loop-over-Graph should iteratively refine the graph."""
    router = EngineeringRouter(_make_store())
    result = router.execute("loop_over_graph", "refine graph")
    assert result["discipline"] == "loop_over_graph"
    assert result.get("metrics", {}).get("rounds", 0) >= 3


def test_engineering_router_unknown_defaults():
    """Unknown discipline should default to graph."""
    router = EngineeringRouter(_make_store())
    result = router.execute("nonexistent", "query")
    assert result["discipline"] == "graph"


def test_engineering_result_to_dict():
    """EngineeringResult should serialize correctly."""
    r = EngineeringResult(output="test", discipline="loop", pattern="iterative",
                          steps=["s1"], metrics={"k": 1})
    d = r.to_dict()
    assert d["discipline"] == "loop"
    assert d["steps"] == ["s1"]


# ===== API Endpoints Tests (Phase 13.4) =====

def test_api_has_rag_endpoints():
    """app.py should have RAG query and patterns endpoints."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api", "app.py")
    content = open(path, encoding="utf-8").read()
    assert "/api/v1/rag/query" in content
    assert "/api/v1/rag/patterns" in content


def test_api_has_agent_endpoints():
    """app.py should have agent query and types endpoints."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api", "app.py")
    content = open(path, encoding="utf-8").read()
    assert "/api/v1/agents/query" in content
    assert "/api/v1/agents/types" in content


def test_api_has_engineering_endpoint():
    """app.py should have engineering discipline endpoint."""
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api", "app.py")
    content = open(path, encoding="utf-8").read()
    assert "/api/v1/engineering/" in content
