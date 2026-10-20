"""REVA acceptance journeys (reva-requirements.md section 13), API level.

Each test drives one journey end to end through the kernel, the SQLite store, the
transparency log and the REST router. UI steps (WarrantDrawer, boards) are out of reach of
this lane and are not claimed. Journeys whose prerequisites do not exist in this repository
are listed in test_unrunnable_journeys_are_named with the exact missing prerequisite, so they
show up as named skips in every run instead of silently disappearing.
"""

from __future__ import annotations

import json

import pytest

from reva.core.ids import warrant_id as compute_warrant_id
from reva.kernel.auditor import audit_transparency_log
from reva.kernel.contradictions import detect_contradictions
from reva.kernel.gaps import list_gaps, open_gap
from reva.kernel.signing import verify_warrant_signature
from reva.kernel.translog import leaf_hash, verify_inclusion

pytestmark = pytest.mark.reva_depth("acceptance")
T = {"x-tenant-id": "t1"}


@pytest.mark.reva_case("journey")
def test_rj01_warrant_lifecycle_and_tamper_evidence(stack):
    """RJ-01 (API part): issue, read, verify signature + inclusion proof, tamper, detect, quarantine."""
    kernel, client, store, log = stack["kernel"], stack["client"], stack["store"], stack["log"]
    sealed = [kernel.issue("t1", stack["draft"](f"svc-{i}", i)) for i in range(3)]
    target = sealed[1]

    got = client.get(f"/api/reva/v1/warrants/{target.warrant_id}", headers=T)
    assert got.status_code == 200
    assert compute_warrant_id(got.json()["body"]) == target.warrant_id
    sig = got.json()["envelope"]["signature"]
    key = store.get_key(stack["producer"].active_key_id)
    assert verify_warrant_signature(target.warrant_id, sig["sig"] if isinstance(sig, dict) else sig,
                                    key["public_key"])
    row = store.conn.execute("SELECT leaf_index, leaf_data FROM reva_log_leaves WHERE log_id = ? AND leaf_data = ?",
                             (log.log_id, target.warrant_id)).fetchone()
    assert row is not None, "every issued warrant is in the transparency log"
    size = log.size()
    proof = client.get(f"/api/reva/v1/logs/{log.log_id}/inclusion",
                       params={"leaf_index": row["leaf_index"], "tree_size": size}).json()["proof"]
    assert verify_inclusion(leaf_hash(row["leaf_data"].encode()), row["leaf_index"], size,
                            [bytes.fromhex(p) for p in proof], log.root(size))

    # Corrupt the stored row directly in the database.
    body = json.loads(store.conn.execute("SELECT body FROM reva_warrants WHERE warrant_id = ?",
                                         (target.warrant_id,)).fetchone()["body"])
    body["statement"]["lines_of_code"] = 424242
    store.conn.execute("UPDATE reva_warrants SET body = ? WHERE warrant_id = ?",
                       (json.dumps(body), target.warrant_id))
    store.conn.commit()

    report = audit_transparency_log(store, log)
    assert not report.clean
    assert any(target.warrant_id in issue for issue in report.issues)
    tampered = client.get(f"/api/reva/v1/warrants/{target.warrant_id}", headers=T)
    assert tampered.status_code >= 400, "a corrupted warrant must never be served"
    assert store.is_quarantined("t1", "warrant", target.warrant_id)
    intact = client.get(f"/api/reva/v1/warrants/{sealed[0].warrant_id}", headers=T)
    assert intact.status_code == 200


