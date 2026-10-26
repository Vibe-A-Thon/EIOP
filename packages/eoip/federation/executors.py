"""Real remote-source executors for the OBDA federation engine (CRA-024.4).

* ``SnowflakeSqlExecutor`` runs the parameterised pushdown SELECT through the official
  ``snowflake-connector-python`` DB-API (any DB-API 2 ``connect`` callable can be injected).
  CI exercises it against ``fakesnow`` (DuckDB-backed Snowflake emulator); live validation
  with a customer Snowflake account is pending.
* ``JiraRestExecutor`` translates pushed-down filters to escaped JQL and pages through the
  Jira Cloud enhanced search API (``POST /rest/api/3/search/jql`` with ``nextPageToken``),
  honouring ``Retry-After`` on 429 and failing closed on 401/403. CI exercises it with
  contract mocks of the documented response shapes; live validation with a customer
  Jira site is pending.

Executors never fabricate rows: failures raise ``SourceExecutionError``/``SourceAuthError``
so the engine can report a PARTIAL outcome with a diagnostic.
"""
from __future__ import annotations

import re
import time
from typing import Any, Callable, Optional

import httpx

from eoip.federation.obda import FederatedPushdownFragment, SourceAuthDelegation, build_select, safe_identifier


class SourceExecutionError(RuntimeError):
    """Remote source failed to answer the pushed-down fragment."""


class SourceAuthError(SourceExecutionError):
    """Remote source rejected the delegated credentials (401/403 or connector auth failure)."""


# --------------------------------------------------------------------------------------------------
# Snowflake (SQL)
# --------------------------------------------------------------------------------------------------


class SnowflakeSqlExecutor:
    """Executes pushdown fragments as bound-parameter SQL against Snowflake (or a DB-API stand-in)."""

    def __init__(
        self,
        table: str,
        *,
        account: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        warehouse: Optional[str] = None,
        auth: Optional[SourceAuthDelegation] = None,
        connect: Optional[Callable[..., Any]] = None,
        max_rows: int = 100_000,
    ) -> None:
        self.table = safe_identifier(table)
        self.account = account
        self.database = database
        self.schema = schema
        self.warehouse = warehouse
        self.auth = auth
        self.max_rows = max_rows
        self._connect = connect
        self._conn: Any = None
        self.last_sql: Optional[str] = None
        self.last_params: dict[str, Any] = {}

    def _connection(self) -> Any:
        if self._conn is not None:
            return self._conn
        connect = self._connect
        if connect is None:
            try:
                import snowflake.connector as sf  # type: ignore[import-not-found]
            except ImportError as exc:  # pragma: no cover - depends on optional extra
                raise SourceExecutionError(
                    "snowflake-connector-python is not installed (pip install 'eoip[snowflake]')"
                ) from exc
            connect = sf.connect
        kwargs: dict[str, Any] = {
            k: v for k, v in {
                "account": self.account, "database": self.database,
                "schema": self.schema, "warehouse": self.warehouse,
            }.items() if v
        }
        if self.auth is not None:
            kwargs.update(self.auth.connector_kwargs())
        try:
            self._conn = connect(**kwargs)
        except Exception as exc:  # noqa: BLE001
            name = type(exc).__name__
            if "Auth" in name or "Forbidden" in name:
                raise SourceAuthError(f"snowflake auth failed: {name}") from exc
            raise SourceExecutionError(f"snowflake connect failed: {name}: {exc}") from exc
        return self._conn

    def __call__(self, fragment: FederatedPushdownFragment) -> list[dict[str, Any]]:
        sql, params = build_select(self.table, fragment.pushed_filters, fragment.pushed_projection)
        self.last_sql, self.last_params = sql, params
        cur = self._connection().cursor()
        try:
            cur.execute(sql, params or None)
            names = [str(d[0]) for d in cur.description or []]
            rows = cur.fetchmany(self.max_rows + 1)
        except Exception as exc:  # noqa: BLE001
            raise SourceExecutionError(f"snowflake query failed: {type(exc).__name__}: {exc}") from exc
        finally:
            try:
                cur.close()
            except Exception:  # noqa: BLE001
                pass
        if len(rows) > self.max_rows:
            raise SourceExecutionError(f"remote result exceeds max_rows={self.max_rows}; refine pushdown")
        # Snowflake upper-cases unquoted identifiers; expose rows under the caller's column names.
        wanted = {c.upper(): c for c in fragment.pushed_projection}
        keys = [wanted.get(n.upper(), n.lower()) for n in names]
        return [dict(zip(keys, row)) for row in rows]

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None


# --------------------------------------------------------------------------------------------------
# Jira Cloud (REST)
# --------------------------------------------------------------------------------------------------

