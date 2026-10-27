"""SP2Bench (Schmidt, Hornung, Lausen, Pinkel - ICDE 2009) through the EOIP SPARQL endpoint (CRA-024 A.2).

The benchmark queries Q1-Q12c and the documents produced by the official SP2Bench generator come from a
pinned commit of RDFLib/rdflib-benchmark (``scripts/fetch_sp2bench.sh``, sha256-checked). Two measurements:

* **correctness** - on a small document every query is answered through ``SparqlProtocolHandler`` on the
  real engine and compared with rdflib's independent evaluation of the same query over the same data
  (rows as a multiset; a page truncated at the 10,000-row budget must be a sub-multiset of the reference);
* **latency** - on a larger document every query is answered through the handler, under the endpoint's
  30 s deadline and 10,000-row page, and the wall time is recorded. Separately the engine's *full*
  evaluation (``SELECT (COUNT(*) AS ?n) { <query> }`` straight to the engine, 30 s server timeout) is timed
  and the counts of the two engines are compared, so a fast first page cannot hide a slow or wrong query.

Nothing here passes by construction: every outcome is what the engine returned, and anything over budget
or wrong is reported as such (the test decides whether it is a recorded known gap).
"""
from __future__ import annotations

import argparse
import bz2
import json
import re
import time
from collections import Counter
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import httpx

from eoip.query.sparql_protocol import SparqlProtocolHandler
from eoip.query.w3c_conformance import _norm, _Store, _term

DEADLINE_S = 30.0
PAGE = 10_000
QUERY_IDS = ("q01", "q02", "q03a", "q03b", "q03c", "q04", "q05a", "q05b", "q06", "q07", "q08", "q09",
             "q10", "q11", "q12a", "q12b", "q12c")


def load_queries(root: Path) -> dict[str, str]:
    return {q: (root / "queries" / f"{q}.sparql").read_text(encoding="utf-8") for q in QUERY_IDS}


def _chunks(path: Path, size: int = 1 << 20) -> Iterator[bytes]:
    with bz2.open(path, "rb") as fh:
        while chunk := fh.read(size):
            yield chunk


def load_document(store: _Store, path: Path) -> float:
    """Stream the generator's Turtle document into the store's default graph; returns seconds taken."""
    t0 = time.perf_counter()
    url = (f"{store.query_endpoint}/data?default" if store.backend == "fuseki"
           else f"{store.query_endpoint}/statements")
    r = httpx.post(url, content=_chunks(path), headers={"Content-Type": "text/turtle"}, auth=store.auth,
                   timeout=1800)
    r.raise_for_status()
    return time.perf_counter() - t0


def _row_key(row: dict[str, Any], vars_: list[str]) -> tuple:
    # Blank-node labels are local to each engine: any blank node matches any blank node (counted apart).
    out = []
    for v in vars_:
        n = _norm(row.get(v))
        out.append(("B",) if n and n[0] == "B" else n)
    return tuple(out)


def reference(path: Path, queries: dict[str, str]) -> dict[str, dict[str, Any]]:
    """rdflib's evaluation of every query over the document: the independent oracle."""
    import rdflib

    g = rdflib.Graph()
    with bz2.open(path) as fh:
        g.parse(fh, format="turtle")
    ref: dict[str, dict[str, Any]] = {}
    for qid, text in queries.items():
        t0 = time.perf_counter()
        res = g.query(text)
        if res.type == "ASK":
            ref[qid] = {"kind": "ASK", "boolean": bool(res.askAnswer)}
        else:
            vars_ = [str(v) for v in res.vars]
            rows = Counter(_row_key({str(k): v for k, v in r.asdict().items()}, vars_) for r in res)
            ref[qid] = {"kind": "SELECT", "vars": vars_, "rows": rows, "count": sum(rows.values())}
        ref[qid]["ms"] = round((time.perf_counter() - t0) * 1000)
    return ref


def through_endpoint(handler: SparqlProtocolHandler, text: str) -> dict[str, Any]:
    t0 = time.perf_counter()
    status, _, body = handler.handle_request("POST", headers={"Content-Type": "application/sparql-query",
                                                              "Accept": "application/sparql-results+json"},
                                             body=text)
    ms = (time.perf_counter() - t0) * 1000
    out: dict[str, Any] = {"status": status, "ms": round(ms)}
    if status != 200:
        out["detail"] = body[:300]
        return out
    data = json.loads(body)
    if "boolean" in data:
        out.update(kind="ASK", boolean=bool(data["boolean"]))
    else:
        vars_ = data["head"]["vars"]
        rows = Counter(_row_key({k: _term(v) for k, v in b.items()}, vars_) for b in data["results"]["bindings"])
        out.update(kind="SELECT", vars=vars_, rows=rows, count=sum(rows.values()))
    return out


def _count_wrapper(text: str) -> str:
    """``SELECT (COUNT(*) AS ?n) { SELECT ... }`` - the full result size, evaluated by the engine."""
    m = re.search(r"\bSELECT\b", text, re.IGNORECASE)
    assert m, "not a SELECT query"
    return f"{text[:m.start()]}SELECT (COUNT(*) AS ?n) WHERE {{\n{text[m.start():]}\n}}"


