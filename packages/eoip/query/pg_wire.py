"""PostgreSQL wire-protocol (v3) BI endpoint over a per-tenant relational projection (CRA-024.10).

Tableau and Power BI both ship PostgreSQL connectors (libpq / Npgsql). This module serves the
platform's graph to those clients as read-only SQL:

* **Projection** — :class:`TenantRelationalProjection` materialises one tenant's graph into an
  in-memory DuckDB database: one table per vertex label (``id`` = canonical id, typed property
  columns), plus ``entities`` and ``relationships``. Rows whose ACL property excludes every role
  of the principal are not projected. Projection fails loudly (no silent truncation) when the
  graph exceeds ``max_rows``.
* **Isolation** — every session gets its own DuckDB database built only from the authenticated
  principal's tenant; external file/network access is disabled and the configuration locked
  before any client SQL runs.
* **Read-only** — statement types are classified by DuckDB's own parser; only SELECT/EXPLAIN
  plus session statements (SET/SHOW/BEGIN/COMMIT/ROLLBACK/DECLARE/FETCH/CLOSE/DEALLOCATE/DISCARD)
  are accepted; anything else is SQLSTATE 25006.
* **Protocol** — startup, SSLRequest (TLS when a context is configured, otherwise ``N``),
  cleartext password over TLS (or loopback when explicitly allowed), simple query, extended
  query (Parse/Bind/Describe/Execute/Sync/Close/Flush) with text-format parameters and
  results, portals with row limits, DECLARE/FETCH cursors (libpq ``UseDeclareFetch``), and
  ErrorResponse with SQLSTATE codes.
* **Session record** — each session appends a :class:`SessionRecord` (client application,
  statement kinds, row counts, SQLSTATEs) for the acceptance evidence; SQL text and parameter
  values are not recorded (only a SHA-256 of the statement).
"""
from __future__ import annotations

import datetime as _dt
import decimal
import hashlib
import ipaddress
import json
import math
import re
import socket
import ssl
import struct
import threading
import time
import uuid
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any

try:  # optional extra: pip install eoip[bi]
    import duckdb  # type: ignore
except ImportError:  # pragma: no cover - exercised when the extra is absent
    duckdb = None  # type: ignore

SSL_REQUEST = 80877103
GSSENC_REQUEST = 80877104
CANCEL_REQUEST = 80877102
PROTOCOL_V3 = 196608
SERVER_VERSION = "14.0 (EOIP BI endpoint)"

# PostgreSQL type OIDs (text format on the wire)
OID_BOOL, OID_INT8, OID_INT2, OID_INT4, OID_TEXT = 16, 20, 21, 23, 25
OID_FLOAT4, OID_FLOAT8, OID_NUMERIC, OID_VARCHAR = 700, 701, 1700, 1043
OID_DATE, OID_TIMESTAMP, OID_TIMESTAMPTZ = 1082, 1114, 1184

_ACL_PROPERTIES = ("acl_vector", "classification")
_CLEARANCE = {"public": 1, "internal": 2, "confidential": 3, "restricted": 4}
_RESERVED_COLUMNS = {"id", "vid", "label"}
_SESSION_KINDS = {"SET", "SHOW", "BEGIN", "START", "COMMIT", "END", "ROLLBACK", "ABORT", "DECLARE",
                  "FETCH", "MOVE", "CLOSE", "DEALLOCATE", "DISCARD", "RESET"}


class PgWireError(Exception):
    def __init__(self, sqlstate: str, message: str, severity: str = "ERROR"):
        super().__init__(message)
        self.sqlstate, self.message, self.severity = sqlstate, message, severity


class ProjectionTooLarge(PgWireError):
    def __init__(self, what: str, n: int, cap: int):
        super().__init__("54000", f"tenant {what} count {n} exceeds BI projection cap {cap}; raise max_rows or use a view")


# ---------------------------------------------------------------------------- projection

def _ident(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_]", "_", str(name)).strip("_") or "t"
    if s[0].isdigit():
        s = "t_" + s
    return s[:63]


def _insert_many(con, sql: str, rows: list) -> None:
    if rows:
        con.executemany(sql, rows)


