"""CRA-024.4 / CRA-024.A.2: OBDA federation over real source executors.

Snowflake: executed through the official snowflake-connector-python DB-API against the fakesnow
emulator (DuckDB-backed). Jira: Jira Cloud enhanced search API (POST /rest/api/3/search/jql)
contract mocks with the documented request/response shapes, pagination, 429 Retry-After and 401.
Residual gap: live validation with a customer Snowflake account / Jira site is pending.
"""
from __future__ import annotations

import base64
import json

import httpx
import pytest

from eoip.federation.executors import (
    JiraRestExecutor,
    SnowflakeSqlExecutor,
    SourceAuthError,
    build_jql,
)
from eoip.federation.obda import (
    FederatedDataSource,
    FederatedPushdownFragment,
    OBDAFederationEngine,
    SemanticsMode,
    SourceAuthDelegation,
    SourceExecutorMissing,
)

fakesnow = pytest.importorskip("fakesnow")
snowflake_connector = pytest.importorskip("snowflake.connector")

pytestmark = pytest.mark.req("CRA-024")


@pytest.fixture()
def snowflake_db():
    """fakesnow-patched snowflake.connector with a BILLING table; yields the list of connect kwargs seen."""
    seen: list[dict] = []
    with fakesnow.patch():
        real_connect = snowflake_connector.connect

        def connect(**kwargs):
            seen.append(dict(kwargs))
            # fakesnow ignores credentials; route to the emulated database
            return real_connect(database=kwargs.get("database"), schema=kwargs.get("schema"))

        setup = real_connect(database="FIN", schema="BILLING")
        cur = setup.cursor()
        cur.execute("create table INVOICES (JIRA_KEY varchar, COST_USD number(10,2), REGION varchar)")
        cur.executemany(
            "insert into INVOICES values (%s, %s, %s)",
            [("PROJ-1", 1250, "eu"), ("PROJ-2", 3400, "us"), ("PROJ-1", 1250, "eu"),
             (None, 99, "eu"), ("PROJ-9", 10, "eu")],
        )
        yield connect, seen, setup


def _sf_source(sid="snowflake_billing"):
    auth = SourceAuthDelegation(sid, "tenant_alpha", "BASIC",
                                {"username": "svc_tenant_alpha", "password": "pw-from-vault"})
    return auth, FederatedDataSource(sid, "SNOWFLAKE", "h1", watermark_timestamp=1_700_000_000.0,
                                     auth_delegation=auth)


def test_snowflake_executor_pushdown_binds_parameters_and_delegates_auth(snowflake_db):
    connect, seen, _ = snowflake_db
    auth, source = _sf_source()
    ex = SnowflakeSqlExecutor("INVOICES", account="acme-xy123", database="FIN", schema="BILLING",
                              warehouse="WH", auth=auth, connect=connect)
    engine = OBDAFederationEngine()
    engine.register_source(source, executor=ex)
    frag = engine.plan_pushdown("snowflake_billing", {"region": "eu"}, ["jira_key", "cost_usd"])
    rows = ex(frag)
    # predicate and projection were pushed down to the source, value bound not interpolated
    assert ex.last_sql == "SELECT jira_key, cost_usd FROM INVOICES WHERE region = %(p0)s"
    assert ex.last_params == {"p0": "eu"}
    assert sorted((r["jira_key"] or "", float(r["cost_usd"])) for r in rows) == [
        ("", 99.0), ("PROJ-1", 1250.0), ("PROJ-1", 1250.0), ("PROJ-9", 10.0)]
    # per-tenant credential propagation reached the connector
    assert seen[0]["user"] == "svc_tenant_alpha" and seen[0]["password"] == "pw-from-vault"
    assert seen[0]["account"] == "acme-xy123" and seen[0]["warehouse"] == "WH"


def test_snowflake_value_injection_is_inert_and_identifier_injection_rejected(snowflake_db):
    connect, _, setup = snowflake_db
    auth, _ = _sf_source()
    ex = SnowflakeSqlExecutor("INVOICES", database="FIN", schema="BILLING", auth=auth, connect=connect)
    frag = FederatedPushdownFragment("f", "s", {"region": "eu' OR '1'='1"}, ["jira_key"], "")
    assert ex(frag) == []
    cur = setup.cursor()
    cur.execute("select count(*) from INVOICES")
    assert cur.fetchone()[0] == 5
    with pytest.raises(ValueError):
        ex(FederatedPushdownFragment("f", "s", {"region; drop table INVOICES": 1}, [], ""))
    with pytest.raises(ValueError):
        SnowflakeSqlExecutor("INVOICES; drop table X")


