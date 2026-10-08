"""HTTP router for compliance and AI governance (SR-GOV-001..005).

``build_router(...)`` constructs the ``/api/v1/compliance`` router. FastAPI
is imported lazily inside the factory so the module stays importable without
the web stack (pattern: ``eoip.graph.bitemporal.build_router``). The wiring
step (apps/api) mounts the returned router unchanged.
"""

from __future__ import annotations

from typing import Any

from eoip.compliance.ai import (
    AIGovernanceStore,
    EvaluationRecord,
    HumanOversightConfig,
    ModelCard,
)
from eoip.compliance.change import ChangeGovernanceStore, ChangeKind, ChangeState
from eoip.compliance.exceptions import PolicyExceptionStore
from eoip.compliance.pack import CompliancePack, EvidenceSources, run_gap_analysis
from eoip.compliance.packs import builtin_packs, pack_by_framework
from eoip.compliance.roles import GovernanceRole, RolesRegistry


def build_router(
    *,
    evidence_sources: EvidenceSources | None = None,
    ai_store: AIGovernanceStore | None = None,
    change_store: ChangeGovernanceStore | None = None,
    exception_store: PolicyExceptionStore | None = None,
    roles_registry: RolesRegistry | None = None,
):
    """Construct the ``/api/v1/compliance`` FastAPI router.

    Stores default to on-disk JSON stores under ``EOIP_DATA_DIR`` when not
    provided, so the router is fully functional without DI in tests/demo.
    """
    from fastapi import APIRouter, HTTPException, Query

    sources = evidence_sources or EvidenceSources(
        policy_exception_store=exception_store,
        ai_governance_store=ai_store,
    )
    ai = ai_store or AIGovernanceStore()
    changes = change_store or ChangeGovernanceStore()
    exceptions = exception_store or PolicyExceptionStore()
    roles = roles_registry or RolesRegistry()

    router = APIRouter(prefix="/api/v1/compliance", tags=["compliance"])

    # -- packs (SR-GOV-001) ------------------------------------------------
    @router.get("/packs", response_model=list[CompliancePack])
    def list_packs() -> list[CompliancePack]:
        return builtin_packs()

    @router.get("/packs/{framework}", response_model=CompliancePack)
    def get_pack(framework: str) -> CompliancePack:
        pack = pack_by_framework(framework)
        if pack is None:
            raise HTTPException(status_code=404, detail=f"Unknown pack: {framework}")
        return pack

    @router.post("/packs/{framework}/gap-analysis")
    def gap_analysis(framework: str) -> dict[str, Any]:
        pack = pack_by_framework(framework)
        if pack is None:
            raise HTTPException(status_code=404, detail=f"Unknown pack: {framework}")
        from eoip.compliance.exceptions import utc_now_iso

        return run_gap_analysis(pack, sources, evaluated_at=utc_now_iso()).model_dump()

    # -- AI governance (SR-GOV-002) ---------------------------------------
    @router.get("/ai/model-cards", response_model=list[ModelCard])
    def list_model_cards() -> list[ModelCard]:
        return ai.list_model_cards()

    @router.post("/ai/model-cards", response_model=ModelCard, status_code=201)
    def register_model_card(card: ModelCard) -> ModelCard:
        return ai.register_model_card(card)

    @router.get("/ai/model-cards/{model_card_id}/label")
    def ai_label(model_card_id: str) -> dict[str, Any]:
        return ai.ai_label_for(model_card_id)

    @router.get("/ai/evaluations", response_model=list[EvaluationRecord])
    def list_evaluations(model_card_id: str | None = Query(default=None)) -> list[EvaluationRecord]:
        return ai.list_evaluations(model_card_id)

    @router.post("/ai/evaluations", response_model=EvaluationRecord, status_code=201)
    def record_evaluation(record: EvaluationRecord) -> EvaluationRecord:
        return ai.record_evaluation(record)

    @router.post("/ai/oversight", response_model=HumanOversightConfig, status_code=201)
    def configure_oversight(config: HumanOversightConfig) -> HumanOversightConfig:
        return ai.configure_oversight(config)

    # -- change governance (SR-GOV-003) -----------------------------------
    @router.get("/changes")
    def list_changes(
        state: ChangeState | None = Query(default=None),
        kind: ChangeKind | None = Query(default=None),
    ) -> list[dict[str, Any]]:
        return [p.model_dump() for p in changes.list(state=state, kind=kind)]

    @router.post("/changes", status_code=201)
    def create_change(
        kind: ChangeKind,
        title: str,
        description: str = "",
        requested_by: str = "",
        created_at: str = "",
    ) -> dict[str, Any]:
        return changes.create(
            kind, title, description=description, requested_by=requested_by, created_at=created_at
        ).model_dump()

    @router.post("/changes/{proposal_id}/transition")
    def transition_change(
        proposal_id: str,
        to_state: ChangeState,
        actor: str,
        at: str,
        reason: str = "",
    ) -> dict[str, Any]:
        try:
            return changes.transition(
                proposal_id, to_state, actor=actor, at=at, reason=reason
            ).model_dump()
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Unknown proposal: {proposal_id}")
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc))

    # -- roles (SR-GOV-004) -------------------------------------------------
    @router.get("/roles")
    def list_roles() -> list[dict[str, Any]]:
        return [r.model_dump() for r in roles.list()]

    @router.get("/roles/auditor-view")
    def auditor_view() -> dict[str, Any]:
        return roles.auditor_view()

    @router.get("/roles/{role}")
    def get_role(role: GovernanceRole) -> dict[str, Any]:
        definition = roles.get(role)
        if definition is None:
            raise HTTPException(status_code=404, detail=f"Unknown role: {role}")
        return definition.model_dump()

    # -- policy exceptions (SR-GOV-005) ------------------------------------
    @router.get("/exceptions")
    def list_exceptions(active_only: bool = Query(default=False)) -> list[dict[str, Any]]:
        return [e.model_dump() for e in exceptions.list(active_only=active_only)]

    @router.post("/exceptions", status_code=201)
    def create_exception(
        policy_ref: str,
        subject: str,
        justification: str,
        approved_by: str,
        expires_at: str,
    ) -> dict[str, Any]:
        return exceptions.create(
            policy_ref, subject, justification, approved_by=approved_by, expires_at=expires_at
        ).model_dump()

    @router.post("/exceptions/{exception_id}/revoke")
    def revoke_exception(exception_id: str, actor: str) -> dict[str, Any]:
        try:
            return exceptions.revoke(exception_id, actor=actor).model_dump()
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Unknown exception: {exception_id}")

    return router