def _quote(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _sql_type(values: list[Any]) -> str:
    kinds = {type(v) for v in values if v is not None}
    if not kinds:
        return "VARCHAR"
    if kinds == {bool}:
        return "BOOLEAN"
    if kinds <= {int}:
        return "BIGINT"
    if kinds <= {int, float}:
        return "DOUBLE"
    if kinds == {_dt.datetime}:
        return "TIMESTAMP"
    if kinds == {_dt.date}:
        return "DATE"
    return "VARCHAR"


def _cell(v: Any, typ: str) -> Any:
    if v is None:
        return None
    if typ == "VARCHAR":
        return v if isinstance(v, str) else json.dumps(v, sort_keys=True, default=str)
    if typ == "DOUBLE":
        return float(v)
    return v


def _clearance(roles: frozenset[str]) -> int:
    # same role -> clearance ladder as eoip.authz.pdp.can_read
    if "admin" in roles:
        return 4
    if "steward" in roles or "confidential_clearance" in roles:
        return 3
    if "analyst" in roles or "internal" in roles:
        return 2
    return 1


def _visible(props: dict, grants: frozenset[str], tenant_id: str = "") -> bool:
    """Row-level read check mirroring eoip.authz.pdp.can_read: classification clearance, then
    ``acl_vector`` intersection with the principal's roles/grants (admin and tenant tag pass)."""
    cls = str(props.get("classification") or "").lower()
    if cls and _CLEARANCE.get(cls, 4) > _clearance(grants):
        return False
    acl = props.get("acl_vector")
    if acl:
        acl = [acl] if isinstance(acl, str) else list(acl)
        if "admin" in grants:
            return True
        return bool(grants.intersection(acl)) or f"tenant:{tenant_id}" in acl
    return True


@dataclass
class TenantRelationalProjection:
    """Read-only DuckDB projection of one tenant's graph."""

    store: Any
    tenant_id: str
    roles: frozenset[str] = frozenset()
    max_rows: int = 200_000

    def build(self):
        if duckdb is None:
            raise PgWireError("0A000", "BI endpoint requires the 'bi' extra (duckdb)")
        n_v = int(self.store.count_vertices())
        if n_v > self.max_rows:
            raise ProjectionTooLarge("vertex", n_v, self.max_rows)
        n_e = int(self.store.count_edges())
        if n_e > self.max_rows:
            raise ProjectionTooLarge("edge", n_e, self.max_rows)
        vertices = [v for v in self.store.find_vertices(limit=self.max_rows)
                    if _visible(v.get("properties") or {}, self.roles, self.tenant_id)]
        if len(vertices) > self.max_rows:  # defensive: backends must honour limit
            raise ProjectionTooLarge("vertex", len(vertices), self.max_rows)
        con = duckdb.connect(":memory:")
        by_label: dict[str, list[dict]] = {}
        for v in vertices:
            by_label.setdefault(str(v.get("label") or "Entity"), []).append(v)
        con.execute("CREATE TABLE entities (id VARCHAR PRIMARY KEY, label VARCHAR NOT NULL)")
        _insert_many(con, "INSERT INTO entities VALUES (?, ?)",
                        [(v.get("canonical_id") or v.get("vid"), v.get("label")) for v in vertices])
        used: set[str] = {"entities", "relationships"}
        self.tables: dict[str, str] = {}
        for label, rows in sorted(by_label.items()):
            table = _ident(label)
            while table.lower() in used:
                table += "_"
            used.add(table.lower())
            self.tables[label] = table
            keys = sorted({k for r in rows for k in (r.get("properties") or {})
                           if k not in _ACL_PROPERTIES and k not in ("canonical_id", "tenant_id") and not k.startswith("_")})
            cols: list[tuple[str, str, str]] = []  # (prop, column, type)
            seen = set(_RESERVED_COLUMNS)
            for k in keys:
                c = _ident(k).lower()
                while c in seen:
                    c += "_"
                seen.add(c)
                cols.append((k, c, _sql_type([(r.get("properties") or {}).get(k) for r in rows])))
            ddl = ", ".join(["id VARCHAR PRIMARY KEY"] + [f"{_quote(c)} {t}" for _, c, t in cols])
            con.execute(f"CREATE TABLE {_quote(table)} ({ddl})")
            ph = ", ".join(["?"] * (1 + len(cols)))
            _insert_many(
                con, f"INSERT INTO {_quote(table)} VALUES ({ph})",
                [[r.get("canonical_id") or r.get("vid")]
                 + [_cell((r.get("properties") or {}).get(k), t) for k, _, t in cols] for r in rows])
        visible = {v.get("vid") for v in vertices} | {v.get("canonical_id") for v in vertices}
        edges = [e for e in self.store.find_edges(limit=self.max_rows)
                 if (e.get("out_cid") or e.get("out_v")) in visible and (e.get("in_cid") or e.get("in_v")) in visible
                 and _visible(e.get("properties") or {}, self.roles, self.tenant_id)]
        con.execute("CREATE TABLE relationships (id VARCHAR, relation VARCHAR, source_id VARCHAR, target_id VARCHAR)")
        _insert_many(con, "INSERT INTO relationships VALUES (?, ?, ?, ?)",
                        [(e.get("eid"), e.get("label"), e.get("out_cid") or e.get("out_v"),
                          e.get("in_cid") or e.get("in_v")) for e in edges])
        # Lock the sandbox before any client SQL: no files, no network, no extension installs.
        con.execute("SET enable_external_access = false")
        con.execute("SET autoinstall_known_extensions = false")
        con.execute("SET autoload_known_extensions = false")
        con.execute("SET lock_configuration = true")
        return con


# ---------------------------------------------------------------------------- auth / records

@dataclass(frozen=True)
class BIPrincipal:
    username: str
    tenant_id: str
    roles: frozenset[str]


Authenticator = Callable[[str, str, str], BIPrincipal | None]


def credential_store_authenticator(store: Any, allowed_roles: Iterable[str] = ("viewer", "analyst", "admin")) -> Authenticator:
    """Accept an API token (preferred for BI tools) or the user's password; require a tenant and a BI-capable role."""
    allowed = frozenset(allowed_roles)

    def auth(user: str, password: str, database: str) -> BIPrincipal | None:
        p = store.authenticate_api_token(password)
        if p is not None and p.username != user:
            p = None
        if p is None:
            p = store.verify_password(user, password)
        if p is None or not p.tenant_id or not allowed.intersection(p.roles):
            return None
        if database and database not in (p.tenant_id, "eoip"):
            return None
        return BIPrincipal(p.username, p.tenant_id, frozenset(p.roles))

    return auth


@dataclass
class SessionRecord:
    session_id: str
    application_name: str
    username: str
    tenant_id: str
    tls: bool
    started_at: str
    statements: list[dict] = field(default_factory=list)
    ended_at: str | None = None

    def add(self, kind: str, sql: str, rows: int, sqlstate: str | None = None, ms: float = 0.0) -> None:
        self.statements.append({"kind": kind, "sql_sha256": hashlib.sha256(sql.encode()).hexdigest()[:16],
                                "rows": rows, "sqlstate": sqlstate, "ms": round(ms, 3)})


# ---------------------------------------------------------------------------- SQL helpers

def split_statements(sql: str) -> list[str]:
    out, buf, i, n = [], [], 0, len(sql)
    quote: str | None = None
    while i < n:
        ch = sql[i]
        if quote:
            buf.append(ch)
            if ch == quote:
                if i + 1 < n and sql[i + 1] == quote:
                    buf.append(sql[i + 1]); i += 1
                else:
                    quote = None
        elif ch in ("'", '"'):
            quote = ch; buf.append(ch)
        elif ch == "-" and sql.startswith("--", i):
            j = sql.find("\n", i)
            i = n if j < 0 else j
            continue
        elif ch == "/" and sql.startswith("/*", i):
            j = sql.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        elif ch == ";":
            s = "".join(buf).strip()
            if s:
                out.append(s)
            buf = []
        else:
            buf.append(ch)
        i += 1
    s = "".join(buf).strip()
    if s:
        out.append(s)
    return out


def _first_word(sql: str) -> str:
    m = re.match(r"\s*([A-Za-z]+)", sql)
    return m.group(1).upper() if m else ""


def _oid_for(type_name: str) -> int:
    t = str(type_name).upper()
    if t == "BOOLEAN":
        return OID_BOOL
    if t in ("BIGINT", "HUGEINT", "UBIGINT"):
        return OID_INT8
    if t in ("INTEGER", "UINTEGER", "USMALLINT"):
        return OID_INT4
    if t in ("SMALLINT", "TINYINT", "UTINYINT"):
        return OID_INT2
    if t in ("DOUBLE",):
        return OID_FLOAT8
    if t in ("FLOAT", "REAL"):
        return OID_FLOAT4
    if t.startswith("DECIMAL"):
        return OID_NUMERIC
    if t == "DATE":
        return OID_DATE
    if t.startswith("TIMESTAMP WITH TIME ZONE") or t == "TIMESTAMPTZ":
        return OID_TIMESTAMPTZ
    if t.startswith("TIMESTAMP"):
        return OID_TIMESTAMP
    if t == "VARCHAR":
        return OID_VARCHAR
    return OID_TEXT


def _text(v: Any) -> bytes | None:
    if v is None:
        return None
    if isinstance(v, bool):
        return b"t" if v else b"f"
    if isinstance(v, float):
        if math.isfinite(v):
            return repr(v).encode()
        return str(v).replace("inf", "Infinity").replace("nan", "NaN").encode()
    if isinstance(v, _dt.datetime):
        return v.isoformat(sep=" ").encode()
    if isinstance(v, (_dt.date, decimal.Decimal, int)):
        return str(v).encode()
    if isinstance(v, (list, dict)):
        return json.dumps(v, default=str).encode()
    if isinstance(v, uuid.UUID):
        return str(v).encode()
    return str(v).encode()


def _param(raw: bytes | None, oid: int) -> Any:
    if raw is None:
        return None
    s = raw.decode()
    if oid in (OID_INT2, OID_INT4, OID_INT8):
        return int(s)
    if oid in (OID_FLOAT4, OID_FLOAT8):
        return float(s)
    if oid == OID_NUMERIC:
        return decimal.Decimal(s)
    if oid == OID_BOOL:
        return s.lower() in ("t", "true", "1", "on", "yes")
    return s


_PG_EPOCH = _dt.datetime(2000, 1, 1)


def _param_binary(raw: bytes | None, oid: int) -> Any:
    """Binary-format parameters as sent by psycopg 3 / Npgsql for scalar types."""
    if raw is None:
        return None
    if oid == OID_INT2:
        return struct.unpack("!h", raw)[0]
    if oid == OID_INT4:
        return struct.unpack("!i", raw)[0]
    if oid == OID_INT8:
        return struct.unpack("!q", raw)[0]
    if oid == OID_FLOAT4:
        return struct.unpack("!f", raw)[0]
    if oid == OID_FLOAT8:
        return struct.unpack("!d", raw)[0]
    if oid == OID_BOOL:
        return raw == b"\x01"
    if oid == OID_DATE:
        return (_PG_EPOCH + _dt.timedelta(days=struct.unpack("!i", raw)[0])).date()
    if oid in (OID_TIMESTAMP, OID_TIMESTAMPTZ):
        return _PG_EPOCH + _dt.timedelta(microseconds=struct.unpack("!q", raw)[0])
    if oid in (OID_TEXT, OID_VARCHAR, 0, 1042, 19):
        return raw.decode()
    raise PgWireError("0A000", f"binary parameter format for type oid {oid} is not supported; use text")


def _classify(con, sql: str) -> str:
    """Return 'select' | 'session' | raise PgWireError(25006) using DuckDB's parser."""
    word = _first_word(sql)
    if word in _SESSION_KINDS:
        return "session"
    try:
        stmts = con.extract_statements(sql)
    except Exception as exc:  # noqa: BLE001 - duckdb raises several parser exception types
        raise PgWireError("42601", f"syntax error: {exc}".split("\n")[0][:300]) from None
    if len(stmts) != 1:
        raise PgWireError("42601", "exactly one statement expected")
    st = stmts[0].type
    if st in (duckdb.StatementType.SELECT, duckdb.StatementType.EXPLAIN):
        return "select"
    raise PgWireError("25006", f"read-only BI endpoint: {str(st).split('.')[-1]} statements are not allowed")


def _rewrite(sql: str) -> str:
    """PostgreSQL-isms BI clients send that DuckDB spells differently."""
    s = re.sub(r"(?i)\bversion\(\s*\)", f"'PostgreSQL {SERVER_VERSION}'", sql)
    s = re.sub(r"(?i)\bcurrent_schema\(\s*\)", "'main'", s)
    s = re.sub(r"::regclass\b", "::VARCHAR", s, flags=re.IGNORECASE)
    return s


# ---------------------------------------------------------------------------- session

class _Conn:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buf = bytearray()

    def recv_exact(self, n: int) -> bytes:
        while len(self.buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("client closed")
            self.buf += chunk
        out = bytes(self.buf[:n])
        del self.buf[:n]
        return out

    def send(self, data: bytes) -> None:
        self.sock.sendall(data)


def _msg(tag: bytes, payload: bytes = b"") -> bytes:
    return tag + struct.pack("!I", len(payload) + 4) + payload


def _cstr(s: str) -> bytes:
    return s.encode() + b"\x00"


def _read_cstr(b: bytes, i: int) -> tuple[str, int]:
    j = b.index(b"\x00", i)
    return b[i:j].decode(), j + 1


@dataclass
class _Prepared:
    sql: str
    param_oids: list[int]
    kind: str


@dataclass
class _Portal:
    prepared: _Prepared
    params: list[Any]
    rows: list[tuple] | None = None
    desc: list[tuple[str, str]] | None = None
    pos: int = 0
    tag: str = ""
    done: bool = False


class PgWireSession:
    def __init__(self, server: PgWireServer, sock: socket.socket, peer: tuple):
        self.server, self.peer = server, peer
        self.io = _Conn(sock)
        self.tls = False
        self.con = None
        self.principal: BIPrincipal | None = None
        self.params: dict[str, str] = {}
        self.settings: dict[str, str] = {"DateStyle": "ISO, MDY", "client_encoding": "UTF8", "TimeZone": "UTC",
                                         "standard_conforming_strings": "on", "extra_float_digits": "1",
                                         "search_path": "main", "transaction_isolation": "read committed"}
        self.in_tx = False
        self.failed_tx = False
        self.prepared: dict[str, _Prepared] = {}
        self.portals: dict[str, _Portal] = {}
        self.cursors: dict[str, _Portal] = {}
        self.record: SessionRecord | None = None

    # -- handshake
    def _startup(self) -> bool:
        while True:
            (length,) = struct.unpack("!I", self.io.recv_exact(4))
            if length < 8 or length > 10_000:
                return False
            body = self.io.recv_exact(length - 4)
            (code,) = struct.unpack("!I", body[:4])
            if code == SSL_REQUEST:
                if self.server.tls_context is not None and not self.tls:
                    self.io.send(b"S")
                    self.io.sock = self.server.tls_context.wrap_socket(self.io.sock, server_side=True)
                    self.tls = True
                else:
                    self.io.send(b"N")
                continue
            if code == GSSENC_REQUEST:
                self.io.send(b"N")
                continue
            if code == CANCEL_REQUEST:
                return False
            if code != PROTOCOL_V3:
                self._error(PgWireError("0A000", "unsupported frontend protocol"), fatal=True)
                return False
            parts = body[4:].split(b"\x00")
            kv = [p.decode() for p in parts if p]
            self.params = dict(zip(kv[0::2], kv[1::2]))
            return True

    def _authenticate(self) -> bool:
        loopback = ipaddress.ip_address(self.peer[0]).is_loopback if self.peer else False
        if not self.tls and not (self.server.allow_insecure_loopback and loopback):
            self._error(PgWireError("28000", "TLS required (cleartext credentials refused on a non-TLS connection)"), fatal=True)
            return False
        self.io.send(_msg(b"R", struct.pack("!I", 3)))  # AuthenticationCleartextPassword
        tag = self.io.recv_exact(1)
        (length,) = struct.unpack("!I", self.io.recv_exact(4))
        body = self.io.recv_exact(length - 4)
        if tag != b"p":
            self._error(PgWireError("08P01", "expected password message"), fatal=True)
            return False
        password = body.rstrip(b"\x00").decode()
        user, database = self.params.get("user", ""), self.params.get("database", "")
        principal = None
        try:
            principal = self.server.authenticator(user, password, database)
        except Exception as exc:  # noqa: BLE001 - any authenticator fault is a refused login, never a crash
            self.server._audit("authenticator_error", user=user, error=type(exc).__name__)
            principal = None
        if principal is None:
            self.server._audit("auth_failed", user=user, peer=self.peer[0] if self.peer else None)
            self._error(PgWireError("28P01", f'password authentication failed for user "{user}"'), fatal=True)
            return False
        self.principal = principal
        try:
            store = self.server.store_for_tenant(principal.tenant_id)
            self.con = TenantRelationalProjection(store, principal.tenant_id, principal.roles, self.server.max_rows).build()
        except PgWireError as exc:
            self._error(exc, fatal=True)
            return False
        except Exception as exc:  # noqa: BLE001 - never leave the client hanging on a projection failure
            self._error(PgWireError("XX000", f"tenant projection failed: {type(exc).__name__}"), fatal=True)
            return False
        self.record = SessionRecord(uuid.uuid4().hex, self.params.get("application_name", ""), principal.username,
                                    principal.tenant_id, self.tls, _dt.datetime.now(_dt.UTC).isoformat())
        self.server._audit("session_start", user=principal.username, tenant=principal.tenant_id, tls=self.tls)
        self.io.send(_msg(b"R", struct.pack("!I", 0)))
        status = {"server_version": SERVER_VERSION, "server_encoding": "UTF8", "client_encoding": "UTF8",
                  "DateStyle": "ISO, MDY", "integer_datetimes": "on", "standard_conforming_strings": "on",
                  "TimeZone": "UTC", "IntervalStyle": "postgres", "is_superuser": "off",
                  "session_authorization": principal.username,
                  "application_name": self.params.get("application_name", "")}
        for k, v in status.items():
            self.io.send(_msg(b"S", _cstr(k) + _cstr(v)))
        self.io.send(_msg(b"K", struct.pack("!II", 0, 0)))
        self._ready()
        return True

    # -- framing
    def _ready(self) -> None:
        st = b"E" if self.failed_tx else (b"T" if self.in_tx else b"I")
        self.io.send(_msg(b"Z", st))

    def _error(self, exc: PgWireError, fatal: bool = False) -> None:
        sev = "FATAL" if fatal else exc.severity
        payload = b"S" + _cstr(sev) + b"V" + _cstr(sev) + b"C" + _cstr(exc.sqlstate) + b"M" + _cstr(exc.message) + b"\x00"
        try:
            self.io.send(_msg(b"E", payload))
        except OSError:
            pass

    def _row_description(self, desc: list[tuple[str, str]]) -> bytes:
        body = struct.pack("!H", len(desc))
        for name, typ in desc:
            oid = _oid_for(typ)
            size = {OID_BOOL: 1, OID_INT2: 2, OID_INT4: 4, OID_INT8: 8, OID_FLOAT4: 4, OID_FLOAT8: 8, OID_DATE: 4,
                    OID_TIMESTAMP: 8, OID_TIMESTAMPTZ: 8}.get(oid, -1)
            body += _cstr(name) + struct.pack("!IhIhih", 0, 0, oid, size, -1, 0)
        return _msg(b"T", body)

    def _data_row(self, row: tuple) -> bytes:
        body = struct.pack("!H", len(row))
        for v in row:
            t = _text(v)
            body += struct.pack("!i", -1) if t is None else struct.pack("!i", len(t)) + t
        return _msg(b"D", body)

    # -- execution
    def _execute_sql(self, sql: str, params: list[Any]) -> tuple[list[tuple[str, str]] | None, list[tuple], str]:
        """Run one statement. Returns (description|None, rows, command tag)."""
        word = _first_word(sql)
        if self.failed_tx and word not in ("ROLLBACK", "ABORT", "COMMIT", "END"):
            raise PgWireError("25P02", "current transaction is aborted, commands ignored until end of transaction block")
        if word in ("BEGIN", "START"):
            self.in_tx = True
            return None, [], "BEGIN"
        if word in ("COMMIT", "END", "ROLLBACK", "ABORT"):
            tag = "ROLLBACK" if (word in ("ROLLBACK", "ABORT") or self.failed_tx) else "COMMIT"
            self.in_tx = self.failed_tx = False
            self.cursors.clear()
            return None, [], tag
        if word in ("SET", "RESET"):
            m = re.match(r"(?is)\s*SET\s+(?:SESSION\s+|LOCAL\s+)?([A-Za-z_][\w.]*)\s*(?:=|\bTO\b)\s*(.+?)\s*$", sql)
            if m:
                self.settings[m.group(1)] = m.group(2).strip().strip("'")
            return None, [], word
        if word == "SHOW":
            m = re.match(r"(?is)\s*SHOW\s+([A-Za-z_][\w.]*)", sql)
            name = m.group(1) if m else ""
            key = next((k for k in self.settings if k.lower() == name.lower()), None)
            if name.lower() == "server_version":
                val = SERVER_VERSION
            elif key is None:
                raise PgWireError("42704", f'unrecognized configuration parameter "{name}"')
            else:
                val = self.settings[key]
            return [(name, "VARCHAR")], [(val,)], "SHOW"
        if word == "DECLARE":
            m = re.match(r'(?is)\s*DECLARE\s+("?[\w]+"?)\s+(?:BINARY\s+)?(?:(?:NO\s+)?SCROLL\s+)?CURSOR\s+(?:(?:WITH|WITHOUT)\s+HOLD\s+)?FOR\s+(.+)$', sql)
            if not m:
                raise PgWireError("42601", "unsupported DECLARE form")
            if not self.in_tx and "WITH HOLD" not in sql.upper():
                raise PgWireError("25P01", "DECLARE CURSOR can only be used in transaction blocks")
            inner = m.group(2)
            if _classify(self.con, inner) != "select":
                raise PgWireError("25006", "cursor query must be a SELECT")
            desc, rows, _ = self._run_select(inner, params)
            self.cursors[m.group(1).strip('"')] = _Portal(_Prepared(inner, [], "select"), params, rows, desc)
            return None, [], "DECLARE CURSOR"
        if word in ("FETCH", "MOVE"):
            m = re.match(r'(?is)\s*(?:FETCH|MOVE)\s+(?:FORWARD\s+)?(ALL|\d+)?\s*(?:FROM|IN)?\s*("?[\w]+"?)\s*$', sql)
            if not m or m.group(2).strip('"') not in self.cursors:
                raise PgWireError("34000", "cursor does not exist")
            cur = self.cursors[m.group(2).strip('"')]
            n = len(cur.rows) if (m.group(1) or "1").upper() == "ALL" else int(m.group(1) or 1)
            chunk = cur.rows[cur.pos:cur.pos + n]
            cur.pos += len(chunk)
            if word == "MOVE":
                return None, [], f"MOVE {len(chunk)}"
            return cur.desc, chunk, f"FETCH {len(chunk)}"
        if word == "CLOSE":
            m = re.match(r'(?is)\s*CLOSE\s+("?[\w]+"?|ALL)\s*$', sql)
            name = (m.group(1) if m else "").strip('"')
            if name.upper() == "ALL":
                self.cursors.clear()
            elif self.cursors.pop(name, None) is None:
                raise PgWireError("34000", f'cursor "{name}" does not exist')
            return None, [], "CLOSE CURSOR"
        if word in ("DEALLOCATE", "DISCARD"):
            if word == "DISCARD":
                self.prepared.clear(); self.cursors.clear()
            return None, [], word + (" ALL" if word == "DISCARD" else "")
        if word in _SESSION_KINDS:
            raise PgWireError("0A000", f"{word} is not supported")
        _classify(self.con, sql)
        return self._run_select(sql, params)

    def _run_select(self, sql: str, params: list[Any]):
        q = _rewrite(sql)
        try:
            cur = self.con.cursor()
            cur.execute(q, params) if params else cur.execute(q)
            desc = [(d[0], str(d[1])) for d in (cur.description or [])]
            rows = cur.fetchmany(self.server.max_result_rows + 1)
        except PgWireError:
            raise
        except Exception as exc:  # noqa: BLE001 - mapped to a SQLSTATE and returned to the client
            name = type(exc).__name__
            state = {"CatalogException": "42P01", "BinderException": "42703", "ParserException": "42601",
                     "PermissionException": "42501", "InvalidInputException": "22P02",
                     "ConversionException": "22P02"}.get(name, "XX000")
            raise PgWireError(state, str(exc).split("\n")[0][:500]) from None
        if len(rows) > self.server.max_result_rows:
            raise PgWireError("54000", f"result exceeds {self.server.max_result_rows} rows; add a LIMIT or aggregate")
        return desc, rows, f"SELECT {len(rows)}"

    def _simple_query(self, sql: str) -> None:
        stmts = split_statements(sql)
        if not stmts:
            self.io.send(_msg(b"I"))
            self._ready()
            return
        for s in stmts:
            t0 = time.perf_counter()
            try:
                desc, rows, tag = self._execute_sql(s, [])
            except PgWireError as exc:
                if self.in_tx:
                    self.failed_tx = True
                self.record.add(_first_word(s), s, 0, exc.sqlstate, (time.perf_counter() - t0) * 1000)
                self._error(exc)
                break
            if desc is not None:
                self.io.send(self._row_description(desc))
                for r in rows:
                    self.io.send(self._data_row(r))
            self.io.send(_msg(b"C", _cstr(tag)))
            self.record.add(_first_word(s), s, len(rows), None, (time.perf_counter() - t0) * 1000)
        self._ready()

    # -- extended protocol
    def _extended(self, tag: bytes, body: bytes) -> None:
        if tag == b"P":
            name, i = _read_cstr(body, 0)
            sql, i = _read_cstr(body, i)
            (n,) = struct.unpack("!H", body[i:i + 2]); i += 2
            oids = list(struct.unpack(f"!{n}I", body[i:i + 4 * n])) if n else []
            stmts = split_statements(sql)
            if len(stmts) > 1:
                raise PgWireError("42601", "cannot insert multiple commands into a prepared statement")
            sql1 = stmts[0] if stmts else ""
            kind = "empty" if not sql1 else ("session" if _first_word(sql1) in _SESSION_KINDS else _classify(self.con, sql1))
            nparams = max([int(x) for x in re.findall(r"\$(\d+)", sql1)] or [0])
            oids += [0] * max(0, nparams - len(oids))
            self.prepared[name] = _Prepared(sql1, oids, kind)
            self.io.send(_msg(b"1"))
        elif tag == b"B":
            portal, i = _read_cstr(body, 0)
            stmt, i = _read_cstr(body, i)
            if stmt not in self.prepared:
                raise PgWireError("26000", f'prepared statement "{stmt}" does not exist')
            (nf,) = struct.unpack("!H", body[i:i + 2]); i += 2
            fmts = list(struct.unpack(f"!{nf}H", body[i:i + 2 * nf])); i += 2 * nf
            (np_,) = struct.unpack("!H", body[i:i + 2]); i += 2
            prep = self.prepared[stmt]
            raw: list[bytes | None] = []
            for _ in range(np_):
                (ln,) = struct.unpack("!i", body[i:i + 4]); i += 4
                raw.append(None if ln < 0 else body[i:i + ln]); i += max(ln, 0)
            (nr,) = struct.unpack("!H", body[i:i + 2]); i += 2
            rfmts = list(struct.unpack(f"!{nr}H", body[i:i + 2 * nr]))
            if any(f == 1 for f in rfmts):
                raise PgWireError("0A000", "binary result format is not supported; use text")
            oids = prep.param_oids + [0] * (len(raw) - len(prep.param_oids))
            if len(fmts) == 1:
                fmts = fmts * len(raw)
            fmts += [0] * (len(raw) - len(fmts))
            self.portals[portal] = _Portal(prep, [_param_binary(r, o) if f == 1 else _param(r, o)
                                                  for r, o, f in zip(raw, oids, fmts)])
            self.io.send(_msg(b"2"))
        elif tag == b"D":
            kind, name = chr(body[0]), body[1:].rstrip(b"\x00").decode()
            if kind == "S":
                prep = self.prepared.get(name)
                if prep is None:
                    raise PgWireError("26000", f'prepared statement "{name}" does not exist')
                self.io.send(_msg(b"t", struct.pack("!H", len(prep.param_oids))
                                  + b"".join(struct.pack("!I", o or OID_TEXT) for o in prep.param_oids)))
                desc = self._describe_sql(prep)
            else:
                p = self.portals.get(name)
                if p is None and name in self.cursors:  # SQL-level cursor described as a portal
                    desc = self.cursors[name].desc
                elif p is None:
                    raise PgWireError("34000", f'portal "{name}" does not exist')
                else:
                    self._materialise(p)
                    desc = p.desc
            self.io.send(self._row_description(desc) if desc else _msg(b"n"))
        elif tag == b"E":
            name, i = _read_cstr(body, 0)
            (maxrows,) = struct.unpack("!I", body[i:i + 4])
            p = self.portals.get(name)
            if p is None:
                raise PgWireError("34000", f'portal "{name}" does not exist')
            if p.prepared.kind == "empty":
                self.io.send(_msg(b"I"))
                return
            t0 = time.perf_counter()
            self._materialise(p)
            rows = p.rows[p.pos:] if not maxrows else p.rows[p.pos:p.pos + maxrows]
            for r in rows:
                self.io.send(self._data_row(r))
            p.pos += len(rows)
            if maxrows and p.pos < len(p.rows):
                self.io.send(_msg(b"s"))  # PortalSuspended
            else:
                tag_out = p.tag if p.desc is None or not p.tag.startswith("SELECT") else f"SELECT {p.pos}"
                self.io.send(_msg(b"C", _cstr(tag_out)))
                self.record.add(_first_word(p.prepared.sql), p.prepared.sql, p.pos, None, (time.perf_counter() - t0) * 1000)
        elif tag == b"C":
            kind, name = chr(body[0]), body[1:].rstrip(b"\x00").decode()
            (self.prepared if kind == "S" else self.portals).pop(name, None)
            self.io.send(_msg(b"3"))
        elif tag == b"H":
            pass
        else:
            raise PgWireError("08P01", f"unsupported message type {tag!r}")

    def _describe_sql(self, prep: _Prepared):
        if prep.kind != "select":
            return [("?column?", "VARCHAR")] if _first_word(prep.sql) == "SHOW" else None
        try:
            cur = self.con.cursor()
            q = _rewrite(prep.sql)
            nparams = len(prep.param_oids)
            if nparams:
                cur.execute(f"SELECT * FROM ({q}) AS _d LIMIT 0", [None] * nparams)
            else:
                cur.execute(f"SELECT * FROM ({q}) AS _d LIMIT 0")
            return [(d[0], str(d[1])) for d in cur.description or []]
        except Exception:  # noqa: BLE001 - describe is best-effort; Execute reports the real error
            return None

    def _materialise(self, p: _Portal) -> None:
        if p.done:
            return
        try:
            desc, rows, tag = self._execute_sql(p.prepared.sql, p.params)
        except PgWireError:
            p.done = True
            raise
        p.desc, p.rows, p.tag, p.done = desc, rows, tag, True

    # -- loop
    def run(self) -> None:
        try:
            if not self._startup() or not self._authenticate():
                return
            skipping = False  # after an extended-protocol error, discard until Sync
            while True:
                tag = self.io.recv_exact(1)
                (length,) = struct.unpack("!I", self.io.recv_exact(4))
                if length > self.server.max_message_bytes:
                    self._error(PgWireError("54000", "message too large"), fatal=True)
                    return
                body = self.io.recv_exact(length - 4)
                if tag == b"X":
                    return
                if tag == b"Q":
                    skipping = False
                    self._simple_query(body.rstrip(b"\x00").decode())
                elif tag == b"S":
                    skipping = False
                    self.portals.pop("", None)
                    self._ready()
                elif skipping:
                    continue
                else:
                    try:
                        self._extended(tag, body)
                    except PgWireError as exc:
                        if self.in_tx:
                            self.failed_tx = True
                        if self.record:
                            self.record.add("EXT", tag.decode(errors="replace"), 0, exc.sqlstate)
                        self._error(exc)
                        skipping = True
        except (ConnectionError, OSError, ssl.SSLError, struct.error):
            return
        finally:
            if self.record is not None:
                self.record.ended_at = _dt.datetime.now(_dt.UTC).isoformat()
                self.server._finish(self.record)
            if self.con is not None:
                self.con.close()
            try:
                self.io.sock.close()
            except OSError:
                pass


class PgWireServer:
    """Threaded PostgreSQL-protocol endpoint. ``start()`` binds and returns the port."""

    def __init__(self, store_for_tenant: Callable[[str], Any], authenticator: Authenticator, *,
                 host: str = "127.0.0.1", port: int = 0, tls_context: ssl.SSLContext | None = None,
                 allow_insecure_loopback: bool = False, max_rows: int = 200_000, max_result_rows: int = 1_000_000,
                 max_message_bytes: int = 4 * 1024 * 1024, max_sessions: int = 64,
                 audit: Callable[[str, dict], None] | None = None) -> None:
        if duckdb is None:
            raise RuntimeError("BI endpoint requires the 'bi' extra (duckdb)")
        self.store_for_tenant, self.authenticator = store_for_tenant, authenticator
        self.host, self.port, self.tls_context = host, port, tls_context
        self.allow_insecure_loopback = allow_insecure_loopback
        self.max_rows, self.max_result_rows, self.max_message_bytes = max_rows, max_result_rows, max_message_bytes
        self.sessions: list[SessionRecord] = []
        self._audit_cb = audit
        self._sem = threading.BoundedSemaphore(max_sessions)
        self._sock: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._lock = threading.Lock()

    def _audit(self, event: str, **fields: Any) -> None:
        if self._audit_cb:
            self._audit_cb(event, fields)

    def _finish(self, rec: SessionRecord) -> None:
        with self._lock:
            self.sessions.append(rec)
        self._audit("session_end", session=rec.session_id, statements=len(rec.statements))

    def wait_for_sessions(self, n: int, timeout: float = 5.0) -> list[SessionRecord]:
        """Block until at least ``n`` sessions have ended (records are appended on disconnect)."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            with self._lock:
                if len(self.sessions) >= n:
                    return list(self.sessions)
            time.sleep(0.01)
        raise TimeoutError(f"{len(self.sessions)} of {n} BI sessions ended within {timeout}s")

    def start(self) -> int:
        s = socket.socket(socket.AF_INET6 if ":" in self.host else socket.AF_INET, socket.SOCK_STREAM)
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):  # Windows: SO_REUSEADDR would allow port hijacking
            s.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        else:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(32)
        s.settimeout(0.2)
        self._sock, self.port = s, s.getsockname()[1]
        self._thread = threading.Thread(target=self._serve, name="eoip-pgwire", daemon=True)
        self._thread.start()
        return self.port

    def _serve(self) -> None:
        while not self._stop.is_set():
            try:
                c, addr = self._sock.accept()
            except (TimeoutError, OSError):
                continue
            if not self._sem.acquire(blocking=False):
                c.sendall(_msg(b"E", b"SFATAL\x00C53300\x00Mtoo many BI sessions\x00\x00"))
                c.close()
                continue
            c.settimeout(None)

            def run(c=c, addr=addr):
                try:
                    PgWireSession(self, c, addr).run()
                finally:
                    self._sem.release()

            threading.Thread(target=run, daemon=True).start()

    def stop(self) -> None:
        self._stop.set()
        if self._sock:
            self._sock.close()
        if self._thread:
            self._thread.join(timeout=2)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *a):
        self.stop()
