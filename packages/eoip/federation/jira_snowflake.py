"""Federated query: local Jira work-item nodes joined with virtualized Snowflake tables (CRA-024 A.2).

Acceptance (CRA-024 A.2, AGG): "a federated query joining local Jira nodes with virtualized Snowflake tables
returns correct results within the deadline". The path is the production one:

1. Jira issues are ingested through :class:`eoip.connectors.jira.JiraConnector` (REST v3 enhanced search) and
   written as ``WorkItem`` vertices in the GraphStore (the "local Jira nodes").
2. The local side is filtered in the graph (``find_vertices``) - the graph-side pushdown.
3. The Snowflake side is never copied: :class:`eoip.federation.obda.OBDAFederationEngine` pushes the filter and
   projection to Snowflake as bound-parameter SQL (:class:`eoip.federation.executors.SnowflakeSqlExecutor`)
   and joins with SQL NULL / SET-or-BAG semantics.
4. The whole query runs under the CRA-024.9 deadline (30 s default); past it the caller gets ``TIMEOUT`` and
   no rows (never partial results presented as complete).

Validation status: PENDING LIVE VALIDATION. CI exercises it with the Jira REST contract mock and the fakesnow
Snowflake emulator; no customer Jira site or Snowflake account has been used.
"""
from __future__ import annotations

import concurrent.futures
import time
from dataclasses import dataclass, field
from typing import Any

from eoip.federation.obda import OBDAFederationEngine, SemanticsMode

VALIDATION_STATUS = "pending live validation (Jira REST contract mock + fakesnow Snowflake emulator)"
DEADLINE_S = 30.0
LOCAL_LIMIT = 1_000_000


def ingest_jira_work_items(connector: Any, store: Any) -> int:
    """Baseline-ingest a Jira connector's issues as ``WorkItem`` vertices; returns the number written."""
    n = 0
    for ev in connector.baseline():
        if ev.metadata.get("record_kind") != "issue" or not ev.payload:
            continue
        issue = ev.payload
        f = issue.get("fields") or {}
        key = str(issue.get("key"))
        store.upsert_vertex("WorkItem", {
            "canonical_id": f"jira:{ev.source_instance_id}:{key}",
            "issue_key": key,
            "summary": str(f.get("summary") or ""),
            "status": (f.get("status") or {}).get("name"),
            "issue_type": (f.get("issuetype") or {}).get("name"),
            "project_key": (f.get("project") or {}).get("key"),
            "source_system": "jira",
            "source_event_id": ev.event_id,
            "modified_at": f.get("updated"),
        })
        n += 1
    return n


@dataclass
class FederatedQueryResult:
    status: str  # SUCCESS | PARTIAL | TIMEOUT
    rows: list[dict[str, Any]]
    local_rows: int
    elapsed_ms: float
    deadline_s: float
    remote_sql: str | None = None
    degraded_sources: list[str] = field(default_factory=list)
    errors: dict[str, str] = field(default_factory=dict)
    validation: str = VALIDATION_STATUS


def query_work_items_with_snowflake(store: Any, engine: OBDAFederationEngine, snowflake_source: str, *,
                                    local_filters: dict[str, Any] | None = None,
                                    remote_filters: dict[str, Any] | None = None,
                                    remote_projection: list[str] | None = None,
                                    remote_key: str = "jira_key",
                                    semantics: SemanticsMode = SemanticsMode.SET,
                                    deadline_s: float = DEADLINE_S) -> FederatedQueryResult:
    """Join local Jira ``WorkItem`` nodes (filtered in the graph) with a virtualized Snowflake table."""
    deadline_s = min(deadline_s, DEADLINE_S)  # tenant budgets may only lower it (CRA-024.9)
    t0 = time.perf_counter()

    def run():
        local = [{"issue_key": v["properties"]["issue_key"], "summary": v["properties"].get("summary"),
                  "status": v["properties"].get("status")}
                 for v in store.find_vertices("WorkItem", filters=local_filters or None, limit=LOCAL_LIMIT)]
        out = engine.execute_federated_join(local, snowflake_source, "issue_key", remote_key,
                                            remote_filters=remote_filters, remote_projection=remote_projection,
                                            semantics=semantics)
        return local, out

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    fut = pool.submit(run)
    try:
        local, out = fut.result(timeout=deadline_s)
    except concurrent.futures.TimeoutError:
        fut.cancel()
        pool.shutdown(wait=False, cancel_futures=True)
        return FederatedQueryResult("TIMEOUT", [], 0, (time.perf_counter() - t0) * 1000, deadline_s,
                                    errors={"deadline": f"federated query exceeded {deadline_s:g} s"})
    pool.shutdown(wait=False)
    executor = engine._source_executors.get(snowflake_source)
    return FederatedQueryResult(out.status, out.rows, len(local), (time.perf_counter() - t0) * 1000, deadline_s,
                                remote_sql=getattr(executor, "last_sql", None),
                                degraded_sources=list(out.degraded_sources), errors=dict(out.errors or {}))
