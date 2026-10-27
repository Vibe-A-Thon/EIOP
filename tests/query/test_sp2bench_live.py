"""SP2Bench Q1-Q12c through the EOIP SPARQL endpoint on live Fuseki and GraphDB Free (CRA-024 A.2, .9).

Needs the pinned benchmark (``scripts/fetch_sp2bench.sh``; ``EOIP_SP2B_ROOT`` points at its ``sp2b``
directory) and live engines (``EOIP_LIVE_FUSEKI_URL`` / ``EOIP_LIVE_GRAPHDB_URL``). CI runs this in the
``sparql-fuseki`` job and fails when it is skipped.

Honest reporting: results must equal rdflib's independent evaluation; a query over the 30 s budget is a
failure unless it is a recorded known gap in ``sp2bench_known_gaps.json`` (with its decision), and a gap
that starts passing must be removed from the file. Over-budget queries must still be cancelled by the
engine at the deadline - the endpoint never hangs.
"""
from __future__ import annotations

import json
import os
from functools import cache
from pathlib import Path

import pytest
from eoip.query.sp2bench import (
    DEADLINE_S,
    QUERY_IDS,
    cancellation_probe,
    load_queries,
    reference,
    run_correctness,
    run_latency,
)
from eoip.query.w3c_conformance import _Store

ROOT = Path(os.environ.get("EOIP_SP2B_ROOT", ".cache/sp2bench/sp2b"))
SMALL, LARGE = ROOT / "16000.n3.bz2", ROOT / "1024000.n3.bz2"
GAPS = json.loads(Path(__file__).with_name("sp2bench_known_gaps.json").read_text(encoding="utf-8"))
OUT = Path(os.environ.get("EOIP_W3C_REPORT_DIR", "test-results"))
HANG_MARGIN_S = 3.0  # an over-budget query must be answered (504) within deadline + margin

pytestmark = pytest.mark.skipif(not (SMALL.exists() and LARGE.exists()),
                                reason="SP2Bench not fetched (scripts/fetch_sp2bench.sh)")


def _backends() -> dict[str, tuple[str, tuple[str, str] | None]]:
    out: dict[str, tuple[str, tuple[str, str] | None]] = {}
    if os.environ.get("EOIP_LIVE_FUSEKI_URL"):
        server = os.environ["EOIP_LIVE_FUSEKI_URL"].rstrip("/").rsplit("/", 1)[0]
        out["fuseki"] = (server, (os.environ.get("EOIP_LIVE_FUSEKI_USER", "admin"),
                                  os.environ.get("EOIP_LIVE_FUSEKI_PASSWORD", "")))
    if os.environ.get("EOIP_LIVE_GRAPHDB_URL"):
        out["graphdb"] = (os.environ["EOIP_LIVE_GRAPHDB_URL"].rstrip("/"), None)
    return out


@cache
def _reference():
    return reference(SMALL, load_queries(ROOT))


@pytest.mark.parametrize("backend", sorted(_backends()) or ["none"])
def test_sp2bench_on_live_engine(backend: str) -> None:
    configured = _backends()
    if backend not in configured:
        pytest.skip("no live Fuseki/GraphDB configured")
    server, auth = configured[backend]
    store = _Store(backend, server, "sp2b", auth)
    queries = load_queries(ROOT)
    correctness = run_correctness(store, SMALL, queries, _reference())
    latency = run_latency(store, LARGE, queries)
    probe = cancellation_probe(store, queries["q05a"])
    report = {"backend": backend, "sp2b_commit": GAPS["sp2b_commit"], "correctness": correctness,
              "latency": latency, "cancellation": probe}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"sp2bench-{backend}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    assert [r["query"] for r in correctness] == list(QUERY_IDS)
    wrong = [f"{r['query']}: {r['detail']}" for r in correctness if r["outcome"] != "pass"]
    assert not wrong, "results differ from rdflib's evaluation of the same query:\n" + "\n".join(wrong)

    known = GAPS["latency_gaps"].get(backend, {})
    rows = {r["query"]: r for r in latency["queries"]}
    over = [q for q, r in rows.items() if not r["within_30s"] and q not in known]
    assert not over, f"queries over the 30 s budget that are not recorded gaps: {over}"
    stale = [q for q in known if rows[q]["within_30s"]]
    assert not stale, f"recorded latency gaps that now pass (remove them from the file): {stale}"
    errors = [f"{q}: {r['endpoint_status']} {r['detail']}" for q, r in rows.items()
              if r["endpoint_status"] not in (200, 504)]
    assert not errors, f"endpoint errors (not timeouts): {errors}"
    hung = [f"{q}: {r['endpoint_ms']} ms" for q, r in rows.items() if r["endpoint_ms"] > (DEADLINE_S + HANG_MARGIN_S) * 1000]
    assert not hung, f"over-budget queries were not cancelled at the deadline: {hung}"
    assert probe["outcome"].startswith("cancelled") and probe["elapsed_ms"] < probe["deadline_ms"] + 1500, probe


def test_sp2bench_engines_agree_on_full_result_sizes() -> None:
    """Both engines' full evaluations (no paging) agree wherever both finished in budget."""
    reports = {b: OUT / f"sp2bench-{b}.json" for b in ("fuseki", "graphdb")}
    if not all(p.exists() for p in reports.values()):
        pytest.skip("needs the reports of both live engines from this run")
    full = {b: {r["query"]: r["full"] for r in json.loads(p.read_text())["latency"]["queries"]}
            for b, p in reports.items()}
    both = [q for q in QUERY_IDS if full["fuseki"][q]["status"] == full["graphdb"][q]["status"] == "ok"]
    assert len(both) >= 10
    differ = [(q, full["fuseki"][q], full["graphdb"][q]) for q in both
              if full["fuseki"][q].get("count", full["fuseki"][q].get("boolean"))
              != full["graphdb"][q].get("count", full["graphdb"][q].get("boolean"))]
    assert not differ, differ
