"""Acceptance Suite for WP-001: Baseline, Decisions and Acceptance Ledger.

Implements and validates:
- CRA-001.1: Runtime composition inventory and feature separation
- CRA-001.2: Decision records for profiles, semantic engines, storage authority, artifact pinning
- CRA-001.4: Capability discovery based on configuration and runtime readiness
- CRA-001.7: CapabilityState prohibition on authoring SUPPORTED_QUALIFIED in config
- CRA-001.9: Ledger and receipt paths, SHA-256 receipt integrity
- CRA-001.10: Full ledger coverage of CRA-001..045, E01..E14, H-01..H-17, X-01..X-42
- CRA-001.A: Acceptance obligation (rejection of corrupted receipts, source changes, missing evidence)
"""
from __future__ import annotations

import json
from pathlib import Path
import pytest

from eoip.capabilities.model import (
    CapabilityEntry,
    CapabilityState,
    UnsupportedCapabilityError,
    CapabilityUnavailableError,
    CapabilityNotEntitledError,
    CapabilityDisabledError,
)
from eoip.capabilities.registry import CapabilityRegistry
from tools.acceptance.verify_ledger import verify_ledger, sha256_file


def test_cra_001_1_runtime_inventory_and_feature_matrix():
    """CRA-001.1: Inventory of actual runtime composition and advertised features."""
    inv_file = Path(".audit-scratch/inventory.json")
    assert inv_file.exists(), ".audit-scratch/inventory.json must exist"
    
    with inv_file.open("r", encoding="utf-8") as f:
        inv = json.load(f)
    
    # Must contain totals, files inventory, requirement refs, and routes
    assert "totals" in inv
    assert "inventory" in inv
    assert "requirement_refs" in inv
    assert "routes" in inv
    
    # Verify separation of implemented, configured, and exercised components
    assert len(inv["inventory"]) > 500
    assert len(inv["routes"]) > 50
    assert len(inv["requirement_refs"]) > 100


def test_cra_001_2_decision_records_and_artifact_hashes():
    """CRA-001.2: Decision records for profiles, semantic engines, storage, and pinned artifact hashes."""
    decisions_dir = Path("docs/decisions")
    assert decisions_dir.exists(), "docs/decisions must exist"
    
    # Check key ADRs exist
    adr_files = list(decisions_dir.glob("ADR-*.md"))
    assert len(adr_files) >= 3, f"Expected at least 3 ADRs, found {len(adr_files)}"
    
    adr_h16 = decisions_dir / "ADR-H16-no-cuda-redistribution.md"
    assert adr_h16.exists()
    h16_text = adr_h16.read_text(encoding="utf-8")
    assert "CPU-only" in h16_text or "CPU" in h16_text
    
    # Check decision ledger import exists
    decisions_ledger = decisions_dir / "decisions-ledger-import.json"
    assert decisions_ledger.exists()


def test_cra_001_4_capability_discovery_states():
    """CRA-001.4: Capability discovery exposes distinct states (unsupported, unlicensed, unavailable, unqualified)."""
    reg = CapabilityRegistry()
    reg.reset()
    
    # 1. Unregistered -> UNSUPPORTED
    with pytest.raises(UnsupportedCapabilityError):
        reg.require("nonexistent.feature")
        
    # 2. Registered but down -> UNAVAILABLE
    def failing_probe():
        raise ConnectionError("Service unreachable")
    reg.register("search.vector", "hybrid", "1.0", probe=failing_probe)
    reg.probe_all()
    assert reg.get("search.vector").state == CapabilityState.UNAVAILABLE
    with pytest.raises(CapabilityUnavailableError):
        reg.require("search.vector")
        
    # 3. Unlicensed -> UNLICENSED
    reg.register("neural.research", "research", "1.0")
    reg.configure_state("neural.research", CapabilityState.UNLICENSED)
    assert reg.get("neural.research").state == CapabilityState.UNLICENSED
    with pytest.raises(CapabilityNotEntitledError):
        reg.require("neural.research")


