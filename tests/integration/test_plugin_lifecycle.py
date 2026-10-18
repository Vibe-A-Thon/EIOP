"""Integration tests for plugin lifecycle, scoped state, migrations, and clean uninstall (CRA-002.5, CRA-002.6)."""

import tempfile
from pathlib import Path
import pytest

from eoip.plugins.manifest import PluginUninstallPolicy
from eoip.plugins.state import PluginStateRepository
from eoip.graph.backends import backend_capabilities, ensure_default_backends, create_graph_store
from eoip.graph.rdf_backend import FusekiGraphStore, GraphDBGraphStore


@pytest.fixture
def state_repo():
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_file = Path(tmp_dir) / "plugin_state.json"
        yield PluginStateRepository(repo_file)


def test_scoped_state_and_cross_tenant_isolation(state_repo):
    """CRA-002.5: Plugin state is strictly scoped by tenant and workspace."""
    # Tenant 1 writes state
    state_repo.set_state("tenant_alpha", "ws_main", "plugin.analytics", "counter", 42)
    # Tenant 2 writes state with same plugin and key
    state_repo.set_state("tenant_beta", "ws_main", "plugin.analytics", "counter", 999)

    # Isolated reads
    assert state_repo.get_state("tenant_alpha", "ws_main", "plugin.analytics", "counter") == 42
    assert state_repo.get_state("tenant_beta", "ws_main", "plugin.analytics", "counter") == 999

    # Tenant 1 cannot access tenant 2's workspace
    assert state_repo.get_state("tenant_alpha", "ws_other", "plugin.analytics", "counter") is None


def test_disable_plugin_revokes_permissions_and_blocks_mutation(state_repo):
    """CRA-002.5: Disable revokes permissions and stops modifications."""
    state_repo.set_state("tenant_alpha", "ws_1", "plugin.jira", "synced_issues", 15)
    assert state_repo.get_state("tenant_alpha", "ws_1", "plugin.jira", "synced_issues") == 15

    # Disable plugin
    state_repo.disable_plugin("tenant_alpha", "ws_1", "plugin.jira")

    # Read returns None when disabled
    assert state_repo.get_state("tenant_alpha", "ws_1", "plugin.jira", "synced_issues") is None

    # Mutation raises PermissionError
    with pytest.raises(PermissionError):
        state_repo.set_state("tenant_alpha", "ws_1", "plugin.jira", "synced_issues", 20)


def test_schema_migration_history(state_repo):
    """CRA-002.5: Versioned schema migrations preserve and transform owned state."""
    state_repo.register_plugin("tenant_alpha", "ws_1", "plugin.mapper", "1.0.0")
    state_repo.set_state("tenant_alpha", "ws_1", "plugin.mapper", "legacy_field", "value_v1")

    def migration_v1_to_v2(data: dict) -> dict:
        new_data = dict(data)
        new_data["modern_field"] = f"v2_{new_data.pop('legacy_field')}"
        return new_data

    state_repo.apply_migration("tenant_alpha", "ws_1", "plugin.mapper", "2.0.0", migration_v1_to_v2)

    assert state_repo.get_state("tenant_alpha", "ws_1", "plugin.mapper", "legacy_field") is None
    assert state_repo.get_state("tenant_alpha", "ws_1", "plugin.mapper", "modern_field") == "v2_value_v1"

    entry = state_repo._entries[("tenant_alpha", "ws_1", "plugin.mapper")]
    assert entry.version == "2.0.0"
    assert len(entry.migration_history) == 1
    assert entry.migration_history[0]["from_version"] == "1.0.0"
    assert entry.migration_history[0]["to_version"] == "2.0.0"


def test_uninstall_policies(state_repo):
    """CRA-002.5: Uninstall handles retention, delete, and archive cleanly."""
    # Test DELETE policy
    state_repo.set_state("t1", "w1", "p.del", "data", "confidential")
    state_repo.uninstall_plugin("t1", "w1", "p.del", PluginUninstallPolicy(retention="delete"))
    assert ("t1", "w1", "p.del") not in state_repo._entries

    # Test ARCHIVE policy
    state_repo.set_state("t1", "w1", "p.arch", "data", "audit_record")
    state_repo.uninstall_plugin("t1", "w1", "p.arch", PluginUninstallPolicy(retention="archive"))
    arch_entry = state_repo._entries[("t1", "w1", "p.arch")]
    assert arch_entry.enabled is False
    assert arch_entry.state_data.get("_archived") is True


def test_engine_replacement_without_altering_domain_contract(monkeypatch):
    """CRA-002.6, CRA-002.10: Replacing graph backend preserves domain operations."""
    ensure_default_backends()
    caps = backend_capabilities()

    # RDF store backend capabilities registered
    assert "fuseki" in caps
    assert "graphdb" in caps
    assert "SPARQL" in caps["fuseki"]["query_languages"]
    assert "rdf" in caps["fuseki"]["models"]

    # GraphStore domain protocol operations work on Fuseki adapter without altering API
    fuseki_store = FusekiGraphStore()
    v = fuseki_store.upsert_vertex("Entity", {"canonical_id": "ent:123", "name": "TestEntity"})
    assert v["canonical_id"] == "ent:123"

    v_retrieved = fuseki_store.get_vertex("ent:123")
    assert v_retrieved is not None
    assert v_retrieved["properties"]["name"] == "TestEntity"

    e = fuseki_store.upsert_edge("connectsTo", "ent:123", "ent:456", {"weight": 1.0})
    assert e["label"] == "connectsTo"
    assert fuseki_store.count_edges() == 1
