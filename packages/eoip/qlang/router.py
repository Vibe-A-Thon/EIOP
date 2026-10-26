"""HTTP surface for the qlang front-end registry (wired by apps/api).

Routes under ``/api/v1/qlang``:
* ``GET  /languages``                — all capability manifests
* ``GET  /languages/{language_id}``  — one manifest
* ``POST /parse``                    — body {language, query} -> QLangPlan
* ``POST /execute``                  — body {language, query, payload?} -> result
* ``GET  /taxonomy``                 — §5.3 KR-vs-query-language classification

Lazy fastapi import (build_router pattern, cf. eoip.graph.bitemporal).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from eoip.qlang.plans import QLangPlan
from eoip.qlang.registry import (
    ExternalGateError,
    get,
    list_manifests,
    parse,
)
from eoip.qlang.taxonomy import (
    KNOWLEDGE_REPRESENTATION_STANDARDS,
    QUERY_LANGUAGE_IDS,
    assert_taxonomy_honesty,
    classification_of,
)


class ParseRequest(BaseModel):
    language: str = Field(min_length=1)
    query: str = Field(min_length=1)


class ExecuteRequest(BaseModel):
    language: str = Field(min_length=1)
    query: str = Field(min_length=1)
    payload: Any = Field(default=None, description="fixture for payload languages")


def build_router(store=None):
    """Construct the FastAPI router; ``store`` is required only for graph
    language execution (GraphQL / Gremlin / openCypher / SPARQL)."""
    from fastapi import APIRouter, HTTPException

    router = APIRouter(prefix="/api/v1/qlang", tags=["qlang"])

    @router.get("/languages")
    def languages() -> list[dict[str, Any]]:
        return [m.model_dump() for m in list_manifests()]

    @router.get("/languages/{language_id}")
    def language_detail(language_id: str) -> dict[str, Any]:
        try:
            return get(language_id).manifest.model_dump()
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @router.get("/taxonomy")
    def taxonomy() -> dict[str, Any]:
        return {
            "knowledge_representation": {
                rec_id: rec.model_dump()
                for rec_id, rec in KNOWLEDGE_REPRESENTATION_STANDARDS.items()
            },
            "query_languages": sorted(QUERY_LANGUAGE_IDS),
            "violations": assert_taxonomy_honesty(),
        }

    @router.post("/parse", response_model=QLangPlan)
    def parse_(body: ParseRequest) -> QLangPlan:
        try:
            return parse(body.language, body.query)
        except ExternalGateError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.post("/execute")
    def execute_(body: ExecuteRequest) -> Any:
        entry = get(body.language)
        if entry.manifest.tier.value == "declared":
            raise HTTPException(
                status_code=422,
                detail=f"{entry.manifest.name} is a declared-tier capability manifest "
                f"(external gate): {entry.manifest.gate_reason}",
            )
        try:
            plan = parse(body.language, body.query)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        graph_languages = {"graphql", "gremlin", "opencypher", "sparql"}
        if body.language in graph_languages:
            if store is None:
                raise HTTPException(
                    status_code=503,
                    detail=f"{body.language} execution requires a GraphStore",
                )
            return entry.evaluator(plan, store)

        evaluator = entry.evaluator
        if evaluator is None:
            raise HTTPException(status_code=422, detail="No evaluator registered")
        if body.language == "promql":
            return {"result": evaluator(plan, body.payload)}
        if body.language == "datalog":
            return {"facts": evaluator(plan)}
        return {"result": evaluator(plan, body.payload)}

    return router


def classification(language_id: str) -> str | None:
    """Public helper: taxonomy classification for a language id (or None)."""
    c = classification_of(language_id)
    return c.value if c is not None else None
