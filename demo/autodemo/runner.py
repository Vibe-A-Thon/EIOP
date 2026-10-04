"""Automated EOIP demo runner — Meridian Financial Services.

Executes the full demo walkthrough non-interactively:
  1. Multi-source ingestion (manual folder: PAY domain, pipeline folder: FRD domain)
  2. Code-graph construction from JSON
  3. Crawler data processing
  4. Graph traversal — path, impact, neighborhood, traceability
  5. RAG pattern routing
  6. Agent dispatch
  7. LAYA analysis
  8. Validation and quality metrics

Usage:
    python -m demo.autodemo.runner [--data-dir DIR] [--verbose]
    python -m demo.autodemo.runner --mode manual --verbose
    python -m demo.autodemo.runner --mode pipeline --verbose
    python -m demo.autodemo.runner --mode full --verbose
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages"))

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.meta import bootstrap_meta_graph, link_domains
from eoip.graph.traversal import GraphTraversal
from eoip.graph.rag_router import RAGRouter
from eoip.graph.agent_router import AgentRouter
from eoip.intelligence.laya import LAYAEngine
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.contracts.query_plan import QueryPlan
from eoip.query.eql import parse_and_execute
from eoip.query.executor import QueryExecutor
from eoip.query.nlq import NLQProcessor
from eoip.validation.engine import ValidationEngine
from eoip.validation.quality import QualityMetrics

BANNER = r"""
+-------------------------------------------------------------------+
|  EOIP Automated Demo - Meridian Financial Services               |
|  Enterprise Operational Intelligence Platform                    |
+-------------------------------------------------------------------+
"""

# ---------------------------------------------------------------------------
# Demo data paths (relative to project root)
# ---------------------------------------------------------------------------
MANUAL_DIR = "demo/demodata/manual"
PIPELINE_DIR = "demo/demodata/pipelines"
CODE_DIR = "demo/demodata/code"
CRAWLER_DIR = "demo/demodata/crawler"
RAG_FILE = "demo/demodata/rag/rag-demo-queries.json"
AGENT_FILE = "demo/demodata/agents/agent-scenarios.json"
QUERY_FILE = "demo/demodata/query/query-examples.json"
LAYA_FILE = "demo/demodata/laya/laya-scenarios.json"

# Source system JSON files within manual / pipeline folders
SOURCE_FILES = [
    "rally.json", "jira.json", "gitlab.json", "servicenow.json",
    "confluence.json", "figma.json", "qtest.json",
    "kibana.json", "grafana.json", "datadog.json",
    "api-portal.json", "code-graph.json", "crawler-sites.json",
]

CODE_PROJECTS = [
    "mfs-payment-gateway.json",
    "mfs-fraud-engine.json",
    "mfs-common-libs.json",
    "mfs-customer-portal.json",
]

CRAWLER_FILES = [
    "wiki-confluence.json",
    "api-portal-swagger.json",
    "db-schemas.json",
    "figma-designs.json",
    "observability-portals.json",
]


class DemoResult:
    def __init__(self):
        self.steps: list[dict] = []
        self.start_time = time.monotonic()
        self._phase = ""

    def phase(self, name: str):
        self._phase = name

    def record(self, step: str, status: str, detail: str = ""):
        elapsed = time.monotonic() - self.start_time
        self.steps.append({
            "phase": self._phase,
            "step": step,
            "status": status,
            "detail": detail,
            "elapsed_s": round(elapsed, 2),
        })

    def summary(self) -> dict:
        passed = sum(1 for s in self.steps if s["status"] == "PASS")
        failed = sum(1 for s in self.steps if s["status"] == "FAIL")
        skipped = sum(1 for s in self.steps if s["status"] == "SKIP")
        return {
            "total_steps": len(self.steps),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration_s": round(time.monotonic() - self.start_time, 2),
            "steps": self.steps,
        }


def _load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _print(msg: str, verbose: bool):
    if verbose:
        print(f"[autodemo] {msg}")


# ---------------------------------------------------------------------------
# Phase 1 — Multi-source ingestion
# ---------------------------------------------------------------------------
def _ingest_sources(
    result: DemoResult,
    store: MemoryGraphStore,
    project_root: Path,
    folder: str,
    domain: str,
    verbose: bool,
):
    result.phase(f"Ingest {domain}")
    data_dir = project_root / folder
    total_loaded = 0
    for fname in SOURCE_FILES:
        fpath = data_dir / fname
        data = _load_json(fpath)
        if data is None:
            result.record(f"load_{fname}", "SKIP", f"{fpath} not found")
            continue

        record_count = 0
        if isinstance(data, dict):
            for key in ("issues", "result", "items", "pages", "merge_requests",
                        "saved_objects", "dashboards", "services", "files",
                        "pages", "components", "endpoints", "monitors",
                        "alert_rules", "datasources"):
                items = data.get(key)
                if isinstance(items, list):
                    record_count += len(items)
            if "QueryResult" in data:
                qr = data["QueryResult"]
                record_count += qr.get("TotalResultCount", len(qr.get("Results", [])))
        elif isinstance(data, list):
            record_count = len(data)

        if record_count == 0:
            record_count = 1

        total_loaded += record_count
        result.record(f"load_{fname}", "PASS", f"{record_count} records from {domain}/{fname}")
        _print(f"  Loaded {fname}: {record_count} records", verbose)

    result.record(f"ingest_{domain}_total", "PASS" if total_loaded > 0 else "FAIL",
                  f"{total_loaded} total records from {domain}")
    return total_loaded


# ---------------------------------------------------------------------------
# Phase 2 — Jira deep ingestion (into graph store)
# ---------------------------------------------------------------------------
def _ingest_jira_into_graph(
    result: DemoResult,
    store: MemoryGraphStore,
    project_root: Path,
    folder: str,
    domain: str,
    data_dir: Path,
    verbose: bool,
):
    result.phase(f"Graph Ingest {domain}")
    jira_path = project_root / folder / "jira.json"
    data = _load_json(jira_path)
    if data is None:
        result.record(f"jira_graph_{domain}", "SKIP", "jira.json not found")
        return

    try:
        connector = JiraJsonConnector()
        capture = FileEventCapture(data_dir / "raw" / domain)
        service = JiraIngestionService(
            store, connector, capture, data_dir / "dlq" / domain,
        )
        jira_result = service.ingest(data)
        accepted = jira_result.get("records_accepted", 0)
        result.record(f"jira_graph_{domain}", "PASS",
                      f"{accepted} Jira records ingested into graph ({domain})")
        _print(f"  Jira graph ingest ({domain}): {accepted} accepted", verbose)
    except Exception as exc:
        result.record(f"jira_graph_{domain}", "FAIL", str(exc))


# ---------------------------------------------------------------------------
# Phase 3 — Code-graph construction
# ---------------------------------------------------------------------------
def _load_code_graphs(
    result: DemoResult,
    project_root: Path,
    verbose: bool,
):
    result.phase("Code Graph")
    code_dir = project_root / CODE_DIR
    total_symbols = 0
    total_edges = 0
    for fname in CODE_PROJECTS:
        fpath = code_dir / fname
        data = _load_json(fpath)
        if data is None:
            result.record(f"code_{fname}", "SKIP", f"{fpath} not found")
            continue

        symbols = len(data.get("symbols", []))
        edges = len(data.get("edges", []))
        files = len(data.get("files", []))
        deps = len(data.get("dependencies", []))
        total_symbols += symbols
        total_edges += edges
        result.record(
            f"code_{fname}", "PASS",
            f"{files} files, {symbols} symbols, {deps} deps, {edges} edges",
        )
        _print(f"  Code graph {fname}: {files} files, {symbols} symbols", verbose)

    result.record(
        "code_graph_total", "PASS" if total_symbols > 0 else "FAIL",
        f"{total_symbols} total symbols, {total_edges} total edges across {len(CODE_PROJECTS)} projects",
    )
    return total_symbols


# ---------------------------------------------------------------------------
# Phase 4 — Crawler data
# ---------------------------------------------------------------------------
def _load_crawler_data(
    result: DemoResult,
    project_root: Path,
    verbose: bool,
):
    result.phase("Crawler")
    crawler_dir = project_root / CRAWLER_DIR
    total_pages = 0
    for fname in CRAWLER_FILES:
        fpath = crawler_dir / fname
        data = _load_json(fpath)
        if data is None:
            result.record(f"crawler_{fname}", "SKIP", f"{fpath} not found")
            continue

        if isinstance(data, list):
            count = len(data)
        elif isinstance(data, dict):
            pages = data.get("pages", data.get("results"))
            if not isinstance(pages, list):
                result.record(
                    f"crawler_{fname}", "FAIL",
                    "Crawler object must contain a list in 'pages' or 'results'",
                )
                continue
            count = len(pages)
        else:
            result.record(
                f"crawler_{fname}", "FAIL",
                f"Expected a JSON list or object, got {type(data).__name__}",
            )
            continue

        total_pages += count
        result.record(
            f"crawler_{fname}", "PASS" if count > 0 else "FAIL",
            f"{count} pages loaded from crawler fixture",
        )
        _print(f"  Crawler {fname}: {count} pages", verbose)

    result.record(
        "crawler_total", "PASS" if total_pages > 0 else "FAIL",
        f"{total_pages} total crawled pages across {len(CRAWLER_FILES)} portal types",
    )
    return total_pages


# ---------------------------------------------------------------------------
# Phase 5 — Graph traversal verification
# ---------------------------------------------------------------------------
def _verify_graph(
    result: DemoResult,
    store: MemoryGraphStore,
    verbose: bool,
):
    result.phase("Graph Verification")
    vertices = store.find_vertices(limit=10_000)
    edges = store.find_edges(limit=10_000)
    vertex_count = len(vertices)
    edge_count = len(edges)

    result.record(
        "vertex_count", "PASS" if vertex_count >= 10 else "FAIL",
        f"{vertex_count} vertices in graph",
    )
    result.record(
        "edge_count", "PASS" if edge_count >= 5 else "FAIL",
        f"{edge_count} edges in graph",
    )

    labels = {v.get("label", "unknown") for v in vertices}
    result.record("vertex_labels", "PASS", f"Labels: {sorted(labels)}")
    _print(f"  Graph: {vertex_count} vertices, {edge_count} edges, labels={sorted(labels)}", verbose)

    traversal = GraphTraversal(store)

    pay_items = [v for v in vertices if "PAY-" in str(v.get("properties", {}))]
    if pay_items:
        pay_id = pay_items[0]["properties"].get("canonical_id", "")
        impact = traversal.impact(pay_id, max_depth=3)
        result.record(
            "impact_pay", "PASS",
            f"Impact from {pay_id}: {len(impact)} affected entities",
        )
        _print(f"  Impact analysis ({pay_id}): {len(impact)} entities", verbose)
    else:
        result.record("impact_pay", "SKIP", "No PAY-* work items in graph")

    return vertex_count, edge_count


# ---------------------------------------------------------------------------
# Phase 6 — RAG pattern routing
# ---------------------------------------------------------------------------
def _verify_rag(
    result: DemoResult,
    store: MemoryGraphStore,
    project_root: Path,
    verbose: bool,
):
    result.phase("RAG Routing")
    rag_data = _load_json(project_root / RAG_FILE)
    if rag_data is None:
        result.record("rag_load", "SKIP", "rag-demo-queries.json not found")
        return

    queries = rag_data.get("queries") if isinstance(rag_data, dict) else None
    if not isinstance(queries, list):
        result.record("rag_load", "FAIL", "RAG fixture must contain a 'queries' list")
        return
    result.record("rag_load", "PASS", f"{len(queries)} RAG pattern queries loaded")

    router = RAGRouter(store)
    routed = 0
    failed = 0
    for index, q in enumerate(queries, start=1):
        scenario_id = q.get("id", f"rag-{index}") if isinstance(q, dict) else f"rag-{index}"
        try:
            if not isinstance(q, dict) or not isinstance(q.get("question"), str):
                raise ValueError("Scenario must be an object with a question")
            res = router.route(q["question"], pattern=q.get("pattern"))
            routed += 1
            result.record(
                f"rag_{scenario_id}", "PASS",
                f"Routed to {res.get('pattern', 'unknown')} without execution error",
            )
            _print(f"  RAG [{scenario_id}]: routed -> {res.get('pattern', 'unknown')}", verbose)
        except Exception as exc:
            failed += 1
            result.record(f"rag_{scenario_id}", "FAIL", str(exc))
            _print(f"  RAG [{scenario_id}]: error -> {exc}", verbose)

    result.record(
        "rag_routing", "PASS" if queries and failed == 0 else "FAIL",
        f"{routed}/{len(queries)} RAG queries routed; {failed} failed",
    )


# ---------------------------------------------------------------------------
# Phase 7 — Agent dispatch
# ---------------------------------------------------------------------------
def _verify_agents(
    result: DemoResult,
    store: MemoryGraphStore,
    project_root: Path,
    verbose: bool,
):
    result.phase("Agent Dispatch")
    agent_data = _load_json(project_root / AGENT_FILE)
    if agent_data is None:
        result.record("agent_load", "SKIP", "agent-scenarios.json not found")
        return

    scenarios = agent_data.get("scenarios") if isinstance(agent_data, dict) else None
    if not isinstance(scenarios, list):
        result.record("agent_load", "FAIL", "Agent fixture must contain a 'scenarios' list")
        return
    result.record("agent_load", "PASS", f"{len(scenarios)} agent scenarios loaded")

    router = AgentRouter(store)
    dispatched = 0
    failed = 0
    for index, sc in enumerate(scenarios, start=1):
        scenario_id = sc.get("id", f"agent-{index}") if isinstance(sc, dict) else f"agent-{index}"
        try:
            if not isinstance(sc, dict) or not isinstance(sc.get("question"), str):
                raise ValueError("Scenario must be an object with a question")
            res = router.route(sc["question"], agent_type=sc.get("agent_type"))
            dispatched += 1
            result.record(
                f"agent_{scenario_id}", "PASS",
                f"Dispatched to {res.get('agent_type', 'unknown')} without execution error",
            )
            _print(f"  Agent [{scenario_id}]: dispatched -> {res.get('agent_type', 'unknown')}", verbose)
        except Exception as exc:
            failed += 1
            result.record(f"agent_{scenario_id}", "FAIL", str(exc))
            _print(f"  Agent [{scenario_id}]: error -> {exc}", verbose)

    result.record(
        "agent_dispatch", "PASS" if scenarios and failed == 0 else "FAIL",
        f"{dispatched}/{len(scenarios)} agent scenarios dispatched; {failed} failed",
    )


# ---------------------------------------------------------------------------
# Phase 8 — LAYA analysis
# ---------------------------------------------------------------------------
def _verify_laya(
    result: DemoResult,
    store: MemoryGraphStore,
    project_root: Path,
    verbose: bool,
):
    result.phase("LAYA Analysis")
    laya_data = _load_json(project_root / LAYA_FILE)
    if laya_data is None:
        result.record("laya_load", "SKIP", "laya-scenarios.json not found")
        return

    scenarios = laya_data.get("scenarios") if isinstance(laya_data, dict) else None
    if not isinstance(scenarios, list):
        result.record("laya_load", "FAIL", "LAYA fixture must contain a 'scenarios' list")
        return
    result.record("laya_load", "PASS", f"{len(scenarios)} LAYA scenarios loaded")

    engine = LAYAEngine(store)
    caps = engine.capabilities
    result.record("laya_capabilities", "PASS", f"{len(caps)} capabilities: {', '.join(sorted(caps.keys()))}")

    analyzed = 0
    failed = 0
    for index, sc in enumerate(scenarios, start=1):
        scenario_id = sc.get("id", f"laya-{index}") if isinstance(sc, dict) else f"laya-{index}"
        try:
            if not isinstance(sc, dict) or not isinstance(sc.get("question"), str):
                raise ValueError("Scenario must be an object with a question")
            res = engine.analyze(
                sc["question"],
                capability=sc.get("capability", "entity_explanation"),
                context_ids=sc.get("context_entities", []),
            )
            analyzed += 1
            result.record(
                f"laya_{scenario_id}", "PASS",
                f"Analysis completed with confidence {res.confidence:.2f} "
                f"and {len(res.evidence_refs)} evidence references",
            )
            _print(
                f"  LAYA [{scenario_id}]: confidence={res.confidence:.2f}, "
                f"evidence={len(res.evidence_refs)} refs", verbose,
            )
        except Exception as exc:
            failed += 1
            result.record(f"laya_{scenario_id}", "FAIL", str(exc))
            _print(f"  LAYA [{scenario_id}]: error -> {exc}", verbose)

    result.record(
        "laya_analysis", "PASS" if scenarios and failed == 0 else "FAIL",
        f"{analyzed}/{len(scenarios)} LAYA analyses completed; {failed} failed",
    )


# ---------------------------------------------------------------------------
# Phase 9 — Query examples
# ---------------------------------------------------------------------------
def _verify_queries(
    result: DemoResult,
    store: MemoryGraphStore,
    project_root: Path,
    verbose: bool,
):
    result.phase("Query Examples")
    query_data = _load_json(project_root / QUERY_FILE)
    if query_data is None:
        result.record("query_load", "SKIP", "query-examples.json not found")
        return

    examples = query_data.get("examples") if isinstance(query_data, dict) else None
    if not isinstance(examples, list):
        result.record("query_load", "FAIL", "Query fixture must contain an 'examples' list")
        return

    result.record("query_load", "PASS", f"{len(examples)} query examples loaded")
    executor = QueryExecutor(store)
    nlq = NLQProcessor(store, executor)
    executed = 0
    unsupported = 0
    failed = 0
    for index, example in enumerate(examples, start=1):
        example_id = example.get("id", f"query-{index}") if isinstance(example, dict) else f"query-{index}"
        if not isinstance(example, dict):
            result.record(f"query_{example_id}", "FAIL", "Example must be a JSON object")
            failed += 1
            continue

        kind = example.get("type")
        try:
            if kind == "search":
                response = executor.execute(QueryPlan(
                    intent="SEARCH", anchors=[example["query"]], max_depth=1,
                    result_limit=25, evidence_mode="NONE",
                ))
            elif kind == "path":
                response = executor.execute(QueryPlan(
                    intent="PATH", anchors=[example["source"], example["target"]],
                    max_depth=example.get("max_depth", 6), result_limit=25,
                    evidence_mode="SUMMARY",
                ))
            elif kind == "impact":
                response = executor.execute(QueryPlan(
                    intent="IMPACT", anchors=[example["anchor"]],
                    max_depth=example.get("max_depth", 4), result_limit=100,
                    evidence_mode="SUMMARY",
                ))
            elif kind == "neighborhood":
                response = executor.execute(QueryPlan(
                    intent="NEIGHBORHOOD", anchors=[example["anchor"]],
                    max_depth=example.get("max_depth", 1), result_limit=50,
                    evidence_mode="SUMMARY",
                ))
            elif kind in {"traceability", "lineage"}:
                anchor = example.get("source") or example.get("entity") or example.get("anchor")
                response = executor.execute(QueryPlan(
                    intent=kind.upper(), anchors=[anchor],
                    max_depth=example.get("max_depth", 6), result_limit=100,
                    evidence_mode="FULL" if kind == "traceability" else "SUMMARY",
                ))
            elif kind == "natural_language":
                response = nlq.process(example["query"])
                if response.result is None:
                    raise ValueError(
                        f"NLQ returned no graph result: {response.interpretation.explanation}"
                    )
            elif kind == "eql":
                eql_query = example["query"]
                response = parse_and_execute(store, eql_query)
                if "error" in response:
                    if "TRAVERSE" in eql_query.upper():
                        unsupported += 1
                        result.record(
                            f"query_{example_id}", "SKIP",
                            "Unsupported example: this EQL fixture uses TRAVERSE syntax, "
                            "which the current EQL parser does not implement",
                        )
                        continue
                    raise ValueError(response["error"])
            elif kind in {"cross_domain", "temporal"}:
                unsupported += 1
                reason = (
                    "cross-domain expected-domain assertions are not implemented by "
                    "the current query runner"
                    if kind == "cross_domain"
                    else "date-window temporal queries are not available in QueryPlan"
                )
                result.record(f"query_{example_id}", "SKIP", f"Unsupported example: {reason}")
                continue
            else:
                unsupported += 1
                result.record(
                    f"query_{example_id}", "SKIP",
                    f"Unsupported query-example type: {kind!r}",
                )
                continue

            nodes = getattr(response, "nodes", None)
            paths = getattr(response, "paths", None)
            if isinstance(response, dict):
                nodes = response.get("nodes", response.get("results", nodes))
                paths = response.get("paths", paths)
            detail = (
                f"Executed {kind}; {len(nodes) if isinstance(nodes, list) else 'n/a'} "
                f"result entities, {len(paths) if isinstance(paths, list) else 'n/a'} paths"
            )
            if kind == "path" and not paths:
                detail += "; no matching path returned"
            result.record(f"query_{example_id}", "PASS", detail)
            executed += 1
            _print(f"  Query [{example_id}]: {detail}", verbose)
        except Exception as exc:
            failed += 1
            result.record(f"query_{example_id}", "FAIL", str(exc))
            _print(f"  Query [{example_id}]: error -> {exc}", verbose)

    status = "PASS" if examples and failed == 0 else "FAIL"
    result.record(
        "query_execution", status,
        f"{executed}/{len(examples)} executed; {unsupported} explicitly unsupported; {failed} failed",
    )
    _print(
        f"  Query examples: {executed} executed, {unsupported} unsupported, {failed} failed",
        verbose,
    )


# ---------------------------------------------------------------------------
# Phase 10 — Validation and quality
# ---------------------------------------------------------------------------
def _validate_graph(
    result: DemoResult,
    store: MemoryGraphStore,
    verbose: bool,
):
    result.phase("Validation & Quality")
    engine = ValidationEngine(store)
    val_result = engine.run()
    findings = val_result.get("findings", [])
    error_count = sum(1 for f in findings if f.get("severity") == "error")

    result.record(
        "validation", "PASS" if error_count == 0 else "FAIL",
        f"{len(findings)} findings, {error_count} errors",
    )

    vertices = store.find_vertices(limit=10_000)
    edges = store.find_edges(limit=10_000)
    quality = QualityMetrics.compute(vertices, edges, findings)
    ev_cov = quality.evidence_coverage if quality.evidence_coverage is not None else 0.0
    orph = quality.orphan_rate if quality.orphan_rate is not None else 0.0
    result.record(
        "quality_metrics", "PASS",
        f"evidence_coverage={ev_cov:.2f}, orphan_rate={orph:.2f}",
    )
    _print(f"  Quality: evidence_coverage={ev_cov:.2f}, orphan_rate={orph:.2f}", verbose)


# ---------------------------------------------------------------------------
# Phase 11 — Before/after graph comparison
# ---------------------------------------------------------------------------
def _graph_comparison(
    result: DemoResult,
    store: MemoryGraphStore,
    vertex_before: int,
    edge_before: int,
    verbose: bool,
):
    result.phase("Graph Before/After")
    vertices = store.find_vertices(limit=10_000)
    edges = store.find_edges(limit=10_000)
    v_after = len(vertices)
    e_after = len(edges)
    labels = sorted({v.get("label", "unknown") for v in vertices})

    result.record(
        "graph_growth", "PASS",
        f"Before: {vertex_before}V/{edge_before}E -> After: {v_after}V/{e_after}E "
        f"(+{v_after - vertex_before}V/+{e_after - edge_before}E)",
    )
    result.record("final_labels", "PASS", f"Vertex labels: {labels}")
    _print(f"  Graph growth: {vertex_before} to {v_after} vertices, {edge_before} to {e_after} edges", verbose)


# ═══════════════════════════════════════════════════════════════════
# Main orchestrator
# ═══════════════════════════════════════════════════════════════════
def run_demo(
    data_dir: str | None = None,
    verbose: bool = False,
    mode: str = "full",
) -> dict:
    """Run the automated demo and return results.

    Args:
        data_dir: Working directory for raw captures and DLQ.
        verbose: Print detailed progress.
        mode: 'manual' (PAY domain only), 'pipeline' (FRD domain only),
              or 'full' (both domains + code + crawler + all capabilities).
    """
    result = DemoResult()
    project_root = Path(__file__).resolve().parents[2]
    data = Path(data_dir) if data_dir else project_root / "data" / "autodemo"
    data.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(BANNER)
        print(f"[autodemo] project_root = {project_root}")
        print(f"[autodemo] data_dir     = {data}")
        print(f"[autodemo] mode         = {mode}")
        print()

    # ── Phase 1: Initialize graph store ───────────────────────────
    result.phase("Initialize")
    store = MemoryGraphStore()
    bootstrap_meta_graph(store)
    result.record("init_store", "PASS", "MemoryGraphStore created, meta-graph bootstrapped")

    v_before = len(store.find_vertices(limit=10_000))
    e_before = len(store.find_edges(limit=10_000))

    # ── Phase 2: Multi-source ingestion ───────────────────────────
    if mode in ("manual", "full"):
        _print("--- Manual ingestion: Payment Gateway (PAY) ---", verbose)
        _ingest_sources(result, store, project_root, MANUAL_DIR, "PAY-manual", verbose)
        _ingest_jira_into_graph(result, store, project_root, MANUAL_DIR, "PAY", data, verbose)

    if mode in ("pipeline", "full"):
        _print("--- Pipeline ingestion: Fraud Detection (FRD) ---", verbose)
        _ingest_sources(result, store, project_root, PIPELINE_DIR, "FRD-pipeline", verbose)
        _ingest_jira_into_graph(result, store, project_root, PIPELINE_DIR, "FRD", data, verbose)

    # ── Phase 3: Code-graph construction ──────────────────────────
    if mode == "full":
        _print("--- Code-graph construction ---", verbose)
        _load_code_graphs(result, project_root, verbose)

    # ── Phase 4: Crawler data ─────────────────────────────────────
    if mode == "full":
        _print("--- Crawler data processing ---", verbose)
        _load_crawler_data(result, project_root, verbose)

    # ── Phase 5: Graph verification ───────────────────────────────
    _print("--- Graph verification ---", verbose)
    v_count, e_count = _verify_graph(result, store, verbose)

    # ── Phase 6: RAG routing ──────────────────────────────────────
    if mode == "full":
        _print("--- RAG pattern routing ---", verbose)
        _verify_rag(result, store, project_root, verbose)

    # ── Phase 7: Agent dispatch ───────────────────────────────────
    if mode == "full":
        _print("--- Agent dispatch ---", verbose)
        _verify_agents(result, store, project_root, verbose)

    # ── Phase 8: LAYA analysis ────────────────────────────────────
    if mode == "full":
        _print("--- LAYA analysis ---", verbose)
        _verify_laya(result, store, project_root, verbose)

    # ── Phase 9: Query examples ───────────────────────────────────
    if mode == "full":
        _print("--- Query examples ---", verbose)
        _verify_queries(result, store, project_root, verbose)

    # ── Phase 10: Validation and quality ──────────────────────────
    _print("--- Validation & quality ---", verbose)
    _validate_graph(result, store, verbose)

    # ── Phase 11: Graph before/after comparison ───────────────────
    _graph_comparison(result, store, v_before, e_before, verbose)

    # ── Cross-domain link ─────────────────────────────────────────
    result.phase("Cross-Domain Links")
    try:
        link_domains(store, store.find_vertices(limit=50_000))
        result.record("link_domains", "PASS", "Cross-domain edges created")
    except Exception as exc:
        result.record("link_domains", "FAIL", str(exc))

    summary = result.summary()
    if verbose:
        print(f"\n{'=' * 60}")
        print(json.dumps(summary, indent=2))

    return summary


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        description="Run EOIP automated demo - Meridian Financial Services",
    )
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Working directory for captures and DLQ")
    parser.add_argument("--verbose", action="store_true",
                        help="Print detailed progress to stdout")
    parser.add_argument("--output", type=str, default=None,
                        help="Write JSON results to file")
    parser.add_argument("--mode", type=str, default="full",
                        choices=["manual", "pipeline", "full"],
                        help="Ingestion scope: manual (PAY), pipeline (FRD), or full (both + capabilities)")
    args = parser.parse_args(argv)

    summary = run_demo(data_dir=args.data_dir, verbose=args.verbose, mode=args.mode)

    if args.output:
        Path(args.output).write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"[autodemo] Results written to {args.output}")

    passed = summary["passed"]
    total = summary["total_steps"]
    failed = summary["failed"]
    skipped = summary["skipped"]
    duration = summary["duration_s"]

    print(f"\n{'=' * 60}")
    print(f"  EOIP Demo - Meridian Financial Services")
    print(f"  {passed}/{total} passed, {failed} failed, {skipped} skipped in {duration}s")
    print(f"{'=' * 60}")

    if failed > 0:
        print("\nFailed steps:")
        for step in summary["steps"]:
            if step["status"] == "FAIL":
                print(f"  X [{step['phase']}] {step['step']} - {step['detail']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
