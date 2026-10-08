"""Layered configuration framework (SR-CFG-001..006, super-requirements §12.3).

This package was converted from the legacy ``eoip.config`` module into a
package; the legacy YAML policy loaders are preserved in
:mod:`eoip.config._yaml` and re-exported here, so existing imports
(``from eoip.config import load_query_policy``) keep working unchanged.

Submodules:

* :mod:`eoip.config.layered` — layer model, typed settings, layered store,
  floors/ceilings (SR-CFG-001/002), effective-config explain (SR-CFG-003),
  feature flags (SR-CFG-005), hot reload (SR-CFG-006).
* :mod:`eoip.config.ascode` — config-as-code export/import/diff/dry-run/
  rollback (SR-CFG-004).
* :mod:`eoip.config.router` — ``build_router(store)`` FastAPI factory
  (lazy import; wired under ``/api/v1/config/*`` by apps/api).

Persistence is in-process and pluggable: the store accepts a
``ConfigPersistence`` port. The default ``MemoryPersistence`` keeps the
framework dependency-free; a relational/raft-backed persistence is an
external gate (ADR-gated, see super-requirements §12.3 storage bindings).
"""

from __future__ import annotations

from eoip.config._yaml import load_agent_config, load_memory_policy, load_query_policy
from eoip.config.ascode import ConfigArchive, apply_archive, diff_configs, export_config, import_config
from eoip.config.layered import (
    LAYERS,
    SECURE_SETTING_MARKERS,
    ConfigChangeRecord,
    ConfigStore,
    EffectiveSetting,
    ExplainResult,
    FeatureFlag,
    FeatureFlagStore,
    HotReloadHandle,
    LayerRef,
    SettingDef,
    SettingScope,
    new_change_id,
    new_setting_id,
    new_version_id,
)

__all__ = [
    "LAYERS",
    "SECURE_SETTING_MARKERS",
    "ConfigArchive",
    "ConfigChangeRecord",
    "ConfigStore",
    "EffectiveSetting",
    "ExplainResult",
    "FeatureFlag",
    "FeatureFlagStore",
    "HotReloadHandle",
    "LayerRef",
    "SettingDef",
    "SettingScope",
    "apply_archive",
    "diff_configs",
    "export_config",
    "import_config",
    "load_agent_config",
    "load_memory_policy",
    "load_query_policy",
    "new_change_id",
    "new_setting_id",
    "new_version_id",
]
