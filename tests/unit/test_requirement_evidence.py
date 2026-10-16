import csv
import json

import pytest

from scripts import verify_requirement_evidence as evidence_script
from scripts.verify_requirement_evidence import verify_requirement_evidence


def _inputs(root, *, decorators='@pytest.mark.req("FR-GRAPH-001")', outcome=""):
    source = root / "tests" / "unit" / "test_example.py"
    source.parent.mkdir(parents=True)
    source.write_text(f"import pytest\n\n{decorators}\ndef test_example():\n    pass\n", encoding="utf-8")
    matrix = root / "matrix.csv"
    with matrix.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["mvp_requirement", "title", "parent_requirements", "implementation_task"])
        for index in range(1, 29):
            writer.writerow([
                f"MVP-FR-{index:03d}", f"Requirement {index}", f"FR-GRAPH-{index:03d}", f"T{index:02d}",
            ])
    junit = root / "results.xml"
    junit.write_text(
        '<testsuites><testsuite tests="1">'
        '<testcase classname="tests.unit.test_example" name="test_example[one]">'
        f"{outcome}</testcase></testsuite></testsuites>", encoding="utf-8",
    )
    return matrix, junit, source


def test_reports_actual_passes_without_claiming_application_completion(tmp_path):
    matrix, junit, source = _inputs(tmp_path)
    result = verify_requirement_evidence(tmp_path, matrix, junit)
    assert result["status"] == "EVIDENCE_GAPS"
    assert result["requirements_with_passing_evidence"] == 1
    assert result["declared_requirements"] == 28
    assert result["requirements"][0]["evidence_status"] == "PASSING_TESTS"
    assert result["requirements"][1]["evidence_status"] == "MISSING"
    assert result["source_hashes"]["tests/unit/test_example.py"]
    assert result["receipt_sha256"]
    assert result["application_completion_percent"] is None
    assert result["source_revision_bound"] is False
    assert source.exists()
    json.dumps(result)


@pytest.mark.parametrize(("outcome", "status"), [
    ("<failure/>", "FAIL"), ("<error/>", "FAIL"), ("<skipped/>", "SKIPPED"),
])
def test_failed_or_skipped_cases_do_not_close_requirements(tmp_path, outcome, status):
    matrix, junit, _ = _inputs(tmp_path, outcome=outcome)
    result = verify_requirement_evidence(tmp_path, matrix, junit)
    assert result["requirements"][0]["evidence_status"] == status
    assert result["requirements_with_passing_evidence"] == 0


def test_all_parent_requirements_need_evidence(tmp_path):
    matrix, junit, _ = _inputs(tmp_path)
    matrix.write_text(
        matrix.read_text().replace("FR-GRAPH-001,T01", '"FR-GRAPH-001,FR-CODE-001",T01'),
        encoding="utf-8",
    )
    result = verify_requirement_evidence(tmp_path, matrix, junit)
    first = result["requirements"][0]
    assert first["evidence_status"] == "PARTIAL"
    assert first["missing_parent_requirements"] == ["FR-CODE-001"]
    assert result["requirements_with_passing_evidence"] == 0


def test_requirement_marker_inheritance_and_parameter_failures(tmp_path):
    matrix, junit, source = _inputs(tmp_path)
    source.write_text(
        'import pytest\npytestmark = pytest.mark.req("MVP-FR-001")\n'
        'class TestExample:\n    def test_example(self):\n        pass\n',
        encoding="utf-8",
    )
    junit.write_text(
        '<testsuites><testsuite tests="2">'
        '<testcase classname="tests.unit.test_example.TestExample" name="test_example[one]"/>'
        '<testcase classname="tests.unit.test_example.TestExample" name="test_example[two]">'
        '<failure/></testcase></testsuite></testsuites>', encoding="utf-8",
    )
    result = verify_requirement_evidence(tmp_path, matrix, junit)
    assert result["requirements"][0]["evidence_status"] == "FAIL"


@pytest.mark.parametrize("corruption", ["missing-row", "duplicate-row", "empty", "truncated", "duplicate-case", "doctype"])
def test_refuses_incomplete_or_ambiguous_evidence(tmp_path, corruption):
    matrix, junit, _ = _inputs(tmp_path)
    if corruption == "missing-row":
        matrix.write_text("\n".join(matrix.read_text().splitlines()[:-1]), encoding="utf-8")
    elif corruption == "duplicate-row":
        matrix.write_text(matrix.read_text() + matrix.read_text().splitlines()[1] + "\n", encoding="utf-8")
    elif corruption == "empty":
        junit.write_text("<testsuites/>", encoding="utf-8")
    elif corruption == "truncated":
        junit.write_text(junit.read_text().replace('tests="1"', 'tests="2"'), encoding="utf-8")
    elif corruption == "duplicate-case":
        content = junit.read_text()
        start, end = content.index("<testcase"), content.index("</testcase>") + len("</testcase>")
        junit.write_text(content.replace("</testsuite>", content[start:end] + "</testsuite>"), encoding="utf-8")
    else:
        junit.write_text('<!DOCTYPE testsuites [<!ENTITY x "unsafe">]><testsuites/>', encoding="utf-8")
    with pytest.raises(ValueError):
        verify_requirement_evidence(tmp_path, matrix, junit)


def test_refuses_dynamic_requirement_annotations(tmp_path):
    matrix, junit, _ = _inputs(tmp_path, decorators='@pytest.mark.req("FR-GRAPH-" + "001")')
    with pytest.raises(ValueError, match="literal"):
        verify_requirement_evidence(tmp_path, matrix, junit)


def test_unrelated_failure_prevents_a_green_evidence_verdict(tmp_path):
    decorators = "@pytest.mark.req(" + ", ".join(
        f'"MVP-FR-{index:03d}"' for index in range(1, 29)
    ) + ")"
    matrix, junit, _ = _inputs(tmp_path, decorators=decorators)
    junit.write_text(
        junit.read_text().replace('tests="1"', 'tests="2"').replace(
            "</testsuite>", '<testcase classname="other" name="test_failure"><failure/></testcase></testsuite>',
        ), encoding="utf-8",
    )
    result = verify_requirement_evidence(tmp_path, matrix, junit)
    assert result["requirements_with_passing_evidence"] == 28
    assert result["status"] == "EVIDENCE_GAPS"
    assert result["failed_or_error_cases"] == 1


def test_cli_persists_gaps_and_returns_failure(monkeypatch, tmp_path):
    matrix, junit, _ = _inputs(tmp_path)
    output = tmp_path / "receipts" / "requirements.json"
    monkeypatch.setattr("sys.argv", [
        "verify_requirement_evidence", str(tmp_path), str(matrix), str(junit), "--output", str(output),
    ])
    with pytest.raises(SystemExit) as exc:
        evidence_script.main()
    assert exc.value.code == 1
    assert json.loads(output.read_text())["status"] == "EVIDENCE_GAPS"


def test_refuses_test_sources_outside_the_project(tmp_path, monkeypatch):
    matrix, junit, source = _inputs(tmp_path)
    original = type(source).resolve

    def resolve(path, *args, **kwargs):
        if path == source:
            return tmp_path.parent / "outside.py"
        return original(path, *args, **kwargs)

    monkeypatch.setattr(type(source), "resolve", resolve)
    with pytest.raises(ValueError, match="test directory"):
        verify_requirement_evidence(tmp_path, matrix, junit)
