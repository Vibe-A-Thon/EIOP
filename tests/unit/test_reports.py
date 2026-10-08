"""Unit tests for the report generator, schedules and reports router (SR-NLQ-008)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from eoip.reports import (
    BUILTIN_TEMPLATES,
    ReportContext,
    ReportGenerator,
    ReportScheduleStore,
    next_run_after,
    template_by_id,
)
from eoip.reports.router import build_router


def _ctx(template_id: str, **params) -> ReportContext:
    return ReportContext(
        title="Test Report",
        params=params,
        graph_stats={"vertices": 10, "edges": 42},
        evidence_manifest=[{"ref": "urn:eoip:provenance:evidence:abc"}],
        findings=["finding one", "GAP: missing control"],
        narrative="Everything is explainable.",
    )


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

class TestTemplates:
    def test_five_builtin_templates(self):
        ids = {t.template_id for t in BUILTIN_TEMPLATES}
        assert ids == {
            "impact-assessment", "incident-rca", "change-risk-review",
            "compliance-evidence", "executive-brief",
        }

    def test_template_lookup(self):
        assert template_by_id("incident-rca") is not None
        assert template_by_id("nope") is None


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class TestGenerator:
    @pytest.mark.parametrize("template_id", [t.template_id for t in BUILTIN_TEMPLATES])
    @pytest.mark.parametrize("fmt", ["markdown", "html", "json"])
    def test_render_all_formats(self, template_id, fmt):
        generator = ReportGenerator()
        ctx = _ctx(template_id, subject="s", incident_id="i", proposal_id="p",
                   framework="GDPR", period="2026-Q1")
        report = generator.render(template_id, ctx, report_format=fmt, generated_at="2026-01-01")
        assert report.template == template_id
        assert report.format == fmt
        assert report.content
        assert report.report_id.startswith("urn:eoip:reports:report:")

    def test_markdown_is_self_contained(self):
        report = ReportGenerator().render("impact-assessment", _ctx("impact-assessment", subject="s"))
        assert report.content.startswith("# Test Report")
        assert "## Evidence appendix" in report.content
        assert "urn:eoip:provenance:evidence:abc" in report.content
        assert "| metric |" in report.content  # table rendered

    def test_html_is_self_contained(self):
        report = ReportGenerator().render(
            "incident-rca", _ctx("incident-rca", incident_id="i-1"), report_format="html"
        )
        assert report.content.startswith("<!doctype html>")
        assert "<style>" in report.content
        assert "<table>" in report.content or "<ul>" in report.content
        assert "</html>" in report.content

    def test_external_formats_raise(self):
        for fmt in ("pdf", "docx", "pptx"):
            with pytest.raises(ValueError, match="External gate"):
                ReportGenerator().render(
                    "executive-brief", _ctx("executive-brief"), report_format=fmt
                )

    def test_unknown_format_raises(self):
        with pytest.raises(ValueError):
            ReportGenerator().render("executive-brief", _ctx("executive-brief"), report_format="rtf")

    def test_missing_required_parameter(self):
        with pytest.raises(ValueError, match="subject"):
            ReportGenerator().render("impact-assessment", ReportContext())

    def test_unknown_template(self):
        with pytest.raises(KeyError):
            ReportGenerator().render("nope", ReportContext())

    def test_evidence_manifest_preserved(self):
        report = ReportGenerator().render(
            "compliance-evidence", _ctx("compliance-evidence", framework="GDPR")
        )
        assert report.evidence_manifest == [{"ref": "urn:eoip:provenance:evidence:abc"}]


# ---------------------------------------------------------------------------
# Schedules
# ---------------------------------------------------------------------------

class TestSchedules:
    def test_create_and_due(self, tmp_path: Path):
        store = ReportScheduleStore(tmp_path / "s.json")
        schedule = store.create("executive-brief", "weekly brief", recurrence="weekly")
        assert schedule.schedule_id.startswith("urn:eoip:reports:schedule:")
        assert store.due_schedules()  # never run -> due

    def test_not_due_after_recent_run(self, tmp_path: Path):
        store = ReportScheduleStore(tmp_path / "s.json")
        schedule = store.create("executive-brief", "daily", recurrence="daily")
        store.mark_run(schedule.schedule_id, at=datetime.now(timezone.utc).isoformat())
        assert store.due_schedules() == []

    def test_due_after_period_elapsed(self, tmp_path: Path):
        store = ReportScheduleStore(tmp_path / "s.json")
        schedule = store.create("executive-brief", "daily", recurrence="daily")
        old = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        store.mark_run(schedule.schedule_id, at=old)
        due = store.due_schedules()
        assert [s.schedule_id for s in due] == [schedule.schedule_id]

    def test_disabled_never_due(self, tmp_path: Path):
        store = ReportScheduleStore(tmp_path / "s.json")
        schedule = store.create("executive-brief", "off", recurrence="daily")
        schedule.enabled = False
        assert store.due_schedules() == []

    def test_next_run_after(self):
        last = "2026-01-01T00:00:00+00:00"
        assert next_run_after(last, "daily").day == 2
        assert next_run_after(last, "weekly").day == 8
        assert next_run_after(last, "monthly").day == 31

    def test_persistence(self, tmp_path: Path):
        path = tmp_path / "s.json"
        store = ReportScheduleStore(path)
        schedule = store.create("incident-rca", "rca", params={"incident_id": "i"})
        reloaded = ReportScheduleStore(path)
        assert reloaded.get(schedule.schedule_id).params == {"incident_id": "i"}

    def test_delete(self, tmp_path: Path):
        store = ReportScheduleStore(tmp_path / "s.json")
        schedule = store.create("executive-brief", "x")
        assert store.delete(schedule.schedule_id)
        assert not store.delete(schedule.schedule_id)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def _client(tmp_path: Path):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()
    app.include_router(build_router(schedule_store=ReportScheduleStore(tmp_path / "s.json")))
    return TestClient(app)


class TestReportsRouter:
    def test_templates_endpoint(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.get("/api/v1/reports/templates")
        assert resp.status_code == 200
        assert len(resp.json()) == 5

    def test_render_markdown(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.post("/api/v1/reports/render", params={
            "template_id": "executive-brief", "report_format": "markdown",
        }, json={"narrative": "Summary text."})
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["content"].startswith("# ")
        assert "Summary text." in body["content"]

    def test_render_html(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.post("/api/v1/reports/render", params={
            "template_id": "incident-rca", "report_format": "html",
        }, json={"params": {"incident_id": "i-9"}})
        assert resp.status_code == 200
        assert resp.json()["content"].startswith("<!doctype html>")

    def test_render_external_format_501(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.post("/api/v1/reports/render", params={
            "template_id": "executive-brief", "report_format": "pdf",
        }, json={})
        assert resp.status_code == 501
        assert "External gate" in resp.json()["detail"]

    def test_render_unknown_template_404(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.post("/api/v1/reports/render", params={"template_id": "nope"}, json={})
        assert resp.status_code == 404

    def test_schedule_endpoints(self, tmp_path: Path):
        client = _client(tmp_path)
        resp = client.post("/api/v1/reports/schedules", params={
            "template_id": "executive-brief", "name": "weekly brief",
            "recurrence": "weekly",
        })
        assert resp.status_code == 201, resp.text
        schedule_id = resp.json()["schedule_id"]
        assert client.get("/api/v1/reports/schedules").json()
        assert client.get("/api/v1/reports/schedules/due").json()
        assert client.post(f"/api/v1/reports/schedules/{schedule_id}/mark-run").status_code == 200
        assert client.delete(f"/api/v1/reports/schedules/{schedule_id}").status_code == 204
        assert client.delete(f"/api/v1/reports/schedules/{schedule_id}").status_code == 404