def full_evaluation(store: _Store, text: str) -> dict[str, Any]:
    """The engine's complete evaluation, bypassing EOIP paging, under the same 30 s server timeout."""
    ask = re.search(r"^\s*ASK\b", re.sub(r"(?im)^\s*PREFIX[^\n]*\n", "", text), re.IGNORECASE) is not None
    q = text if ask else _count_wrapper(text)
    url = f"{store.query_endpoint}/sparql" if store.backend == "fuseki" else store.query_endpoint
    t0 = time.perf_counter()
    try:
        r = httpx.post(url, data={"query": q, "timeout": str(int(DEADLINE_S))},  # seconds on both engines
                       headers={"Accept": "application/sparql-results+json"}, auth=store.auth,
                       timeout=DEADLINE_S + 15)
    except httpx.TimeoutException:
        return {"status": "timeout", "ms": round((time.perf_counter() - t0) * 1000)}
    ms = round((time.perf_counter() - t0) * 1000)
    if r.status_code != 200:
        timed_out = r.status_code == 503 or "timeout" in r.text.lower() or (r.status_code >= 500 and ms >= DEADLINE_S * 950)
        return {"status": "timeout" if timed_out else "error",
                "http": r.status_code, "ms": ms, "detail": r.text[:200]}
    if "timed out" in r.headers.get("X-GraphDB-Warning", "").lower():
        return {"status": "timeout", "ms": ms, "detail": "GraphDB: incomplete results at the timeout"}
    try:
        data = r.json()
    except json.JSONDecodeError:
        return {"status": "timeout", "ms": ms, "detail": "truncated stream"}
    if ask:
        return {"status": "ok", "ms": ms, "boolean": bool(data["boolean"])}
    return {"status": "ok", "ms": ms, "count": int(data["results"]["bindings"][0]["n"]["value"])}


def judge_correctness(ref: dict[str, Any], got: dict[str, Any]) -> tuple[bool, str]:
    if got["status"] != 200:
        return False, f"HTTP {got['status']}: {got.get('detail', '')[:120]}"
    if ref["kind"] == "ASK":
        ok = got.get("boolean") == ref["boolean"]
        return ok, f"ASK {got.get('boolean')} vs reference {ref['boolean']}"
    if got.get("vars") != ref["vars"]:
        return False, f"vars {got.get('vars')} vs {ref['vars']}"
    if ref["count"] <= PAGE:
        ok = got["rows"] == ref["rows"]
        return ok, f"{got['count']} rows vs reference {ref['count']}" + ("" if ok else " (multisets differ)")
    extra = got["rows"] - ref["rows"]  # truncated page: every returned row must be a reference row
    ok = got["count"] == PAGE and not extra
    return ok, f"page of {got['count']} of {ref['count']} reference rows; {sum(extra.values())} not in reference"


def run_correctness(store: _Store, doc: Path, queries: dict[str, str],
                    ref: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    store.create()
    store.clear()
    load_document(store, doc)
    ref = ref or reference(doc, queries)
    handler = SparqlProtocolHandler(rdf_backend=store.sparql_backend())
    out = []
    for qid, text in queries.items():
        got = through_endpoint(handler, text)
        ok, detail = judge_correctness(ref[qid], got)
        out.append({"query": qid, "outcome": "pass" if ok else "fail", "detail": detail, "endpoint_ms": got["ms"],
                    "reference_ms": ref[qid]["ms"]})
    return out


def run_latency(store: _Store, doc: Path, queries: dict[str, str]) -> dict[str, Any]:
    store.create()
    store.clear()
    load_s = load_document(store, doc)
    handler = SparqlProtocolHandler(rdf_backend=store.sparql_backend())
    rows = []
    for qid, text in queries.items():
        got = through_endpoint(handler, text)
        full = full_evaluation(store, text)
        within = got["status"] == 200 and got["ms"] <= DEADLINE_S * 1000
        rows.append({"query": qid, "endpoint_status": got["status"], "endpoint_ms": got["ms"],
                     "endpoint_rows": got.get("count", got.get("boolean")),
                     "within_30s": within, "full": full,
                     "full_within_30s": full["status"] == "ok" and full["ms"] <= DEADLINE_S * 1000,
                     "detail": got.get("detail", "")})
    return {"document": doc.name, "load_s": round(load_s, 1), "queries": rows}


def cancellation_probe(store: _Store, text: str, deadline_ms: int = 5_000) -> dict[str, Any]:
    """A query known to run long, under a lowered deadline: the engine must abort it server-side and the
    endpoint must answer promptly (CRA-024.9) - not wait for the client-side safety margin."""
    from eoip.query.sparql_backend import SparqlCancelled

    backend = store.sparql_backend()
    backend.deadline_ms = deadline_ms
    t0 = time.perf_counter()
    try:
        backend.query(text)
        outcome = "completed"
    except SparqlCancelled as exc:
        outcome = "cancelled: " + str(exc)
    return {"deadline_ms": deadline_ms, "elapsed_ms": round((time.perf_counter() - t0) * 1000), "outcome": outcome}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, required=True, help="sp2b/ directory of the pinned fetch")
    ap.add_argument("--backend", choices=("fuseki", "graphdb"), required=True)
    ap.add_argument("--server", required=True)
    ap.add_argument("--dataset", default="sp2b")
    ap.add_argument("--small", default="16000.n3.bz2")
    ap.add_argument("--large", default="1024000.n3.bz2")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    import os

    user, pw = os.environ.get("EOIP_W3C_BACKEND_USER", ""), os.environ.get("EOIP_W3C_BACKEND_PASSWORD", "")
    store = _Store(a.backend, a.server, a.dataset, (user, pw) if user else None)
    queries = load_queries(a.root)
    report = {"backend": a.backend, "correctness": run_correctness(store, a.root / a.small, queries),
              "latency": run_latency(store, a.root / a.large, queries)}
    report["cancellation"] = cancellation_probe(store, queries["q05a"])
    a.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
