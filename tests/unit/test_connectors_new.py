"""Tests for new connectors: Rally, Grafana, Datadog, Kibana, qTest, Figma, API Portal."""

from unittest.mock import MagicMock

import pytest


class TestRallyConnector:
    def test_init(self):
        from eoip.connectors.rally import RallyConnector
        c = RallyConnector("https://rally1.rallydev.com", token="tok")
        assert c.source_system == "rally"
        assert "user_story" in c.types

    def test_init_custom_types(self):
        from eoip.connectors.rally import RallyConnector
        c = RallyConnector("https://rally1.rallydev.com", token="tok",
                           types={"defect": "Defect"})
        assert "defect" in c.types
        assert "user_story" in c.types

    def test_init_invalid_page_size(self):
        from eoip.connectors.rally import RallyConnector
        with pytest.raises(ValueError, match="page_size"):
            RallyConnector("https://rally1.rallydev.com", token="tok", page_size=0)

    def test_map_event(self):
        from eoip.connectors.rally import RallyConnector
        c = RallyConnector("https://rally1.rallydev.com", token="tok")
        event = MagicMock()
        event.payload = {
            "ObjectID": 12345, "Name": "Story-1", "Description": "desc",
            "ScheduleState": "Defined", "PlanEstimate": 5, "FormattedID": "US100",
            "Iteration": {"_refObjectName": "Sprint 1"},
            "Release": {"_refObjectName": "R1"},
        }
        event.metadata = {"record_kind": "user_story"}
        mapped = c.map_event(event)
        assert mapped["kind"] == "user_story"
        assert mapped["record_id"] == "12345"
        assert mapped["name"] == "Story-1"
        assert mapped["iteration"] == "Sprint 1"

    def test_map_event_unsupported_kind(self):
        from eoip.connectors.rally import RallyConnector
        c = RallyConnector("https://rally1.rallydev.com", token="tok")
        event = MagicMock()
        event.payload = {"ObjectID": 1}
        event.metadata = {"record_kind": "unknown_type"}
        with pytest.raises(ValueError, match="unsupported"):
            c.map_event(event)


class TestGrafanaConnector:
    def test_init(self):
        from eoip.connectors.grafana import GrafanaConnector
        c = GrafanaConnector("https://grafana.example.com", token="tok")
        assert c.source_system == "grafana"

    @pytest.mark.req("G2-SRC-GRAF-002", "G2-SRC-GRAF-003")
    def test_map_event_dashboard(self):
        from eoip.connectors.grafana import GrafanaConnector
        c = GrafanaConnector("https://grafana.example.com", token="tok")
        event = MagicMock()
        event.payload = {"uid": "abc123", "title": "API Latency", "url": "/d/abc123"}
        event.metadata = {"record_kind": "dashboard"}
        mapped = c.map_event(event)
        assert mapped["kind"] == "dashboard"
        assert mapped["title"] == "API Latency"
        assert mapped["dashboard_uid"] == "abc123"


class TestDatadogConnector:
    def test_init(self):
        from eoip.connectors.datadog import DatadogConnector
        c = DatadogConnector("https://api.datadoghq.com", api_key="k", app_key="a")
        assert c.source_system == "datadog"

    @pytest.mark.req("G2-SRC-DD-002", "G2-SRC-DD-003", "G2-SRC-DD-004")
    def test_map_event(self):
        from eoip.connectors.datadog import DatadogConnector
        c = DatadogConnector("https://api.datadoghq.com", api_key="k", app_key="a")
        event = MagicMock()
        event.payload = {"id": "dash-1", "title": "Overview", "url": "/dashboard/dash-1"}
        event.metadata = {"record_kind": "dashboard"}
        mapped = c.map_event(event)
        assert mapped["kind"] == "dashboard"
        assert mapped["title"] == "Overview"


class TestKibanaConnector:
    def test_init(self):
        from eoip.connectors.kibana import KibanaConnector
        c = KibanaConnector("https://kibana.example.com", token="tok")
        assert c.source_system == "kibana"

    @pytest.mark.req("G2-SRC-KIB-002", "G2-SRC-KIB-003", "G2-SRC-KIB-004", "G2-SRC-KIB-005")
    def test_map_event(self):
        from eoip.connectors.kibana import KibanaConnector
        c = KibanaConnector("https://kibana.example.com", token="tok")
        event = MagicMock()
        event.payload = {"id": "saved-1", "attributes": {"title": "Error Logs"}, "type": "dashboard"}
        event.metadata = {"record_kind": "dashboard"}
        mapped = c.map_event(event)
        assert mapped["kind"] == "dashboard"
        assert mapped["title"] == "Error Logs"


class TestQTestConnector:
    def test_init(self):
        from eoip.connectors.qtest import QTestConnector
        c = QTestConnector("https://qtest.example.com", project_id=123, token="tok")
        assert c.source_system == "qtest"

    def test_map_event(self):
        from eoip.connectors.qtest import QTestConnector
        c = QTestConnector("https://qtest.example.com", project_id=123, token="tok")
        event = MagicMock()
        event.payload = {"id": 456, "name": "Login Test", "pid": "TC-456"}
        event.metadata = {"record_kind": "test_case"}
        mapped = c.map_event(event)
        assert mapped["kind"] == "test_case"
        assert mapped["name"] == "Login Test"


class TestFigmaConnector:
    def test_init(self):
        from eoip.connectors.figma import FigmaConnector
        c = FigmaConnector(team_id="team-1", token="tok")
        assert c.source_system == "figma"

    def test_map_event_file(self):
        from eoip.connectors.figma import FigmaConnector
        c = FigmaConnector(team_id="team-1", token="tok")
        event = MagicMock()
        event.payload = {"key": "fk-1", "name": "Homepage", "last_modified": "2024-01-01"}
        event.metadata = {"record_kind": "file"}
        mapped = c.map_event(event)
        assert mapped["kind"] == "file"
        assert mapped["name"] == "Homepage"
        assert mapped["file_key"] == "fk-1"


class TestAPIPortalConnector:
    def test_init(self):
        from eoip.connectors.api_portal import APIPortalConnector
        c = APIPortalConnector("https://portal.example.com", token="tok")
        assert c.source_system == "api_portal"

    def test_map_event(self):
        from eoip.connectors.api_portal import APIPortalConnector
        c = APIPortalConnector("https://portal.example.com", token="tok")
        event = MagicMock()
        event.payload = {"id": "svc-1", "name": "User API", "version": "v2"}
        event.metadata = {"record_kind": "service"}
        mapped = c.map_event(event)
        assert mapped["kind"] == "service"
        assert mapped["api_name"] == "User API"
