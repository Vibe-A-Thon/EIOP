"""Schema Migration & Version Control — versioned schema changes with up/down migrations."""

from __future__ import annotations

import hashlib
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable


class MigrationStatus(str, Enum):
    PENDING = "PENDING"
    APPLIED = "APPLIED"
    ROLLING_BACK = "ROLLING_BACK"
    ROLLED_BACK = "ROLLED_BACK"
    FAILED = "FAILED"


class MigrationAction(str, Enum):
    ADD_VERTEX_TYPE = "ADD_VERTEX_TYPE"
    REMOVE_VERTEX_TYPE = "REMOVE_VERTEX_TYPE"
    ADD_EDGE_TYPE = "ADD_EDGE_TYPE"
    REMOVE_EDGE_TYPE = "REMOVE_EDGE_TYPE"
    ADD_PROPERTY = "ADD_PROPERTY"
    REMOVE_PROPERTY = "REMOVE_PROPERTY"
    RENAME_PROPERTY = "RENAME_PROPERTY"
    CHANGE_PROPERTY_TYPE = "CHANGE_PROPERTY_TYPE"
    ADD_INDEX = "ADD_INDEX"
    REMOVE_INDEX = "REMOVE_INDEX"
    ADD_CONSTRAINT = "ADD_CONSTRAINT"
    REMOVE_CONSTRAINT = "REMOVE_CONSTRAINT"


@dataclass
class MigrationStep:
    action: MigrationAction
    target: str
    params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["action"] = self.action.value
        return d


@dataclass
class Migration:
    migration_id: str
    version: str
    name: str
    description: str = ""
    up_steps: list[MigrationStep] = field(default_factory=list)
    down_steps: list[MigrationStep] = field(default_factory=list)
    status: MigrationStatus = MigrationStatus.PENDING
    applied_at: str | None = None
    rolled_back_at: str | None = None
    checksum: str = ""
    depends_on: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = {
            "migration_id": self.migration_id,
            "version": self.version,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "applied_at": self.applied_at,
            "rolled_back_at": self.rolled_back_at,
            "checksum": self.checksum,
            "up_steps": [s.to_dict() for s in self.up_steps],
            "down_steps": [s.to_dict() for s in self.down_steps],
            "depends_on": self.depends_on,
        }
        return d


class SchemaMigrationManager:
    """Manages versioned schema migrations with rollback support."""

    def __init__(self, apply_fn: Callable[[MigrationStep], bool] | None = None) -> None:
        self._apply_fn = apply_fn or (lambda step: True)
        self._migrations: dict[str, Migration] = {}
        self._version_order: list[str] = []
        self._current_version: str = "0.0.0"
        self._schema_state: dict[str, Any] = {
            "vertex_types": {}, "edge_types": {},
            "properties": {}, "indexes": [], "constraints": [],
        }
        self._lock = threading.RLock()

    def create_migration(self, version: str, name: str,
                         up_steps: list[dict[str, Any]],
                         down_steps: list[dict[str, Any]] | None = None,
                         description: str = "",
                         depends_on: list[str] | None = None) -> Migration:
        with self._lock:
            mid = uuid.uuid4().hex[:12]
            parsed_up = [
                MigrationStep(
                    action=MigrationAction(s["action"]),
                    target=s["target"],
                    params=s.get("params", {}),
                )
                for s in up_steps
            ]
            parsed_down = [
                MigrationStep(
                    action=MigrationAction(s["action"]),
                    target=s["target"],
                    params=s.get("params", {}),
                )
                for s in (down_steps or [])
            ]
            raw = f"{version}:{name}:{[s.to_dict() for s in parsed_up]}"
            checksum = hashlib.sha256(raw.encode()).hexdigest()[:12]

            migration = Migration(
                migration_id=mid, version=version, name=name,
                description=description, up_steps=parsed_up,
                down_steps=parsed_down, checksum=checksum,
                depends_on=depends_on or [],
            )
            self._migrations[mid] = migration
            self._version_order.append(mid)
            return migration

    def apply_migration(self, migration_id: str) -> bool:
        with self._lock:
            migration = self._migrations.get(migration_id)
            if not migration or migration.status != MigrationStatus.PENDING:
                return False

            for dep_id in migration.depends_on:
                dep = self._migrations.get(dep_id)
                if dep and dep.status != MigrationStatus.APPLIED:
                    return False

            for step in migration.up_steps:
                try:
                    success = self._apply_fn(step)
                    if success:
                        self._update_schema_state(step)
                    else:
                        migration.status = MigrationStatus.FAILED
                        return False
                except Exception:
                    migration.status = MigrationStatus.FAILED
                    return False

            migration.status = MigrationStatus.APPLIED
            migration.applied_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            self._current_version = migration.version
            return True

    def rollback_migration(self, migration_id: str) -> bool:
        with self._lock:
            migration = self._migrations.get(migration_id)
            if not migration or migration.status != MigrationStatus.APPLIED:
                return False

            if not migration.down_steps:
                return False

            migration.status = MigrationStatus.ROLLING_BACK
            for step in migration.down_steps:
                try:
                    self._apply_fn(step)
                    self._update_schema_state(step)
                except Exception:
                    migration.status = MigrationStatus.FAILED
                    return False

            migration.status = MigrationStatus.ROLLED_BACK
            migration.rolled_back_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            applied = [m for m in self._migrations.values()
                       if m.status == MigrationStatus.APPLIED]
            if applied:
                self._current_version = max(applied, key=lambda m: m.version).version
            else:
                self._current_version = "0.0.0"
            return True

    def apply_all_pending(self) -> dict[str, Any]:
        applied = []
        failed = []
        for mid in self._version_order:
            migration = self._migrations.get(mid)
            if migration and migration.status == MigrationStatus.PENDING:
                if self.apply_migration(mid):
                    applied.append(mid)
                else:
                    failed.append(mid)
                    break
        return {"applied": applied, "failed": failed, "version": self._current_version}

    def get_migration(self, migration_id: str) -> Migration | None:
        return self._migrations.get(migration_id)

    def list_migrations(self) -> list[dict[str, Any]]:
        return [self._migrations[mid].to_dict()
                for mid in self._version_order if mid in self._migrations]

    def get_current_version(self) -> str:
        return self._current_version

    def get_schema_state(self) -> dict[str, Any]:
        return dict(self._schema_state)

    def _update_schema_state(self, step: MigrationStep) -> None:
        action = step.action
        if action == MigrationAction.ADD_VERTEX_TYPE:
            self._schema_state["vertex_types"][step.target] = step.params
        elif action == MigrationAction.REMOVE_VERTEX_TYPE:
            self._schema_state["vertex_types"].pop(step.target, None)
        elif action == MigrationAction.ADD_EDGE_TYPE:
            self._schema_state["edge_types"][step.target] = step.params
        elif action == MigrationAction.REMOVE_EDGE_TYPE:
            self._schema_state["edge_types"].pop(step.target, None)
        elif action == MigrationAction.ADD_PROPERTY:
            self._schema_state["properties"][step.target] = step.params
        elif action == MigrationAction.REMOVE_PROPERTY:
            self._schema_state["properties"].pop(step.target, None)
        elif action == MigrationAction.ADD_INDEX:
            self._schema_state["indexes"].append({"target": step.target, **step.params})
        elif action == MigrationAction.ADD_CONSTRAINT:
            self._schema_state["constraints"].append({"target": step.target, **step.params})
