"""Meta-graph bootstrap: seeds GraphDomain and OntologyVersion vertices (FR-GRAPH-005)."""

from __future__ import annotations

from eoip.contracts.source_event import utc_now_iso
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import DOMAINS, ONTOLOGY_VERSION, SCHEMA_VERSION


def bootstrap_meta_graph(store: GraphStore) -> dict:
    now = utc_now_iso()
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
