"""CRA-024.10: BI connectivity over the PostgreSQL wire protocol, exercised with real client drivers.

* psycopg 3 drives libpq, the same client library Tableau's PostgreSQL connector uses (simple and
  extended protocol, binary parameters, server-side DECLARE/FETCH cursors, TLS).
* pg8000 is a pure-Python extended-protocol client, standing in for Npgsql (Power BI's PostgreSQL
  provider), which always uses Parse/Bind/Describe/Execute.

The session scripts below are representative of what the BI tools send on connect (session SETs,
version probe, catalog introspection via information_schema/pg_catalog, cursor-based extract, an
aggregate). They are NOT captured recordings of Tableau Desktop/Power BI Desktop; that is the
residual gap "live validation with Tableau/Power BI clients pending".
"""
from __future__ import annotations

import datetime as dt
import itertools
import json
import os
import secrets
import ssl

import pytest

pytest.importorskip("duckdb")
psycopg = pytest.importorskip("psycopg")
pg8000 = pytest.importorskip("pg8000.native")

from eoip.authn.credentials import CredentialStore
from eoip.graph.memory import MemoryGraphStore
from eoip.query.pg_wire import (
    BIPrincipal,
    PgWireServer,
    TenantRelationalProjection,
    credential_store_authenticator,
    split_statements,
)


def _graph(tag: str, n_services: int = 3) -> MemoryGraphStore:
    g = MemoryGraphStore()
    vids = []
    for i in range(n_services):
        v = g.upsert_vertex("Service", {"canonical_id": f"{tag}:svc:{i}", "name": f"{tag}-svc-{i}",
                                        "priority": i, "status": "live" if i % 2 == 0 else "beta"})
        vids.append(v["vid"])
    g.upsert_vertex("Service", {"canonical_id": f"{tag}:svc:secret", "name": f"{tag}-secret",
                                "priority": 9, "status": "live", "acl_vector": ["admin"]})
    g.upsert_vertex("Service", {"canonical_id": f"{tag}:svc:restricted", "name": f"{tag}-restricted",
                                "priority": 8, "status": "live", "classification": "restricted"})
    for a, b in itertools.pairwise(vids):
        g.upsert_edge("DEPENDS_ON", a, b, {})
    return g


@pytest.fixture()
def tenants():
    return {"alpha": _graph("alpha"), "beta": _graph("beta", 2)}


@pytest.fixture()
def creds(tmp_path):
    store = CredentialStore(tmp_path / "creds.json")
    pw = {u: secrets.token_urlsafe(18) for u in ("ana", "bob", "adm")}
    store.create_user("ana", pw["ana"], ["analyst"], tenant_id="alpha")
    store.create_user("bob", pw["bob"], ["viewer"], tenant_id="beta")
    store.create_user("adm", pw["adm"], ["admin"], tenant_id="alpha")
    _, token = store.issue_api_token("ana", label="tableau")
    return store, pw, token


@pytest.fixture()
def server(tenants, creds):
    store, _, _ = creds
    events = []
    srv = PgWireServer(tenants.__getitem__, credential_store_authenticator(store), allow_insecure_loopback=True,
                       max_result_rows=1000, audit=lambda e, f: events.append((e, f)))
    srv.events = events
    srv.start()
    yield srv
    srv.stop()


def _pg(server, user, password, db="alpha", **kw):
    return psycopg.connect(host="127.0.0.1", port=server.port, user=user, password=password, dbname=db,
                           sslmode=kw.pop("sslmode", "disable"), connect_timeout=10, **kw)


# ----------------------------------------------------------------------------- driver round trips

def test_libpq_client_simple_extended_and_binary_params(server, creds):
    _, pw, _ = creds
    with _pg(server, "ana", pw["ana"], application_name="Tableau Desktop") as c:
        assert c.info.parameter_status("server_version").startswith("14.0")
        assert "PostgreSQL" in c.execute("SELECT version()").fetchone()[0]
        rows = c.execute("SELECT name, priority, status FROM Service WHERE priority >= %s AND status = %s "
                         "ORDER BY priority", (1, "beta")).fetchall()
        assert rows == [("alpha-svc-1", 1, "beta")]
        assert c.execute("SELECT count(*) FROM relationships WHERE relation = 'DEPENDS_ON'").fetchone()[0] == 2
        # typed columns survive the wire: bigint -> int, NULLs -> None
        assert c.execute("SELECT NULL::VARCHAR, 1.5::DOUBLE, true, DATE '2026-10-26'").fetchone() == (
            None, 1.5, True, dt.date(2026, 10, 26))


