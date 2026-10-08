"""Config-as-code: export/import, diff, dry-run apply, rollback (SR-CFG-004).

Implements the GitOps-facing half of the layered configuration framework:

* :func:`export_config` — serialize one layer's settings (plus bounds and
  definitions) to a portable, human-reviewable :class:`ConfigArchive`
  (JSON; YAML via ``to_yaml``).
* :func:`import_config` / :func:`apply_archive` — validate an archive and
  apply it to a layer, optionally as a **dry run** (returns the would-be
  change records without writing). Validation covers the JSON Schema of
  each setting and floor/ceiling bounds (SR-CFG-002) — a lower layer
  cannot import a value that loosens an upper-layer bound.
* :func:`diff_configs` — key-by-key diff of two archives (or archive vs.
  live store) producing an added/removed/changed report for GitOps
  promotion (dev → stage → prod is orchestrated by CI; external gate).
* :meth:`ConfigStore.rollback` — restore a setting at a layer to a
  previous version, audited like any other set (SR-CFG-001/004).

Change-approval workflow (SR-CFG-004): archives are plain data; approval
is modeled as an optional ``approved_by`` field on apply that is recorded
in each change record's ``reason``. Full multi-party approval orchestration
is external gate (ADR-gated, governance workflows in §12.3).
"""

from __future__ import annotations

import json
from typing import Any, Literal

import jsonschema
import yaml
from eoip.config.layered import (
    ConfigChangeRecord,
    ConfigStore,
    LayerRef,
    SettingDef,
    new_change_id,
)
from pydantic import BaseModel, ConfigDict, Field

ARCHIVE_FORMAT = "eoip.config-archive/v1"


class ArchiveEntry(BaseModel):
    """One setting value contributed by the archived layer."""

    model_config = ConfigDict(extra="forbid")

    key: str
    value: Any = None
    floor: Any = None
    ceiling: Any = None


class ConfigArchive(BaseModel):
    """Portable export of one layer's configuration (SR-CFG-004)."""

    model_config = ConfigDict(extra="forbid")

    format: str = ARCHIVE_FORMAT
    layer: LayerRef
    definitions: list[SettingDef] = Field(default_factory=list)
    entries: list[ArchiveEntry] = Field(default_factory=list)
    exported_at: str = ""

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_yaml(self) -> str:
        return yaml.safe_dump(json.loads(self.model_dump_json()), sort_keys=False)

    @classmethod
    def from_payload(cls, payload: str | bytes | dict, fmt: Literal["json", "yaml"] = "json") -> ConfigArchive:
        if isinstance(payload, dict):
            data = payload
        else:
            text = payload.decode("utf-8") if isinstance(payload, bytes) else payload
            data = yaml.safe_load(text) if fmt == "yaml" else json.loads(text)
        return cls.model_validate(data)


class DiffEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    status: Literal["added", "removed", "changed", "unchanged"]
    old_value: Any = None
    new_value: Any = None


class ConfigDiff(BaseModel):
    """Key-by-key diff between two configuration snapshots (SR-CFG-004)."""

    model_config = ConfigDict(extra="forbid")

    diff_id: str
    added: list[str] = Field(default_factory=list)
    removed: list[str] = Field(default_factory=list)
    changed: list[DiffEntry] = Field(default_factory=list)
    unchanged: list[str] = Field(default_factory=list)

    @property
    def changed_count(self) -> int:
        return len(self.added) + len(self.removed) + len(self.changed)


def _entries_by_key(archive: ConfigArchive) -> dict[str, ArchiveEntry]:
    return {e.key: e for e in archive.entries}


def diff_configs(a: ConfigArchive, b: ConfigArchive) -> ConfigDiff:
    """Diff archive ``a`` (old) against archive ``b`` (new)."""
    ea, eb = _entries_by_key(a), _entries_by_key(b)
    added = sorted(k for k in eb if k not in ea)
    removed = sorted(k for k in ea if k not in eb)
    changed = [
        DiffEntry(key=k, status="changed", old_value=ea[k].value, new_value=eb[k].value)
        for k in sorted(ea.keys() & eb.keys())
        if ea[k].value != eb[k].value
    ]
    unchanged = sorted(
        k for k in ea.keys() & eb.keys() if ea[k].value == eb[k].value
    )
    return ConfigDiff(
        diff_id=new_change_id(),
        added=added,
        removed=removed,
        changed=changed,
        unchanged=unchanged,
    )


