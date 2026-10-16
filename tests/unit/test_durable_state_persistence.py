"""Unit tests for durable multi-replica state persistence (CP-03).

Verifies disk-backed atomic persistence and restart reload for:
- RoleRegistry
- UserStore
- FileConfigPersistence & ConfigStore
- ThemeRegistry
"""

from __future__ import annotations

from pathlib import Path

from eoip.authz.core import RoleRegistry, UserStore
from eoip.branding.theme import ThemePackage, ThemeRegistry
from eoip.config.layered import (
    ConfigStore,
    FeatureFlag,
    FeatureFlagStore,
    FileConfigPersistence,
    LayerRef,
    SettingDef,
    SettingScope,
)


def test_role_registry_file_persistence(tmp_path: Path):
    path = tmp_path / "roles.json"
    reg1 = RoleRegistry(storage_path=path)

    # Built-ins are present
    assert reg1.get_role("admin") is not None

    # Create custom role
    reg1.create_role(
        "custom_auditor",
        description="Auditor role",
        permissions=["graph:read"],
    )
    assert path.exists()

    # Second instance reloading from disk
    reg2 = RoleRegistry(storage_path=path)
    auditor = reg2.get_role("custom_auditor")
    assert auditor is not None
    assert auditor["description"] == "Auditor role"
    assert "graph:read" in auditor["permissions"]

    # Update role
    reg2.update_role("custom_auditor", description="Updated auditor description")
    reg3 = RoleRegistry(storage_path=path)
    assert reg3.get_role("custom_auditor")["description"] == "Updated auditor description"

    # Delete custom role
    reg3.delete_role("custom_auditor")
    reg4 = RoleRegistry(storage_path=path)
    assert reg4.get_role("custom_auditor") is None


def test_user_store_file_persistence(tmp_path: Path):
    path = tmp_path / "users.json"
    store1 = UserStore(storage_path=path)

    # Create user
    store1.create_user("user_persist_1", roles=["analyst"], attributes={"dept": "finance"})
    assert path.exists()

    # Second instance reloading from disk
    store2 = UserStore(storage_path=path)
    user = store2.get_user("user_persist_1")
    assert user is not None
    assert user.roles == ["analyst"]
    assert user.attributes.get("dept") == "finance"

    # Update user
    store2.update_user("user_persist_1", roles=["analyst", "steward"])
    store3 = UserStore(storage_path=path)
    user_reloaded = store3.get_user("user_persist_1")
    assert user_reloaded.roles == ["analyst", "steward"]

    # Delete user
    store3.delete_user("user_persist_1")
    store4 = UserStore(storage_path=path)
    assert store4.get_user("user_persist_1") is None


def test_config_store_file_persistence(tmp_path: Path):
    path = tmp_path / "config.json"
    persistence1 = FileConfigPersistence(path)
    store1 = ConfigStore(persistence=persistence1)

    sdef = SettingDef(
        key="app.timeout",
        schema={"type": "integer", "minimum": 1},
        default=30,
        description="Request timeout",
    )
    store1.register(sdef)
    tenant_layer = LayerRef(kind="tenant", instance="tenant_alpha")
    store1.set("app.timeout", tenant_layer, 60, actor="test_admin")

    # Add a feature flag via FeatureFlagStore
    flags1 = FeatureFlagStore(store1)
    flag = FeatureFlag(key="feature.beta", enabled=True, description="Beta flag")
    flags1.register(flag)
    assert path.exists()

    # Second instance reloading from disk
    persistence2 = FileConfigPersistence(path)
    store2 = ConfigStore(persistence=persistence2)
    flags2 = FeatureFlagStore(store2)

    # The registered setting and flag should be restored
    assert "app.timeout" in [d.key for d in store2.definitions()]
    scope = SettingScope(tenant="tenant_alpha")
    explain = store2.explain("app.timeout", scope)
    assert explain.effective.value == 60
    assert flags2.get("feature.beta").enabled is True


def test_theme_registry_file_persistence(tmp_path: Path):
    path = tmp_path / "themes.json"
    default_pkg = ThemePackage(
        id="urn:eoip:branding:theme:default",
        name="Default Theme",
        app_name="EOIP Default",
    )
    custom_pkg = ThemePackage(
        id="urn:eoip:branding:theme:acme-dark",
        name="Acme Dark",
        app_name="Acme Portal",
    )
    reg1 = ThemeRegistry(default_theme=default_pkg, storage_path=path)
    reg1.register(custom_pkg)
    reg1.assign("acme_tenant", custom_pkg.id)
    assert path.exists()

    # Second instance reloading from disk
    reg2 = ThemeRegistry(storage_path=path)
    resolved = reg2.resolve("acme_tenant")
    assert resolved.id == custom_pkg.id
    assert resolved.app_name == "Acme Portal"
