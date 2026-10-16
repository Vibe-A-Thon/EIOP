import json
from types import SimpleNamespace

from demo.autodemo import runner
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.rag_router import RAGRouter
from eoip.intelligence.laya import LAYAEngine


def _write_json(root, relative_path, data):
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path.parent.parent


def _step(summary, name):
    return next(step for step in summary.steps if step["step"] == name)


def test_crawler_loader_accepts_top_level_lists_and_object_pages(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "CRAWLER_DIR", "crawler")
    monkeypatch.setattr(runner, "CRAWLER_FILES", ["list.json", "object.json"])
    crawler_dir = tmp_path / "crawler"
    crawler_dir.mkdir()
    (crawler_dir / "list.json").write_text(json.dumps([{"url": "/one"}, {"url": "/two"}]))
    (crawler_dir / "object.json").write_text(json.dumps({"pages": [{"url": "/three"}]}))
    summary = runner.DemoResult()

    assert runner._load_crawler_data(summary, tmp_path, verbose=False) == 3
    assert _step(summary, "crawler_list.json")["status"] == "PASS"
    assert _step(summary, "crawler_object.json")["status"] == "PASS"
    assert _step(summary, "crawler_total")["detail"].startswith("3 total")


def test_crawler_loader_reports_invalid_object_shape(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "CRAWLER_DIR", "crawler")
    monkeypatch.setattr(runner, "CRAWLER_FILES", ["invalid.json"])
    crawler_dir = tmp_path / "crawler"
    crawler_dir.mkdir()
    (crawler_dir / "invalid.json").write_text(json.dumps({"unexpected": []}))
    summary = runner.DemoResult()

    assert runner._load_crawler_data(summary, tmp_path, verbose=False) == 0
    assert _step(summary, "crawler_invalid.json")["status"] == "FAIL"
    assert _step(summary, "crawler_total")["status"] == "FAIL"


def test_rag_verifier_attempts_every_query_and_records_route_errors(tmp_path, monkeypatch):
    queries = [{"id": f"rag-{index}", "question": f"Question {index}"} for index in range(7)]
    _write_json(tmp_path, runner.RAG_FILE, {"queries": queries})
    attempted = []

    class FakeRouter:
        def __init__(self, store):
            pass

        def route(self, question, pattern=None):
            attempted.append(question)
            if question == "Question 4":
                raise RuntimeError("route unavailable")
            return {"pattern": pattern or "simple"}

    monkeypatch.setattr(runner, "RAGRouter", FakeRouter)
    summary = runner.DemoResult()
    runner._verify_rag(summary, object(), tmp_path, verbose=False)

    assert len(attempted) == len(queries)
    assert _step(summary, "rag_rag-6")["status"] == "PASS"
    assert _step(summary, "rag_rag-4")["status"] == "FAIL"
    assert _step(summary, "rag_routing")["status"] == "FAIL"
    assert "1 failed" in _step(summary, "rag_routing")["detail"]


def test_agent_verifier_attempts_every_scenario_and_records_dispatch_errors(tmp_path, monkeypatch):
    scenarios = [{"id": f"agent-{index}", "question": f"Question {index}"} for index in range(6)]
    _write_json(tmp_path, runner.AGENT_FILE, {"scenarios": scenarios})
    attempted = []

    class FakeRouter:
        def __init__(self, store):
            pass

        def route(self, question, agent_type=None):
            attempted.append(question)
            if question == "Question 2":
                raise RuntimeError("agent unavailable")
            return {"agent_type": agent_type or "retrieval"}

    monkeypatch.setattr(runner, "AgentRouter", FakeRouter)
    summary = runner.DemoResult()
    runner._verify_agents(summary, object(), tmp_path, verbose=False)

    assert len(attempted) == len(scenarios)
    assert _step(summary, "agent_agent-5")["status"] == "PASS"
    assert _step(summary, "agent_agent-2")["status"] == "FAIL"
    assert _step(summary, "agent_dispatch")["status"] == "FAIL"


