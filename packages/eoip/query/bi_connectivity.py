"""BI client session driver for the PostgreSQL-wire BI endpoint (CRA-024.10).

This replaces an earlier emulator that returned hard-coded rows without contacting any server.
``BISessionDriver`` now connects to a running :class:`eoip.query.pg_wire.PgWireServer` (or any
PostgreSQL-wire endpoint) with the pure-Python ``pg8000`` driver, runs a representative BI script
(handshake, catalog introspection, column discovery, an aggregate), and records what the server
actually returned. The scripts are representative of Tableau/Power BI connect sequences; they are
not captured recordings of those desktop clients.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

# Representative connect sequences. Tableau (libpq) issues session SETs and a version probe first;
# Power BI (Npgsql) loads types from pg_catalog before discovering tables.
BI_SCRIPTS: dict[str, list[str]] = {
    "tableau": [
        "SELECT 1",
        "SELECT version()",
        "SELECT table_schema, table_name FROM information_schema.tables "
        "WHERE table_schema NOT IN ('pg_catalog', 'information_schema') ORDER BY 1, 2",
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'entities' "
        "ORDER BY ordinal_position",
        "SELECT label, COUNT(*) AS n FROM entities GROUP BY label ORDER BY label",
    ],
    "power bi": [
        "SELECT 1",
        "SELECT t.oid, t.typname FROM pg_catalog.pg_type AS t ORDER BY t.oid LIMIT 20",
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY 1",
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'relationships' "
        "ORDER BY ordinal_position",
        "SELECT relation, COUNT(*) AS n FROM relationships GROUP BY relation ORDER BY relation",
    ],
}


@dataclass
class BISessionQueryRecord:
    step: int
    query_type: str  # "SQL"
    query_text: str
    status_code: int  # 200 when the server answered, 500 when it returned an error
    response_rows_count: int
    duration_ms: float
    error: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class BISessionLog:
    session_id: str
    tool_name: str
    connected: bool
    queries: list[BISessionQueryRecord]
    metadata: dict[str, Any] = field(default_factory=dict)


class BISessionDriver:
    """Drive a representative BI session against a real PostgreSQL-wire endpoint."""

    def __init__(self, host: str, port: int, user: str, password: str, database: str,
                 ssl_context: Any = None, timeout: float = 30.0) -> None:
        self.host, self.port, self.user, self.password = host, port, user, password
        self.database, self.ssl_context, self.timeout = database, ssl_context, timeout

    def run_bi_session(self, tool_name: str = "Tableau", script: list[str] | None = None) -> BISessionLog:
        import pg8000.native  # client driver; installed by the dev/test extras

        queries = list(script or BI_SCRIPTS.get(tool_name.lower(), BI_SCRIPTS["tableau"]))
        session_id = f"bi_session_{tool_name.lower().replace(' ', '_')}_{int(time.time())}"
        con = pg8000.native.Connection(self.user, host=self.host, port=self.port, password=self.password,
                                       database=self.database, ssl_context=self.ssl_context,
                                       timeout=self.timeout, application_name=tool_name)
        records: list[BISessionQueryRecord] = []
        try:
            server_version = con.parameter_statuses.get("server_version")
            for step, sql in enumerate(queries, start=1):
                t0 = time.perf_counter()
                try:
                    rows = con.run(sql)
                    records.append(BISessionQueryRecord(step, "SQL", sql, 200, len(rows or []),
                                                        (time.perf_counter() - t0) * 1000.0))
                except pg8000.native.DatabaseError as exc:
                    info = exc.args[0] if exc.args and isinstance(exc.args[0], dict) else {}
                    records.append(BISessionQueryRecord(step, "SQL", sql, 500, 0,
                                                        (time.perf_counter() - t0) * 1000.0,
                                                        error=str(info.get("C", "")) or type(exc).__name__))
        finally:
            con.close()
        return BISessionLog(session_id, tool_name, True, records,
                            metadata={"auth_mode": "PASSWORD_OR_API_TOKEN", "ssl_enabled": self.ssl_context is not None,
                                      "server_version": server_version, "endpoint": f"{self.host}:{self.port}"})


class BISessionEmulator:
    """Compatibility wrapper kept for the public API; it no longer fabricates results.

    The original class returned hard-coded rows without contacting any server. It now delegates to a
    real endpoint: pass a :class:`BISessionDriver` (or any object with ``run_bi_session``) as
    ``sql_adapter``. Without one it raises instead of inventing a session. ``sparql_handler`` is
    accepted for signature compatibility and ignored: the SPARQL protocol has its own handler and tests.
    """

    def __init__(self, sql_adapter: Optional[Any] = None, sparql_handler: Optional[Any] = None) -> None:  # noqa: UP045
        self.sql_adapter = sql_adapter
        self.sparql_handler = sparql_handler

    def run_bi_session(self, tool_name: str = "Tableau") -> BISessionLog:
        if self.sql_adapter is None or not hasattr(self.sql_adapter, "run_bi_session"):
            raise RuntimeError("no BI endpoint configured: pass a BISessionDriver connected to the "
                               "PostgreSQL-wire BI endpoint (eoip.query.pg_wire.PgWireServer)")
        return self.sql_adapter.run_bi_session(tool_name=tool_name)
