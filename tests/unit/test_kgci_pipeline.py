"""Unit tests for the KG CI/CD pipeline (GAP-KGCI-001..004, §30, §16)."""

from __future__ import annotations

import json

import pytest
from eoip.ci import (
    FAIL_ON_BREAKING,
    FAIL_ON_NEVER,
    KGCIPipeline,
    KGCIReport,
    StageStatus,
    run_pipeline,
)
from eoip.ci.pipeline import STAGE_ORDER, main


@pytest.fixture()
def dirs(tmp_path):
    ontology = tmp_path / "ontology"
    ontology.mkdir()
    (ontology / "ontology-v1.yaml").write_text("version: '1.0'\nlabels: [Service]\n", encoding="utf-8")
    gt = tmp_path / "graphtest"
    gt.mkdir()
    contracts = tmp_path / "contracts"
    contracts.mkdir()
    scan = tmp_path / "scan"
    scan.mkdir()
    (scan / "clean.py").write_text("x = 1\n", encoding="utf-8")
    out = tmp_path / "out"
    return {"tmp": tmp_path, "ontology": ontology, "gt": gt, "contracts": contracts, "scan": scan, "out": out}


def _good_contract(path):
    path.write_text(
        json.dumps({"connector": "jira", "entity_type": "WorkItem", "mapping": {"key": "id"}}),
        encoding="utf-8",
    )


def _good_suite(path):
    path.write_text(
        json.dumps({
            "id": "urn:eoip:cicd:suite:basic",
            "name": "basic",
            "assertions": [
                {"id": "a1", "type": "no_orphan", "label": "Service", "relationship": "OWNS"}
            ],
        }),
        encoding="utf-8",
    )


def _baseline(tmp_path, manifest):
    path = tmp_path / "baseline.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def _pass_kwargs(dirs):
    _good_contract(dirs["contracts"] / "jira.json")
    _good_suite(dirs["gt"] / "basic.json")
    return {
        "ontology_dir": dirs["ontology"],
        "graphtest_dir": dirs["gt"],
        "contract_dir": dirs["contracts"],
        "scan_dirs": [dirs["scan"]],
        "output_dir": dirs["out"],
        "version": "9.9.9",
    }


def test_all_stages_present_in_order():
    assert STAGE_ORDER == [
        "lint", "schema_validation", "contract_checks", "graph_invariants",
        "quality_gates", "compatibility", "security", "migration", "publish",
    ]


def test_pass_path_all_stages(dirs):
    report = run_pipeline(**_pass_kwargs(dirs))
    assert isinstance(report, KGCIReport)
    assert report.passed, report.to_dict()
    assert [s.stage for s in report.stages] == STAGE_ORDER
    statuses = {s.stage: s.status for s in report.stages}
    assert statuses["compatibility"] == StageStatus.SKIPPED  # no baseline
    assert statuses["migration"] == StageStatus.SKIPPED
    assert statuses["publish"] == StageStatus.PASSED
    assert report.exit_code() == 0
    # Publish artifact + versioned file emitted (GAP-KGCI-004).
    artifact = dirs["out"] / "ontology-artifacts" / "ontology-9.9.9.json"
    assert artifact.is_file()
    data = json.loads(artifact.read_text(encoding="utf-8"))
    assert data["ontology_version"] == "9.9.9"
    assert data["artifact_type"] == "urn:eoip:cicd:artifact:ontology"


def test_skipped_when_inputs_absent(tmp_path):
    report = run_pipeline(ontology_dir=tmp_path / "missing")
    statuses = {s.stage: s.status for s in report.stages}
    assert statuses["lint"] == StageStatus.SKIPPED
    assert statuses["contract_checks"] == StageStatus.SKIPPED
    assert statuses["graph_invariants"] == StageStatus.SKIPPED
    assert statuses["security"] == StageStatus.SKIPPED
    assert statuses["publish"] == StageStatus.SKIPPED
    assert report.passed


