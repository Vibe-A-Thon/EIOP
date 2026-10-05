"""Extended capability router wiring the new eoip.* modules into the API.

Exposes, under ``/api/v1``:
- Federation (GAP-FABRIC-001..008): source registry + federated query planner.
- Truth model (GAP-TRUTH-001..010): claims, contradictions, resolution,
  assertions, explanation, export.
- Knowledge products (GAP-KP-001..005): catalog CRUD, lifecycle transitions,
  lineage, export/import.
- Query intelligence (GAP-QI-001..008): plan explain, cost estimation,
  history, slow-query report, saved templates with safe binding.
- Faceted search (GAP-SEARCH-001..002): keyword search with facet aggregation.
- Graph test framework (GAP-GRAPHTEST-001..011): declarative graph assertions.
- SKOS taxonomy (GAP-TAX-001, GAP-GOV-003): schemes, concepts, mappings,
  integrity validation, JSON-LD export.
- Retrieval strategies (GAP-RET-002/003/006): keyword / vector / hybrid
  retrieval with ranking trace.
"""

from __future__ import annotations

import json
from typing import Any

from eoip.catalog.products import (
    KnowledgeProduct,
    KnowledgeProductCatalog,
    ProductNotFoundError,
    ProductState,
    ProductValidationError,
)
from eoip.contracts.query_plan import QueryPlan
from eoip.federation import (
    FederatedQueryPlanner,
    HugeGraphLocalAdapter,
    InMemoryDemoAdapter,
    SourceCapability,
    SourceMode,
)
from eoip.graphtest.framework import GraphTestRunner, load_suite
from eoip.graph.store import GraphStore
from eoip.ontology.skos import MappingKind, SkosTaxonomy
from eoip.query.intelligence import QueryIntelligence, TemplateBindingError
from eoip.retrieval.service import retrieve
from eoip.retrieval.vectors import build_search_index
from eoip.search import FacetedSearch, SearchRequest, SearchResponse
from eoip.truth import Claim, TruthStore
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel, Field, ValidationError


class ExtendedState:
    """App-state holders for the extended capabilities."""

    def __init__(self, store: GraphStore) -> None:
        self.truth_store = TruthStore()
        self.catalog = KnowledgeProductCatalog(store)
        self.query_intel = QueryIntelligence(store)
        self.faceted_search = FacetedSearch(store)
        self.skos = SkosTaxonomy()
        self.planner = FederatedQueryPlanner()
        self.planner.register(
            InMemoryDemoAdapter(
                SourceCapability(
                    source_id="demo-memory",
                    entity_types=["WorkItem", "Commit"],
                    pushdown_filters=True,
                    pushdown_projection=True,
                    mode=SourceMode.MATERIALIZED,
                ),
                rows=[
                    {
                        "entity_type": "WorkItem",
                        "canonical_id": "urn:eoip:demo:workitem:FED-1",
                        "issue_key": "FED-1",
                        "summary": "Federated demo work item",
                    },
                    {
                        "entity_type": "Commit",
                        "canonical_id": "urn:eoip:demo:commit:fed0001",
                        "commit_sha": "fed0001",
                        "message": "Federated demo commit",
                    },
                ],
            )
        )
        self.planner.register(
            HugeGraphLocalAdapter(
                SourceCapability(
                    source_id="hugegraph-local",
                    entity_types=list(_store_labels(store)),
                    pushdown_filters=False,
                    pushdown_projection=False,
                    mode=SourceMode.HYBRID,
                    locality=1.0,
                ),
                store,
            )
        )


def _store_labels(store: GraphStore) -> list[str]:
    labels: set[str] = set()
    for vertex in store.find_vertices(limit=50_000):
        labels.add(vertex["label"])
    return sorted(labels)


class FederationQueryRequest(BaseModel):
    entity_types: list[str] = Field(default_factory=list, max_length=50)
    filters: dict[str, Any] = Field(default_factory=dict)
    projection: list[str] = Field(default_factory=list, max_length=50)
    merge_key: str = "canonical_id"


class TruthResolveRequest(BaseModel):
    subject_id: str = Field(min_length=1, max_length=512)
    predicate: str = Field(min_length=1, max_length=256)
    policy: str = "highest-authority"
    adjudicator: str | None = None
    manual_choice: str | None = None


