"""HTTP router for privacy endpoints (SR-PRV-001..004, SR-PRV-006).

``build_router(...)`` constructs the FastAPI router with a LAZY fastapi
import, matching ``eoip.graph.bitemporal.build_router``. The API wiring
step (apps/api) includes this router under ``/api/v1/privacy`` — no
apps/ changes are made here. Deep items (DPIA generation, legal-hold
workflows, DP aggregates) are deliberately absent — ADR-gated.
"""



import json
from typing import Any

from eoip.privacy.classification import ClassificationEngine
from eoip.privacy.consent import ConsentRecord, ConsentRegistry
from eoip.privacy.dsar import ErasurePropagator, locate_subject
from eoip.privacy.residency import ResidencyAspect, ResidencyValidator
from eoip.privacy.retention import RetainableRecord, RetentionEngine
from pydantic import BaseModel


class ClassifyRequest(BaseModel):
    payload: dict
    source_ref: str = ""
    tenant_id: str | None = None


class LocateRequest(BaseModel):
    subject_id: str
    tenant_id: str | None = None
    subject_properties: list[str] | None = None


class RectifyRequest(BaseModel):
    subject_id: str
    tenant_id: str | None = None
    old_value: str
    new_value: str


class RetentionRequest(BaseModel):
    records: list[RetainableRecord]


class ResidencyRequest(BaseModel):
    tenant_id: str
    placements: dict[ResidencyAspect, str]


def build_router(
    classifier: ClassificationEngine | None = None,
    consent: ConsentRegistry | None = None,
    retention: RetentionEngine | None = None,
    residency: ResidencyValidator | None = None,
    *,
    graph_store: Any = None,
    graph_labels: list[str] | None = None,
    raw_captures: Any = None,
    derived_registries: list[Any] | None = None,
    erasers: dict[str, Any] | None = None,
    tenant_layers: Any = None,
    embed: Any = None,
    summarize: Any = None,
):
    """Construct the FastAPI router for privacy endpoints.

    Routes:
    * ``POST /api/v1/privacy/classify``            — classify an ingest payload
    * ``POST /api/v1/privacy/dsar/locate``         — subject access report
    * ``POST /api/v1/privacy/dsar/erase``          — erasure with propagation + proof
    * ``GET  /api/v1/privacy/consents/allowed``    — purpose limitation check
    * ``POST /api/v1/privacy/consents``            — record a consent grant/revocation
    * ``POST /api/v1/privacy/retention/evaluate``  — evaluate records for expiry
    * ``POST /api/v1/privacy/residency/validate``  — check placements vs policy
    """
    from fastapi import APIRouter, HTTPException, Request

    router = APIRouter(prefix="/api/v1/privacy", tags=["privacy"])
    classifier = classifier or ClassificationEngine()
    consent = consent or ConsentRegistry()
    retention = retention or RetentionEngine()
    residency = residency or ResidencyValidator()
    propagator = ErasurePropagator(graph_store=graph_store, derived_erasers=erasers)

    @router.post("/classify")
    def classify(body: ClassifyRequest):
        result = classifier.classify(body.payload, source_ref=body.source_ref, tenant_id=body.tenant_id)
        return result.model_dump()

    def _tenant(request: Request, requested: str | None) -> str:
        """The tenant comes from the authenticated principal; a body tenant may only repeat it.
        Platform principals (no tenant) must name the tenant explicitly."""
        principal = getattr(request.state, "principal", None)
        bound = getattr(principal, "tenant_id", None) if principal is not None else None
        if bound:
            if requested and requested != bound:
                raise HTTPException(403, "tenant_id does not match the authenticated principal")
            return bound
        if not requested:
            raise HTTPException(422, "tenant_id is required for platform principals")
        return requested

    def _workflow(tenant_id: str):
        from eoip.privacy.dsr import SubjectRequestWorkflow

        return SubjectRequestWorkflow(tenant_layers.ensure_tenant(tenant_id), graph_store=graph_store,
                                      graph_labels=tuple(graph_labels or ["Person"]), embed=embed,
                                      summarize=summarize)

    def _legacy_report(body: LocateRequest, tenant_id: str | None):
        return locate_subject(
            body.subject_id,
            tenant_id=tenant_id,
            graph_store=graph_store,
            graph_labels=graph_labels,
            raw_captures=raw_captures,
            derived_registries=derived_registries,
            subject_properties=body.subject_properties,
        )

    @router.post("/dsar/locate")
    def dsar_locate(body: LocateRequest, request: Request):
        if tenant_layers is None:
            return _legacy_report(body, body.tenant_id).model_dump()
        return _workflow(_tenant(request, body.tenant_id)).locate(body.subject_id).model_dump()

    @router.post("/dsar/export")
    def dsar_export(body: LocateRequest, request: Request):
        if tenant_layers is None:
            raise HTTPException(501, "DSAR export needs tenant stores")
        tenant = _tenant(request, body.tenant_id)
        name, proof = _workflow(tenant).access_export(body.subject_id)
        bundle = json.loads(tenant_layers.for_tenant(tenant).read_export(name))
        return {"export": name, "bundle": bundle, "proof": proof.model_dump()}

    @router.post("/dsar/rectify")
    def dsar_rectify(body: RectifyRequest, request: Request):
        if tenant_layers is None:
            raise HTTPException(501, "DSAR rectification needs tenant stores")
        if not body.old_value or body.old_value == body.new_value:
            raise HTTPException(422, "old_value must be non-empty and differ from new_value")
        proof = _workflow(_tenant(request, body.tenant_id)).rectify(body.subject_id, body.old_value, body.new_value)
        return proof.model_dump()

    @router.post("/dsar/erase")
    def dsar_erase(body: LocateRequest, request: Request):
        if tenant_layers is None:
            return propagator.erase(_legacy_report(body, body.tenant_id)).model_dump()
        return _workflow(_tenant(request, body.tenant_id)).erase(body.subject_id).model_dump()

    @router.get("/consents/allowed")
    def consents_allowed(subject_id: str, purpose: str, tenant_id: str, source: str | None = None):
        return {
            "subject_id": subject_id,
            "purpose": purpose,
            "allowed": consent.allowed(subject_id, purpose, source),
        }

    @router.post("/consents")
    def record_consent(record: ConsentRecord):
        consent.record(record)
        return {"recorded": True, "id": record.id}

    @router.post("/retention/evaluate")
    def retention_evaluate(body: RetentionRequest):
        return {"decisions": [d.model_dump() for d in retention.run_expiry(body.records)]}

    @router.post("/residency/validate")
    def residency_validate(body: ResidencyRequest):
        return residency.validate(body.tenant_id, body.placements).model_dump()

    return router