def test_lint_failure_on_bad_yaml(dirs):
    (dirs["ontology"] / "broken.yaml").write_text("a: [unclosed\n", encoding="utf-8")
    report = run_pipeline(**_pass_kwargs(dirs))
    lint = next(s for s in report.stages if s.stage == "lint")
    assert lint.status == StageStatus.FAILED
    assert not report.passed
    assert report.exit_code() == 1


def test_contract_check_failure(dirs):
    (dirs["contracts"] / "bad.json").write_text(json.dumps({"connector": "x"}), encoding="utf-8")
    report = run_pipeline(**_pass_kwargs(dirs))
    contracts = next(s for s in report.stages if s.stage == "contract_checks")
    assert contracts.status == StageStatus.FAILED
    assert "missing keys" in contracts.findings[0].message


def test_graph_invariant_failure(dirs):
    _good_contract(dirs["contracts"] / "jira.json")
    (dirs["gt"] / "fail.json").write_text(
        json.dumps({
            "id": "urn:eoip:cicd:suite:bad",
            "assertions": [
                {"id": "a1", "type": "path_exists", "source_label": "Service",
                 "target_label": "Service", "relationship": "OWNS", "via": []}
            ],
        }),
        encoding="utf-8",
    )
    report = run_pipeline(**_pass_kwargs(dirs))
    inv = next(s for s in report.stages if s.stage == "graph_invariants")
    assert inv.status == StageStatus.FAILED
    assert inv.details["assertions"] == inv.details["assertions_passed"] + 1


def test_quality_gate_slo_breach(dirs):
    kwargs = _pass_kwargs(dirs)
    kwargs["graph_data"] = (
        [{"vid": "v1", "label": "Service", "properties": {}}],
        [],
        [{"severity": "ERROR"}],
    )
    report = run_pipeline(**kwargs)
    quality = next(s for s in report.stages if s.stage == "quality_gates")
    assert quality.status == StageStatus.FAILED
    assert any("error-level findings" in f.message for f in quality.findings)


def test_security_scan_detects_secret(dirs):
    (dirs["scan"] / "leak.py").write_text('api_key = "AKIAIOSFODNN7EXAMPLE"\n', encoding="utf-8")
    report = run_pipeline(**_pass_kwargs(dirs))
    sec = next(s for s in report.stages if s.stage == "security")
    assert sec.status == StageStatus.FAILED
    assert sec.details["files_scanned"] == 2


def test_security_flagged_example_is_generic_secret_too(dirs):
    # Ensure the generic detector alone fires without an AWS-shaped key.
    (dirs["scan"] / "leak.py").write_text('password = "supersecretvalue123"\n', encoding="utf-8")
    report = run_pipeline(**_pass_kwargs(dirs))
    sec = next(s for s in report.stages if s.stage == "security")
    assert sec.status == StageStatus.FAILED
    assert any("generic-secret" in f.message for f in sec.findings)


def test_compatibility_breaking_change(dirs, monkeypatch):
    from eoip.ontology.gitops import current_manifest_snapshot

    baseline = _baseline(dirs["tmp"], current_manifest_snapshot())
    # Remove a vertex label from the "new" manifest to force a breaking diff.
    new = current_manifest_snapshot()
    removed = min(new["vertex_labels"])
    del new["vertex_labels"][removed]
    monkeypatch.setattr("eoip.ontology.gitops.current_manifest_snapshot", lambda: new)
    kwargs = _pass_kwargs(dirs)
    kwargs["baseline_manifest"] = baseline
    report = run_pipeline(**kwargs)
    compat = next(s for s in report.stages if s.stage == "compatibility")
    migration = next(s for s in report.stages if s.stage == "migration")
    assert compat.status == StageStatus.FAILED
    assert migration.details["classification"] == "major"
    assert migration.status == StageStatus.FAILED


