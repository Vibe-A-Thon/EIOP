"""Report generator (SR-NLQ-008).

Parameterized report templates — impact assessment, incident RCA, change-risk
review, compliance evidence and executive brief — rendered from graph data +
evidence manifests to self-contained HTML and Markdown. JSON export is a
plain ``model_dump`` of the rendered report. PDF/DOCX/PPTX export is an
External gate: no binary renderers are bundled (P0 covers HTML/MD; PDF et al.
need an external rendering service). Approval workflow and white-label
styling are ADR-gated on top of this generator; the HTML renderer accepts a
``brand`` block for future white-label theming.
"""

from __future__ import annotations

import html
import json
import uuid
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field

from eoip.compliance.pack import new_id

SUPPORTED_FORMATS = ("html", "markdown", "json")
EXTERNAL_FORMATS = ("pdf", "docx", "pptx")  # External gate (SR-NLQ-008)


class ReportParameter(BaseModel):
    """A template parameter declaration."""

    model_config = ConfigDict(extra="forbid")

    name: str
    label: str
    required: bool = False
    default: Any = None


class ReportSection(BaseModel):
    """One rendered section of a report."""

    model_config = ConfigDict(extra="forbid")

    heading: str
    body_markdown: str = ""
    table: dict[str, list[str]] | None = None  # column -> values
    items: list[str] = Field(default_factory=list)


class RenderedReport(BaseModel):
    """A fully rendered report in one format."""

    model_config = ConfigDict(extra="forbid")

    report_id: str
    template: str
    title: str
    format: str
    generated_at: str
    content: str
    evidence_manifest: list[dict[str, Any]] = Field(default_factory=list)


class ReportContext(BaseModel):
    """Inputs available to every template.

    ``graph_stats`` and ``evidence_manifest`` come from the real graph store
    and provenance/audit layers; templates degrade gracefully when a field is
    absent so they also work in unit tests with synthetic data.
    """

    model_config = ConfigDict(extra="forbid")

    title: str = ""
    params: dict[str, Any] = Field(default_factory=dict)
    graph_stats: dict[str, Any] = Field(default_factory=dict)
    evidence_manifest: list[dict[str, Any]] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)
    narrative: str = ""


class ReportTemplate(BaseModel):
    """A parameterized report template (SR-NLQ-008)."""

    model_config = ConfigDict(extra="forbid")

    template_id: str
    name: str
    description: str = ""
    parameters: list[ReportParameter] = Field(default_factory=list)
    section_builder: Callable[[ReportContext], list[ReportSection]] = Field(exclude=True, repr=False)


def _sections_impact(ctx: ReportContext) -> list[ReportSection]:
    subject = ctx.params.get("subject", "the requested change")
    depth = ctx.params.get("max_hops", 6)
    return [
        ReportSection(heading="Scope", body_markdown=f"Impact assessment for **{subject}** (bounded to {depth} hops)."),
        ReportSection(
            heading="Graph footprint",
            table={"metric": list(ctx.graph_stats.keys()) or ["vertices", "edges"],
                   "value": [str(v) for v in ctx.graph_stats.values()] or ["0", "0"]},
        ),
        ReportSection(heading="Findings", items=ctx.findings),
        ReportSection(
            heading="Evidence appendix",
            items=[e.get("ref", str(e)) for e in ctx.evidence_manifest],
        ),
    ]


def _sections_rca(ctx: ReportContext) -> list[ReportSection]:
    incident = ctx.params.get("incident_id", "unknown incident")
    return [
        ReportSection(heading="Incident", body_markdown=f"Root-cause analysis for incident `{incident}`."),
        ReportSection(heading="Timeline", items=ctx.findings),
        ReportSection(heading="Root cause", body_markdown=ctx.narrative),
        ReportSection(heading="Evidence appendix", items=[e.get("ref", str(e)) for e in ctx.evidence_manifest]),
    ]


def _sections_change_risk(ctx: ReportContext) -> list[ReportSection]:
    proposal = ctx.params.get("proposal_id", "unknown proposal")
    return [
        ReportSection(heading="Change under review", body_markdown=f"Change-risk review for proposal `{proposal}`."),
        ReportSection(heading="Risk findings", items=ctx.findings),
        ReportSection(heading="Governance status", body_markdown=ctx.narrative),
        ReportSection(heading="Evidence appendix", items=[e.get("ref", str(e)) for e in ctx.evidence_manifest]),
    ]


def _sections_compliance(ctx: ReportContext) -> list[ReportSection]:
    framework = ctx.params.get("framework", "framework")
    return [
        ReportSection(heading="Framework", body_markdown=f"Compliance evidence report for **{framework}**."),
        ReportSection(heading="Control status", items=ctx.findings),
        ReportSection(heading="Gaps", items=[f for f in ctx.findings if f.startswith("GAP")]),
        ReportSection(heading="Evidence appendix", items=[e.get("ref", str(e)) for e in ctx.evidence_manifest]),
    ]


def _sections_executive(ctx: ReportContext) -> list[ReportSection]:
    return [
        ReportSection(heading="Summary", body_markdown=ctx.narrative),
        ReportSection(heading="Key metrics", table={
            "metric": list(ctx.graph_stats.keys()) or ["vertices"],
            "value": [str(v) for v in ctx.graph_stats.values()] or ["0"],
        }),
        ReportSection(heading="Top findings", items=ctx.findings[:5]),
    ]