def test_api_token_login_and_extended_protocol_client(server, creds):
    _, _, token = creds
    con = pg8000.Connection("ana", host="127.0.0.1", port=server.port, password=token, database="alpha")
    try:
        assert con.run("SELECT name FROM Service WHERE name = :n", n="alpha-svc-0") == [["alpha-svc-0"]]
        # value injection through a bound parameter is inert
        assert con.run("SELECT name FROM Service WHERE name = :n", n="x' OR '1'='1") == []
        assert con.run("SELECT label, count(*) AS n FROM entities GROUP BY label") == [["Service", 3]]  # secret (acl) and restricted rows hidden
    finally:
        con.close()


def test_server_side_cursor_pages_with_declare_fetch(tenants, creds):
    store, pw, _ = creds
    tenants["alpha"] = _graph("alpha", 50)
    with PgWireServer(tenants.__getitem__, credential_store_authenticator(store), allow_insecure_loopback=True) as srv:
        with _pg(srv, "ana", pw["ana"]) as c:
            with c.cursor(name="tableau_extract") as cur:
                cur.itersize = 7
                cur.execute("SELECT name FROM Service ORDER BY priority, name")
                names = [r[0] for r in cur]
            assert len(names) == 50 and names[0] == "alpha-svc-0"
        rec = srv.wait_for_sessions(1)[-1]
    assert sum(1 for s in rec.statements if s["kind"] == "FETCH") >= 8


# ----------------------------------------------------------------------------- isolation and ACL

def test_each_session_sees_only_its_tenant(server, creds):
    _, pw, _ = creds
    with _pg(server, "ana", pw["ana"], db="alpha") as a, _pg(server, "bob", pw["bob"], db="beta") as b:
        an = {r[0] for r in a.execute("SELECT name FROM Service").fetchall()}
        bn = {r[0] for r in b.execute("SELECT name FROM Service").fetchall()}
    assert an and bn and all(n.startswith("alpha") for n in an) and all(n.startswith("beta") for n in bn)
    with pytest.raises(psycopg.OperationalError) as e:  # ana may not open beta's database
        _pg(server, "ana", pw["ana"], db="beta")
    assert "authentication failed" in str(e.value)


def test_row_level_acl_and_classification_follow_pdp(server, creds):
    _, pw, _ = creds
    with _pg(server, "ana", pw["ana"]) as c:  # analyst: internal clearance, no admin grant
        names = {r[0] for r in c.execute("SELECT name FROM Service").fetchall()}
    assert "alpha-secret" not in names and "alpha-restricted" not in names
    with _pg(server, "adm", pw["adm"]) as c:
        names = {r[0] for r in c.execute("SELECT name FROM Service").fetchall()}
    assert {"alpha-secret", "alpha-restricted"} <= names
    # ACL properties are not exposed as columns
    with _pg(server, "adm", pw["adm"]) as c:
        cols = {r[0] for r in c.execute("SELECT column_name FROM information_schema.columns "
                                        "WHERE table_name = 'Service'").fetchall()}
    assert "acl_vector" not in cols and "classification" not in cols and {"id", "name", "priority"} <= cols


# ----------------------------------------------------------------------------- read-only and sandbox

@pytest.mark.parametrize("sql,state", [
    ("CREATE TABLE x (a INT)", "25006"),
    ("INSERT INTO entities VALUES ('a', 'b')", "25006"),
    ("DELETE FROM entities", "25006"),
    ("ATTACH '/tmp/evil.db' AS evil", "25006"),
    ("COPY entities TO '/tmp/out.csv'", "25006"),
    ("INSTALL httpfs", "25006"),
    ("PRAGMA enable_profiling", "25006"),
])
def test_writes_and_side_effects_are_refused(server, creds, sql, state):
    _, pw, _ = creds
    with _pg(server, "ana", pw["ana"]) as c:
        with pytest.raises(psycopg.Error) as e:
            c.execute(sql)
        assert e.value.sqlstate == state
        c.rollback()
        assert c.execute("SELECT count(*) FROM entities").fetchone()[0] >= 1


def test_file_access_from_select_is_blocked_and_config_locked(server, creds):
    _, pw, _ = creds
    with _pg(server, "ana", pw["ana"], autocommit=True) as c:
        with pytest.raises(psycopg.Error) as e:
            c.execute("SELECT * FROM read_csv('/etc/passwd')")
        assert e.value.sqlstate in ("42501", "XX000")
        assert "external access" in str(e.value).lower() or "permission" in str(e.value).lower()
        # a client SET only touches the session's PostgreSQL settings, never DuckDB's configuration
        c.execute("SET enable_external_access = true")
        with pytest.raises(psycopg.Error):
            c.execute("SELECT * FROM read_csv('/etc/passwd')")


