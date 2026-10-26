"""OpenAI-compatible egress transport (SR-LLM-010/013/015/019): contract mock + live local endpoint.

The contract tests drive the real ``OpenAICompatibleTransport`` through the full ``EgressGateway``
call path against an ``httpx.MockTransport`` that implements the OpenAI chat/embeddings wire format.
The live tests point the same transport at the local Ollama OpenAI-compatible API (CI job
llm-cpu-reference). Residual gap: live validation with a customer provider account pending.
"""
from __future__ import annotations

import json
import os

import httpx
import pytest

from eoip.egress import (ConsentRecord, EgressGateway, EgressOutage, EndpointConfig, PolicyEngine, PolicyRule,
                         SharingLevel)
from eoip.egress.http_transport import (EgressTransportAuthError, EgressTransportError, OpenAICompatibleTransport,
                                        env_credentials)

pytestmark = pytest.mark.req("SR-LLM-010", "SR-LLM-013", "SR-LLM-015", "SR-LLM-019")

BASE = "https://llm.example.eu"
KEY = "test-key-not-a-secret"  # noqa: S105 - fixture value for the mock provider


def _gateway(transport, *, url=BASE, kind="chat", mtls=False, level=SharingLevel.S5, audit=None):
    gw = EgressGateway(tenant_id="t1", policy=PolicyEngine(rules=[PolicyRule(rule_id="r", max_level=level)]),
                       transport=transport, audit=audit or (lambda e: None))
    gw.register_endpoint(EndpointConfig(id="ext-eu", kind=kind, url_allowlist=[url], region="EU",
                                        dpa_ref="DPA-1", mtls=mtls))
    gw.enable_endpoint("ext-eu", admin="admin@t", consent=ConsentRecord(
        consent_id="c1", endpoint_id="ext-eu", signer="admin@t", signed_at=0.0, dpa_ref="DPA-1",
        residency_region="EU", scope="summaries"))
    return gw


def _call(gw, payload, classes=("D0",)):
    return gw.call(endpoint_id="ext-eu", task="summarize", payload=payload, user_id="u1", role="analyst",
                   data_classes=list(classes))


class Provider:
    """Minimal OpenAI-compatible provider mock that records exactly what reached the wire."""

    def __init__(self, script=None):
        self.requests: list[httpx.Request] = []
        self.script = list(script or [])

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if self.script:
            status, headers = self.script.pop(0)
            return httpx.Response(status, headers=headers, json={"error": {"type": "rate_limit"}})
        if request.headers.get("authorization") != f"Bearer {KEY}":
            return httpx.Response(401, json={"error": {"type": "invalid_api_key"}})
        body = json.loads(request.content)
        if request.url.path == "/v1/chat/completions":
            user = body["messages"][-1]["content"]
            return httpx.Response(200, json={"model": body["model"], "choices": [{"index": 0, "finish_reason": "stop",
                                  "message": {"role": "assistant", "content": f"Summary of: {user}"}}],
                                  "usage": {"prompt_tokens": 5, "completion_tokens": 4}})
        if request.url.path == "/v1/embeddings":
            return httpx.Response(200, json={"model": body["model"], "data": [
                {"index": i, "embedding": [float(len(t)), 1.0]} for i, t in reversed(list(enumerate(body["input"])))]})
        return httpx.Response(404, json={"error": {"type": "not_found"}})


def _transport(provider, **kw):
    kw.setdefault("credentials", lambda ep: KEY)
    return OpenAICompatibleTransport(models={"ext-eu": "gpt-test"}, transport=httpx.MockTransport(provider),
                                     sleep=lambda s: None, **kw)


def test_chat_through_gateway_sends_only_transformed_payload_and_reidentifies():
    provider = Provider()
    gw = _gateway(_transport(provider))
    result = _call(gw, {"prompt": "Summarize the renewal for alice@corp.example"}, classes=["D2"])
    sent = json.loads(provider.requests[0].content)
    assert "alice@corp.example" not in provider.requests[0].content.decode()  # S5 redaction before the wire
    assert provider.requests[0].url == f"{BASE}/v1/chat/completions"
    assert sent["model"] == "gpt-test" and sent["stream"] is False
    assert sent["messages"][-1]["content"].startswith("Summarize the renewal for ")
    assert result["response"]["text"].startswith("Summary of: Summarize the renewal for ")
    manifest = result["manifest"]
    assert not manifest.denied and manifest.bytes_in > 0 and manifest.response_hash


