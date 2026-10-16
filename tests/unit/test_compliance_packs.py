"""Unit tests for compliance packs, AI governance, change governance, roles and exceptions."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from eoip.audit.sink import AuditSink
from eoip.compliance import (
    AIGovernanceStore,
    ChangeGovernanceStore,
    CompliancePack,
    Control,
    EvaluationRecord,
    EvidenceQuerySpec,
    EvidenceSources,
    HumanOversightConfig,
    ModelCard,
    PolicyExceptionStore,
    RolesRegistry,
    builtin_packs,
    evaluate_control,
    pack_by_framework,
    run_gap_analysis,
)
from eoip.compliance.change import ChangeProposal
from eoip.compliance.roles import GovernanceRole
from eoip.compliance.router import build_router
from eoip.contracts.audit import AuditEvent


def _audit_event(action: str = "graph.read") -> AuditEvent:
    return AuditEvent(
        audit_id="evt-1", event_type="audit.event", actor="tester",
        correlation_id="corr-1", outcome=action,
    )


# ---------------------------------------------------------------------------
# Pack format
# ---------------------------------------------------------------------------

class TestCompliancePacks:
    def test_builtin_packs_cover_frameworks(self):
        frameworks = {p.framework for p in builtin_packs()}
        assert frameworks == {"GDPR", "SOC2", "ISO27001", "HIPAA", "DPDP-2023"}

    def test_each_pack_has_at_least_ten_controls(self):
        for pack in builtin_packs():
            assert len(pack.controls) >= 10, pack.framework

    def test_controls_map_to_capabilities_and_evidence(self):
        for pack in builtin_packs():
            for control in pack.controls:
                assert control.platform_capabilities, control.control_id
                assert control.evidence, control.control_id
                assert control.control_id.startswith(control.framework)

    def test_pack_round_trip(self):
        pack = builtin_packs()[0]
        restored = CompliancePack(**json.loads(pack.model_dump_json()))
        assert restored == pack

    def test_pack_by_framework_case_insensitive(self):
        assert pack_by_framework("gdpr").framework == "GDPR"
        assert pack_by_framework("nope") is None


# ---------------------------------------------------------------------------
# Evidence evaluation
# ---------------------------------------------------------------------------

class TestEvidenceEvaluation:
    def test_evaluate_control_present(self, tmp_path: Path):
        sink = AuditSink(tmp_path / "audit")
        sink.emit(_audit_event("graph.mutate"))
        sources = EvidenceSources(audit_sink=sink)
        control = Control(
            control_id="T-1", framework="T", title="t",
            evidence=[EvidenceQuerySpec(kind="audit_event", params={"action": "graph.mutate"})],
        )
        status = evaluate_control(control, sources)
        assert status.present
        assert status.details[0]["found"] == 1

    def test_evaluate_control_missing(self):
        control = Control(
            control_id="T-2", framework="T", title="t",
            evidence=[EvidenceQuerySpec(kind="audit_event", params={"action": "graph.mutate"})],
        )
        status = evaluate_control(control, EvidenceSources())
        assert not status.present

    def test_min_count(self, tmp_path: Path):
        sink = AuditSink(tmp_path / "audit")
        sink.emit(_audit_event())
        sources = EvidenceSources(audit_sink=sink)
        control = Control(
            control_id="T-3", framework="T", title="t",
            evidence=[EvidenceQuerySpec(kind="audit_event", min_count=2)],
        )
        assert not evaluate_control(control, sources).present

    def test_gap_analysis_counts_gaps(self):
        pack = builtin_packs()[0]
        result = run_gap_analysis(pack, EvidenceSources(), evaluated_at="2026-01-01")
        assert result.total_controls == len(pack.controls)
        assert result.satisfied == 0
        assert len(result.gaps) == len(pack.controls)
        assert all(not s.present for s in result.control_status)

    def test_gap_analysis_with_graph_store(self, tmp_path: Path):
        from eoip.graph.memory import MemoryGraphStore

        store = MemoryGraphStore()
        store.upsert_vertex("Person", {"canonical_id": "urn:eoip:test:entity:1"})
        store.upsert_vertex("Evidence", {"canonical_id": "urn:eoip:test:evidence:1"})
        pack = builtin_packs()[0]
        result = run_gap_analysis(
            pack, EvidenceSources(graph_store=store), evaluated_at="2026-01-01"
        )
        # Some controls only need graph vertices and should now be satisfied.
        assert result.satisfied > 0


# ---------------------------------------------------------------------------
# AI governance (SR-GOV-002)
# ---------------------------------------------------------------------------

class TestAIGovernance:
    def test_model_card_and_label(self, tmp_path: Path):
        store = AIGovernanceStore(tmp_path / "ai.json")
        card = store.new_model_card(
            "summarizer", "1.0",
            risk_classification="limited",
            intended_use=["internal summarization"],
            prohibited_use=["legal advice"],
            created_at="2026-01-01",
        )
        assert card.model_card_id.startswith("urn:eoip:compliance:model-card:")
        label = store.ai_label_for(card.model_card_id)
        assert label["ai_generated"] is True
        assert "summarizer" in label["label"]
        assert "limited" in label["label"]

    def test_label_unknown_model(self, tmp_path: Path):
        store = AIGovernanceStore(tmp_path / "ai.json")
        assert store.ai_label_for("missing")["ai_generated"] is False

    def test_evaluation_records(self, tmp_path: Path):
        store = AIGovernanceStore(tmp_path / "ai.json")
        card = store.new_model_card("m", "1.0")
        store.record_evaluation(EvaluationRecord(
            evaluation_id="ev-1", model_card_id=card.model_card_id,
            evaluated_at="2026-01-01", benchmark="faithfulness", score=0.9,
            threshold=0.8, passed=True,
        ))
        assert len(store.list_evaluations(card.model_card_id)) == 1
        assert store.list_evaluations("other") == []

    def test_persistence_round_trip(self, tmp_path: Path):
        path = tmp_path / "ai.json"
        store = AIGovernanceStore(path)
        card = store.new_model_card("m", "1.0")
        store.configure_oversight(HumanOversightConfig(
            oversight_id="ov-1", name="default", reviewer_role="auditor",
        ))
        reloaded = AIGovernanceStore(path)
        assert reloaded.get_model_card(card.model_card_id) is not None
        assert reloaded.get_oversight("ov-1").reviewer_role == "auditor"


# ---------------------------------------------------------------------------
# Change governance (SR-GOV-003)
# ---------------------------------------------------------------------------

class TestChangeGovernance:
    def test_happy_path(self, tmp_path: Path):
        store = ChangeGovernanceStore(tmp_path / "cg.json")
        proposal = store.create("ontology", "Add Persona entity", requested_by="curator")
        assert proposal.state == "proposed"
        store.transition(proposal.proposal_id, "review", actor="curator", at="2026-01-01")
        store.transition(proposal.proposal_id, "approved", actor="admin", at="2026-01-02")
        store.transition(
            proposal.proposal_id, "rolled_out", actor="admin", at="2026-01-03",
            applied_mutation_ref="mutation-1",
        )
        final = store.get(proposal.proposal_id)
        assert final.state == "rolled_out"
        assert final.applied_mutation_ref == "mutation-1"
        assert [t.from_state for t in final.audit_trail] == ["proposed", "review", "approved"]
        assert all(t.actor for t in final.audit_trail)

    def test_invalid_transition_rejected(self, tmp_path: Path):
        store = ChangeGovernanceStore(tmp_path / "cg.json")
        proposal = store.create("policy", "Relax egress rule")
        with pytest.raises(ValueError, match="Invalid transition"):
            store.transition(proposal.proposal_id, "rolled_out", actor="admin", at="2026-01-01")

    def test_rollback_first_class(self, tmp_path: Path):
        store = ChangeGovernanceStore(tmp_path / "cg.json")
        proposal = store.create("model", "Swap embedding model")
        store.transition(proposal.proposal_id, "review", actor="a", at="t1")
        store.transition(proposal.proposal_id, "approved", actor="a", at="t2")
        store.transition(proposal.proposal_id, "rolled_back", actor="a", at="t3", reason="regression")
        assert store.get(proposal.proposal_id).state == "rolled_back"
        with pytest.raises(ValueError):
            store.transition(proposal.proposal_id, "review", actor="a", at="t4")

    def test_persistence(self, tmp_path: Path):
        path = tmp_path / "cg.json"
        store = ChangeGovernanceStore(path)
        proposal = store.create("agent", "New agent role", created_at="2026-01-01")
        reloaded = ChangeGovernanceStore(path)
        assert reloaded.get(proposal.proposal_id) is not None
        assert isinstance(reloaded.list(kind="agent")[0], ChangeProposal)


# ---------------------------------------------------------------------------
# Roles (SR-GOV-004)
# ---------------------------------------------------------------------------

class TestRoles:
    def test_auditor_role_is_read_only_tamper_evident(self):
        registry = RolesRegistry()
        auditor = registry.get(GovernanceRole.AUDITOR)
        assert auditor.read_only
        assert auditor.tamper_evident_view
        view = registry.auditor_view()
        assert view["read_only"] is True
        assert view["tamper_evident"] is True
        assert "audit:read" in view["permissions"]

    def test_all_governance_roles_present(self):
        registry = RolesRegistry()
        roles = {r.role for r in registry.list()}
        assert roles == {
            GovernanceRole.DATA_OWNER, GovernanceRole.STEWARD,
            GovernanceRole.CUSTODIAN, GovernanceRole.ONTOLOGY_CURATOR,
            GovernanceRole.SECURITY_ADMIN, GovernanceRole.AUDITOR,
        }


# ---------------------------------------------------------------------------
# Policy exceptions (SR-GOV-005)
# ---------------------------------------------------------------------------

class TestPolicyExceptions:
    def test_active_until_expiry(self, tmp_path: Path):
        store = PolicyExceptionStore(tmp_path / "pe.json")
        future = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
        exc = store.create("authz:egress", "connector:x", "urgent customer need",
                           approved_by="admin", expires_at=future)
        assert exc.is_active()
        assert store.list(active_only=True) == [exc]

    def test_auto_expires(self, tmp_path: Path):
        store = PolicyExceptionStore(tmp_path / "pe.json")
        past = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
        exc = store.create("retention:short", "dataset:y", "legacy import",
                           approved_by="admin", expires_at=past)
        assert not exc.is_active()
        assert store.list(active_only=True) == []

    def test_revoke(self, tmp_path: Path):
        store = PolicyExceptionStore(tmp_path / "pe.json")
        future = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        exc = store.create("policy:p", "s", "j", approved_by="admin", expires_at=future)
        store.revoke(exc.exception_id, actor="admin")
        assert not store.get(exc.exception_id).is_active()

    def test_requires_approver(self, tmp_path: Path):
        store = PolicyExceptionStore(tmp_path / "pe.json")
        with pytest.raises(ValueError):
            store.create("policy:p", "s", "j", approved_by="", expires_at="2030-01-01")

    def test_persistence(self, tmp_path: Path):
        path = tmp_path / "pe.json"
        store = PolicyExceptionStore(path)
        future = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        exc = store.create("policy:p", "s", "j", approved_by="admin", expires_at=future)
        reloaded = PolicyExceptionStore(path)
        assert reloaded.get(exc.exception_id) is not None


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def _client(tmp_path: Path):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    ai = AIGovernanceStore(tmp_path / "ai.json")
    changes = ChangeGovernanceStore(tmp_path / "cg.json")
    exceptions = PolicyExceptionStore(tmp_path / "pe.json")
    app = FastAPI()
    app.include_router(build_router(
        ai_store=ai, change_store=changes, exception_store=exceptions,
    ))
    return TestClient(app)


class TestComplianceRouter:
    def test_packs_listing(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.get("/api/v1/compliance/packs")
        assert resp.status_code == 200
        assert len(resp.json()) == 5

    def test_gap_analysis_endpoint(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.post("/api/v1/compliance/packs/gdpr/gap-analysis")
        assert resp.status_code == 200
        body = resp.json()
        assert body["total_controls"] >= 10
        assert body["satisfied"] == 0

    def test_change_workflow_via_http(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.post("/api/v1/compliance/changes", params={
            "kind": "ontology", "title": "Add entity",
        })
        assert resp.status_code == 201
        pid = resp.json()["proposal_id"]
        resp = client.post(f"/api/v1/compliance/changes/{pid}/transition", params={
            "to_state": "rolled_out", "actor": "admin", "at": "2026-01-01",
        })
        assert resp.status_code == 409  # invalid transition
        for state in ("review", "approved", "rolled_out"):
            resp = client.post(f"/api/v1/compliance/changes/{pid}/transition", params={
                "to_state": state, "actor": "admin", "at": "2026-01-01",
            })
            assert resp.status_code == 200, resp.text

    def test_exception_endpoints(self, tmp_path: Path):
        client = _client(tmp_path)
        future = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        resp = client.post("/api/v1/compliance/exceptions", params={
            "policy_ref": "p", "subject": "s", "justification": "j",
            "approved_by": "admin", "expires_at": future,
        })
        assert resp.status_code == 201
        assert client.get("/api/v1/compliance/exceptions", params={"active_only": True}).json()

    def test_auditor_view_endpoint(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.get("/api/v1/compliance/roles/auditor-view")
        assert resp.status_code == 200
        assert resp.json()["read_only"] is True