_JQL_FIELD = re.compile(r"^(?:[A-Za-z][A-Za-z0-9_]*|customfield_\d+|cf\[\d+\])$")


def jql_literal(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def build_jql(filters: dict[str, Any], base_jql: str = "") -> str:
    clauses = [f"({base_jql})"] if base_jql else []
    for field_name, value in filters.items():
        if not _JQL_FIELD.match(field_name):
            raise ValueError(f"unsafe JQL field: {field_name!r}")
        if value is None:
            clauses.append(f"{field_name} is EMPTY")
        elif isinstance(value, (list, tuple, set)):
            clauses.append(f"{field_name} in ({', '.join(jql_literal(v) for v in value)})")
        else:
            clauses.append(f"{field_name} = {jql_literal(value)}")
    return " AND ".join(clauses) + " ORDER BY key ASC" if clauses else "ORDER BY key ASC"


def _flatten_field(value: Any) -> Any:
    if isinstance(value, dict):
        for k in ("name", "value", "displayName", "key"):
            if k in value:
                return value[k]
    if isinstance(value, list):
        return [_flatten_field(v) for v in value]
    return value


class JiraRestExecutor:
    """Executes pushdown fragments against Jira Cloud's enhanced JQL search API."""

    SEARCH_PATH = "/rest/api/3/search/jql"

    def __init__(
        self,
        base_url: str,
        auth: SourceAuthDelegation,
        *,
        base_jql: str = "",
        page_size: int = 100,
        max_issues: int = 10_000,
        max_retries: int = 3,
        timeout: float = 30.0,
        transport: Optional[httpx.BaseTransport] = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if not base_url.startswith("https://") and not base_url.startswith("http://127.0.0.1") \
                and not base_url.startswith("http://localhost") and transport is None:
            raise ValueError("Jira base_url must be https")
        self.base_url = base_url.rstrip("/")
        self.auth = auth
        self.base_jql = base_jql
        self.page_size = max(1, min(page_size, 5000))
        self.max_issues = max_issues
        self.max_retries = max_retries
        self.timeout = timeout
        self._transport = transport
        self._sleep = sleep
        self.requests_made = 0

    def _post(self, client: httpx.Client, body: dict[str, Any]) -> dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            self.requests_made += 1
            try:
                resp = client.post(self.SEARCH_PATH, json=body)
            except httpx.HTTPError as exc:
                raise SourceExecutionError(f"jira transport error: {type(exc).__name__}") from exc
            if resp.status_code == 429 and attempt < self.max_retries:
                try:
                    delay = float(resp.headers.get("Retry-After", "1"))
                except ValueError:
                    delay = 1.0
                self._sleep(min(max(delay, 0.0), 60.0))
                continue
            if resp.status_code in (401, 403):
                raise SourceAuthError(f"jira rejected delegated credentials (HTTP {resp.status_code})")
            if resp.status_code >= 400:
                msgs = []
                try:
                    msgs = resp.json().get("errorMessages", [])
                except ValueError:
                    pass
                raise SourceExecutionError(f"jira search failed (HTTP {resp.status_code}): {'; '.join(msgs)[:300]}")
            try:
                return resp.json()
            except ValueError as exc:
                raise SourceExecutionError("jira returned non-JSON body") from exc
        raise SourceExecutionError("jira rate limit: retries exhausted")

    def __call__(self, fragment: FederatedPushdownFragment) -> list[dict[str, Any]]:
        projection = list(fragment.pushed_projection)
        jira_fields = [f for f in projection if f not in ("key", "id")] or ["*navigable"]
        body: dict[str, Any] = {
            "jql": build_jql(fragment.pushed_filters, self.base_jql),
            "fields": jira_fields,
            "maxResults": self.page_size,
        }
        headers = {"Accept": "application/json", **self.auth.get_auth_headers()}
        rows: list[dict[str, Any]] = []
        with httpx.Client(base_url=self.base_url, headers=headers, timeout=self.timeout,
                          transport=self._transport) as client:
            while True:
                page = self._post(client, body)
                for issue in page.get("issues", []):
                    fields = issue.get("fields") or {}
                    row: dict[str, Any] = {"key": issue.get("key"), "id": issue.get("id")}
                    for name, value in fields.items():
                        row[name] = _flatten_field(value)
                    if projection:
                        row = {k: row.get(k) for k in projection}
                    rows.append(row)
                    if len(rows) > self.max_issues:
                        raise SourceExecutionError(f"jira result exceeds max_issues={self.max_issues}")
                token = page.get("nextPageToken")
                if page.get("isLast", token is None) or not token:
                    break
                body = {**body, "nextPageToken": token}
        return rows
