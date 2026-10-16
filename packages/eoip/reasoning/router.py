"""HTTP surface for the §7 reasoning layer (wired by apps/api; not here).

Routes under ``/api/v1/reasoning/*``:

* ``GET  /strategies``            — list registered §7 reasoning strategies.
* ``POST /strategies/{name}/run`` — run one strategy over a problem.
* ``POST /select``                — meta-reasoning: select + run best strategy.
* ``POST /memory/working``        — token-budgeted working memory add/query.
* ``GET  /agentops/costs``        — cost-ledger totals.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from eoip.reasoning.agentops import CostLedger
from eoip.reasoning.evaluation import TrajectoryScorer
from eoip.reasoning.memory import WorkingMemory
from eoip.reasoning.strategies import ReasoningProblem, default_registry


def build_router() -> APIRouter:
    """Construct the reasoning router (see module docstring for routes)."""
    router = APIRouter(prefix="/api/v1/reasoning", tags=["reasoning"])
    registry = default_registry()
    working = WorkingMemory()
    costs = CostLedger()
    scorer = TrajectoryScorer()

    @router.get("/strategies")
    def list_strategies() -> dict:
        return {"strategies": registry.names()}

    @router.post("/strategies/{name}/run")
    def run_strategy(name: str, problem: ReasoningProblem) -> dict:
        try:
            return registry.run(name, problem).model_dump()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @router.post("/select")
    def select_and_run(problem: ReasoningProblem) -> dict:
        return registry.select_and_run(problem).model_dump()

    @router.post("/memory/working")
    def working_add(body: dict) -> dict:
        item, evicted = working.add(str(body.get("content", "")), priority=float(body.get("priority", 0.0)))
        return {
            "item": item.model_dump(),
            "evicted": [e.item_id for e in evicted],
            "used_tokens": working.used_tokens,
            "token_budget": working.token_budget,
        }

    @router.get("/memory/working")
    def working_snapshot() -> dict:
        return {
            "items": [i.model_dump() for i in working.snapshot()],
            "used_tokens": working.used_tokens,
            "token_budget": working.token_budget,
        }

    @router.get("/agentops/costs")
    def cost_totals() -> dict:
        return costs.totals()

    @router.get("/evaluation/references")
    def evaluation_references() -> dict:
        return {
            "references": scorer.references,
            "golden_tools": scorer.golden_tools,
        }

    return router
