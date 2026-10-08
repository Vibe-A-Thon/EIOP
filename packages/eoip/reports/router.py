"""HTTP router for report generation and export (SR-NLQ-008).

``build_router(...)`` constructs the ``/api/v1/reports`` router. FastAPI is
imported lazily inside the factory (pattern: ``eoip.graph.bitemporal``).
Export endpoints serve HTML, Markdown and JSON; PDF/DOCX/PPTX are an
External gate and return 501 with an explanatory detail.
"""

from __future__ import annotations

from typing import Any

from eoip.reports.generator import (
    BUILTIN_TEMPLATES,
    EXTERNAL_FORMATS,
    ReportContext,
    ReportGenerator,
    template_by_id,
)
from eoip.reports.schedule import ReportScheduleStore


def build_router(
    *,
    graph_store: Any = None,
    schedule_store: ReportScheduleStore | None = None,
):
    """Construct the ``/api/v1/reports`` FastAPI router.

    ``graph_store`` is optional; when provided, report contexts are seeded
    with live vertex/edge counts. The schedule store defaults to the on-disk
    JSON store under ``EOIP_DATA_DIR``.
    """
    from fastapi import APIRouter, HTTPException, Query

    schedules = schedule_store or ReportScheduleStore()
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
        report_format: str = Query(default="markdown"),
        generated_at: str = "",
    ) -> dict[str, Any]:
        if template_by_id(template_id) is None:
            raise HTTPException(status_code=404, detail=f"Unknown template: {template_id}")
        if report_format in EXTERNAL_FORMATS:
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
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        return report.model_dump()

    @router.get("/export/{report_id}")
    def export_placeholder(report_id: str, report_format: str = Query(default="html")) -> dict[str, Any]:
        # Report bodies are rendered statelessly via POST /render; this
        # endpoint documents the export surface for the wiring step.
        raise HTTPException(
            status_code=501,
            detail=(
                f"Export of stored report '{report_id}' as '{report_format}' is "
                "ADR-gated: render via POST /api/v1/reports/render instead."
            ),
        )

    # -- schedules (SR-NLQ-008) ----------------------------------------------
    @router.get("/schedules")
    def list_schedules() -> list[dict[str, Any]]:
        return [s.model_dump() for s in schedules.list()]

    @router.post("/schedules", status_code=201)
    def create_schedule(
        template_id: str,
        name: str,
        recurrence: str = "weekly",
        params: dict[str, Any] | None = None,
        report_format: str = "markdown",
    ) -> dict[str, Any]:
        if template_by_id(template_id) is None:
            raise HTTPException(status_code=404, detail=f"Unknown template: {template_id}")
        schedule = schedules.create(
            template_id, name,
            recurrence=recurrence,  # type: ignore[arg-type]
            params=params or {},
            report_format=report_format,
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

    @router.delete("/schedules/{schedule_id}", status_code=204)
    def delete_schedule(schedule_id: str) -> None:
        if not schedules.delete(schedule_id):
            raise HTTPException(status_code=404, detail=f"Unknown schedule: {schedule_id}")

    return router
