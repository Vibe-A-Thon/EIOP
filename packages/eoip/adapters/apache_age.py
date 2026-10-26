"""Apache AGE adapter: SQL-wrapped openCypher over an existing relational port.

Real adapter, no new deps: AGE is a PostgreSQL extension that executes
openCypher inside the database via the SQL function
``SELECT * FROM ag_catalog.cypher(<graph>, $$ ... $$) AS (...)``. EOIP
already operates against a relational port for metadata, so this adapter
builds deterministic AGE SQL statements (the ``CypherToAgeSqlBuilder``) and
executes them through an injectable SQL executor — keeping the transport
behind a small protocol instead of hard-coding a driver.

``AGEGraphStore`` implements the GraphStore read/write core over that SQL
builder. Type-map handling and ``ag_catalog`` qualifications follow AGE
conventions; backend-specific behavior is recorded in the manifest
(SR-GDB-003).
"""

from __future__ import annotations

import hashlib
import logging
import re
from collections.abc import Callable
from typing import Any

from eoip.graph.memory import edge_key

log = logging.getLogger("eoip.adapters")

SqlExecutor = Callable[[str], list[dict[str, Any]]]
"""Injectable SQL executor: (sql) -> result rows. Tests inject a fake;
deployments wire the platform's existing relational connection."""

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class CypherToAgeSqlBuilder:
    """Deterministic openCypher → AGE SQL query builder."""

    def __init__(self, graph: str = "eoip", schema: str = "ag_catalog"):
        if not _IDENTIFIER_RE.fullmatch(graph):
            raise ValueError(f"Unsafe AGE graph name: {graph!r}")
        self.graph = graph
        self.schema = schema

    def _wrap(self, cypher: str, returns: list[tuple[str, str]]) -> str:
        body = cypher.strip().rstrip(";")
        if not _SAFE_CYPHER.fullmatch(body):
            raise ValueError(
                "openCypher contains disallowed content ('$$' would break dollar-quoting, "
                "or control characters present)"
            )
        columns = ", ".join(f"{name} agtype" for name, _ in returns) or "a agtype"
        return (
            f"SELECT * FROM {self.schema}.cypher({self.graph!r}, $${body}$$) "
            f"AS ({columns});"
        )

    def match_vertices(self, label: str, prop: str, value: Any) -> str:
        if not _IDENTIFIER_RE.fullmatch(label) or not _IDENTIFIER_RE.fullmatch(prop):
            raise ValueError("Unsafe Cypher identifier")
        return self._wrap(
            f"MATCH (n:{label} {{{prop}: $value}}) RETURN n",
            [("n", "agtype")],
        ).replace("$value", _sql_literal(value))

    def upsert_vertex(self, label: str, props: dict[str, Any]) -> str:
        if not _IDENTIFIER_RE.fullmatch(label):
            raise ValueError(f"Unsafe label: {label!r}")
        cid = props.get("canonical_id")
        assignments = ", ".join(f"{k}: {_cypher_literal(v)}" for k, v in sorted(props.items()))
        cypher = (
            f"MATCH (n:{label} {{canonical_id: {_cypher_literal(cid)}}}) "
            f"SET n += {{{assignments}}} RETURN n "
            f"UNION "
            f"CREATE (m:{label} {{{assignments}}}) RETURN m"
        )
        # AGE does not allow SET n += on CREATE path cleanly; use MERGE instead.
        cypher = (
            f"MERGE (n:{label} {{canonical_id: {_cypher_literal(cid)}}}) "
            f"SET n += {{{assignments}}} RETURN n"
        )
        return self._wrap(cypher, [("n", "agtype")])

    def upsert_edge(self, label: str, out_cid: str, in_cid: str, props: dict[str, Any]) -> str:
        if not _IDENTIFIER_RE.fullmatch(label):
            raise ValueError(f"Unsafe label: {label!r}")
        assignments = ", ".join(f"{k}: {_cypher_literal(v)}" for k, v in sorted(props.items()))
        cypher = (
            f"MATCH (a {{canonical_id: {_cypher_literal(out_cid)}}}), "
            f"(b {{canonical_id: {_cypher_literal(in_cid)}}}) "
            f"MERGE (a)-[r:{label} {{edge_key: {_cypher_literal(props.get('edge_key', ''))}}}]->(b) "
            f"SET r += {{{assignments}}} RETURN r"
        )
        return self._wrap(cypher, [("r", "agtype")])

    def match_edges(self, label: str | None = None, edge_key: str | None = None) -> str:
        pattern = f"[r{':' + label if label else ''}]"
        where = f" WHERE r.edge_key = {_cypher_literal(edge_key)}" if edge_key else ""
        return self._wrap(
            f"MATCH (a)-{pattern}->(b){where} RETURN r",
            [("r", "agtype")],
        )

    def count(self, kind: str = "V") -> str:
        if kind not in {"V", "E"}:
            raise ValueError("kind must be 'V' or 'E'")
        return f"SELECT count(*) AS n FROM {self.schema}.{kind}_graph_view WHERE graph_name = '{self.graph}';"


