"""Model Provider Port, local adapters, task routing, LLM telemetry and guardrails.

SR-LLM-001, SR-LLM-002, SR-LLM-004, SR-LLM-008, SR-LLM-009. No network: HTTP adapters use
httpx.MockTransport and the egress gateway uses a stub transport.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from eoip.egress import (
    CanaryRegistry,
    ConsentRecord,
    EgressGateway,
    EndpointConfig,
    PolicyEngine,
    PolicyRule,
    SharingLevel,
)
from eoip.models.guardrails import GuardrailBlocked, Guardrails
from eoip.models.port import (
    LOCAL_RUNTIMES,
    RUNTIME_CHAT_PATHS,
    AdapterInactive,
    Capability,
    CapabilityMismatch,
    ModelAdapter,
    ModelCapabilities,
    ModelPort,
    ModelRequest,
    ModelResult,
    NoModelAvailable,
    StructuredOutputInvalid,
    TaskRouter,
    http_chat_adapter,
    in_process_adapter,
    negotiate,
)
from eoip.tenancy.quotas import TenantCircuitBreaker

ALL = frozenset(Capability)


def caps(*c, ctx=8192, tools=False, det=True, size="small", modalities=("text",)):
    return ModelCapabilities(capabilities=frozenset(c) or ALL, context_length=ctx, supports_tools=tools,
                             deterministic=det, size_class=size, modalities=frozenset(modalities))


def adapter(name, *, out="ok", size="small", fail=False, calls=None, **kw):
    def invoke(req):
        if calls is not None:
            calls.append((name, req.tenant_id))
        if fail:
            raise ConnectionError("runtime down")
        return ModelResult(output=out, adapter=name, tokens_in=5, tokens_out=7, cost=0.001)
    return ModelAdapter(name=name, runtime="vllm", caps=caps(size=size, **kw), invoke=invoke)


def req(task="classification", capability=Capability.CHAT, inp="hello", **kw):
    return ModelRequest(task=task, capability=capability, input=inp, **kw)


# ---------------------------------------------------------------------------
# SR-LLM-001 - one port, every capability, negotiation before the call
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-001")
class TestModelProviderPort:
    @pytest.mark.parametrize("capability", list(Capability))
    def test_every_capability_is_served_only_by_adapters_that_declare_it(self, capability):
        port = ModelPort()
        port.register(adapter("has", det=False, tools=True, modalities=("text", "image", "audio")))
        port.register(ModelAdapter(name="lacks", runtime="vllm",
                                   caps=caps(*(set(Capability) - {capability})), invoke=lambda r: None))
        r = req(capability=capability)
        assert port.invoke("has", r).output == "ok"
        with pytest.raises(CapabilityMismatch, match=capability.value):
            port.invoke("lacks", req(capability=capability))

    def test_negotiation_checks_context_modalities_tools_and_determinism(self):
        c = caps(Capability.CHAT, ctx=1000, tools=False, det=False)
        with pytest.raises(CapabilityMismatch, match="context length"):
            negotiate(req(input_tokens=900, max_tokens=200), c)
        with pytest.raises(CapabilityMismatch, match="modalities image"):
            negotiate(req(modalities=frozenset({"text", "image"})), c)
        with pytest.raises(CapabilityMismatch, match="tools"):
            negotiate(req(tools=("search",)), c)
        with pytest.raises(CapabilityMismatch, match="determinism"):
            negotiate(req(require_determinism=True), c)
        with pytest.raises(CapabilityMismatch, match="structured output"):
            negotiate(req(json_schema={"type": "object"}), c)
        negotiate(req(input_tokens=100), c)  # fits

    def test_structured_output_is_validated_against_the_json_schema(self):
        schema = {"type": "object", "required": ["label"], "properties": {"label": {"enum": ["bug", "feature"]}}}
        port = ModelPort()
        port.register(adapter("good", out={"label": "bug"}))
        port.register(adapter("bad", out={"label": "spam"}))
        assert port.invoke("good", req(capability=Capability.STRUCTURED_OUTPUT, json_schema=schema)).output == {
            "label": "bug"}
        with pytest.raises(StructuredOutputInvalid):
            port.invoke("bad", req(capability=Capability.STRUCTURED_OUTPUT, json_schema=schema))


# ---------------------------------------------------------------------------
# SR-LLM-002 - local by default; external only via tenant admin + egress gateway
# ---------------------------------------------------------------------------

def _mock_factory(runtime, seen):
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append((request.url.path, json.loads(request.content)))
        if runtime == "ollama":
            return httpx.Response(200, json={"message": {"content": "hi"}, "prompt_eval_count": 3, "eval_count": 2})
        return httpx.Response(200, json={"choices": [{"message": {"content": "hi"}}],
                                         "usage": {"prompt_tokens": 3, "completion_tokens": 2}})
    return lambda: httpx.Client(transport=httpx.MockTransport(handler))


def _gateway(sent):
    gw = EgressGateway(tenant_id="t1", policy=PolicyEngine(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S1)]),
                       transport=lambda payload, endpoint: sent.append(payload) or {"text": "external ok"},
                       audit=lambda e: None, canaries=CanaryRegistry())
    gw.register_endpoint(EndpointConfig(id="ext-eu", kind="chat", url_allowlist=["https://llm.example.eu"],
                                        region="EU", dpa_ref="DPA-1"))
    return gw


@pytest.mark.req("SR-LLM-002")
class TestLocalByDefault:
    @pytest.mark.parametrize("runtime", sorted(RUNTIME_CHAT_PATHS))
    def test_http_adapter_for_each_local_runtime_class(self, runtime):
        seen = []
        a = http_chat_adapter(f"m-{runtime}", runtime, url="http://local-model:8000", model="m",
                              caps=caps(Capability.CHAT), client_factory=_mock_factory(runtime, seen))
        port = ModelPort()
        port.register(a)
        assert a.local and f"m-{runtime}" in port.active  # active without any admin action
        result = port.invoke(f"m-{runtime}", req())
        assert (result.output, result.tokens_in, result.tokens_out) == ("hi", 3, 2)
        assert seen[0][0] == RUNTIME_CHAT_PATHS[runtime]

    def test_in_process_onnx_runtime_adapter(self):
        a = in_process_adapter("onnx", "onnxruntime", lambda r: r.input.upper(), caps=caps(Capability.CHAT))
        port = ModelPort()
        port.register(a)
        assert port.invoke("onnx", req(inp="abc")).output == "ABC"
        assert {"vllm", "sglang", "llama_cpp", "ollama", "tgi", "onnxruntime", "openvino",
                "tensorrt_llm"} == set(LOCAL_RUNTIMES)

    def test_external_adapter_inactive_until_tenant_admin_enables_it_and_calls_go_through_egress(self):
        sent = []
        gw = _gateway(sent)
        port = ModelPort(egress_gateway=gw)
        with pytest.raises(ValueError, match="egress"):
            port.register(ModelAdapter(name="no-ep", runtime="external", caps=caps(), invoke=lambda r: None))
        port.register(ModelAdapter(name="cloud", runtime="external", caps=caps(), invoke=lambda r: None,
                                   egress_endpoint_id="ext-eu"))
        assert "cloud" not in port.active
        with pytest.raises(AdapterInactive):
            port.invoke("cloud", req())
        with pytest.raises(PermissionError, match="tenant administrator"):
            port.enable_external("cloud", admin="bob", admin_roles={"analyst"})
        with pytest.raises(PermissionError, match="egress endpoint"):
            port.enable_external("cloud", admin="alice", admin_roles={"tenant_admin"})
        gw.enable_endpoint("ext-eu", admin="alice", consent=ConsentRecord(
            consent_id="c1", endpoint_id="ext-eu", signer="alice", signed_at=0.0, dpa_ref="DPA-1",
            residency_region="EU", scope="D0"))
        port.enable_external("cloud", admin="alice", admin_roles={"tenant_admin"})
        assert port.invoke("cloud", req(inp="summarise")).output == {"text": "external ok"}
        assert sent and port.audit[-1]["event"] == "model.external_enabled"


# ---------------------------------------------------------------------------
# SR-LLM-004 - task routing, fallbacks, per-tenant breakers and allowlists
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-004")
class TestTaskRouting:
    def _router(self, *, small_fail=False):
        calls = []
        port = ModelPort()
        port.register(adapter("small-a", size="small", fail=small_fail, calls=calls))
        port.register(adapter("large-a", size="large", calls=calls))
        return TaskRouter(port, breaker=TenantCircuitBreaker(failure_threshold=2, cooldown_s=60,
                                                            clock=lambda: 0.0)), calls

    def test_small_models_for_classification_extraction_routing_large_for_synthesis(self):
        router, _ = self._router()
        for task in ("classification", "extraction", "routing"):
            assert router.route(req(task=task)).adapter == "small-a"
        assert router.route(req(task="synthesis")).adapter == "large-a"

    def test_fallback_and_per_tenant_circuit_breaker(self):
        router, calls = self._router(small_fail=True)
        for _ in range(2):
            assert router.route(req(tenant_id="t1")).adapter == "large-a"  # fell back
        assert router.breaker.state("t1", "small-a") == "open"
        calls.clear()
        router.route(req(tenant_id="t1"))
        assert ("small-a", "t1") not in calls  # open breaker skips the failing model
        assert router.decisions[-1]["fallbacks"] == [("small-a", "circuit_open")]
        assert router.breaker.state("t2", "small-a") == "closed"  # other tenants unaffected
        router.route(req(tenant_id="t2"))
        assert ("small-a", "t2") in calls

    def test_per_tenant_model_allowlist(self):
        router, _ = self._router()
        router.set_allowlist("t1", {"large-a"})
        assert router.route(req(tenant_id="t1", task="classification")).adapter == "large-a"
        assert router.route(req(tenant_id="t2", task="classification")).adapter == "small-a"
        router.set_allowlist("t3", set())
        with pytest.raises(NoModelAvailable):
            router.route(req(tenant_id="t3"))


# ---------------------------------------------------------------------------
# SR-LLM-008 - per-call LLM telemetry, local only unless exported
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-008")
class TestLLMTelemetry:
    def test_every_call_records_latency_tokens_cost_cache_refusal_guardrails_quality(self):
        ticks = iter([0.0, 0.25, 1.0, 1.0, 2.0, 2.5, 3.0, 3.1])
        port = ModelPort(clock=lambda: next(ticks), guardrails=Guardrails())

        def invoke(r):
            refused = r.input == "refuse"
            return ModelResult(output="mail bob@corp.example" if not refused else "", adapter="m", tokens_in=11,
                               tokens_out=4, cost=0.002, refused=refused, quality_score=0.9)
        port.register(ModelAdapter(name="m", runtime="vllm", caps=caps(), invoke=invoke))
        port.invoke("m", req(inp="q1"))
        port.invoke("m", req(inp="q1"))  # deterministic -> cache hit
        port.invoke("m", req(inp="refuse"))
        first, second, third = port.telemetry.calls[:3]
        assert first["latency_ms"] == 250.0 and first["tokens_in"] == 11 and first["tokens_out"] == 4
        assert first["cost"] == 0.002 and first["quality_score"] == 0.9
        assert first["guardrail_triggers"] == ["output:redacted:EMAIL"]
        assert (first["cache_hit"], second["cache_hit"]) == (False, True)
        assert third["refused"] is True
        s = port.telemetry.summary("_platform")
        assert s["calls"] == 3 and s["cache_hits"] == 1 and s["refusals"] == 1 and s["guardrail_triggers"] >= 1

    def test_telemetry_stays_local_unless_the_tenant_enables_export(self):
        port = ModelPort()
        port.register(adapter("m"))
        port.invoke("m", req(tenant_id="t1"))
        port.invoke("m", req(tenant_id="t2", inp="other"))
        with pytest.raises(PermissionError, match="not enabled"):
            port.telemetry.export("t1")
        with pytest.raises(PermissionError):
            port.telemetry.enable_export("t1", admin="")
        port.telemetry.enable_export("t1", admin="alice")
        exported = port.telemetry.export("t1")
        assert len(exported) == 1 and exported[0]["tenant_id"] == "t1"
        with pytest.raises(PermissionError):
            port.telemetry.export("t2")


# ---------------------------------------------------------------------------
# SR-LLM-009 - guardrails + OWASP-aligned jailbreak/injection corpus in CI
# ---------------------------------------------------------------------------

CORPUS = json.loads((Path(__file__).parents[1] / "fixtures" / "llm_guardrail_corpus.json").read_text())
PLACEHOLDERS = {
    "{{SECRET_ASSIGNMENT}}": "api" + "_key = '" + "sk" + "_live_" + "0123456789abcdefABCDEF'",
    "{{AWS_KEY}}": "AK" + "IA" + "ABCDEFGHIJKLMNOP",
    "{{CARD}}": " ".join(["4111"] * 4),
}


def _expand(text):
    for k, v in PLACEHOLDERS.items():
        text = text.replace(k, v)
    return text


@pytest.mark.req("SR-LLM-009")
class TestGuardrails:
    def test_corpus_covers_every_in_scope_owasp_category(self):
        tagged = {c["owasp"] for c in CORPUS["cases"] if c["owasp"]}
        assert set(CORPUS["categories_in_scope"]) <= tagged
        assert set(CORPUS["categories_in_scope"]) | set(CORPUS["categories_elsewhere"]) == {
            f"LLM{i:02d}" for i in range(1, 11)}

    @pytest.mark.parametrize("case", CORPUS["cases"], ids=lambda c: c["id"])
    def test_corpus_case(self, case):
        g = Guardrails()
        port = ModelPort(guardrails=g)
        port.register(adapter("m", out=_expand(case.get("text", "")), tools=True, ctx=4096))
        if case["kind"] == "input":
            r = req(inp=_expand(case["text"]))
            if case["expect"] == "block":
                with pytest.raises(GuardrailBlocked):
                    port.invoke("m", r)
                return
            port.invoke("m", r)
            if case["expect"] == "redact":
                assert "@" not in r.input and "123-45-6789" not in r.input
                assert any(t.startswith("input:pii_redacted") for t in port.telemetry.calls[-1]["guardrail_triggers"])
            else:
                assert port.telemetry.calls[-1]["guardrail_triggers"] == []
        elif case["kind"] == "output":
            res = port.invoke("m", req(inp="summarise"))
            if case["expect"] == "redact":
                assert "4111" not in res.output and "[REDACTED:" in res.output
            elif case["expect"] == "neutralise":
                assert "output:active_content" in res.guardrail_triggers
                assert "script>" not in res.output and "javascript:" not in res.output
            else:
                assert res.guardrail_triggers == [] and res.output == case["text"]
        elif case["kind"] == "tools":
            with pytest.raises(GuardrailBlocked, match="allowlist"):
                port.invoke("m", req(tools=tuple(case["tools"])))
        elif case["kind"] == "budget":
            with pytest.raises(CapabilityMismatch, match="context length"):
                port.invoke("m", req(input_tokens=case["input_tokens"]))

    def test_tool_allowlist_permits_listed_tools_and_raw_pii_only_by_policy(self):
        g = Guardrails(allow_raw_pii={"t-ok"})
        g.set_tool_allowlist("t1", {"search"})
        port = ModelPort(guardrails=g)
        port.register(adapter("m", tools=True))
        port.invoke("m", req(tenant_id="t1", tools=("search",)))
        with pytest.raises(GuardrailBlocked):
            port.invoke("m", req(tenant_id="t1", tools=("search", "shell")))
        r = req(tenant_id="t-ok", inp="mail jane@corp.example")
        port.invoke("m", r)
        assert r.input == "mail jane@corp.example"