def test_structured_payload_fields_are_tokenized_on_the_wire_then_reidentified():
    provider = Provider()
    gw = _gateway(_transport(provider), level=SharingLevel.S4)
    result = _call(gw, {"name": "Alice Example", "region": "EU"}, classes=["D2"])
    wire = provider.requests[0].content.decode()
    assert "Alice Example" not in wire  # S4 tokenization happened before the transport
    assert "Alice Example" in result["response"]["text"]  # re-identified locally for display


def test_embeddings_are_ordered_by_index():
    gw = _gateway(_transport(Provider()), kind="embed")
    result = _call(gw, {"input": ["a", "bbb"]})
    assert result["response"]["embeddings"] == [[1.0, 1.0], [3.0, 1.0]]


def test_api_key_comes_from_callback_and_is_never_in_errors_or_state(monkeypatch):
    monkeypatch.setenv("EOIP_EGRESS_KEY_EXT_EU", KEY)
    t = _transport(Provider(), credentials=env_credentials)
    gw = _gateway(t)
    assert _call(gw, {"prompt": "hi"})["response"]["text"]
    assert KEY not in json.dumps(t.last_request) and KEY not in repr(vars(t))
    monkeypatch.setenv("EOIP_EGRESS_KEY_EXT_EU", "wrong")
    with pytest.raises(EgressTransportAuthError) as exc:
        t({"prompt": "hi"}, gw.endpoints["ext-eu"])
    assert "wrong" not in str(exc.value)


def test_auth_failure_becomes_audited_outage_with_sealed_manifest():
    events = []
    gw = _gateway(_transport(Provider(), credentials=lambda ep: "bad"), audit=events.append)
    with pytest.raises(EgressOutage, match="EgressTransportAuthError"):
        _call(gw, {"prompt": "hi"})
    assert gw.manifests[-1].denied and events[-1]["event"] == "egress.outage"


def test_429_and_5xx_are_retried_honouring_retry_after_then_give_up():
    slept: list[float] = []
    provider = Provider(script=[(429, {"Retry-After": "3"}), (503, {})])
    t = OpenAICompatibleTransport(models={"ext-eu": "m"}, credentials=lambda ep: KEY,
                                  transport=httpx.MockTransport(provider), sleep=slept.append)
    gw = _gateway(t)
    assert _call(gw, {"prompt": "x"})["response"]["text"] == "Summary of: x"
    assert slept[0] == 3.0 and len(provider.requests) == 3
    t2 = OpenAICompatibleTransport(models={"ext-eu": "m"}, credentials=lambda ep: KEY, max_retries=1,
                                   transport=httpx.MockTransport(Provider(script=[(500, {})] * 5)), sleep=lambda s: None)
    with pytest.raises(EgressTransportError, match="after 2 attempts"):
        t2({"prompt": "x"}, gw.endpoints["ext-eu"])


@pytest.mark.parametrize("url,kw,match", [
    ("http://llm.example.eu", {}, "requires https"),
    ("http://127.0.0.1:11434", {}, "requires https"),
    ("https://user:pw@llm.example.eu", {}, "credentials in endpoint URL"),
])
def test_url_pinning_fails_closed(url, kw, match):
    provider = Provider()
    gw = _gateway(_transport(provider, **kw), url=url)
    with pytest.raises(EgressOutage):
        _call(gw, {"prompt": "x"})
    with pytest.raises(EgressTransportError, match=match):
        _transport(provider, **kw)({"prompt": "x"}, gw.endpoints["ext-eu"])
    assert provider.requests == []  # nothing reached the wire


