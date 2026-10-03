"""Test intelligence service (G2-T0601..0603).

Maps tests to code symbols, test runs to builds/releases,
and provides change-based test selection.
"""

from __future__ import annotations

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import EDGE_LABELS


def map_tests_to_code(store: GraphStore) -> list[dict]:
    """Find test-to-code mappings through TESTS edges and code coverage evidence."""
    tests = store.find_vertices(label="TestCase", limit=10_000)
    mappings: list[dict] = []
    for test in tests:
        edges = store.find_edges(out_v=test["vid"], limit=1000)
        targets = []
        for edge in edges:
            if edge["label"] == "TESTS":
                target = store.get_vertex(edge["in_v"])
                if target and target["label"] in ("CodeSymbol", "File", "APIEndpoint"):
                    targets.append({
                        "canonical_id": target["canonical_id"],
                        "label": target["label"],
                        "name": target["properties"].get("name") or target["properties"].get("qualified_name", ""),
                    })
        if targets:
            mappings.append({
                "test_id": test["canonical_id"],
                "test_name": test["properties"].get("name", ""),
                "test_type": test["properties"].get("test_type", ""),
                "code_targets": targets,
            })
    return mappings


def map_test_runs_to_builds(store: GraphStore) -> list[dict]:
    """Map test runs to their associated builds/releases through edge traversal."""
    runs = store.find_vertices(label="TestRun", limit=10_000)
    mappings: list[dict] = []
    for run in runs:
        edges = store.find_edges(out_v=run["vid"], limit=1000)
        builds: list[dict] = []
        for edge in edges:
            target = store.get_vertex(edge["in_v"])
            if not target:
                continue
            if target["label"] in ("PipelineRun", "BuildRecord", "Release", "Deployment"):
                builds.append({
                    "canonical_id": target["canonical_id"],
                    "label": target["label"],
                    "name": target["properties"].get("name", ""),
                    "status": target["properties"].get("status", ""),
                })
        suite_edges = store.find_edges(in_v=run["vid"], limit=100)
        suite_name = None
        for se in suite_edges:
            src = store.get_vertex(se["out_v"])
            if src and src["label"] == "TestSuite":
                suite_name = src["properties"].get("name")
                break
        mappings.append({
            "run_id": run["canonical_id"],
            "run_name": run["properties"].get("name", ""),
            "execution_status": run["properties"].get("execution_status", ""),
            "passed_count": run["properties"].get("passed_count"),
            "failed_count": run["properties"].get("failed_count"),
            "suite_name": suite_name,
            "builds": builds,
        })
    return mappings


def select_tests_for_changes(store: GraphStore, changed_files: list[str]) -> dict:
    """Given changed file canonical IDs, find tests that cover the affected code.

    Traversal: changed File -> DECLARES -> CodeSymbol <- TESTS <- TestCase
    Also: changed File <- TESTS <- TestCase (direct file-level tests)
    """
    affected_tests: list[dict] = []
    seen_test_ids: set[str] = set()
    affected_symbols: list[dict] = []

    for file_cid in changed_files:
        file_v = store.get_vertex_by_canonical_id(file_cid)
        if not file_v:
            continue

        direct_test_edges = store.find_edges(in_v=file_v["vid"], limit=1000)
        for edge in direct_test_edges:
            if edge["label"] == "TESTS":
                test = store.get_vertex(edge["out_v"])
                if test and test["canonical_id"] not in seen_test_ids:
                    seen_test_ids.add(test["canonical_id"])
                    affected_tests.append({
                        "test_id": test["canonical_id"],
                        "test_name": test["properties"].get("name", ""),
                        "reason": f"directly tests {file_cid}",
                    })

        symbol_edges = store.find_edges(out_v=file_v["vid"], limit=1000)
        for se in symbol_edges:
            if se["label"] == "DECLARES":
                symbol = store.get_vertex(se["in_v"])
                if not symbol:
                    continue
                affected_symbols.append({
                    "canonical_id": symbol["canonical_id"],
                    "name": symbol["properties"].get("qualified_name", ""),
                })
                test_edges = store.find_edges(in_v=symbol["vid"], limit=1000)
                for te in test_edges:
                    if te["label"] == "TESTS":
                        test = store.get_vertex(te["out_v"])
                        if test and test["canonical_id"] not in seen_test_ids:
                            seen_test_ids.add(test["canonical_id"])
                            affected_tests.append({
                                "test_id": test["canonical_id"],
                                "test_name": test["properties"].get("name", ""),
                                "reason": f"tests symbol {symbol['canonical_id']} in {file_cid}",
                            })

    return {
        "changed_files": changed_files,
        "affected_symbols": affected_symbols,
        "selected_tests": affected_tests,
        "total_tests": len(affected_tests),
    }
