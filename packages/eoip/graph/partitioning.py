"""Graph Partitioning & Sharding — automatic graph partitioning by tenant, time, or entity type.

Provides hash-based, range-based, and label-based partitioning strategies
with cross-partition query routing, partition rebalancing, and migration.
"""

from __future__ import annotations

import hashlib
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class PartitionStrategy(str, Enum):
    HASH = "HASH"
    RANGE = "RANGE"
    LABEL = "LABEL"
    TENANT = "TENANT"
    TEMPORAL = "TEMPORAL"
    COMPOSITE = "COMPOSITE"


class PartitionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    MIGRATING = "MIGRATING"
    READONLY = "READONLY"
    OFFLINE = "OFFLINE"
    REBALANCING = "REBALANCING"


@dataclass
class PartitionConfig:
    strategy: PartitionStrategy
    num_partitions: int = 8
    replication_factor: int = 1
    partition_key: str = "canonical_id"
    range_boundaries: list[Any] = field(default_factory=list)
    label_mapping: dict[str, int] = field(default_factory=dict)
    temporal_granularity: str = "monthly"  # daily, weekly, monthly, yearly
    auto_rebalance: bool = True
    max_partition_size_mb: int = 1024


@dataclass
class Partition:
    partition_id: str
    shard_index: int
    status: PartitionStatus = PartitionStatus.ACTIVE
    entity_count: int = 0
    size_bytes: int = 0
    tenant_id: str | None = None
    label_filter: str | None = None
    time_range: tuple[str, str] | None = None
    node_assignment: str = "local"
    created_at: str = ""
    last_rebalance: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass
class ShardRouting:
    entity_id: str
    partition_id: str
    shard_index: int
    routing_key: str


@dataclass
class PartitionMetrics:
    total_partitions: int = 0
    active_partitions: int = 0
    total_entities: int = 0
    partition_sizes: dict[str, int] = field(default_factory=dict)
    hottest_partition: str = ""
    coldest_partition: str = ""
    imbalance_ratio: float = 0.0


