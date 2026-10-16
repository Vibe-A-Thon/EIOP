"""HTTP router for report generation and export (SR-NLQ-008).

``build_router(...)`` constructs the ``/api/v1/reports`` router. FastAPI is
imported lazily inside the factory (pattern: ``eoip.graph.bitemporal``).
Exports serve the stored format. PDF/DOCX/PPTX require the reports extra
and EOIP_ENABLE_EXTERNAL_REPORT_FORMATS; disabled formats return 501.
"""

from __future__ import annotations

from typing import Any

from starlette.requests import Request

from eoip.reports.generator import (
    BUILTIN_TEMPLATES,
    EXTERNAL_FORMATS,
    ReportContext,
    ReportGenerator,
    template_by_id,
)
from eoip.reports.schedule import ReportScheduleStore
from eoip.reports.store import ReportArtifactStore


def build_router(
    *,
    graph_store: Any = None,
    schedule_store: ReportScheduleStore | None = None,
    artifact_store: ReportArtifactStore | None = None,
):
    """Construct the ``/api/v1/reports`` FastAPI router.

    ``graph_store`` is optional; when provided, report contexts are seeded
    with live vertex/edge counts. The schedule and artifact stores default
    to durable disk-backed stores under ``EOIP_DATA_DIR`` (CP-03, CP-25).
    """
    from fastapi import APIRouter, HTTPException, Query, Request

    schedules = schedule_store or ReportScheduleStore()
    artifacts = artifact_store or ReportArtifactStore()
    generator = ReportGenerator()

    router = APIRouter(prefix="/api/v1/reports", tags=["reports"])

    def _seed_context(ctx: ReportContext) -> ReportContext:
        if graph_store is not None and not ctx.graph_stats:
            try:
                ctx.graph_stats = {
                    "vertices": graph_store.count_vertices(),
                    "edges": graph_store.count_edges(),
                }
            except TypeError:
                pass
        return ctx

    @router.get("")
    def reports_capability() -> dict[str, Any]:
        """Summarize report-generation capabilities at the router root."""
        return {
            "service": "reports",
            "templates": len(BUILTIN_TEMPLATES),
            "supported_formats": ["html", "json", "markdown"],
            "external_gated_formats": sorted(EXTERNAL_FORMATS),
            "schedules": len(schedules.list()),
            "routes": [
                "GET /api/v1/reports",
                "GET /api/v1/reports/templates",
                "POST /api/v1/reports/render",
                "GET /api/v1/reports/schedules",
                "POST /api/v1/reports/schedules",
            ],
        }

    # -- templates ---------------------------------------------------------
    @router.get("/templates")
    def list_templates() -> list[dict[str, Any]]:
        return [
            {
                "template_id": t.template_id,
                "name": t.name,
                "description": t.description,
                "parameters": [p.model_dump() for p in t.parameters],
            }
            for t in BUILTIN_TEMPLATES
        ]

    # -- generation / export -------------------------------------------------
    @router.post("/render")
    def render_report(
        template_id: str,
        ctx: ReportContext,
        request: Request,
        report_format: str = Query(default="markdown"),
        generated_at: str = "",
    ) -> dict[str, Any]:
        import os
        if template_by_id(template_id) is None:
            raise HTTPException(status_code=404, detail=f"Unknown template: {template_id}")
        allow_ext = os.getenv("EOIP_ENABLE_EXTERNAL_REPORT_FORMATS", "").lower() in ("true", "1", "yes")
        if report_format in EXTERNAL_FORMATS and not allow_ext:
            raise HTTPException(
                status_code=501,
                detail=(
                    f"Format '{report_format}' is an External gate (SR-NLQ-008): "
                    "HTML, Markdown and JSON are supported in-product."
                ),
            )
        try:
            report = generator.render(
                template_id,
                _seed_context(ctx),
                report_format=report_format,
                generated_at=generated_at,
                allow_external_formats=allow_ext,
            )
            principal = getattr(request.state, "principal", None)
            tenant_id = getattr(request.state, "tenant_id", None) or (principal.tenant_id if principal else None)
            created_by = getattr(principal, "username", None) if principal else getattr(principal, "id", None) or "local-user"
            report.tenant_id = tenant_id
            report.created_by = created_by
            if hasattr(artifacts, "put"):
                artifacts.put(report)
            elif isinstance(artifacts, dict):
                artifacts[report.report_id] = report
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except ImportError as exc:
            raise HTTPException(status_code=503, detail="Report renderer unavailable; install eoip[reports]") from exc
        return report.model_dump()

    @router.get("/export/{report_id}")
    def export_report(
        report_id: str,
        request: Request,
        report_format: str | None = Query(default=None),
    ):
        import base64

        from fastapi.responses import Response

        principal = getattr(request.state, "principal", None)
        req_tenant = getattr(request.state, "tenant_id", None) or (principal.tenant_id if principal else None)
        is_admin = principal and any(r in ("admin", "platform_admin") for r in getattr(principal, "roles", ()))

        if hasattr(artifacts, "get"):
            report = artifacts.get(report_id)
        elif isinstance(artifacts, dict):
            report = artifacts.get(report_id)
        else:
            report = None
        if report is None:
            raise HTTPException(
                status_code=404,
                detail=f"Report '{report_id}' not found. Render via POST /api/v1/reports/render first.",
            )
        if report.tenant_id and req_tenant and report.tenant_id != req_tenant and not (is_admin and req_tenant in ("system", "global")):
            raise HTTPException(status_code=403, detail="Cross-tenant access forbidden")

        media_types = {
            "html": "text/html; charset=utf-8",
            "markdown": "text/markdown; charset=utf-8",
            "json": "application/json",
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        }
        fmt = report.format.lower()
        if report_format is not None and report_format != fmt:
            raise HTTPException(status_code=409, detail="Requested format differs from the stored artifact; render it first")
        media_type = media_types.get(fmt, "application/octet-stream")
        if fmt in ("pdf", "docx", "pptx"):
            try:
                body_bytes = base64.b64decode(report.content, validate=True)
            except ValueError as exc:
                raise HTTPException(status_code=500, detail="Stored report artifact is corrupt") from exc
        else:
            body_bytes = report.content.encode("utf-8")

        return Response(
            content=body_bytes,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{report_id}.{fmt}"'},
        )

    # -- schedules (SR-NLQ-008) ----------------------------------------------
    @router.get("/schedules")
    def list_schedules(request: Request) -> list[dict[str, Any]]:
        principal = getattr(request.state, "principal", None)
        tenant_id = getattr(request.state, "tenant_id", None) or (principal.tenant_id if principal else None)
        is_admin = principal and any(r in ("admin", "platform_admin") for r in getattr(principal, "roles", ()))
        filter_tenant = None if (is_admin and tenant_id in ("system", "global")) else tenant_id
        return [s.model_dump() for s in schedules.list(tenant_id=filter_tenant)]

    @router.post("/schedules", status_code=201)
    def create_schedule(
        template_id: str,
        name: str,
        request: Request,
        recurrence: str = "weekly",
        params: dict[str, Any] | None = None,
        report_format: str = "markdown",
    ) -> dict[str, Any]:
        if template_by_id(template_id) is None:
            raise HTTPException(status_code=404, detail=f"Unknown template: {template_id}")
        principal = getattr(request.state, "principal", None)
        tenant_id = getattr(request.state, "tenant_id", None) or (principal.tenant_id if principal else None)
        created_by = getattr(principal, "username", None) if principal else getattr(principal, "id", None) or "local-user"
        schedule = schedules.create(
            template_id, name,
            recurrence=recurrence,  # type: ignore[arg-type]
            params=params or {},
            report_format=report_format,
            tenant_id=tenant_id,
            created_by=created_by,
        )
        return schedule.model_dump()

    @router.get("/schedules/due")
    def due_schedules() -> list[dict[str, Any]]:
        return [s.model_dump() for s in schedules.due_schedules()]

    @router.post("/schedules/{schedule_id}/mark-run")
    def mark_run(schedule_id: str, at: str = "") -> dict[str, Any]:
        try:
            return schedules.mark_run(schedule_id, at=at or None).model_dump()  # type: ignore[arg-type]
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Unknown schedule: {schedule_id}")

    @router.post("/schedules/{schedule_id}/run", status_code=200)
    def run_schedule(schedule_id: str, request: Request) -> dict[str, Any]:
        principal = getattr(request.state, "principal", None)
        req_tenant = getattr(request.state, "tenant_id", None) or (principal.tenant_id if principal else None)
        is_admin = principal and any(r in ("admin", "platform_admin") for r in getattr(principal, "roles", ()))
        schedule = schedules.get(schedule_id)
        if schedule is None:
            raise HTTPException(status_code=404, detail=f"Unknown schedule: {schedule_id}")
        if schedule.tenant_id and req_tenant and schedule.tenant_id != req_tenant and not (is_admin and req_tenant in ("system", "global")):
            raise HTTPException(status_code=403, detail="Cross-tenant access forbidden")
        rendered = schedules.run_schedule(schedule_id, generator, artifacts, tenant_id=req_tenant)
        return rendered.model_dump()

    @router.delete("/schedules/{schedule_id}", status_code=204, response_model=None)
    def delete_schedule(schedule_id: str, request: Request) -> None:
        principal = getattr(request.state, "principal", None)
        req_tenant = getattr(request.state, "tenant_id", None) or (principal.tenant_id if principal else None)
        is_admin = principal and any(r in ("admin", "platform_admin") for r in getattr(principal, "roles", ()))
        schedule = schedules.get(schedule_id)
        if schedule is None:
            raise HTTPException(status_code=404, detail=f"Unknown schedule: {schedule_id}")
        if schedule.tenant_id and req_tenant and schedule.tenant_id != req_tenant and not (is_admin and req_tenant in ("system", "global")):
            raise HTTPException(status_code=403, detail="Cross-tenant access forbidden")
        if not schedules.delete(schedule_id):
            raise HTTPException(status_code=404, detail=f"Unknown schedule: {schedule_id}")

    return router

