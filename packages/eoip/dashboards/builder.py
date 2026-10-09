"""Dashboard Builder — drag-and-drop composable dashboard framework.

Supports graph metrics, KPIs, time-series, topology views, tables,
and custom widgets with configurable data sources, refresh intervals,
and layout positioning.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class WidgetType(str, Enum):
    METRIC_CARD = "METRIC_CARD"
    LINE_CHART = "LINE_CHART"
    BAR_CHART = "BAR_CHART"
    PIE_CHART = "PIE_CHART"
    HEATMAP = "HEATMAP"
    TABLE = "TABLE"
    GRAPH_TOPOLOGY = "GRAPH_TOPOLOGY"
    KPI_GAUGE = "KPI_GAUGE"
    TIMELINE = "TIMELINE"
    STAT_COUNTER = "STAT_COUNTER"
    ALERT_LIST = "ALERT_LIST"
    SYSTEM_STATUS = "SYSTEM_STATUS"
    QUERY_RESULT = "QUERY_RESULT"
    LOG_STREAM = "LOG_STREAM"
    CUSTOM = "CUSTOM"


@dataclass
class WidgetPosition:
    x: int = 0
    y: int = 0
    width: int = 4
    height: int = 3
    min_width: int = 2
    min_height: int = 2


@dataclass
class WidgetDataSource:
    source_type: str = "query"  # query, metric, api, static, computed
    query: str = ""
    endpoint: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    refresh_interval_seconds: int = 60
    transform: str | None = None  # jq-like expression


@dataclass
class DashboardWidget:
    widget_id: str
    widget_type: WidgetType
    title: str
    data_source: WidgetDataSource = field(default_factory=WidgetDataSource)
    position: WidgetPosition = field(default_factory=WidgetPosition)
    config: dict[str, Any] = field(default_factory=dict)
    # config examples: {"color": "#3b82f6", "threshold": 95, "unit": "%",
    #                   "sparkline": true, "stacked": false}
    filters: dict[str, Any] = field(default_factory=dict)
    visible: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DashboardLayout:
    columns: int = 12
    row_height: int = 80
    gap: int = 8
    responsive_breakpoints: dict[str, int] = field(
        default_factory=lambda: {"lg": 1200, "md": 996, "sm": 768, "xs": 480}
    )


@dataclass
class Dashboard:
    dashboard_id: str
    name: str
    description: str = ""
    owner: str = ""
    widgets: list[DashboardWidget] = field(default_factory=list)
    layout: DashboardLayout = field(default_factory=DashboardLayout)
    global_filters: dict[str, Any] = field(default_factory=dict)
    refresh_interval_seconds: int = 300
    tags: list[str] = field(default_factory=list)
    shared_with: list[str] = field(default_factory=list)
    is_default: bool = False
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def add_widget(self, widget: DashboardWidget) -> None:
        self.widgets.append(widget)

    def remove_widget(self, widget_id: str) -> bool:
        before = len(self.widgets)
        self.widgets = [w for w in self.widgets if w.widget_id != widget_id]
        return len(self.widgets) < before

    def get_widget(self, widget_id: str) -> DashboardWidget | None:
        for w in self.widgets:
            if w.widget_id == widget_id:
                return w
        return None


class DashboardStore:
    """In-memory dashboard persistence with CRUD operations."""

    def __init__(self) -> None:
        self._dashboards: dict[str, Dashboard] = {}
        self._lock = threading.RLock()
        self._create_default_dashboards()

    def _create_default_dashboards(self) -> None:
        overview = Dashboard(
            dashboard_id="dash-overview",
            name="Platform Overview",
            description="System health, ingestion stats, and graph metrics",
            is_default=True,
            created_at=self._now(),
            widgets=[
                DashboardWidget(
                    widget_id="w-total-entities", widget_type=WidgetType.STAT_COUNTER,
                    title="Total Entities",
                    data_source=WidgetDataSource(source_type="metric", query="graph.entity_count"),
                    position=WidgetPosition(x=0, y=0, width=3, height=2),
                ),
                DashboardWidget(
                    widget_id="w-total-relationships", widget_type=WidgetType.STAT_COUNTER,
                    title="Total Relationships",
                    data_source=WidgetDataSource(source_type="metric", query="graph.edge_count"),
                    position=WidgetPosition(x=3, y=0, width=3, height=2),
                ),
                DashboardWidget(
                    widget_id="w-systems-status", widget_type=WidgetType.SYSTEM_STATUS,
                    title="Connected Systems",
                    data_source=WidgetDataSource(source_type="api", endpoint="/api/v1/systems/"),
                    position=WidgetPosition(x=6, y=0, width=6, height=4),
                ),
                DashboardWidget(
                    widget_id="w-ingestion-timeline", widget_type=WidgetType.TIMELINE,
                    title="Ingestion Activity",
                    data_source=WidgetDataSource(source_type="metric", query="ingestion.records_per_hour"),
                    position=WidgetPosition(x=0, y=2, width=6, height=4),
                ),
                DashboardWidget(
                    widget_id="w-quality-scores", widget_type=WidgetType.BAR_CHART,
                    title="Data Quality by Entity Type",
                    data_source=WidgetDataSource(source_type="metric", query="quality.avg_scores_by_type"),
                    position=WidgetPosition(x=0, y=6, width=6, height=4),
                ),
                DashboardWidget(
                    widget_id="w-alert-list", widget_type=WidgetType.ALERT_LIST,
                    title="Recent Alerts",
                    data_source=WidgetDataSource(source_type="api", endpoint="/api/v1/alerts/recent"),
                    position=WidgetPosition(x=6, y=4, width=6, height=4),
                ),
            ],
        )
        self._dashboards[overview.dashboard_id] = overview

    def create(self, dashboard: Dashboard) -> Dashboard:
        with self._lock:
            if not dashboard.dashboard_id:
                dashboard.dashboard_id = f"dash-{uuid.uuid4().hex[:8]}"
            now = self._now()
            dashboard.created_at = now
            dashboard.updated_at = now
            self._dashboards[dashboard.dashboard_id] = dashboard
            return dashboard

    def get(self, dashboard_id: str) -> Dashboard | None:
        return self._dashboards.get(dashboard_id)

    def list(self, owner: str | None = None, tag: str | None = None) -> list[Dashboard]:
        dashboards = list(self._dashboards.values())
        if owner:
            dashboards = [d for d in dashboards if d.owner == owner]
        if tag:
            dashboards = [d for d in dashboards if tag in d.tags]
        return dashboards

    def update(self, dashboard_id: str, updates: dict[str, Any]) -> Dashboard | None:
        with self._lock:
            d = self._dashboards.get(dashboard_id)
            if not d:
                return None
            for k, v in updates.items():
                if hasattr(d, k):
                    setattr(d, k, v)
            d.updated_at = self._now()
            return d

    def delete(self, dashboard_id: str) -> bool:
        with self._lock:
            return self._dashboards.pop(dashboard_id, None) is not None

    def clone(self, dashboard_id: str, new_name: str) -> Dashboard | None:
        src = self._dashboards.get(dashboard_id)
        if not src:
            return None
        import copy
        clone = copy.deepcopy(src)
        clone.dashboard_id = f"dash-{uuid.uuid4().hex[:8]}"
        clone.name = new_name
        clone.is_default = False
        return self.create(clone)

    def _now(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class DashboardBuilder:
    """High-level API for composing dashboards programmatically."""

    def __init__(self, store: DashboardStore | None = None) -> None:
        self._store = store or DashboardStore()

    @property
    def store(self) -> DashboardStore:
        return self._store

    def new_dashboard(self, name: str, description: str = "", owner: str = "") -> Dashboard:
        return self._store.create(Dashboard(
            dashboard_id="", name=name, description=description, owner=owner,
        ))

    def add_metric_card(self, dashboard_id: str, title: str, metric_query: str,
                        unit: str = "", threshold: float | None = None) -> DashboardWidget:
        widget = DashboardWidget(
            widget_id=f"w-{uuid.uuid4().hex[:6]}",
            widget_type=WidgetType.METRIC_CARD,
            title=title,
            data_source=WidgetDataSource(source_type="metric", query=metric_query),
            config={"unit": unit, "threshold": threshold},
        )
        d = self._store.get(dashboard_id)
        if d:
            d.add_widget(widget)
        return widget

    def add_chart(self, dashboard_id: str, title: str, chart_type: WidgetType,
                  query: str, config: dict[str, Any] | None = None) -> DashboardWidget:
        widget = DashboardWidget(
            widget_id=f"w-{uuid.uuid4().hex[:6]}",
            widget_type=chart_type,
            title=title,
            data_source=WidgetDataSource(source_type="query", query=query),
            config=config or {},
        )
        d = self._store.get(dashboard_id)
        if d:
            d.add_widget(widget)
        return widget

    def add_topology_view(self, dashboard_id: str, title: str,
                          entity_types: list[str] | None = None) -> DashboardWidget:
        widget = DashboardWidget(
            widget_id=f"w-{uuid.uuid4().hex[:6]}",
            widget_type=WidgetType.GRAPH_TOPOLOGY,
            title=title,
            data_source=WidgetDataSource(source_type="query", query="MATCH (n) RETURN n LIMIT 100"),
            config={"entity_types": entity_types or [], "layout": "force-directed"},
        )
        d = self._store.get(dashboard_id)
        if d:
            d.add_widget(widget)
        return widget