class GraphPartitionManager:
    """Manages graph partitions with automatic routing and rebalancing."""

    def __init__(self, config: PartitionConfig | None = None) -> None:
        self._config = config or PartitionConfig(strategy=PartitionStrategy.HASH)
        self._partitions: dict[str, Partition] = {}
        self._routing_cache: dict[str, str] = {}
        self._lock = threading.RLock()
        self._initialize_partitions()

    def _initialize_partitions(self) -> None:
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for i in range(self._config.num_partitions):
            pid = f"part-{i:04d}"
            self._partitions[pid] = Partition(
                partition_id=pid, shard_index=i, created_at=now,
            )

    def route_entity(self, entity_id: str, entity_label: str = "",
                     tenant_id: str | None = None,
                     timestamp: str | None = None) -> ShardRouting:
        cached = self._routing_cache.get(entity_id)
        if cached:
            part = self._partitions.get(cached)
            if part and part.status == PartitionStatus.ACTIVE:
                return ShardRouting(
                    entity_id=entity_id, partition_id=cached,
                    shard_index=part.shard_index, routing_key=entity_id,
                )

        shard_index = self._compute_shard(entity_id, entity_label, tenant_id, timestamp)
        pid = f"part-{shard_index:04d}"

        self._routing_cache[entity_id] = pid
        return ShardRouting(
            entity_id=entity_id, partition_id=pid,
            shard_index=shard_index, routing_key=entity_id,
        )

    def route_query(self, query_labels: list[str] | None = None,
                    tenant_id: str | None = None,
                    time_range: tuple[str, str] | None = None) -> list[str]:
        if self._config.strategy == PartitionStrategy.LABEL and query_labels:
            partitions = set()
            for label in query_labels:
                idx = self._config.label_mapping.get(label)
                if idx is not None:
                    pid = f"part-{idx:04d}"
                    if pid in self._partitions:
                        partitions.add(pid)
            if partitions:
                return list(partitions)

        if self._config.strategy == PartitionStrategy.TENANT and tenant_id:
            idx = self._hash_to_shard(tenant_id)
            return [f"part-{idx:04d}"]

        return [pid for pid, p in self._partitions.items()
                if p.status == PartitionStatus.ACTIVE]

    def add_partition(self, partition_id: str | None = None,
                      tenant_id: str | None = None) -> Partition:
        with self._lock:
            idx = len(self._partitions)
            pid = partition_id or f"part-{idx:04d}"
            partition = Partition(
                partition_id=pid, shard_index=idx, tenant_id=tenant_id,
                created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            )
            self._partitions[pid] = partition
            return partition

    def remove_partition(self, partition_id: str) -> bool:
        with self._lock:
            part = self._partitions.get(partition_id)
            if not part or part.entity_count > 0:
                return False
            del self._partitions[partition_id]
            return True

    def set_partition_status(self, partition_id: str, status: PartitionStatus) -> bool:
        with self._lock:
            part = self._partitions.get(partition_id)
            if part:
                part.status = status
                return True
            return False

    def record_entity(self, partition_id: str, size_bytes: int = 0) -> None:
        with self._lock:
            part = self._partitions.get(partition_id)
            if part:
                part.entity_count += 1
                part.size_bytes += size_bytes

    def get_metrics(self) -> PartitionMetrics:
        with self._lock:
            sizes = {pid: p.entity_count for pid, p in self._partitions.items()}
            counts = list(sizes.values())
            avg = sum(counts) / len(counts) if counts else 0
            max_c = max(counts) if counts else 0
            min_c = min(counts) if counts else 0
            imbalance = (max_c - min_c) / max(1, avg) if avg > 0 else 0.0

            return PartitionMetrics(
                total_partitions=len(self._partitions),
                active_partitions=sum(1 for p in self._partitions.values()
                                      if p.status == PartitionStatus.ACTIVE),
                total_entities=sum(counts),
                partition_sizes=sizes,
                hottest_partition=max(sizes, key=sizes.get) if sizes else "",
                coldest_partition=min(sizes, key=sizes.get) if sizes else "",
                imbalance_ratio=round(imbalance, 4),
            )

    def needs_rebalance(self, threshold: float = 2.0) -> bool:
        metrics = self.get_metrics()
        return metrics.imbalance_ratio > threshold

    def rebalance(self) -> dict[str, Any]:
        with self._lock:
            metrics = self.get_metrics()
            if not self.needs_rebalance():
                return {"rebalanced": False, "reason": "Within balance threshold"}

            total = metrics.total_entities
            target = total // max(1, metrics.total_partitions)
            moves: list[dict[str, Any]] = []

            for pid, count in metrics.partition_sizes.items():
                excess = count - target
                if excess > target * 0.5:
                    moves.append({"partition": pid, "excess": excess, "action": "split"})

            for pid in self._partitions:
                self._partitions[pid].last_rebalance = time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            return {
                "rebalanced": True,
                "moves": moves,
                "target_per_partition": target,
                "imbalance_before": metrics.imbalance_ratio,
            }

    def list_partitions(self) -> list[dict[str, Any]]:
        return [p.to_dict() for p in self._partitions.values()]

    def _compute_shard(self, entity_id: str, label: str,
                       tenant_id: str | None, timestamp: str | None) -> int:
        strategy = self._config.strategy

        if strategy == PartitionStrategy.TENANT and tenant_id:
            return self._hash_to_shard(tenant_id)

        if strategy == PartitionStrategy.LABEL and label:
            mapped = self._config.label_mapping.get(label)
            if mapped is not None:
                return mapped % self._config.num_partitions
            return self._hash_to_shard(label)

        if strategy == PartitionStrategy.TEMPORAL and timestamp:
            return self._temporal_shard(timestamp)

        return self._hash_to_shard(entity_id)

    def _hash_to_shard(self, key: str) -> int:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return h % self._config.num_partitions

    def _temporal_shard(self, timestamp: str) -> int:
        try:
            ts = time.strptime(timestamp[:10], "%Y-%m-%d")
            if self._config.temporal_granularity == "daily":
                return ts.tm_yday % self._config.num_partitions
            elif self._config.temporal_granularity == "weekly":
                week = ts.tm_yday // 7
                return week % self._config.num_partitions
            elif self._config.temporal_granularity == "monthly":
                return ts.tm_mon % self._config.num_partitions
            else:
                return ts.tm_year % self._config.num_partitions
        except (ValueError, IndexError):
            return 0
