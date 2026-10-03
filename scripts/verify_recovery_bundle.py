"""Actual HugeGraph/configuration/binary-asset recovery in a disposable project."""

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from eoip.config import load_agent_config, load_memory_policy, load_query_policy
from eoip.graph.hugegraph import HugeGraphStore
from eoip.jobs import JobQueue, write_json
from eoip.recovery_bundle import backup_bundle, restore_bundle

from scripts.verify_clean_demo import golden_queries, load_canonical_demo
from scripts.verify_restore import verify_restored_bundle


def verify_recovery_bundle(source, target, root: Path, *, project_root: Path | None = None) -> dict:
    for store in (source, target):
        assert store.count_vertices() == store.count_edges() == 0, "Requires empty disposable graphs"
    project = project_root or Path(__file__).resolve().parents[1]
    data = root / "original"
    source.ensure_schema({})
    load_canonical_demo(source, data, project_root)
    golden = golden_queries(source, data)
    pending = JobQueue(data).submit("DEMO", {})
    config, models = root / "config", root / "models"
    shutil.copytree(project / "config", config)
    weights = b"EOIP synthetic binary recovery fixture\x00\xff" * 32_768
    sha = hashlib.sha256(weights).hexdigest()
    blob = models / "blobs" / f"sha256-{sha}"
    blob.parent.mkdir(parents=True)
    blob.write_bytes(weights)
    write_json(models / "manifests" / "registry.ollama.ai" / "library" / "recovery" / "latest", {
        "schemaVersion": 2,
        "config": {"digest": f"sha256:{sha}", "size": len(weights)},
        "layers": [{"digest": f"sha256:{sha}", "size": len(weights)}],
    })
    archive = root / "recovery.zip"
    exported = backup_bundle(source, data, archive, config_dir=config, model_dir=models)
    restored_root = root / "restored"
    restored = restore_bundle(
        target, restored_root / "data", archive,
        config_dir=restored_root / "config", model_dir=restored_root / "models",
    )
    verify_restored_bundle(
        target, restored_root / "data", archive,
        config_dir=restored_root / "config", model_dir=restored_root / "models",
    )
    assert golden_queries(target, restored_root / "data") == golden
    assert JobQueue(restored_root / "data").get(pending["job_id"])["status"] == "HELD"
    with patch.dict(os.environ, {"EOIP_CONFIG_DIR": str(config)}):
        expected = (load_memory_policy(), load_query_policy(), load_agent_config("Trace Impact"))
        assert expected[2] is not None, "Agent configuration was not loaded"
    with patch.dict(os.environ, {"EOIP_CONFIG_DIR": str(restored_root / "config")}):
        assert (load_memory_policy(), load_query_policy(), load_agent_config("Trace Impact")) == expected
    try:
        restore_bundle(
            target, restored_root / "data", archive,
            config_dir=root / "refused-config", model_dir=root / "refused-models",
        )
    except ValueError as exc:
        assert "empty" in str(exc)
    else:
        raise AssertionError("Populated graph accepted recovery bundle")
    assert not (root / "refused-config").exists()
    assert not (root / "refused-models").exists()
    return {
        "status": "PASS", "graph": restored, "asset_files": exported["asset_files"],
        "model_blobs": exported["model_blobs"], "weight_bytes": len(weights),
        "weight_sha256": sha, "asset_inventory_and_bytes_equal": True,
        "configuration_loaders_equal": True, "pending_job_held": True,
        "golden_queries_equal": True, "populated_graph_rejected": True,
        "model_fixture": "synthetic Ollama-layout binary bytes; not inference certification",
    }


def main():
    report = Path(os.environ["EOIP_ACCEPTANCE_REPORT"])
    password = os.environ["EOIP_HUGEGRAPH_PASSWORD"]
    source = HugeGraphStore(os.environ["EOIP_ACCEPTANCE_SOURCE_URL"], password=password)
    target = HugeGraphStore(os.environ["EOIP_ACCEPTANCE_TARGET_URL"], password=password)
    try:
        with tempfile.TemporaryDirectory(prefix="eoip-recovery-gate-") as temporary:
            result = verify_recovery_bundle(source, target, Path(temporary))
        write_json(report, result)
        print(json.dumps(result))
    except Exception as exc:
        write_json(report, {"status": "FAIL", "reason_code": type(exc).__name__})
        raise
    finally:
        source.close()
        target.close()


if __name__ == "__main__":
    main()
