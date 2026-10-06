from eoip.ops.production import (
    CacheTopology,
    HighAvailabilityTopology,
    build_shard_plan,
    helm_release_summary,
)


def test_ha_topology_validates_replicas_and_cache() -> None:
    topology = HighAvailabilityTopology(
        api_replicas=2,
        worker_replicas=2,
        graph_nodes=3,
        cache=CacheTopology(backend="redis", url="redis://cache:6379/0"),
    )
    assert topology.to_dict()["ready"] is True
    assert topology.to_dict()["cache"]["distributed"] is True


def test_ha_topology_reports_missing_quorum() -> None:
    topology = HighAvailabilityTopology(api_replicas=1, worker_replicas=1, graph_nodes=1)
    findings = topology.validate()
    assert any("api_replicas" in item for item in findings)
    assert any("graph_nodes" in item for item in findings)


def test_shard_plan_keeps_stable_canonical_routing() -> None:
    plan = build_shard_plan(entity_count=10, shard_count=3)
    assert plan["shard_count"] == 3
    assert sum(shard["estimated_entities"] for shard in plan["shards"]) == 10
    assert {shard["routing_key"] for shard in plan["shards"]} == {"canonical_id"}


def test_helm_release_summary_defaults_to_production_ready_topology() -> None:
    summary = helm_release_summary({})
    assert summary["api_replicas"] == 2
    assert summary["worker_replicas"] == 2
    assert summary["graph_cluster_enabled"] is True
    assert summary["redis_enabled"] is False


def test_helm_release_summary_accepts_chart_value_names() -> None:
    summary = helm_release_summary(
        {
            "api": {"replicaCount": 3},
            "worker": {"replicaCount": 4},
            "hugegraph": {"enabled": True},
            "redis": {"enabled": True},
        }
    )
    assert summary["api_replicas"] == 3
    assert summary["worker_replicas"] == 4
    assert summary["graph_cluster_enabled"] is True
    assert summary["redis_enabled"] is True
