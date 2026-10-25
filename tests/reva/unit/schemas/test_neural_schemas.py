"""
Unit Tests for Neural Schemas: Models, Dual-Pathway Assimilation, CSCG, and AST Engine (NS-REQ-*).
"""

import pytest
from pydantic import ValidationError

from packages.eoip.neural.schemas import (
    SlotConstraint,
    NeuralSchema,
    DualPathwayAssimilator,
    CSCGGraph,
    AttentionSchemaEngine,
)

pytestmark = pytest.mark.reva_depth("unit")


def test_neural_schema_model_and_id():
    slots = {
        "user_id": SlotConstraint(name="user_id", required=True, allowed_types=["str"]),
        "action": SlotConstraint(name="action", required=True, allowed_types=["str"]),
        "count": SlotConstraint(name="count", required=False, allowed_types=["int"]),
    }
    schema = NeuralSchema.create(
        name="UserActionSchema",
        domain="security",
        slots=slots,
    )

    assert schema.schema_id.startswith("sch1_")
    assert len(schema.schema_id) == 5 + 64
    assert schema.name == "UserActionSchema"

    # Verify extra="forbid" raises ValidationError
    with pytest.raises(ValidationError):
        NeuralSchema(
            schema_id=schema.schema_id,
            name="Tampered",
            domain="security",
            unauthorized_field="forbidden",
        )


def test_dual_pathway_assimilation():
    slots = {
        "service": SlotConstraint(name="service", required=True, allowed_types=["str"]),
        "endpoint": SlotConstraint(name="endpoint", required=True, allowed_types=["str"]),
        "status_code": SlotConstraint(name="status_code", required=True, allowed_types=["int"]),
    }
    schema = NeuralSchema.create(name="HTTPLogSchema", domain="observability", slots=slots)
    assimilator = DualPathwayAssimilator()
    assimilator.register_schema(schema)

    # 1. Fast Pathway (Valid slots)
    valid_data = {
        "service": "auth-service",
        "endpoint": "/v1/login",
        "status_code": 200,
    }
    res_fast = assimilator.assimilate(schema.schema_id, valid_data)
    assert res_fast.status == "assimilated"
    assert res_fast.confidence == 1.0
    assert res_fast.latency_ms < 50.0
    assert res_fast.epistemic_state == "inferred"
    assert res_fast.filled_slots["service"]["epistemic_state"] == "inferred"

    # 2. Slow Novelty Gap Pathway (Missing required slot 'status_code')
    incomplete_data = {
        "service": "auth-service",
        "endpoint": "/v1/login",
    }
    res_gap = assimilator.assimilate(schema.schema_id, incomplete_data)
    assert res_gap.status == "novel_gap_routed"
    assert "status_code" in res_gap.missing_slots
    assert res_gap.gap_id is not None
    assert res_gap.gap_id.startswith("gap1_")


def test_cscg_clone_splitting_and_rebinding():
    cscg = CSCGGraph()
    # Split polysemous token 'transfer' in two distinct contexts
    clone_bank = cscg.split_clone("transfer", context_tag="banking")
    clone_file = cscg.split_clone("transfer", context_tag="network_file")

    assert clone_bank.clone_id != clone_file.clone_id
    assert clone_bank.context_tag == "banking"
    assert clone_file.context_tag == "network_file"

    # Set transition
    login_clone = cscg.split_clone("login", context_tag="banking")
    cscg.set_transition(login_clone.clone_id, clone_bank.clone_id, 0.95)

    # Rebind schema
    rebound = cscg.rebind_schema(
        source_context="banking",
        target_context="crypto",
        symbol_mapping={"transfer": "send_tx", "login": "connect_wallet"},
    )
    assert len(rebound.transitions) == 1


def test_attention_schema_engine_and_thrashing():
    ast_engine = AttentionSchemaEngine(thrashing_window_s=5.0, thrashing_switch_threshold=3)

    # Set focus
    f1 = ast_engine.set_focus("mod:auth", "module", intensity=0.8)
    assert ast_engine.current_focus.target_id == "mod:auth"

    # Handoff packet
    packet = ast_engine.handoff_attention("agent_sentinel_2")
    assert packet["handoff_to"] == "agent_sentinel_2"
    assert packet["focus_target"] == "mod:auth"

    # Simulate rapid thrashing switches across multiple targets
    ast_engine.set_focus("fn:login", "function")
    ast_engine.set_focus("cls:DBClient", "class")
    ast_engine.set_focus("ep:/health", "endpoint")

    report = ast_engine.detect_thrashing()
    assert report.is_thrashing
    assert report.recommended_action == "PAUSE_AND_EXPEDITE_GOAL"