def test_compatibility_additive_is_patch(dirs, monkeypatch):
    from eoip.ontology.gitops import current_manifest_snapshot

    new = current_manifest_snapshot()
    base = json.loads(json.dumps(new))
    added = min(new["vertex_labels"])
    base["vertex_labels"].pop(added)  # new has it, baseline does not
    baseline = _baseline(dirs["tmp"], base)
    monkeypatch.setattr("eoip.ontology.gitops.current_manifest_snapshot", lambda: new)
    kwargs = _pass_kwargs(dirs)
    kwargs["baseline_manifest"] = baseline
    report = run_pipeline(**kwargs)
    assert next(s for s in report.stages if s.stage == "compatibility").status == StageStatus.PASSED
    migration = next(s for s in report.stages if s.stage == "migration")
    assert migration.details["classification"] == "patch"
    assert migration.status == StageStatus.PASSED


def test_fail_on_breaking_mode(dirs, monkeypatch):
    from eoip.ontology.gitops import current_manifest_snapshot

    baseline = _baseline(dirs["tmp"], current_manifest_snapshot())
    new = current_manifest_snapshot()
    del new["vertex_labels"][min(new["vertex_labels"])]
    monkeypatch.setattr("eoip.ontology.gitops.current_manifest_snapshot", lambda: new)
    kwargs = _pass_kwargs(dirs)
    kwargs["baseline_manifest"] = baseline
    report = run_pipeline(**kwargs)
    assert report.exit_code() == 1
    report.fail_on = FAIL_ON_NEVER
    assert report.exit_code() == 0
    report.fail_on = FAIL_ON_BREAKING
    assert report.exit_code() == 1
    # breaking mode passes when only non-breaking stages fail
    clean = run_pipeline(**_pass_kwargs(dirs))
    clean.fail_on = FAIL_ON_BREAKING
    clean.stages[0].status = StageStatus.FAILED
    assert clean.exit_code() == 0


def test_fail_on_never_mode(dirs):
    (dirs["ontology"] / "broken.yaml").write_text("a: [unclosed\n", encoding="utf-8")
    report = run_pipeline(**{**_pass_kwargs(dirs), "fail_on": FAIL_ON_NEVER})
    assert not report.passed
    assert report.exit_code() == 0


def test_invalid_fail_on_rejected():
    with pytest.raises(ValueError):
        KGCIPipeline(fail_on="bogus")


def test_report_json_round_trip(dirs):
    report = run_pipeline(**_pass_kwargs(dirs))
    payload = report.to_dict()
    assert payload["passed"] is True
    assert payload["failed_stages"] == []
    assert payload["id"].startswith("urn:eoip:cicd:report:")
    assert len(payload["stages"]) == len(STAGE_ORDER)
    KGCIReport.model_validate(payload)


def test_cli_main_pass_and_report_file(dirs, capsys):
    kwargs = _pass_kwargs(dirs)
    code = main([
        "--ontology-dir", str(kwargs["ontology_dir"]),
        "--graphtest-dir", str(kwargs["graphtest_dir"]),
        "--contract-dir", str(kwargs["contract_dir"]),
        "--scan-dirs", str(kwargs["scan_dirs"][0]),
        "--output-dir", str(kwargs["output_dir"]),
        "--version", "1.2.3",
        "--report", str(dirs["out"] / "report.json"),
    ])
    assert code == 0
    written = json.loads((dirs["out"] / "report.json").read_text(encoding="utf-8"))
    assert written["passed"] is True
    out = capsys.readouterr().out
    assert '"passed": true' in out


def test_cli_main_fail_exit_code(dirs, capsys):
    (dirs["ontology"] / "broken.yaml").write_text("x: [unclosed\n", encoding="utf-8")
    code = main(["--ontology-dir", str(dirs["ontology"]), "--scan-dirs", str(dirs["scan"])])
    assert code == 1
    out = capsys.readouterr().out
    assert '"passed": false' in out
