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


def test_capsule_is_reproducible(tmp_path):
    store = _store()
    service = KnowledgeCapsuleService(store, tmp_path)
    first = service.build(CapsuleDefinition(name="rel", root_entities=("w:1",)))
    second = service.build(CapsuleDefinition(name="rel", root_entities=("w:1",)))
    assert first.capsule_id == second.capsule_id
    assert first.graph_fingerprint == second.graph_fingerprint


def test_capsule_trust_threshold_excludes_inferred(tmp_path):
    service = KnowledgeCapsuleService(_store(), tmp_path)
    capsule = service.build(
        CapsuleDefinition(
            name="trusted", root_entities=("w:1",), trust_threshold="DETERMINISTIC"
        )
    )
    trusts = {rel["trust"] for rel in capsule.relationships}
    assert trusts == {"DETERMINISTIC"}
    assert all(rel["type"] != "CALLS" for rel in capsule.relationships)


def test_capsule_domain_filter(tmp_path):
    service = KnowledgeCapsuleService(_store(), tmp_path)
    capsule = service.build(
        CapsuleDefinition(name="work-only", root_entities=("w:1",), domains=("WORK",))
    )
    assert {entity["domain"] for entity in capsule.entities} == {"WORK"}


def test_capsule_persists_manifest_and_is_listable(tmp_path):
    service = KnowledgeCapsuleService(_store(), tmp_path)
    service.build(CapsuleDefinition(name="persisted", root_entities=("w:1",)))

    manifests = service.list_manifests()
    assert len(manifests) == 1
    assert manifests[0]["definition"]["name"] == "persisted"

    document = service.get_manifest("persisted")
    assert document is not None
    assert document["manifest"]["definition"]["name"] == "persisted"
    assert service.get_manifest("missing") is None


def test_capsule_validates_definition(tmp_path):
    service = KnowledgeCapsuleService(_store(), tmp_path)
    with pytest.raises(ValueError, match="at least one root"):
        service.build(CapsuleDefinition(name="x", root_entities=()))
    with pytest.raises(ValueError, match="max_depth"):
        service.build(CapsuleDefinition(name="x", root_entities=("w:1",), max_depth=9))
    with pytest.raises(ValueError, match="not found"):
        service.build(CapsuleDefinition(name="x", root_entities=("missing:1",)))
