"""Run the RAG golden evaluation set and emit a JSON report (FR-RAG-005).

Usage:
    python -m scripts.rag_eval [--store configured|memory] [--synthesize]

The report (per-case results plus aggregate metrics) is printed to stdout and
written to data_root()/state/rag_eval_report.json. Exit code is 0 when every
case passes and 1 otherwise.

`--store configured` (default) uses eoip.runtime.create_store. `--store memory`
loads the demo corpus into a MemoryGraphStore for local/CI runs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eoip.retrieval.eval import EvalCase, run_eval
from eoip.runtime import data_root

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = PROJECT_ROOT / "examples" / "eval" / "rag-golden.json"


def load_cases(path: str | Path) -> list[EvalCase]:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    return [EvalCase(**case) for case in document["cases"]]


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = min(len(ordered) - 1, max(0, round((pct / 100.0) * (len(ordered) - 1))))
    return ordered[rank]


def aggregate(results) -> dict:
    latencies = [r.latency_ms for r in results]
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    return {
        "cases": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "mean_facts_precision": round(sum(r.facts_precision for r in results) / total, 4) if total else 0.0,
        "mean_facts_recall": round(sum(r.facts_recall for r in results) / total, 4) if total else 0.0,
        "mean_evidence_coverage": round(sum(r.evidence_coverage for r in results) / total, 4) if total else 0.0,
        "latency_ms_p50": _percentile(latencies, 50),
        "latency_ms_p95": _percentile(latencies, 95),
    }


def build_store(backend: str):
    if backend == "memory":
        from eoip.demo import load_demo
        from eoip.graph.memory import MemoryGraphStore

        store = MemoryGraphStore()
        load_demo(store, data_root())
        return store
    from eoip.runtime import create_store

    return create_store()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE), help="Path to the golden fixture JSON.")
    parser.add_argument(
        "--store",
        choices=["configured", "memory"],
        default="configured",
        help="Graph store backend: 'configured' uses eoip.runtime.create_store; 'memory' loads the demo corpus.",
    )
    parser.add_argument("--synthesize", action="store_true", help="Enable local model synthesis during retrieval.")
    args = parser.parse_args(argv)

    cases = load_cases(args.fixture)
    store = build_store(args.store)
    results = run_eval(store, cases, synthesize=args.synthesize)
    report = {
        "fixture": str(Path(args.fixture).resolve()),
        "store": args.store,
        "cases": [r.model_dump() for r in results],
        "aggregate": aggregate(results),
    }
    print(json.dumps(report, indent=2))

    report_path = data_root() / "state" / "rag_eval_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"report written to {report_path}", file=sys.stderr)

    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
