"""Automated EOIP demo runner.

Executes the full demo walkthrough non-interactively, loading data,
running queries, and capturing output for verification.

Usage:
    python -m Demo.autodemo.runner [--data-dir DIR] [--verbose]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages"))

from eoip.demo import load_demo
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.meta import bootstrap_meta_graph
from eoip.graph.traversal import GraphTraversal
from eoip.validation.engine import ValidationEngine
from eoip.validation.quality import QualityMetrics


class DemoResult:
    def __init__(self):
        self.steps = []
        self.start_time = time.monotonic()

    def record(self, step: str, status: str, detail: str = ""):
        elapsed = time.monotonic() - self.start_time
        self.steps.append({
            "step": step,
            "status": status,
            "detail": detail,
            "elapsed_s": round(elapsed, 2),
        })

    def summary(self) -> dict:
        passed = sum(1 for s in self.steps if s["status"] == "PASS")
        failed = sum(1 for s in self.steps if s["status"] == "FAIL")
        return {
            "total_steps": len(self.steps),
            "passed": passed,
            "failed": failed,
            "duration_s": round(time.monotonic() - self.start_time, 2),
            "steps": self.steps,
        }


def run_demo(data_dir: str | None = None, verbose: bool = False) -> dict:
    """Run the automated demo and return results."""
    result = DemoResult()
    project_root = Path(__file__).resolve().parents[2]
    data = Path(data_dir) if data_dir else project_root / "data" / "autodemo"
    data.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"[autodemo] project_root={project_root}")
        print(f"[autodemo] data_dir={data}")

    # Step 1: Initialize graph store
    store = MemoryGraphStore()
    result.record("init_store", "PASS", "MemoryGraphStore created")

    # Step 2: Load demo data
    try:
        demo_result = load_demo(store, str(data), project_root=str(project_root))
        jira_count = demo_result.get("jira", {}).get("records_accepted", 0)
        git_files = demo_result.get("git", {}).get("files", 0)
        result.record(
            "load_demo", "PASS",
            f"Jira: {jira_count} records, Git: {git_files} files",
        )
        if verbose:
            print(f"[autodemo] Demo loaded: {json.dumps(demo_result, indent=2)}")
    except Exception as exc:
        result.record("load_demo", "FAIL", str(exc))
        return result.summary()

    # Step 3: Verify vertex counts
    vertices = store.find_vertices(limit=10_000)
    vertex_count = len(vertices)
    if vertex_count >= 50:
        result.record("vertex_count", "PASS", f"{vertex_count} vertices")
    else:
        result.record("vertex_count", "FAIL", f"Only {vertex_count} vertices (expected >= 50)")

    # Step 4: Verify edge counts
    edges = store.find_edges(limit=10_000)
    edge_count = len(edges)
    if edge_count >= 40:
        result.record("edge_count", "PASS", f"{edge_count} edges")
    else:
        result.record("edge_count", "FAIL", f"Only {edge_count} edges (expected >= 40)")

    # Step 5: Search for EOIP-1
    search_results = store.find_vertices(label="WorkItem", limit=100)
    eoip1 = [v for v in search_results if "EOIP-1" in str(v.get("properties", {}))]
    if eoip1:
        result.record("search_eoip1", "PASS", "WorkItem EOIP-1 found")
    else:
        result.record("search_eoip1", "FAIL", "WorkItem EOIP-1 not found")

    # Step 6: Path query — EOIP-1 to compute_impact
    traversal = GraphTraversal(store)
    source_id = "urn:eoip:work:item:jira:EOIP-1"
    target_candidates = [
        v for v in store.find_vertices(label="CodeSymbol", limit=500)
        if "compute_impact" in str(v.get("properties", {}).get("qualified_name", ""))
    ]
    if target_candidates:
        target_id = target_candidates[0]["properties"]["canonical_id"]
        path = traversal.find_path(source_id, target_id, max_depth=6)
        if path:
            result.record(
                "golden_path", "PASS",
                f"Path found: {len(path)} hops from EOIP-1 to compute_impact",
            )
        else:
            result.record("golden_path", "FAIL", "No path found")
    else:
        result.record("golden_path", "FAIL", "compute_impact symbol not found")

    # Step 7: Impact analysis
    impact = traversal.impact(source_id, max_depth=3)
    if impact:
        result.record("impact_analysis", "PASS", f"{len(impact)} affected entities")
    else:
        result.record("impact_analysis", "FAIL", "No impact results")

    # Step 8: Validation
    engine = ValidationEngine(store)
    val_result = engine.run()
    error_count = sum(
        1 for f in val_result.get("findings", [])
        if f.get("severity") == "error"
    )
    result.record(
        "validation", "PASS" if error_count == 0 else "FAIL",
        f"{len(val_result.get('findings', []))} findings, {error_count} errors",
    )

    # Step 9: Quality metrics
    findings = val_result.get("findings", [])
    quality = QualityMetrics.compute(vertices, edges, findings)
    ev_cov = quality.evidence_coverage if quality.evidence_coverage is not None else 0.0
    orph = quality.orphan_rate if quality.orphan_rate is not None else 0.0
    result.record(
        "quality_metrics", "PASS",
        f"evidence_coverage={ev_cov:.2f}, orphan_rate={orph:.2f}",
    )

    # Step 10: Cross-domain vertex labels
    labels = set()
    for v in vertices:
        labels.add(v.get("label", "unknown"))
    expected = {"Project", "WorkItem", "Person", "Repository", "File", "CodeSymbol"}
    found = expected & labels
    if found == expected:
        result.record("required_labels", "PASS", f"All required labels present: {sorted(found)}")
    else:
        missing = expected - found
        result.record("required_labels", "FAIL", f"Missing labels: {sorted(missing)}")

    summary = result.summary()
    if verbose:
        print(f"\n[autodemo] Summary: {json.dumps(summary, indent=2)}")

    return summary


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="Run EOIP automated demo")
    parser.add_argument("--data-dir", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--output", type=str, default=None, help="Write JSON results to file")
    args = parser.parse_args(argv)

    summary = run_demo(data_dir=args.data_dir, verbose=args.verbose)

    if args.output:
        Path(args.output).write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"[autodemo] Results written to {args.output}")

    passed = summary["passed"]
    total = summary["total_steps"]
    failed = summary["failed"]
    print(f"\n[autodemo] {passed}/{total} passed, {failed} failed in {summary['duration_s']}s")

    if failed > 0:
        for step in summary["steps"]:
            if step["status"] == "FAIL":
                print(f"  FAIL: {step['step']} — {step['detail']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
