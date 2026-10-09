"""FastAPI router for Enterprise Brain OS, Loops, Agents, and Living Brain endpoints."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from eoip.brain.brain_os import BrainOSKernel
from eoip.agents.loops import LoopType, RiskTier
from eoip.retrieval.rag_suite import RAGMode
from eoip.graph.database_adapters import DatabaseType

router = APIRouter(prefix="/brain", tags=["Enterprise Brain OS"])
_kernel = BrainOSKernel()


class BrainAskRequest(BaseModel):
    query: str
    loop: str = "HITL-FE"
    risk_tier: str = "R1"
    rag_mode: str = "HYBRID_RAG"
    target_database: str = "NEO4J"
    force_deterministic: bool = False
    context: dict[str, Any] = Field(default_factory=dict)


class InduceRequest(BaseModel):
    corpus: list[str]


@router.post("/ask")
def ask_brain(req: BrainAskRequest) -> dict[str, Any]:
    try:
        loop_enum = LoopType(req.loop)
    except ValueError:
        loop_enum = LoopType.HITL_FE

    try:
        risk_enum = RiskTier(req.risk_tier)
    except ValueError:
        risk_enum = RiskTier.R1

    try:
        rag_enum = RAGMode(req.rag_mode)
    except ValueError:
        rag_enum = RAGMode.HYBRID_RAG

    try:
        db_enum = DatabaseType(req.target_database)
    except ValueError:
        db_enum = DatabaseType.NEO4J

    ans = _kernel.ask(
        query=req.query,
        loop=loop_enum,
        risk=risk_enum,
        rag_mode=rag_enum,
        target_db=db_enum,
        force_deterministic=req.force_deterministic,
        context=req.context,
    )
    return ans.to_dict()


@router.get("/telemetry")
def get_telemetry() -> dict[str, Any]:
    return _kernel.get_system_telemetry()


@router.get("/loops")
def list_loops() -> list[str]:
    return [l.value for l in LoopType]


@router.get("/agents")
def list_agents() -> list[str]:
    from eoip.agents.archetypes import AgentFactory
    return AgentFactory.list_archetypes()


@router.get("/rag-modes")
def list_rag_modes() -> list[str]:
    return [m.value for m in RAGMode]


@router.get("/dialects")
def list_dialects() -> list[str]:
    from eoip.query.polyglot_engine import QueryDialect
    return [d.value for d in QueryDialect]


@router.get("/databases")
def list_databases() -> list[str]:
    return _kernel.db_registry.list_supported_databases()


@router.post("/induce")
def induce_ontology(req: InduceRequest) -> list[dict[str, Any]]:
    concepts = _kernel.living_brain.induce_ontology_from_corpus(req.corpus)
    return [
        {
            "concept_id": c.concept_id,
            "name": c.name,
            "properties": c.properties,
            "confidence": c.confidence,
        }
        for c in concepts
    ]


@router.get("/snapshot")
def get_brain_snapshot() -> dict[str, Any]:
    s = _kernel.living_brain.compute_brain_snapshot()
    return {
        "snapshot_id": s.snapshot_id,
        "timestamp": s.timestamp,
        "concept_count": s.concept_count,
        "relationship_count": s.relationship_count,
        "coherence_score": s.coherence_score,
        "merkle_root": s.merkle_root,
        "metadata": s.metadata,
    }


def build_brain_router() -> APIRouter:
    return router
