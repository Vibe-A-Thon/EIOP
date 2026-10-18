"""Graph backend registry and config-driven store factory.

This module is the product-facing selection layer: runtime code asks for the
primary GraphStore, while deployment config decides whether that means
HugeGraph, Neptune, Neo4j, an in-memory local store, or a future registered
adapter.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from eoip.graph.store import GraphStore

SUPPORTED_EXPORTS = [
    "rdf",
    "rdf_xml",
    "rdfs",
    "owl",
    "gremlin",
    "cypher",
    "opencypher",
    "gql",
    "sparql",
    "shacl",
    "pgql",
]

APPLICATION_QUERY_LANGUAGES = [
    "EQL",
    "EOQL",
    "OSQL",
    "SemanticQL",
    "Natural Language Query",
    "Semantic Prompts",
]


@dataclass(frozen=True)
class GraphBackendCapabilities:
    backend: str
    models: list[str] = field(default_factory=list)
    query_languages: list[str] = field(default_factory=list)
    native_query_language: str = ""
    exports: list[str] = field(default_factory=lambda: list(SUPPORTED_EXPORTS))
    architecture: list[str] = field(default_factory=list)
    application_query_languages: list[str] = field(default_factory=lambda: list(APPLICATION_QUERY_LANGUAGES))
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend,
            "models": list(self.models),
            "query_languages": list(self.query_languages),
            "native_query_language": self.native_query_language,
            "exports": list(self.exports),
            "architecture": list(self.architecture),
            "application_query_languages": list(self.application_query_languages),
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class GraphBackendDefinition:
    backend: str
    factory: Callable[[dict[str, Any]], GraphStore]
    capabilities: GraphBackendCapabilities


class GraphBackendConfigurationError(ValueError):
    """Raised when graph backend config cannot be resolved safely."""


_REGISTRY: dict[str, GraphBackendDefinition] = {}


def register_backend(definition: GraphBackendDefinition) -> None:
    _REGISTRY[definition.backend] = definition


def backend_capabilities(backend: str | None = None) -> dict[str, Any]:
    ensure_default_backends()
    if backend:
        definition = _REGISTRY.get(backend)
        if definition is None:
            raise GraphBackendConfigurationError(f"Unknown graph backend: {backend}")
        return definition.capabilities.to_dict()
    return {name: item.capabilities.to_dict() for name, item in sorted(_REGISTRY.items())}


def _config_root() -> Path:
    return Path(os.getenv("EOIP_CONFIG_DIR", "config"))


def _graph_config_path() -> Path:
    return Path(os.getenv("EOIP_GRAPH_CONFIG", str(_config_root() / "graph-store.yaml")))


def _load_graph_config(path: Path | None = None) -> dict[str, Any]:
    path = path or _graph_config_path()
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise GraphBackendConfigurationError(f"Graph config must be a mapping: {path}")
    return data


def _legacy_hugegraph_config() -> dict[str, Any]:
    return {
        "type": "hugegraph",
        "url": os.getenv("EOIP_HUGEGRAPH_URL", "http://hugegraph-server:8080"),
        "graph": os.getenv("EOIP_HUGEGRAPH_GRAPH", "hugegraph"),
        "username": os.getenv("EOIP_HUGEGRAPH_USER", "admin"),
        "password": os.getenv("EOIP_HUGEGRAPH_PASSWORD", ""),
    }


def _apply_env_overrides(name: str, config: dict[str, Any]) -> dict[str, Any]:
    out = dict(config)
    backend = str(out.get("type") or name)
    generic_prefix = "EOIP_GRAPH_"
    backend_prefix = f"EOIP_{backend.upper()}_"

    def env(*keys: str) -> str | None:
        for key in keys:
            value = os.getenv(key)
            if value:
                return value
        return None

    if value := env(generic_prefix + "URL", backend_prefix + "URL"):
        out["url"] = value
    if value := env(
        generic_prefix + "DATABASE",
        generic_prefix + "GRAPH",
        backend_prefix + "DATABASE",
        backend_prefix + "GRAPH",
    ):
        out["database"] = value
        out["graph"] = value
    if value := env(generic_prefix + "USER", backend_prefix + "USER"):
        out["username"] = value
    if value := env(generic_prefix + "PASSWORD", backend_prefix + "PASSWORD"):
        out["password"] = value
    return out


def resolve_graph_backend_config(path: Path | None = None) -> tuple[str, dict[str, Any]]:
    """Resolve the selected graph connection from YAML plus env overrides.

    Selection order:
    1. ``EOIP_GRAPH_BACKEND`` as either a connection key or backend type.
    2. ``primary`` in ``config/graph-store.yaml``.
    3. legacy HugeGraph environment variables.
    """
    data = _load_graph_config(path)
    connections = data.get("connections") or {}
    if connections and not isinstance(connections, dict):
        raise GraphBackendConfigurationError("graph connections must be a mapping")

    selected = os.getenv("EOIP_GRAPH_BACKEND") or data.get("primary")
    if not connections:
        config = _legacy_hugegraph_config()
        if selected:
            config["type"] = str(selected)
        return str(config["type"]), _apply_env_overrides(str(config["type"]), config)

    if selected is None:
        selected = next(iter(connections))
    if selected in connections:
        config = dict(connections[selected] or {})
        backend = str(config.get("type") or selected)
        return backend, _apply_env_overrides(str(selected), {**config, "name": selected, "type": backend})

    for name, item in connections.items():
        item = dict(item or {})
        if item.get("type") == selected:
            return str(selected), _apply_env_overrides(name, {**item, "name": name})

    raise GraphBackendConfigurationError(f"Graph backend connection not found: {selected}")


def create_graph_store(path: Path | None = None) -> GraphStore:
    backend, config = resolve_graph_backend_config(path)
    ensure_default_backends()
    definition = _REGISTRY.get(backend)
    if definition is None:
        available = ", ".join(sorted(_REGISTRY))
        raise GraphBackendConfigurationError(
            f"Unsupported graph backend {backend!r}; available backends: {available}"
        )
    return definition.factory(config)


def _hugegraph_factory(config: dict[str, Any]) -> GraphStore:
    from eoip.graph.hugegraph import HugeGraphStore

    return HugeGraphStore(
        config.get("url", "http://hugegraph-server:8080"),
        config.get("graph") or config.get("database") or "hugegraph",
        config.get("username", "admin"),
        config.get("password", ""),
    )


def _neptune_factory(config: dict[str, Any]) -> GraphStore:
    from eoip.graph.neptune import NeptuneGraphStore

    return NeptuneGraphStore(
        config.get("url", "https://localhost:8182"),
        database=config.get("database") or config.get("graph") or "neptune",
        open_cypher_path=config.get("open_cypher_path", "/openCypher"),
        sparql_path=config.get("sparql_path", "/sparql"),
        gremlin_path=config.get("gremlin_path", "/gremlin"),
        username=config.get("username", ""),
        password=config.get("password", ""),
        verify=bool(config.get("verify_tls", True)),
    )


def _neo4j_factory(config: dict[str, Any]) -> GraphStore:
    from eoip.graph.neo4j import Neo4jGraphStore

    return Neo4jGraphStore(
        config.get("url", "http://localhost:7474"),
        database=config.get("database") or config.get("graph") or "neo4j",
        username=config.get("username", "neo4j"),
        password=config.get("password", ""),
        verify=bool(config.get("verify_tls", True)),
    )


def _memory_factory(config: dict[str, Any]) -> GraphStore:
    from eoip.graph.memory import MemoryGraphStore

    return MemoryGraphStore()


def _fuseki_factory(config: dict[str, Any]) -> GraphStore:
    from eoip.graph.rdf_backend import FusekiGraphStore

    return FusekiGraphStore(
        endpoint_url=config.get("url", "http://localhost:3030/ds"),
        dataset=config.get("dataset") or config.get("graph") or "ds",
        username=config.get("username", ""),
        password=config.get("password", ""),
        timeout=float(config.get("timeout", 30.0)),
    )


def _graphdb_factory(config: dict[str, Any]) -> GraphStore:
    from eoip.graph.rdf_backend import GraphDBGraphStore

    return GraphDBGraphStore(
        endpoint_url=config.get("url", "http://localhost:7200"),
        repository=config.get("repository") or config.get("graph") or "eoip",
        username=config.get("username", ""),
        password=config.get("password", ""),
        timeout=float(config.get("timeout", 30.0)),
    )


def ensure_default_backends() -> None:
    if _REGISTRY:
        return
    register_backend(
        GraphBackendDefinition(
            "hugegraph",
            _hugegraph_factory,
            GraphBackendCapabilities(
                backend="hugegraph",
                models=["property_graph"],
                query_languages=["Gremlin"],
                native_query_language="Gremlin",
                architecture=["distributed_graph_engine", "external_storage_backend"],
                notes=["Current default deployment backend."],
            ),
        )
    )
    register_backend(
        GraphBackendDefinition(
            "neptune",
            _neptune_factory,
            GraphBackendCapabilities(
                backend="neptune",
                models=["property_graph", "rdf"],
                query_languages=["openCypher", "Gremlin", "SPARQL"],
                native_query_language="openCypher",
                architecture=["managed", "multi-model", "decoupled_storage_compute"],
                notes=[
                    "Uses Neptune openCypher HTTPS for EOIP GraphStore operations.",
                    "SPARQL and Gremlin are exposed for native database access where policy allows.",
                ],
            ),
        )
    )
    register_backend(
        GraphBackendDefinition(
            "neo4j",
            _neo4j_factory,
            GraphBackendCapabilities(
                backend="neo4j",
                models=["property_graph"],
                query_languages=["Cypher"],
                native_query_language="Cypher",
                architecture=["self_managed_or_managed", "property_graph"],
                notes=[
                    "Uses Neo4j transactional Cypher HTTP for EOIP GraphStore operations.",
                    "Suitable for client deployments that standardize on Neo4j or Neo4j-compatible Cypher.",
                ],
            ),
        )
    )
    register_backend(
        GraphBackendDefinition(
            "memory",
            _memory_factory,
            GraphBackendCapabilities(
                backend="memory",
                models=["property_graph"],
                query_languages=["EOIP GraphStore API"],
                native_query_language="EOIP GraphStore API",
                architecture=["in_process"],
                notes=["For tests and explicit local harnesses only."],
            ),
        )
    )
    register_backend(
        GraphBackendDefinition(
            "fuseki",
            _fuseki_factory,
            GraphBackendCapabilities(
                backend="fuseki",
                models=["rdf"],
                query_languages=["SPARQL"],
                native_query_language="SPARQL",
                architecture=["rdf_triple_store", "sparql_1_1_http"],
                notes=[
                    "Apache Jena Fuseki reference RDF store adapter (CRA-002.10, ONT-003).",
                    "GPL/AGPL servers are reachable only over network protocol and never linked, vendored or bundled.",
                ],
            ),
        )
    )
    register_backend(
        GraphBackendDefinition(
            "graphdb",
            _graphdb_factory,
            GraphBackendCapabilities(
                backend="graphdb",
                models=["rdf"],
                query_languages=["SPARQL"],
                native_query_language="SPARQL",
                architecture=["certified_commercial_rdf_store", "sparql_1_1_http"],
                notes=[
                    "Ontotext GraphDB certified commercial RDF adapter (CRA-002.10, ONT-003).",
                    "Capability state UNQUALIFIED until CRA-024 receipts.",
                ],
            ),
        )
    )

