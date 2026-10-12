"""Knowledge Capsules (G2-CAP-001..006)."""

import pytest
from eoip.graph.capsules import CapsuleDefinition, KnowledgeCapsuleService
from eoip.graph.memory import MemoryGraphStore


def _store() -> MemoryGraphStore:
    store = MemoryGraphStore()
    store.ensure_schema({})
    store.upsert_vertex(
        "WorkItem",
        {"canonical_id": "w:1", "issue_key": "EOIP-1", "summary": "Root item"},
    )
    store.upsert_vertex(
        "CodeSymbol",
        {
            "canonical_id": "s:1",
            "qualified_name": "demo.compute_impact",
            "symbol_kind": "function",
        },
    )
    store.upsert_vertex(
        "CodeSymbol",
        {
            "canonical_id": "s:2",
            "qualified_name": "demo.helper",
            "symbol_kind": "function",
        },
    )
    w = store.get_vertex_by_canonical_id("w:1")
    s1 = store.get_vertex_by_canonical_id("s:1")
    s2 = store.get_vertex_by_canonical_id("s:2")
    store.upsert_edge(
        "REFERENCES",
        w["vid"],
        s1["vid"],
        {"fact_key": "f:1", "source_ref": "git://demo/commit/abc", "creation_status": "DETERMINISTIC"},
    )
    store.upsert_edge(
        "CALLS",
        s1["vid"],
        s2["vid"],
        {"fact_key": "f:2", "creation_status": "INFERRED"},
    )
    return store


def test_capsule_builds_bounded_context_with_evidence(tmp_path):
    service = KnowledgeCapsuleService(_store(), tmp_path)
    capsule = service.build(
        CapsuleDefinition(name="release", root_entities=("w:1",), max_depth=2)
    )

    ids = {entity["canonical_id"] for entity in capsule.entities}
    assert {"w:1", "s:1", "s:2"} <= ids
    assert any(rel["source_ref"] == "git://demo/commit/abc" for rel in capsule.relationships)
    assert "git://demo/commit/abc" in capsule.evidence_refs
    assert capsule.manifest["counts"]["entities"] == len(capsule.entities)
    assert capsule.capsule_id and capsule.graph_fingerprint


@pytest.mark.req("G2-CAP-002")
def test_capsule_is_reproducible_g2_cap_002(tmp_path):
    store = _store()
    service = KnowledgeCapsuleService(store, tmp_path)
    first = service.build(CapsuleDefinition(name="rel", root_entities=("w:1",)))
    second = service.build(CapsuleDefinition(name="rel", root_entities=("w:1",)))
    assert first.capsule_id == second.capsule_id
    assert first.graph_fingerprint == second.graph_fingerprint


@pytest.mark.req("G2-CAP-003")
def test_capsule_reduces_context_exposure_g2_cap_003(tmp_path):
    service = KnowledgeCapsuleService(_store(), tmp_path)
    # Bounded depth and trust filter limits exposure
    capsule = service.build(
        CapsuleDefinition(
            name="trusted", root_entities=("w:1",), max_depth=1, trust_threshold="DETERMINISTIC"
        )
    )
    trusts = {rel["trust"] for rel in capsule.relationships}
    assert trusts == {"DETERMINISTIC"}
    assert all(rel["type"] != "CALLS" for rel in capsule.relationships)
    # Target entity s:2 at depth 2 is not exposed
    cids = {e["canonical_id"] for e in capsule.entities}
    assert "s:2" not in cids


@pytest.mark.req("G2-CAP-004")
def test_capsule_includes_manifest_and_evidence_g2_cap_004(tmp_path):
    service = KnowledgeCapsuleService(_store(), tmp_path)
    capsule = service.build(
        CapsuleDefinition(name="release_manifest", root_entities=("w:1",), max_depth=2, include_evidence=True)
    )
    assert capsule.manifest is not None
    assert capsule.manifest["capsule_id"] == capsule.capsule_id
    assert "git://demo/commit/abc" in capsule.manifest["evidence_refs"]
    assert "git://demo/commit/abc" in capsule.evidence_refs


@pytest.mark.req("G2-CAP-005")
def test_capsule_example_types_g2_cap_005(tmp_path):
    from eoip.graph.capsules import EXAMPLE_CAPSULE_TYPES, create_example_capsule_definition
    service = KnowledgeCapsuleService(_store(), tmp_path)

    for cap_type in ("release", "incident", "service", "application", "change_request", "architecture_review", "audit_evidence"):
        assert cap_type in EXAMPLE_CAPSULE_TYPES
        definition = create_example_capsule_definition(cap_type, root_entities=("w:1",), max_depth=2)
        capsule = service.build(definition)
        assert capsule.definition["name"] == cap_type
        assert len(capsule.entities) >= 1

    with pytest.raises(ValueError, match="Unsupported example capsule type"):
        create_example_capsule_definition("unknown_type", root_entities=("w:1",))


@pytest.mark.req("G2-CAP-006")
def test_capsule_export_package_format_g2_cap_006(tmp_path):
    import json
    service = KnowledgeCapsuleService(_store(), tmp_path)
    service.build(CapsuleDefinition(name="exportable", root_entities=("w:1",)))

    export_path = tmp_path / "exported" / "exportable.pkg.json"
    result_path = service.export_package("exportable", output_path=export_path)

    assert result_path.exists()
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    assert payload["package_format"] == "eoip-capsule-package/1.0"
    assert "manifest" in payload
    assert "payload" in payload
    assert len(payload["payload"]["entities"]) > 0


def test_capsule_validates_definition(tmp_path):
    service = KnowledgeCapsuleService(_store(), tmp_path)
    with pytest.raises(ValueError, match="at least one root"):
        service.build(CapsuleDefinition(name="x", root_entities=()))
    with pytest.raises(ValueError, match="max_depth"):
        service.build(CapsuleDefinition(name="x", root_entities=("w:1",), max_depth=9))
    with pytest.raises(ValueError, match="not found"):
        service.build(CapsuleDefinition(name="x", root_entities=("missing:1",)))
