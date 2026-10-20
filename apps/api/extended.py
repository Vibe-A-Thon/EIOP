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

import glob
import json
import os
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml
from eoip.audit.sink import AuditSink
from eoip.authn import AuthenticationError, LocalIdentityProvider, TokenService
from eoip.authz import PolicyEnforcer, RoleRegistry, UserStore
from eoip.branding.content import LegalContentRegistry
from eoip.branding.localization import LocalizationRegistry
from eoip.branding.router import build_router as build_branding_router
from eoip.branding.terminology import TerminologyRegistry
from eoip.branding.theme import ThemePackage, ThemeRegistry
from eoip.catalog.products import (
    KnowledgeProduct,
    KnowledgeProductCatalog,
    ProductNotFoundError,
    ProductState,
    ProductValidationError,
)
from eoip.ci import KGCIPipeline
from eoip.ci.pipeline import FAIL_ON_CHOICES
from eoip.compliance.router import build_router as build_compliance_router
from eoip.config.layered import ConfigStore, FeatureFlagStore, FileConfigPersistence
from eoip.config.router import build_router as build_config_router
from eoip.contracts.query_plan import QueryPlan
from eoip.egress.gateway import EgressGateway
from eoip.egress.router import build_router as build_egress_router
from eoip.federation import (
    FederatedQueryPlanner,
    LocalGraphStoreAdapter,
    SourceCapability,
    SourceMode,
)
from eoip.graph.store import GraphStore
from eoip.graphtest.framework import GraphTestRunner, load_suite
from eoip.ingest.profile import build_router as build_ingest_profile_router
from eoip.licensing.api import build_router as build_licensing_router
from eoip.licensing.entitlements import EntitlementChecker
from eoip.licensing.license_file import LicensePayload, sign_license, verify_license
from eoip.licensing.meter import UsageMeter
from eoip.loops.router import build_router as build_loops_router
from eoip.marketplace import (
    DependencyConflict,
    IntegrityError,
    PackageInstaller,
    PackageRegistry,
)
from eoip.models.embeddings import build_embedding_provider
from eoip.models.governance import (
    Feature,
    GovernancePolicy,
    HallucinationIncidentLog,
    KillSwitch,
    ModelEntry,
    ModelOutput,
    ModelRegistry,
    PromptTemplate,
    PromptTemplateRegistry,
)
from eoip.observability.metrics import Registry as MetricsRegistry
from eoip.observability.metrics import record_request
from eoip.ontology.manifest import VERTEX_LABELS
from eoip.ontology.packs import (
    DEFAULT_PACKS_DIR,
    METADATA_FILENAME,
    list_installed_packs,
    load_metadata,
    load_ontology,
    validate_pack,
)
from eoip.ontology.skos import MappingKind, SkosTaxonomy
from eoip.ops import (
    build_shard_plan,
    collect_support_bundle,
    default_ha_topology,
    helm_release_summary,
    plan_upgrade,
    run_preflight,
)
from eoip.privacy.router import build_router as build_privacy_router
from eoip.qa.router import build_router as build_qa_router
from eoip.query.intelligence import QueryIntelligence, TemplateBindingError
from eoip.reports.router import build_router as build_reports_router
from eoip.retrieval.service import retrieve
from eoip.retrieval.vectors import HashingEmbedder, build_search_index
from eoip.search import FacetedSearch, SearchRequest, SearchResponse
from eoip.suggest.router import build_router as build_suggest_router
from eoip.systems.router import build_systems_router
from eoip.tenancy.router import build_router as build_tenancy_router
from eoip.tenancy.service import TenancyService
from eoip.truth import Claim, TruthStore
from fastapi import APIRouter, Body, HTTPException, Query, Response
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, ValidationError

