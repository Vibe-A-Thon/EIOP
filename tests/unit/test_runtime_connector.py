import pytest
import eoip.connectors.runtime_infra as runtime_module
from eoip.connectors.runtime_infra import RuntimeInfraConnector


@pytest.mark.req("G2-SRC-RUNTIME-002")
def test_runtime_infra_resource_discovery_and_extraction(monkeypatch):
    monkeypatch.setattr(runtime_module, "_K8S_AVAILABLE", True)
    connector = RuntimeInfraConnector(source_id="k8s-prod", namespace="payments")

    discovery = connector.discover()
    assert discovery.source_id == "k8s-prod"
    res_ids = [r.resource_id for r in discovery.resources]
    assert "pods" in res_ids
    assert "deployments" in res_ids
    assert "services" in res_ids

    resources = [
        {
            "kind": "pod",
            "name": "payment-api-7b8f9-abcd",
            "namespace": "payments",
            "node_name": "worker-pool-node-3",
            "phase": "Running",
            "containers": [{"name": "payment-api", "image": "payments:v2.1.0", "ready": True}],
            "resource_version": "1849204",
        },
        {
            "kind": "deployment",
            "name": "payment-api",
            "namespace": "payments",
            "replicas": 3,
            "available_replicas": 3,
            "resource_version": "1849100",
        },
    ]
    events = connector.extract(resources)
    assert len(events) == 2
    assert events[0].metadata["record_kind"] == "pod"
    assert "payment-api-7b8f9-abcd" in events[0].source_record_id
    assert events[0].source_version == "1849204"
    assert events[1].metadata["record_kind"] == "deployment"
    assert events[1].payload["replicas"] == 3


@pytest.mark.req("G2-SRC-RUNTIME-003")
def test_runtime_infra_dependency_handling_and_health(monkeypatch):
    # Test unavailable state
    monkeypatch.setattr(runtime_module, "_K8S_AVAILABLE", False)
    connector = RuntimeInfraConnector(source_id="k8s-local")

    health = connector.health()
    assert health.status == "UNAVAILABLE"
    assert "kubernetes client is not installed" in health.detail

    with pytest.raises(ImportError, match="kubernetes client is required"):
        connector.extract([{"kind": "pod", "name": "pod-1"}])

    # Test healthy state
    monkeypatch.setattr(runtime_module, "_K8S_AVAILABLE", True)
    assert connector.health().status == "HEALTHY"
    assert connector.checkpoint() is None
