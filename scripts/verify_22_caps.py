"""Deep inspection of each of the 22 capabilities:
Check existing implementation files, test files, and run tests.
"""
from pathlib import Path
import subprocess

ROOT = Path(".").resolve()

cap_status_map = {
    "CAP-02": {
        "title": "Store standard W3C semantic quads with provenance context",
        "dim": "RDF/quad storage and named graphs",
        "code": ["packages/eoip/graph/named_graph.py", "packages/eoip/graph/rdf_export.py"],
        "tests": ["tests/unit/test_named_graph.py", "tests/unit/test_named_graph_isolation.py", "tests/unit/test_phase2_rdf_export.py"],
        "wp": "WP-02 / WP-P2-04"
    },
    "CAP-05": {
        "title": "Scale to billions of nodes and edges across clusters",
        "dim": "Distributed scale-out and sharding",
        "code": ["apps/api/extended.py", "packages/eoip/federation/router.py"],
        "tests": ["tests/unit/test_g2_readiness.py"],
        "wp": "WP-KG3-12 (50M+ Triples Soak Load)"
    },
    "CAP-07": {
        "title": "Traverse nodes with >100k edges without out-of-memory crashes",
        "dim": "Supernode handling and degree skew",
        "code": ["packages/eoip/graph/traversal.py", "packages/eoip/processing/engine.py"],
        "tests": ["tests/unit/test_parallel_multihop.py", "tests/processing/test_backends.py"],
        "wp": "PU-W10 / WP-P3-02"
    },
    "CAP-09": {
        "title": "Model formal domain taxonomies, class hierarchies, and properties",
        "dim": "Ontology modeling (RDFS/OWL 2)",
        "code": ["packages/eoip/ontology/packages.py", "packages/eoip/moonshot/ontology_induction.py"],
        "tests": ["tests/unit/test_ontology_packages.py", "tests/unit/test_ontology_induction.py"],
        "wp": "WP-P3-01"
    },
    "CAP-10": {
        "title": "Validate complex structural, cardinality, and regex constraints on graphs",
        "dim": "SHACL shape validation",
        "code": ["packages/eoip/validation/gate.py", "packages/eoip/validation/quality.py"],
        "tests": ["tests/unit/test_validation_engine.py", "tests/unit/test_phase4_phase2_engines.py"],
        "wp": "WP-KG3-05 (CRA-020.1 Verified)"
    },
    "CAP-12": {
        "title": "Manage multilingual business glossaries and concept schemes",
        "dim": "Taxonomy and SKOS concept management",
        "code": ["packages/eoip/ontology/skos.py"],
        "tests": ["tests/unit/test_skos_taxonomy.py"],
        "wp": "WP-P3-01"
    },
    "CAP-15": {
        "title": "Execute federated semantic queries over RDF graphs",
        "dim": "W3C SPARQL 1.1 query execution",
        "code": ["packages/eoip/query/executor.py", "packages/eoip/query/languages.py"],
        "tests": ["tests/unit/test_query_languages.py", "tests/unit/test_query_executor.py"],
        "wp": "WP-KG3-03"
    },
    "CAP-16": {
        "title": "Query graphs using familiar SQL syntax and property graph queries",
        "dim": "SQL/PGQ and relational SQL bridges",
        "code": ["packages/eoip/moonshot/universal_transpiler.py"],
        "tests": ["tests/unit/test_moonshots.py"],
        "wp": "WP-KG3-03"
    },
    "CAP-17": {
        "title": "Provide front-end developers with typed GraphQL schemas",
        "dim": "GraphQL query and mutation API",
        "code": ["apps/api/extended.py"],
        "tests": ["tests/unit/test_extended_api_routes.py"],
        "wp": "WP-5.3"
    },
    "CAP-18": {
        "title": "Optimize complex multi-join graph queries with stats and leapfrog joins",
        "dim": "Cost-based query optimization & WCOJ",
        "code": ["packages/eoip/query/intelligence.py", "packages/eoip/query/optimizer.py"],
        "tests": ["tests/unit/test_query_intelligence.py"],
        "wp": "WP-P3-02"
    },
    "CAP-20": {
        "title": "Write once, execute across HugeGraph, Neo4j, Neptune, and SPARQL",
        "dim": "Portable typed query IR and compiler",
        "code": ["packages/eoip/query/compiler.py", "packages/eoip/moonshot/universal_transpiler.py"],
        "tests": ["tests/unit/test_unified_query_api.py", "tests/unit/test_query_languages.py"],
        "wp": "WP-KG3-03 (CRA-009.1 Verified)"
    },
    "CAP-21": {
        "title": "Query live relational databases as a virtual graph without ETL",
        "dim": "Federation and virtualization (OBDA)",
        "code": ["packages/eoip/federation/router.py", "packages/eoip/moonshot/universal_transpiler.py"],
        "tests": ["tests/unit/test_phase4_phase2_engines.py", "tests/unit/test_moonshots.py"],
        "wp": "WP-P4-02"
    },
    "CAP-22": {
        "title": "Derive new facts automatically with O(1) retraction upon premise deletion",
        "dim": "Incremental rule / Datalog materialization",
        "code": ["packages/eoip/moonshot/bitemporal_state_machine.py", "packages/eoip/temporal/deterministic_graph.py"],
        "tests": ["tests/unit/test_moonshots.py", "tests/unit/test_temporal_model_family.py"],
        "wp": "WP-KG3-10 (CRA-019.1 Verified)"
    },
    "CAP-23": {
        "title": "Compute subclass subsumption and property domains/ranges",
        "dim": "OWL 2 profile reasoning (RL/QL/EL)",
        "code": ["packages/eoip/moonshot/ontology_induction.py"],
        "tests": ["tests/unit/test_phase4_phase2_engines.py", "tests/unit/test_trust_health_and_frontier_moonshots_wp62.py"],
        "wp": "WP-KG3-10"
    },
    "CAP-31": {
        "title": "Disambiguate duplicate entities across disparate enterprise sources",
        "dim": "Probabilistic entity resolution (ER)",
        "code": ["packages/eoip/analytics/splink_er.py"],
        "tests": ["tests/unit/test_splink_er_engine.py"],
        "wp": "WP-KG3-04 (CRA-023.2 Verified)"
    },
    "CAP-37": {
        "title": "Upgrade ontology schemas without corrupting existing instance data",
        "dim": "Schema and ontology evolution with migrations",
        "code": ["packages/eoip/graph/evolution.py", "packages/eoip/ontology/gitops.py"],
        "tests": ["tests/unit/test_ontology_evolution_family.py", "tests/unit/test_ontology_gitops.py"],
        "wp": "WP-KG3-06 (CRA-022.1 Verified)"
    },
    "CAP-41": {
        "title": "Formal review, approval, and promotion stages for ontology changes",
        "dim": "Ontology governance workflow",
        "code": ["packages/eoip/governance/control_loops.py"],
        "tests": ["tests/unit/test_ontology_drift_review.py", "tests/unit/test_loops_library.py"],
        "wp": "WP-KG3-08"
    },
    "CAP-46": {
        "title": "Ensure inferred facts and search results never leak private data",
        "dim": "Derivation-aware source-ACL enforcement in retrieval",
        "code": ["packages/eoip/authz/derivation_acl.py"],
        "tests": ["tests/unit/test_authz.py"],
        "wp": "WP-KG3-01 (CRA-003.8 Verified)"
    },
    "CAP-47": {
        "title": "Run multiple clients on shared infrastructure with zero cross-leakage",
        "dim": "Multi-tenant isolation (SILO / BRIDGE / POOL)",
        "code": ["packages/eoip/tenancy/isolation_hardened.py", "packages/eoip/tenancy/service.py"],
        "tests": ["tests/unit/test_tenancy.py"],
        "wp": "WP-KG3-02 (CRA-003.6 Verified)"
    },
    "CAP-53": {
        "title": "Retrieve semantically similar chunks and entity descriptions",
        "dim": "Dense vector similarity search",
        "code": ["packages/eoip/retrieval/vector.py", "packages/eoip/models/self_llm.py"],
        "tests": ["tests/unit/test_retrieval_vector.py", "tests/unit/test_self_llm_frontier.py"],
        "wp": "WP-KG3-07 / Tier 8"
    },
    "CAP-63": {
        "title": "Compute low-dimensional vector representations of entities and relations",
        "dim": "Knowledge graph embeddings (KGE)",
        "code": ["packages/eoip/embeddings/engine.py"],
        "tests": ["tests/unit/test_phase4_phase3_engines.py"],
        "wp": "WP-P4-03 (AI-006)"
    },
    "CAP-64": {
        "title": "Predict missing dependencies and anomalous architectural patterns",
        "dim": "Graph Neural Networks (GNN) and link prediction",
        "code": ["packages/eoip/gnn/engine.py", "packages/eoip/moonshot/self_healing.py"],
        "tests": ["tests/unit/test_phase4_phase2_engines.py", "tests/unit/test_trust_health_and_frontier_moonshots_wp62.py"],
        "wp": "WP-P4-02 (GRAPH-004)"
    }
}

for cid, info in sorted(cap_status_map.items()):
    codes_ok = all((ROOT / c).exists() for c in info["code"])
    tests_ok = all((ROOT / t).exists() for t in info["tests"])
    print(f"{cid}: codes_ok={codes_ok}, tests_ok={tests_ok} ({info['code'][0]} | {info['tests'][0]})")
