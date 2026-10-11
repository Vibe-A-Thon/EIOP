"""Tests for Docker Compose smoke test manifest and operational boot contract (H-06)."""

from pathlib import Path
import pytest
import yaml

COMPOSE_PATH = Path(__file__).resolve().parents[2] / "deploy" / "docker-compose.yml"
SMOKE_TEST_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "smoke_test.py"


@pytest.mark.req("H-06")
def test_docker_compose_manifest_services_and_healthchecks_exist():
    assert COMPOSE_PATH.exists(), "deploy/docker-compose.yml must exist"
    data = yaml.safe_load(COMPOSE_PATH.read_text(encoding="utf-8"))
    services = data.get("services", {})
    
    # Required core services for EOIP deployment
    assert "hugegraph-server" in services, "hugegraph-server service must be defined"
    assert "eoip-api" in services, "eoip-api service must be defined"
    assert "eoip-web" in services, "eoip-web service must be defined"

    # API depends on schema-init, which in turn waits for hugegraph-server to be healthy
    api_depends = services["eoip-api"].get("depends_on", {})
    assert "schema-init" in api_depends, "eoip-api must depend on schema-init"
    assert "hugegraph-server" in services["schema-init"].get("depends_on", {}), "schema-init must depend on hugegraph-server"
    assert "healthcheck" in services["hugegraph-server"], "hugegraph-server must have healthcheck"


@pytest.mark.req("H-06")
def test_smoke_test_script_is_present_and_executable():
    assert SMOKE_TEST_SCRIPT.exists(), "scripts/smoke_test.py must exist"
    content = SMOKE_TEST_SCRIPT.read_text(encoding="utf-8")
    assert "health/ready" in content, "smoke test must check /health/ready"
    assert "api/v1/search" in content, "smoke test must check search endpoint"
    assert "api/v1/path" in content, "smoke test must check path traversal"
