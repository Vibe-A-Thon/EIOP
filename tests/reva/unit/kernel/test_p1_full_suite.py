"""Comprehensive tests covering Worker, Outbox, STH, Auditor, Bundles, EntityRegistry, Projector, Gaps, and Contradictions (Phase P1 completion)."""

import json
from pathlib import Path
import pytest
from pydantic import BaseModel

from reva.core.time import format_ts, utc_now_ms
from reva.graph.entity_registry import EntityRegistry
from reva.graph.kgf_adapter import MemoryGraphPort
from reva.graph.projector import GraphProjector
from reva.kernel.acl import Principal
from reva.kernel.authority import Authority, ConfidenceBand
from reva.kernel.blobs import BlobStore
from reva.kernel.builder import WarrantDraftBuilder
from reva.kernel.bundles import export_bundle, import_bundle
from reva.kernel.contradictions import detect_contradictions, list_contradictions, resolve_contradiction
from reva.kernel.events import EventBus, default_event_bus, dispatch_outbox
from reva.kernel.gaps import list_gaps, open_gap, transition_gap
from reva.kernel.kernel import WarrantKernel
from reva.kernel.keys import decrypt_private_key, generate_key
from reva.kernel.predicates import register_predicate
from reva.kernel.producers import register_producer
from reva.kernel.sth import issue_sth_now, verify_sth
from reva.kernel.auditor import audit_transparency_log
from reva.kernel.store import RevaStore
from reva.kernel.translog import TransparencyLog
from reva.worker import JobWorker, enqueue_job


class ArtifactMetricStatement(BaseModel):
    lines_of_code: int = 100


@pytest.fixture(autouse=True)
def setup_predicates():
    try:
        register_predicate(
            name="reva.pred.code_metric",
            statement_model=ArtifactMetricStatement,
            description="Code metric test predicate",
        )
    except Exception:
        pass



@pytest.mark.reva_depth("unit")
def test_worker_and_events():
    store = RevaStore(":memory:")
    bus = EventBus()
    received_events = []

    bus.subscribe("test.event", lambda ev: received_events.append(ev.event_id))

    # Save outbox event and dispatch
    store.save_outbox_event("evt_1", "t1", "test.event", {"hello": "world"})
    dispatched = dispatch_outbox(store, bus)
    assert dispatched == 1
    assert "evt_1" in received_events

    # Re-dispatch has nothing new
    assert dispatch_outbox(store, bus) == 0

    # Job queue and worker execution
    worker = JobWorker(store, "w1")
    executed_jobs = []

    worker.register("compute_stats", lambda j: executed_jobs.append(j.job_id))
    jid = enqueue_job(store, "t1", "compute_stats", {"scope": "all"})

    did_work = worker.run_once()
    assert did_work is True
    assert jid in executed_jobs


@pytest.mark.reva_depth("unit")
def test_sth_generation_and_audit(tmp_path):
    store = RevaStore(":memory:")
    log = TransparencyLog(store, "log_sth_test")

    # Generate log signing key
    log_key = generate_key(store, "t1", "log", "log_sth_test")
    priv_key = decrypt_private_key(log_key.private_key_enc)

    # Append leaves
    for i in range(5):
        log.append(f"wr1_{i:064x}")

    # Issue STH
    sth = issue_sth_now(store, log, log_key.key_id, priv_key)
    assert sth.tree_size == 5
    assert verify_sth(sth, log_key.public_key_bytes) is True

    # Run audit
    report = audit_transparency_log(store, log)
    assert report.clean is True
    assert report.sths_checked == 1
    assert len(report.issues) == 0


@pytest.mark.reva_depth("unit")
def test_bundles_export_import(tmp_path):
    store = RevaStore(":memory:")
    blobs = BlobStore(root_dir=str(tmp_path / "cas1"))
    log = TransparencyLog(store, "log_b1")
    kernel = WarrantKernel(store=store, blobs=blobs, log=log)

    tenant1 = "tenant_export"
    prod = register_producer(store, tenant1, "tool", "packager", "1.0.0")

    # Log key and initial STH
    log_key = generate_key(store, tenant1, "log", "log_b1")
    priv_key = decrypt_private_key(log_key.private_key_enc)

    draft = (
        WarrantDraftBuilder("reva.pred.code_metric", "analyze")
        .producer(prod.producer_id, prod.name, prod.version, producer_type="tool", key_id=prod.active_key_id)
        .about_artifact("c" * 64, size_bytes=50)
        .authority(Authority.SHIPPED_ARTIFACT)
        .observed()
        .confidence(ConfidenceBand.EXACT, 10000)
        .statement({"lines_of_code": 100})
        .build()
    )

    w = kernel.issue(tenant1, draft, raw=b"binary payload for bundle")
    sth = issue_sth_now(store, log, log_key.key_id, priv_key)

    bundle_zip = str(tmp_path / "bundle.zip")
    principal = Principal(id="exporter", tenant_id=tenant1, is_admin=True)

    bid = export_bundle(
        store=store,
        blobs=blobs,
        log=log,
        tenant_id=tenant1,
        principal=principal,
        warrant_ids=[w.warrant_id],
        destination_zip_path=bundle_zip,
        sth_record=sth,
    )
    assert bid.startswith("bun1_")

    # Import into tenant2
    store2 = RevaStore(":memory:")
    blobs2 = BlobStore(root_dir=str(tmp_path / "cas2"))
    log2 = TransparencyLog(store2, "log_b2")

    import_rep = import_bundle(store2, blobs2, log2, "tenant_import", bundle_zip)
    assert import_rep.success is True
    assert import_rep.warrants_imported == 1
    assert import_rep.blobs_imported == 1

    # Imported warrant exists in target store
    imported_row = store2.get_warrant("tenant_import", w.warrant_id)
    assert imported_row is not None


