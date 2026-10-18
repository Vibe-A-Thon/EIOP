"""Comprehensive tests for the 8 advanced complementary cognitive capabilities."""

from __future__ import annotations

import time
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from eoip.platform_router import build_platform_router
from eoip.security.reflection_sandbox import (
    ReflectionSandbox,
    JailbreakInoculator,
    get_reflection_sandbox,
    get_jailbreak_inoculator,
)
from eoip.context.graph_slicing import (
    AttentionGraphSlicer,
    BitemporalContextSlate,
    get_attention_graph_slicer,
    get_bitemporal_context_slate,
)
from eoip.evaluation.distillation_sentinel import (
    ContinuousPromptDistiller,
    GraphRepairSentinel,
    get_continuous_prompt_distiller,
    get_graph_repair_sentinel,
)
from eoip.tools_contract.mcp_bridge import (
    ExternalMCPClient,
    MCPHostNotAllowed,
    ToolExecutionAttestor,
    get_tool_execution_attestor,
)
from eoip.state.engine import get_state_engine


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(build_platform_router())
    return TestClient(app)


# ── Feature 1: Reflection Sandbox Invariance ──────────────────────

def test_feature_1_reflection_sandbox_invariance_enforcement() -> None:
    sandbox = ReflectionSandbox()

    # Legitimate action should pass
    ok_res = sandbox.execute_step(
        step_id="step-01",
        action_type="enrich_metadata",
        target_entity="auth-service",
        proposed_payload={"cluster": "us-west-2", "version": "v1.4"},
        agent_role="engineer",
    )
    assert ok_res.allowed is True
    assert ok_res.state_after["version"] == "v1.4"

    # Action targeting forbidden system entity should be blocked
    blocked_res = sandbox.execute_step(
        step_id="step-02",
        action_type="delete_entity",
        target_entity="audit_ledger",
        proposed_payload={"drop": True},
        agent_role="engineer",
    )
    assert blocked_res.allowed is False
    assert any(v.rule_name == "FORBIDDEN_TARGET_INVARIANCE" for v in blocked_res.violations)

    # Identical reflection cycle should be detected
    cycle_res = sandbox.execute_step(
        step_id="step-03",
        action_type="enrich_metadata",
        target_entity="auth-service",
        proposed_payload={"cluster": "us-west-2", "version": "v1.4"},
        agent_role="engineer",
    )
    assert cycle_res.allowed is False
    assert any(v.rule_name == "REFLECTION_CYCLE_DETECTED" for v in cycle_res.violations)


# ── Feature 2: Jailbreak Inoculation ──────────────────────────────

def test_feature_2_jailbreak_inoculation() -> None:
    inoculator = get_jailbreak_inoculator()
    res = inoculator.inoculate("enterprise_agent")
    assert res["target_prompt_name"] == "enterprise_agent"
    assert res["rules_inoculated"] >= 3
    assert res["registered_version"] >= 1


# ── Feature 3: Attention-Weighted Graph Slicing ───────────────────

def test_feature_3_attention_weighted_graph_slicing() -> None:
    slicer = get_attention_graph_slicer()
    sliced = slicer.slice_graph(
        query="authenticate session tokens and billing transactions",
        seed_ids=["auth-gateway"],
        attention_threshold=0.35,
    )
    assert sliced.total_candidates >= 5
    assert sliced.retained_count < sliced.total_candidates
    assert sliced.compression_ratio > 0.0
    assert any(e.entity_id == "auth-gateway" for e in sliced.entities)
    assert "Attention-Weighted Subgraph" in sliced.rendered_context


# ── Feature 4: Bitemporal Context Slate ───────────────────────────

def test_feature_4_bitemporal_context_slate() -> None:
    state_engine = get_state_engine()
    t_past = time.time()
    state_engine.record("billing-schema", "upsert", {"tax_rate": 0.08, "currency": "USD"})

    time.sleep(0.01)
    t_now = time.time()
    state_engine.record("billing-schema", "upsert", {"tax_rate": 0.09, "discount_enabled": True})

    slate_builder = get_bitemporal_context_slate()
    slate = slate_builder.build_slate("billing-schema", t_past, t_now)
    assert slate["stream"] == "billing-schema"
    assert "tax_rate" in slate["delta_summary"]["modified_keys"]
    assert "discount_enabled" in slate["delta_summary"]["added_keys"]
    assert "Bitemporal Delta Slate" in slate["rendered_slate"]


# ── Feature 5: Continuous Prompt Distillation ────────────────────

def test_feature_5_continuous_prompt_distillation() -> None:
    distiller = get_continuous_prompt_distiller()
    res = distiller.distill_from_benchmarks("causal_copilot", "graph_rag_accuracy")
    assert "causal_copilot_distilled" in res["distilled_prompt_name"]
    assert res["exemplars_count"] >= 2
    assert res["version"] >= 1


