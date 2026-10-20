"""SR-PRV-002: data-subject requests across graph, raw captures, vector/search indexes, caches,
derived graphs, summaries, exports and backups (flagged) - access/export, rectification and erasure
with propagation, each with a proof."""
from __future__ import annotations

import json

import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.privacy.dsr import ERASED, SubjectRequestWorkflow
from eoip.tenancy.isolation import REQUIRED_LAYERS, IsolationModel, IsolationPlacement, IsolationRegistry
from eoip.tenancy.layers import TenantLayers

pytestmark = pytest.mark.req("SR-PRV-002")

ALICE, BOB = "alice@corp.example", "bob@corp.example"


def _embed(text: str) -> list[float]:
    return [float(len(text)), float(sum(map(ord, text)) % 997)]


@pytest.fixture
def world(tmp_path):
    reg = IsolationRegistry()
    for t in ("acme", "bolt"):
        reg.register(IsolationPlacement(model=IsolationModel.POOL, tenant_id=t,
                                        layers={l: f"{l}-pool" for l in REQUIRED_LAYERS}))
    layers = TenantLayers(reg, root=tmp_path, master_key=b"k" * 32)
    h, other = layers.for_tenant("acme"), layers.for_tenant("bolt")
    g = MemoryGraphStore()
    g.upsert_vertex("Person", {"canonical_id": "p1", "email": ALICE, "display_name": "Alice Smyth"})
    g.upsert_vertex("Person", {"canonical_id": "p2", "email": BOB, "display_name": "Bob"})
    g.upsert_vertex("GenericEntity", {"canonical_id": "d1", "description": f"Alice Smyth ({ALICE}) owns billing"})
    h.put_object("raw/jira/1.json", json.dumps({"reporter": ALICE, "text": "Alice Smyth filed it"}).encode())
    h.put_object("raw/jira/2.json", json.dumps({"reporter": BOB}).encode())
    h.vector_upsert("e1", _embed("Alice Smyth on-call"), {"text": "Alice Smyth on-call", "subject_ids": [ALICE]})
    h.vector_upsert("e2", _embed("Bob on-call"), {"text": "Bob on-call", "subject_ids": [BOB]})
    h.search_add("s1", f"incident handled by Alice Smyth {ALICE}", {"subject_ids": [ALICE]})
    h.search_add("s2", "incident handled by Bob", {"subject_ids": [BOB]})
    h.cache_set("q:owners", {"rows": [ALICE, "Alice Smyth"]})
    h.cache_set("q:other", {"rows": [BOB]})
    h.put_object("summaries/team.json", json.dumps({"text": "Alice Smyth and Bob run billing.", "sources": [
        {"id": "s1", "text": "Alice Smyth runs billing", "subject_ids": [ALICE]},
        {"id": "s2", "text": "Bob runs billing", "subject_ids": [BOB]}]}).encode())
    h.write_export("weekly.csv", f"owner,{ALICE}\n".encode())
    h.backup("nightly", {"people": [ALICE, BOB]})
    other.vector_upsert("x1", [1.0], {"text": ALICE, "subject_ids": [ALICE]})  # another tenant's copy
    wf = SubjectRequestWorkflow(h, graph_store=g, derived_labels=("GenericEntity",), embed=_embed,
                                summarize=lambda texts: " ".join(texts))
    return wf, h, other, g


def test_locate_covers_every_store_and_stays_in_tenant(world):
    wf, *_ = world
    rep = wf.locate(ALICE)
    assert rep.surface_counts() == {"graph": 1, "derived_graph": 1, "raw_capture": 1, "vector": 1, "search": 1,
                                    "cache": 1, "summary": 1, "export": 1, "backup": 1}
    assert "x1" not in {h.ref for h in rep.hits}


def test_access_export_bundles_the_subjects_data_with_proof(world):
    wf, h, *_ = world
    name, proof = wf.access_export(ALICE)
    bundle = json.loads(h.read_export(name))
    assert bundle["data"]["graph"][0]["properties"]["email"] == ALICE
    assert bundle["data"]["vector"][0]["payload"]["text"] == "Alice Smyth on-call"
    assert "Bob" not in json.dumps(bundle["data"]["vector"])
    assert proof.action == "access" and proof.verified and len(proof.digest) == 64


def test_rectification_propagates_to_embeddings_indexes_caches_and_summaries(world):
    wf, h, _, g = world
    old_vec = h.vector_items()["e1"][0]
    proof = wf.rectify(ALICE, "Smyth", "Smith")
    assert proof.verified
    assert g.get_vertex_by_canonical_id("p1")["properties"]["display_name"] == "Alice Smith"
    assert "Alice Smith" in g.get_vertex_by_canonical_id("d1")["properties"]["description"]
    vec, payload = h.vector_items()["e1"]
    assert payload["text"] == "Alice Smith on-call" and vec == _embed("Alice Smith on-call") != old_vec
    assert "Smyth" not in h.search_docs()["s1"][0]
    assert h.cache_get("q:owners") is None and h.cache_get("q:other") == {"rows": [BOB]}
    assert "Alice Smith runs billing" in json.loads(h.get_object("summaries/team.json"))["text"]
    assert json.loads(h.get_object("rectifications/raw/jira/1.json"))["new"] == "Smith"
    ops = {(a["surface"], a["op"]) for a in proof.actions}
    assert ("vector", "re-embedded") in ops and ("export", "flagged-stale") in ops


def test_erasure_propagates_everywhere_flags_backups_and_proves_it(world):
    wf, h, other, g = world
    proof = wf.erase(ALICE)
    assert proof.verified and proof.flagged == ["backup:nightly.bak"]
    assert proof.after == {"backup": 1}
    p1 = g.get_vertex_by_canonical_id("p1")["properties"]
    assert p1["email"] == ERASED and p1["deleted_at"]
    assert ALICE not in g.get_vertex_by_canonical_id("d1")["properties"]["description"]
    assert h.list_objects("raw/") == ["raw/jira/2.json"]
    assert set(h.vector_items()) == {"e2"} and set(h.search_docs()) == {"s2"}
    assert h.cache_get("q:owners") is None and h.cache_get("q:other") == {"rows": [BOB]}
    summary = json.loads(h.get_object("summaries/team.json"))
    assert summary["text"] == "Bob runs billing" and [s["id"] for s in summary["sources"]] == ["s2"]
    assert h.list_exports() == []
    assert wf.locate(BOB).surface_counts()["graph"] == 1  # other subjects untouched
    assert "x1" in other.vector_items()  # another tenant's store is outside this tenant's request
    bob = wf.erase(BOB)
    assert bob.verified and bob.digest != proof.digest


def test_erasure_proof_fails_when_a_store_cannot_be_cleaned(world, monkeypatch):
    wf, h, *_ = world
    monkeypatch.setattr(h, "vector_delete", lambda doc_id: False)
    proof = wf.erase(ALICE)
    assert proof.verified is False and proof.after.get("vector") == 1


def test_rectify_then_erase_leaves_no_rectification_trail(world):
    wf, h, *_ = world
    assert wf.rectify(ALICE, "Smyth", "Smith").verified
    proof = wf.erase(ALICE)
    assert proof.verified and h.list_objects("rectifications/") == []