class CatalogTransitionRequest(BaseModel):
    to_state: str = Field(min_length=1, max_length=64)


class SkosSchemeRequest(BaseModel):
    title: str = Field(min_length=1, max_length=512)
    description: str = ""
    scheme_id: str | None = None


class SkosConceptRequest(BaseModel):
    scheme_id: str = Field(min_length=1, max_length=256)
    pref_label: str = Field(min_length=1, max_length=512)
    concept_id: str | None = None
    definition: str = ""
    notation: str = ""
    alt_labels: list[str] = Field(default_factory=list, max_length=100)
    hidden_labels: list[str] = Field(default_factory=list, max_length=100)


class SkosMappingRequest(BaseModel):
    source_id: str = Field(min_length=1, max_length=256)
    target_id: str = Field(min_length=1, max_length=256)
    kind: MappingKind


class TemplateSaveRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    intent: str = Field(min_length=1, max_length=64)
    anchor_params: list[str] = Field(min_length=1, max_length=20)
    description: str = ""
    filters_template: dict | None = None
    relationship_allowlist: list[str] | None = None
    max_depth: int = Field(default=3, ge=1, le=8)
    result_limit: int = Field(default=50, ge=1, le=500)
    timeout_ms: int = Field(default=5000, ge=50, le=30000)
    evidence_mode: str = "SUMMARY"
    created_by: str = "system"


class TemplateBindRequest(BaseModel):
    params: dict[str, str] = Field(default_factory=dict)


class RetrievalSearchRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2048)
    canonical_id: str | None = None
    strategy: str | None = Field(
        default=None, pattern="^(keyword|vector|hybrid)$"
    )
    top_k: int = Field(default=10, ge=1, le=100)


def _raise_skos(exc: Exception) -> None:
    if isinstance(exc, KeyError):
        raise HTTPException(status_code=404, detail=str(exc.args[0] if exc.args else exc))
    if isinstance(exc, ValueError) and "already exists" in str(exc):
        raise HTTPException(status_code=409, detail=str(exc))
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=422, detail=str(exc))
    raise exc


