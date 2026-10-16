"""Ontology GitOps semantic diff (GAP-GITOPS-001..008)."""

from eoip.ontology.gitops import (
    current_manifest_snapshot,
    diff_manifests,
    validate_ontology_change,
)


def _base():
    return current_manifest_snapshot()


def test_identical_manifests_have_no_changes():
    result = validate_ontology_change(_base(), _base())
    assert result["publishable"] is True
    assert result["counts"]["total"] == 0
    assert result["verdict"] == "PUBLISH_OK"


def test_additive_changes_are_publishable():
    new = _base()
    new["vertex_labels"]["Widget"] = {"domain": "CODE", "required": ["canonical_id"], "optional": []}
    new["property_keys"]["widget_size"] = "TEXT"
    result = validate_ontology_change(_base(), new)
    assert result["publishable"] is True
    kinds = {change["change_type"] for change in result["changes"]}
    assert "vertex_label_added" in kinds
    assert "property_key_added" in kinds


def test_removed_label_is_breaking_and_refused():
    new = _base()
    removed = min(new["vertex_labels"])
    del new["vertex_labels"][removed]
    result = validate_ontology_change(_base(), new)
    assert result["publishable"] is False
    assert result["verdict"] == "BREAKING_CHANGE_REFUSED"
    change = next(c for c in result["changes"] if c["change_type"] == "vertex_label_removed")
    assert change["subject"] == removed
    assert change["classification"] == "breaking"


def test_tightened_required_property_is_flagged():
    new = _base()
    label = min(new["vertex_labels"])
    new["vertex_labels"][label]["required"] = sorted(
        [*new["vertex_labels"][label]["required"], "summary"]
    )
    result = diff_manifests(_base(), new)
    change = next(c for c in result.changes if c.change_type == "required_property_added")
    assert change.classification == "potentially_breaking"


def test_edge_endpoint_narrowing_is_flagged():
    new = _base()
    edge = min(new["edge_labels"])
    new["edge_labels"][edge]["out"] = new["edge_labels"][edge]["out"][:-1]
    result = diff_manifests(_base(), new)
    change = next(c for c in result.changes if c.change_type == "edge_endpoints_narrowed")
    assert change.classification == "potentially_breaking"


def test_property_type_change_is_flagged():
    new = _base()
    key = min(new["property_keys"])
    new["property_keys"][key] = "INT"
    result = diff_manifests(_base(), new)
    change = next(c for c in result.changes if c.change_type == "property_type_changed")
    assert change.subject == key


def test_cli_refuses_breaking_change(tmp_path, capsys):
    from scripts.ontology_diff import main as cli_main

    new = _base()
    del new["property_keys"][min(new["property_keys"])]
    old_path = tmp_path / "old.json"
    new_path = tmp_path / "new.json"
    old_path.write_text(__import__("json").dumps(_base()), encoding="utf-8")
    new_path.write_text(__import__("json").dumps(new), encoding="utf-8")
    assert cli_main([str(old_path), str(new_path)]) == 1
    assert "BREAKING_CHANGE_REFUSED" in capsys.readouterr().out


def test_cli_accepts_additive_change():
    from scripts.ontology_diff import main as cli_main

    assert cli_main(["-", "-"]) == 0
