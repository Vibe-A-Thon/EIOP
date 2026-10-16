"""Scheduled / recurring report definitions (SR-NLQ-008).

A schedule binds a template + parameters to a recurrence (daily / weekly /
monthly) and an output format. ``due_schedules(now)`` returns definitions
whose next run has passed; the caller (jobs runner / wiring step) renders
and records ``last_run_at``. Scheduling execution itself is External gate:
this module is the durable definition store; a cron/APScheduler-style
runner is intentionally not bundled.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from eoip.compliance.pack import new_id

Recurrence = Literal["daily", "weekly", "monthly"]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def next_run_after(last_run_at: str, recurrence: Recurrence) -> datetime:
    last = datetime.fromisoformat(last_run_at)
    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)
    days = {"daily": 1, "weekly": 7, "monthly": 30}[recurrence]
    return last.fromtimestamp(last.timestamp() + days * 86400, tz=timezone.utc)


class ReportSchedule(BaseModel):
    """A scheduled/recurring report definition (SR-NLQ-008)."""

    model_config = ConfigDict(extra="forbid")

    schedule_id: str
    template_id: str
    name: str
    recurrence: Recurrence = "weekly"
    params: dict[str, Any] = Field(default_factory=dict)
    report_format: str = "markdown"
    enabled: bool = True
    last_run_at: str | None = None
    tenant_id: str | None = None
    created_by: str | None = None

    def is_due(self, now: datetime | None = None) -> bool:
        if not self.enabled:
            return False
        now = now or datetime.now(timezone.utc)
        if self.last_run_at is None:
            return True
        return now >= next_run_after(self.last_run_at, self.recurrence)


class ReportScheduleStore:
    """JSON-file store for recurring report definitions (SR-NLQ-008)."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._lock = RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "report-schedules.json"
        self._items: dict[str, ReportSchedule] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for item in data.get("schedules", []):
            schedule = ReportSchedule(**item)
            self._items[schedule.schedule_id] = schedule

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schedules": [s.model_dump() for s in self._items.values()]}
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def create(
        self,
        template_id: str,
        name: str,
        *,
        recurrence: Recurrence = "weekly",
        params: dict[str, Any] | None = None,
        report_format: str = "markdown",
        tenant_id: str | None = None,
        created_by: str | None = None,
    ) -> ReportSchedule:
        schedule = ReportSchedule(
            schedule_id=new_id("reports", "schedule"),
            template_id=template_id,
            name=name,
            recurrence=recurrence,
            params=params or {},
            report_format=report_format,
            tenant_id=tenant_id,
            created_by=created_by,
        )
        with self._lock:
            self._items[schedule.schedule_id] = schedule
            self._save()
        return schedule

    def get(self, schedule_id: str, tenant_id: str | None = None) -> ReportSchedule | None:
        schedule = self._items.get(schedule_id)
        if schedule is None:
            return None
        if tenant_id and schedule.tenant_id and schedule.tenant_id != tenant_id:
            return None
        return schedule

    def list(self, tenant_id: str | None = None) -> list[ReportSchedule]:
        if not tenant_id:
            return list(self._items.values())
        return [s for s in self._items.values() if not s.tenant_id or s.tenant_id == tenant_id]

    def due_schedules(self, now: datetime | None = None) -> list[ReportSchedule]:
        return [s for s in self._items.values() if s.is_due(now)]

    def mark_run(self, schedule_id: str, *, at: str | None = None) -> ReportSchedule:
        with self._lock:
            schedule = self._items.get(schedule_id)
            if schedule is None:
                raise KeyError(f"Unknown schedule: {schedule_id}")
            schedule.last_run_at = at or utc_now_iso()
            self._save()
            return schedule

    def delete(self, schedule_id: str, tenant_id: str | None = None) -> bool:
        with self._lock:
            schedule = self._items.get(schedule_id)
            if schedule is None:
                return False
            if tenant_id and schedule.tenant_id and schedule.tenant_id != tenant_id:
                return False
            existed = self._items.pop(schedule_id, None) is not None
            if existed:
                self._save()
            return existed

    def run_schedule(
        self,
        schedule_id: str,
        generator: Any,
        artifact_store: Any,
        *,
        tenant_id: str | None = None,
        now: datetime | None = None,
    ) -> Any:
        schedule = self.get(schedule_id, tenant_id=tenant_id)
        if schedule is None:
            raise KeyError(f"Unknown schedule: {schedule_id}")

        from eoip.reports.generator import ReportContext
        ctx = ReportContext(
            title=schedule.name,
            params=schedule.params,
            graph_stats=schedule.params.get("graph_stats", {}),
        )

        rendered = generator.render(
            schedule.template_id,
            ctx,
            report_format=schedule.report_format,
            allow_external_formats=True,
            tenant_id=schedule.tenant_id,
            created_by=schedule.created_by,
        )
        artifact_store.put(rendered)
        self.mark_run(schedule_id, at=(now.isoformat() if now else None))
        return rendered

