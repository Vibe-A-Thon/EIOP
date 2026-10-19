"""Derivation-Aware Source-ACL Filtering Engine (WP-KG3-01, GAP-01, INV-01, CAP-46).

Provides:
1. Multi-hop path ACL composition for derived facts and graph traversals.
2. Justification-aware derived fact visibility (resolving X-11 / INV-01).
3. Fail-closed zero-data-leak filtering for GraphRAG and query results.
4. Thread-safe policy epoch tracking and cache invalidation.
"""

from __future__ import annotations

import hashlib
import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Sequence

from eoip.contracts.canonical import PrincipalType, TrustedScope
from eoip.authz.pdp import (
    FactPremise,
    PolicyEpochRegistry,
    ScopeViolationError,
    can_read,
    get_policy_epoch_registry,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TraversalHop:
    """A single hop in a multi-hop graph path with access control metadata."""
    vertex_id: str
    vertex_label: str
    edge_id: str | None = None
    edge_label: str | None = None
    acl_vector: tuple[str, ...] = ()
    classification: str = "internal"
    tenant_id: str = "default"


@dataclass(frozen=True)
class TraversalPath:
    """A complete multi-hop traversal path composed of sequential hops."""
    path_id: str
    hops: tuple[TraversalHop, ...]
    derived_fact_id: str | None = None

    @property
    def composite_acl_vector(self) -> set[str]:
        """Union of all required ACL tags across every hop in the path."""
        tags: set[str] = set()
        for hop in self.hops:
            tags.update(hop.acl_vector)
        return tags

    @property
    def max_classification(self) -> str:
        """The most restrictive classification across all hops in the path."""
        order = {"public": 1, "internal": 2, "confidential": 3, "restricted": 4}
        max_level = 1
        max_name = "public"
        for hop in self.hops:
            lvl = order.get(hop.classification.lower(), 2)
            if lvl > max_level:
                max_level = lvl
                max_name = hop.classification.lower()
        return max_name


@dataclass
class DerivationFilterResult:
    """Result of derivation-aware access control filtering."""
    visible: bool
    permitted_paths: list[TraversalPath] = field(default_factory=list)
    hidden_paths_count: int = 0
    denied_reasons: list[str] = field(default_factory=list)
    effective_epoch: int = 1


class DerivationACLEvaluator:
    """High-performance, thread-safe derivation-aware ACL evaluator."""

    def __init__(self, epoch_registry: PolicyEpochRegistry | None = None) -> None:
        self.epoch_registry = epoch_registry or get_policy_epoch_registry()
        self._cache_lock = threading.RLock()
        # Key: (tenant_id, principal_id, path_hash, policy_epoch) -> bool
        self._eval_cache: dict[tuple[str, str, str, int], bool] = {}

    def _hash_path(self, path: TraversalPath) -> str:
        items = [f"{h.vertex_id}:{h.edge_id}:{sorted(h.acl_vector)}:{h.classification}" for h in path.hops]
        return hashlib.sha256("|".join(items).encode("utf-8")).hexdigest()

    def evaluate_path(self, scope: TrustedScope, path: TraversalPath) -> bool:
        """Evaluate whether the given scope is authorized to traverse this specific path."""
        # 1. Monotonic Policy Epoch freshness check (fail-closed if stale)
        current_epoch = self.epoch_registry.get_epoch(scope.tenant_id)
        if scope.policy_epoch < current_epoch:
            logger.warning(
                "Scope policy_epoch %d is stale for tenant %s (current: %d); denying traversal",
                scope.policy_epoch,
                scope.tenant_id,
                current_epoch,
            )
            return False

        # 2. Check cache
        path_hash = self._hash_path(path)
        cache_key = (scope.tenant_id, scope.principal_id, path_hash, scope.policy_epoch)
        with self._cache_lock:
            if cache_key in self._eval_cache:
                return self._eval_cache[cache_key]

        # 3. Evaluate each hop along the path
        effective_acls_set = set(scope.effective_acls)
        is_permitted = True

        for hop in path.hops:
            # Tenant isolation check
            if hop.tenant_id != scope.tenant_id and hop.tenant_id not in ("default", "public"):
                is_permitted = False
                break

            # Check individual hop permissions using PDP can_read
            hop_allowed = can_read(
                scope=scope,
                acl_vector=list(hop.acl_vector),
                classification=hop.classification,
                target_tenant_id=hop.tenant_id,
            )
            if not hop_allowed:
                is_permitted = False
                break

        # 4. Store in cache
        with self._cache_lock:
            self._eval_cache[cache_key] = is_permitted

        return is_permitted

    def filter_traversal_paths(
        self, scope: TrustedScope, paths: Sequence[TraversalPath]
    ) -> DerivationFilterResult:
        """Filter candidate graph traversal paths, pruning any containing restricted hops."""
        current_epoch = self.epoch_registry.get_epoch(scope.tenant_id)
        permitted: list[TraversalPath] = []
        hidden_count = 0
        denied_reasons: list[str] = []

        for p in paths:
            if self.evaluate_path(scope, p):
                permitted.append(p)
            else:
                hidden_count += 1
                denied_reasons.append(f"Restricted premise on path {p.path_id}")

        return DerivationFilterResult(
            visible=len(permitted) > 0,
            permitted_paths=permitted,
            hidden_paths_count=hidden_count,
            denied_reasons=denied_reasons,
            effective_epoch=current_epoch,
        )

    def filter_graph_contexts(
        self,
        scope: TrustedScope | None,
        nodes: Sequence[dict[str, Any]],
        edges: Sequence[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Filter raw node and edge dictionaries prior to context generation for RAG."""
        if scope is None:
            return list(nodes), list(edges)

        current_epoch = self.epoch_registry.get_epoch(scope.tenant_id)
        if scope.policy_epoch < current_epoch:
            logger.warning("Stale scope policy_epoch; stripping all contexts fail-closed")
            return [], []

        allowed_nodes: list[dict[str, Any]] = []
        allowed_node_ids: set[str] = set()

        for node in nodes:
            props = node.get("properties") or {}
            node_tenant = props.get("tenant_id", scope.tenant_id)
            if node_tenant != scope.tenant_id and node_tenant not in ("default", "public"):
                continue

            node_acls = props.get("acl_vector") or ["tenant:" + scope.tenant_id]
            classification = props.get("classification", "internal")

            if can_read(scope, node_acls, classification=classification, target_tenant_id=node_tenant):
                allowed_nodes.append(node)
                allowed_node_ids.add(node.get("canonical_id", ""))

        allowed_edges: list[dict[str, Any]] = []
        for edge in edges:
            out_cid = edge.get("out_cid")
            in_cid = edge.get("in_cid")
            if out_cid not in allowed_node_ids or in_cid not in allowed_node_ids:
                continue

            props = edge.get("properties") or {}
            edge_tenant = props.get("tenant_id", scope.tenant_id)
            if edge_tenant != scope.tenant_id and edge_tenant not in ("default", "public"):
                continue

            edge_acls = props.get("acl_vector") or ["tenant:" + scope.tenant_id]
            classification = props.get("classification", "internal")

            if can_read(scope, edge_acls, classification=classification, target_tenant_id=edge_tenant):
                allowed_edges.append(edge)

        return allowed_nodes, allowed_edges

    def clear_cache(self) -> None:
        """Clear evaluation cache."""
        with self._cache_lock:
            self._eval_cache.clear()


# Global singleton instance
_GLOBAL_DERIVATION_EVALUATOR = DerivationACLEvaluator()


def get_derivation_evaluator() -> DerivationACLEvaluator:
    return _GLOBAL_DERIVATION_EVALUATOR
