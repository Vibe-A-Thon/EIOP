"""CRA-024 A.2: federated query joining local Jira nodes with virtualized Snowflake tables, within the deadline.

PENDING LIVE VALIDATION: Jira is the REST v3 enhanced-search contract mock (paged with nextPageToken) driven
through the production JiraConnector; Snowflake is the fakesnow emulator behind the official connector API.
Correctness is checked against an oracle computed independently from the generated source data.
"""
from __future__ import annotations

import random
import time

import httpx
import pytest
from eoip.connectors.jira import JiraConnector
from eoip.federation.executors import SnowflakeSqlExecutor
from eoip.federation.jira_snowflake import (
    DEADLINE_S,
    VALIDATION_STATUS,
    ingest_jira_work_items,
    query_work_items_with_snowflake,
)
from eoip.federation.obda import FederatedDataSource, OBDAFederationEngine, SemanticsMode, SourceAuthDelegation
from eoip.graph.memory import MemoryGraphStore

fakesnow = pytest.importorskip("fakesnow")
snowflake_connector = pytest.importorskip("snowflake.connector")
pytestmark = pytest.mark.req("CRA-024")

N_ISSUES, PAGE = 3000, 100
STATUSES = ["Open", "In Progress", "Done"]


def _issues():
    return [{"id": str(10000 + i), "key": f"PROJ-{i}", "fields": {
        "summary": f"Work item {i}", "project": {"key": "PROJ"}, "issuetype": {"id": "1", "name": "Story"},
        "status": {"id": str(i % 3), "name": STATUSES[i % 3]},
        "created": "2026-10-01T10:00:00.000+0000", "updated": f"2026-10-02T12:{i % 60:02d}:00.000+0000"}}
        for i in range(N_ISSUES)]


def _jira_handler(issues, calls):
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        calls.append(path)
        if path.endswith("/project/PROJ"):
            return httpx.Response(200, json={"key": "PROJ", "name": "Project", "id": "1000"})
        if path.endswith("/project/PROJ/version") or path.endswith("/project/PROJ/statuses"):
            return httpx.Response(200, json=[] if path.endswith("statuses") else {"values": []})
        if path.endswith("/search/jql"):
            import json as _j
            body = _j.loads(request.content)
            start = int(body.get("nextPageToken") or 0)
            page = issues[start:start + int(body["maxResults"])]
            nxt = start + len(page)
            return httpx.Response(200, json={"issues": page, "isLast": nxt >= len(issues),
                                             **({"nextPageToken": str(nxt)} if nxt < len(issues) else {})})
        return httpx.Response(404, json={"error": "not found"})
    return handler


@pytest.fixture()
def world():
    rng = random.Random(24)
    invoices = []
    for i in range(N_ISSUES):
        for _ in range(rng.randint(0, 3)):
            invoices.append((f"PROJ-{i}", rng.randint(1, 5000), rng.choice(["eu", "us"])))
    invoices += [(None, 7, "eu"), ("PROJ-999999", 11, "eu")]  # NULL key and an orphan key never join
    with fakesnow.patch():
        real_connect = snowflake_connector.connect

        def connect(**kwargs):
            return real_connect(database=kwargs.get("database"), schema=kwargs.get("schema"))

        setup = real_connect(database="FIN", schema="BILLING")
        cur = setup.cursor()
        cur.execute("create table INVOICES (JIRA_KEY varchar, COST_USD number(10,2), REGION varchar)")
        cur.executemany("insert into INVOICES values (%s, %s, %s)", invoices)
        calls: list[str] = []
        client = httpx.Client(base_url="https://jira.example", transport=httpx.MockTransport(_jira_handler(_issues(), calls)))
        conn = JiraConnector("jira-prod", "https://jira.example", projects=["PROJ"], token="mock-token", client=client,
                             include_comments=False, include_changelog=False, page_size=PAGE)
        store = MemoryGraphStore()
        auth = SourceAuthDelegation("snowflake_billing", "tenant_alpha", "BASIC",
                                    {"username": "svc_tenant_alpha", "password": "from-vault"})
        engine = OBDAFederationEngine()
        engine.register_source(FederatedDataSource("snowflake_billing", "SNOWFLAKE", "h1",
                                                    watermark_timestamp=1_700_000_000.0, auth_delegation=auth),
                               executor=SnowflakeSqlExecutor("INVOICES", database="FIN", schema="BILLING",
                                                             auth=auth, connect=connect))
        yield conn, store, engine, invoices, calls


