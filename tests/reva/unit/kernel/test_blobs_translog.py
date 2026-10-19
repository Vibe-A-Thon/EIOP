"""Unit tests for blobs and transparency log (T-109 / T-110)."""

import io
import pytest

from reva.core.errors import RevaIntegrityError, RevaNotFoundError
from reva.kernel.blobs import BlobStore
from reva.kernel.store import RevaStore
from reva.kernel.translog import (
    TransparencyLog,
    compute_consistency_proof,
    compute_path,
    empty_tree_root,
    leaf_hash,
    mth,
    node_hash,
    verify_consistency,
    verify_inclusion,
)


@pytest.mark.reva_depth("unit")
def test_blob_store_roundtrip_and_gc(tmp_path):
    store = BlobStore(root_dir=str(tmp_path))
    content = b"hello reva evidence cas blob"
    ref = store.put("tenant_test", content, media_type="text/plain", classification="internal")

    assert ref.blob_id.startswith("blb1_")
    assert store.exists("tenant_test", ref.blob_id)
    assert store.exists("tenant_test", ref.sha256)

    # Read back
    retrieved = store.get_bytes("tenant_test", ref.blob_id)
    assert retrieved == content

    # Streaming read
    reader = store.get("tenant_test", ref.blob_id)
    stream_content = reader.read()
    assert stream_content == content
    reader.close()

    # Dry-run GC
    orphans = store.gc_dry_run("tenant_test", referenced_blob_ids=set(), older_than_s=0)
    assert ref.blob_id in orphans

    # GC removes orphan
    removed = store.gc("tenant_test", referenced_blob_ids=set(), older_than_s=0)
    assert ref.blob_id in removed
    assert not store.exists("tenant_test", ref.blob_id)


@pytest.mark.reva_depth("unit")
def test_translog_rfc6962_proofs():
    db = RevaStore(":memory:")
    log = TransparencyLog(db, "log_unit_test")

    # Empty log
    assert log.root() == empty_tree_root()

    # Append 10 items
    leaf_ids = [f"wr1_{i:064x}" for i in range(10)]
    for item in leaf_ids:
        log.append(item)

    assert log.size() == 10
    root10 = log.root()
    assert len(root10) == 32

    # Check inclusion proof for each leaf
    leaves = log.get_leaves()
    for idx, item in enumerate(leaf_ids):
        proof_hex = log.inclusion_proof(idx)
        proof_bytes = [bytes.fromhex(p) for p in proof_hex]
        lh = leaf_hash(item.encode("utf-8"))
        assert verify_inclusion(lh, idx, 10, proof_bytes, root10) is True

        # Tampered leaf fails
        tampered_lh = leaf_hash(b"tampered")
        assert verify_inclusion(tampered_lh, idx, 10, proof_bytes, root10) is False

    # Check consistency proof between sizes
    root5 = log.root(size=5)
    proof_5_10_hex = log.consistency_proof(5, 10)
    proof_5_10_bytes = [bytes.fromhex(p) for p in proof_5_10_hex]
    assert verify_consistency(5, 10, root5, root10, proof_5_10_bytes) is True