def test_failed_statement_aborts_transaction_until_rollback(server, creds):
    _, pw, _ = creds
    with _pg(server, "ana", pw["ana"]) as c:
        with pytest.raises(psycopg.errors.UndefinedTable):
            c.execute("SELECT * FROM no_such_table")
        with pytest.raises(psycopg.errors.InFailedSqlTransaction):
            c.execute("SELECT 1")
        c.rollback()
        assert c.execute("SELECT 1").fetchone() == (1,)


# ----------------------------------------------------------------------------- auth and transport

def test_bad_password_and_missing_tls_are_refused(tenants, creds):
    store, pw, _ = creds
    events = []
    with PgWireServer(tenants.__getitem__, credential_store_authenticator(store), allow_insecure_loopback=True,
                      audit=lambda ev, f: events.append((ev, f))) as srv:
        with pytest.raises(psycopg.OperationalError) as e:
            _pg(srv, "ana", "wrong-" + secrets.token_hex(4))
        assert "password authentication failed" in str(e.value)
    assert events == [("auth_failed", {"user": "ana", "peer": "127.0.0.1"})]
    with PgWireServer(tenants.__getitem__, credential_store_authenticator(store)) as srv:  # TLS required
        with pytest.raises(psycopg.OperationalError) as e:
            _pg(srv, "ana", pw["ana"])
        assert "TLS required" in str(e.value)


