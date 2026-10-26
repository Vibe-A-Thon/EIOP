"""HTTP routers (lazy FastAPI pattern; wiring lives in apps/api).

* ``build_graphbuild_router()`` — /api/v1/graphbuild/*
* ``build_adapters_router()``  — /api/v1/adapters/*
"""

from __future__ import annotations

from eoip.graphbuild.models import GraphDelta


def build_graphbuild_router():
    """Router for deterministic graph-building endpoints.

    Routes (all POST unless noted):
    ``/api/v1/graphbuild/schema/induce``, ``/plan``,
    ``/cochange``, ``/inclusion-dependencies``, ``/mentions``,
    ``/hierarchy``, ``/rollup``, ``/similarity``, ``/link-prediction``,
    ``/repair``, ``/enrichment/submit``.
    """
    from fastapi import APIRouter

    from eoip.graphbuild.cochange import CoChangeConfig, build_cochange_edges
    from eoip.graphbuild.dependencies import InclusionDependencyConfig, discover_inclusion_dependencies
    from eoip.graphbuild.hierarchy import HierarchyConfig, induce_hierarchy
    from eoip.graphbuild.linking import Gazetteer, extract_mentions_batch
    from eoip.graphbuild.linkprediction import LinkPredictionConfig, score_pairs
    from eoip.graphbuild.modes import plan_construction
    from eoip.graphbuild.repair import repair_report
    from eoip.graphbuild.rollup import build_hierarchical_rollup
    from eoip.graphbuild.schema import induce_schema
    from eoip.graphbuild.similarity import SimilarityConfig, build_similarity_graph
    from eoip.ingest.profile import profile_records

    router = APIRouter(prefix="/api/v1/graphbuild", tags=["graphbuild"])

    @router.post("/schema/induce")
    def schema_induce(body: dict):
        report = profile_records(body.get("records", []), dataset=body.get("dataset", "dataset"))
        return induce_schema(report, root_class=body.get("root_class")).model_dump()

    @router.post("/plan")
    def plan(body: dict):
        return plan_construction(
            body.get("mode", "hybrid"),
            body.get("dataset", "dataset"),
            ontology_classes=body.get("ontology_classes"),
        ).model_dump()

    @router.post("/cochange", response_model=GraphDelta)
    def cochange(body: dict):
        return build_cochange_edges(body.get("commits", []), CoChangeConfig(**body.get("config", {})))

    @router.post("/inclusion-dependencies", response_model=GraphDelta)
    def inclusion_dependencies(body: dict):
        return discover_inclusion_dependencies(
            {k: v for k, v in body.get("columns", {}).items()},
            InclusionDependencyConfig(**body.get("config", {})),
        )

    @router.post("/mentions", response_model=GraphDelta)
    def mentions(body: dict):
        gazetteer = Gazetteer(
            entities=body.get("entities", {}),
            aliases={k.casefold(): v for k, v in body.get("aliases", {}).items()},
        )
        return extract_mentions_batch(body.get("documents", {}), gazetteer)

    @router.post("/hierarchy", response_model=GraphDelta)
    def hierarchy(body: dict):
        return induce_hierarchy(body.get("records", []), HierarchyConfig(**body.get("config", {})))

    @router.post("/rollup")
    def rollup(body: dict):
        return build_hierarchical_rollup(
            {k: set(v) for k, v in body.get("adjacency", {}).items()},
            base_partition=body.get("base_partition"),
            max_levels=int(body.get("max_levels", 4)),
        ).model_dump()

    @router.post("/similarity", response_model=GraphDelta)
    def similarity(body: dict):
        return build_similarity_graph(body.get("embeddings", {}), SimilarityConfig(**body.get("config", {})))

    @router.post("/link-prediction", response_model=GraphDelta)
    def link_prediction(body: dict):
        return score_pairs(
            {k: set(v) for k, v in body.get("adjacency", {}).items()},
            LinkPredictionConfig(**body.get("config", {})),
        )

    @router.post("/repair")
    def repair(body: dict):
        return repair_report(set(body.get("vertices", [])), body.get("edges", [])).model_dump()

    return router


def build_adapters_router():
    """Router for the §6 backend catalog (SR-GDB-002 manifests).

    Routes: ``GET /api/v1/adapters/``, ``GET /api/v1/adapters/{backend}``,
    ``GET /api/v1/adapters/{backend}/statements`` (AGE/Janus statement preview).
    """
    from fastapi import APIRouter, HTTPException

    from eoip.adapters.catalog import CatalogError, default_catalog

    router = APIRouter(prefix="/api/v1/adapters", tags=["adapters"])
    catalog = default_catalog()

    @router.get("")
    def list_adapters(category: str | None = None, tier: str | None = None, role: str | None = None):
        return catalog.manifest_dicts(category=category, tier=tier, role=role)

    @router.get("/{backend}")
    def get_adapter(backend: str):
        try:
            return catalog.get(backend).model_dump()
        except CatalogError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @router.get("/{backend}/statements")
    def statements(backend: str):
        if backend != "apache_age":
            raise HTTPException(status_code=400, detail="statement preview is available for apache_age only")
        from eoip.adapters.apache_age import ApacheAGEStore

        return ApacheAGEStore(graph="eoip").statements()

    return router
