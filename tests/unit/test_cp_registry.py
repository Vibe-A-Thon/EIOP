"""CP-00 regression cases: incomplete evidence must never close requirements."""

import copy
import json
from pathlib import Path

import pytest
from eoip.verification.cp_registry import (
    Implementation,
    load_audit,
    load_registry,
    load_routing,
    migrate_registry,
    validate_registry,
)

pytestmark = pytest.mark.req("BASE-01", "BASE-04")


@pytest.fixture()
def audit_project(tmp_path):
    (tmp_path / "source.md").write_text("# Source\n| R-1 | A complete requirement |\n", encoding="utf-8")
    cells = ["`REQ-API-001`", "`R-1`: A requirement with \\| an embedded pipe", "`source.md:2`",
             "`functional`", "`P3`", "Expected behavior", "`MISSED`", "`none`", "`none`",
             "Missing integration", "`UNKNOWN`", "`HIGH`", "`M`", "Not stated", "Implement and verify"]
    (tmp_path / "gaps-audit-cp.md").write_text("| " + " | ".join(cells) + " |\n", encoding="utf-8")
    (tmp_path / "gaps-audit-cp-implementation-plan.md").write_text(
        "| `REQ-API-001` | title | source | P3 | MISSED | [CP-07](#cp-07) | explicit | TRACE/BUILD |\n",
        encoding="utf-8",
    )
    return tmp_path


def _load(root):
    return load_audit(root, expected_sha256=None, expected_count=1)


def test_import_preserves_every_audit_column_and_escaped_pipes(audit_project):
    row = _load(audit_project)[0]
    baseline = row["audit_baseline"]
    assert row["id"] == "R-1"
    assert "\\|" in baseline["requirement"]
    assert baseline["priority"] == "`P3`"
    assert baseline["source_line_text"] == "| R-1 | A complete requirement |"
    assert len(baseline["source_sha256"]) == 64
    assert load_routing(audit_project, [row]) == {"REQ-API-001": "CP-07"}


def test_migration_keeps_legacy_ids_and_metadata_without_claiming_completion(audit_project):
    audit = _load(audit_project)
    legacy = [{"id": "R-1", "status": "FULLY_DEVELOPED", "code_paths": ["x.py"],
               "test_files": ["test_x.py"], "evidence_receipt": "tests_passed=True"},
              {"id": "LEGACY-ONLY", "custom": {"keep": True}, "status": "ROADMAP"}]
    result = migrate_registry(legacy, audit, {"REQ-API-001": "CP-07"})
    assert legacy[0]["status"] == "FULLY_DEVELOPED"
    imported = next(r for r in result if r["id"] == "R-1")
    assert imported["legacy_claims"]["status"] == "FULLY_DEVELOPED"
    assert imported["status"] == "UNTRIAGED"
    assert "evidence_receipt" not in imported
    assert imported["code_paths"] == ["x.py"]
    assert result[0]["custom"] == {"keep": True}
    assert result == migrate_registry(result, audit, {"REQ-API-001": "CP-07"})
    assert validate_registry(audit_project, result, audit)["valid"]


@pytest.mark.parametrize("corruption", ["duplicate", "column", "source-line", "traversal", "missing-source"])
def test_audit_rejects_ambiguous_or_unsafe_input(audit_project, corruption):
    path = audit_project / "gaps-audit-cp.md"
    text = path.read_text()
    if corruption == "duplicate":
        text += text
    elif corruption == "column":
        text = text.replace(" | `HIGH`", " | accidental | `HIGH`")
    elif corruption == "source-line":
        text = text.replace("source.md:2", "source.md:200")
    elif corruption == "traversal":
        text = text.replace("source.md:2", "../outside.md:2")
    else:
        (audit_project / "source.md").unlink()
    path.write_text(text)
    with pytest.raises(ValueError):
        _load(audit_project)


def test_baseline_hash_and_count_are_enforced(audit_project):
    with pytest.raises(ValueError, match="digest"):
        load_audit(audit_project)
    with pytest.raises(ValueError, match="count"):
        load_audit(audit_project, expected_sha256=None)


def test_document_hashes_are_stable_across_checkout_line_endings(audit_project):
    before = _load(audit_project)
    for name in ("source.md", "gaps-audit-cp.md"):
        path = audit_project / name
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert _load(audit_project) == before


