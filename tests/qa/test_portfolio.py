from argparse import Namespace

from qa.bench import ROOT
from qa.portfolio import build_catalog, category, manifest, run_suite
from qa.schema_quality import analyze


def test_manifest_has_unique_suites_and_no_command_for_quarantined_bench():
    suites = manifest()
    assert len(suites) >= 20
    legacy = next(suite for suite in suites if suite["id"] == "legacy-functional-bench")
    assert legacy["command"] is None
    assert legacy["risk"] == "quarantined"


def test_catalog_discovers_python_and_browser_suites():
    catalog = build_catalog()
    assert catalog["totals"]["files"] >= 100
    assert catalog["totals"]["test_definitions"] >= 100
    assert category(ROOT / "tests" / "security" / "test_example.py") == "security"
    assert category(ROOT / "apps" / "web" / "tests" / "example.spec.js") == "web-browser"


def test_expensive_suite_needs_explicit_opt_in():
    suite = next(item for item in manifest() if item["id"] == "e2e")
    args = Namespace(allow_expensive=False, allow_infrastructure=False, base_url="http://127.0.0.1:8000", allow_remote=False)
    assert run_suite(suite, args)["status"] == "blocked"


def test_schema_quality_counts_empty_contracts():
    document = {"paths": {
        "/typed": {"get": {"operationId": "typed", "responses": {"200": {"content": {"application/json": {"schema": {"type": "object"}}}}}}},
        "/empty": {"post": {"operationId": "empty", "responses": {"200": {"content": {"application/json": {"schema": {}}}}}}},
        "/no-content": {"get": {"operationId": "none", "responses": {"200": {"description": "ok"}}}},
    }}
    report = analyze(document)
    assert report["operation_count"] == 3
    assert report["counts_by_reason"] == {"empty_response_schema": 1, "no_response_content": 1}
