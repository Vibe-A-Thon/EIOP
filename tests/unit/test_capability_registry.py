"""Unit tests for CapabilityRegistry and capability enforcement (CRA-001.4-001.8)."""
from __future__ import annotations
import json, tempfile
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

@pytest.fixture
def registry():
    reg = CapabilityRegistry()
    reg.reset()
    return reg

def test_initial_state_and_qualification_ledger(registry, tmp_path):
    ledger = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [
            {"id": "CRA-001.1", "kind": "clause", "state": "ACCEPTED", "receipts": [{"path": "rcpt1.json", "sha256": "abc"}], "updated_at": "2026-10-18T00:00:00Z"},
            {"id": "CRA-001.2", "kind": "clause", "state": "OPEN", "receipts": [], "updated_at": "2026-10-18T00:00:00Z"},
        ],
    }
    led_file = tmp_path / "ledger.json"
    led_file.write_text(json.dumps(ledger), encoding="utf-8")
    registry.set_ledger_path(led_file)

    # 1. Unqualified capability: only 1 of 2 clauses accepted
    entry1 = registry.register(
        capability_id="graph.neo4j",
        provider_id="neo4j",
        provider_version="5.21.0",
        qualifying_clauses=["CRA-001.1", "CRA-001.2"],
    )
    assert entry1.state == CapabilityState.SUPPORTED_UNQUALIFIED

    # 2. Qualified capability: all clauses accepted
    entry2 = registry.register(
        capability_id="graph.memory",
        provider_id="memory",
        provider_version="1.0.0",
        qualifying_clauses=["CRA-001.1"],
    )
    assert entry2.state == CapabilityState.SUPPORTED_QUALIFIED
    assert entry2.receipt_ref == "rcpt1.json"

def test_cannot_configure_supported_qualified(registry):
    registry.register(
        capability_id="test.cap",
        provider_id="test",
        provider_version="1.0",
    )
    with pytest.raises(ValueError, match="CRA-001.7 violation"):
        registry.configure_state("test.cap", CapabilityState.SUPPORTED_QUALIFIED)

def test_probe_failure_sets_unavailable(registry):
    def failing_probe():
        raise RuntimeError("database down")

    registry.register(
        capability_id="db.failing",
        provider_id="db",
        provider_version="1.0",
        probe=failing_probe,
    )
    results = registry.probe_all()
    assert results["db.failing"] is False
    entry = registry.get("db.failing")
    assert entry.state == CapabilityState.UNAVAILABLE

def test_require_unsupported_capability_and_construct(registry):
    # Unregistered capability -> 422
    with pytest.raises(UnsupportedCapabilityError) as exc_info:
        registry.require("nonexistent.service")
    assert exc_info.value.status_code == 422
    assert exc_info.value.code == "UNSUPPORTED_CAPABILITY"

    # Registered with unsupported construct -> 422 naming construct
    registry.register(
        capability_id="query.sparql",
        provider_id="sparql-engine",
        provider_version="1.1",
        unsupported_constructs=["SPARQL_STAR", "PROPERTY_PATHS"],
    )
    with pytest.raises(UnsupportedCapabilityError) as exc_info:
        registry.require("query.sparql", construct="SPARQL_STAR")
    assert exc_info.value.status_code == 422
    assert exc_info.value.details["unsupported_construct"] == "SPARQL_STAR"

def test_require_disabled_unavailable_and_unlicensed(registry):
    registry.register("cap.disabled", "p", "1.0")
    registry.configure_state("cap.disabled", CapabilityState.DISABLED)
    with pytest.raises(CapabilityDisabledError) as exc_info:
        registry.require("cap.disabled")
    assert exc_info.value.status_code == 409

    registry.register("cap.unlicensed", "p", "1.0")
    registry.configure_state("cap.unlicensed", CapabilityState.UNLICENSED)
    with pytest.raises(CapabilityNotEntitledError) as exc_info:
        registry.require("cap.unlicensed")
    assert exc_info.value.status_code == 403

    registry.register("cap.unavailable", "p", "1.0")
    registry.configure_state("cap.unavailable", CapabilityState.UNAVAILABLE)
    with pytest.raises(CapabilityUnavailableError) as exc_info:
        registry.require("cap.unavailable")
    assert exc_info.value.status_code == 503
