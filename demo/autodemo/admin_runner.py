"""Automated EOIP Administration Demo — Meridian Financial Services.

Demonstrates platform administration capabilities against the live API:
  1.  Graph health status
  2.  Ontology schema inspection
  3.  Connector catalog listing
  4.  Single JSON ingestion
  5.  Batch JSON ingestion
  6.  Export format listing
  7.  Graph export (GraphML)
  8.  Gap requirements coverage
  9.  Evidence manifest generation
  10. Test intelligence mappings
  11. Knowledge firewall inspection
  12. Trust state taxonomy

Usage:
    python -m demo.autodemo.admin_runner [--verbose] [--skip-ingest] [--output FILE]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

BANNER = r"""
+-------------------------------------------------------------------+
|  EOIP Administration Demo - Meridian Financial Services           |
|  Platform Administration & Governance Capabilities                |
+-------------------------------------------------------------------+
"""

API_BASE = "http://localhost:8000"
MANUAL_DIR = "demo/demodata/manual"


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


def _print(msg: str, verbose: bool):
    if verbose:
        print(f"[admin-demo] {msg}")


def _api_get(path: str, timeout: float = 30.0) -> dict:
    import urllib.request
    import urllib.error
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"_error": True, "status": exc.code, "reason": exc.reason}
    except Exception as exc:
        return {"_error": True, "reason": str(exc)}


def _api_post(path: str, data: dict | list | None = None,
              file_path: Path | None = None, timeout: float = 60.0) -> dict:
    import urllib.request
    import urllib.error
    url = f"{API_BASE}{path}"
    if file_path is not None:
        body = file_path.read_bytes()
        content_type = "application/json"
    elif data is not None:
        body = json.dumps(data).encode("utf-8")
        content_type = "application/json"
    else:
        body = b""
        content_type = "application/json"
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Content-Type": content_type, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body_text = ""
        try:
            body_text = exc.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        return {"_error": True, "status": exc.code, "reason": exc.reason, "body": body_text}
    except Exception as exc:
        return {"_error": True, "reason": str(exc)}


def _check_api_health(result: DemoResult, verbose: bool) -> bool:
    result.phase("API Health")
    resp = _api_get("/health")
    if resp.get("_error"):
        result.record("api_health", "FAIL",
                       f"API at {API_BASE} not reachable: {resp.get('reason', 'unknown')}")
        return False
    result.record("api_health", "PASS", f"API healthy: {resp.get('status', 'ok')}")
    _print(f"API health: {resp.get('status', 'ok')}", verbose)
    return True


def _step_graph_health(result: DemoResult, verbose: bool):
    result.phase("Graph Health")
    resp = _api_get("/api/v1/graph/health")
    if resp.get("_error"):
        result.record("graph_health", "FAIL", f"Error: {resp.get('reason')}")
        return
    vertices = resp.get("vertex_count", resp.get("vertices", "n/a"))
    edges = resp.get("edge_count", resp.get("edges", "n/a"))
    result.record("graph_health", "PASS",
                   f"Graph: {vertices} vertices, {edges} edges")
    _print(f"Graph health: {vertices} vertices, {edges} edges", verbose)


def _step_schema_inspection(result: DemoResult, verbose: bool):
    result.phase("Schema Inspection")
    resp = _api_get("/api/v1/ontology/schema")
    if resp.get("_error"):
        result.record("schema_inspect", "FAIL", f"Error: {resp.get('reason')}")
        return
    vertex_types = resp.get("vertex_types", resp.get("vertex_labels", []))
    edge_types = resp.get("edge_types", resp.get("edge_labels", []))
    result.record("schema_vertex_types", "PASS",
                   f"{len(vertex_types)} vertex types: {', '.join(vertex_types[:10])}")
    result.record("schema_edge_types", "PASS",
                   f"{len(edge_types)} edge types: {', '.join(edge_types[:10])}")
    _print(f"Schema: {len(vertex_types)} vertex types, {len(edge_types)} edge types", verbose)


def _step_connector_catalog(result: DemoResult, verbose: bool):
    result.phase("Connector Catalog")
    resp = _api_get("/api/v1/connectors")
    if resp.get("_error"):
        result.record("connector_catalog", "FAIL", f"Error: {resp.get('reason')}")
        return
    connectors = resp.get("connectors", resp.get("items", []))
    names = [c.get("name", c.get("id", "?")) for c in connectors] if isinstance(connectors, list) else []
    result.record("connector_catalog", "PASS",
                   f"{len(connectors)} connectors: {', '.join(names[:8])}")
    _print(f"Connectors: {', '.join(names[:8])}", verbose)


def _step_single_ingest(result: DemoResult, project_root: Path, verbose: bool):
    result.phase("Single Ingestion")
    sample_file = project_root / MANUAL_DIR / "rally.json"
    if not sample_file.exists():
        result.record("single_ingest", "SKIP", f"{sample_file} not found")
        return
    resp = _api_post("/api/v1/ingest/json", file_path=sample_file)
    if resp.get("_error"):
        result.record("single_ingest", "FAIL", f"Error: {resp.get('reason')}")
        return
    accepted = resp.get("records_accepted", resp.get("count", "n/a"))
    result.record("single_ingest", "PASS", f"Ingested rally.json: {accepted} records accepted")
    _print(f"Single ingest (rally.json): {accepted} records", verbose)


def _step_batch_ingest(result: DemoResult, project_root: Path, verbose: bool):
    result.phase("Batch Ingestion")
    batch_files = ["jira.json", "gitlab.json", "servicenow.json"]
    payloads = []
    for fname in batch_files:
        fpath = project_root / MANUAL_DIR / fname
        if fpath.exists():
            data = json.loads(fpath.read_text(encoding="utf-8"))
            payloads.append({"source": fname, "data": data})
    if not payloads:
        result.record("batch_ingest", "SKIP", "No source files found")
        return
    resp = _api_post("/api/v1/ingest/batch", data={"items": payloads})
    if resp.get("_error"):
        result.record("batch_ingest", "FAIL", f"Error: {resp.get('reason')}")
        return
    total = resp.get("total_accepted", resp.get("count", len(payloads)))
    result.record("batch_ingest", "PASS",
                   f"Batch ingested {len(payloads)} files: {total} total records")
    _print(f"Batch ingest: {len(payloads)} files, {total} records", verbose)


def _step_export_formats(result: DemoResult, verbose: bool):
    result.phase("Export Formats")
    resp = _api_get("/api/v1/export/formats")
    if resp.get("_error"):
        result.record("export_formats", "FAIL", f"Error: {resp.get('reason')}")
        return
    formats = resp.get("formats", resp.get("items", []))
    names = [f.get("name", f.get("id", "?")) for f in formats] if isinstance(formats, list) else []
    result.record("export_formats", "PASS",
                   f"{len(formats)} export formats: {', '.join(names)}")
    _print(f"Export formats: {', '.join(names)}", verbose)


def _step_graph_export(result: DemoResult, verbose: bool):
    result.phase("Graph Export")
    resp = _api_get("/api/v1/export/graphml?limit=100")
    if resp.get("_error"):
        result.record("graph_export", "FAIL", f"Error: {resp.get('reason')}")
        return
    size = resp.get("size", resp.get("byte_count", len(json.dumps(resp))))
    result.record("graph_export", "PASS", f"GraphML export: {size} bytes")
    _print(f"Graph export (GraphML): {size} bytes", verbose)


def _step_gap_coverage(result: DemoResult, verbose: bool):
    result.phase("Gap Coverage")
    resp = _api_get("/api/v1/gaps/coverage")
    if resp.get("_error"):
        result.record("gap_coverage", "FAIL", f"Error: {resp.get('reason')}")
        return
    total = resp.get("total_requirements", resp.get("total", 0))
    covered = resp.get("covered", 0)
    pct = resp.get("coverage_pct", (covered / total * 100) if total > 0 else 0)
    result.record("gap_coverage", "PASS",
                   f"Gap coverage: {covered}/{total} requirements ({pct:.1f}%)")
    _print(f"Gap coverage: {covered}/{total} ({pct:.1f}%)", verbose)


def _step_evidence_manifest(result: DemoResult, verbose: bool):
    result.phase("Evidence Manifests")
    resp = _api_post("/api/v1/evidence/manifest", data={"scope": "all"})
    if resp.get("_error"):
        result.record("evidence_manifest", "FAIL", f"Error: {resp.get('reason')}")
        return
    items = resp.get("evidence_items", resp.get("items", []))
    result.record("evidence_manifest", "PASS",
                   f"Evidence manifest: {len(items)} evidence items generated")
    _print(f"Evidence manifest: {len(items)} items", verbose)


def _step_test_intelligence(result: DemoResult, verbose: bool):
    result.phase("Test Intelligence")
    resp = _api_get("/api/v1/test-intelligence/mappings")
    if resp.get("_error"):
        result.record("test_intelligence", "FAIL", f"Error: {resp.get('reason')}")
        return
    mappings = resp.get("mappings", resp.get("items", []))
    result.record("test_intelligence", "PASS",
                   f"Test intelligence: {len(mappings)} test-to-requirement mappings")
    _print(f"Test intelligence: {len(mappings)} mappings", verbose)


def _step_knowledge_firewall(result: DemoResult, verbose: bool):
    result.phase("Knowledge Firewall")
    resp = _api_get("/api/v1/firewall/rules")
    if resp.get("_error"):
        result.record("knowledge_firewall", "FAIL", f"Error: {resp.get('reason')}")
        return
    rules = resp.get("rules", resp.get("items", []))
    result.record("knowledge_firewall", "PASS",
                   f"Knowledge firewall: {len(rules)} access rules defined")
    _print(f"Knowledge firewall: {len(rules)} rules", verbose)


def _step_trust_states(result: DemoResult, verbose: bool):
    result.phase("Trust States")
    resp = _api_get("/api/v1/trust/states")
    if resp.get("_error"):
        result.record("trust_states", "FAIL", f"Error: {resp.get('reason')}")
        return
    states = resp.get("states", resp.get("items", []))
    transitions = resp.get("transitions", [])
    result.record("trust_states", "PASS",
                   f"Trust taxonomy: {len(states)} states, {len(transitions)} transitions")
    _print(f"Trust states: {len(states)} states, {len(transitions)} transitions", verbose)


def run_admin_demo(
    verbose: bool = False,
    skip_ingest: bool = False,
) -> dict:
    result = DemoResult()
    project_root = Path(__file__).resolve().parents[2]

    if verbose:
        print(BANNER)
        print(f"[admin-demo] project_root = {project_root}")
        print(f"[admin-demo] skip_ingest  = {skip_ingest}")
        print()

    if not _check_api_health(result, verbose):
        print("\nERROR: EOIP API is not reachable at localhost:8000.")
        print("Start the platform with: scripts\\docker.ps1 up")
        return result.summary()

    _print("--- Step 1: Graph Health ---", verbose)
    _step_graph_health(result, verbose)

    _print("--- Step 2: Schema Inspection ---", verbose)
    _step_schema_inspection(result, verbose)

    _print("--- Step 3: Connector Catalog ---", verbose)
    _step_connector_catalog(result, verbose)

    if not skip_ingest:
        _print("--- Step 4: Single JSON Ingestion ---", verbose)
        _step_single_ingest(result, project_root, verbose)

        _print("--- Step 5: Batch JSON Ingestion ---", verbose)
        _step_batch_ingest(result, project_root, verbose)
    else:
        result.phase("Ingestion")
        result.record("single_ingest", "SKIP", "Skipped (--skip-ingest)")
        result.record("batch_ingest", "SKIP", "Skipped (--skip-ingest)")

    _print("--- Step 6: Export Formats ---", verbose)
    _step_export_formats(result, verbose)

    _print("--- Step 7: Graph Export ---", verbose)
    _step_graph_export(result, verbose)

    _print("--- Step 8: Gap Coverage ---", verbose)
    _step_gap_coverage(result, verbose)

    _print("--- Step 9: Evidence Manifest ---", verbose)
    _step_evidence_manifest(result, verbose)

    _print("--- Step 10: Test Intelligence ---", verbose)
    _step_test_intelligence(result, verbose)

    _print("--- Step 11: Knowledge Firewall ---", verbose)
    _step_knowledge_firewall(result, verbose)

    _print("--- Step 12: Trust States ---", verbose)
    _step_trust_states(result, verbose)

    summary = result.summary()
    if verbose:
        print(f"\n{'=' * 60}")
        print(json.dumps(summary, indent=2))

    return summary


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        description="Run EOIP administration demo - Meridian Financial Services",
    )
    parser.add_argument("--verbose", action="store_true",
                        help="Print detailed progress to stdout")
    parser.add_argument("--output", type=str, default=None,
                        help="Write JSON results to file")
    parser.add_argument("--skip-ingest", action="store_true",
                        help="Skip ingestion steps (use pre-loaded data)")
    args = parser.parse_args(argv)

    summary = run_admin_demo(verbose=args.verbose, skip_ingest=args.skip_ingest)

    if args.output:
        Path(args.output).write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"[admin-demo] Results written to {args.output}")

    passed = summary["passed"]
    total = summary["total_steps"]
    failed = summary["failed"]
    skipped = summary["skipped"]
    duration = summary["duration_s"]

    print(f"\n{'=' * 60}")
    print(f"  EOIP Administration Demo - Meridian Financial Services")
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