def test_federated_join_snowflake_null_bag_set_semantics(snowflake_db):
    connect, _, _ = snowflake_db
    auth, source = _sf_source()
    engine = OBDAFederationEngine()
    engine.register_source(source, executor=SnowflakeSqlExecutor(
        "INVOICES", database="FIN", schema="BILLING", auth=auth, connect=connect))
    local = [{"jira_key": "PROJ-1", "title": "DB migration"}, {"jira_key": "PROJ-3", "title": "No bill"},
             {"jira_key": None, "title": "Unkeyed"}]
    bag = engine.execute_federated_join(local, "snowflake_billing", "jira_key", "jira_key",
                                        remote_projection=["jira_key", "cost_usd"], semantics=SemanticsMode.BAG)
    assert bag.status == "SUCCESS" and bag.freshness_watermarks == {"snowflake_billing": 1_700_000_000.0}
    assert [r["jira_key"] for r in bag.rows].count("PROJ-1") == 2  # duplicate source rows preserved
    # NULL never joins (remote NULL row and local NULL key both unmatched)
    unkeyed = next(r for r in bag.rows if r["title"] == "Unkeyed")
    assert unkeyed["remote_jira_key"] is None and "remote_cost_usd" not in unkeyed
    assert next(r for r in bag.rows if r["jira_key"] == "PROJ-3")["remote_jira_key"] is None
    st = engine.execute_federated_join(local, "snowflake_billing", "jira_key", "jira_key",
                                       remote_projection=["jira_key", "cost_usd"], semantics=SemanticsMode.SET)
    assert [r["jira_key"] for r in st.rows].count("PROJ-1") == 1 and st.total_rows == 3


def test_snowflake_auth_failure_degrades_to_partial_with_diagnostic():
    class DatabaseAuthError(Exception):
        pass

    def refusing_connect(**_kw):
        raise DatabaseAuthError("250001: Incorrect username or password was specified.")

    auth, source = _sf_source()
    engine = OBDAFederationEngine()
    engine.register_source(source, executor=SnowflakeSqlExecutor("INVOICES", auth=auth, connect=refusing_connect))
    out = engine.execute_federated_join([{"jira_key": "PROJ-1"}], "snowflake_billing", "jira_key", "jira_key")
    assert out.status == "PARTIAL" and out.degraded_sources == ["snowflake_billing"]
    assert out.errors["snowflake_billing"].startswith("SourceAuthError")
    assert out.rows == [{"jira_key": "PROJ-1"}]


def test_missing_executor_is_an_error_not_empty_rows():
    engine = OBDAFederationEngine()
    engine.register_source(FederatedDataSource("orphan", "SNOWFLAKE", "h"))
    with pytest.raises(SourceExecutorMissing):
        engine.execute_federated_join([{"k": 1}], "orphan", "k", "k")


def test_auth_delegation_requires_credentials():
    with pytest.raises(ValueError):
        SourceAuthDelegation("s", "t", "BEARER_TOKEN", {}).get_auth_headers()
    hdr = SourceAuthDelegation("s", "t", "BASIC", {"username": "a@x.io", "password": "tok"}).get_auth_headers()
    assert base64.b64decode(hdr["Authorization"].split()[1]) == b"a@x.io:tok"
    assert SourceAuthDelegation("s", "t", "BEARER_TOKEN", {"token": "oat"}).connector_kwargs() == {
        "authenticator": "oauth", "token": "oat"}


# ----------------------------------------------------------------------------------------------
# Jira Cloud REST contract mock
# ----------------------------------------------------------------------------------------------

ISSUES = [
    {"id": "10001", "key": "PROJ-1", "fields": {"summary": "Database migration", "status": {"name": "In Progress"},
                                                 "assignee": {"displayName": "Ada"}}},
    {"id": "10002", "key": "PROJ-2", "fields": {"summary": "Cache layer upgrade", "status": {"name": "Done"},
                                                 "assignee": None}},
    {"id": "10003", "key": "PROJ-3", "fields": {"summary": "Unbilled spike", "status": {"name": "In Progress"},
                                                 "assignee": {"displayName": "Lin"}}},
]


class JiraContractMock:
    """Validates requests against the documented enhanced-search contract and serves paged responses."""

    def __init__(self, *, user="bot@acme.io", token="jira-api-token", rate_limit_first=False, status=None):
        self.expected_auth = "Basic " + base64.b64encode(f"{user}:{token}".encode()).decode()
        self.rate_limit_first = rate_limit_first
        self.status = status
        self.bodies: list[dict] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        assert request.method == "POST" and request.url.path == "/rest/api/3/search/jql"
        assert request.headers["content-type"] == "application/json"
        if request.headers.get("authorization") != self.expected_auth:
            return httpx.Response(401, json={"errorMessages": ["Client must be authenticated to access this resource."]})
        if self.status:
            return httpx.Response(self.status, json={"errorMessages": ["The value 'NOPE' does not exist for the field 'project'."]})
        if self.rate_limit_first:
            self.rate_limit_first = False
            return httpx.Response(429, headers={"Retry-After": "2"}, json={"errorMessages": ["Rate limit exceeded"]})
        body = json.loads(request.content)
        assert set(body) <= {"jql", "fields", "maxResults", "nextPageToken", "expand", "properties"}
        assert isinstance(body["fields"], list) and 1 <= body["maxResults"] <= 5000
        self.bodies.append(body)
        matching = ISSUES if 'status = "In Progress"' not in body["jql"] else [
            i for i in ISSUES if i["fields"]["status"]["name"] == "In Progress"]
        start = int(body.get("nextPageToken") or 0)
        page = matching[start:start + body["maxResults"]]
        nxt = start + body["maxResults"]
        out = {"issues": [{**i, "fields": {k: v for k, v in i["fields"].items() if k in body["fields"]}}
                          for i in page], "isLast": nxt >= len(matching)}
        if nxt < len(matching):
            out["nextPageToken"] = str(nxt)
        return httpx.Response(200, json=out)


