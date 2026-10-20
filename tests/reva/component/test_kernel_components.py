"""REVA component tests: kernel + SQLite store + transparency log + REST router together."""

from __future__ import annotations

import json

import pytest

from reva.core.ids import warrant_id as compute_warrant_id
from reva.kernel.auditor import audit_transparency_log
from reva.kernel.contradictions import detect_contradictions
from reva.kernel.signing import verify_warrant_signature
from reva.kernel.store import RevaStore
from reva.kernel.keys import decrypt_private_key, generate_key
from reva.kernel.sth import issue_sth_now, verify_sth
from reva.kernel.translog import leaf_hash as rfc6962_leaf_hash, verify_consistency, verify_inclusion

pytestmark = pytest.mark.reva_depth("component")


@pytest.mark.reva_case("positive")
def test_issued_warrant_round_trips_through_rest_and_verifies(stack):
    sealed = stack["kernel"].issue("t1", stack["draft"]("svc-a", 120))
    client = stack["client"]
    got = client.get(f"/api/reva/v1/warrants/{sealed.warrant_id}", headers={"x-tenant-id": "t1"})
    assert got.status_code == 200, got.text
    body = got.json()["body"]
    assert compute_warrant_id(body) == sealed.warrant_id
    key = stack["store"].get_key(stack["producer"].active_key_id)
    signature = got.json()["envelope"]["signature"]
    sig = signature["sig"] if isinstance(signature, dict) else signature
    assert verify_warrant_signature(sealed.warrant_id, sig, key["public_key"])
    query = client.post("/api/reva/v1/warrants/query", json={"limit": 10}, headers={"x-tenant-id": "t1"})
    assert [item["warrant_id"] for item in query.json()["items"]] == [sealed.warrant_id]
    other = client.post("/api/reva/v1/warrants/query", json={"limit": 10}, headers={"x-tenant-id": "t2"})
    assert other.json()["total"] == 0  # tenant isolation across the REST boundary


@pytest.mark.reva_case("positive")
def test_warrants_survive_a_store_reopen(stack):
    sealed = stack["kernel"].issue("t1", stack["draft"]("svc-b", 7))
    stack["store"].conn.commit()
    reopened = RevaStore(str(stack["path"]))
    try:
        row = reopened.conn.execute("SELECT body FROM reva_warrants WHERE warrant_id = ?",
                                    (sealed.warrant_id,)).fetchone()
        assert row is not None and compute_warrant_id(json.loads(row["body"])) == sealed.warrant_id
    finally:
        reopened.conn.close()


@pytest.mark.reva_case("positive")
def test_rest_inclusion_and_consistency_proofs_verify(stack):
    ids = [stack["kernel"].issue("t1", stack["draft"](f"svc-{i}", i)).warrant_id for i in range(5)]
    log, client = stack["log"], stack["client"]
    size = log.size()
    assert size >= len(ids)
    root = log.root(size)
    head = client.get("/api/reva/v1/logs/reva_main_log/sth").json()
    assert head["signed"] is False and head["tree_size"] == size and head["root_hash"] == root.hex()
    key = generate_key(stack["store"], "t1", "log", "reva_main_log")
    signed = issue_sth_now(stack["store"], log, key.key_id, decrypt_private_key(key.private_key_enc))
    assert verify_sth(signed, key.public_key_bytes)
    head = client.get("/api/reva/v1/logs/reva_main_log/sth").json()
    assert head["signed"] is True and head["key_id"] == key.key_id and head["root_hash"] == root.hex()
    assert client.get("/api/reva/v1/logs/no_such_log/sth").status_code == 404
    assert client.get("/api/reva/v1/logs/reva_main_log/inclusion",
                      params={"leaf_index": size, "tree_size": size}).status_code == 400
    leaves = log.get_leaves()
    for index in (0, size - 1):
        proof = client.get("/api/reva/v1/logs/reva_main_log/inclusion",
                           params={"leaf_index": index, "tree_size": size}).json()["proof"]
        row = stack["store"].conn.execute(
            "SELECT leaf_data FROM reva_log_leaves WHERE log_id = ? AND leaf_index = ?",
            ("reva_main_log", index)).fetchone()
        leaf = rfc6962_leaf_hash(row["leaf_data"].encode("utf-8"))
        assert verify_inclusion(leaf, index, size, [bytes.fromhex(p) for p in proof], root)
    assert leaves
    proof = client.get("/api/reva/v1/logs/reva_main_log/consistency",
                       params={"first_size": 2, "second_size": size}).json()["proof"]
    assert verify_consistency(2, size, log.root(2), root, [bytes.fromhex(p) for p in proof])


@pytest.mark.reva_case("negative")
def test_auditor_detects_a_tampered_warrant_row(stack):
    sealed = stack["kernel"].issue("t1", stack["draft"]("svc-tamper", 1))
    assert audit_transparency_log(stack["store"], stack["log"]).clean
    row = stack["store"].conn.execute("SELECT body FROM reva_warrants WHERE warrant_id = ?",
                                      (sealed.warrant_id,)).fetchone()
    body = json.loads(row["body"])
    body["statement"]["lines_of_code"] = 999_999
    stack["store"].conn.execute("UPDATE reva_warrants SET body = ? WHERE warrant_id = ?",
                                (json.dumps(body), sealed.warrant_id))
    report = audit_transparency_log(stack["store"], stack["log"])
    assert not report.clean
    assert any(sealed.warrant_id in issue and "digest" in issue for issue in report.issues)


@pytest.mark.reva_case("positive")
def test_contradiction_detected_listed_and_resolved_over_rest(stack):
    kernel, client = stack["kernel"], stack["client"]
    first = kernel.issue("t1", stack["draft"]("scan-a", 100, artifact="d" * 64))
    second = kernel.issue("t1", stack["draft"]("scan-b", 200, artifact="d" * 64))
    found = detect_contradictions(stack["store"], "t1", second)
    assert len(found) == 1
    listed = client.get("/api/reva/v1/contradictions", headers={"x-tenant-id": "t1"}).json()
    items = listed["items"] if isinstance(listed, dict) else listed
    assert found[0].contradiction_id in json.dumps(items)
    resolved = client.post(f"/api/reva/v1/contradictions/{found[0].contradiction_id}/resolve",
                           json={"rule": "human_decision", "winner_warrant_id": second.warrant_id},
                           headers={"x-tenant-id": "t1", "x-principal-id": "reviewer"})
    assert resolved.status_code == 200, resolved.text
    assert resolved.json()["status"] == "resolved"
    loser = client.get(f"/api/reva/v1/warrants/{first.warrant_id}", headers={"x-tenant-id": "t1"}).json()
    assert loser["envelope"]["status"] == "superseded"


@pytest.mark.reva_case("positive")
def test_gap_created_and_read_back_over_rest(stack):
    client = stack["client"]
    created = client.post("/api/reva/v1/gaps", headers={"x-tenant-id": "t1"}, json={
        "domain": "runtime", "question": "which service calls svc-a at runtime?",
        "severity": "high", "scope": {"kind": "service", "key": "svc-a"}})
    assert created.status_code in (200, 201), created.text
    gap_id = created.json()["gap_id"]
    got = client.get(f"/api/reva/v1/gaps/{gap_id}", headers={"x-tenant-id": "t1"})
    assert got.status_code == 200 and got.json()["gap_id"] == gap_id
    listed = client.get("/api/reva/v1/gaps", headers={"x-tenant-id": "t1"}).json()
    assert gap_id in json.dumps(listed)