@pytest.mark.reva_case("journey")
def test_rj02_contradiction_governance(stack):
    """RJ-02 (API part): overlapping conflicting claims open one conflict; human resolution keeps history."""
    kernel, client, store = stack["kernel"], stack["client"], stack["store"]
    owner_a = kernel.issue("t1", stack["draft"]("confluence", 1, artifact="b" * 64,
                                                valid=("2026-01-01T00:00:00.000Z", "2026-12-31T00:00:00.000Z")))
    owner_b = kernel.issue("t1", stack["draft"]("cmdb", 2, artifact="b" * 64,
                                                valid=("2026-06-01T00:00:00.000Z", None)))
    opened = detect_contradictions(store, "t1", owner_b)
    assert len(opened) == 1 and opened[0].status == "open"
    assert sorted(opened[0].member_warrant_ids) == sorted([owner_a.warrant_id, owner_b.warrant_id])
    assert detect_contradictions(store, "t1", owner_b) == [] or \
        len(client.get("/api/reva/v1/contradictions", headers=T).json()["items"]) == 1

    # Disjoint validity is a valid-time split, not a contradiction.
    earlier = kernel.issue("t1", stack["draft"]("archive", 3, artifact="9" * 64,
                                                valid=("2020-01-01T00:00:00.000Z", "2020-12-31T00:00:00.000Z")))
    later = kernel.issue("t1", stack["draft"]("archive", 4, artifact="9" * 64,
                                              valid=("2021-01-01T00:00:00.000Z", None)))
    assert detect_contradictions(store, "t1", later) == []
    assert earlier.warrant_id != later.warrant_id

    resolved = client.post(f"/api/reva/v1/contradictions/{opened[0].contradiction_id}/resolve",
                           json={"rule": "human_decision", "winner_warrant_id": owner_b.warrant_id},
                           headers={**T, "x-principal-id": "reviewer-jane"})
    assert resolved.status_code == 200 and resolved.json()["status"] == "resolved"
    loser = client.get(f"/api/reva/v1/warrants/{owner_a.warrant_id}", headers=T)
    winner = client.get(f"/api/reva/v1/warrants/{owner_b.warrant_id}", headers=T)
    assert loser.status_code == 200 and loser.json()["envelope"]["status"] == "superseded"
    assert winner.json()["envelope"]["status"] == "active"
    record = client.get(f"/api/reva/v1/contradictions/{opened[0].contradiction_id}", headers=T).json()
    assert record["status"] == "resolved" and record["resolution_warrant_id"] == owner_b.warrant_id
    assert sorted(record["member_warrant_ids"]) == sorted([owner_a.warrant_id, owner_b.warrant_id])


@pytest.mark.reva_case("journey")
def test_rj05_knowledge_gap_workflow(stack):
    """RJ-05 (API part): gap created once, assigned, addressed with evidence, closed; board ordered by impact."""
    client, store = stack["client"], stack["store"]
    payload = {"domain": "runtime", "question": "Which service calls /internal/settle at runtime?",
               "scope": {"service": "billing"}, "severity": "high"}
    first = client.post("/api/reva/v1/gaps", json=payload, headers=T).json()
    again = client.post("/api/reva/v1/gaps", json=payload, headers=T).json()
    assert first["gap_id"] == again["gap_id"], "the same gap is created once"
    gap_id = first["gap_id"]

    assigned = client.patch(f"/api/reva/v1/gaps/{gap_id}", headers={**T, "x-principal-id": "lead"},
                            json={"expected_revision": 1, "status": "assigned", "owner": "team-payments"})
    assert assigned.status_code == 200, assigned.text
    assert assigned.json()["owner"] == "team-payments" and assigned.json()["revision"] == 2
    stale = client.patch(f"/api/reva/v1/gaps/{gap_id}", json={"expected_revision": 1, "status": "addressed"},
                         headers=T)
    assert stale.status_code == 409, "a stale revision must not overwrite the gap"
    no_evidence = client.patch(f"/api/reva/v1/gaps/{gap_id}", json={"expected_revision": 2, "status": "closed"},
                               headers=T)
    assert no_evidence.status_code in (400, 409, 422), "closing needs an addressed gap with evidence"

    probe = stack["kernel"].issue("t1", stack["draft"]("probe", 1, artifact="7" * 64))
    addressed = client.patch(f"/api/reva/v1/gaps/{gap_id}", headers=T, json={
        "expected_revision": 2, "status": "addressed", "supporting_warrant_ids": [probe.warrant_id]})
    assert addressed.status_code == 200, addressed.text
    closed = client.patch(f"/api/reva/v1/gaps/{gap_id}", headers=T, json={"expected_revision": 3, "status": "closed"})
    assert closed.status_code == 200, closed.text
    final = client.get(f"/api/reva/v1/gaps/{gap_id}", headers=T).json()
    assert final["status"] == "closed" and final["revision"] == 4
    assert [h["to_status"] for h in final["history"]] == ["open", "assigned", "addressed", "closed"]
    assert final["supporting_warrant_ids"] == [probe.warrant_id]

    open_gap(store, "t1", "runtime", "low impact", "s1", severity="low", impact_score_bp=100)
    open_gap(store, "t1", "runtime", "high impact", "s2", severity="high", impact_score_bp=9000)
    board = [g.question for g in list_gaps(store, "t1", status="open")]
    assert board == ["high impact", "low impact"]