def _jira(mock, **kw):
    auth = SourceAuthDelegation("jira", "tenant_alpha", "BASIC", {"username": "bot@acme.io", "password": "jira-api-token"})
    return JiraRestExecutor("https://acme.atlassian.net", auth, transport=httpx.MockTransport(mock), **kw)


def test_jira_executor_pages_and_maps_fields():
    mock = JiraContractMock()
    ex = _jira(mock, page_size=2, base_jql="project = PROJ")
    rows = ex(FederatedPushdownFragment("f", "jira", {}, ["key", "summary", "status", "assignee"], ""))
    assert [r["key"] for r in rows] == ["PROJ-1", "PROJ-2", "PROJ-3"]
    assert rows[0] == {"key": "PROJ-1", "summary": "Database migration", "status": "In Progress", "assignee": "Ada"}
    assert rows[1]["assignee"] is None
    assert len(mock.bodies) == 2 and mock.bodies[1]["nextPageToken"] == "2"
    assert mock.bodies[0]["jql"] == "(project = PROJ) ORDER BY key ASC"
    assert mock.bodies[0]["fields"] == ["summary", "status", "assignee"]


def test_jira_jql_pushdown_escapes_values_and_rejects_unsafe_fields():
    assert build_jql({"status": "In Progress"}) == 'status = "In Progress" ORDER BY key ASC'
    assert build_jql({"summary": 'x" OR project = SECRET'}) == 'summary = "x\\" OR project = SECRET" ORDER BY key ASC'
    assert build_jql({"assignee": None, "priority": ["High", "Low"]}) == \
        'assignee is EMPTY AND priority in ("High", "Low") ORDER BY key ASC'
    with pytest.raises(ValueError):
        build_jql({"status = Done OR project": "x"})
    mock = JiraContractMock()
    rows = _jira(mock)(FederatedPushdownFragment("f", "jira", {"status": "In Progress"}, ["key"], ""))
    assert [r["key"] for r in rows] == ["PROJ-1", "PROJ-3"]


def test_jira_rate_limit_retry_after_is_honoured():
    slept: list[float] = []
    mock = JiraContractMock(rate_limit_first=True)
    ex = _jira(mock, sleep=slept.append)
    assert len(ex(FederatedPushdownFragment("f", "jira", {}, ["key"], ""))) == 3
    assert slept == [2.0] and ex.requests_made == 2


def test_jira_auth_and_query_errors_fail_closed():
    bad = SourceAuthDelegation("jira", "t", "BASIC", {"username": "bot@acme.io", "password": "wrong"})
    ex = JiraRestExecutor("https://acme.atlassian.net", bad, transport=httpx.MockTransport(JiraContractMock()))
    with pytest.raises(SourceAuthError):
        ex(FederatedPushdownFragment("f", "jira", {}, ["key"], ""))
    engine = OBDAFederationEngine()
    engine.register_source(FederatedDataSource("jira", "REST", "h"), executor=_jira(JiraContractMock(status=400)))
    out = engine.execute_federated_join([{"k": "PROJ-1"}], "jira", "k", "key")
    assert out.status == "PARTIAL" and "HTTP 400" in out.errors["jira"]
    with pytest.raises(ValueError):
        JiraRestExecutor("http://acme.atlassian.net", bad)


def test_federated_jira_x_snowflake_join_end_to_end(snowflake_db):
    """CRA-024.A.2: Jira issues (REST executor) joined with Snowflake billing (SQL executor)."""
    connect, _, _ = snowflake_db
    jira_rows = _jira(JiraContractMock())(
        FederatedPushdownFragment("f", "jira", {"status": "In Progress"}, ["key", "summary"], ""))
    auth, source = _sf_source()
    engine = OBDAFederationEngine()
    engine.register_source(source, executor=SnowflakeSqlExecutor(
        "INVOICES", database="FIN", schema="BILLING", auth=auth, connect=connect))
    out = engine.execute_federated_join(jira_rows, "snowflake_billing", "key", "jira_key",
                                        remote_filters={"region": "eu"},
                                        remote_projection=["jira_key", "cost_usd"])
    assert out.status == "SUCCESS"
    by_key = {r["key"]: r for r in out.rows}
    assert float(by_key["PROJ-1"]["remote_cost_usd"]) == 1250.0  # SET semantics collapsed the duplicate
    assert by_key["PROJ-3"]["remote_jira_key"] is None
    assert out.total_rows == 2
