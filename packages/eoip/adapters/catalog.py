"""BackendCatalog with SR-GDB-002 honesty validation.

The catalog is the single lookup the planner and API use to enumerate
backends, filter by tier/role/category, and instantiate *real* adapters.
Manifest-only entries can be listed and planned against but can never be
instantiated as live stores — the refusal is explicit, never silent.
"""

from __future__ import annotations

from typing import Any

from eoip.adapters.manifests import CapabilityManifest, load_manifests
from eoip.graph.backends import GraphBackendConfigurationError

#: Factories for in-repo real adapters: backend key -> callable(config) -> GraphStore.
#: JanusGraph/AGE factories live here (not in eoip.graph.backends, which is owned
#: by the graph module wiring step) and delegate to eoip.graph stores where a
#: compatible implementation already exists.


class CatalogError(GraphBackendConfigurationError):
    """Raised when a catalog entry cannot be used as requested."""


class BackendCatalog:
    """Registry over the §6 manifest set with honesty enforcement."""

    def __init__(self, manifests: dict[str, CapabilityManifest] | None = None):
        self._manifests = manifests or load_manifests()

    # -- queries ------------------------------------------------------------
    def list(
        self,
        *,
        category: str | None = None,
        tier: str | None = None,
        role: str | None = None,
        adapter_status: str | None = None,
    ) -> list[CapabilityManifest]:
        out = []
        for key in sorted(self._manifests):
            m = self._manifests[key]
            if category and m.category != category:
                continue
            if tier and m.tier != tier:
                continue
            if role and m.role != role:
                continue
            if adapter_status and m.adapter_status != adapter_status:
                continue
            out.append(m)
        return out

    def get(self, backend: str) -> CapabilityManifest:
        try:
            return self._manifests[backend]
        except KeyError:
            raise CatalogError(f"Unknown backend: {backend}") from None

    def manifest_dicts(self, **filters: Any) -> list[dict[str, Any]]:
        return [m.model_dump() for m in self.list(**filters)]

    # -- instantiation (honesty gate) ----------------------------------------
    def can_instantiate(self, backend: str) -> bool:
        return self._manifests.get(backend) is not None and self.get(backend).adapter_status == "real"

    def create_store(self, backend: str, config: dict[str, Any] | None = None):
        """Instantiate a real adapter. Manifest-only/external-gate entries are
        refused explicitly with the manifest's own notes (SR-GDB-002)."""
        manifest = self.get(backend)
        if manifest.adapter_status != "real":
            raise CatalogError(
                f"Backend {backend!r} is manifest-only"
                + (" (External gate: " + "; ".join(manifest.notes) + ")" if manifest.external_gate else "")
                + "; it cannot be instantiated as a live store."
            )
        return self._factory(backend)({**manifest.connection_config, **(config or {})})

    # -- factories -----------------------------------------------------------
    @staticmethod
    def _factory(backend: str):
        if backend in {"neo4j", "neptune", "hugegraph", "memory"}:
            # Owned by eoip.graph.backends; resolve through the existing registry.
            def _from_graph_registry(config: dict[str, Any]):
                from eoip.graph.backends import ensure_default_backends, _REGISTRY

                ensure_default_backends()
                definition = _REGISTRY[backend]
                return definition.factory(config)

            return _from_graph_registry
        if backend == "janusgraph":
            def _janus(config: dict[str, Any]):
                from eoip.adapters.janusgraph import JanusGraphStore

                return JanusGraphStore(
                    config.get("url", "http://localhost:8182"),
                    graph=config.get("graph") or config.get("database") or "g",
                    traversal_source=config.get("traversal_source", "g"),
                    username=config.get("username", ""),
                    password=config.get("password", ""),
                )

            return _janus
        if backend == "apache_age":
            def _age(config: dict[str, Any]):
                from eoip.adapters.apache_age import ApacheAGEStore

                return ApacheAGEStore(
                    host=config.get("host", "localhost"),
                    port=int(config.get("port", 5432)),
                    database=config.get("database", "postgres"),
                    graph=config.get("graph", "eoip"),
                    username=config.get("username", "postgres"),
                    password=config.get("password", ""),
                )

            return _age
        raise CatalogError(f"No real adapter factory registered for backend: {backend}")


_default: BackendCatalog | None = None


def default_catalog() -> BackendCatalog:
    global _default
    if _default is None:
        _default = BackendCatalog()
    return _default
