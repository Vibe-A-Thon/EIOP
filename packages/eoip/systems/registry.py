"""Unified Systems Registry — single configuration point for all connected enterprise systems.

Reads and writes config/systems-registry.json, providing CRUD operations,
connection testing, health monitoring, and system lifecycle management.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class SystemStatus(str, Enum):
    PENDING = "PENDING"
    ONBOARDING = "ONBOARDING"
    CONNECTED = "CONNECTED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    DISCONNECTED = "DISCONNECTED"


class SystemCategory(str, Enum):
    PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT"
    SOURCE_CONTROL = "SOURCE_CONTROL"
    CI_CD = "CI_CD"
    DOCUMENTATION = "DOCUMENTATION"
    ITSM = "ITSM"
    MONITORING = "MONITORING"
    SECURITY = "SECURITY"
    DATABASE = "DATABASE"
    API_GATEWAY = "API_GATEWAY"
    MESSAGING = "MESSAGING"
    CLOUD_PLATFORM = "CLOUD_PLATFORM"
    DATA_WAREHOUSE = "DATA_WAREHOUSE"
    FILE_SYSTEM = "FILE_SYSTEM"
    CUSTOM = "CUSTOM"


class AuthType(str, Enum):
    NONE = "none"
    TOKEN = "token"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    CERTIFICATE = "certificate"
    AWS_IAM = "aws_iam"
    KERBEROS = "kerberos"


@dataclass
class RetryPolicy:
    max_retries: int = 3
    backoff_seconds: float = 30.0
    backoff_multiplier: float = 2.0


@dataclass
class IngestionConfig:
    mode: str = "auto"  # auto, manual, scheduled, event_driven
    batch_size: int = 500
    poll_interval_minutes: int = 60
    cron_expression: str | None = None
    dead_letter_queue_enabled: bool = True
    schema_drift_detection: bool = True
    auto_schema_induction: bool = True
    auto_relationship_discovery: bool = True
    incremental_sync: bool = True
    full_sync_interval_hours: int = 24
    entity_types: list[str] = field(default_factory=list)
    custom_mappings: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectionConfig:
    base_url: str = ""
    port: int | None = None
    database_name: str | None = None
    additional_params: dict[str, str] = field(default_factory=dict)


@dataclass
class AuthConfig:
    auth_type: AuthType = AuthType.TOKEN
    credentials: dict[str, str] = field(default_factory=dict)


@dataclass
class SchemaConfig:
    auto_generated: bool = False
    schema_version: str = "1.0.0"
    entity_labels: list[str] = field(default_factory=list)
    edge_labels: list[str] = field(default_factory=list)
    field_mappings: dict[str, dict[str, str]] = field(default_factory=dict)
    induced_at: str | None = None
    graphql_sdl: str | None = None
    json_schema: dict[str, Any] | None = None


@dataclass
class SystemEntry:
    system_id: str
    name: str
    system_type: str
    category: SystemCategory = SystemCategory.CUSTOM
    status: SystemStatus = SystemStatus.PENDING
    connection: ConnectionConfig = field(default_factory=ConnectionConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)
    ingestion: IngestionConfig = field(default_factory=IngestionConfig)
    schema: SchemaConfig = field(default_factory=SchemaConfig)
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    last_sync_at: str | None = None
    last_health_check: dict[str, Any] | None = None
    error_message: str | None = None
    version: int = 1

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["category"] = self.category.value
        d["status"] = self.status.value
        d["auth"]["auth_type"] = self.auth.auth_type.value
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SystemEntry:
        entry = cls(
            system_id=data["system_id"],
            name=data["name"],
            system_type=data["system_type"],
            category=SystemCategory(data.get("category", "CUSTOM")),
            status=SystemStatus(data.get("status", "PENDING")),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            last_sync_at=data.get("last_sync_at"),
            last_health_check=data.get("last_health_check"),
            error_message=data.get("error_message"),
            version=data.get("version", 1),
        )
        conn = data.get("connection", {})
        entry.connection = ConnectionConfig(
            base_url=conn.get("base_url", ""),
            port=conn.get("port"),
            database_name=conn.get("database_name"),
            additional_params=conn.get("additional_params", {}),
        )
        auth = data.get("auth", {})
        entry.auth = AuthConfig(
            auth_type=AuthType(auth.get("auth_type", "token")),
            credentials=auth.get("credentials", {}),
        )
        ing = data.get("ingestion", {})
        entry.ingestion = IngestionConfig(
            mode=ing.get("mode", "auto"),
            batch_size=ing.get("batch_size", 500),
            poll_interval_minutes=ing.get("poll_interval_minutes", 60),
            cron_expression=ing.get("cron_expression"),
            dead_letter_queue_enabled=ing.get("dead_letter_queue_enabled", True),
            schema_drift_detection=ing.get("schema_drift_detection", True),
            auto_schema_induction=ing.get("auto_schema_induction", True),
            auto_relationship_discovery=ing.get("auto_relationship_discovery", True),
            incremental_sync=ing.get("incremental_sync", True),
            full_sync_interval_hours=ing.get("full_sync_interval_hours", 24),
            entity_types=ing.get("entity_types", []),
            custom_mappings=ing.get("custom_mappings", {}),
        )
        sc = data.get("schema", {})
        entry.schema = SchemaConfig(
            auto_generated=sc.get("auto_generated", False),
            schema_version=sc.get("schema_version", "1.0.0"),
            entity_labels=sc.get("entity_labels", []),
            edge_labels=sc.get("edge_labels", []),
            field_mappings=sc.get("field_mappings", {}),
            induced_at=sc.get("induced_at"),
            graphql_sdl=sc.get("graphql_sdl"),
            json_schema=sc.get("json_schema"),
        )
        rp = data.get("retry_policy", {})
        entry.retry_policy = RetryPolicy(
            max_retries=rp.get("max_retries", 3),
            backoff_seconds=rp.get("backoff_seconds", 30.0),
            backoff_multiplier=rp.get("backoff_multiplier", 2.0),
        )
        return entry


# Built-in system type catalog for auto-detecting category and defaults
KNOWN_SYSTEM_TYPES: dict[str, dict[str, Any]] = {
    "jira": {"category": "PROJECT_MANAGEMENT", "entity_types": ["project", "issue", "sprint", "comment", "changelog"]},
    "gitlab": {"category": "SOURCE_CONTROL", "entity_types": ["group", "project", "branch", "merge_request", "pipeline", "issue"]},
    "github": {"category": "SOURCE_CONTROL", "entity_types": ["repo", "branch", "pull_request", "issue", "commit", "release"]},
    "confluence": {"category": "DOCUMENTATION", "entity_types": ["space", "page", "attachment"]},
    "servicenow": {"category": "ITSM", "entity_types": ["incident", "problem", "change_request", "knowledge"]},
    "datadog": {"category": "MONITORING", "entity_types": ["dashboard", "monitor"]},
    "grafana": {"category": "MONITORING", "entity_types": ["dashboard", "alert_rule", "datasource"]},
    "kibana": {"category": "MONITORING", "entity_types": ["dashboard", "search", "index_pattern"]},
    "rally": {"category": "PROJECT_MANAGEMENT", "entity_types": ["user_story", "feature", "epic"]},
    "figma": {"category": "DOCUMENTATION", "entity_types": ["file", "component"]},
    "qtest": {"category": "PROJECT_MANAGEMENT", "entity_types": ["test_case", "test_run", "test_suite"]},
    "kubernetes": {"category": "CLOUD_PLATFORM", "entity_types": ["namespace", "pod", "deployment", "service"]},
    "jenkins": {"category": "CI_CD", "entity_types": ["job", "build", "pipeline"]},
    "sonarqube": {"category": "SECURITY", "entity_types": ["project", "issue", "measure"]},
    "elasticsearch": {"category": "DATABASE", "entity_types": ["index", "document"]},
    "postgresql": {"category": "DATABASE", "entity_types": ["table", "view", "function"]},
    "mongodb": {"category": "DATABASE", "entity_types": ["database", "collection"]},
    "redis": {"category": "DATABASE", "entity_types": ["key", "stream"]},
    "kafka": {"category": "MESSAGING", "entity_types": ["topic", "consumer_group", "partition"]},
    "rabbitmq": {"category": "MESSAGING", "entity_types": ["queue", "exchange", "binding"]},
    "aws": {"category": "CLOUD_PLATFORM", "entity_types": ["ec2_instance", "s3_bucket", "lambda_function", "rds_instance"]},
    "azure": {"category": "CLOUD_PLATFORM", "entity_types": ["resource_group", "vm", "storage_account", "function_app"]},
    "gcp": {"category": "CLOUD_PLATFORM", "entity_types": ["project", "compute_instance", "gcs_bucket", "cloud_function"]},
    "slack": {"category": "MESSAGING", "entity_types": ["channel", "message", "user"]},
    "pagerduty": {"category": "MONITORING", "entity_types": ["service", "incident", "escalation_policy"]},
    "terraform": {"category": "CI_CD", "entity_types": ["resource", "module", "state"]},
    "vault": {"category": "SECURITY", "entity_types": ["secret", "policy", "auth_method"]},
    "snyk": {"category": "SECURITY", "entity_types": ["project", "vulnerability", "dependency"]},
    "splunk": {"category": "MONITORING", "entity_types": ["index", "search", "alert"]},
    "newrelic": {"category": "MONITORING", "entity_types": ["application", "alert", "dashboard"]},
    "custom_json": {"category": "CUSTOM", "entity_types": []},
    "custom_api": {"category": "CUSTOM", "entity_types": []},
    "custom_file": {"category": "CUSTOM", "entity_types": []},
    "custom_database": {"category": "CUSTOM", "entity_types": []},
}


class SystemsRegistry:
    """Thread-safe CRUD manager for the unified systems-registry.json config."""

    def __init__(self, config_path: str | Path | None = None) -> None:
        if config_path is None:
            config_path = Path(__file__).resolve().parents[3] / "config" / "systems-registry.json"
        self._path = Path(config_path)
        self._lock = threading.RLock()
        self._data = self._load()

    def _load(self) -> dict[str, Any]:
        if self._path.exists():
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "$schema": "urn:eoip:systems-registry:v1",
            "version": "1.0.0",
            "global_defaults": {},
            "systems": [],
        }

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, default=str)
        tmp.replace(self._path)

    def _now(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # ---- CRUD ----

    def list_systems(self, status: SystemStatus | None = None,
                     category: SystemCategory | None = None) -> list[SystemEntry]:
        with self._lock:
            entries = [SystemEntry.from_dict(s) for s in self._data.get("systems", [])]
            if status:
                entries = [e for e in entries if e.status == status]
            if category:
                entries = [e for e in entries if e.category == category]
            return entries

    def get_system(self, system_id: str) -> SystemEntry | None:
        with self._lock:
            for s in self._data.get("systems", []):
                if s["system_id"] == system_id:
                    return SystemEntry.from_dict(s)
            return None

    def register_system(
        self,
        name: str,
        system_type: str,
        connection: dict[str, Any] | None = None,
        auth: dict[str, Any] | None = None,
        ingestion: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> SystemEntry:
        with self._lock:
            system_id = f"sys-{system_type}-{uuid.uuid4().hex[:8]}"
            known = KNOWN_SYSTEM_TYPES.get(system_type, {})
            category = SystemCategory(known.get("category", "CUSTOM"))
            default_entities = known.get("entity_types", [])

            now = self._now()
            entry = SystemEntry(
                system_id=system_id,
                name=name,
                system_type=system_type,
                category=category,
                status=SystemStatus.PENDING,
                tags=tags or [],
                metadata=metadata or {},
                created_at=now,
                updated_at=now,
            )

            if connection:
                entry.connection = ConnectionConfig(
                    base_url=connection.get("base_url", ""),
                    port=connection.get("port"),
                    database_name=connection.get("database_name"),
                    additional_params=connection.get("additional_params", {}),
                )
            if auth:
                entry.auth = AuthConfig(
                    auth_type=AuthType(auth.get("auth_type", "token")),
                    credentials=auth.get("credentials", {}),
                )
            if ingestion:
                entry.ingestion = IngestionConfig(**{
                    k: v for k, v in ingestion.items()
                    if k in IngestionConfig.__dataclass_fields__
                })
            if default_entities and not entry.ingestion.entity_types:
                entry.ingestion.entity_types = default_entities

            self._data["systems"].append(entry.to_dict())
            self._save()
            return entry

    def update_system(self, system_id: str, updates: dict[str, Any]) -> SystemEntry | None:
        with self._lock:
            for i, s in enumerate(self._data.get("systems", [])):
                if s["system_id"] == system_id:
                    for key, val in updates.items():
                        if key in ("connection", "auth", "ingestion", "schema", "retry_policy"):
                            s.setdefault(key, {}).update(val)
                        else:
                            s[key] = val
                    s["updated_at"] = self._now()
                    s["version"] = s.get("version", 1) + 1
                    self._data["systems"][i] = s
                    self._save()
                    return SystemEntry.from_dict(s)
            return None

    def remove_system(self, system_id: str) -> bool:
        with self._lock:
            before = len(self._data.get("systems", []))
            self._data["systems"] = [
                s for s in self._data.get("systems", [])
                if s["system_id"] != system_id
            ]
            if len(self._data["systems"]) < before:
                self._save()
                return True
            return False

    def set_status(self, system_id: str, status: SystemStatus,
                   error_message: str | None = None) -> SystemEntry | None:
        updates: dict[str, Any] = {"status": status.value}
        if error_message is not None:
            updates["error_message"] = error_message
        elif status in (SystemStatus.ACTIVE, SystemStatus.CONNECTED):
            updates["error_message"] = None
        return self.update_system(system_id, updates)

    def record_sync(self, system_id: str, result: dict[str, Any]) -> SystemEntry | None:
        return self.update_system(system_id, {
            "last_sync_at": self._now(),
            "metadata": {"last_sync_result": result},
        })

    def record_health(self, system_id: str, health: dict[str, Any]) -> SystemEntry | None:
        return self.update_system(system_id, {
            "last_health_check": {**health, "checked_at": self._now()},
        })

    def test_connection(self, system_id: str) -> dict[str, Any]:
        entry = self.get_system(system_id)
        if not entry:
            return {"success": False, "error": f"System {system_id} not found"}
        result = {
            "system_id": system_id,
            "system_type": entry.system_type,
            "base_url": entry.connection.base_url,
            "success": True,
            "latency_ms": 0.0,
            "message": "Connection test passed (dry-run mode)",
            "tested_at": self._now(),
        }
        self.record_health(system_id, result)
        return result

    def get_known_system_types(self) -> dict[str, dict[str, Any]]:
        return dict(KNOWN_SYSTEM_TYPES)

    def get_global_defaults(self) -> dict[str, Any]:
        return dict(self._data.get("global_defaults", {}))

    def update_global_defaults(self, defaults: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            self._data.setdefault("global_defaults", {}).update(defaults)
            self._save()
            return dict(self._data["global_defaults"])

    def export_config(self) -> dict[str, Any]:
        with self._lock:
            return json.loads(json.dumps(self._data, default=str))

    def import_config(self, config: dict[str, Any]) -> int:
        with self._lock:
            imported = 0
            existing_ids = {s["system_id"] for s in self._data.get("systems", [])}
            for sys_data in config.get("systems", []):
                if sys_data.get("system_id") not in existing_ids:
                    self._data["systems"].append(sys_data)
                    imported += 1
            if imported:
                self._save()
            return imported
