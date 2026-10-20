"""Layered configuration store (SR-CFG-001, SR-CFG-002, SR-CFG-003,
SR-CFG-005, SR-CFG-006).

Implements the seven-layer configuration hierarchy from super-requirements
§12.1/§12.3:

    product-default → edition → partner → tenant → business-unit →
    workspace → user

Each *setting* is a key/value pair scoped to one layer instance (a
``LayerRef``: layer kind + instance id, e.g. ``tenant=acme``). Every
setting is typed via a JSON Schema document attached to its
:class:`SettingDef`, validated on write, versioned (monotonic version per
setting, previous versions retained), and audited (one
:class:`ConfigChangeRecord` per successful ``set``).

Floors and ceilings (SR-CFG-002): a setting definition may carry
``floor`` / ``ceiling`` bounds. Any layer write is clamped/rejected so
lower layers cannot loosen an upper layer's bound. For numeric security
settings the *most restrictive* bound across all defined layers wins;
which direction is "restrictive" is declared per setting via
:func:`SettingDef.restrictive_direction`. Floors/ceilings set at a given
layer are inherited by all lower layers.

Effective-config explain (SR-CFG-003): :meth:`ConfigStore.explain` walks
the layer chain for a key, lists every layer's contribution (or absence),
applies precedence (highest layer wins) and floor/ceiling clamping, and
reports the last change record.

Feature flags (SR-CFG-005) live in :class:`FeatureFlagStore` — separate
namespace, distinct URN area, no schema layering; flags never bypass
policy: the store only models flag state, policy enforcement stays in
``eoip.authz`` (External gate: wiring of flag checks into the AuthZ PEP).

Hot reload (SR-CFG-006): non-structural settings (``structural=False``
on the definition) can be subscribed to via :meth:`ConfigStore.hot_reload`;
subscribers are notified synchronously on change. Structural settings
(backend bindings, ontology major versions) are marked structural and are
excluded from hot reload — runtime migration of those is ADR-gated.

Persistence port: :class:`ConfigPersistence`. The default
:class:`MemoryPersistence` is in-process; durable shared persistence is
an external gate (ADR-gated, super-requirements §12.3 storage bindings).
"""

from __future__ import annotations

import json
import threading
import uuid
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import UTC
from pathlib import Path
from typing import Any, Literal, Protocol

import jsonschema
from pydantic import BaseModel, ConfigDict, Field

LayerKind = Literal[
    "product-default",
    "edition",
    "partner",
    "tenant",
    "business-unit",
    "workspace",
    "user",
]

#: Canonical precedence order, lowest (widest) first. Higher layers win.
LAYERS: tuple[LayerKind, ...] = (
    "product-default",
    "edition",
    "partner",
    "tenant",
    "business-unit",
    "workspace",
    "user",
)

#: Setting keys containing these markers are treated as security-relevant
#: for most-restrictive-wins resolution (SR-CFG-002).
SECURE_SETTING_MARKERS: tuple[str, ...] = (
    "security",
    "auth",
    "egress",
    "privacy",
    "compliance",
    "encryption",
    "retention",
)


def _urn(area: str, type_: str) -> str:
    return f"urn:eoip:{area}:{type_}:{uuid.uuid4()}"


def new_setting_id() -> str:
    return _urn("config", "setting")


def new_change_id() -> str:
    return _urn("config", "change")


def new_version_id() -> str:
    return _urn("config", "version")


class LayerRef(BaseModel):
    """One layer instance in the hierarchy, e.g. tenant=acme."""

    model_config = ConfigDict(extra="forbid")

    kind: LayerKind
    instance: str = Field(default="default", description="Layer instance id (tenant slug, user id, ...)")


class SettingScope(BaseModel):
    """Optional scoping of a setting to a domain/tenant subtree (SR-TEN-001)."""

    model_config = ConfigDict(extra="forbid")

    tenant: str | None = None
    business_unit: str | None = None
    workspace: str | None = None


