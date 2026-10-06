"""Optional Kubernetes discovery connector (G2-SRC-K8S).

Implements the common :class:`SourceConnector` protocol
(``eoip.connectors.base``) against the Kubernetes API, using in-cluster
service-account auth when running inside a cluster and kubeconfig otherwise.
Namespaces, pods, deployments and services are discovered as
:class:`DiscoveredResource` entries and emitted as canonical SourceEventV2
records on baseline/poll.

Requires the optional ``kubernetes`` package (``pip install eoip[k8s]``); every
API touch is import-guarded so importing this module — and the rest of the
connector registry — works without it.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Iterable, Iterator
from typing import Any

from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
)
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities

RESOURCE_TYPES = ("namespace", "pod", "deployment", "service")


class KubernetesDependencyMissingError(RuntimeError):
    """Raised when a connector method needs the optional ``kubernetes`` package."""


def _load_kubernetes() -> Any:
    try:
        import kubernetes
    except ImportError as exc:
        raise KubernetesDependencyMissingError(
            "Kubernetes connector requires the optional dependency "
            "'kubernetes' (pip install eoip[k8s]) (G2-SRC-K8S)"
        ) from exc
    return kubernetes


class KubernetesConnector:
    """SourceConnector adapter over the Kubernetes API (G2-SRC-K8S)."""

    source_system = "kubernetes"
    mapper_version = "kubernetes/1.0"

    def __init__(
        self,
        source_id: str = "kubernetes",
        *,
        namespaces: list[str] | None = None,
        kubeconfig_path: str | None = None,
        context: str | None = None,
        in_cluster: bool | None = None,
        client: Any | None = None,
    ) -> None:
        self.source_id = source_id
        self.namespaces = list(namespaces) if namespaces else None
        self.kubeconfig_path = kubeconfig_path
        self.context = context
        self._in_cluster = in_cluster
        self._client = client  # pre-built k8s client (tests); else built lazily

    # -- client bootstrap ----------------------------------------------------

    def _core(self) -> Any:
        if self._client is not None:
            return self._client
        kubernetes = _load_kubernetes()
        if self._in_cluster is None:
            try:
                kubernetes.config.load_incluster_config()
                self._in_cluster = True
            except (kubernetes.config.ConfigException, OSError):
                self._in_cluster = False
        if not self._in_cluster:
            kubernetes.config.load_kube_config(
                config_file=self.kubeconfig_path, context=self.context
            )
        self._client = kubernetes.client.CoreV1Api()
        return self._client

    def _apps(self) -> Any:
        if self._client is not None:
            return self._client
        kubernetes = _load_kubernetes()
        return kubernetes.client.AppsV1Api()

    # -- protocol: capabilities / discovery ----------------------------------

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(baseline=True, polling=True, discovery=True)

    def _target_namespaces(self, core: Any) -> list[str]:
        if self.namespaces:
            return list(self.namespaces)
        return [ns.metadata.name for ns in core.list_namespace().items]

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        core = self._core()
        warnings: list[str] = []
        resources: list[DiscoveredResource] = []
        try:
            namespaces = self._target_namespaces(core)
        except Exception as exc:  # noqa: BLE001 - surfaced as warning, not crash
            return DiscoveryResult(
                source_id=self.source_id,
                resources=[],
                warnings=[f"failed to list namespaces: {exc}"],
            )
        for namespace in namespaces:
            if scope.include and namespace not in scope.include:
                continue
            if namespace in scope.exclude:
                continue
            pods = core.list_namespaced_pod(namespace).items
            services = core.list_namespaced_service(namespace).items
            resources.append(
                DiscoveredResource(
                    resource_id=f"namespace/{namespace}",
                    resource_type="namespace",
                    name=namespace,
                    estimated_records=len(pods),
                    metadata={"pod_count": len(pods)},
                )
            )
            for pod in pods:
                resources.append(
                    DiscoveredResource(
                        resource_id=f"pod/{namespace}/{pod.metadata.name}",
                        resource_type="pod",
                        name=pod.metadata.name,
                        metadata={
                            "namespace": namespace,
                            "phase": getattr(pod.status, "phase", None),
                        },
                    )
                )
            for service in services:
                resources.append(
                    DiscoveredResource(
                        resource_id=f"service/{namespace}/{service.metadata.name}",
                        resource_type="service",
                        name=service.metadata.name,
                        metadata={"namespace": namespace},
                    )
                )
        try:
            for namespace in namespaces:
                if scope.include and namespace not in scope.include:
                    continue
                if namespace in scope.exclude:
                    continue
                for deployment in self._apps().list_namespaced_deployment(namespace).items:
                    resources.append(
                        DiscoveredResource(
                            resource_id=f"deployment/{namespace}/{deployment.metadata.name}",
                            resource_type="deployment",
                            name=deployment.metadata.name,
                            metadata={
                                "namespace": namespace,
                                "replicas": getattr(deployment.spec, "replicas", None),
                            },
                        )
                    )
        except Exception as exc:  # noqa: BLE001 - apps API may be unavailable
            warnings.append(f"failed to list deployments: {exc}")
        return DiscoveryResult(source_id=self.source_id, resources=resources, warnings=warnings)

    # -- protocol: event streams ----------------------------------------------

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        del checkpoint
        yield from self._events()

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        del checkpoint  # full re-list; the platform dedupes by content hash
        yield from self._events()

    def _events(self) -> Iterator[SourceEventV2]:
        result = self.discover(DiscoveryScope())
        for warning in result.warnings:
            raise KubernetesDependencyMissingError(warning)
        for resource in result.resources:
            yield self._event(resource)

    def _event(self, resource: DiscoveredResource) -> SourceEventV2:
        payload_json = json.dumps(resource.metadata, sort_keys=True, separators=(",", ":"))
        content_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        captured_at = utc_now_iso()
        return SourceEventV2(
            event_id=hashlib.sha256(
                f"{self.source_system}:{resource.resource_id}:{content_hash}".encode()
            ).hexdigest(),
            source_system=self.source_system,
            source_instance_id=self.source_id,
            source_record_id=resource.resource_id,
            source_record_type=resource.resource_type,
            operation="UPSERT",
            source_version=content_hash,
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=content_hash,
            payload={
                "resource_id": resource.resource_id,
                "resource_type": resource.resource_type,
                "name": resource.name,
                "metadata": resource.metadata,
            },
            metadata={"mapper_version": self.mapper_version},
        )

    def handle_event(self, event: dict[str, Any]) -> Iterator[SourceEventV2]:
        ref = event.get("ref") or event.get("resource_id")
        return iter((self.fetch_record(str(ref)),)) if ref else iter(())

    def fetch_record(self, ref: str) -> SourceEventV2:
        """Fetch one object by ``<type>/<namespace>/<name>`` (or ``namespace/<name>``)."""
        parts = ref.split("/")
        core = self._core()
        if len(parts) == 2 and parts[0] == "namespace":
            obj = core.read_namespace(parts[1])
        elif len(parts) == 3:
            kind, namespace, name = parts
            if kind == "pod":
                obj = core.read_namespaced_pod(name, namespace)
            elif kind == "service":
                obj = core.read_namespaced_service(name, namespace)
            elif kind == "deployment":
                obj = self._apps().read_namespaced_deployment(name, namespace)
            else:
                raise LookupError(f"unsupported resource type: {kind}")
        else:
            raise LookupError(f"unrecognized reference: {ref}")
        metadata = {
            "namespace": getattr(obj.metadata, "namespace", None),
            "uid": getattr(obj.metadata, "uid", None),
        }
        return self._event(
            DiscoveredResource(
                resource_id=ref,
                resource_type=parts[0],
                name=parts[-1],
                metadata={k: v for k, v in metadata.items() if v is not None},
            )
        )

    def health(self) -> ConnectorHealth:
        started = time.perf_counter()
        try:
            self._core().list_namespace()
        except KubernetesDependencyMissingError as exc:
            return ConnectorHealth(
                status="MISCONFIGURED", checked_at=utc_now_iso(), detail=str(exc)
            )
        except Exception as exc:  # noqa: BLE001 - any API failure is UNAVAILABLE
            return ConnectorHealth(
                status="UNAVAILABLE",
                checked_at=utc_now_iso(),
                detail=str(exc),
                latency_ms=(time.perf_counter() - started) * 1000,
            )
        return ConnectorHealth(
            status="HEALTHY",
            checked_at=utc_now_iso(),
            latency_ms=(time.perf_counter() - started) * 1000,
        )

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]:
        return iter(events)
