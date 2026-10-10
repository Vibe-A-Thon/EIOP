"""FastAPI router for Enterprise Brain OS, Loops, Agents, and Living Brain endpoints."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from eoip.brain.brain_os import BrainOSKernel
from eoip.agents.loops import LoopType, RiskTier
from eoip.retrieval.rag_suite import RAGMode
from eoip.graph.database_adapters import DatabaseType
from eoip.models.self_llm import (
    CognitiveTier,
    GenerationConfig,
    TIER_PROFILES,
    get_self_llm_engine,
)
from eoip.brain.report_generator import QueryApproach
from eoip.brain.learning_engine import LearningParadigm

router = APIRouter(prefix="/brain", tags=["Enterprise Brain OS"])
_kernel = BrainOSKernel()


class IntelligentQueryRequest(BaseModel):
    query: str
    approach: str = "HYBRID"
    tier: str = "OPUS_FRONTIER"
    context: dict[str, Any] = Field(default_factory=dict)


class BrainQueryReportRequest(BaseModel):
    query: str
    approach: str = "HYBRID"
    tier: str = "OPUS_FRONTIER"
    context: dict[str, Any] = Field(default_factory=dict)


class CognitiveNarrateRequest(BaseModel):
    query: str
    tier: str = "OPUS_FRONTIER"
    context: dict[str, Any] = Field(default_factory=dict)



class LearningTrainRequest(BaseModel):
    paradigm: str = "Q_LEARNING"
    query: str = ""
    action: str = ""
    reward: float = 1.0
    steps: list[str] = Field(default_factory=list)
    outcome_rating: float = 1.0
    concepts: list[str] = Field(default_factory=list)
    error_trace: str = ""
    system_prompt: str = ""



class BrainAskRequest(BaseModel):
    query: str
    loop: str = "HITL-FE"
    risk_tier: str = "R1"
    rag_mode: str = "HYBRID_RAG"
    target_database: str = "NEO4J"
    force_deterministic: bool = False
    tier: str = "OPUS_FRONTIER"
    context: dict[str, Any] = Field(default_factory=dict)


class InduceRequest(BaseModel):
    corpus: list[str]
    confidence_threshold: float = 0.3


class LLMGenerateRequest(BaseModel):
    prompt: str
    tier: str = "OPUS_FRONTIER"
    system_prompt: str = ""
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 40
    min_p: float = 0.05
    repetition_penalty: float = 1.1
    json_schema: dict[str, Any] | None = None
    enable_xai: bool = True
    context: str = ""


class LLMTokenizeRequest(BaseModel):
    text: str


class LLMEmbedRequest(BaseModel):
    text: str
    dimensions: int = 1536


@router.post("/intelligent-query")
def intelligent_query(req: IntelligentQueryRequest) -> dict[str, Any]:
    """Unified intelligent query: understands the question, queries the live graph,
    runs multi-approach analysis, and returns a flowing LLM-style narrative answer."""
    try:
        tier_enum = CognitiveTier(req.tier.upper())
    except ValueError:
        tier_enum = CognitiveTier.OPUS_FRONTIER

    return _kernel.intelligent_query(
        query=req.query,
        approach=req.approach.upper(),
        tier=tier_enum,
        context=req.context,
    )


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

    try:
        tier_enum = CognitiveTier(req.tier)
    except ValueError:
        tier_enum = CognitiveTier.OPUS_FRONTIER

    ans = _kernel.ask(
        query=req.query,
        loop=loop_enum,
        risk=risk_enum,
        rag_mode=rag_enum,
        target_db=db_enum,
        force_deterministic=req.force_deterministic,
        context=req.context,
        tier=tier_enum,
    )
    return ans.to_dict()


@router.post("/query")
def query_brain_report(req: BrainQueryReportRequest) -> dict[str, Any]:
    try:
        app_enum = QueryApproach(req.approach.upper())
    except ValueError:
        app_enum = QueryApproach.HYBRID

    try:
        tier_enum = CognitiveTier(req.tier.upper())
    except ValueError:
        tier_enum = CognitiveTier.OPUS_FRONTIER

    report = _kernel.query_and_report(
        query=req.query,
        approach=app_enum,
        tier=tier_enum,
        context=req.context,
    )
    return report.to_dict()


@router.post("/narrate")
def narrate_brain_inquiry(req: CognitiveNarrateRequest) -> dict[str, Any]:
    try:
        tier_enum = CognitiveTier(req.tier.upper())
    except ValueError:
        tier_enum = CognitiveTier.OPUS_FRONTIER

    narration = _kernel.narrate_query(
        query=req.query,
        tier=tier_enum,
        context=req.context,
    )
    return narration.to_dict()


@router.get("/approaches")

def list_query_approaches() -> list[str]:
    return [a.value for a in QueryApproach]


@router.get("/learning/status")
def get_learning_status() -> dict[str, Any]:
    return _kernel.learning_engine.get_learning_telemetry()


@router.post("/learning/save")
def save_learning_state(directory: str = "data/learning") -> dict[str, str]:
    """Persist all learning engine state to disk for durability across restarts."""
    _kernel.learning_engine.save_state(directory)
    return {"status": "SAVED", "directory": directory}


@router.post("/learning/load")
def load_learning_state(directory: str = "data/learning") -> dict[str, Any]:
    """Restore learning engine state from a previous save."""
    loaded = _kernel.learning_engine.load_state(directory)
    return {"status": "LOADED" if loaded else "NOT_FOUND", "directory": directory}


@router.get("/learning/policy")
def get_learned_policy() -> dict[str, str]:
    """Returns the Q-Learning policy: best action per state."""
    return _kernel.learning_engine.q_learning.get_policy_summary()


@router.post("/learning/train")
def train_learning_engine(req: LearningTrainRequest) -> dict[str, Any]:
    paradigm = req.paradigm.upper()
    if paradigm in ("Q_LEARNING", "REINFORCEMENT_LEARNING"):
        q_val = _kernel.learning_engine.q_learning.update(
            query=req.query,
            action=req.action or "HYBRID_HYPERAUTOMATION",
            reward=req.reward,
        )
        return {
            "status": "UPDATED",
            "paradigm": "Q_LEARNING",
            "query": req.query,
            "action": req.action,
            "q_value": q_val,
        }
    elif paradigm == "IMITATION_LEARNING":
        traj = _kernel.learning_engine.imitation_learning.record_demonstration(
            query=req.query,
            approach=req.action or "HYBRID",
            steps=req.steps or ["Execute reasoning pipeline"],
            outcome_rating=req.outcome_rating,
        )
        return {
            "status": "RECORDED",
            "paradigm": "IMITATION_LEARNING",
            "trajectory_id": traj.trajectory_id,
            "steps_count": len(traj.steps),
        }
    elif paradigm == "CLUSTERING":
        clusters = _kernel.learning_engine.clusterer.cluster_concepts(req.concepts or [req.query])
        return {
            "status": "CLUSTERED",
            "paradigm": "UNSUPERVISED_CLUSTERING",
            "clusters": clusters,
        }
    elif paradigm == "PROMPT_EVOLUTION":
        evolved = _kernel.learning_engine.self_evolving.evolve_agent_prompt(
            agent_archetype=req.action or "AdaptiveAgent",
            system_prompt=req.system_prompt or "Enterprise reasoning agent.",
            failure_trace=req.error_trace or "Execution suboptimal",
        )
        return {
            "status": "EVOLVED",
            "paradigm": "SELF_EVOLVING_AGENTS",
            "evolved_prompt": evolved,
        }
    else:
        return {
            "status": "NOOP",
            "message": f"Unknown learning paradigm: {req.paradigm}",
            "telemetry": _kernel.learning_engine.get_learning_telemetry(),
        }


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
    concepts = _kernel.living_brain.induce_ontology_from_corpus(
        req.corpus,
        confidence_threshold=req.confidence_threshold,
    )
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


@router.get("/llm/models")
def list_llm_models() -> list[dict[str, Any]]:
    return [
        {
            "tier": profile.tier.value,
            "name": profile.name,
            "description": profile.description,
            "context_window": profile.context_window,
            "hidden_dim": profile.hidden_dim,
            "num_heads": profile.num_heads,
            "layers": profile.layers,
            "supports_structured": profile.supports_structured,
            "supports_vision": profile.supports_vision,
            "supports_tools": profile.supports_tools,
            "latency_target_ms": profile.latency_target_ms,
        }
        for profile in TIER_PROFILES.values()
    ]


@router.post("/llm/generate")
def generate_llm(req: LLMGenerateRequest) -> dict[str, Any]:
    try:
        tier_enum = CognitiveTier(req.tier)
    except ValueError:
        tier_enum = CognitiveTier.OPUS_FRONTIER

    cfg = GenerationConfig(
        tier=tier_enum,
        system_prompt=req.system_prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=req.top_p,
        top_k=req.top_k,
        min_p=req.min_p,
        repetition_penalty=req.repetition_penalty,
        json_schema=req.json_schema,
        enable_xai=req.enable_xai,
    )
    res = _kernel.self_llm.generate(prompt=req.prompt, config=cfg, context=req.context)
    xai_data = None
    if res.xai:
        xai_data = {
            "token_attributions": [
                {"token": t.token, "salience": t.salience_score, "entity": t.grounded_entity}
                for t in res.xai.token_attributions
            ],
            "neuro_symbolic_citations": res.xai.neuro_symbolic_citations,
            "counterfactuals": [
                {"premise": c.premise, "impact_delta": c.impact_delta, "explanation": c.explanation}
                for c in res.xai.counterfactuals
            ],
            "uncertainty": {
                "epistemic": res.xai.epistemic_uncertainty,
                "aleatoric": res.xai.aleatoric_uncertainty,
                "coverage_pct": res.xai.conformal_coverage_pct,
            },
        }

    return {
        "content": res.content,
        "tier": res.tier.value,
        "model_name": res.model_name,
        "tokens_generated": res.tokens_generated,
        "prompt_tokens": res.prompt_tokens,
        "latency_ms": res.latency_ms,
        "time_to_first_token_ms": res.time_to_first_token_ms,
        "reasoning_trace": res.reasoning_trace,
        "structured_json": res.structured_json,
        "xai": xai_data,
        "speculative_accepted_tokens": res.speculative_accepted_tokens,
        "metadata": res.metadata,
    }


@router.post("/llm/stream")
def stream_llm(req: LLMGenerateRequest) -> list[dict[str, Any]]:
    try:
        tier_enum = CognitiveTier(req.tier)
    except ValueError:
        tier_enum = CognitiveTier.SONNET_BALANCED

    cfg = GenerationConfig(tier=tier_enum, system_prompt=req.system_prompt)
    chunks = list(_kernel.self_llm.generate_stream(prompt=req.prompt, config=cfg, context=req.context))
    return [
        {
            "chunk_id": c.chunk_id,
            "delta": c.delta,
            "index": c.index,
            "is_final": c.is_final,
            "accumulated": c.accumulated_content,
            "usage": c.usage,
        }
        for c in chunks
    ]


@router.post("/llm/explain")
def explain_llm(req: LLMGenerateRequest) -> dict[str, Any]:
    gen_res = generate_llm(req)
    return {
        "prompt": req.prompt,
        "tier": req.tier,
        "content": gen_res["content"],
        "reasoning_trace": gen_res["reasoning_trace"],
        "xai": gen_res["xai"],
    }


@router.post("/llm/tokenize")
def tokenize_text(req: LLMTokenizeRequest) -> dict[str, Any]:
    tokens = _kernel.self_llm.tokenize(req.text)
    return {
        "token_count": len(tokens),
        "token_ids": tokens[:100],
    }


@router.post("/llm/embed")
def embed_text(req: LLMEmbedRequest) -> dict[str, Any]:
    vec = _kernel.self_llm.embed(req.text, dimensions=req.dimensions)
    return {
        "dimensions": len(vec),
        "embedding": vec,
    }


def build_brain_router(store: Any = None) -> APIRouter:
    global _kernel
    if store is not None:
        _kernel = BrainOSKernel(graph_store=store)
    return router


