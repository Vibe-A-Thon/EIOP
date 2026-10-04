"""NFR-SEC-006: Container hardening.

Validates that the Docker Compose deployment applies security hardening:
non-root where practical, no-new-privileges, dropped capabilities,
healthchecks, and private networks. These are structural tests against
the compose manifest.
"""

import yaml
from pathlib import Path

COMPOSE_PATH = Path(__file__).resolve().parents[2] / "deploy" / "docker-compose.yml"


def _load_compose():
    return yaml.safe_load(COMPOSE_PATH.read_text(encoding="utf-8"))


def _get_effective_service(compose, name):
    """Resolve YAML anchors by reading the raw dict."""
    svc = compose["services"][name]
    anchor = compose.get("x-application", {})
    if "<<" in svc:
        merged = dict(anchor)
        merged.update({k: v for k, v in svc.items() if k != "<<"})
        return merged
    return svc


def test_application_anchor_drops_all_capabilities():
    """The shared application anchor must drop ALL capabilities."""
    compose = _load_compose()
    anchor = compose.get("x-application", {})
    cap_drop = anchor.get("cap_drop", [])
    assert "ALL" in cap_drop, (
        f"x-application must cap_drop ALL, found: {cap_drop}"
    )


def test_application_anchor_no_new_privileges():
    """The shared application anchor must set no-new-privileges."""
    compose = _load_compose()
    anchor = compose.get("x-application", {})
    security_opt = anchor.get("security_opt", [])
    assert "no-new-privileges:true" in security_opt, (
        f"x-application must set no-new-privileges:true, found: {security_opt}"
    )


def test_application_anchor_uses_init():
    """The shared application anchor must use init for proper signal handling."""
    compose = _load_compose()
    anchor = compose.get("x-application", {})
    assert anchor.get("init") is True, (
        "x-application must set init: true for proper PID 1 signal handling"
    )


def test_all_long_running_services_have_healthchecks():
    """All long-running services must define healthchecks."""
    compose = _load_compose()
    long_running = [
        "hugegraph-server", "eoip-api", "eoip-worker",
        "eoip-mcp", "eoip-web",
    ]
    for svc_name in long_running:
        svc = compose["services"][svc_name]
        assert "healthcheck" in svc, (
            f"Service {svc_name} must define a healthcheck"
        )
        hc = svc["healthcheck"]
        assert "test" in hc, f"{svc_name} healthcheck must have a test command"


def test_hugegraph_not_on_frontend():
    """HugeGraph must not be on the frontend network."""
    compose = _load_compose()
    hg = compose["services"]["hugegraph-server"]
    networks = hg.get("networks", [])
    assert "frontend" not in networks, (
        "HugeGraph must not be exposed on the frontend network"
    )


def test_backend_network_isolates_internal_services():
    """The backend network must be internal to isolate HugeGraph and model."""
    compose = _load_compose()
    assert compose["networks"]["backend"].get("internal") is True


def test_restart_policies():
    """Long-running services must have restart policies."""
    compose = _load_compose()
    for svc_name in ["hugegraph-server", "eoip-api", "eoip-worker", "eoip-mcp", "eoip-web"]:
        svc = compose["services"][svc_name]
        assert svc.get("restart") == "unless-stopped", (
            f"{svc_name} must have restart: unless-stopped"
        )


def test_schema_init_no_restart():
    """The schema-init service must not restart (one-shot task)."""
    compose = _load_compose()
    svc = compose["services"]["schema-init"]
    assert svc.get("restart") == "no", (
        "schema-init must have restart: no (one-shot)"
    )