# ── Feature 6: Graph Repair Sentinel ──────────────────────────────

def test_feature_6_graph_repair_sentinel() -> None:
    sentinel = get_graph_repair_sentinel()
    res = sentinel.inspect_and_repair(
        nodes=[
            {"id": "api-gateway", "label": "Service", "degree": 3},
            {"id": "auth-service", "label": "Service", "degree": 2},
            {"id": "orphan-worker", "label": "Worker", "degree": 0},
        ],
        edges=[{"from": "api-gateway", "to": "auth-service"}],
    )
    assert res["status"] == "repaired"
    assert "orphan-worker" in res["orphans_detected"]
    assert res["remediation_loop_converged"] is True
    assert res["repaired_edges_count"] == 2


# ── Feature 7: Universal External MCP Client ─────────────────────

@pytest.mark.asyncio
async def test_feature_7_external_mcp_client_rejects_unconfigured_host() -> None:
    client = ExternalMCPClient(allowed_hosts=set())
    with pytest.raises(MCPHostNotAllowed):
        await client.connect_server(
            server_name="kubernetes_cluster",
            transport="streamable-http",
            endpoint="https://k8s-mcp.internal/v1",
        )
    assert client.list_connected_servers() == []


# ── Feature 8: Cryptographic Tool Attestation ────────────────────

def test_feature_8_cryptographic_tool_attestation() -> None:
    attestor = ToolExecutionAttestor(signing_secret="test-hmac-key-for-integrity-only-32")
    cert = attestor.attest_execution(
        tool_name="deploy_canary",
        arguments={"service": "checkout", "traffic_percent": 10},
        output={"status": "canary_active", "rollout_id": "ro-9941"},
        caller_id="cd-pipeline",
    )
    assert cert.certificate_id.startswith("attest-")
    assert len(cert.hmac_signature) == 64

    # Verify signature
    verification = attestor.verify_certificate(cert.certificate_id)
    assert verification["valid"] is True
    assert verification["tool_name"] == "deploy_canary"

    # Verify tamper resistance with invalid ID
    fake_verif = attestor.verify_certificate("attest-nonexistent-id")
    assert fake_verif["valid"] is False


# ── Feature 9: REST API Verification ─────────────────────────────

def test_feature_9_advanced_capabilities_api_endpoints() -> None:
    client = _client()

    # 1. Sandbox endpoint
    sb_resp = client.post(
        "/api/v1/platform/guardrails/reflection-sandbox",
        json={
            "step_id": "api-step-1",
            "action_type": "update_config",
            "target_entity": "auth-proxy",
            "proposed_payload": {"retries": 3},
            "agent_role": "operator",
        },
    )
    assert sb_resp.status_code == 200
    assert sb_resp.json()["allowed"] is True

    # 2. Inoculate endpoint
    inoc_resp = client.post(
        "/api/v1/platform/guardrails/inoculate",
        json={"target_prompt_name": "copilot_system"},
    )
    assert inoc_resp.status_code == 200
    assert inoc_resp.json()["rules_inoculated"] >= 3

    # 3. Context slice endpoint
    slice_resp = client.post(
        "/api/v1/platform/context/slice-graph",
        json={"query": "billing database and authentication", "attention_threshold": 0.3},
    )
    assert slice_resp.status_code == 200
    assert "rendered_context" in slice_resp.json()

    # 4. Bitemporal slate endpoint
    slate_resp = client.post(
        "/api/v1/platform/context/bitemporal-slate",
        json={"stream": "billing-schema", "past_timestamp": time.time() - 100},
    )
    assert slate_resp.status_code == 200
    assert "delta_summary" in slate_resp.json()

    # 5. Distill prompts endpoint
    dist_resp = client.post(
        "/api/v1/platform/eval/distill-prompts",
        json={"target_prompt_name": "api_copilot", "benchmark_name": "graph_rag_accuracy"},
    )
    assert dist_resp.status_code == 200
    assert dist_resp.json()["exemplars_count"] >= 2

    # 6. Graph repair sentinel endpoint
    repair_resp = client.post(
        "/api/v1/platform/eval/graph-repair-sentinel",
        json={},
    )
    assert repair_resp.status_code == 200
    assert repair_resp.json()["status"] == "repaired"

    # 7. External MCP connect requires an authenticated configured operator.
    mcp_resp = client.post(
        "/api/v1/platform/tools/mcp/connect-external",
        json={"server_name": "github_enterprise", "endpoint": "https://mcp.github.com"},
    )
    assert mcp_resp.status_code == 401

    # 8. Tool attest & verify endpoints
    attest_resp = client.post(
        "/api/v1/platform/tools/attest-execution",
        json={
            "tool_name": "github_enterprise_query",
            "arguments": {"query": "repo:org/core"},
            "caller_id": "test-suite",
        },
    )
    assert attest_resp.status_code == 401
