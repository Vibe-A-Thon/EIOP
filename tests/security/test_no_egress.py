"""NFR-SEC-001: No outbound enterprise-data egress.

Validates that the Docker Compose deployment configures internal networks
to prevent outbound data egress from backend services. These are structural
tests against the compose manifest; live network tests require a running
Docker environment.
"""

from pathlib import Path

import pytest
import yaml

COMPOSE_PATH = Path(__file__).resolve().parents[2] / "deploy" / "docker-compose.yml"


def _load_compose():
    return yaml.safe_load(COMPOSE_PATH.read_text(encoding="utf-8"))


@pytest.mark.req("NFR-SEC-001")
def test_backend_network_is_internal():
    """The backend network must be declared as internal to block egress."""
    compose = _load_compose()
    networks = compose.get("networks", {})
    assert "backend" in networks, "backend network not defined"
    assert networks["backend"].get("internal") is True, (
        "backend network must be internal: true to prevent egress"
    )


def test_hugegraph_only_on_backend():
    """HugeGraph must only be on the internal backend network."""
    compose = _load_compose()
    hg = compose["services"]["hugegraph-server"]
    networks = hg.get("networks", [])
    assert networks == ["backend"], (
        f"HugeGraph must be on backend only, found: {networks}"
    )
    assert "ports" not in hg, "HugeGraph must not expose ports externally"


def test_local_model_only_on_backend():
    """The local model service must only be on the internal backend network."""
    compose = _load_compose()
    model = compose["services"]["local-model"]
    networks = model.get("networks", [])
    assert networks == ["backend"], (
        f"local-model must be on backend only, found: {networks}"
    )
    assert "ports" not in model, "local-model must not expose ports externally"


def test_api_ports_bound_to_loopback():
    """API, MCP, and web ports must bind to 127.0.0.1 only."""
    compose = _load_compose()
    for svc_name in ["eoip-api", "eoip-mcp", "eoip-web", "hubble"]:
        svc = compose["services"][svc_name]
        ports = svc.get("ports", [])
        for port in ports:
            assert str(port).startswith("127.0.0.1:"), (
                f"{svc_name} port {port} must bind to 127.0.0.1"
            )


def test_no_host_network_mode():
    """No service should use host network mode."""
    compose = _load_compose()
    for name, svc in compose["services"].items():
        assert svc.get("network_mode") != "host", (
            f"Service {name} must not use host network mode"
        )


def test_application_services_include_backend():
    """All application services must be on the backend network for HugeGraph access."""
    compose = _load_compose()
    app_services = ["eoip-api", "eoip-worker", "eoip-mcp"]
    for svc_name in app_services:
        svc = compose["services"][svc_name]
        networks = svc.get("networks", [])
        assert "backend" in networks, (
            f"{svc_name} must include backend network for HugeGraph access"
        )
