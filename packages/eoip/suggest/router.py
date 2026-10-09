"""HTTP surface for the NL suggestion engine (wired by apps/api; not here).

``build_router(store=None, enforcer=None)`` constructs the
``/api/v1/suggest`` router lazily (pattern: ``eoip.graph.bitemporal``).
"""

from __future__ import annotations

from typing import Any

from eoip.suggest.engine import SuggestionEngine
from eoip.suggest.models import SuggestionRequest, SuggestionResponse


def build_router(store: Any = None, enforcer: Any = None, *, llm_hook: Any = None):
    """Construct the ``/api/v1/suggest`` FastAPI router.

    ``store`` is a GraphStore (or None — suggestions then carry no entity
    bindings); ``enforcer`` is an ``eoip.authz.PolicyEnforcer`` used for the
    permission pre-check note; ``llm_hook`` is the optional External-gate
    LLM-assist callable.
    """
    from fastapi import APIRouter

    engine = SuggestionEngine(store, enforcer=enforcer, llm_hook=llm_hook)
    router = APIRouter(prefix="/api/v1/suggest", tags=["suggest"])

    @router.post("", response_model=SuggestionResponse)
    @router.post("/", response_model=SuggestionResponse, include_in_schema=False)
    def suggest(request: SuggestionRequest) -> SuggestionResponse:
        return engine.suggest(request)

    @router.post("/interpret", response_model=SuggestionResponse)
    def interpret(request: SuggestionRequest) -> SuggestionResponse:
        return engine.suggest(request)

    @router.get("/intents")
    def intents() -> dict[str, Any]:
        from eoip.suggest import parser

        return {
            "intents": sorted(parser._INTENT_PATTERNS),
            "cost_tiers": sorted(__import__("eoip.suggest.models", fromlist=["COST_TIERS"]).COST_TIERS),
            "answer_modes": ["deterministic", "narrated", "exploratory", "report"],
            "deterministic_tier": True,
            "llm_assist": "external-gate optional hook",
        }

    return router
