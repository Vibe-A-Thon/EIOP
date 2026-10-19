"""Unit and lifecycle tests for WarrantDraftBuilder, Producer, WarrantKernel, ACL, and Query (T-111..T-114, T-118)."""

import pytest

from reva.core.errors import RevaNotFoundError
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.acl import Principal
from reva.kernel.authority import Authority, ConfidenceBand
from reva.kernel.blobs import BlobStore
from reva.kernel.builder import WarrantDraftBuilder
from reva.kernel.kernel import WarrantKernel
from reva.kernel.predicates import register_predicate

from pydantic import BaseModel
from reva.kernel.producers import get_producer, register_producer
from reva.kernel.store import RevaStore


class DummyArtifactStatement(BaseModel):
    file_type: str = "python"



@pytest.fixture(autouse=True)
def setup_dummy_predicate():
    try:
        register_predicate(
            name="reva.pred.test_artifact",
            statement_model=DummyArtifactStatement,
            description="Test predicate for kernel testing",
        )
    except Exception:
        pass



@pytest.mark.reva_depth("unit")
def test_warrant_issue_and_retrieval(tmp_path):
    store = RevaStore(":memory:")
    blobs = BlobStore(root_dir=str(tmp_path))
    kernel = WarrantKernel(store=store, blobs=blobs)

    tenant = "tenant_k1"
    prod = register_producer(store, tenant, "tool", "pytest-producer", "1.0.0")

    draft = (
        WarrantDraftBuilder("reva.pred.test_artifact", "analyze")
        .producer(prod.producer_id, prod.name, prod.version, producer_type="tool", key_id=prod.active_key_id)
        .about_artifact("a" * 64, size_bytes=100)
        .authority(Authority.SHIPPED_ARTIFACT)
        .observed()
        .confidence(ConfidenceBand.EXACT, 10000)
        .statement({"file_type": "python"})

        .acl(required_tokens=["sec_review"])
        .build()
    )

    # Issue
    sealed = kernel.issue(tenant, draft, raw=b"print('hello world')")
    assert sealed.warrant_id.startswith("wr1_")
    assert sealed.envelope.log.leaf_index == 0
    assert sealed.body.raw_ref is not None
    assert sealed.body.raw_ref.blob_id.startswith("blb1_")

    # Idempotent re-issue returns exact same warrant
    reissued = kernel.issue(tenant, draft, raw=b"print('hello world')")
    assert reissued.warrant_id == sealed.warrant_id

    # Retrieve with authorized principal
    principal_ok = Principal(id="alice", tenant_id=tenant, tokens={"sec_review"})
    fetched = kernel.get(tenant, principal_ok, sealed.warrant_id)
    assert fetched.warrant_id == sealed.warrant_id

    # Retrieve with unauthorized principal raises 404 (NotFoundError)
    principal_unauth = Principal(id="bob", tenant_id=tenant, tokens={"other_token"})
    with pytest.raises(RevaNotFoundError):
        kernel.get(tenant, principal_unauth, sealed.warrant_id)


@pytest.mark.reva_depth("unit")
def test_warrant_supersede_and_retract(tmp_path):
    store = RevaStore(":memory:")
    blobs = BlobStore(root_dir=str(tmp_path))
    kernel = WarrantKernel(store=store, blobs=blobs)

    tenant = "tenant_k2"
    prod = register_producer(store, tenant, "tool", "pytest-producer", "1.0.0")

    draft1 = (
        WarrantDraftBuilder("reva.pred.test_artifact", "analyze")
        .producer(prod.producer_id, prod.name, prod.version, producer_type="tool", key_id=prod.active_key_id)
        .about_artifact("b" * 64)
        .authority(Authority.SHIPPED_ARTIFACT)
        .observed()
        .confidence(ConfidenceBand.HIGH, 8500)
        .statement({"file_type": "python"})
        .build()
    )
    w1 = kernel.issue(tenant, draft1)

    # Supersede w1 with w2
    draft2 = (
        WarrantDraftBuilder("reva.pred.test_artifact", "analyze_v2")
        .producer(prod.producer_id, prod.name, prod.version, producer_type="tool", key_id=prod.active_key_id)
        .about_artifact("b" * 64)
        .authority(Authority.SHIPPED_ARTIFACT)
        .observed()
        .confidence(ConfidenceBand.EXACT, 10000)
        .statement({"file_type": "python"})

        .build()
    )

    w2 = kernel.supersede(tenant, w1.warrant_id, draft2, reason="updated analysis")
    assert w2.warrant_id != w1.warrant_id

    # Check status of w1 in store is now superseded
    principal = Principal(id="admin", tenant_id=tenant, is_admin=True)
    w1_updated = kernel.get(tenant, principal, w1.warrant_id)
    assert w1_updated.envelope.status == "superseded"

    # Current query excludes w1, includes w2
    results = kernel.query(tenant, principal, status="active")
    active_ids = [r.warrant_id for r in results]
    assert w2.warrant_id in active_ids
    assert w1.warrant_id not in active_ids

    # Retract w2
    retraction = kernel.retract(tenant, w2.warrant_id, reason="false positive", producer_id=prod.producer_id)
    assert retraction.warrant_id.startswith("wr1_")
    w2_updated = kernel.get(tenant, principal, w2.warrant_id)
    assert w2_updated.envelope.status == "retracted"

