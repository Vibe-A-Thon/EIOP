"""Acceptance tests for conservative, complete mechanical documentation scanning."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.documentation_audit import build_audit, main, recorded_runtime_progress, render_markdown


@pytest.fixture
def repository(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "fixture@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "Audit Fixture"], check=True)
    (tmp_path / "README.md").write_text("# Scope\nREQ-001: MUST preserve evidence.\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "Original fixture"], check=True, capture_output=True)
    return tmp_path


def create(root, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_runtime_progress_records_failures_skips_and_missing_receipts(repository):
    create(repository, "test-results/enterprise-search-focused-junit.xml", """<testsuites>
      <testsuite><testcase/><testcase><failure/></testcase>
      <testcase><error/></testcase><testcase><skipped/></testcase></testsuite>
    </testsuites>""")
    create(repository, "demo/demodata/enterprise/scenario-pack.json", json.dumps({
        "version": "test", "scenarios": [{}], "vertices": [{}, {}], "edges": [{}],
    }))
    create(repository, "test-results/enterprise-whatif-source-junit.xml",
           "<testsuites><testsuite><testcase/></testsuite></testsuites>")
    create(repository, "test-results/enterprise-code-ingestion-final-junit.xml",
           "<testsuites><testsuite><testcase/></testsuite></testsuites>")
    progress = recorded_runtime_progress(repository)
    assert progress["seed"] == {
        "version": "test", "scenarios": 1, "entities": 2, "relationships": 1,
    }
    receipt = progress["receipts"][1]
    assert receipt["status"] == "RECORDED_FAILURE"
    assert [receipt[key] for key in ("passed", "failed", "errors", "skipped")] == [1, 1, 1, 1]
    assert len(receipt["sha256"]) == 64
    assert progress["receipts"][2]["status"] == "UNVERIFIED"
    assert progress["receipts"][-1]["status"] == "RECORDED_PASS"
    assert progress["receipts"][-1]["passed"] == 1
    assert progress["receipts"][-2]["status"] == "UNVERIFIED"


@pytest.mark.req("REQ-001", "REQ-002")
def test_nested_kgr_and_unnumbered_obligations_are_read(repository):
    create(repository, "EOIP-engg-doc-pkg/KGR-requirements.md", "FR-KGR-001: SHALL render.\nMUST bound queries.\n")
    create(repository, "nested/deep/readme.txt", "All lines\nincluding the final line")
    report = build_audit(repository)
    assert report["counts"]["documents"] == 3
    assert report["counts"]["document_lines"] == 6
    assert {row["requirement_id"] for row in report["requirements"]} >= {"REQ-001", "FR-KGR-001"}
    assert any(row["record_type"] == "unnumbered_obligation_candidate" for row in report["requirements"])
    assert all(row["mechanical_read"] == "complete" and row["semantic_review"] == "pending"
               for row in report["documents"])


@pytest.mark.req("REQ-003")
def test_mentions_never_establish_acceptance(repository):
    create(repository, "packages/logic.py", "# REQ-001 implemented\n")
    create(repository, "tests/test_logic.py", "# REQ-001 accepted\n")
    report = build_audit(repository)
    row = next(row for row in report["requirements"] if row["requirement_id"] == "REQ-001")
    assert row["implementation_status"] == "Partial"
    assert not row["acceptance_verified"]
    assert row["implementation_leads"][0]["line"] == 1
    assert row["test_leads"][0]["kind"] == "identifier_occurrence"
    assert "No global completion" in render_markdown(report)


@pytest.mark.req("REQ-004")
def test_audit_tooling_is_reported_as_phase_evidence_not_acceptance(repository):
    create(repository, "EOIP-engg-doc-pkg/audits/generated/phase-1-spec.md", "REQ-004: persist reports.\n")
    create(repository, "scripts/documentation_audit.py", "# REQ-004 implementation lead\n")
    create(repository, "tests/unit/test_documentation_audit.py", "# REQ-004 test lead\n")

    report = build_audit(repository)
    row = next(row for row in report["requirements"] if row["requirement_id"] == "REQ-004")

    assert row["implementation_status"] == "Partial"
    assert not row["acceptance_verified"]
    assert row["implementation_leads"][0]["path"] == "scripts/documentation_audit.py"
    assert row["test_leads"][0]["path"] == "tests/unit/test_documentation_audit.py"


@pytest.mark.req("REQ-001")
def test_secrets_dependencies_reports_and_ignored_files_are_not_read(repository):
    for name in [
        "secrets.example/api-token.txt", "node_modules/library/readme.md",
        "EOIP-engg-doc-pkg/audits/generated/current-gap-report.md", "test-results/report.txt",
    ]:
        create(repository, name, "invalid encoding placeholder")
        (repository / name).write_bytes(b"\xff")
    create(repository, ".gitignore", "ignored/\n")
    create(repository, "ignored/private.md", "MUST NOT be included")
    report = build_audit(repository)
    assert report["counts"]["documents"] == 1
    assert len(report["excluded"]) == 4
    assert all(not entry["content_read"] for entry in report["excluded"])


@pytest.mark.req("REQ-001", "REQ-002")
def test_historical_reports_are_read_but_not_recursive_obligations(repository):
    create(repository, "EOIP-engg-doc-pkg/audits/generated/gap-report.md", "REQ-999 MUST be historical only.\n")
    report = build_audit(repository)
    assert report["counts"]["documents"] == 2
    assert "REQ-999" not in {row["requirement_id"] for row in report["requirements"]}
    history = next(row for row in report["documents"] if row["path"].endswith("gap-report.md"))
    assert history["mechanical_read"] == "complete"
    assert history["role"] == "historical_audit_evidence"


@pytest.mark.req("REQ-001")
def test_invalid_encoding_fails_instead_of_claiming_complete(repository):
    (repository / "bad.txt").write_bytes(b"\xff")
    with pytest.raises(UnicodeDecodeError):
        build_audit(repository)


@pytest.mark.req("REQ-004")
def test_cli_persists_consistent_json_and_markdown(repository):
    assert main(["--project-root", str(repository)]) == 0
    directory = repository / "EOIP-engg-doc-pkg" / "audits" / "generated"
    report = json.loads((directory / "current-gap-report.json").read_text(encoding="utf-8"))
    inventory = json.loads((directory / "documentation-inventory.json").read_text(encoding="utf-8"))
    assert inventory["documents"] == report["documents"]
    assert not inventory["semantic_review_complete"]
    assert (directory / "current-gap-report.md").read_text(encoding="utf-8") == render_markdown(report)
    assert main(["--project-root", str(repository)]) == 0
    refreshed = json.loads((directory / "current-gap-report.json").read_text(encoding="utf-8"))
    assert refreshed["documents"] == report["documents"]
    assert refreshed["requirements"] == report["requirements"]


@pytest.mark.req("REQ-004")
def test_cli_cannot_overwrite_source_directory(repository):
    with pytest.raises(SystemExit):
        main(["--project-root", str(repository), "--output-directory", str(repository)])


@pytest.mark.req("REQ-001", "REQ-004")
def test_oversized_input_does_not_write_receipts(repository, monkeypatch):
    monkeypatch.setattr("scripts.documentation_audit.MAX_FILE_BYTES", 1)
    with pytest.raises(ValueError, match="file budget"):
        main(["--project-root", str(repository)])
    assert not (repository / "EOIP-engg-doc-pkg" / "audits" / "generated").exists()


@pytest.mark.req("REQ-001")
def test_total_input_budget_is_enforced(repository, monkeypatch):
    monkeypatch.setattr("scripts.documentation_audit.MAX_TOTAL_BYTES", 1)
    with pytest.raises(ValueError, match="total byte budget"):
        build_audit(repository)


@pytest.mark.req("REQ-001", "REQ-004")
def test_symlink_inputs_and_outputs_are_refused(repository, monkeypatch):
    original = Path.is_symlink
    input_path = repository / "README.md"
    monkeypatch.setattr(Path, "is_symlink", lambda path: path == input_path or original(path))
    with pytest.raises(ValueError, match="symlink input"):
        build_audit(repository)
    output_path = repository / "EOIP-engg-doc-pkg" / "audits" / "generated" / "current-gap-report.md"
    monkeypatch.setattr(Path, "is_symlink", lambda path: path == output_path or original(path))
    with pytest.raises(SystemExit):
        main(["--project-root", str(repository)])
    assert not output_path.parent.exists()


@pytest.mark.req("REQ-005")
def test_ci_installs_native_parser_extra():
    root = Path(__file__).resolve().parents[2]
    workflow = (root / ".github" / "workflows" / "validation-evidence.yml").read_text(encoding="utf-8")
    action = (root / ".github" / "actions" / "setup-eoip-python" / "action.yml").read_text(encoding="utf-8")
    # FT-F04/FT-F06: CI uses the documented install; the 'test' extra must keep
    # pulling in the native parser extras. CI-PERF moved the install into the shared setup
    # action (uv, pip fallback): both commands keep the lock constraints, and the extras
    # default to 'test' and are never narrowed by the workflow.
    import yaml
    assert "uses: ./.github/actions/setup-eoip-python" in workflow
    assert "extras:" not in workflow
    assert yaml.safe_load(action)["inputs"]["extras"]["default"] == "test"
    assert 'uv pip install --system --python "$py" -c requirements.lock -e "$spec"' in action
    assert 'python -m pip install -c requirements.lock -e "$spec"' in action
    assert "python -X utf8 -m pytest -q" in workflow
    import tomllib
    extras = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]["optional-dependencies"]
    bundled = extras["test"][0]
    for name in ("dev", "codeparse", "fileparse"):
        assert name in bundled.split("[", 1)[1], bundled


@pytest.mark.req("REQ-004")
def test_real_cli_subprocess_and_bad_destination(repository):
    result = subprocess.run(
        [sys.executable, "-m", "scripts.documentation_audit", "--project-root", str(repository)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["documents"] == 1
    bad = subprocess.run(
        [sys.executable, "-m", "scripts.documentation_audit", "--project-root", str(repository),
         "--output-directory", str(repository)],
        capture_output=True, text=True, check=False,
    )
    assert bad.returncode == 2
    assert "output directory must be" in bad.stderr