class SettingDef(BaseModel):
    """Typed setting definition (SR-CFG-001).

    ``schema`` is a JSON Schema document validated with ``jsonschema``.
    ``floor`` / ``ceiling`` bound the value; whether the floor is a
    minimum or maximum depends on ``restrictive_direction``:

    * ``"high"`` — higher values are more permissive (e.g. token TTL,
      max results). Floor = minimum allowed, ceiling = maximum allowed;
      the *most restrictive* value is the smallest.
    * ``"low"`` — lower values are more permissive (e.g. log verbosity,
      data retention days where less retention is stricter per policy;
      more commonly: minimum required strength). The most restrictive
      value is the largest.
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    key: str
    description: str = ""
    domain: str = "general"
    json_schema: dict[str, Any] = Field(
        default_factory=lambda: {"type": "string"},
        alias="schema",
        description="JSON Schema document for values (serialized as 'schema')",
    )
    default: Any = None
    structural: bool = False
    floor: Any = None
    ceiling: Any = None
    restrictive_direction: Literal["high", "low"] = "high"
    scope: SettingScope = Field(default_factory=SettingScope)

    @property
    def security_relevant(self) -> bool:
        lowered = self.key.lower()
        return any(marker in lowered for marker in SECURE_SETTING_MARKERS)

    def validate_value(self, value: Any) -> None:
        jsonschema.validate(value, self.json_schema)

    def clamp(self, value: Any) -> Any:
        """Apply floor/ceiling bounds (most-restrictive-wins, SR-CFG-002)."""
        if self.floor is None and self.ceiling is None:
            return value
        if self.floor is not None and value < self.floor:
            return self.floor
        if self.ceiling is not None and value > self.ceiling:
            return self.ceiling
        return value

    def violates_bound(self, value: Any) -> str | None:
        """Return a reason string if ``value`` is outside floor/ceiling."""
        if self.floor is not None and value < self.floor:
            return f"value {value!r} below floor {self.floor!r}"
        if self.ceiling is not None and value > self.ceiling:
            return f"value {value!r} above ceiling {self.ceiling!r}"
        return None

    def most_restrictive_floor(self, a: Any, b: Any) -> Any:
        """Merge two floors: for ``low`` direction a *higher* floor is more
        restrictive (e.g. minimum password length); for ``high`` a lower
        floor is more restrictive."""
        if self.restrictive_direction == "low":
            return max(a, b)
        return min(a, b)

    def most_restrictive_ceiling(self, a: Any, b: Any) -> Any:
        if self.restrictive_direction == "low":
            return max(a, b)
        return min(a, b)


class ConfigVersion(BaseModel):
    """One immutable version of a setting value (SR-CFG-001)."""

    model_config = ConfigDict(extra="forbid")

    version_id: str
    version: int
    layer: LayerRef
    value: Any
    change_id: str
    observed_at: str


class ConfigChangeRecord(BaseModel):
    """Audit record for one successful set operation (SR-CFG-001)."""

    model_config = ConfigDict(extra="forbid")

    change_id: str = Field(default_factory=new_change_id)
    key: str
    layer: LayerRef
    old_version: int
    new_version: int
    old_value: Any = None
    new_value: Any = None
    actor: str = "system"
    observed_at: str = ""
    reason: str = ""


class EffectiveSetting(BaseModel):
    """The resolved value of one key at a scope (SR-CFG-001/003)."""

    model_config = ConfigDict(extra="forbid")

    key: str
    value: Any = None
    layer: LayerRef | None = None
    version: int = 0
    change_id: str | None = None
    clamped: bool = False
    structural: bool = False


class LayerContribution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    layer: LayerRef
    present: bool
    version: int = 0
    value: Any = None
    change_id: str | None = None
    floor: Any = None
    ceiling: Any = None


class ExplainResult(BaseModel):
    """Layer-chain trace for one key (SR-CFG-003)."""

    model_config = ConfigDict(extra="forbid")

    key: str
    scope: SettingScope
    effective: EffectiveSetting
    chain: list[LayerContribution]
    last_change: ConfigChangeRecord | None = None


class FeatureFlag(BaseModel):
    """Feature flag — distinct from configuration (SR-CFG-005).

    Flags are simple on/off (or multi-variant) toggles with an owner and
    description; they carry no JSON Schema layering and never bypass
    policy — enforcement hooks live in ``eoip.authz`` (external gate).
    """

    model_config = ConfigDict(extra="forbid")

    flag_id: str = Field(default_factory=lambda: _urn("feature-flag", "flag"))
    key: str
    enabled: bool = False
    variants: dict[str, Any] = Field(default_factory=dict)
    owner: str = ""
    description: str = ""
    never_bypasses_policy: Literal[True] = True


# ---------------------------------------------------------------------------
# Persistence port
# ---------------------------------------------------------------------------


class ConfigPersistence(Protocol):
    """Persistence port for the config store (external gate: durable impl)."""

    def save_snapshot(self, snapshot: dict[str, Any]) -> None: ...

    def load_snapshot(self) -> dict[str, Any]: ...


class MemoryPersistence:
    """In-process persistence (default)."""

    def __init__(self) -> None:
        self._snapshot: dict[str, Any] = {}

    def save_snapshot(self, snapshot: dict[str, Any]) -> None:
        self._snapshot = json.loads(json.dumps(snapshot))

    def load_snapshot(self) -> dict[str, Any]:
        return json.loads(json.dumps(self._snapshot))


class FileConfigPersistence:
    """Atomic filesystem persistence for layered configuration (CP-03)."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def save_snapshot(self, snapshot: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)
        tmp.replace(self.path)

    def load_snapshot(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


@dataclass
class _SettingState:
    definition: SettingDef
    versions: dict[tuple[str, str], ConfigVersion] = field(default_factory=dict)  # (kind, instance) -> current
    history: dict[tuple[str, str], list[ConfigVersion]] = field(default_factory=dict)
    changes: list[ConfigChangeRecord] = field(default_factory=list)
    floors: dict[tuple[str, str], Any] = field(default_factory=dict)  # bound set at layer
    ceilings: dict[tuple[str, str], Any] = field(default_factory=dict)


def _utcnow() -> str:
    from datetime import datetime

    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class ConfigStore:
    """Layered, typed, versioned, audited configuration store."""

    def __init__(
        self,
        persistence: ConfigPersistence | None = None,
        *,
        auto_restore: bool = True,
    ) -> None:
        self._settings: dict[str, _SettingState] = {}
        self._flags: dict[str, FeatureFlag] = {}
        self._flag_changes: list[dict[str, Any]] = []
        self._persistence = persistence or MemoryPersistence()
        self._lock = threading.RLock()
        self._subscribers: dict[str, list[Callable[[EffectiveSetting], None]]] = {}
        if auto_restore and persistence is not None:
            self.restore()

    # -- setting definitions -------------------------------------------

    def register(self, definition: SettingDef) -> None:
        with self._lock:
            self._settings[definition.key] = _SettingState(definition=definition)
            self._persist()

    def definitions(self) -> list[SettingDef]:
        return [s.definition for s in self._settings.values()]

    def _state(self, key: str) -> _SettingState:
        if key not in self._settings:
            raise KeyError(f"unknown setting: {key}")
        return self._settings[key]

    # -- layer chain -----------------------------------------------------

    def scope_layers(self, scope: SettingScope) -> list[LayerRef]:
        """Resolve the layer chain for a scope, lowest first."""
        chain: list[LayerRef] = [LayerRef(kind="product-default", instance="default")]
        if scope.tenant:
            chain.append(LayerRef(kind="tenant", instance=scope.tenant))
            if scope.business_unit:
                chain.append(LayerRef(kind="business-unit", instance=scope.business_unit))
                if scope.workspace:
                    chain.append(LayerRef(kind="workspace", instance=scope.workspace))
        if scope.tenant is None:
            return chain
        # user layer is resolved by callers passing a user-scoped scope
        return chain

    def user_layer(self, user_id: str) -> LayerRef:
        return LayerRef(kind="user", instance=user_id)

    def chain_for(self, scope: SettingScope, user_id: str | None = None) -> list[LayerRef]:
        chain = self.scope_layers(scope)
        if user_id:
            chain.append(LayerRef(kind="user", instance=user_id))
        return chain

    # -- bounds (SR-CFG-002) ---------------------------------------------

    def set_bound(
        self,
        key: str,
        layer: LayerRef,
        *,
        floor: Any = None,
        ceiling: Any = None,
        actor: str = "system",
    ) -> ConfigChangeRecord:
        """Set a floor/ceiling at a layer; lower layers cannot loosen it."""
        with self._lock:
            state = self._state(key)
            old_floor = state.floors.get((layer.kind, layer.instance))
            old_ceiling = state.ceilings.get((layer.kind, layer.instance))
            state.floors[(layer.kind, layer.instance)] = floor
            state.ceilings[(layer.kind, layer.instance)] = ceiling
            rec = ConfigChangeRecord(
                key=key,
                layer=layer,
                old_version=-1,
                new_version=-1,
                old_value={"floor": old_floor, "ceiling": old_ceiling},
                new_value={"floor": floor, "ceiling": ceiling},
                actor=actor,
                observed_at=_utcnow(),
                reason="bound-change",
            )
            state.changes.append(rec)
            self._persist()
            return rec

    def effective_bounds(self, key: str, chain: Iterable[LayerRef]) -> tuple[Any, Any]:
        """Most-restrictive floor and ceiling over the chain (SR-CFG-002)."""
        state = self._state(key)
        definition = state.definition
        kinds = {layer.kind for layer in chain}
        floor = definition.floor
        ceiling = definition.ceiling
        for (kind, _instance), bound in state.floors.items():
            if kind in kinds and bound is not None:
                floor = bound if floor is None else definition.most_restrictive_floor(floor, bound)
        for (kind, _instance), bound in state.ceilings.items():
            if kind in kinds and bound is not None:
                ceiling = bound if ceiling is None else definition.most_restrictive_ceiling(ceiling, bound)
        return floor, ceiling

    # -- writes ----------------------------------------------------------

    def set(
        self,
        key: str,
        layer: LayerRef,
        value: Any,
        *,
        actor: str = "system",
        reason: str = "",
    ) -> ConfigChangeRecord:
        """Write a setting value at a layer. Validates schema and bounds.

        Raises ``jsonschema.ValidationError`` on schema mismatch and
        ``ValueError`` on floor/ceiling violation (SR-CFG-002).
        """
        with self._lock:
            state = self._state(key)
            definition = state.definition
            definition.validate_value(value)
            idx = LAYERS.index(layer.kind)
            chain = [LayerRef(kind=k, instance=layer.instance) for k in LAYERS[: idx + 1]]
            floor, ceiling = self.effective_bounds(key, chain)
            probe = definition.model_copy(update={"floor": floor, "ceiling": ceiling})
            violation = probe.violates_bound(value)
            if violation:
                raise ValueError(
                    f"setting {key!r} at layer {layer.kind}/{layer.instance} violates "
                    f"bound from an upper layer (most-restrictive-wins): {violation}"
                )
            loc = (layer.kind, layer.instance)
            current = state.versions.get(loc)
            new_version = (current.version if current else 0) + 1
            change = ConfigChangeRecord(
                key=key,
                layer=layer,
                old_version=current.version if current else 0,
                new_version=new_version,
                old_value=current.value if current else None,
                new_value=value,
                actor=actor,
                observed_at=_utcnow(),
                reason=reason,
            )
            version = ConfigVersion(
                version_id=new_version_id(),
                version=new_version,
                layer=layer,
                value=value,
                change_id=change.change_id,
                observed_at=change.observed_at,
            )
            state.versions[loc] = version
            state.history.setdefault(loc, []).append(version)
            state.changes.append(change)
            self._persist()
            self._notify(
                key,
                EffectiveSetting(
                    key=key,
                    value=value,
                    layer=layer,
                    version=new_version,
                    change_id=change.change_id,
                    structural=definition.structural,
                ),
            )
            return change

    # -- reads -----------------------------------------------------------

    def get(
        self,
        key: str,
        scope: SettingScope | None = None,
        *,
        user_id: str | None = None,
    ) -> EffectiveSetting:
        return self.explain(key, scope or SettingScope(), user_id=user_id).effective

    def explain(
        self,
        key: str,
        scope: SettingScope | None = None,
        *,
        user_id: str | None = None,
    ) -> ExplainResult:
        """Layer-chain trace for one key (SR-CFG-003)."""
        with self._lock:
            state = self._state(key)
            definition = state.definition
            scope = scope or SettingScope()
            chain = self.chain_for(scope, user_id=user_id)
            contributions: list[LayerContribution] = []
            winner: ConfigVersion | None = None
            winner_layer: LayerRef | None = None
            floor, ceiling = self.effective_bounds(key, chain)
            for layer in chain:
                loc = (layer.kind, layer.instance)
                version = state.versions.get(loc)
                present = version is not None
                contributions.append(
                    LayerContribution(
                        layer=layer,
                        present=present,
                        version=version.version if version else 0,
                        value=version.value if version else None,
                        change_id=version.change_id if version else None,
                        floor=state.floors.get(loc),
                        ceiling=state.ceilings.get(loc),
                    )
                )
                if present:
                    winner = version
                    winner_layer = layer
            value = winner.value if winner else definition.default
            clamped = False
            if winner is not None and (floor is not None or ceiling is not None):
                probe = definition.model_copy(update={"floor": floor, "ceiling": ceiling})
                clamped_value = probe.clamp(value)
                clamped = clamped_value != value
                value = clamped_value
            last_change = state.changes[-1] if state.changes else None
            return ExplainResult(
                key=key,
                scope=scope,
                effective=EffectiveSetting(
                    key=key,
                    value=value,
                    layer=winner_layer,
                    version=winner.version if winner else 0,
                    change_id=winner.change_id if winner else None,
                    clamped=clamped,
                    structural=definition.structural,
                ),
                chain=contributions,
                last_change=last_change,
            )

    def audit_trail(self, key: str) -> list[ConfigChangeRecord]:
        with self._lock:
            return list(self._state(key).changes)

    def get_version(self, key: str, layer: LayerRef, version: int) -> ConfigVersion | None:
        with self._lock:
            state = self._state(key)
            for v in state.history.get((layer.kind, layer.instance), []):
                if v.version == version:
                    return v
            return None

    # -- hot reload (SR-CFG-006) -----------------------------------------

    def hot_reload(self, key: str, callback: Callable[[EffectiveSetting], None]) -> HotReloadHandle:
        """Subscribe to non-structural changes of ``key`` (SR-CFG-006)."""
        state = self._state(key)
        if state.definition.structural:
            raise ValueError(
                f"setting {key!r} is structural; changes require a migration plan "
                "(SR-CFG-006, ADR-gated)"
            )
        with self._lock:
            self._subscribers.setdefault(key, []).append(callback)

        def unsubscribe() -> None:
            with self._lock:
                subs = self._subscribers.get(key, [])
                if callback in subs:
                    subs.remove(callback)

        return HotReloadHandle(key=key, unsubscribe=unsubscribe)

    def _notify(self, key: str, effective: EffectiveSetting) -> None:
        for callback in self._subscribers.get(key, []):
            callback(effective)

    # -- persistence -------------------------------------------------------

    def _persist(self) -> None:
        snapshot = {
            "settings": {
                key: {
                    "definition": state.definition.model_dump(),
                    "versions": {f"{k[0]}|{k[1]}": v.model_dump() for k, v in state.versions.items()},
                    "history": {
                        f"{k[0]}|{k[1]}": [v.model_dump() for v in vs]
                        for k, vs in state.history.items()
                    },
                    "changes": [c.model_dump() for c in state.changes],
                    "floors": {f"{k[0]}|{k[1]}": v for k, v in state.floors.items()},
                    "ceilings": {f"{k[0]}|{k[1]}": v for k, v in state.ceilings.items()},
                }
                for key, state in self._settings.items()
            },
            "flags": {k: f.model_dump() for k, f in self._flags.items()},
        }
        self._persistence.save_snapshot(snapshot)

    def restore(self) -> None:
        """Load state from the persistence port (hot-restart recovery)."""
        snapshot = self._persistence.load_snapshot()
        with self._lock:
            for key, data in snapshot.get("settings", {}).items():
                state = _SettingState(definition=SettingDef.model_validate(data["definition"]))
                state.versions = {
                    _split_loc(k): ConfigVersion.model_validate(v) for k, v in data["versions"].items()
                }
                state.history = {
                    _split_loc(k): [ConfigVersion.model_validate(x) for x in vs]
                    for k, vs in data["history"].items()
                }
                state.changes = [ConfigChangeRecord.model_validate(c) for c in data["changes"]]
                state.floors = {_split_loc(k): v for k, v in data["floors"].items()}
                state.ceilings = {_split_loc(k): v for k, v in data["ceilings"].items()}
                self._settings[key] = state
            self._flags = {k: FeatureFlag.model_validate(f) for k, f in snapshot.get("flags", {}).items()}


def _split_loc(k: str) -> tuple[str, str]:
    kind, _, instance = k.partition("|")
    return (kind, instance)


class HotReloadHandle(BaseModel):
    """Subscription handle for non-structural hot reload (SR-CFG-006)."""

    model_config = ConfigDict(extra="forbid")

    key: str
    unsubscribe: Callable[[], None] = Field(exclude=True)

    def close(self) -> None:
        self.unsubscribe()


# ---------------------------------------------------------------------------
# Feature flags (SR-CFG-005)
# ---------------------------------------------------------------------------


class FeatureFlagStore:
    """Feature flags, distinct from configuration (SR-CFG-005).

    Flags never bypass policy: toggling a flag has no effect on AuthZ
    decisions here; the AuthZ PEP consults flags through an explicit
    external gate (wiring in apps/api, ADR-gated).
    """

    def __init__(self, config_store: ConfigStore | None = None) -> None:
        self._config = config_store
        self._flags: dict[str, FeatureFlag] = {}
        if config_store and hasattr(config_store, "_flags") and config_store._flags:
            self._flags.update(config_store._flags)
        self._changes: list[dict[str, Any]] = []

    def register(self, flag: FeatureFlag) -> None:
        self._flags[flag.key] = flag
        if self._config is not None:
            self._config._flags[flag.key] = flag
            self._config._persist()

    def set(self, key: str, enabled: bool, *, actor: str = "system") -> FeatureFlag:
        flag = self._flags[key]
        self._changes.append(
            {"key": key, "old": flag.enabled, "new": enabled, "actor": actor, "at": _utcnow()}
        )
        flag.enabled = enabled
        if self._config is not None:
            self._config._flags[key] = flag
            self._config._persist()
        return flag

    def get(self, key: str) -> FeatureFlag:
        return self._flags[key]

    def is_active(self, key: str, *, policy_allows: bool) -> bool:
        """A flag can only narrow what policy already allows (SR-CFG-005).

        Callers must pass the policy decision for the action the flag gates; the result is
        ``policy_allows and flag.enabled``. An unknown flag is inactive. There is no code path where
        an enabled flag turns a policy denial into an allow.
        """
        if not isinstance(policy_allows, bool):
            raise TypeError("policy_allows must be the boolean policy decision")
        flag = self._flags.get(key)
        return bool(policy_allows and flag is not None and flag.enabled)

    def list(self) -> list[FeatureFlag]:
        return list(self._flags.values())

    def history(self, key: str) -> list[dict[str, Any]]:
        return [c for c in self._changes if c["key"] == key]