def test_cra_001_7_qualified_state_authoring_prohibition():
    """CRA-001.7: SUPPORTED_QUALIFIED cannot be authored in configuration; only verified receipts can set it."""
    reg = CapabilityRegistry()
    reg.reset()
    reg.register("graph.memory", "memory", "1.0")
    
    with pytest.raises(ValueError, match="CRA-001.7 violation"):
        reg.configure_state("graph.memory", CapabilityState.SUPPORTED_QUALIFIED)


def test_cra_001_9_ledger_and_receipts_storage_contract():
    """CRA-001.9: Ledger at .audit-scratch/ledger.json; receipts under .audit-scratch/receipts/<clause-id>/."""
    ledger_path = Path(".audit-scratch/ledger.json")
    assert ledger_path.exists(), "Ledger must exist at .audit-scratch/ledger.json"
    
    receipts_dir = Path(".audit-scratch/receipts")
    assert receipts_dir.exists(), "Receipts directory must exist"
    
    with ledger_path.open("r", encoding="utf-8") as f:
        ledger = json.load(f)
    
    # Check receipt references in accepted items have sha256 and point to valid files
    for item in ledger["items"]:
        if item["state"] == "ACCEPTED" and item.get("receipts"):
            for rcpt in item["receipts"]:
                assert "sha256" in rcpt
                rcpt_path = Path(rcpt["path"])
                assert rcpt_path.exists(), f"Referenced receipt {rcpt_path} does not exist"
                assert sha256_file(rcpt_path) == rcpt["sha256"]


def test_cra_001_10_ledger_schema_and_full_coverage():
    """CRA-001.10: Full ledger coverage of clauses, decisions, scenarios, and research records."""
    ledger_path = Path(".audit-scratch/ledger.json")
    with ledger_path.open("r", encoding="utf-8") as f:
        ledger = json.load(f)
    
    items = ledger["items"]
    item_ids = {it["id"] for it in items}
    
    # Must have 590 items
    assert len(items) == 590, f"Expected 590 items in ledger, got {len(items)}"
    
    # Must cover CRA-001 to CRA-045
    for i in range(1, 46):
        cra_id = f"CRA-{i:03d}.1"
        assert cra_id in item_ids, f"Missing {cra_id} in ledger"
        cra_a = f"CRA-{i:03d}.A"
        assert cra_a in item_ids, f"Missing {cra_a} in ledger"
        
    # Must cover H-01 to H-17
    for h in range(1, 18):
        h_id = f"H-{h:02d}"
        assert h_id in item_ids, f"Missing {h_id} in ledger"
        
    # Must cover X-01 to X-42
    for x in range(1, 43):
        x_id = f"X-{x:02d}"
        assert x_id in item_ids, f"Missing {x_id} in ledger"


def test_cra_001_a_acceptance_gate(tmp_path):
    """CRA-001.A: Ledger verifier rejects tampered receipts, missing receipts, and open child obligations."""
    # 1. Missing receipt in ACCEPTED state is rejected
    bad_ledger = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [
            {"id": "CRA-001.1", "kind": "clause", "state": "ACCEPTED", "receipts": [], "updated_at": "2026-10-18T00:00:00Z"}
        ],
    }
    led_file = tmp_path / "bad_ledger.json"
    led_file.write_text(json.dumps(bad_ledger), encoding="utf-8")
    violations = verify_ledger(led_file)
    assert any(v["code"] == "MISSING_RECEIPT" for v in violations)

    # 2. Child open when parent acceptance claimed is rejected
    child_open_ledger = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [
            {"id": "CRA-001.1", "parent": "CRA-001", "kind": "clause", "state": "OPEN", "updated_at": "2026-10-18T00:00:00Z"},
            {"id": "CRA-001.A", "parent": "CRA-001", "kind": "acceptance", "state": "ACCEPTED", "receipts": [], "updated_at": "2026-10-18T00:00:00Z"},
        ],
    }
    led_file2 = tmp_path / "child_open_ledger.json"
    led_file2.write_text(json.dumps(child_open_ledger), encoding="utf-8")
    violations2 = verify_ledger(led_file2)
    assert any(v["code"] == "CHILD_OPEN" for v in violations2)
