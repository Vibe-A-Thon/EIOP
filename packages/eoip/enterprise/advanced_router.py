"""Advanced Enterprise Cognitive Capabilities Router.

Exposes REST APIs for:
1. Live Causal Digital Twin & Counterfactual Blast-Radius Engine
2. Multi-Paradigm Semantic Query Dispatcher (Deterministic, Probabilistic, Heuristic, Stochastic, Non-Deterministic)
3. Domain Pack Lifecycle & Deployment Manager
4. Verifiable Zero-Knowledge XAI Decision Factor Attribution Ledger
5. Resilient Agent Mesh & Auto-Recovery Supervisor
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from eoip.agents.mesh_supervisor import ResilientAgentMeshSupervisor
from eoip.audit.xai_ledger import VerifiableXAIAttributionLedger
from eoip.graph.store import GraphStore
from eoip.moonshot.live_causal_engine import LiveCausalGraphEngine
from eoip.ontology.domain_pack_manager import DomainPackLifecycleManager
from eoip.query.multi_paradigm_dispatcher import MultiParadigmQueryDispatcher


class LiveBlastRadiusRequest(BaseModel):
    shock_entities: dict[str, float] = Field(
        ...,
        description="Map of canonical_id -> initial shock magnitude (0.0 to 1.0)",
        examples=[{"cyber-asset-gw-01": 1.0}],
    )
    max_depth: int = Field(default=3, ge=1, le=10)
    failure_threshold: float = Field(default=0.5, ge=0.1, le=1.0)
    dampening_factor: float = Field(default=0.85, ge=0.1, le=1.0)


class CounterfactualInterventionRequest(BaseModel):
    shock_entities: dict[str, float]
    interventions: dict[str, float] = Field(
        ...,
        description="Map of canonical_id -> new hardened resilience (0.0 to 1.0)",
    )
    max_depth: int = Field(default=3, ge=1, le=10)


class MultiParadigmQueryRequest(BaseModel):
    query: str = Field(..., min_length=2)
    seed_canonical_ids: list[str] | None = None
    max_depth: int = Field(default=2, ge=1, le=6)
    monte_carlo_samples: int = Field(default=50, ge=10, le=500)


class ActivateDomainPackRequest(BaseModel):
    seed_live_topology: bool = True


class CertifyDecisionRequest(BaseModel):
    decision_id: str
    agent_id: str
    decision_summary: str
    evidence_entities: list[dict[str, Any]]
    private_reasoning_trace: str | None = None


def build_advanced_capabilities_router(store: GraphStore) -> APIRouter:
    router = APIRouter(tags=["Enterprise Advanced Capabilities"])

    causal_engine = LiveCausalGraphEngine(store)
    multi_dispatcher = MultiParadigmQueryDispatcher(store)
    pack_manager = DomainPackLifecycleManager(store)
    xai_ledger = VerifiableXAIAttributionLedger()
    mesh_supervisor = ResilientAgentMeshSupervisor()

    # -------------------------------------------------------------
    # 1. Live Causal Digital Twin & Counterfactual Blast Radius
    # -------------------------------------------------------------
    @router.post("/api/v1/causal/live-blast-radius")
    def live_blast_radius(req: LiveBlastRadiusRequest):
        return causal_engine.compute_blast_radius(
            shock_entities=req.shock_entities,
            max_depth=req.max_depth,
            failure_threshold=req.failure_threshold,
            dampening_factor=req.dampening_factor,
        )

    @router.post("/api/v1/causal/counterfactual-intervention")
    def counterfactual_intervention(req: CounterfactualInterventionRequest):
        return causal_engine.evaluate_counterfactual(
            shock_entities=req.shock_entities,
            interventions=req.interventions,
            max_depth=req.max_depth,
        )

    # -------------------------------------------------------------
    # 2. Multi-Paradigm Semantic Query Dispatcher
    # -------------------------------------------------------------
    @router.post("/api/v1/query/multi-paradigm")
    def multi_paradigm_query(req: MultiParadigmQueryRequest):
        resp = multi_dispatcher.execute(
            query=req.query,
            seed_canonical_ids=req.seed_canonical_ids,
            max_depth=req.max_depth,
            monte_carlo_samples=req.monte_carlo_samples,
        )
        return {
            "query": resp.query,
            "target_canonical_ids": resp.target_canonical_ids,
            "deterministic_subgraph": resp.deterministic_subgraph,
            "probabilistic_matches": resp.probabilistic_matches,
            "heuristic_paths": resp.heuristic_paths,
            "stochastic_metrics": resp.stochastic_metrics,
            "cognitive_narration": resp.cognitive_narration,
            "kernel_breakdown": resp.kernel_breakdown,
        }

    # -------------------------------------------------------------
    # 3. Domain Pack Lifecycle & Deployment Manager
    # -------------------------------------------------------------
    @router.get("/api/v1/domain-packs")
    def list_domain_packs():
        return {"packs": pack_manager.list_packs(), "active_packs": pack_manager.get_active_packs()}

    @router.get("/api/v1/domain-packs/{pack_name}")
    def get_domain_pack(pack_name: str):
        try:
            return pack_manager.get_pack(pack_name)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @router.post("/api/v1/domain-packs/{pack_name}/activate")
    def activate_domain_pack(pack_name: str, req: ActivateDomainPackRequest):
        try:
            return pack_manager.activate_pack(pack_name, seed_live_topology=req.seed_live_topology)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    # -------------------------------------------------------------
    # 4. Verifiable Zero-Knowledge XAI Decision-Factor Attribution
    # -------------------------------------------------------------
    @router.post("/api/v1/xai/certify-decision")
    def certify_decision(req: CertifyDecisionRequest):
        cert = xai_ledger.certify_decision(
            decision_id=req.decision_id,
            agent_id=req.agent_id,
            decision_summary=req.decision_summary,
            evidence_entities=req.evidence_entities,
            private_reasoning_trace=req.private_reasoning_trace,
        )
        return cert.to_dict()

    @router.post("/api/v1/xai/verify-certificate")
    def verify_certificate(cert_data: dict[str, Any]):
        is_valid = xai_ledger.verify_certificate(cert_data)
        return {"valid": is_valid, "certificate_id": cert_data.get("certificate_id")}

    # -------------------------------------------------------------
    # 5. Resilient Agent Mesh & Auto-Recovery Supervisor
    # -------------------------------------------------------------
    @router.get("/api/v1/agents/mesh/recoveries")
    def list_recovery_bundles(status: str | None = Query(default=None)):
        return {"recoveries": mesh_supervisor.list_bundles(status=status)}

    @router.post("/api/v1/agents/mesh/recover/{recovery_id}")
    def recover_bundle(recovery_id: str):
        try:
            res = mesh_supervisor.recover(
                recovery_id=recovery_id,
                resume_handler=lambda b: {"resumed_step": b.last_completed_step, "recovered": True},
            )
            return res
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return router