def test_laya_verifier_attempts_every_scenario_and_records_analysis_errors(tmp_path, monkeypatch):
    scenarios = [
        {"id": f"laya-{index}", "question": f"Question {index}"}
        for index in range(5)
    ]
    _write_json(tmp_path, runner.LAYA_FILE, {"scenarios": scenarios})
    attempted = []

    class FakeEngine:
        capabilities = {"entity_explanation": object()}

        def __init__(self, store):
            pass

        def analyze(self, question, capability, context_ids):
            attempted.append(question)
            if question == "Question 3":
                raise RuntimeError("analysis unavailable")
            return SimpleNamespace(confidence=0.8, evidence_refs=["evidence"])

    monkeypatch.setattr(runner, "LAYAEngine", FakeEngine)
    summary = runner.DemoResult()
    runner._verify_laya(summary, object(), tmp_path, verbose=False)

    assert len(attempted) == len(scenarios)
    assert _step(summary, "laya_laya-4")["status"] == "PASS"
    assert _step(summary, "laya_laya-3")["status"] == "FAIL"
    assert _step(summary, "laya_analysis")["status"] == "FAIL"


def test_query_verifier_executes_supported_examples_and_marks_unsupported(tmp_path, monkeypatch):
    examples = [
        {"id": "search", "type": "search", "query": "PAY-101"},
        {"id": "path", "type": "path", "source": "source-id", "target": "target-id"},
        {"id": "impact", "type": "impact", "anchor": "anchor-id"},
        {"id": "nl", "type": "natural_language", "query": "What is PAY-101 about?"},
        {"id": "eql", "type": "eql", "query": "FIND WorkItem TRAVERSE IMPLEMENTS TO CodeSymbol"},
        {"id": "cross", "type": "cross_domain", "query": "Find cross-domain coverage"},
        {"id": "temporal", "type": "temporal", "query": "Find changes in a date window"},
    ]
    _write_json(tmp_path, runner.QUERY_FILE, {"examples": examples})
    executed = []
    fake_result = SimpleNamespace(nodes=[object()], paths=[object()])

    class FakeExecutor:
        def __init__(self, store):
            pass

        def execute(self, plan):
            executed.append(plan.intent)
            return fake_result

    class FakeNLQ:
        def __init__(self, store, executor):
            pass

        def process(self, question):
            executed.append("NATURAL_LANGUAGE")
            return SimpleNamespace(
                result=fake_result,
                interpretation=SimpleNamespace(explanation="interpreted"),
            )

    monkeypatch.setattr(runner, "QueryExecutor", FakeExecutor)
    monkeypatch.setattr(runner, "NLQProcessor", FakeNLQ)
    monkeypatch.setattr(
        runner, "parse_and_execute",
        lambda store, query: {"error": "TRAVERSE is unsupported"},
    )
    summary = runner.DemoResult()
    runner._verify_queries(summary, object(), tmp_path, verbose=False)

    assert executed == ["SEARCH", "PATH", "IMPACT", "NATURAL_LANGUAGE"]
    assert _step(summary, "query_search")["status"] == "PASS"
    assert _step(summary, "query_path")["status"] == "PASS"
    assert _step(summary, "query_eql")["status"] == "SKIP"
    assert _step(summary, "query_cross")["status"] == "SKIP"
    assert _step(summary, "query_temporal")["status"] == "SKIP"
    assert _step(summary, "query_execution")["status"] == "PASS"
    assert "4/7 executed; 3 explicitly unsupported; 0 failed" in _step(
        summary, "query_execution"
    )["detail"]


def test_conversational_rag_route_initializes_session_memory():
    response = RAGRouter(MemoryGraphStore()).route(
        "Explore the current graph context", pattern="conversational"
    )

    assert response["rag_pattern"] == "conversational"
    assert response["metadata"]["session_turns"] == 1


def test_laya_gathers_incoming_and_outgoing_graph_neighbors():
    store = MemoryGraphStore()
    first = store.upsert_vertex(
        "Service",
        {"canonical_id": "service:first", "service_id": "first", "name": "first"},
    )
    center = store.upsert_vertex(
        "Service",
        {"canonical_id": "service:center", "service_id": "center", "name": "center"},
    )
    last = store.upsert_vertex(
        "Service",
        {"canonical_id": "service:last", "service_id": "last", "name": "last"},
    )
    store.upsert_edge("DEPENDS_ON", first["vid"], center["vid"], {})
    store.upsert_edge("DEPENDS_ON", center["vid"], last["vid"], {})

    result = LAYAEngine(store).analyze(
        "Explain the service connections",
        context_ids=["service:center"],
    )

    assert result.evidence_refs == ["service:center"]
    assert "connected to 2 Service" in result.answer