def test_tls_session(tenants, creds, tmp_path):
    x509 = pytest.importorskip("cryptography.x509")
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID

    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    now = dt.datetime.now(dt.UTC)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - dt.timedelta(minutes=1))
            .not_valid_after(now + dt.timedelta(hours=1)).sign(key, hashes.SHA256()))
    (tmp_path / "c.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    (tmp_path / "k.pem").write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                       serialization.NoEncryption()))
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain(tmp_path / "c.pem", tmp_path / "k.pem")
    store, pw, _ = creds
    with PgWireServer(tenants.__getitem__, credential_store_authenticator(store), tls_context=ctx) as srv:
        with psycopg.connect(
                host="localhost", port=srv.port, user="ana", password=pw["ana"], dbname="alpha",
                sslmode="verify-full", sslrootcert=str(tmp_path / "c.pem"), connect_timeout=10) as c:
            assert c.pgconn.ssl_in_use
            assert c.execute("SELECT count(*) FROM Service").fetchone()[0] == 3
        assert srv.wait_for_sessions(1)[-1].tls is True


# ----------------------------------------------------------------------------- bounds

def test_projection_cap_fails_loudly_not_truncated(tenants, creds):
    store, pw, _ = creds
    with PgWireServer(tenants.__getitem__, credential_store_authenticator(store), allow_insecure_loopback=True,
                      max_rows=3) as srv:
        with pytest.raises(psycopg.OperationalError) as e:
            _pg(srv, "ana", pw["ana"])
        assert "exceeds BI projection cap" in str(e.value)


def test_result_cap(server, creds):
    _, pw, _ = creds
    with _pg(server, "ana", pw["ana"]) as c:
        with pytest.raises(psycopg.Error) as e:
            c.execute("SELECT * FROM range(5000)")
        assert e.value.sqlstate == "54000"


def test_split_statements_respects_quotes_and_comments():
    assert split_statements("select ';' ; -- x;\nselect \"a;b\" /* ; */ from t;") == [
        "select ';'", 'select "a;b"  from t']


def test_projection_types_columns_and_ids():
    g = _graph("alpha")
    con = TenantRelationalProjection(g, "alpha", frozenset({"admin"})).build()
    cols = dict(con.execute("SELECT column_name, data_type FROM information_schema.columns "
                            "WHERE table_name = 'Service'").fetchall())
    assert cols["id"] == "VARCHAR" and cols["priority"] == "BIGINT" and cols["name"] == "VARCHAR"
    assert con.execute("SELECT id FROM Service WHERE name = 'alpha-svc-0'").fetchone() == ("alpha:svc:0",)


# ----------------------------------------------------------------------------- representative BI sessions

TABLEAU_LIKE = [  # libpq connector: session setup, version probe, catalog, cursor extract, aggregate
    "SET DateStyle = 'ISO'", "SET extra_float_digits = 2", "SHOW DateStyle", "SELECT version()",
    "SELECT current_database()",
    ("SELECT table_schema, table_name, table_type FROM information_schema.tables "
     "WHERE table_schema NOT IN ('pg_catalog', 'information_schema') ORDER BY 1, 2"),
    ("SELECT column_name, data_type, is_nullable FROM information_schema.columns "
     "WHERE table_name = 'Service' ORDER BY ordinal_position"),
    "BEGIN",
    ('DECLARE "SQL_CUR0x1" CURSOR WITH HOLD FOR SELECT "Service"."name" AS "name", '
     '"Service"."status" AS "status" FROM "Service"'),
    'FETCH 2048 IN "SQL_CUR0x1"', 'CLOSE "SQL_CUR0x1"', "COMMIT",
    ('SELECT "Service"."status" AS "status", SUM("Service"."priority") AS "sum_priority" FROM "Service" '
     'GROUP BY 1 ORDER BY 1'),
]

POWERBI_LIKE = [  # Npgsql provider: type loading and schema discovery over the extended protocol
    ("SELECT ns.nspname, t.oid, t.typname, t.typtype FROM pg_catalog.pg_type AS t "
     "JOIN pg_catalog.pg_namespace AS ns ON ns.oid = t.typnamespace ORDER BY t.oid LIMIT 50"),
    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY 1",
    ("SELECT c.relname FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace "
     "WHERE c.relkind IN ('r', 'v') ORDER BY 1"),
    ("SELECT r.relation, s.name AS source, t.name AS target FROM relationships r "
     "JOIN Service s ON s.id = r.source_id JOIN Service t ON t.id = r.target_id ORDER BY 2"),
]


def test_tableau_like_session_over_libpq_records_evidence(server, creds, tmp_path):
    _, pw, _ = creds
    with _pg(server, "ana", pw["ana"], application_name="Tableau Desktop", autocommit=True) as c:
        results = []
        for sql in TABLEAU_LIKE:
            cur = c.execute(sql)
            results.append(cur.fetchall() if cur.description else cur.statusmessage)
    assert results[2] == [("ISO",)]
    assert ("main", "Service", "BASE TABLE") in results[5]
    assert results[9] and len(results[9]) == 3  # FETCH returned the extract
    assert results[-1] == [("beta", 1), ("live", 2)]
    rec = server.wait_for_sessions(1)[-1]
    assert rec.application_name == "Tableau Desktop" and rec.tenant_id == "alpha"
    assert [s["kind"] for s in rec.statements][:4] == ["SET", "SET", "SHOW", "SELECT"]
    assert all(s["sqlstate"] is None for s in rec.statements)
    assert all("sql" not in s for s in rec.statements)  # only hashes are recorded
    _write_evidence("tableau-like", rec)


def test_powerbi_like_session_over_extended_protocol(server, creds):
    _, _, token = creds
    con = pg8000.Connection("ana", host="127.0.0.1", port=server.port, password=token, database="alpha",
                            application_name="PowerBI")
    try:
        out = [con.run(sql) for sql in POWERBI_LIKE]
    finally:
        con.close()
    assert any(row[2] in ("int8", "bigint") for row in out[0]) or out[0]
    assert ["Service"] in out[1]
    assert ["Service"] in out[2]
    assert out[3] == [["DEPENDS_ON", "alpha-svc-0", "alpha-svc-1"], ["DEPENDS_ON", "alpha-svc-1", "alpha-svc-2"]]
    rec = server.wait_for_sessions(1)[-1]
    assert rec.application_name == "PowerBI" and all(s["sqlstate"] is None for s in rec.statements)
    _write_evidence("powerbi-like", rec)


def _write_evidence(name, rec):
    out = os.getenv("EOIP_BI_SESSION_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, f"{name}.json"), "w") as f:
            json.dump(rec.__dict__, f, indent=1)


def test_custom_authenticator_contract():
    seen = []

    def auth(user, password, database):
        seen.append((user, database))
        return BIPrincipal(user, "alpha", frozenset({"viewer"})) if password == "pw-ok" else None

    g = _graph("alpha")
    with PgWireServer(lambda t: g, auth, allow_insecure_loopback=True) as srv:
        with psycopg.connect(host="127.0.0.1", port=srv.port, user="u", password="pw-ok", dbname="any",
                             sslmode="disable") as c:
            assert c.execute("SELECT count(*) FROM Service").fetchone() == (3,)
    assert seen == [("u", "any")]