def build_extended_router(store: GraphStore) -> tuple[APIRouter, ExtendedState]:
    """Build the extended-capability router and its app-state holders."""
    state = ExtendedState(store)
    router = APIRouter()

    # -- Federation (GAP-FABRIC-001..008) -----------------------------------

    @router.get("/api/v1/federation/sources")
    def federation_sources() -> dict[str, Any]:
        """GAP-FABRIC-001: registered federated source capabilities."""
        return {
            "sources": [cap.model_dump() for cap in state.planner.sources()]
        }

    @router.post("/api/v1/federation/query")
    def federation_query(payload: FederationQueryRequest) -> dict[str, Any]:
        """GAP-FABRIC-002..007: execute a federated query, returning merged
        rows plus the explainable routing plan."""
        return state.planner.execute(
            entity_types=payload.entity_types,
            filters=payload.filters,
            projection=payload.projection,
            merge_key=payload.merge_key,
        )

    # -- Truth model (GAP-TRUTH-001..010) ------------------------------------

    @router.post("/api/v1/truth/claims", status_code=201)
    def truth_add_claim(claim: Claim) -> Claim:
        """GAP-TRUTH-001: register a claim (immutable, conflict-preserving)."""
        try:
            return state.truth_store.add_claim(claim)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))

    @router.get("/api/v1/truth/contradictions")
    def truth_contradictions() -> dict[str, Any]:
        """GAP-TRUTH-006: all conflicting (subject, predicate) claim groups."""
        groups = state.truth_store.contradictions()
        return {
            "contradictions": [
                {
                    "subject_id": subject_id,
                    "predicate": predicate,
                    "claims": [c.model_dump() for c in claims],
                }
                for (subject_id, predicate), claims in sorted(groups.items())
            ]
        }

    @router.post("/api/v1/truth/resolve")
    def truth_resolve(payload: TruthResolveRequest) -> dict[str, Any]:
        """GAP-TRUTH-007/008: resolve conflicting claims into a canonical
        assertion using a policy (or manual adjudication)."""
        try:
            decision = state.truth_store.resolve(
                payload.subject_id,
                payload.predicate,
                policy=payload.policy,
                adjudicator=payload.adjudicator,
                manual_choice=payload.manual_choice,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        return decision.model_dump()

    @router.get("/api/v1/truth/assertions/{subject_id}/{predicate}")
    def truth_assertion(subject_id: str, predicate: str) -> dict[str, Any]:
        """GAP-TRUTH-003: the canonical assertion for a (subject, predicate)."""
        assertion = state.truth_store.get_assertion(subject_id, predicate)
        if assertion is None:
            raise HTTPException(
                status_code=404,
                detail=f"No canonical assertion for {subject_id} {predicate}",
            )
        return assertion.model_dump()

    @router.get("/api/v1/truth/explain/{subject_id}/{predicate}")
    def truth_explain(subject_id: str, predicate: str) -> dict[str, Any]:
        """GAP-TRUTH-010: why this fact was selected."""
        return state.truth_store.explain(subject_id, predicate)

    @router.get("/api/v1/truth/export")
    def truth_export() -> Response:
        """GAP-TRUTH-005: deterministic JSON snapshot of the truth store."""
        return Response(
            content=state.truth_store.export(),
            media_type="application/json",
        )

    # -- Knowledge products (GAP-KP-001..005) --------------------------------

    @router.get("/api/v1/catalog/products")
    def catalog_list_products(
        owner: str | None = None,
        domain: str | None = None,
        state_filter: str | None = Query(default=None, alias="state"),
        access_policy: str | None = None,
        consumer: str | None = None,
    ) -> dict[str, Any]:
        """GAP-KP-003: list knowledge products with optional filters."""
        try:
            products = state.catalog.list(
                owner=owner,
                domain=domain,
                state=state_filter,
                access_policy=access_policy,
                consumer=consumer,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        return {"products": [p.model_dump() for p in products]}

    @router.post("/api/v1/catalog/products", status_code=201)
    def catalog_create_product(product: KnowledgeProduct) -> KnowledgeProduct:
        """GAP-KP-001: create a knowledge product (assigns canonical id)."""
        try:
            return state.catalog.create(product)
        except ProductValidationError as exc:
            raise HTTPException(status_code=422, detail=str(exc))

    @router.get("/api/v1/catalog/products/{product_id}")
    def catalog_get_product(product_id: str) -> KnowledgeProduct:
        """GAP-KP-001: fetch one knowledge product."""
        try:
            return state.catalog.get(product_id)
        except ProductNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc.args[0] if exc.args else exc))

    @router.put("/api/v1/catalog/products/{product_id}")
    def catalog_update_product(product_id: str, product: KnowledgeProduct) -> KnowledgeProduct:
        """GAP-KP-001: update mutable fields of a knowledge product."""
        product.product_id = product_id
        try:
            return state.catalog.update(product)
        except ProductNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc.args[0] if exc.args else exc))
        except ProductValidationError as exc:
            raise HTTPException(status_code=422, detail=str(exc))

    @router.delete("/api/v1/catalog/products/{product_id}")
    def catalog_delete_product(product_id: str) -> dict[str, Any]:
        """GAP-KP-001: tombstone a knowledge product."""
        try:
            deleted = state.catalog.delete(product_id)
        except ProductNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc.args[0] if exc.args else exc))
        return {"product_id": product_id, "deleted": deleted}

    @router.post("/api/v1/catalog/products/{product_id}/transition")
    def catalog_transition_product(
        product_id: str, payload: CatalogTransitionRequest
    ) -> KnowledgeProduct:
        """GAP-KP-002: apply a lifecycle state transition."""
        try:
            return state.catalog.transition(product_id, ProductState(payload.to_state))
        except ProductNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc.args[0] if exc.args else exc))
        except (ProductValidationError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc))

    @router.get("/api/v1/catalog/products/{product_id}/lineage")
    def catalog_product_lineage(product_id: str) -> dict[str, Any]:
        """GAP-KP-005: source graphs -> product -> consumers lineage."""
        try:
            return state.catalog.lineage(product_id)
        except ProductNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc.args[0] if exc.args else exc))

    @router.get("/api/v1/catalog/products/{product_id}/export")
    def catalog_export_product(product_id: str) -> Response:
        """GAP-KP-004: export one product definition as JSON."""
        try:
            payload = state.catalog.export_json(product_id)
        except ProductNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc.args[0] if exc.args else exc))
        return Response(content=payload, media_type="application/json")

    @router.post("/api/v1/catalog/products/import", status_code=201)
    def catalog_import_product(product: KnowledgeProduct) -> KnowledgeProduct:
        """GAP-KP-004: import a product definition (upserts by canonical id)."""
        try:
            return state.catalog.import_json(product.model_dump())
        except (ProductValidationError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc))

    # -- Query intelligence (GAP-QI-001..008) --------------------------------

    @router.post("/api/v1/query/explain")
    def query_explain(plan: QueryPlan) -> dict[str, Any]:
        """GAP-QI-001: explain a query plan (steps, fanout, indexes, risks)."""
        return state.query_intel.explain(plan).model_dump()

    @router.post("/api/v1/query/cost")
    def query_cost(plan: QueryPlan) -> dict[str, Any]:
        """GAP-QI-002: heuristic cost estimate for a query plan."""
        return state.query_intel.cost(plan).model_dump()

    @router.get("/api/v1/query/history")
    def query_history() -> dict[str, Any]:
        """GAP-QI-003: recorded query history entries."""
        return {
            "history": [entry.model_dump() for entry in state.query_intel.history]
        }

    @router.get("/api/v1/query/slow")
    def query_slow(
        threshold_ms: float = Query(default=1000.0, ge=0.0),
        top_n: int = Query(default=10, ge=1, le=100),
    ) -> dict[str, Any]:
        """GAP-QI-004/005: slow-query report with top-N and index suggestions."""
        return state.query_intel.slow_queries(
            threshold_ms=threshold_ms, top_n=top_n
        ).model_dump()

    @router.get("/api/v1/query/templates")
    def query_list_templates() -> dict[str, Any]:
        """GAP-QI-007: list saved parameterized query templates."""
        return {
            "templates": [t.model_dump() for t in state.query_intel.list_templates()]
        }

    @router.post("/api/v1/query/templates", status_code=201)
    def query_save_template(template: TemplateSaveRequest) -> dict[str, Any]:
        """GAP-QI-007: save a query template (policy-validated on bind)."""
        try:
            saved = state.query_intel.save_template(
                template.name,
                template.intent,
                template.anchor_params,
                description=template.description,
                filters_template=template.filters_template,
                relationship_allowlist=template.relationship_allowlist,
                max_depth=template.max_depth,
                result_limit=template.result_limit,
                timeout_ms=template.timeout_ms,
                evidence_mode=template.evidence_mode,
                created_by=template.created_by,
            )
        except TemplateBindingError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        return saved.model_dump()

    @router.get("/api/v1/query/templates/{template_id}")
    def query_get_template(template_id: str) -> dict[str, Any]:
        """GAP-QI-007: fetch one saved query template."""
        try:
            return state.query_intel.get_template(template_id).model_dump()
        except TemplateBindingError as exc:
            raise HTTPException(status_code=404, detail=str(exc))

    @router.delete("/api/v1/query/templates/{template_id}")
    def query_delete_template(template_id: str) -> dict[str, Any]:
        """GAP-QI-007: delete a saved query template."""
        deleted = state.query_intel.delete_template(template_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Unknown template: {template_id}")
        return {"template_id": template_id, "deleted": deleted}

    @router.post("/api/v1/query/templates/{template_id}/bind")
    def query_bind_template(
        template_id: str, payload: TemplateBindRequest
    ) -> dict[str, Any]:
        """GAP-QI-007/008: bind named parameters into a validated QueryPlan."""
        try:
            template = state.query_intel.get_template(template_id)
            plan = state.query_intel.bind_template(template, payload.params)
        except TemplateBindingError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        return plan.model_dump()

    # -- Faceted search (GAP-SEARCH-001..002) ---------------------------------

    @router.post("/api/v1/search/faceted", response_model=SearchResponse)
    def search_faceted(request: SearchRequest) -> SearchResponse:
        """GAP-SEARCH-001/002: keyword search with semantic facet aggregation;
        every hit preserves graph identity and provenance pointers."""
        return state.faceted_search.search(request)

    # -- Graph test framework (GAP-GRAPHTEST-001..011) -------------------------

    @router.post("/api/v1/graph-tests/run")
    def graph_tests_run(suite: dict[str, Any]) -> dict[str, Any]:
        """GAP-GRAPHTEST-004: run a declarative graph-assertion suite and
        return the machine-readable report (200 even when assertions fail)."""
        try:
            loaded = load_suite(suite)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        report = GraphTestRunner(store).run(loaded)
        return report.to_dict()

    # -- SKOS taxonomy (GAP-TAX-001, GAP-GOV-003) ------------------------------

    @router.post("/api/v1/taxonomy/schemes", status_code=201)
    def taxonomy_create_scheme(payload: SkosSchemeRequest) -> dict[str, Any]:
        """GAP-TAX-001: create a SKOS ConceptScheme."""
        try:
            scheme = state.skos.create_scheme(
                payload.title, payload.description, payload.scheme_id
            )
        except ValueError as exc:
            _raise_skos(exc)
        return scheme.model_dump()

    @router.get("/api/v1/taxonomy/schemes")
    def taxonomy_list_schemes() -> dict[str, Any]:
        """GAP-TAX-001: list SKOS ConceptSchemes."""
        return {
            "schemes": [s.model_dump() for s in state.skos.schemes.values()]
        }

    @router.post("/api/v1/taxonomy/concepts", status_code=201)
    def taxonomy_add_concept(payload: SkosConceptRequest) -> dict[str, Any]:
        """GAP-TAX-001: add a SKOS Concept to a scheme."""
        try:
            concept = state.skos.add_concept(
                payload.scheme_id,
                payload.pref_label,
                concept_id=payload.concept_id,
                definition=payload.definition,
                notation=payload.notation,
                alt_labels=payload.alt_labels,
                hidden_labels=payload.hidden_labels,
            )
        except (ValueError, KeyError) as exc:
            _raise_skos(exc)
        return concept.model_dump()

    @router.get("/api/v1/taxonomy/concepts")
    def taxonomy_list_concepts(scheme: str | None = None) -> dict[str, Any]:
        """GAP-TAX-001: list SKOS Concepts, optionally filtered by scheme."""
        concepts = list(state.skos.concepts.values())
        if scheme is not None:
            concepts = [c for c in concepts if c.scheme_id == scheme]
        return {
            "concepts": [c.model_dump() for c in sorted(concepts, key=lambda c: c.concept_id)]
        }

    @router.post("/api/v1/taxonomy/mappings", status_code=201)
    def taxonomy_add_mapping(payload: SkosMappingRequest) -> dict[str, Any]:
        """GAP-GOV-003: crosswalk mapping between two concepts."""
        try:
            mapping = state.skos.add_mapping(
                payload.source_id, payload.target_id, payload.kind
            )
        except (ValueError, KeyError) as exc:
            _raise_skos(exc)
        return mapping.model_dump()

    @router.get("/api/v1/taxonomy/mappings")
    def taxonomy_list_mappings() -> dict[str, Any]:
        """GAP-GOV-003: list concept crosswalk mappings."""
        return {
            "mappings": [m.model_dump() for m in state.skos.mappings]
        }

    @router.get("/api/v1/taxonomy/validate")
    def taxonomy_validate(scheme: str | None = None) -> dict[str, Any]:
        """GAP-TAX-001: SKOS integrity issues and prefLabel conflicts."""
        return {
            "integrity_issues": [
                issue.model_dump()
                for issue in state.skos.validate_integrity(scheme)
            ],
            "label_conflicts": [
                conflict.model_dump()
                for conflict in state.skos.detect_label_conflicts(scheme)
            ],
        }

    @router.get("/api/v1/taxonomy/export.rdf")
    def taxonomy_export_rdf() -> Response:
        """GAP-TAX-001: export the taxonomy as SKOS JSON-LD."""
        return Response(
            content=json.dumps(state.skos.export_rdf(), indent=2, sort_keys=True),
            media_type="application/ld+json",
        )

    # -- Retrieval strategies (GAP-RET-002/003/006) ----------------------------

    @router.post("/api/v1/retrieval/search")
    def retrieval_search(payload: RetrievalSearchRequest) -> dict[str, Any]:
        """GAP-RET-002/003/006: keyword / vector / hybrid retrieval with
        evidence-quality re-ranking and a deterministic trace."""
        index = (
            build_search_index(store)
            if payload.strategy in ("keyword", "vector", "hybrid")
            else None
        )
        try:
            result = retrieve(
                store,
                payload.canonical_id or "",
                payload.question,
                strategy=payload.strategy,
                search_index=index,
                top_k=payload.top_k,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        return result.model_dump()

    # ------------------------------------------------------------------
    # Graph Algorithms (extended)
    # ------------------------------------------------------------------

    class AlgorithmRequest(BaseModel):
        algorithm: str = Field(description="Algorithm name from registry")
        source_id: str | None = None
        target_id: str | None = None
        canonical_ids: list[str] | None = None
        max_depth: int = Field(default=4, ge=1, le=20)
        limit: int = Field(default=20, ge=1, le=500)
        k: int = Field(default=5, ge=1, le=50)
        direction: str = Field(default="outgoing")
        allowed_labels: list[str] | None = None
        blocked_labels: list[str] | None = None

    @router.get("/api/v1/algorithms")
    def list_algorithms():
        from eoip.agents.graph_analytics import ALGORITHM_REGISTRY
        return {"algorithms": sorted(ALGORITHM_REGISTRY.keys()), "count": len(ALGORITHM_REGISTRY)}

    @router.post("/api/v1/algorithms/run")
    def run_algorithm(payload: AlgorithmRequest):
        from eoip.graph.algorithms import GraphAlgorithms
        algo = GraphAlgorithms(store)
        dispatch = {
            "ring_detection": lambda: [r.to_dict() for r in algo.detect_rings(max_length=payload.max_depth, limit=payload.limit)],
            "intersection_detection": lambda: algo.detect_intersection(payload.source_id or "", payload.target_id or "", max_depth=payload.max_depth).to_dict(),
            "weighted_shortest_path": lambda: (r.to_dict() if (r := algo.weighted_shortest_path(payload.source_id or "", payload.target_id or "")) else None),
            "single_source_weighted": lambda: {k: v.to_dict() for k, v in algo.single_source_weighted_paths(payload.source_id or "", limit=payload.limit).items()},
            "k_step_neighbors": lambda: algo.k_step_neighbors(payload.source_id or "", k=payload.k, limit=payload.limit).to_dict(),
            "k_jump": lambda: algo.k_jump(payload.source_id or "", k=payload.k, walks=payload.limit),
            "custom_path": lambda: algo.custom_path(payload.source_id or "", payload.target_id or "", allowed_labels=payload.allowed_labels, blocked_labels=payload.blocked_labels, max_depth=payload.max_depth, max_paths=payload.limit),
            "ray_detection": lambda: algo.ray_detection(payload.source_id or "", direction=payload.direction, edge_labels=payload.allowed_labels, max_depth=payload.max_depth).to_dict(),
            "co_neighbors": lambda: algo.co_neighbors(payload.source_id or "", payload.target_id or "").to_dict(),
            "personal_rank": lambda: algo.personal_rank(payload.source_id or "", limit=payload.limit),
            "neighbor_rank": lambda: algo.neighbor_rank(payload.source_id or "", limit=payload.limit),
            "model_similarity": lambda: algo.model_similarity(payload.canonical_ids[:len(payload.canonical_ids)//2] if payload.canonical_ids else [], payload.canonical_ids[len(payload.canonical_ids)//2:] if payload.canonical_ids else []),
        }
        fn = dispatch.get(payload.algorithm)
        if fn is None:
            raise HTTPException(status_code=400, detail=f"Unknown algorithm: {payload.algorithm}. Available: {sorted(dispatch.keys())}")
        try:
            return {"algorithm": payload.algorithm, "result": fn()}
        except Exception as exc:
            raise HTTPException(status_code=422, detail=str(exc))

    # ------------------------------------------------------------------
    # Query Languages (EOQL, OSQL, Semantic QL)
    # ------------------------------------------------------------------

    class QueryLanguageRequest(BaseModel):
        language: str = Field(description="Query language: eoql, osql, semantic")
        query: str = Field(min_length=1)

    @router.post("/api/v1/query/language")
    def query_language(payload: QueryLanguageRequest):
        from eoip.query.languages import parse_eoql, parse_osql, parse_semantic_query
        dispatch = {
            "eoql": lambda: parse_eoql(store, payload.query),
            "osql": lambda: parse_osql(store, payload.query),
            "semantic": lambda: parse_semantic_query(store, payload.query),
        }
        fn = dispatch.get(payload.language.lower())
        if fn is None:
            raise HTTPException(status_code=400, detail=f"Unknown language: {payload.language}. Available: {sorted(dispatch.keys())}")
        return fn()

    # ------------------------------------------------------------------
    # Format Export (extended with SHACL, PGQL, OpenCypher)
    # ------------------------------------------------------------------

    @router.get("/api/v1/export/formats")
    def list_export_formats():
        return {"formats": ["rdf", "rdf_xml", "rdfs", "owl", "gremlin", "cypher", "opencypher", "gql", "sparql", "shacl", "pgql"]}

    # ------------------------------------------------------------------
    # Semantic Pipeline
    # ------------------------------------------------------------------

    class SemanticPipelineRequest(BaseModel):
        stages: list[str] | None = None
        scope: dict[str, str] | None = None

    @router.post("/api/v1/admin/semantic-pipeline")
    def run_semantic_pipeline(payload: SemanticPipelineRequest):
        from eoip.ingestion.semantic_pipeline import PipelineStage, SemanticPipeline
        pipeline = SemanticPipeline(store)
        stages = None
        if payload.stages:
            stages = []
            for s in payload.stages:
                try:
                    stages.append(PipelineStage(s))
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Unknown stage: {s}. Available: {[ps.value for ps in PipelineStage]}")
        result = pipeline.run(stages=stages, scope=payload.scope or {})
        return result.to_dict()

    @router.get("/api/v1/admin/semantic-pipeline/stages")
    def list_pipeline_stages():
        from eoip.ingestion.semantic_pipeline import PipelineStage
        return {"stages": [ps.value for ps in PipelineStage]}

    # ------------------------------------------------------------------
    # Agent-Driven Analytics
    # ------------------------------------------------------------------

    class AgentAnalyticsRequest(BaseModel):
        algorithm: str = Field(default="all", description="Algorithm name or 'all' for swarm")
        context_refs: list[str] = Field(default_factory=list)
        budgets: dict[str, int] = Field(default_factory=dict)

    @router.post("/api/v1/agents/analytics")
    def run_analytics_agent(payload: AgentAnalyticsRequest):
        from eoip.agents.graph_analytics import GraphAnalyticsAgent
        from eoip.contracts.agent import AgentRequest
        agent = GraphAnalyticsAgent()
        request = AgentRequest(
            request_id=f"api-analytics-{id(payload)}",
            goal=payload.algorithm,
            context_refs=payload.context_refs,
            budgets=payload.budgets or None,
        )
        result = agent.execute(request, store)
        return result.model_dump() if hasattr(result, "model_dump") else {"status": result.status, "summary": result.summary, "data": result.data}

    @router.post("/api/v1/agents/semantic-index")
    def run_semantic_index_agent(payload: AgentAnalyticsRequest):
        from eoip.agents.semantic_index import SemanticIndexAgent
        from eoip.contracts.agent import AgentRequest
        agent = SemanticIndexAgent()
        request = AgentRequest(
            request_id=f"api-semantic-{id(payload)}",
            goal=payload.algorithm,
            context_refs=payload.context_refs,
            budgets=payload.budgets or None,
        )
        result = agent.execute(request, store)
        return result.model_dump() if hasattr(result, "model_dump") else {"status": result.status, "summary": result.summary, "data": result.data}

    return router, state


def ensure_extended(app, store: GraphStore) -> None:
    """Idempotently attach the extended router/state to an app that does not
    already carry them (used by the deployment factory in main.py, which
    builds on top of apps.api.app.create_app)."""
    if getattr(app.state, "extended_state", None) is not None:
        return
    router, state = build_extended_router(store)
    app.state.extended_state = state
    app.include_router(router)
