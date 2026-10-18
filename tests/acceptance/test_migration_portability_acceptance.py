"""Acceptance test suite for Migration, Portability, and Rollback (WP-034, CRA-034.1-034.8, CRA-034.A)."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.migration.cli import create_parser, main
from eoip.migration.protocol import (
    CutoverApproval,
    LossLedger,
    MigrationManifest,
    MigrationProtocolEngine,
    MigrationStage,
    ReconciliationReport,
)
from eoip.migration.r2rml_importer import ThirdPartyRMLImporter


@pytest.fixture
def populated_source():
    store = MemoryGraphStore()
    v1 = store.upsert_vertex("Project", {"canonical_id": "proj:alpha", "name": "Project Alpha"})
    v2 = store.upsert_vertex("WorkItem", {"canonical_id": "item:1", "issue_key": "ALPHA-1", "summary": "Setup DB"})
    v3 = store.upsert_vertex("WorkItem", {"canonical_id": "item:2", "issue_key": "ALPHA-2", "summary": "Configure ETL"})
    store.upsert_edge("CONTAINS", v1["vid"], v2["vid"], {})
    store.upsert_edge("PARENT_OF", v2["vid"], v3["vid"], {})
    return store


# ===========================================================================
# CRA-034.1: CLI conventions, dry-run, and scope
# ===========================================================================

def test_cra_034_1_cli_conventions_and_dry_run(tmp_path):
    # 1. Discover dry-run
    res_disc = main(["discover", "--source", "eoip://prod-graph", "--dry-run"])
    assert res_disc == 0

    # 2. Export with manifest
    out_file = tmp_path / "export" / "manifest.json"
    res_exp = main(["export", "--output", str(out_file)])
    assert res_exp == 0
    assert out_file.exists()

    # 3. Validate
    res_val = main(["validate", "--input", str(out_file)])
    assert res_val == 0

    # 4. Compare
    res_cmp = main(["compare", "--source", "eoip://source", "--target", "eoip://target"])
    assert res_cmp == 0

    # 5. Rollback
    res_roll = main(["rollback", "--reason", "Rehearsal rollback drill"])
    assert res_roll == 0


# ===========================================================================
# CRA-034.6: eoip-migrate CLI structure and subcommands
# ===========================================================================

def test_cra_034_6_eoip_migrate_cli_interface():
    parser = create_parser()

    # All 7 subcommands required by CRA-034.6 must be registered and available
    choices = parser._subparsers._actions[1].choices
    assert "discover" in choices
    assert "export" in choices
    assert "validate" in choices
    assert "compare" in choices
    assert "replay" in choices
    assert "cutover" in choices
    assert "rollback" in choices


# ===========================================================================
# CRA-034.2: Fidelity preservation semantics (IRIs, blank nodes, datatypes, ACLs)
# ===========================================================================

def test_cra_034_2_fidelity_preservation_semantics(populated_source):
    engine = MigrationProtocolEngine()
    target_store = MemoryGraphStore()

    # Stage baseline
    manifest = engine.stage_1_discover_and_pin(populated_source, "source://store-a", "target://store-b")
    engine.stage_4_staged_loading(populated_source, target_store)
    report = engine.stage_5_verify_equivalence(populated_source, target_store)

    assert report.counts_match is True
    assert report.named_graphs_preserved is True
    assert report.blank_nodes_preserved is True
    assert report.acl_vectors_preserved is True

    # Entities and properties match exactly
    s_vertices = populated_source.find_vertices()
    t_vertices = target_store.find_vertices()
    assert len(s_vertices) == len(t_vertices)
    assert any(v["properties"]["canonical_id"] == "proj:alpha" for v in t_vertices)


# ===========================================================================
# CRA-034.3: Feature/loss/unsupported ledger & non-lossless refusal
# ===========================================================================

def test_cra_034_3_feature_loss_unsupported_ledger():
    ledger = LossLedger(is_lossless=True)

    # Clean ledger is lossless
    assert ledger.is_lossless is True

    # Dropped construct immediately blocks lossless declaration
    ledger.record_dropped(
        construct_type="NonStandardJoin",
        identifier="join_clause_99",
        detail="Complex recursive join not supported in target engine",
    )
    assert ledger.is_lossless is False
    assert len(ledger.unsupported_constructs) == 1

    # Lossy coercion also blocks lossless declaration
    ledger.record_coercion("Coerced high-precision decimal to 64-bit float")
    assert ledger.is_lossless is False
    assert len(ledger.lossy_coercions) == 1


# ===========================================================================
# CRA-034.4: Staged loading, shadow-read, and bound cutover
# ===========================================================================

def test_cra_034_4_staged_shadow_read_and_bound_cutover(populated_source):
    engine = MigrationProtocolEngine()
    target_store = MemoryGraphStore()

    manifest = engine.stage_1_discover_and_pin(populated_source, "source://store-1", "target://store-2")
    engine.stage_4_staged_loading(populated_source, target_store)

    # CDC deltas replay
    deltas = [
        {"operation": "UPSERT", "label": "WorkItem", "properties": {"canonical_id": "item:3", "issue_key": "ALPHA-3", "summary": "Deploy staging"}},
        {"operation": "DELETE", "entity_id": "item:1"},
        {"operation": "ACL_UPDATE", "entity_id": "proj:alpha", "acl": ["role:auditor"]},
    ]
    replayed = engine.stage_6_cdc_catch_up(target_store, deltas)
    assert replayed == 3
    assert target_store.count_vertices() == 4

    # Cutover approval with matching checksum succeeds
    valid_approval = CutoverApproval(
        approval_id="appr-01",
        source_uri="source://store-1",
        target_uri="target://store-2",
        mapping_revision="rev-v1.4",
        policy_revision="pol-v2.0",
        approved_by="Auditor",
        approved_at=100.0,
        manifest_checksum=manifest.source_checksum,
        is_valid=True,
    )
    assert engine.stage_7_cutover(valid_approval) is True
    assert engine.active_routing == "target"

    # Mismatched approval checksum fails cutover
    bad_approval = CutoverApproval(
        approval_id="appr-bad",
        source_uri="source://store-1",
        target_uri="target://store-2",
        mapping_revision="rev-v1.4",
        policy_revision="pol-v2.0",
        approved_by="Auditor",
        approved_at=100.0,
        manifest_checksum="invalid_tampered_checksum",
        is_valid=True,
    )
    with pytest.raises(ValueError, match="does not match pinned source manifest"):
        engine.stage_7_cutover(bad_approval)


# ===========================================================================
# CRA-034.5: Rollback of routing and data with 14-day window
# ===========================================================================

def test_cra_034_5_rollback_routing_and_retention(populated_source):
    engine = MigrationProtocolEngine(rollback_window_days=14)
    target_store = MemoryGraphStore()

    manifest = engine.stage_1_discover_and_pin(populated_source, "source://1", "target://2")
    engine.stage_4_staged_loading(populated_source, target_store)

    approval = CutoverApproval(
        approval_id="appr-1",
        source_uri="source://1",
        target_uri="target://2",
        mapping_revision="v1",
        policy_revision="v1",
        approved_by="Lead",
        approved_at=100.0,
        manifest_checksum=manifest.source_checksum,
    )
    engine.stage_7_cutover(approval)
    assert engine.active_routing == "target"

    # Rollback reverts routing to shadow source
    res = engine.stage_8_rollback(reason="Elevated transaction error rate observed in target")
    assert res["status"] == "ROLLED_BACK"
    assert engine.active_routing == "source"
    assert res["rollback_window_days"] == 14
    assert res["source_retained"] is True


# ===========================================================================
# CRA-034.7: Full eight-stage migration protocol execution
# ===========================================================================

def test_cra_034_7_eight_stage_protocol_execution(populated_source):
    engine = MigrationProtocolEngine()
    target = MemoryGraphStore()

    # Stage 1: Discover & pin
    m = engine.stage_1_discover_and_pin(populated_source, "s://alpha", "t://beta")
    assert engine.current_stage == MigrationStage.STAGE_1_DISCOVERY_AND_PIN

    # Stage 2: Format extraction with hashes
    hashes = engine.stage_2_extract_formats()
    assert "turtle_hash" in hashes
    assert engine.current_stage == MigrationStage.STAGE_2_EXTRACTION_AND_HASH

    # Stage 3: Mapping synthesis & loss analysis
    loss = engine.stage_3_synthesize_mapping({"unsupported": [], "coercions": []})
    assert loss.is_lossless is True
    assert engine.current_stage == MigrationStage.STAGE_3_MAPPING_AND_LOSS_ANALYSIS

    # Stage 4: Staged loading
    engine.stage_4_staged_loading(populated_source, target)
    assert engine.current_stage == MigrationStage.STAGE_4_STAGED_LOADING

    # Stage 5: Semantic equivalence
    recon = engine.stage_5_verify_equivalence(populated_source, target)
    assert recon.counts_match is True
    assert engine.current_stage == MigrationStage.STAGE_5_SEMANTIC_EQUIVALENCE

    # Stage 6: CDC catch-up
    replayed = engine.stage_6_cdc_catch_up(target, [{"operation": "UPSERT", "label": "WorkItem", "properties": {"canonical_id": "item:x", "issue_key": "X-1", "summary": "delta"}}])
    assert replayed == 1
    assert engine.current_stage == MigrationStage.STAGE_6_CDC_CATCH_UP

    # Stage 7: Cutover
    appr = CutoverApproval("ap-1", "s://alpha", "t://beta", "r1", "p1", "Auditor", 100.0, m.source_checksum)
    engine.stage_7_cutover(appr)
    assert engine.active_routing == "target"
    assert engine.current_stage == MigrationStage.STAGE_7_ATOMIC_CUTOVER

    # Stage 8: Rollback window
    roll = engine.stage_8_rollback("Simulation test")
    assert engine.active_routing == "source"
    assert engine.current_stage == MigrationStage.STAGE_8_ROLLBACK_WINDOW


# ===========================================================================
# CRA-034.8: Third-party R2RML / RML translation (Ontop, Morph-KGC, RMLStreamer)
# ===========================================================================

def test_cra_034_8_r2rml_rml_third_party_translation():
    # 1. Ontop translation with vendor SQL coercion
    ontop_importer = ThirdPartyRMLImporter(engine_origin="ontop")
    ontop_rml = {
        "id": "ontop_billing_mapping",
        "logicalSource": {"sqlQuery": "SELECT id, amount, REGEXP_REPLACE(code, '-', '') FROM billing"},
        "subjectMap": {"template": "http://corp.org/bill/{id}", "class": "http://corp.org/schema#Bill"},
        "predicateObjectMap": [
            {"predicate": "http://corp.org/schema#amount", "objectMap": {"column": "amount"}}
        ]
    }
    ontop_ir, ontop_loss = ontop_importer.translate_to_cml_ir(ontop_rml)
    assert ontop_ir.mapping_id == "ontop_billing_mapping"
    assert ontop_loss.is_lossless is False
    assert any("SQL-92" in c for c in ontop_loss.lossy_coercions)

    # 2. Morph-KGC translation with unsupported binary Excel source
    morph_importer = ThirdPartyRMLImporter(engine_origin="morph-kgc")
    morph_rml = {
        "id": "morph_excel_mapping",
        "logicalSource": {"format": "excel", "path": "sheets/data.xlsx"},
        "subjectMap": {"template": "http://corp.org/row/{id}", "class": "http://corp.org/schema#Row"},
    }
    _, morph_loss = morph_importer.translate_to_cml_ir(morph_rml)
    assert morph_loss.is_lossless is False
    assert any(u.construct_type == "MorphKGC_BinaryExcel" for u in morph_loss.unsupported_constructs)

    # 3. RMLStreamer translation with unsupported WebSocket stream source
    streamer_importer = ThirdPartyRMLImporter(engine_origin="rmlstreamer")
    streamer_rml = {
        "id": "streamer_ws_mapping",
        "logicalSource": {"sourceType": "websocket", "endpoint": "wss://stream.internal/trades"},
        "subjectMap": {"template": "http://corp.org/trade/{id}", "class": "http://corp.org/schema#Trade"},
    }
    _, streamer_loss = streamer_importer.translate_to_cml_ir(streamer_rml)
    assert streamer_loss.is_lossless is False
    assert any(u.construct_type == "RMLStreamer_StreamSource" for u in streamer_loss.unsupported_constructs)


# ===========================================================================
# CRA-034.A: Standards ontology and corpus migration acceptance
# ===========================================================================

def test_cra_034_a_standards_ontology_and_corpus_migration_acceptance(populated_source):
    # 1. Migrate through two qualified stores and verify equivalence
    engine = MigrationProtocolEngine()
    target_store = MemoryGraphStore()

    manifest = engine.stage_1_discover_and_pin(populated_source, "source://alpha", "target://beta")
    engine.stage_4_staged_loading(populated_source, target_store)
    recon = engine.stage_5_verify_equivalence(populated_source, target_store)
    assert recon.counts_match is True

    # 2. Inject mapping failure and verify loss ledger blocks lossless claim
    flawed_mapping = {
        "unsupported": [
            {"type": "UnsupportedGeometryDatatype", "id": "geo:shape", "detail": "Spatial polygon dropped"}
        ]
    }
    loss_report = engine.stage_3_synthesize_mapping(flawed_mapping)
    assert loss_report.is_lossless is False
    assert len(loss_report.unsupported_constructs) == 1

    # 3. Delta catch-up, atomic cutover, and clean rollback
    replayed = engine.stage_6_cdc_catch_up(target_store, [{"operation": "UPSERT", "label": "WorkItem", "properties": {"canonical_id": "item:post", "issue_key": "P-1", "summary": "post-cutover"}}])
    assert replayed == 1

    approval = CutoverApproval("cutover-final", "source://alpha", "target://beta", "v1", "v1", "Auditor", 100.0, manifest.source_checksum)
    assert engine.stage_7_cutover(approval) is True
    assert engine.active_routing == "target"

    rollback_result = engine.stage_8_rollback("Adversarial drill: rollback execution")
    assert rollback_result["status"] == "ROLLED_BACK"
    assert engine.active_routing == "source"
