from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_ha_compose_overlay_declares_replicated_services() -> None:
    data = yaml.safe_load((ROOT / "deploy/docker-compose.ha.yml").read_text())
    services = data["services"]
    assert services["api-lb"]["depends_on"]["eoip-api-1"]["condition"] == "service_healthy"
    assert services["api-lb"]["depends_on"]["eoip-api-2"]["condition"] == "service_healthy"
    assert services["eoip-api-1"]["healthcheck"]
    assert services["eoip-api-2"]["healthcheck"]
    assert services["eoip-worker-1"]["environment"]["EOIP_LEASE_PATH"] == "/leases/worker.lock"
    assert services["eoip-worker-2"]["environment"]["EOIP_LEASE_PATH"] == "/leases/worker.lock"
    assert services["hugegraph-pd"]["profiles"] == ["hugegraph-distributed"]
    assert services["hugegraph-store-1"]["profiles"] == ["hugegraph-distributed"]


def test_helm_chart_contains_ha_defaults_and_probes() -> None:
    values = yaml.safe_load((ROOT / "deploy/helm/eoip/values.yaml").read_text())
    assert values["api"]["replicaCount"] == 2
    assert values["worker"]["replicaCount"] == 2
    assert values["hpa"]["enabled"] is True
    assert values["hpa"]["minReplicas"] == 2
    assert values["hugegraph"]["enabled"] is True
    assert values["redis"]["enabled"] is False

    deployment = (ROOT / "deploy/helm/eoip/templates/deployment.yaml").read_text()
    assert "readinessProbe" in deployment
    assert "livenessProbe" in deployment
    assert "EOIP_REDIS_URL" in deployment
    redis = (ROOT / "deploy/helm/eoip/templates/redis.yaml").read_text()
    assert "{{- if .Values.redis.enabled }}" in redis
    assert "kind: Service" in redis
