"""FT-D03: CMDB tables are known profiles (CRA-008.6) but synced only on opt-in;
a missing/forbidden optional table is skipped with a warning, not a failed sync."""

import httpx
import pytest

from eoip.connectors.errors import ConnectorError
from eoip.connectors.servicenow import CORE_TABLES, OPTIONAL_TABLES, ServiceNowConnector

ROWS = {
    "incident": [{"sys_id": "i-1", "number": "INC001"}],
    "problem": [], "change_request": [], "kb_knowledge": [],
    "cmdb_ci": [{"sys_id": "ci-1", "number": "CI001", "name": "srv1"}],
}


def _connector(handler, **kwargs):
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return ServiceNowConnector("https://sn.local", token="t", client=client, **kwargs)


def _handler(requested, missing=()):
    def handle(request):
        table = request.url.path.rsplit("/", 1)[-1]
        requested.append(table)
        if table in missing:
            return httpx.Response(404, json={"error": "Invalid table"})
        return httpx.Response(200, json={"result": ROWS.get(table, [])})
    return handle


def test_default_sync_requests_only_fr_snow_001_tables():
    requested = []
    connector = _connector(_handler(requested))
    assert set(OPTIONAL_TABLES) <= set(connector.tables)  # profiles still known (CRA-008.6)
    connector.sync(watermark="2026-10-03T00:00:00Z")
    assert set(requested) == set(CORE_TABLES.values())


def test_include_cmdb_syncs_cmdb_and_skips_a_missing_optional_table():
    requested = []
    connector = _connector(_handler(requested, missing={"cmdb_rel_ci"}), include_cmdb=True)
    batch = connector.sync(watermark="2026-10-03T00:00:00Z")
    assert {"cmdb_ci", "cmdb_rel_ci"} <= set(requested)
    assert {e.metadata["record_kind"] for e in batch.events} == {"incident", "cmdb_ci"}
    assert connector.skipped_tables == [{"table": "cmdb_rel_ci", "category": "remote_error"}]


def test_core_table_errors_still_fail_the_sync():
    connector = _connector(_handler([], missing={"problem"}), include_cmdb=True)
    with pytest.raises(ConnectorError):
        connector.sync(watermark="2026-10-03T00:00:00Z")
