"""Tests for CC3-001: Model egress policy and local endpoint restriction (SR-LLM-002)."""

import pytest
from eoip.models.provider import (
    LocalModelProvider,
    ModelUnavailable,
    create_model_provider,
    validate_model_endpoint_url,
)


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost:11434",
        "http://127.0.0.1:11434",
        "http://[::1]:11434",
        "http://local-model:11434",
        "https://localhost:8443",
    ],
)
def test_allowed_local_endpoints(url):
    # Should not raise
    validate_model_endpoint_url(url)
    provider = LocalModelProvider(url=url)
    assert provider._url == url


@pytest.mark.parametrize(
    "url,reason",
    [
        ("ftp://localhost:11434", "scheme"),
        ("file:///etc/passwd", "scheme"),
        ("http://169.254.169.254/latest/meta-data", "metadata"),
        ("http://169.254.170.2/v2/metadata", "metadata"),
        ("http://metadata.google.internal/computeMetadata/v1", "metadata"),
        ("http://169.254.1.1:11434", "link-local"),
        ("http://evil.com:11434", "unauthorized"),
        ("http://api.openai.com/v1", "unauthorized"),
        ("http://10.0.0.5:11434", "unauthorized"),
        ("http://", "missing host"),
    ],
)
def test_disallowed_endpoints_fail_closed(url, reason):
    with pytest.raises(ModelUnavailable) as exc_info:
        validate_model_endpoint_url(url)
    assert "Egress policy violation" in str(exc_info.value) or "missing host" in str(exc_info.value)

    with pytest.raises(ModelUnavailable):
        LocalModelProvider(url=url)


def test_custom_allowed_hosts_via_env(monkeypatch):
    monkeypatch.setenv("EOIP_ALLOWED_MODEL_HOSTS", "custom-model-cluster.internal, trusted-ai-node")
    validate_model_endpoint_url("http://custom-model-cluster.internal:11434")
    validate_model_endpoint_url("http://trusted-ai-node:8000")

    with pytest.raises(ModelUnavailable):
        validate_model_endpoint_url("http://untrusted-host:8000")


def test_trailing_dot_and_case_normalized():
    # "localhost." and "LOCALHOST" must not bypass the allowlist via naive parsing
    validate_model_endpoint_url("http://LOCALHOST.:11434")
    validate_model_endpoint_url("http://127.0.0.1.:11434")


def test_userinfo_rejected():
    # authority confusion: the real host is after "@", never trust userinfo
    with pytest.raises(ModelUnavailable):
        validate_model_endpoint_url("http://user:pass@localhost:11434")


def test_non_local_profile_rejected():
    with pytest.raises(ModelUnavailable):
        validate_model_endpoint_url("http://localhost:11434", profile="remote")
    with pytest.raises(ModelUnavailable):
        LocalModelProvider(url="http://localhost:11434", profile="remote")


def test_unspecified_ip_rejected():
    with pytest.raises(ModelUnavailable):
        validate_model_endpoint_url("http://0.0.0.0:11434")


def _redirecting_client(monkeypatch, status=302, location="http://evil.example/"):
    import httpx

    real_client = httpx.Client

    def factory(**kwargs):
        return real_client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(status, headers={"location": location})
            ),
            **kwargs,
        )

    monkeypatch.setattr(httpx, "Client", factory)


def test_redirect_refused(monkeypatch):
    _redirecting_client(monkeypatch)
    provider = LocalModelProvider(model="m", url="http://localhost:11434")
    with pytest.raises(ModelUnavailable, match="redirect"):
        provider.generate("sys", "user")
    with pytest.raises(ModelUnavailable, match="redirect"):
        provider.generate_raw("prompt")
    with pytest.raises(ModelUnavailable, match="redirect"):
        list(provider.stream_raw("prompt"))
    # health() never treats a redirect as healthy
    assert provider.health() is False


def test_dns_rebinding_to_metadata_rejected(monkeypatch):
    import socket as socket_module

    def fake_getaddrinfo(host, port, *args, **kwargs):
        return [(socket_module.AF_INET, 0, 0, "", ("169.254.169.254", 0))]

    monkeypatch.setattr("eoip.models.provider.socket.getaddrinfo", fake_getaddrinfo)
    provider = LocalModelProvider(model="m", url="http://localhost:11434")
    with pytest.raises(ModelUnavailable, match="denied address"):
        provider.generate("sys", "user")


def test_dns_resolution_failure_fails_closed(monkeypatch):
    import socket as socket_module

    def fake_getaddrinfo(host, port, *args, **kwargs):
        raise socket_module.gaierror("name resolution failed")

    monkeypatch.setattr("eoip.models.provider.socket.getaddrinfo", fake_getaddrinfo)
    provider = LocalModelProvider(model="m", url="http://localhost:11434")
    with pytest.raises(ModelUnavailable, match="cannot be resolved"):
        provider.generate("sys", "user")
    assert provider.health() is False


def test_localhost_allowed_in_local_profile():
    provider = create_model_provider(model="m", url="http://localhost:11434")
    assert provider.available
    assert provider.model_name == "m"


def test_port_http_adapter_validates_url():
    from eoip.models.port import Capability, ModelCapabilities, http_chat_adapter

    caps = ModelCapabilities(capabilities=frozenset({Capability.CHAT}), context_length=8192)
    http_chat_adapter("ok", "ollama", url="http://localhost:11434", model="m", caps=caps)
    with pytest.raises(ModelUnavailable):
        http_chat_adapter("bad", "ollama", url="http://169.254.169.254/latest/meta-data", model="m", caps=caps)
    with pytest.raises(ModelUnavailable):
        http_chat_adapter("bad2", "ollama", url="ftp://localhost:11434", model="m", caps=caps)


def test_live_call_sites_use_shared_factory():
    """All live model call sites construct the provider via the shared hardened factory (CC3-001)."""
    import apps.api.main as api_main
    import eoip.query.nl as nl
    import eoip.retrieval.service as retrieval_service

    assert api_main.create_model_provider is create_model_provider
    assert nl.create_model_provider is create_model_provider
    assert retrieval_service.create_model_provider is create_model_provider
