"""ServiceNow Table API connector emitting SourceEvents for operations records."""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso

logger = logging.getLogger(__name__)

# FR-SNOW-001 sync scope: these record kinds are fetched by default.
CORE_TABLES = {
    "incident": "incident",
    "problem": "problem",
    "change": "change_request",
    "knowledge": "kb_knowledge",
}
# CRA-008.6 CMDB table profiles. Known (mapping + ACL), but synced only when
# opted in (include_cmdb=True or an explicit tables= entry): least privilege,
# no cmdb_read scope required by default, and instances without CMDB still
# sync (FT-D03).
OPTIONAL_TABLES = {
    "cmdb_ci": "cmdb_ci",
    "cmdb_rel_ci": "cmdb_rel_ci",
}
DEFAULT_TABLES = {**CORE_TABLES, **OPTIONAL_TABLES}

DEFAULT_FIELDS = {
    "record_id": "sys_id",
    "number": "number",
    "short_description": "short_description",
    "description": "description",
    "state": "state",
    "updated_at": "sys_updated_on",
}
TABLE_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class ServiceNowConnector(RestConnector):
    source_system = "servicenow"
    mapper_version = "servicenow-table-api/1.0"

    def __init__(
        self,
        base_url: str,
        *,
        tables: dict[str, str] | None = None,
        field_mapping: dict[str, str] | None = None,
        page_size: int = 500,
        include_cmdb: bool = False,
        **kwargs,
    ) -> None:
        if not 1 <= page_size <= 10000:
            raise ValueError("page_size must be between 1 and 10000")
        self.tables = {**DEFAULT_TABLES, **(tables or {})}
        explicit = set(tables or {})
        self.sync_kinds = [
            kind for kind in self.tables
            if kind in CORE_TABLES or kind in explicit or (include_cmdb and kind in OPTIONAL_TABLES)
        ]
        self.skipped_tables: list[dict[str, str]] = []
        if not self.tables or any(not TABLE_NAME.fullmatch(table) for table in self.tables.values()):
            raise ValueError("ServiceNow table names must be simple identifiers")
        self.field_mapping = {**DEFAULT_FIELDS, **(field_mapping or {})}
        super().__init__(base_url, **kwargs)
        self.page_size = page_size

    def sync(
        self,
        *,
        checkpoint: str | None = None,
        watermark: str | None = None,
        correlation_id: str | None = None,
    ) -> SyncBatch:
        correlation_id = self.correlation_id(correlation_id)
        watermark_dt = parse_utc(watermark) if watermark else datetime.now(UTC)
        if watermark_dt is None:
            raise ValueError("invalid ServiceNow watermark")
        next_checkpoint = utc_timestamp(watermark_dt)
        checkpoint_dt = parse_utc(checkpoint)
        query_parts = []
        if checkpoint_dt:
            query_parts.append(f"sys_updated_on>={self._sn_time(checkpoint_dt)}")
        query_parts.extend(
            [
                f"sys_updated_on<={self._sn_time(watermark_dt)}",
                "ORDERBYsys_updated_on",
                "ORDERBYsys_id",
            ]
        )
        query = "^".join(query_parts)
        events = []
        self.skipped_tables = []
        for record_kind in self.sync_kinds:
            table = self.tables[record_kind]
            offset = 0
            while True:
                try:
                    response = self.get_json(
                        f"/api/now/table/{table}",
                        params={
                            "sysparm_query": query,
                            "sysparm_limit": self.page_size,
                            "sysparm_offset": offset,
                            "sysparm_display_value": "false",
                            "sysparm_exclude_reference_link": "true",
                        },
                        correlation_id=correlation_id,
                    )
                except ConnectorError as exc:
                    # An optional (CMDB) table that is missing or forbidden on this instance
                    # yields a per-table warning instead of failing the whole sync (FT-D03).
                    if record_kind in OPTIONAL_TABLES and exc.category in ("authentication_failed", "remote_error"):
                        logger.warning(
                            "servicenow optional table skipped",
                            extra={"table": table, "error_category": exc.category, "correlation_id": correlation_id},
                        )
                        self.skipped_tables.append({"table": table, "category": exc.category})
                        break
                    raise
                records = response.get("result")
                if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
                    self._log_failure("invalid_response", correlation_id)
                    raise ConnectorError(self.source_system, "invalid_response", correlation_id)
                if not records:
                    break
                for record in records:
                    record_id = record.get("sys_id")
                    if record_id is None or not str(record_id).strip():
                        self._log_failure("schema_drift", correlation_id)
                        raise ConnectorError(self.source_system, "schema_drift", correlation_id)
                    version = record.get("sys_updated_on") or record.get("sys_mod_count")
                    events.append(
                        self.make_event(
                            record_kind,
                            f"{self.instance_id}:{table}:{record_id}",
                            record,
                            version,
                        )
                    )
                offset += len(records)
                if len(records) < self.page_size:
                    break
        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind not in self.tables:
            raise ValueError("unsupported ServiceNow record kind")
        record_id = record.get(self.field_mapping["record_id"])
        number = record.get(self.field_mapping["number"])
        if record_id is None or not str(record_id).strip():
            raise ValueError("ServiceNow record requires sys_id")
        if number is None or not str(number).strip():
            raise ValueError("ServiceNow record requires number")
        return {
            "kind": kind,
            "record_id": str(record_id),
            "number": str(number),
            "short_description": record.get(self.field_mapping["short_description"]),
            "description": record.get(self.field_mapping["description"]),
            "state": record.get(self.field_mapping["state"]),
            "updated_at": record.get(self.field_mapping["updated_at"]),
        }

    def make_event(
        self,
        record_kind: str,
        source_record_id: str,
        payload: dict,
        source_version: str | int | None,
        *,
        operation: str = "UPSERT",
        permissions: PermissionMetadata | None = None,
    ) -> SourceEventV2:
        import hashlib
        import json
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        event_id = hashlib.sha256(
            f"{self.source_system}:{record_kind}:{source_record_id}:{payload_hash}:{operation}".encode()
        ).hexdigest()
        captured_at = utc_now_iso()

        if permissions is None:
            domain = str(payload.get("sys_domain") or "global")
            principals = [f"servicenow:domain:{domain}"]
            if record_kind.startswith("cmdb"):
                principals.append("servicenow:role:cmdb_read")
            else:
                principals.append("servicenow:role:itil")
            permissions = PermissionMetadata(
                visibility="RESTRICTED" if domain != "global" else "INTERNAL",
                principal_refs=principals,
                inherited_from=f"servicenow:domain:{domain}",
            )

        return SourceEventV2(
            event_id=event_id,
            source_system=self.source_system,
            source_instance_id=self.instance_id,
            source_record_id=source_record_id,
            operation=operation,
            source_version=str(source_version) if source_version is not None else payload_hash,
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=payload_hash,
            permissions=permissions,
            payload=payload if operation != "DELETE" else None,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": record_kind,
                "source_instance_id": self.instance_id,
                "acl_vector": list(permissions.principal_refs),
            },
        )

    @staticmethod
    def detect_cmdb_cycles(relations: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Detect directed cycles in CMDB CI relations and return data-quality findings without dropping edges (CRA-008.9)."""
        from collections import defaultdict
        adj = defaultdict(list)
        for rel in relations:
            parent = rel.get("parent")
            child = rel.get("child")
            if parent and child:
                adj[str(parent)].append(str(child))

        visited: dict[str, int] = {}
        stack: list[str] = []
        cycles: list[list[str]] = []

        def dfs(node: str):
            visited[node] = 1
            stack.append(node)
            for neighbor in adj.get(node, []):
                if visited.get(neighbor) == 1:
                    idx = stack.index(neighbor)
                    cycles.append(stack[idx:] + [neighbor])
                elif not visited.get(neighbor):
                    dfs(neighbor)
            stack.pop()
            visited[node] = 2

        for node in list(adj.keys()):
            if not visited.get(node):
                dfs(node)

        findings = []
        for c in cycles:
            findings.append({
                "type": "CMDB_DEPENDENCY_CYCLE",
                "severity": "HIGH",
                "cycle_path": c,
                "cycle_length": len(c) - 1,
                "description": f"Circular dependency detected in CMDB: {' -> '.join(c)}",
            })
        return findings

    @staticmethod
    def _sn_time(value) -> str:
        return value.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S")
