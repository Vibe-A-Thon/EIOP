"""Report generation: parameterized templates, HTML/Markdown renderers, schedules.

Implements SR-NLQ-008 (report templates, scheduled/recurring reports,
parameterized multi-format export). HTML and Markdown renderers are
in-product; PDF/DOCX/PPTX are an External gate. HTTP wiring:
``eoip.reports.router.build_router`` mounts under ``/api/v1/reports``.
"""

from eoip.reports.generator import (
    BUILTIN_TEMPLATES,
    EXTERNAL_FORMATS,
    SUPPORTED_FORMATS,
    RenderedReport,
    ReportContext,
    ReportGenerator,
    ReportParameter,
    ReportSection,
    ReportTemplate,
    template_by_id,
)
from eoip.reports.schedule import (
    ReportSchedule,
    ReportScheduleStore,
    next_run_after,
)

__all__ = [
    "BUILTIN_TEMPLATES",
    "EXTERNAL_FORMATS",
    "SUPPORTED_FORMATS",
    "RenderedReport",
    "ReportContext",
    "ReportGenerator",
    "ReportParameter",
    "ReportSchedule",
    "ReportScheduleStore",
    "ReportSection",
    "ReportTemplate",
    "next_run_after",
    "template_by_id",
]
