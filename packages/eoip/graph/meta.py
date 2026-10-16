"""Meta-graph bootstrap: seeds GraphDomain and OntologyVersion vertices (FR-GRAPH-005)."""

from __future__ import annotations

from collections.abc import Iterable

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import (
    DOMAINS,
    ONTOLOGY_VERSION,
    SCHEMA_VERSION,
    VERTEX_LABELS,
    edge_endpoints_valid,
)


def ensure_domains(store: GraphStore, domains: Iterable[str] | None = None) -> dict[str, dict]:
    """Upsert GraphDomain nodes for the given domains (defaults to all DOMAINS)."""
    nodes = {}
    for name in (list(domains) if domains is not None else list(DOMAINS)):
        nodes[name] = store.upsert_vertex(
            "GraphDomain",
            {
                "canonical_id": f"urn:eoip:meta:domain:{name.lower()}",
                "name": name,
                "description": f"{name} logical graph domain",
            },
        )
    return nodes


def link_domains(store: GraphStore, vertices: Iterable[dict]) -> int:
    """Idempotently upsert BELONGS_TO_DOMAIN edges to each vertex's GraphDomain (FR-GRAPH-002).

    Ensures the needed domain nodes exist, then links every business vertex
    whose label permits a BELONGS_TO_DOMAIN edge, skipping vertices already
    linked to the same domain.
    """
    vertices = list(vertices)
    if not vertices:
        return 0
    needed = {
        VERTEX_LABELS[vertex["label"]][0]
        for vertex in vertices
        if vertex["label"] in VERTEX_LABELS
    }
    domain_vertices = ensure_domains(store, needed)
    linked = 0
    for vertex in vertices:
        label = vertex["label"]
        spec = VERTEX_LABELS.get(label)
        if spec is None or not edge_endpoints_valid("BELONGS_TO_DOMAIN", label, "GraphDomain"):
            continue
        domain_name, _required, _optional = spec
        domain_node = domain_vertices[domain_name]
        already_linked = any(
            edge["label"] == "BELONGS_TO_DOMAIN" and edge["in_cid"] == domain_node["canonical_id"]
            for edge in store.edges_from(vertex["vid"])
        )
        if not already_linked:
            store.upsert_edge(
                "BELONGS_TO_DOMAIN",
                vertex["vid"],
                domain_node["vid"],
                {"fact_key": f"domain:{vertex['canonical_id']}:{domain_name}"},
            )
            linked += 1
    return linked


class SchemaVersionConflict(RuntimeError):
    """Raised when the running code's schema is incompatible with the persisted graph."""


def _major(version: str) -> str:
    return version.split(".")[0]


def check_schema_compatibility(store: GraphStore) -> None:
    """Fail fast if the persisted graph uses an incompatible schema major version.

    A major-version bump (e.g. 1.x → 2.x) is incompatible: the store may
    contain labels, properties, or edge constraints that the running code
    no longer understands. Minor bumps (1.0 → 1.1) are additive and safe.
    """
    existing = store.get_vertex_by_canonical_id(f"urn:eoip:meta:ontology:{ONTOLOGY_VERSION}")
    if existing:
        return
    all_versions = store.find_vertices(label="OntologyVersion", limit=10)
    if not all_versions:
        return
    for vertex in all_versions:
        stored_schema = vertex.get("properties", vertex).get("schema_version", "")
        if stored_schema and _major(stored_schema) != _major(SCHEMA_VERSION):
            raise SchemaVersionConflict(
                f"Persisted graph uses schema {stored_schema} (major {_major(stored_schema)}), "
                f"but running code expects schema {SCHEMA_VERSION} (major {_major(SCHEMA_VERSION)}). "
                f"Back up the database before upgrading."
            )


def bootstrap_meta_graph(store: GraphStore) -> dict:
    check_schema_compatibility(store)

    created = {"domains": 0, "ontology_version": 0}

    for domain in DOMAINS:
        store.upsert_vertex(
            "GraphDomain",
            {
                "canonical_id": f"urn:eoip:meta:domain:{domain.lower()}",
                "name": domain,
                "description": f"{domain} logical graph domain",
            },
        )
        created["domains"] += 1

    store.upsert_vertex(
        "OntologyVersion",
        {
            "canonical_id": f"urn:eoip:meta:ontology:{ONTOLOGY_VERSION}",
            "ontology_version": ONTOLOGY_VERSION,
            "schema_version": SCHEMA_VERSION,
        },
    )
    created["ontology_version"] = 1

    store.upsert_vertex(
        "DataSource",
        {
            "canonical_id": "urn:eoip:meta:source:jira",
            "name": "Jira",
            "source_system": "jira",
            "description": "Jira project management",
        },
    )
    store.upsert_vertex(
        "DataSource",
        {
            "canonical_id": "urn:eoip:meta:source:git",
            "name": "Git",
            "source_system": "git",
            "description": "Git repository metadata and code",
        },
    )
    store.upsert_vertex(
        "DataSource",
        {
            "canonical_id": "urn:eoip:meta:source:gitlab",
            "name": "GitLab",
            "source_system": "gitlab",
            "description": "GitLab MR and pipeline metadata",
        },
    )
    created["data_sources"] = 3

    return created