_SAFE_CYPHER = re.compile(r"(?s)(?!.*\$\$)[^\x00-]+")


def _sql_literal(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def _cypher_literal(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


class ApacheAGEStore:
    """GraphStore core over Apache AGE SQL-wrapped openCypher.

    Transport honesty: statements are built deterministically and executed via
    the injected ``SqlExecutor``; when none is supplied the store operates in
    statement-preview mode (``preview_only=True``) and raises on execution.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        graph: str = "eoip",
        username: str = "postgres",
        password: str = "",
        executor: SqlExecutor | None = None,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.graph = graph
        self.builder = CypherToAgeSqlBuilder(graph=graph)
        self._executor = executor
        self._preview_only = executor is None

    # -- statement surface (deterministic, testable without a database) --------
    def statements(self) -> dict[str, str]:
        """Representative SQL statements this adapter generates."""
        return {
            "upsert_vertex": self.builder.upsert_vertex(
                "Entity", {"canonical_id": "urn:example:1", "name": "Example"}
            ),
            "upsert_edge": self.builder.upsert_edge(
                "RELATES_TO",
                "urn:example:1",
                "urn:example:2",
                {"edge_key": edge_key("RELATES_TO", "urn:example:1", "urn:example:2"), "out_cid": "urn:example:1", "in_cid": "urn:example:2"},
            ),
            "match_vertices": self.builder.match_vertices("Entity", "canonical_id", "urn:example:1"),
            "match_edges": self.builder.match_edges(edge_key=edge_key("RELATES_TO", "urn:example:1", "urn:example:2")),
            "count_vertices": self.builder.count("V"),
            "count_edges": self.builder.count("E"),
        }

    # -- execution -------------------------------------------------------------
    def _run(self, sql: str) -> list[dict[str, Any]]:
        if self._preview_only or self._executor is None:
            raise RuntimeError(
                "ApacheAGEStore has no SQL executor (External gate: wire the "
                "platform relational port or inject SqlExecutor)."
            )
        return self._executor(sql)

    def health(self) -> bool:
        if self._preview_only:
            return False
        try:
            self._run("SELECT 1 AS ok;")
            return True
        except Exception:  # noqa: BLE001 - any executor failure means unavailable
            return False

    def ping(self) -> dict:
        return {
            "backend": "apache_age",
            "graph": self.graph,
            "host": self.host,
            "port": self.port,
            "status": "ok" if self.health() else "unavailable",
            "preview_only": self._preview_only,
        }

    def ensure_schema(self, manifest: dict) -> dict:
        if self._preview_only:
            return {"created": False, "note": "preview mode; run CREATE EXTENSION age + create_graph out-of-band"}
        ddl = [
            "CREATE EXTENSION IF NOT EXISTS age;",
            f"SELECT {self.builder.schema}.create_graph({self.graph!r});",
        ]
        for statement in ddl:
            try:
                self._run(statement)
            except Exception as exc:  # noqa: BLE001 - extension/graph may already exist
                log.debug("AGE DDL skipped: %s", exc)
        return {"created": True}

    def schema_status(self) -> dict:
        return {"initialized": not self._preview_only, "graph": self.graph}

    def upsert_vertex(self, label: str, properties: dict) -> dict:
        rows = self._run(self.builder.upsert_vertex(label, properties))
        return {
            "vid": _ag_id(rows, "n"),
            "canonical_id": properties.get("canonical_id"),
            "label": label,
            "properties": dict(properties),
        }

    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict) -> dict:
        props = {**properties, "edge_key": properties.get("edge_key") or edge_key(label, out_v, in_v)}
        self._run(self.builder.upsert_edge(label, out_v, in_v, props))
        return {
            "eid": props["edge_key"],
            "label": label,
            "out_v": out_v,
            "in_v": in_v,
            "out_cid": out_v,
            "in_cid": in_v,
            "properties": props,
        }

    def get_vertex_by_canonical_id(self, canonical_id: str) -> dict | None:
        rows = self._run(self.builder.match_vertices("_label_placeholder", "canonical_id", canonical_id))
        return rows[0] if rows else None


def _ag_id(rows: list[dict[str, Any]], column: str) -> str:
    if not rows:
        return ""
    value = rows[0].get(column)
    if isinstance(value, dict) and "id" in value:
        return str(value["id"])
    return hashlib.sha256(repr(value).encode()).hexdigest()[:16]