@pytest.mark.reva_depth("unit")
def test_entity_registry_and_graph_projector():
    store = RevaStore(":memory:")
    registry = EntityRegistry(store)

    eid = registry.upsert_entity("t1", "Service", "order-service")
    assert eid.startswith("ent1_")

    vid = registry.record_version("t1", eid, "commit", "sha256:abcd", warrant_id="wr1_mock1")
    assert vid.startswith("ver1_")

    ent = registry.get_entity("t1", eid)
    assert ent.current_version_id == vid

    # Projector test
    graph = MemoryGraphPort()
    projector = GraphProjector(graph)

    # Fake warrant object to project
    from reva.kernel.warrant import ArtifactSubject, SealedWarrant, WarrantAcl, WarrantBody, WarrantClassification, WarrantEnvelope, WarrantLogRef, WarrantSignature
    w = SealedWarrant(
        warrant_id="wr1_proj_test",
        body=WarrantBody(
            schema="reva.warrant/1",
            tenant_id="t1",
            subject=ArtifactSubject(artifact_id="art1_test", sha256="d"*64, size_bytes=10, media_type="text/plain", format="text"),
            producer={"producer_id": "prd1_1", "producer_type": "tool", "name": "p", "version": "1", "key_id": "key1_1"},
            operation="test",
            predicate="reva.pred.code_metric",
            parameters={},
            statement={"lines_of_code": 100},
            authority=Authority.SHIPPED_ARTIFACT,
            epistemic_state="observed",
            confidence={"band": "exact", "score_bp": 10000},
            observed_at=format_ts(utc_now_ms()),
            valid_time={"from": format_ts(utc_now_ms())},
        ),
        envelope=WarrantEnvelope(
            warrant_id="wr1_proj_test",
            signature=WarrantSignature(alg="ed25519", key_id="key1_1", sig="sig"),
            recorded_at=format_ts(utc_now_ms()),
            log=WarrantLogRef(log_id="log1", leaf_index=0),
            status="active",
        ),
    )

    projected_count = projector.project(w)
    assert projected_count >= 2
    assert graph.get_vertex("wr1_proj_test") is not None
    assert graph.get_vertex("art1_test") is not None


@pytest.mark.reva_depth("unit")
def test_gaps_and_contradictions(tmp_path):
    store = RevaStore(":memory:")
    blobs = BlobStore(root_dir=str(tmp_path))
    kernel = WarrantKernel(store=store, blobs=blobs)

    # 1. Gaps
    gap = open_gap(store, "t1", "auth", "Does service X validate JWT tokens?", "auth_module", severity="high", impact_score_bp=8000)
    assert gap.status == "open"
    assert gap.gap_id.startswith("gap1_")

    transitioned = transition_gap(store, "t1", gap.gap_id, "assigned", "Assigned to Alice", "lead")
    assert transitioned.status == "assigned"
    assert len(transitioned.history) == 2

    gaps = list_gaps(store, "t1", status="assigned")
    assert len(gaps) == 1

    # 2. Contradictions
    prod = register_producer(store, "t1", "tool", "c_prod", "1.0.0")
    draft_a = (
        WarrantDraftBuilder("reva.pred.code_metric", "scan_a")
        .producer(prod.producer_id, prod.name, prod.version, producer_type="tool", key_id=prod.active_key_id)
        .about_artifact("e" * 64)
        .authority(Authority.SHIPPED_ARTIFACT)
        .observed()
        .confidence(ConfidenceBand.EXACT, 10000)
        .statement({"lines_of_code": 100})
        .build()
    )
    w_a = kernel.issue("t1", draft_a)

    draft_b = (
        WarrantDraftBuilder("reva.pred.code_metric", "scan_b")
        .producer(prod.producer_id, prod.name, prod.version, producer_type="tool", key_id=prod.active_key_id)
        .about_artifact("e" * 64)
        .authority(Authority.SHIPPED_ARTIFACT)
        .observed()
        .confidence(ConfidenceBand.EXACT, 10000)
        .statement({"lines_of_code": 200})  # Conflict: 200 vs 100
        .build()
    )
    w_b = kernel.issue("t1", draft_b)

    # Detect contradictions
    cx_list = detect_contradictions(store, "t1", w_b)
    assert len(cx_list) == 1
    cx = cx_list[0]
    assert cx.contradiction_id.startswith("cx1_")

    # Resolve contradiction in favor of w_b
    resolved = resolve_contradiction(store, "t1", cx.contradiction_id, winning_warrant_id=w_b.warrant_id, rationale="scan_b was newer and more accurate")
    assert resolved.status == "resolved"

    # w_a should now be marked superseded
    principal = Principal(id="auditor", tenant_id="t1", is_admin=True)
    w_a_fetched = kernel.get("t1", principal, w_a.warrant_id)
    assert w_a_fetched.envelope.status == "superseded"