def test_plan_must_cover_exact_audit_set(audit_project):
    path = audit_project / "gaps-audit-cp-implementation-plan.md"
    path.write_text(path.read_text().replace("REQ-API-001", "REQ-API-002"))
    with pytest.raises(ValueError, match="exact audit"):
        load_routing(audit_project, _load(audit_project))


@pytest.mark.parametrize("state", ["READY", "IMPLEMENTED", "INTEGRATION_VERIFIED", "VERIFIED"])
def test_checkbox_status_without_source_review_and_evidence_is_rejected(audit_project, state):
    audit = _load(audit_project)
    records = migrate_registry([], audit, {"REQ-API-001": "CP-07"})
    records[0]["implementation"]["state"] = state
    records[0]["status"] = state
    report = validate_registry(audit_project, records, audit)
    assert not report["valid"]
    assert "source review" in report["errors"][0]


def test_missing_and_altered_audit_records_fail_validation(audit_project):
    audit = _load(audit_project)
    assert not validate_registry(audit_project, [], audit)["valid"]
    records = migrate_registry([], audit, {"REQ-API-001": "CP-07"})
    records[0]["audit_baseline"]["gap"] = "silently changed"
    assert not validate_registry(audit_project, records, _load(audit_project))["valid"]


def test_source_changes_require_explicit_reconciliation(audit_project):
    original = _load(audit_project)
    records = migrate_registry([], original, {"REQ-API-001": "CP-07"})
    (audit_project / "source.md").write_text("# Updated\nDifferent requirement\n")
    with pytest.raises(ValueError, match="baseline changed"):
        migrate_registry(records, _load(audit_project), {"REQ-API-001": "CP-07"})


def test_alias_cycles_and_duplicate_clauses_are_rejected(audit_project):
    audit = _load(audit_project)
    records = migrate_registry([], audit, {"REQ-API-001": "CP-07"})
    records[0]["implementation"].update(classification="ALIAS", canonical_id="R-1", disposition_reason="self")
    assert "cyclic" in validate_registry(audit_project, records, audit)["errors"][0]
    records[0]["implementation"] = Implementation(primary_package="CP-07").model_dump()
    clause = {"id": "AC01", "outcome": "real behavior", "test_node_ids": []}
    records[0]["implementation"]["acceptance_clauses"] = [clause, copy.deepcopy(clause)]
    assert "duplicate acceptance" in validate_registry(audit_project, records, audit)["errors"][0]


def test_registry_loader_rejects_duplicate_ids(audit_project):
    path = audit_project / "registry.json"
    path.write_text(json.dumps([{"id": "x"}, {"id": "x"}]))
    with pytest.raises(ValueError, match="duplicate"):
        load_registry(path)


def test_real_registry_roundtrip_is_bounded_and_independent_of_git_history(tmp_path):
    from eoip.jobs import write_json
    from eoip.verification.cp_registry import MAX_DOCUMENT_BYTES

    root = Path(__file__).resolve().parents[2]
    audit = load_audit(root)
    routing = load_routing(root, audit)
    records = load_registry(root / "requirements-registry.json")
    migrated = migrate_registry(records, audit, routing)
    target = tmp_path / "registry.json"
    write_json(target, migrated, indent=2)
    assert target.stat().st_size < MAX_DOCUMENT_BYTES
    assert load_registry(target) == migrated
    assert migrated == migrate_registry(migrated, load_audit(root), routing)
    assert len(audit) == 2603


def test_registry_source_uses_pinned_snapshot_not_current_output(audit_project, monkeypatch):
    from eoip.verification import cp_registry

    baseline = audit_project / cp_registry.REGISTRY_BASELINE_FILE
    baseline.parent.mkdir(parents=True)
    baseline.write_bytes(b'[{"id": "R-1"}]\n')
    monkeypatch.setattr(cp_registry, "REGISTRY_BASELINE_SHA256", cp_registry.digest(baseline.read_bytes()))
    audit = audit_project / "gaps-audit-cp.md"
    audit.write_text(audit.read_text().replace("source.md:2", "requirements-registry.json:1"))
    first = _load(audit_project)
    (audit_project / "requirements-registry.json").write_text('[]')
    assert _load(audit_project) == first
    baseline.write_text('[]')
    with pytest.raises(ValueError, match="baseline digest"):
        _load(audit_project)
    baseline.unlink()
    with pytest.raises(ValueError, match="Missing referenced"):
        _load(audit_project)
