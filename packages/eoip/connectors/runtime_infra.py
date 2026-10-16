"""Docker/Kubernetes runtime infrastructure connector (G2-SRC-RUNTIME-001..003).

Ingests container and Kubernetes resource metadata (pods, services,
deployments, namespaces) as SourceEventV2 envelopes. Requires the
``kubernetes`` Python client at runtime; when unavailable, ``health()``
reports UNAVAILABLE and data methods raise ``ImportError``.
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any

from eoip.connectors.base import ConnectorHealth, DiscoveredResource, DiscoveryResult, DiscoveryScope
from eoip.contracts.source_event import SourceEventV2, utc_now_iso

logger = logging.getLogger(__name__)

_K8S_AVAILABLE = False
try:
    import kubernetes  # noqa: F401

    _K8S_AVAILABLE = True
except ImportError:
    pass


class RuntimeInfraConnector:
    """Docker/Kubernetes runtime infrastructure connector (G2-SRC-RUNTIME-001..003).

    Provides ``discover``, ``extract``, ``checkpoint`` and ``health`` methods
    following the common connector pattern. Requires the ``kubernetes`` Python
    client to be installed for Kubernetes API access; when it is not,
    ``health()`` returns ``UNAVAILABLE`` and data methods raise ``ImportError``.
    """

    source_system = "runtime_infra"
    mapper_version = "k8s-docker/1.0"

    def __init__(
        self,
        *,
        source_id: str = "runtime-default",
        kubeconfig_path: str | None = None,
        namespace: str | None = None,
    ) -> None:
        self.source_id = source_id
        self.kubeconfig_path = kubeconfig_path
        self.namespace = namespace or "default"
        self._checkpoint: str | None = None

    def _require_k8s(self) -> None:
        if not _K8S_AVAILABLE:
            raise ImportError(
                "kubernetes client is required for RuntimeInfraConnector. "
                "Install it with: pip install kubernetes"
            )

    def discover(self, scope: DiscoveryScope | None = None) -> DiscoveryResult:
        """Discover available runtime resource types."""
        resources = [
            DiscoveredResource(
                resource_id="pods",
                resource_type="pod",
                name="Kubernetes Pods",
                metadata={"available": _K8S_AVAILABLE, "namespace": self.namespace},
            ),
            DiscoveredResource(
                resource_id="services",
                resource_type="service",
                name="Kubernetes Services",
                metadata={"available": _K8S_AVAILABLE, "namespace": self.namespace},
            ),
            DiscoveredResource(
                resource_id="deployments",
                resource_type="deployment",
                name="Kubernetes Deployments",
                metadata={"available": _K8S_AVAILABLE, "namespace": self.namespace},
            ),
            DiscoveredResource(
                resource_id="namespaces",
                resource_type="namespace",
                name="Kubernetes Namespaces",
                metadata={"available": _K8S_AVAILABLE},
            ),
        ]
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def _make_event(
        self,
        record_kind: str,
        record_id: str,
        payload: dict[str, Any],
        version: str | None = None,
    ) -> SourceEventV2:
        captured_at = utc_now_iso()
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        content_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        event_id = hashlib.sha256(
            f"{self.source_system}:{record_kind}:{record_id}:{content_hash}".encode()
        ).hexdigest()
        return SourceEventV2(
            event_id=event_id,
            source_system=self.source_system,
            source_instance_id=self.source_id,
            source_record_id=record_id,
            operation="UPSERT",
            source_version=version or content_hash[:16],
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=content_hash,
            payload=payload,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": record_kind,
            },
        )

    def extract(
        self,
        resources: list[dict[str, Any]] | None = None,
    ) -> list[SourceEventV2]:
        """Extract runtime infrastructure resources into SourceEventV2 envelopes.

        Parameters
        ----------
        resources:
            List of resource dicts with ``kind`` (pod, service, deployment),
            ``name``, ``namespace`` and metadata.

        Returns
        -------
        list[SourceEventV2]
            Extracted source events.
        """
        self._require_k8s()
        events: list[SourceEventV2] = []
        for resource in resources or []:
            kind = resource.get("kind", "unknown")
            name = resource.get("name", "unnamed")
            ns = resource.get("namespace", self.namespace)
            record_id = f"{self.source_id}:{kind}:{ns}/{name}"
            version = resource.get("resource_version")
            events.append(self._make_event(kind, record_id, resource, version))
        return events

    def checkpoint(self) -> str | None:
        """Return the current extraction checkpoint."""
        return self._checkpoint

    def health(self) -> ConnectorHealth:
        """Check connector health; returns UNAVAILABLE when K8s client is missing."""
        checked_at = utc_now_iso()
        if not _K8S_AVAILABLE:
            return ConnectorHealth(
                status="UNAVAILABLE",
                checked_at=checked_at,
                detail="kubernetes client is not installed",
            )
        return ConnectorHealth(
            status="HEALTHY",
            checked_at=checked_at,
            detail="Kubernetes client available",
        )
