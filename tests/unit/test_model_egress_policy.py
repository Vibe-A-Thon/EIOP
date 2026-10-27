"""Tests for CC3-001: Model egress policy and local endpoint restriction (SR-LLM-002)."""

import pytest
from eoip.models.provider import (
    LocalModelProvider,
    ModelUnavailable,
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
