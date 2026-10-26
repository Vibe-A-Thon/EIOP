"""Enterprise knowledge-graph building algorithms (gap analysis §6, part B).

Deterministic-first builders for constructing and enriching EOIP knowledge
graphs from profiled datasets, commit histories, dictionaries/gazetteers, and
existing graph structure. No mandatory LLM: every builder is pure Python over
plain data structures; enrichment only applies validated additions.

Submodules:

* ``schema``        — class/property induction from eoip.ingest.profile reports
* ``modes``         — ontology-first / data-first / hybrid construction plans
* ``cochange``      — co-change coupling edges from commit histories
* ``dependencies``  — inclusion-dependency / value-overlap discovery (MinHash bands)
* ``linking``       — mention / entity extraction (dictionary + gazetteer)
* ``hierarchy``     — parent-pointer / path-string / lexical clustering
* ``rollup``        — hierarchical community rollup above Leiden results
* ``similarity``    — kNN similarity graph from an embedding index
* ``linkprediction``— common-neighbors / Adamic-Adar / preferential-attachment proposals
* ``repair``        — dangling-edge detection + orphan clustering
* ``enrichment``    — incremental validated-only enrichment loop
* ``router``        — build_router() for /api/v1/graphbuild/* and /api/v1/adapters/*
"""

from eoip.graphbuild.router import build_adapters_router, build_graphbuild_router

__all__ = ["build_adapters_router", "build_graphbuild_router"]