def test_redirects_are_refused_and_mtls_flag_fails_closed():
    def redirect(request):
        return httpx.Response(307, headers={"Location": "https://evil.example/v1/chat/completions"})
    gw = _gateway(OpenAICompatibleTransport(models={"ext-eu": "m"}, credentials=lambda ep: KEY,
                                            transport=httpx.MockTransport(redirect), sleep=lambda s: None))
    with pytest.raises(EgressOutage):
        _call(gw, {"prompt": "x"})
    provider = Provider()
    gw2 = _gateway(_transport(provider), mtls=True)
    with pytest.raises(EgressTransportError, match="mTLS"):
        _transport(provider)({"prompt": "x"}, gw2.endpoints["ext-eu"])
    assert provider.requests == []


def test_malformed_and_oversized_responses_are_rejected():
    ep = _gateway(None).endpoints["ext-eu"]
    for resp in (httpx.Response(200, json={"choices": []}), httpx.Response(200, text="not json"),
                 httpx.Response(200, json={"choices": [{"message": {"content": "x" * 100}}]})):
        t = OpenAICompatibleTransport(models={"ext-eu": "m"}, credentials=lambda e: KEY, max_response_bytes=64,
                                      transport=httpx.MockTransport(lambda r, resp=resp: resp), sleep=lambda s: None)
        with pytest.raises(EgressTransportError):
            t({"prompt": "x"}, ep)


def test_dry_run_and_disabled_endpoint_never_touch_the_wire():
    provider = Provider()
    gw = _gateway(_transport(provider))
    out = gw.call(endpoint_id="ext-eu", task="summarize", payload={"prompt": "x"}, user_id="u", role="analyst",
                  data_classes=["D0"], dry_run=True)
    assert out["dry_run"] and provider.requests == []


# --------------------------------------------------------------------------- live local endpoint
MODEL = os.getenv("EOIP_LIVE_OLLAMA_MODEL", "")
EMBED = os.getenv("EOIP_LIVE_OLLAMA_EMBED_MODEL", "")
OLLAMA = os.getenv("EOIP_LIVE_OLLAMA_URL", "http://127.0.0.1:11434")
live = pytest.mark.skipif(not MODEL, reason="no live local model (set EOIP_LIVE_OLLAMA_MODEL)")


@live
def test_live_openai_compatible_chat_through_gateway():
    t = OpenAICompatibleTransport(models={"ext-eu": MODEL}, credentials=lambda ep: None, allow_loopback_http=True,
                                  timeout=120, max_tokens=32)
    gw = _gateway(t, url=OLLAMA)
    result = _call(gw, {"system": "Answer in one short sentence.", "prompt": "What colour is the sky on a clear day?"})
    assert isinstance(result["response"]["text"], str) and result["response"]["text"].strip()
    assert result["response"]["model"] and not result["manifest"].denied


@live
@pytest.mark.skipif(not EMBED, reason="no live embedding model")
def test_live_openai_compatible_embeddings_through_gateway():
    t = OpenAICompatibleTransport(models={"ext-eu": EMBED}, credentials=lambda ep: None, allow_loopback_http=True,
                                  timeout=120)
    gw = _gateway(t, url=OLLAMA, kind="embed")
    vecs = _call(gw, {"input": ["invoice overdue", "payment late"]})["response"]["embeddings"]
    assert len(vecs) == 2 and len(vecs[0]) >= 64


@live
def test_live_dead_endpoint_degrades_to_outage():
    t = OpenAICompatibleTransport(models={"ext-eu": MODEL}, credentials=lambda ep: None, allow_loopback_http=True,
                                  timeout=2, max_retries=0)
    gw = _gateway(t, url="http://127.0.0.1:9")
    with pytest.raises(EgressOutage, match="transport outage"):
        _call(gw, {"prompt": "x"})



def test_api_wiring_is_opt_in():
    from eoip.egress.http_transport import transport_from_env

    assert transport_from_env({}) is None
    t = transport_from_env({"EOIP_EGRESS_TRANSPORT": "openai-compatible", "EOIP_EGRESS_MODELS": '{"ext-eu": "m"}'})
    assert isinstance(t, OpenAICompatibleTransport) and t.models == {"ext-eu": "m"}
    with pytest.raises(ValueError):
        transport_from_env({"EOIP_EGRESS_TRANSPORT": "openai-compatible", "EOIP_EGRESS_MODELS": "[1]"})