def _oracle(invoices, status, region):
    local = {f"PROJ-{i}" for i in range(N_ISSUES) if STATUSES[i % 3] == status}
    remote = {(k, float(c)) for k, c, r in invoices if r == region and k is not None}  # SET semantics
    out = set()
    for key in local:
        matches = {c for k, c in remote if k == key}
        out |= {(key, c) for c in matches} if matches else {(key, None)}
    return out


def test_federated_jira_nodes_x_snowflake_correct_within_deadline(world):
    conn, store, engine, invoices, calls = world
    t0 = time.perf_counter()
    assert ingest_jira_work_items(conn, store) == N_ISSUES
    assert sum(p.endswith("/search/jql") for p in calls) == N_ISSUES // PAGE  # paged through the REST API
    assert store.count_vertices("WorkItem") == N_ISSUES
    res = query_work_items_with_snowflake(store, engine, "snowflake_billing",
                                          local_filters={"status": "In Progress"},
                                          remote_filters={"region": "eu"},
                                          remote_projection=["jira_key", "cost_usd"])
    total_s = time.perf_counter() - t0
    assert res.status == "SUCCESS" and res.validation == VALIDATION_STATUS
    assert res.local_rows == N_ISSUES // 3
    assert res.remote_sql == "SELECT jira_key, cost_usd FROM INVOICES WHERE region = %(p0)s"  # pushed down
    got = {(r["issue_key"], None if r.get("remote_cost_usd") is None else float(r["remote_cost_usd"]))
           for r in res.rows}
    assert got == _oracle(invoices, "In Progress", "eu")
    assert len(res.rows) == len(got)  # SET semantics: no duplicate rows
    assert res.elapsed_ms < DEADLINE_S * 1000 and total_s < DEADLINE_S  # ingestion + query inside the budget


def test_bag_semantics_keep_duplicate_invoices(world):
    conn, store, engine, invoices, _ = world
    ingest_jira_work_items(conn, store)
    res = query_work_items_with_snowflake(store, engine, "snowflake_billing", local_filters={"status": "Done"},
                                          remote_filters={"region": "us"}, remote_projection=["jira_key", "cost_usd"],
                                          semantics=SemanticsMode.BAG)
    done = {f"PROJ-{i}" for i in range(N_ISSUES) if i % 3 == 2}
    matched = sum(1 for k, _, r in invoices if r == "us" and k in done)
    unmatched = len(done - {k for k, _, r in invoices if r == "us"})
    assert res.status == "SUCCESS" and len(res.rows) == matched + unmatched


def test_deadline_is_enforced_without_partial_rows(world):
    conn, store, engine, _, _ = world
    ingest_jira_work_items(conn, store)
    slow = engine._source_executors["snowflake_billing"]

    def stalled(fragment):
        time.sleep(3)
        return slow(fragment)

    engine._source_executors["snowflake_billing"] = stalled
    res = query_work_items_with_snowflake(store, engine, "snowflake_billing", deadline_s=0.5)
    assert res.status == "TIMEOUT" and res.rows == [] and res.elapsed_ms < 2000
    assert res.deadline_s == 0.5


def test_tenant_budget_cannot_raise_the_deadline(world):
    conn, store, engine, _, _ = world
    res = query_work_items_with_snowflake(store, engine, "snowflake_billing", deadline_s=120)
    assert res.deadline_s == DEADLINE_S


def test_snowflake_outage_degrades_to_partial_with_diagnostic(world):
    conn, store, engine, _, _ = world
    ingest_jira_work_items(conn, store)

    def down(fragment):
        raise ConnectionError("snowflake unreachable")

    engine._source_executors["snowflake_billing"] = down
    res = query_work_items_with_snowflake(store, engine, "snowflake_billing", local_filters={"status": "Open"})
    assert res.status == "PARTIAL" and res.degraded_sources == ["snowflake_billing"]
    assert "snowflake unreachable" in res.errors["snowflake_billing"]
