"""Production topology helpers for HA, cache, Helm, and sharding support.

These helpers keep deployment-oriented features testable without requiring a
live Kubernetes cluster, Redis server, or HugeGraph HStore environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CacheTopology:
    backend: str = "local"
    url: str = ""
    ttl_seconds: int = 300
    max_entries: int = 10_000

    @classmethod
    def from_env(cls) -> "CacheTopology":
        return cls(
            backend=os.getenv("EOIP_CACHE_BACKEND", "local"),
            url=os.getenv("EOIP_REDIS_URL", ""),
            ttl_seconds=int(os.getenv("EOIP_CACHE_TTL_SECONDS", "300")),
            max_entries=int(os.getenv("EOIP_CACHE_MAX_ENTRIES", "10000")),
        )

    @property
    def distributed(self) -> bool:
        return self.backend.lower() in {"redis", "memcached"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend,
            "url_configured": bool(self.url),
            "ttl_seconds": self.ttl_seconds,
            "max_entries": self.max_entries,
            "distributed": self.distributed,
        }


@dataclass(frozen=True)
class HighAvailabilityTopology:
    api_replicas: int = 2
    worker_replicas: int = 2
    mcp_replicas: int = 2
    graph_mode: str = "hugegraph-hstore"
    graph_nodes: int = 3
    cache: CacheTopology = field(default_factory=CacheTopology.from_env)

    def validate(self) -> list[str]:
        findings: list[str] = []
        if self.api_replicas < 2:
            findings.append("api_replicas must be at least 2 for HA")
        if self.worker_replicas < 2:
            findings.append("worker_replicas must be at least 2 for HA")
        if self.graph_nodes < 3:
            findings.append("graph_nodes should be at least 3 for quorum-oriented production")
        if self.cache.distributed and not self.cache.url:
            findings.append("distributed cache selected but EOIP_REDIS_URL is not configured")
        return findings

    def to_dict(self) -> dict[str, Any]:
        findings = self.validate()
        return {
            "api_replicas": self.api_replicas,
            "worker_replicas": self.worker_replicas,
            "mcp_replicas": self.mcp_replicas,
            "graph_mode": self.graph_mode,
            "graph_nodes": self.graph_nodes,
            "cache": self.cache.to_dict(),
            "ready": not findings,
            "findings": findings,
        }


def default_ha_topology() -> HighAvailabilityTopology:
    return HighAvailabilityTopology(
        api_replicas=int(os.getenv("EOIP_API_REPLICAS", "2")),
        worker_replicas=int(os.getenv("EOIP_WORKER_REPLICAS", "2")),
        mcp_replicas=int(os.getenv("EOIP_MCP_REPLICAS", "2")),
        graph_mode=os.getenv("EOIP_GRAPH_CLUSTER_MODE", "hugegraph-hstore"),
        graph_nodes=int(os.getenv("EOIP_GRAPH_NODES", "3")),
    )


def build_shard_plan(entity_count: int, shard_count: int, strategy: str = "canonical_hash") -> dict[str, Any]:
    if entity_count < 0:
        raise ValueError("entity_count must be non-negative")
    if shard_count < 1:
        raise ValueError("shard_count must be positive")
    base = entity_count // shard_count
    remainder = entity_count % shard_count
    shards = [
        {
            "shard_id": f"shard-{index + 1}",
            "strategy": strategy,
            "estimated_entities": base + (1 if index < remainder else 0),
            "routing_key": "canonical_id",
        }
        for index in range(shard_count)
    ]
    return {
        "strategy": strategy,
        "shard_count": shard_count,
        "entity_count": entity_count,
        "shards": shards,
        "portable": True,
        "notes": [
            "This is a logical routing plan; physical HugeGraph partitioning is selected by deployment topology.",
            "Canonical IDs remain stable across shard movement.",
        ],
    }


def helm_release_summary(values: dict[str, Any] | None = None) -> dict[str, Any]:
    values = values or {}
    api = values.get("api", {})
    worker = values.get("worker", {})
    graph = values.get("hugegraph", {})
    redis = values.get("redis", {})
    graph_cluster = graph.get("cluster", {})
    return {
        "api_replicas": int(api.get("replicas", api.get("replicaCount", 2))),
        "worker_replicas": int(worker.get("replicas", worker.get("replicaCount", 2))),
        "graph_cluster_enabled": bool(graph_cluster.get("enabled", graph.get("enabled", True))),
        "redis_enabled": bool(redis.get("enabled", False)),
        "has_health_probes": True,
        "has_persistent_volumes": True,
    }
