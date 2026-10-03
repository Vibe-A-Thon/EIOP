"""Self-contained local configuration and model-weight recovery."""

import hashlib
import json
import runpy
import sys
import zipfile

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.recovery_bundle import backup_bundle, restore_bundle
from eoip.snapshot import digest

from scripts.verify_restore import select_snapshot, verify_restored_bundle


def assets(root):
    config = root / "config"
    config.mkdir(parents=True)
    (config / "memory-policy.yaml").write_text("schema_version: '1.0'\nttl_seconds: 60\n")
    models = root / "models"
    weights = b"offline-model-weights" * 1000
    sha = hashlib.sha256(weights).hexdigest()
    blob = models / "blobs" / f"sha256-{sha}"
    blob.parent.mkdir(parents=True)
    blob.write_bytes(weights)
    manifest = models / "manifests" / "registry.ollama.ai" / "library" / "demo" / "latest"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps({
        "schemaVersion": 2, "config": {"digest": f"sha256:{sha}", "size": len(weights)},
        "layers": [{"digest": f"sha256:{sha}", "size": len(weights)}],
    }))
    return config, models, blob


def make_bundle(tmp_path):
    config, models, blob = assets(tmp_path / "source")
    graph = MemoryGraphStore()
    graph.upsert_vertex("WorkItem", {"canonical_id": "test:bundle", "issue_key": "BUNDLE-1"})
    bundle = tmp_path / "backup.zip"
    backup_bundle(graph, tmp_path / "source" / "data", bundle, config_dir=config, model_dir=models)
    return bundle, config, models, blob


@pytest.mark.req("NFR-REL-002", "G2-REL-007")
def test_bundle_restores_actual_weights_configuration_and_graph(tmp_path):
    bundle, config, models, blob = make_bundle(tmp_path)
    target = tmp_path / "restored"
    graph = MemoryGraphStore()
    result = restore_bundle(
        graph, target / "data", bundle, config_dir=target / "config", model_dir=target / "models",
    )
    assert result["vertices"] == 1
    assert (target / "config" / "memory-policy.yaml").read_bytes() == (
        config / "memory-policy.yaml"
    ).read_bytes()
    assert (target / "models" / blob.relative_to(models)).read_bytes() == blob.read_bytes()
    assert graph.get_vertex_by_canonical_id("test:bundle") is not None


