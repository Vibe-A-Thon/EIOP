"""Guard the completeness inventory against false claims of coverage."""

from qa.completeness import coverage_status, mcp_tools, source_files
from qa.postman.build_api_catalog import collection


def test_catalog_lists_every_operation_but_cannot_execute_it():
    document = {
        "paths": {
            "/a/{identifier}": {
                "get": {"operationId": "read_a", "responses": {"200": {}}},
                "delete": {"operationId": "delete_a", "requestBody": {}, "responses": {"204": {}}},
            },
        },
    }
    result = collection(document)
    items = [item for group in result["item"] for item in group["item"]]
    assert {(item["request"]["method"], item["name"]) for item in items} == {
        ("GET", "GET /a/{identifier}"), ("DELETE", "DELETE /a/{identifier}")
    }
    assert all("{{qa_identifier}}" in item["request"]["url"]["raw"] for item in items)
    assert "pm.execution.skipRequest();" in result["event"][0]["script"]["exec"]
    assert all(item["response"] == [] for item in items)


def test_source_inventory_excludes_tests_and_build_artifacts(tmp_path):
    for name in (
        "packages/eoip/core.py", "packages/eoip/test_core.py", "apps/web/src/view.tsx",
        "apps/web/src/view.test.ts", "apps/vscode-extension/dist/bundle.js",
    ):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("pass\n", encoding="utf-8")
    python, web = source_files(tmp_path)
    assert python == ["packages/eoip/core.py"]
    assert web == ["apps/web/src/view.tsx"]


def test_mcp_tool_inventory_follows_registration_not_a_manual_count(tmp_path):
    source = tmp_path / "mcp.py"
    source.write_text("@mcp.tool()\nasync def alpha():\n    pass\n", encoding="utf-8")
    assert mcp_tools(source) == ["alpha"]


def test_missing_coverage_is_unverified_not_a_pass():
    assert coverage_status("packages/eoip/core.py", None)["status"] == "unmeasured"
    report = {"files": {"packages/eoip/core.py": {"summary": {
        "num_statements": 10, "missing_lines": 1,
        "num_branches": 2, "missing_branches": 0,
    }}}, "meta": {"branch_coverage": True}}
    assert coverage_status("packages/eoip/core.py", report)["status"] == "partially_measured"
    report["files"]["packages/eoip/core.py"]["summary"]["missing_lines"] = 0
    assert coverage_status("packages/eoip/core.py", report)["status"] == "line_and_branch_measured"
    report["meta"]["branch_coverage"] = False
    assert coverage_status("packages/eoip/core.py", report)["status"] == "line_only_measured"