_DEFAULT_POLICY_YAML = """
policies:
  - id: admin-full-access
    role: admin
    permission: admin:*
    description: admins may perform any action
  - id: steward-publish
    role: steward
    permission: ontology:publish
  - id: steward-agents
    role: steward
    permission: agents:approve
  - id: analyst-read
    role: analyst
    permission: graph:read
  - id: viewer-read
    role: viewer
    permission: graph:read
"""


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
            LocalGraphStoreAdapter(
                SourceCapability(
                    source_id=_store_source_id(store),
                    adapter_kind="hugegraph",
                    entity_types=list(_store_labels(store)),
                    pushdown_filters=False,
                    pushdown_projection=False,
                    mode=SourceMode.HYBRID,
                    locality=1.0,
                ),
                store,
            )
        )
        self._init_pass2(Path(os.getenv("EOIP_DATA_DIR", ".data")))
        self._init_sr_wave(Path(os.getenv("EOIP_DATA_DIR", ".data")), store)

    def _init_pass2(self, data_dir: Path) -> None:
        state_dir = data_dir / "state"
        state_dir.mkdir(parents=True, exist_ok=True)
        # -- AuthN / AuthZ (GAP-SEC-001..006, CP-03) ------------------------
        self.identity_provider = LocalIdentityProvider()
        self.token_service = TokenService()
        self.role_registry = RoleRegistry(storage_path=state_dir / "roles.json")
        self.user_store = UserStore(storage_path=state_dir / "users.json")
        self.policy_enforcer = PolicyEnforcer()
        self.policy_enforcer.load_yaml(_DEFAULT_POLICY_YAML)
        self.decision_log: list[dict] = []

        # -- Model governance (§49) -------------------------------------------
        self.model_registry = ModelRegistry()
        self.template_registry = PromptTemplateRegistry()
        self.governance_policy = GovernancePolicy(
            groundedness_threshold=float(
                os.getenv("EOIP_GOV_GROUNDEDNESS_THRESHOLD", "0.8")
            ),
            unsafe_action_threshold=float(
                os.getenv("EOIP_GOV_UNSAFE_ACTION_THRESHOLD", "0.1")
            ),
        )
        self.kill_switch = KillSwitch()
        if os.getenv("EOIP_KILL_SWITCH", "").strip().lower() in (
            "1", "true", "off", "disabled",
        ):
            self.kill_switch.disable_all("disabled via EOIP_KILL_SWITCH env")
        incidents_dir = data_dir / "governance"
        incidents_dir.mkdir(parents=True, exist_ok=True)
        self.incident_log = HallucinationIncidentLog(
            incidents_dir / "hallucination-incidents.jsonl"
        )

        # -- Marketplace (GAP-MKT-001..008) ------------------------------------
        self.package_registry = PackageRegistry(
            os.getenv("EOIP_REGISTRY_PATH")
            or str(data_dir / "marketplace-registry.json")
        )
        install_key = os.getenv("EOIP_INSTALL_KEY")
        self.package_installer = PackageInstaller(
            self.package_registry, key=install_key.encode() if install_key else None
        )

        # -- KGCI (GAP-KGCI-001..004) -------------------------------------------
        self.kgci_last_report: dict | None = None

        # -- Metrics (GAP-OBS-003) ------------------------------------------------
        self.metrics = MetricsRegistry()
        self.metrics_renderers: list[Callable[[], str]] = [self.metrics.render]
        self.metrics.counter(
            "http_requests_total",
            "Total HTTP requests handled.",
            ("method", "path", "status"),
        )
        self.metrics.histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds.",
            ("method", "path", "status"),
        )

        # -- Audit sink for the support bundle (§47) -----------------------------
        self.audit_sink = AuditSink(data_dir / "audit")

    def _init_sr_wave(self, data_dir: Path, store: GraphStore) -> None:
        # -- Super-Requirements (SR-*) commercial baseline, pass 9 ----------
        # Each holder mirrors one eoip package's ``build_router`` factory; the
        # routers themselves are mounted in ``build_extended_router`` below.

        # Tenancy (SR-TEN-001/002/003/006/007/009): fail-closed tenant context,
        # isolation models/placement, quotas, lifecycle, hash-chained metering.
        self.tenancy_service = TenancyService(graph_store=store)
        # Runtime per-layer tenant stores (SR-TEN-003) on the same isolation registry; the KMS master
        # key comes from EOIP_TENANT_MASTER_KEY or a 0600 key file created once under the data dir.
        from eoip.tenancy.layers import TenantLayers, load_or_create_master_key

        self.tenant_layers = TenantLayers(
            self.tenancy_service.isolation, root=data_dir / "tenants",
            master_key=lambda: load_or_create_master_key(data_dir / "state" / "tenant-master.key"))

        # Licensing (SR-DEP-007, SR-COM-001, SR-TEN-009): checker from a signed
        # license at EOIP_LICENSE_PATH when present; otherwise a permissive
        # self-signed *development* license (documented default — production
        # installs must ship a vendor-signed license file). Meter is the
        # tamper-evident JSONL usage meter under the data dir.
        license_path = os.getenv("EOIP_LICENSE_PATH", "").strip()
        if license_path and Path(license_path).is_file():
            license_doc = json.loads(Path(license_path).read_text(encoding="utf-8"))
            vendor_key = os.getenv("EOIP_LICENSE_VENDOR_KEY", "eoip-dev-vendor-key")
            self.entitlement_checker = EntitlementChecker(
                verify_license(license_doc, vendor_key)
            )
        else:
            dev_doc = sign_license(
                LicensePayload(
                    customer="EOIP development (default permissive dev license)",
                    edition="enterprise",
                    model="perpetual",
                ),
                "eoip-dev-vendor-key",
            )
            self.entitlement_checker = EntitlementChecker(
                verify_license(dev_doc, "eoip-dev-vendor-key")
            )
        self.usage_meter = UsageMeter(data_dir / "meter")

        state_dir = data_dir / "state"
        state_dir.mkdir(parents=True, exist_ok=True)
        # Layered config (SR-CFG-001..006, CP-03): typed, layered, audited settings
        # plus feature flags. Disk-backed atomic persistence via FileConfigPersistence.
        self.config_store = ConfigStore(
            persistence=FileConfigPersistence(state_dir / "config.json")
        )
        self.feature_flags = FeatureFlagStore(self.config_store)

        # Egress gateway (SR-LLM-010..020, SR-CON-010/011): single policy-gated
        # egress path. No transport is registered by default — external calls
        # are disabled by design until an admin enables an endpoint with
        # consent; dry-run calls still exercise policy + manifests + canaries.
        self.egress_gateway = EgressGateway(tenant_id="platform-default")

        # Branding (SR-WL-001/003/004-partial/006/007, SR-ONT-007, CP-03): default
        # theme, terminology, localization and legal-content registries.
        self.branding_themes = ThemeRegistry(
            default_theme=ThemePackage(
                id="urn:eoip:branding:theme:eoip-default",
                name="EOIP Default",
                app_name="EOIP",
            ),
            storage_path=state_dir / "themes.json",
        )
        self.branding_terminology = TerminologyRegistry()
        self.branding_locales = LocalizationRegistry()
        self.branding_legal = LegalContentRegistry()


