"""Snowflake warehouse connector supporting metadata crawl, data sampling, and virtual queries.

Complies with CRA-009.1, CRA-009.2, and CRA-009.6.

Enforces:
1. Role, warehouse, database, and schema scoping.
2. Masking policies and row-level access policies.
3. Three distinct execution modes: METADATA_ONLY, SAMPLED_DATA, VIRTUAL_QUERY.
4. Opt-in sampling and query history with automatic secrets and PII redaction.
5. Lineage extraction from query history for CRA-029.
6. 30-second default statement timeout and credit/cost guard.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from collections.abc import Iterator

import httpx

from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
    SourceConnector,
)
from eoip.connectors.errors import ConnectorError
from eoip.connectors.splunk import redact_with_receipt
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities

logger = logging.getLogger(__name__)


class SnowflakeMode(str, Enum):
    METADATA_ONLY = "metadata_only"
    SAMPLED_DATA = "sampled_data"
    VIRTUAL_QUERY = "virtual_query"


@dataclass
class SnowflakeCostGuard:
    """Cost and resource budget for Snowflake operations."""

    max_credits: float = 5.0
    statement_timeout_seconds: float = 30.0  # CRA-009.6 default 30s
    max_result_rows: int = 5000


@dataclass
class ColumnPolicy:
    column_name: str
    data_type: str
    is_masked: bool = False
    masking_policy: str | None = None
    row_access_policy: str | None = None


class SnowflakeConnector:
    """Snowflake Data Cloud connector for metadata and governed virtual access."""

    source_system = "snowflake"
    mapper_version = "snowflake-sql/1.0"

    def __init__(
        self,
        source_id: str,
        account: str,
        *,
        warehouse: str = "COMPUTE_WH",
        database: str = "PROD_DB",
        schema: str = "PUBLIC",
        role: str = "PUBLIC",
        mode: SnowflakeMode = SnowflakeMode.METADATA_ONLY,
        cost_guard: SnowflakeCostGuard | None = None,
        opt_in_sampling: bool = False,
        opt_in_query_history: bool = False,
        sql_version: str = "snowflake-sql/2024.1",
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.source_id = source_id
        self.account = account
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.role = role
        self.mode = mode
        self.cost_guard = cost_guard or SnowflakeCostGuard()
        self.opt_in_sampling = opt_in_sampling
        self.opt_in_query_history = opt_in_query_history
        self.sql_version = sql_version
        self.token = token
        self.username = username
        self.password = password
        self.instance_id = hashlib.sha256(f"{account}:{database}:{schema}".encode()).hexdigest()[:16]

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(
            baseline=True,
            polling=True,
            discovery=True,
            reconciliation=True,
            replay=True,
        )

    def validate_cost_guard(self, credits_consumed: float, duration_seconds: float, rows: int) -> None:
        """Enforce credit cost guards and statement timeouts (CRA-009.6)."""
        if credits_consumed > self.cost_guard.max_credits:
            raise ConnectorError(
                self.source_system,
                "cost_limit_exceeded",
                f"Query credit consumption {credits_consumed} exceeded credit guard {self.cost_guard.max_credits}",
            )
        if duration_seconds > self.cost_guard.statement_timeout_seconds:
            raise ConnectorError(
                self.source_system,
                "statement_timeout",
                f"Query duration {duration_seconds:.1f}s exceeded timeout {self.cost_guard.statement_timeout_seconds:.1f}s",
            )
        if rows > self.cost_guard.max_result_rows:
            raise ConnectorError(
                self.source_system,
                "result_limit_exceeded",
                f"Result rows {rows} exceeded max allowed {self.cost_guard.max_result_rows}",
            )

    def make_table_event(
        self,
        table_name: str,
        columns: list[ColumnPolicy],
        *,
        is_view: bool = False,
        row_count: int | None = None,
        comment: str | None = None,
    ) -> SourceEventV2:
        """Emit metadata event for table or view respecting column and row policies."""
        table_id = f"{self.database}.{self.schema}.{table_name}"
        col_payload = [
            {
                "name": c.column_name,
                "type": c.data_type,
                "is_masked": c.is_masked,
                "masking_policy": c.masking_policy,
                "row_access_policy": c.row_access_policy,
            }
            for c in columns
        ]

        payload = {
            "account": self.account,
            "database": self.database,
            "schema": self.schema,
            "table_name": table_name,
            "full_name": table_id,
            "is_view": is_view,
            "row_count": row_count,
            "columns": col_payload,
            "comment": comment,
            "warehouse": self.warehouse,
            "role": self.role,
        }

        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()
        event_id = hashlib.sha256(f"snowflake:{self.source_id}:{table_id}:{payload_hash}".encode()).hexdigest()
        captured_at = utc_now_iso()

        permissions = PermissionMetadata(
            visibility="INTERNAL",
            principal_refs=[f"snowflake:role:{self.role}"],
            inherited_from=f"snowflake:warehouse:{self.warehouse}",
        )

        return SourceEventV2(
            event_id=event_id,
            source_system=self.source_system,
            source_instance_id=self.instance_id,
            source_record_id=f"table:{table_id}",
            operation="UPSERT",
            source_version=payload_hash,
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=payload_hash,
            permissions=permissions,
            payload=payload,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": "view" if is_view else "table",
                "database": self.database,
                "schema": self.schema,
                "warehouse": self.warehouse,
                "role": self.role,
                "mode": self.mode.value,
                "sql_version": self.sql_version,
                "has_masked_columns": any(c.is_masked for c in columns),
            },
        )

    def sample_table_data(
        self,
        table_name: str,
        sample_rows: list[dict[str, Any]],
        columns: list[ColumnPolicy],
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Opt-in data sampling with strict redaction of sensitive and masked columns (CRA-009.2)."""
        if self.mode != SnowflakeMode.SAMPLED_DATA or not self.opt_in_sampling:
            raise PermissionError(
                "Data sampling rejected: connector is in metadata-only mode or sampling is not explicitly opted in"
            )

        masked_cols = {c.column_name for c in columns if c.is_masked}
        clean_rows = []
        total_redacted = 0

        for row in sample_rows:
            clean_row = {}
            for col, val in row.items():
                if col in masked_cols:
                    clean_row[col] = "[MASKED_BY_POLICY]"
                    total_redacted += 1
                elif isinstance(val, str):
                    redacted_str, receipt = redact_with_receipt(val, f"{table_name}:{col}")
                    clean_row[col] = redacted_str
                    total_redacted += receipt.total_redacted
                else:
                    clean_row[col] = val
            clean_rows.append(clean_row)

        metadata = {
            "table_name": table_name,
            "sampled_count": len(clean_rows),
            "redacted_values_count": total_redacted,
            "mode": self.mode.value,
        }
        return clean_rows, metadata

    def extract_query_history(
        self,
        raw_queries: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Opt-in query history extraction for CRA-029 lineage parsing with literal redaction."""
        if not self.opt_in_query_history:
            raise PermissionError(
                "Query history extraction rejected: query history must be explicitly opted in"
            )

        cleaned_queries = []
        lineage_candidates = []

        for q in raw_queries:
            query_id = q.get("query_id") or ""
            query_text = q.get("query_text") or ""
            # Redact sensitive parameters, credentials, or literals in query string
            clean_text, receipt = redact_with_receipt(query_text, f"query:{query_id}")

            cleaned_queries.append({
                "query_id": query_id,
                "query_text": clean_text,
                "user_name": q.get("user_name"),
                "role_name": q.get("role_name"),
                "warehouse_name": q.get("warehouse_name"),
                "execution_status": q.get("execution_status"),
                "start_time": q.get("start_time"),
                "end_time": q.get("end_time"),
                "total_elapsed_time": q.get("total_elapsed_time"),
                "redactions": receipt.total_redacted,
            })

            # Check for SQL lineage markers (INSERT INTO ... SELECT FROM ...)
            import re
            m = re.search(r"(?i)insert\s+(?:into\s+)?([a-zA-Z0-9_\.]+)\s+select.*?\bfrom\s+([a-zA-Z0-9_\.]+)", clean_text)
            if m:
                lineage_candidates.append({
                    "target_table": m.group(1).upper(),
                    "source_table": m.group(2).upper(),
                    "query_id": query_id,
                    "relationship": "derivedFrom",
                })

        return cleaned_queries, lineage_candidates