@pytest.mark.parametrize("failure", ["checksum", "traversal", "duplicate", "unsupported", "graph"])
def test_invalid_bundle_refused_before_graph_or_destination_writes(tmp_path, failure):
    bundle, _, _, _ = make_bundle(tmp_path)
    with zipfile.ZipFile(bundle) as archive:
        entries = {info.filename: archive.read(info) for info in archive.infolist()}
    manifest = json.loads(entries["bundle.json"])
    blob_name = next(name for name in entries if name.startswith("models/blobs/"))
    if failure == "checksum":
        entries[blob_name] = b"corrupt"
    elif failure == "traversal":
        entries["config/../../escape.yaml"] = b"safe: true"
    elif failure == "unsupported":
        manifest["schema_version"] = "future"
        entries["bundle.json"] = json.dumps(manifest).encode()
    elif failure == "graph":
        snapshot = json.loads(entries["snapshot.json"])
        snapshot["sha256"] = "wrong"
        entries["snapshot.json"] = json.dumps(snapshot).encode()
        manifest["files"]["snapshot.json"] = {
            "size": len(entries["snapshot.json"]),
            "sha256": hashlib.sha256(entries["snapshot.json"]).hexdigest(),
        }
        entries["bundle.json"] = json.dumps(manifest).encode()
    with zipfile.ZipFile(bundle, "w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
        if failure == "duplicate":
            archive.writestr(blob_name, entries[blob_name])
    graph = MemoryGraphStore()
    target = tmp_path / "restored"
    with pytest.raises(ValueError):
        restore_bundle(graph, target / "data", bundle, config_dir=target / "config", model_dir=target / "models")
    assert graph.count_vertices() == 0
    assert not target.exists()


@pytest.mark.parametrize("kind", ["secret", "missing_blob", "changed_blob", "bound"])
def test_invalid_source_assets_refused_without_publishing_bundle(tmp_path, kind):
    config, models, blob = assets(tmp_path / "source")
    if kind == "secret":
        (config / "credentials.yaml").write_text("api_token: not-an-env-reference\n")
    elif kind == "missing_blob":
        blob.unlink()
    elif kind == "changed_blob":
        blob.write_bytes(b"different")
    destination = tmp_path / "backup.zip"
    destination.write_bytes(b"previous-good-backup")
    options = {"max_bytes": 16} if kind == "bound" else {}
    with pytest.raises(ValueError):
        backup_bundle(
            MemoryGraphStore(), tmp_path / "data", destination,
            config_dir=config, model_dir=models, **options,
        )
    assert destination.read_bytes() == b"previous-good-backup"
    assert not list(tmp_path.glob("*.tmp"))


@pytest.mark.parametrize("populated", ["config", "models", "graph"])
def test_restore_refuses_populated_targets(tmp_path, populated):
    bundle, _, _, _ = make_bundle(tmp_path)
    target = tmp_path / "restored"
    graph = MemoryGraphStore()
    if populated == "graph":
        graph.upsert_vertex("WorkItem", {"canonical_id": "keep", "issue_key": "KEEP-1"})
    else:
        directory = target / populated
        directory.mkdir(parents=True)
        (directory / "keep").write_bytes(b"keep")
    with pytest.raises(ValueError, match="empty"):
        restore_bundle(graph, target / "data", bundle, config_dir=target / "config", model_dir=target / "models")
    assert graph.get_vertex_by_canonical_id("test:bundle") is None


def test_model_disabled_bundle_does_not_require_downloaded_weights(tmp_path):
    config = tmp_path / "config"
    config.mkdir()
    (config / "policy.yaml").write_text("secret_refs:\n  token: env://TOKEN\n")
    backup_bundle(
        MemoryGraphStore(), tmp_path / "data", tmp_path / "backup.zip",
        config_dir=config, model_dir=tmp_path / "empty-models",
    )
    with zipfile.ZipFile(tmp_path / "backup.zip") as archive:
        assert json.loads(archive.read("bundle.json"))["model_blobs"] == 0


@pytest.mark.parametrize("mutation", ["config", "weight", "extra"])
def test_verifier_requires_exact_asset_bytes_and_inventory(tmp_path, mutation):
    bundle, _, models, blob = make_bundle(tmp_path)
    target, graph = tmp_path / "target", MemoryGraphStore()
    options = {"config_dir": target / "config", "model_dir": target / "models"}
    restore_bundle(graph, target / "data", bundle, **options)
    verify_restored_bundle(graph, target / "data", bundle, **options)
    path = {
        "config": target / "config" / "memory-policy.yaml",
        "weight": target / "models" / blob.relative_to(models),
        "extra": target / "config" / "extra.yaml",
    }[mutation]
    path.write_bytes(b"changed")
    with pytest.raises(AssertionError, match="differ"):
        verify_restored_bundle(graph, target / "data", bundle, **options)


@pytest.mark.parametrize("mutation", ["duplicate_vid", "duplicate_canonical", "bad_properties"])
def test_invalid_inner_graph_refused_even_with_valid_checksums(tmp_path, mutation):
    bundle, _, _, _ = make_bundle(tmp_path)
    with zipfile.ZipFile(bundle) as archive:
        entries = {name: archive.read(name) for name in archive.namelist()}
    snapshot = json.loads(entries["snapshot.json"])
    vertex = snapshot["payload"]["vertices"][0]
    if mutation.startswith("duplicate"):
        duplicate = dict(vertex)
        if mutation == "duplicate_canonical":
            duplicate["vid"] = "different"
        snapshot["payload"]["vertices"].append(duplicate)
    else:
        vertex["properties"] = []
    snapshot["sha256"] = digest(snapshot["payload"])
    entries["snapshot.json"] = json.dumps(snapshot).encode()
    manifest = json.loads(entries["bundle.json"])
    manifest["files"]["snapshot.json"] = {
        "size": len(entries["snapshot.json"]),
        "sha256": hashlib.sha256(entries["snapshot.json"]).hexdigest(),
    }
    entries["bundle.json"] = json.dumps(manifest).encode()
    with zipfile.ZipFile(bundle, "w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    target, graph = tmp_path / "target", MemoryGraphStore()
    with pytest.raises(ValueError):
        restore_bundle(graph, target / "data", bundle,
                       config_dir=target / "config", model_dir=target / "models")
    assert graph.count_vertices() == 0 and not target.exists()


def test_audited_cli_round_trip_and_bundle_selection(tmp_path, monkeypatch):
    from eoip import runtime

    config, models, blob = assets(tmp_path / "source")
    bundle = tmp_path / "eoip-20261003.zip"
    graph = MemoryGraphStore()
    graph.upsert_vertex("WorkItem", {"canonical_id": "test:cli"})
    closed = []
    monkeypatch.setattr(graph, "close", lambda: closed.append("source"), raising=False)
    monkeypatch.setattr(runtime, "create_store", lambda: graph)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path / "source" / "data"))
    monkeypatch.setattr(sys, "argv", [
        "backup", "--bundle", "--config-dir", str(config), "--model-dir", str(models),
        "--output", str(bundle),
    ])
    runpy.run_module("scripts.backup", run_name="__main__")
    assert select_snapshot(None, tmp_path) == bundle
    target = tmp_path / "target"
    restored = MemoryGraphStore()
    monkeypatch.setattr(restored, "close", lambda: closed.append("target"), raising=False)
    monkeypatch.setattr(runtime, "create_store", lambda: restored)
    monkeypatch.setenv("EOIP_DATA_DIR", str(target / "data"))
    monkeypatch.setattr(sys, "argv", [
        "restore", str(bundle), "--config-dir", str(target / "config"),
        "--model-dir", str(target / "models"),
    ])
    runpy.run_module("scripts.restore", run_name="__main__")
    assert restored.get_vertex_by_canonical_id("test:cli") is not None
    assert (target / "models" / blob.relative_to(models)).read_bytes() == blob.read_bytes()
    audit = (target / "data" / "audit" / "audit.jsonl").read_text()
    assert '"event_type":"restore_intent"' in audit and '"outcome":"success"' in audit
    assert closed == ["source", "target"]