def _store_labels(store: GraphStore) -> list[str]:
    labels: set[str] = set()
    for vertex in store.find_vertices(limit=50_000):
        labels.add(vertex["label"])
    return sorted(labels or set(VERTEX_LABELS))


def _store_source_id(store: GraphStore) -> str:
    try:
        ping = store.ping()
    except Exception:  # noqa: BLE001 - backend discovery must not break router setup
        ping = {}
    backend = ping.get("backend") if isinstance(ping, dict) else None
    if backend == "memory":
        return "hugegraph-local"
    return f"{backend or 'graph'}-local"


class FederationQueryRequest(BaseModel):
    entity_types: list[str] = Field(default_factory=list, max_length=50)
    filters: dict[str, Any] = Field(default_factory=dict)
    projection: list[str] = Field(default_factory=list, max_length=50)
    merge_key: str = "canonical_id"
    policy_context: dict[str, Any] = Field(default_factory=dict)


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


class QueryLanguageRequest(BaseModel):
    language: str = Field(description="Query language: eoql, osql, semantic")
    query: str = Field(min_length=1)


class SemanticPipelineRequest(BaseModel):
    stages: list[str] | None = None
    scope: dict[str, str] | None = None


class AgentAnalyticsRequest(BaseModel):
    algorithm: str = Field(default="all", description="Algorithm name or 'all' for swarm")
    context_refs: list[str] = Field(default_factory=list)
    budgets: dict[str, int] = Field(default_factory=dict)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=256)
    password: str = Field(min_length=1, max_length=256)


class AuthzUserRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=512)
    roles: list[str] = Field(default_factory=list, max_length=50)
    attributes: dict[str, Any] = Field(default_factory=dict)


class AuthzRoleRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str = ""
    permissions: list[str] = Field(default_factory=list, max_length=100)


class AuthzEvaluateRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=512)
    action: str = Field(min_length=1, max_length=256)
    resource_attrs: dict[str, Any] = Field(default_factory=dict)


class KillSwitchRequest(BaseModel):
    enabled: bool
    reason: str = ""


class KillSwitchFeatureRequest(BaseModel):
    enabled: bool
    reason: str = ""