@pytest.mark.reva_case("journey")
def test_rj06_proof_of_done(tmp_path):
    """RJ-06 (engine part): nothing closes on test files alone, AG-05/AG-06/stale are rejected,
    only complete evidence closes, and a manual 'Done' is never a closure."""
    from reva.kernel.authority import Depth
    from reva.pd.antigaming import check_ag05_meaningful_assertion, check_ag06_no_self_mock
    from reva.pd.bindings import Binding, OwnerRef, VerifierSpec
    from reva.pd.closure import ClosureContext, evaluate_closure
    from reva.pd.obligations import Obligation
    from reva.pd.runs import ParsedTest, RunRecord
    import ast

    ob = Obligation(key="OBL-FEAT-1", requirement_id="FEAT-1", title="discount rule",
                    case_kinds=["positive"], reviewed_warrant_id="review:jane")
    binding = Binding(obligation_key=ob.key, owners=[OwnerRef(repo_id="r", path="pricing.py",
                                                              symbol="discount", owner_digest="d1")],
                      verifier=VerifierSpec(verifier_id="pytest", argv=["pytest"]))

    def run(tests):
        return RunRecord(run_id="vr1_r", verifier_id="pytest", binding_digest=binding.digest(), repo_id="r",
                         commit="c1", tree_digest="t", clean=True, environment={}, profile="unit",
                         depth=Depth.UNIT, network="none", argv=["pytest"], started_at="s", finished_at="f",
                         exit_code=0, timed_out=False, lineage={}, artifacts=[], tests=tests, reruns=1)

    good = ParsedTest("t::good", "passed", 1, [ob.key], ["positive"], {"d1": 4})
    ctx = lambda runs, digests=None, scores=None: ClosureContext(  # noqa: E731
        obligation=ob, binding=binding, commit="c1", runs=runs,
        current_owner_digests=digests or {"pricing.py::discount": "d1"}, mutation_scores=scores or {"d1": 0.9})

    # (a) only test files exist: no run -> not closed
    assert evaluate_closure(ctx([])).outcome != "closed"
    # (b) a test that only asserts True is not meaningful (AG-05)
    assert check_ag05_meaningful_assertion(ast.parse("def test_x():\n    assert True\n").body[0]) is False
    assert check_ag05_meaningful_assertion(ast.parse("def test_x():\n    assert f(1) == 2\n").body[0]) is True
    # (c) a test that mocks the owner itself is rejected (AG-06)
    assert check_ag06_no_self_mock(["pricing.discount"], ["pricing.discount"]) is False
    # (d) complete evidence closes
    closed = evaluate_closure(ctx([run([good])]))
    assert closed.outcome == "closed", closed.reasons
    # (e) the owner changed after the run -> stale
    stale = evaluate_closure(ctx([run([good])], digests={"pricing.py::discount": "d2"}))
    assert stale.outcome == "stale" and "OWNER_STALE" in stale.reasons
    # (f) a board item set to Done by hand without a run is not closed
    manual = evaluate_closure(ctx([]))
    assert manual.outcome in ("unknown", "open") and "NO_RUN_AT_COMMIT" in manual.reasons
    # Deterministic ledger IDs
    assert evaluate_closure(ctx([run([good])])).closure_id == closed.closure_id


UNRUNNABLE = {
    "RJ-03": "needs the 3-repo fixture estate (Spring Boot, FastAPI, Electron, Helm, OTel) and impact.service_account golden files",
    "RJ-04": "needs collected coverage contexts and the DISCOUNT_RULE_7 fixture with golden impacted symbols",
    "RJ-07": "needs two connector principals with different Confluence permissions and connector revocation events",
    "RJ-08": "needs the reference evaluation suite and grounded-answer pipeline (REVA_ANSWER_CONTRACT)",
    "RJ-09": "needs CI-built Spring Boot JAR / Go binary / OCI image fixtures for one commit",
    "RJ-10": "needs HAR + OTel + NGINX log fixtures for the fixture estate and golden reconciliation counts",
    "RJ-11": "needs the Electron (E-06) and Spring fixture repos at commits A and B",
    "RJ-12": "needs a deployed stack with Neo4j, volume destroy/restore and producer key rotation",
}


@pytest.mark.parametrize("journey", sorted(UNRUNNABLE))
@pytest.mark.reva_case("journey")
def test_unrunnable_journeys_are_named(journey):
    pytest.skip(f"{journey} NOT RUN: {UNRUNNABLE[journey]}")