BUILTIN_TEMPLATES: list[ReportTemplate] = [
    ReportTemplate(
        template_id="impact-assessment",
        name="Impact Assessment",
        description="Bounded graph impact analysis for a change or entity (SR-NLQ-008).",
        parameters=[
            ReportParameter(name="subject", label="Subject entity/change", required=True),
            ReportParameter(name="max_hops", label="Maximum traversal depth", default=6),
        ],
        section_builder=_sections_impact,
    ),
    ReportTemplate(
        template_id="incident-rca",
        name="Incident RCA",
        description="Root-cause analysis with timeline and evidence appendix.",
        parameters=[ReportParameter(name="incident_id", label="Incident identifier", required=True)],
        section_builder=_sections_rca,
    ),
    ReportTemplate(
        template_id="change-risk-review",
        name="Change-Risk Review",
        description="Risk review for a governed change proposal (SR-GOV-003).",
        parameters=[ReportParameter(name="proposal_id", label="Change proposal id", required=True)],
        section_builder=_sections_change_risk,
    ),
    ReportTemplate(
        template_id="compliance-evidence",
        name="Compliance Evidence",
        description="Per-control evidence status and gaps for a compliance pack (SR-GOV-001).",
        parameters=[ReportParameter(name="framework", label="Compliance framework", required=True)],
        section_builder=_sections_compliance,
    ),
    ReportTemplate(
        template_id="executive-brief",
        name="Executive Brief",
        description="One-page narrative summary with key metrics.",
        parameters=[ReportParameter(name="period", label="Reporting period")],
        section_builder=_sections_executive,
    ),
]


def template_by_id(template_id: str) -> ReportTemplate | None:
    for template in BUILTIN_TEMPLATES:
        if template.template_id == template_id:
            return template
    return None


def _sections_to_markdown(title: str, sections: list[ReportSection]) -> str:
    lines = [f"# {title}", ""]
    for section in sections:
        lines.append(f"## {section.heading}")
        lines.append("")
        if section.body_markdown:
            lines.append(section.body_markdown)
            lines.append("")
        if section.items:
            lines.extend(f"- {item}" for item in section.items)
            lines.append("")
        if section.table:
            columns = list(section.table.keys())
            lines.append("| " + " | ".join(columns) + " |")
            lines.append("|" + "---|" * len(columns))
            rows = max((len(v) for v in section.table.values()), default=0)
            for i in range(rows):
                lines.append(
                    "| " + " | ".join(
                        str(section.table[col][i]) if i < len(section.table[col]) else ""
                        for col in columns
                    ) + " |"
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


_HTML_HEAD = """<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
body {{ font-family: -apple-system, "Segoe UI", sans-serif; margin: 2rem auto; max-width: 760px; color: #1a1a2e; }}
h1 {{ border-bottom: 2px solid #4a4e69; padding-bottom: .3rem; }}
h2 {{ color: #4a4e69; margin-top: 1.6rem; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border: 1px solid #cfd2dc; padding: .35rem .6rem; text-align: left; }}
</style></head><body>
"""


def _sections_to_html(title: str, sections: list[ReportSection]) -> str:
    parts = [_HTML_HEAD.format(title=html.escape(title)), f"<h1>{html.escape(title)}</h1>"]
    for section in sections:
        parts.append(f"<h2>{html.escape(section.heading)}</h2>")
        if section.body_markdown:
            parts.append(f"<p>{html.escape(section.body_markdown)}</p>")
        if section.items:
            parts.append("<ul>")
            parts.extend(f"<li>{html.escape(item)}</li>" for item in section.items)
            parts.append("</ul>")
        if section.table:
            columns = list(section.table.keys())
            parts.append("<table><thead><tr>")
            parts.extend(f"<th>{html.escape(col)}</th>" for col in columns)
            parts.append("</tr></thead><tbody>")
            rows = max((len(v) for v in section.table.values()), default=0)
            for i in range(rows):
                parts.append("<tr>")
                for col in columns:
                    cell = str(section.table[col][i]) if i < len(section.table[col]) else ""
                    parts.append(f"<td>{html.escape(cell)}</td>")
                parts.append("</tr>")
            parts.append("</tbody></table>")
    parts.append("</body></html>")
    return "\n".join(parts)


class ReportGenerator:
    """Renders parameterized templates to self-contained HTML / Markdown / JSON."""

    def render(
        self,
        template_id: str,
        ctx: ReportContext,
        *,
        report_format: str = "markdown",
        generated_at: str = "",
    ) -> RenderedReport:
        template = template_by_id(template_id)
        if template is None:
            raise KeyError(f"Unknown template: {template_id}")
        if report_format in EXTERNAL_FORMATS:
            raise ValueError(
                f"Format '{report_format}' is an External gate (SR-NLQ-008): "
                f"supported formats are {SUPPORTED_FORMATS}"
            )
        if report_format not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {report_format}")
        for param in template.parameters:
            if param.required and param.name not in ctx.params:
                raise ValueError(f"Missing required parameter: {param.name}")

        title = ctx.title or template.name
        sections = template.section_builder(ctx)
        if report_format == "markdown":
            content = _sections_to_markdown(title, sections)
        elif report_format == "html":
            content = _sections_to_html(title, sections)
        else:  # json
            content = json.dumps(
                {"title": title, "sections": [s.model_dump() for s in sections]},
                indent=2,
                sort_keys=True,
            )
        return RenderedReport(
            report_id=new_id("reports", "report"),
            template=template_id,
            title=title,
            format=report_format,
            generated_at=generated_at,
            content=content,
            evidence_manifest=ctx.evidence_manifest,
        )