class UpgradePlanRequest(BaseModel):
    current_version: str = Field(min_length=1, max_length=64)
    target_version: str = Field(min_length=1, max_length=64)
    current_manifest: dict[str, Any] | None = None
    target_manifest: dict[str, Any] | None = None


class KGCIRunRequest(BaseModel):
    ontology_dir: str | None = None
    fail_on: str = "any"


class ShardPlanRequest(BaseModel):
    entity_count: int = Field(ge=0)
    shard_count: int = Field(default=3, ge=1, le=1024)
    strategy: str = Field(default="canonical_hash", min_length=1, max_length=64)


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
            policy_context=payload.policy_context,
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
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=422, detail=str(exc))


    # ------------------------------------------------------------------
    # Query Languages (EOQL, OSQL, Semantic QL)
    # ------------------------------------------------------------------

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

    @router.post("/api/v1/agents/analytics")
    def run_analytics_agent(payload: AgentAnalyticsRequest):
        from eoip.agents.graph_analytics import GraphAnalyticsAgent
        from eoip.contracts.agent import AgentRequest
        agent = GraphAnalyticsAgent()
        request = AgentRequest(
            request_id=f"api-analytics-{id(payload)}",
            agent_id="graph-analytics",
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
            agent_id="semantic-index",
            goal=payload.algorithm,
            context_refs=payload.context_refs,
            budgets=payload.budgets or None,
        )
        result = agent.execute(request, store)
        return result.model_dump() if hasattr(result, "model_dump") else {"status": result.status, "summary": result.summary, "data": result.data}

    # -- AuthN / AuthZ (GAP-SEC-001..006) --------------------------------------

    @router.post("/api/v1/auth/login")
    def auth_login(payload: LoginRequest) -> dict[str, str]:
        """GAP-SEC-001/004: exchange username/password for a bearer token.

        Passwords are never logged. Authentication failures return 401."""
        try:
            principal = state.identity_provider.authenticate(
                {"username": payload.username, "password": payload.password}
            )
        except AuthenticationError:
            raise HTTPException(status_code=401, detail="invalid credentials")
        return {"token": state.token_service.issue(principal)}

    @router.get("/api/v1/auth/health")
    def auth_health() -> dict[str, Any]:
        """GAP-SEC-001: identity backend liveness (no secrets exposed)."""
        return state.identity_provider.health()

    # Note: /api/v1/authz/* routes have no local token check, matching the
    # rest of this router; the deployment app (main.py) protects all
    # /api/v1 paths via its bearer-token middleware.

    @router.get("/api/v1/authz/users")
    def authz_list_users() -> dict[str, Any]:
        """GAP-SEC-006: list users in the authorization user store."""
        return {
            "users": [u.to_dict() for u in state.user_store.list_users()]
        }

    @router.post("/api/v1/authz/users", status_code=201)
    def authz_create_user(payload: AuthzUserRequest) -> dict[str, Any]:
        """GAP-SEC-006: create a user with roles (and optional attributes)."""
        try:
            user = state.user_store.create_user(
                payload.user_id, payload.roles, payload.attributes
            )
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc))
        return user.to_dict()

    @router.get("/api/v1/authz/users/export")
    def authz_export_users() -> Response:
        """GAP-SEC-006: deterministic JSON export of the user store."""
        return Response(
            content=state.user_store.export_json(), media_type="application/json"
        )

    @router.get("/api/v1/authz/roles")
    def authz_list_roles() -> dict[str, Any]:
        """GAP-SEC-005: list role definitions."""
        return {"roles": state.role_registry.list_roles()}

    @router.post("/api/v1/authz/roles", status_code=201)
    def authz_create_role(payload: AuthzRoleRequest) -> dict[str, Any]:
        """GAP-SEC-005: create a role with catalog-validated permissions."""
        try:
            return state.role_registry.create_role(
                payload.name,
                description=payload.description,
                permissions=payload.permissions,
            )
        except ValueError as exc:
            status = 409 if "already exists" in str(exc) else 422
            raise HTTPException(status_code=status, detail=str(exc))

    @router.get("/api/v1/authz/roles/export")
    def authz_export_roles() -> Response:
        """GAP-SEC-005: deterministic JSON export of the role registry."""
        return Response(
            content=state.role_registry.export_json(), media_type="application/json"
        )

    @router.get("/api/v1/authz/policies")
    def authz_list_policies() -> dict[str, Any]:
        """GAP-SEC-003: loaded policy-as-code statements."""
        return {
            "policies": [s.to_dict() for s in state.policy_enforcer.statements]
        }

    @router.post("/api/v1/authz/policies/reload")
    def authz_reload_policies(
        policy_yaml: str = Body(media_type="application/yaml"),
        replace_existing: bool = Query(default=False),
    ) -> dict[str, Any]:
        """GAP-SEC-003: load additional policy statements from YAML text."""
        try:
            loaded = (state.policy_enforcer.replace_yaml(policy_yaml) if replace_existing
                      else state.policy_enforcer.load_yaml(policy_yaml))
        except (yaml.YAMLError, KeyError, TypeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        return {"loaded": loaded}

    @router.get("/api/v1/authz/decisions")
    def authz_decisions() -> dict[str, Any]:
        """GAP-SEC-004: audit trail of authorization decisions (audit:read)."""
        return {"decisions": list(state.decision_log)}

    @router.post("/api/v1/authz/evaluate")
    def authz_evaluate(payload: AuthzEvaluateRequest) -> dict[str, Any]:
        """GAP-SEC-004: evaluate (user, action, resource attrs) and record
        the default-deny decision for audit/debugging."""
        user = state.user_store.get_user(payload.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"unknown user: {payload.user_id}")
        decision = state.policy_enforcer.enforce(
            user, payload.action, payload.resource_attrs
        )
        record = decision.to_audit_record()
        state.decision_log.append(record)
        return record

    # -- Model governance (§49) -------------------------------------------------

    @router.get("/api/v1/governance/models")
    def governance_list_models() -> dict[str, Any]:
        """§49.2: registered models with approval state."""
        return {
            "models": [m.model_dump() for m in state.model_registry.list_models()]
        }

    @router.post("/api/v1/governance/models", status_code=201)
    def governance_register_model(entry: ModelEntry) -> dict[str, Any]:
        """§49.2: register a model version."""
        state.model_registry.register(entry)
        return entry.model_dump()

    @router.post("/api/v1/governance/models/{model_id}/approval")
    def governance_approve_model(model_id: str) -> dict[str, Any]:
        """§49.2: approve a registered model."""
        try:
            state.model_registry.approve(model_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        return {"model_id": model_id, "approved": True}

    @router.delete("/api/v1/governance/models/{model_id}/approval")
    def governance_revoke_model(model_id: str) -> dict[str, Any]:
        """§49.2: revoke a model approval."""
        try:
            state.model_registry.revoke(model_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        return {"model_id": model_id, "approved": False}

    @router.get("/api/v1/governance/templates")
    def governance_list_templates() -> dict[str, Any]:
        """§49.3: versioned prompt templates with content hashes."""
        return {
            "templates": [
                t.model_dump() for t in state.template_registry.list_templates()
            ]
        }

    @router.post("/api/v1/governance/templates", status_code=201)
    def governance_register_template(template: PromptTemplate) -> dict[str, Any]:
        """§49.3: register a prompt template version."""
        return state.template_registry.register(template).model_dump()

    @router.get("/api/v1/governance/kill-switch")
    def governance_kill_switch_status() -> dict[str, Any]:
        """§49.6: global + per-feature AI kill switch status."""
        features = {f.value: state.kill_switch.is_enabled(f) for f in Feature}
        return {
            "global_enabled": any(features.values()),
            "features": features,
        }

    @router.post("/api/v1/governance/kill-switch")
    def governance_set_kill_switch(payload: KillSwitchRequest) -> dict[str, Any]:
        """§49.6: enable/disable the global AI kill switch."""
        if payload.enabled:
            state.kill_switch.enable_all()
        else:
            state.kill_switch.disable_all(payload.reason or "disabled via API")
        return {
            "global_enabled": payload.enabled,
            "features": {
                f.value: state.kill_switch.is_enabled(f) for f in Feature
            },
        }

    @router.post("/api/v1/governance/kill-switch/features/{feature}")
    def governance_set_feature_kill_switch(
        feature: str, payload: KillSwitchFeatureRequest
    ) -> dict[str, Any]:
        """§49.6: enable/disable one AI feature (rag, agents, nlq)."""
        try:
            parsed = Feature(feature)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"unknown feature: {feature}; expected one of {[f.value for f in Feature]}",
            )
        if payload.enabled:
            state.kill_switch.enable(parsed)
        else:
            state.kill_switch.disable(parsed, payload.reason)
        return {"feature": parsed.value, "enabled": payload.enabled}

    @router.get("/api/v1/governance/incidents")
    def governance_incidents() -> dict[str, Any]:
        """§49.8: recorded hallucination incidents (append-only JSONL)."""
        return {"incidents": state.incident_log.read_all()}

    @router.post("/api/v1/governance/evaluate")
    def governance_evaluate(output: ModelOutput) -> dict[str, Any]:
        """§49.5: evaluate a scored model output against governance thresholds."""
        return state.governance_policy.evaluate(output).model_dump()

    # -- Marketplace (GAP-MKT-001..008) ------------------------------------------

    @router.get("/api/v1/marketplace/installed")
    def marketplace_installed() -> dict[str, Any]:
        """GAP-MKT-006: installed extension packages."""
        return {
            "packages": [r.to_dict() for r in state.package_registry.list()]
        }

    @router.get("/api/v1/marketplace/installed/search")
    def marketplace_search(q: str = Query(default="", max_length=256)) -> dict[str, Any]:
        """GAP-MKT-006: search installed packages by name/description."""
        return {
            "packages": [r.to_dict() for r in state.package_registry.search(q)]
        }

    @router.post("/api/v1/marketplace/install", status_code=201)
    def marketplace_install(
        package: bytes = Body(media_type="application/zip"),
    ) -> dict[str, Any]:
        """GAP-MKT-005/007: install a raw ``.eoipkg`` archive (zip bytes)."""
        try:
            manifest = state.package_installer.install(package)
        except IntegrityError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        except DependencyConflict as exc:
            raise HTTPException(status_code=409, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        return manifest.model_dump()

    @router.post("/api/v1/marketplace/uninstall/{name}")
    def marketplace_uninstall(name: str) -> dict[str, Any]:
        """GAP-MKT-006: uninstall a package (refuses with dependents)."""
        try:
            removed = state.package_installer.uninstall(name)
        except DependencyConflict as exc:
            raise HTTPException(status_code=409, detail=str(exc))
        if not removed:
            raise HTTPException(status_code=404, detail=f"package not installed: {name}")
        return {"name": name, "uninstalled": True}

    # -- Domain packs (GAP-DP-*) ---------------------------------------------------

    @router.get("/api/v1/ontology/packs")
    def ontology_list_packs() -> dict[str, Any]:
        """GAP-DP-005: metadata for every installed domain pack."""
        return {
            "packs": [m.model_dump() for m in list_installed_packs()]
        }

    @router.get("/api/v1/ontology/packs/{name}")
    def ontology_pack_detail(name: str) -> dict[str, Any]:
        """GAP-DP-005: one domain pack with its validation result.

        404 for unknown packs; 422 (with conflicts) when the pack is invalid."""
        pack_dir = Path(DEFAULT_PACKS_DIR) / name
        if not (pack_dir / METADATA_FILENAME).is_file():
            raise HTTPException(status_code=404, detail=f"unknown domain pack: {name}")
        metadata = load_metadata(pack_dir)
        pack = load_ontology(pack_dir, metadata)
        result = validate_pack(pack)
        detail = {
            "name": metadata.name,
            "valid": result.valid,
            "metadata": metadata.model_dump(),
            "classes": sorted(pack.classes),
            "extensions": list(result.extensions),
            "conflicts": [c.model_dump() for c in result.conflicts],
        }
        if not result.valid:
            raise HTTPException(status_code=422, detail=detail)
        return detail

    # -- KGCI (GAP-KGCI-001..004) ---------------------------------------------------

    @router.post("/api/v1/kgci/run")
    def kgci_run(payload: KGCIRunRequest | None = None) -> dict[str, Any]:
        """GAP-KGCI-001..004: run the deterministic KG CI/CD pipeline
        synchronously and return the aggregate report."""
        payload = payload or KGCIRunRequest()
        if payload.fail_on not in FAIL_ON_CHOICES:
            raise HTTPException(
                status_code=422,
                detail=f"fail_on must be one of {list(FAIL_ON_CHOICES)}",
            )
        pipeline = KGCIPipeline(
            ontology_dir=payload.ontology_dir,
            scan_dirs=["packages/eoip", "config"],
            output_dir=None,
            fail_on=payload.fail_on,
        )
        report = pipeline.run()
        state.kgci_last_report = report.to_dict()
        return state.kgci_last_report

    @router.get("/api/v1/kgci/report")
    def kgci_last_report() -> dict[str, Any]:
        """GAP-KGCI-004: the most recent KGCI report, if any."""
        if state.kgci_last_report is None:
            raise HTTPException(status_code=404, detail="no KGCI report has been run")
        return state.kgci_last_report

    # -- Ops (§47) -----------------------------------------------------------------

    @router.get("/api/v1/ops/preflight")
    def ops_preflight() -> dict[str, Any]:
        """§47: startup/operational preflight checks (env, token config,
        ontology files, graph store, disk, port)."""
        report = run_preflight(
            required_env=[],
            ontology_paths=sorted(glob.glob("config/ontology/*.yaml")),
            graph_store=store,
            token_env="EOIP_API_TOKEN",
            port=8000,
        )
        return report.to_dict()

    @router.post("/api/v1/ops/upgrade-plan")
    def ops_upgrade_plan(payload: UpgradePlanRequest) -> dict[str, Any]:
        """§47: version-to-version upgrade plan with migration classification."""
        return plan_upgrade(
            payload.current_version,
            payload.target_version,
            current_manifest=payload.current_manifest,
            target_manifest=payload.target_manifest,
            graph_store=store,
        )

    @router.get("/api/v1/ops/support-bundle")
    def ops_support_bundle() -> dict[str, Any]:
        """§47: redacted health/support bundle (config, recent audit events,
        graph store stats, versions)."""
        return collect_support_bundle(
            audit_sink=state.audit_sink, graph_store=store
        )

    @router.get("/api/v1/ops/ha-topology")
    def ops_ha_topology() -> dict[str, Any]:
        """G2-DEPLOY-HA/GAP-PERF-001: resolved HA topology readiness."""
        return default_ha_topology().to_dict()

    @router.post("/api/v1/ops/shard-plan")
    def ops_shard_plan(payload: ShardPlanRequest) -> dict[str, Any]:
        """G2-SCALE-SHARD: logical graph sharding plan with stable routing keys."""
        return build_shard_plan(
            payload.entity_count,
            payload.shard_count,
            strategy=payload.strategy,
        )

    @router.post("/api/v1/ops/helm-summary")
    def ops_helm_summary(values: dict[str, Any] | None = None) -> dict[str, Any]:
        """G2-DEPLOY-HELM: summarize Helm values for deployment review."""
        return helm_release_summary(values or {})

    # -- Metrics (GAP-OBS-003) -----------------------------------------------------

    @router.get("/metrics", response_class=PlainTextResponse)
    def metrics_render() -> str:
        """GAP-OBS-003: Prometheus text exposition of request metrics."""
        return "\n".join(render() for render in state.metrics_renderers)

    # -- Embeddings health (GAP-SEARCH-001/§7.3) -----------------------------------

    @router.get("/api/v1/health/embeddings")
    def health_embeddings() -> dict[str, Any]:
        """Embedding provider health; reports the deterministic hashing
        fallback when no Ollama model is configured."""
        provider = build_embedding_provider()
        if provider is None:
            return {
                "provider": "hashing",
                "healthy": True,
                "dim": HashingEmbedder().dimensions,
            }
        try:
            healthy = bool(provider.health())
        except Exception:  # noqa: BLE001 - health probe must never fail the route
            healthy = False
        return {"provider": "ollama", "healthy": healthy, "dim": provider.dim}

    # ======================================================================
    # SR wave (pass 9): Super-Requirements commercial baseline
    # ======================================================================

    # Tenancy (SR-TEN-001/002/003/006/007/009): fail-closed tenant context,
    # isolation placement, quotas, lifecycle, hash-chained metering.
    router.include_router(build_tenancy_router(state.tenancy_service))

    # Licensing (SR-DEP-007, SR-COM-001, SR-TEN-009): license status, offline
    # verify, module entitlement checks, tamper-evident usage meter.
    router.include_router(
        build_licensing_router(state.entitlement_checker, state.usage_meter)
    )

    # Layered config (SR-CFG-001..006): effective config, explain, set,
    # bounds, audit, rollback, export/import/diff, feature flags.
    router.include_router(build_config_router(state.config_store, state.feature_flags))

    # Egress gateway (SR-LLM-010..020, SR-CON-010/011): policy matrix rules,
    # dry-run/live calls, manifests, canaries, kill switch, provider plugins.
    router.include_router(build_egress_router(state.egress_gateway))

    # Branding (SR-WL-001/003/004-partial/006/007, SR-ONT-007): theme tokens,
    # terminology rename/canonicalize, localized messages, legal content.
    router.include_router(
        build_branding_router(
            state.branding_themes,
            state.branding_terminology,
            state.branding_locales,
            state.branding_legal,
        )
    )

    # Privacy (SR-PRV-001..004, 006 partials): ingest classification, DSAR
    # locate/erase over the live graph store, consents, retention, residency.
    # Person/WorkItem carry subject-bearing properties (email, owner);
    # the default label list would only scan "Entity".
    router.include_router(
        build_privacy_router(
            graph_store=store, graph_labels=["Person", "WorkItem"], tenant_layers=state.tenant_layers
        )
    )

    # Compliance packs (SR-GOV-001..005): GDPR/SOC2/ISO27001/HIPAA/CMMC
    # skeleton packs, gap analysis, AI governance, change governance, roles.
    router.include_router(build_compliance_router())

    # Report generator (SR-NLQ-008): template render (HTML/MD/JSON in-product;
    # PDF/DOCX/PPTX are External gates), schedules, live graph stats.
    router.include_router(build_reports_router(graph_store=store))

    # Loop engineering catalog/runtime (GAP-LOOP-001..047): route-level
    # product evidence for bounded agent loops and approval patterns.
    router.include_router(build_loops_router())

    # QA gate integrity (SR-QA-010..014): behavioral evidence registry,
    # mutation checks, three-number dashboard, code introspection, policy gate.
    router.include_router(build_qa_router())

    # NL suggestion engine (SR-NLQ-002/003/004-partial): deterministic
    # intent interpretations over the graph store with authz pre-check note.
    router.include_router(build_suggest_router(store, state.policy_enforcer))

    # Schema profiler (SR-ING-010/012/013/016-hook): dataset profile, drift,
    # key candidates, relationship discovery.
    router.include_router(build_ingest_profile_router())

    # Diamond-Standard Moonshots 1, 2, 3, 4, 5, 8, 9, 10
    from eoip.moonshot.router import build_moonshot_router
    router.include_router(build_moonshot_router())

    from eoip.brain.router import build_brain_router
    router.include_router(build_brain_router())

    router.include_router(build_systems_router())

    from eoip.enterprise.router import build_enterprise_router
    router.include_router(build_enterprise_router())

    from eoip.enterprise.advanced_router import build_advanced_capabilities_router
    router.include_router(build_advanced_capabilities_router(store))

    # Unified engineering/productivity platform surface. Routes are under
    # /api/v1/platform and lazily import their engines on call.
    from eoip.platform_router import build_platform_router
    router.include_router(build_platform_router())

    # GitOps and Marketplace routes (GAP-GITOPS-002..008, GAP-MKT-002..008)
    from eoip.ontology.gitops_router import build_gitops_marketplace_router
    router.include_router(build_gitops_marketplace_router())

    # Enterprise Security routes (GAP-SEC-008..012)
    from eoip.authz.security_router import build_security_router
    router.include_router(build_security_router(role_registry=state.role_registry))

    # Processing Units routes (PU-W15, PUR-CON-001..010, /api/processing/v1)
    from eoip.processing.router import build_processing_router
    router.include_router(build_processing_router())

    return router, state



def add_metrics_middleware(app: Any, state: ExtendedState) -> None:
    """Record request metrics into the state metrics registry (GAP-OBS-003)."""

    @app.middleware("http")
    async def eoip_metrics_middleware(request: Any, call_next: Any) -> Any:
        started = time.perf_counter()
        response = await call_next(request)
        try:
            record_request(
                state.metrics,
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                duration_seconds=time.perf_counter() - started,
            )
        except Exception:  # noqa: BLE001, S110 - metrics must never break requests
            pass

        return response


def ensure_extended(app, store: GraphStore) -> None:
    """Idempotently attach the extended router/state to an app that does not
    already carry them (used by the deployment factory in main.py, which
    builds on top of apps.api.app.create_app)."""
    if getattr(app.state, "extended_state", None) is not None:
        return
    router, state = build_extended_router(store)
    app.state.extended_state = state
    app.include_router(router)
    add_metrics_middleware(app, state)