def test_restore_byte_bound_refuses_before_target_writes(tmp_path):
    bundle, _, _, _ = make_bundle(tmp_path)
    target = tmp_path / "target"
    with pytest.raises(ValueError, match="bound"):
        restore_bundle(MemoryGraphStore(), target / "data", bundle,
                       config_dir=target / "config", model_dir=target / "models", max_bytes=16)
    assert not target.exists()


def test_recursive_yaml_refused_without_replacing_backup(tmp_path):
    config, models, _ = assets(tmp_path / "source")
    (config / "recursive.yaml").write_text("items: &items [*items]\n")
    bundle = tmp_path / "backup.zip"
    bundle.write_bytes(b"keep")
    with pytest.raises(ValueError, match="recursive"):
        backup_bundle(MemoryGraphStore(), tmp_path / "data", bundle,
                      config_dir=config, model_dir=models)
    assert bundle.read_bytes() == b"keep"


@pytest.mark.parametrize("key", ["api-token", "apiKey", "Authorization", "private_key"])
def test_plaintext_secret_key_variants_are_not_archived(tmp_path, key):
    config, models, _ = assets(tmp_path / "source")
    (config / "credentials.yaml").write_text(f"{key}: plaintext\n")
    with pytest.raises(ValueError, match="secret references"):
        backup_bundle(MemoryGraphStore(), tmp_path / "data", tmp_path / "backup.zip",
                      config_dir=config, model_dir=models)
    assert not (tmp_path / "backup.zip").exists()
