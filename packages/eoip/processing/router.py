"""FastAPI Router for EOIP Processing Runtime (PUR-CON-001..010, Section 5.3).

Exposes /api/processing/v1 routes for capability discovery, device inventory,
plan DAG validation, durable job submission, cancellation, result and receipt retrieval.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from pydantic import BaseModel, Field

from eoip.processing.catalog import (
    get_operator_spec,
    get_unit_capabilities,
    list_operator_specs,
)
from eoip.processing.contracts import (
    ExecutionContext,
    ExecutionPlan,
    ExecutionReceipt,
    JobRecord,
    JobStatus,
    LogicalUnit,
    PlanNode,
    ProcessingRequest,
)
from eoip.processing.devices import enumerate_devices
from eoip.processing.planner import compile_execution_plan
from eoip.processing.service import ProcessingService, get_processing_service


router = APIRouter(prefix="/api/processing/v1", tags=["Processing Units"])


class PlanRequest(BaseModel):
    nodes: List[PlanNode]


class JobSubmitResponse(BaseModel):
    job_id: str
    status: str
    request_digest: str
    plan_digest: str


class JobListResponse(BaseModel):
    jobs: List[JobRecord]
    total: int
    cursor: int
    limit: int


def _get_execution_context(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    x_principal_id: Optional[str] = Header(None, alias="X-Principal-ID"),
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-ID"),
) -> ExecutionContext:
    tenant = x_tenant_id or "default_tenant"
    principal = x_principal_id or "default_principal"
    corr = x_correlation_id or f"corr_{uuid4().hex[:8]}"
    return ExecutionContext(
        tenant_id=tenant,
        principal_id=principal,
        correlation_id=corr,
    )


@router.get("/capabilities", summary="List logical units and operator capabilities")
def get_capabilities(
    context: ExecutionContext = Depends(_get_execution_context),
) -> Dict[str, Any]:
    """Retrieve tenant-filtered logical units, operators, and qualification references."""
    unit_caps = get_unit_capabilities()
    return {
        "tenant_id": context.tenant_id,
        "units": unit_caps,
        "total_units": len(unit_caps),
        "total_operators": sum(u["operator_count"] for u in unit_caps.values()),
        "status": "active",
    }


@router.get("/devices", summary="List available computing devices")
def get_devices(
    context: ExecutionContext = Depends(_get_execution_context),
) -> Dict[str, Any]:
    """Retrieve redacted physical and simulated device descriptors."""
    devices = enumerate_devices()
    return {
        "tenant_id": context.tenant_id,
        "devices": [d.model_dump() for d in devices],
        "count": len(devices),
    }


@router.post("/plans", summary="Validate DAG and compile execution plan")
def create_plan(
    plan_req: PlanRequest,
    context: ExecutionContext = Depends(_get_execution_context),
) -> Dict[str, Any]:
    """Compile and validate an operator DAG without executing side-effects."""
    try:
        plan = compile_execution_plan(plan_req.nodes)
        return plan.model_dump()
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_code": "INVALID_REQUEST", "message": str(exc)},
        ) from exc


@router.post(
    "/jobs",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a processing job",
    response_model=JobSubmitResponse,
)
def submit_job(
    request: ProcessingRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    auto_process: bool = Query(True, description="Immediately execute synchronously in local test mode"),
    context: ExecutionContext = Depends(_get_execution_context),
    service: ProcessingService = Depends(get_processing_service),
) -> JobSubmitResponse:
    """Submit a processing job with optional idempotency key."""
    spec = get_operator_spec(request.operator_id)
    if not spec:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_code": "INVALID_REQUEST", "message": f"Unregistered operator: {request.operator_id}"},
        )

    try:
        job = service.submit_job(
            request=request,
            context=context,
            idempotency_key=idempotency_key,
        )
        if auto_process:
            job = service.process_job(job.job_id)

        return JobSubmitResponse(
            job_id=job.job_id,
            status=job.status.value,
            request_digest=job.request_digest,
            plan_digest=job.plan_digest,
        )
    except ValueError as exc:
        if "IDEMPOTENCY_CONFLICT" in str(exc):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error_code": "IDEMPOTENCY_CONFLICT", "message": str(exc)},
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_code": "INVALID_REQUEST", "message": str(exc)},
        ) from exc


@router.get("/jobs", summary="List jobs for tenant", response_model=JobListResponse)
def list_jobs(
    limit: int = Query(50, ge=1, le=100),
    cursor: int = Query(0, ge=0),
    context: ExecutionContext = Depends(_get_execution_context),
    service: ProcessingService = Depends(get_processing_service),
) -> JobListResponse:
    """Retrieve tenant-scoped cursor-paginated jobs."""
    jobs, total = service.list_jobs(tenant_id=context.tenant_id, limit=limit, cursor=cursor)
    return JobListResponse(
        jobs=jobs,
        total=total,
        cursor=cursor,
        limit=limit,
    )


@router.get("/jobs/{job_id}", summary="Get job details")
def get_job(
    job_id: str,
    context: ExecutionContext = Depends(_get_execution_context),
    service: ProcessingService = Depends(get_processing_service),
) -> Dict[str, Any]:
    """Retrieve authorized status and references for a job."""
    job = service.get_job(job_id, tenant_id=context.tenant_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Job not found: {job_id}"},
        )
    return job.model_dump()


@router.post("/jobs/{job_id}/cancel", summary="Cancel a job")
def cancel_job(
    job_id: str,
    context: ExecutionContext = Depends(_get_execution_context),
    service: ProcessingService = Depends(get_processing_service),
) -> Dict[str, Any]:
    """Idempotently cancel a queued or running job."""
    try:
        job = service.cancel_job(job_id, tenant_id=context.tenant_id)
        return job.model_dump()
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Job not found: {job_id}"},
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_code": "CONFLICT", "message": str(exc)},
        ) from exc


@router.get("/jobs/{job_id}/result", summary="Get job result")
def get_job_result(
    job_id: str,
    context: ExecutionContext = Depends(_get_execution_context),
    service: ProcessingService = Depends(get_processing_service),
) -> Dict[str, Any]:
    """Retrieve output result for a finished job."""
    try:
        res = service.get_result(job_id, tenant_id=context.tenant_id)
        return {"job_id": job_id, "result": res}
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Job not found: {job_id}"},
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_code": "JOB_NOT_READY", "message": str(exc)},
        ) from exc


@router.get("/jobs/{job_id}/receipt", summary="Get job execution receipt")
def get_job_receipt(
    job_id: str,
    context: ExecutionContext = Depends(_get_execution_context),
    service: ProcessingService = Depends(get_processing_service),
) -> Dict[str, Any]:
    """Retrieve verified execution receipt with cryptographic digests."""
    try:
        receipt = service.get_receipt(job_id, tenant_id=context.tenant_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error_code": "NOT_FOUND", "message": f"Receipt not found for job: {job_id}"},
            )
        return receipt.model_dump()
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Job not found: {job_id}"},
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_code": "JOB_NOT_READY", "message": str(exc)},
        ) from exc


@router.post("/profiles/{profile_id}/probes", summary="Probe hardware/runtime profile")
def probe_profile(
    profile_id: str,
    context: ExecutionContext = Depends(_get_execution_context),
    service: ProcessingService = Depends(get_processing_service),
) -> Dict[str, Any]:
    """Privileged, bounded asynchronous probe without package installation."""
    probe_res = service.probe_profile(profile_id)
    return probe_res


def build_processing_router() -> APIRouter:
    """Helper factory for including the processing router in FastAPI apps."""
    return router