def export_config(store: ConfigStore, layer: LayerRef, *, exported_at: str = "") -> ConfigArchive:
    """Export one layer's settings from the live store (SR-CFG-004)."""
    archive = ConfigArchive(layer=layer, exported_at=exported_at)
    for definition in store.definitions():
        state_key = definition.key
        # only include values actually set at this layer instance
        value = None
        for version in _layer_versions(store, definition.key, layer):
            value = version.value
        floor, ceiling = _layer_bounds(store, definition.key, layer)
        if value is not None or floor is not None or ceiling is not None:
            archive.definitions.append(definition)
            archive.entries.append(
                ArchiveEntry(key=state_key, value=value, floor=floor, ceiling=ceiling)
            )
    return archive


def _layer_versions(store: ConfigStore, key: str, layer: LayerRef) -> list:
    state = store._state(key)
    version = state.versions.get((layer.kind, layer.instance))
    return [version] if version else []


def _layer_bounds(store: ConfigStore, key: str, layer: LayerRef) -> tuple[Any, Any]:
    state = store._state(key)
    loc = (layer.kind, layer.instance)
    return state.floors.get(loc), state.ceilings.get(loc)


def import_config(
    store: ConfigStore,
    payload: str | bytes | dict,
    *,
    fmt: Literal["json", "yaml"] = "json",
    dry_run: bool = False,
    actor: str = "system",
    approved_by: str | None = None,
) -> dict[str, Any]:
    """Import an archive into the store (SR-CFG-004).

    With ``dry_run=True`` nothing is written; the returned report lists
    the change records that *would* be created. Approval workflow: pass
    ``approved_by`` to record the approver on every change (external gate:
    multi-party orchestration).
    """
    archive = ConfigArchive.from_payload(payload, fmt=fmt)
    return apply_archive(
        store,
        archive,
        dry_run=dry_run,
        actor=actor,
        approved_by=approved_by,
    )


def apply_archive(
    store: ConfigStore,
    archive: ConfigArchive,
    *,
    dry_run: bool = False,
    actor: str = "system",
    approved_by: str | None = None,
) -> dict[str, Any]:
    """Validate and apply an archive to its layer. See :func:`import_config`."""
    if archive.format != ARCHIVE_FORMAT:
        raise ValueError(f"unsupported archive format: {archive.format!r}")
    reason = f"config-as-code import (actor={actor})"
    if approved_by:
        reason += f" approved_by={approved_by}"
    applied: list[ConfigChangeRecord] = []
    errors: list[dict[str, str]] = []
    staged: list[tuple[str, Any]] = []
    for entry in archive.entries:
        try:
            definition = _definition_for(store, archive, entry.key)
            definition.validate_value(entry.value)
            staged.append((entry.key, entry.value))
        except KeyError as exc:
            errors.append({"key": entry.key, "error": str(exc)})
        except jsonschema.ValidationError as exc:
            errors.append({"key": entry.key, "error": str(exc)})
    if errors:
        return {"ok": False, "dry_run": dry_run, "applied": [], "errors": errors}
    if not dry_run:
        for key, value in staged:
            try:
                rec = store.set(key, archive.layer, value, actor=actor, reason=reason)
            except ValueError as exc:
                errors.append({"key": key, "error": str(exc)})
                continue
            applied.append(rec)
        if errors:
            return {"ok": False, "dry_run": dry_run, "applied": applied, "errors": errors}
    else:
        for key, value in staged:
            applied.append(
                ConfigChangeRecord(
                    key=key,
                    layer=archive.layer,
                    old_version=0,
                    new_version=1,
                    old_value=None,
                    new_value=value,
                    actor=actor,
                    reason=reason + " [dry-run]",
                )
            )
    return {"ok": True, "dry_run": dry_run, "applied": applied, "errors": []}


def _definition_for(store: ConfigStore, archive: ConfigArchive, key: str) -> SettingDef:
    for definition in archive.definitions:
        if definition.key == key:
            # ensure the key is known to the store
            store._state(key)
            return definition
    state = store._state(key)
    return state.definition


def rollback(
    store: ConfigStore,
    key: str,
    layer: LayerRef,
    to_version: int,
    *,
    actor: str = "system",
) -> ConfigChangeRecord:
    """Restore a setting at a layer to a previous version (SR-CFG-004).

    The rollback itself is a normal audited set, so the audit trail shows
    both the original change and the rollback.
    """
    previous = store.get_version(key, layer, to_version)
    if previous is None:
        raise ValueError(f"no version {to_version} for {key!r} at {layer.kind}/{layer.instance}")
    return store.set(
        key,
        layer,
        previous.value,
        actor=actor,
        reason=f"rollback to version {to_version} ({previous.version_id})",
    )
