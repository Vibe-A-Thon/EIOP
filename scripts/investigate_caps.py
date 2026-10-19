"""Investigate the 22 capabilities mentioned by the user
"""
from pathlib import Path
import re
import json

ROOT = Path(".").resolve()

target_caps = [
    "CAP-02", "CAP-05", "CAP-07", "CAP-10", "CAP-16", "CAP-22", "CAP-31", 
    "CAP-37", "CAP-46", "CAP-64", "CAP-17", "CAP-20", "CAP-23", "CAP-41", 
    "CAP-47", "CAP-53", "CAP-63", "CAP-21", "CAP-18", "CAP-15", "CAP-12", "CAP-09"
]

# 1. Check their entries in 06-MASTER-CAPABILITY-MATRIX.md
matrix_path = Path("EOIP-engg-doc-pkg/competitive-research-v3/06-MASTER-CAPABILITY-MATRIX.md")
cap_defs = {}
if matrix_path.exists():
    for line in matrix_path.read_text(encoding="utf-8").splitlines():
        for cid in target_caps:
            if f"| `{cid}`" in line or f"| {cid} " in line:
                parts = [p.strip() for p in line.split("|")[1:-1]]
                cap_defs[cid] = parts

print(f"Loaded {len(cap_defs)} target capability definitions from matrix:")
for cid, p in sorted(cap_defs.items()):
    print(f"  {cid}: {p[1]} | Baseline: {p[4]} | Dec: {p[6] if len(p) > 6 else ''}")

# 2. Check related code files in packages/eoip and tests/
print("\nScanning related modules and tests for each capability...")
cap_evidence = {}
# Known mappings:
mappings = {
    "CAP-02": {"modules": ["packages/eoip/graph/named_graph.py", "packages/eoip/graph/rdf_export.py"], "tests": ["tests/unit/test_named_graph.py", "tests/unit/test_named_graph_isolation.py", "tests/unit/test_phase2_rdf_export.py"]},
    "CAP-05": {"modules": ["packages/eoip/federation/router.py", "apps/api/extended.py"], "tests": ["tests/unit/test_g2_readiness.py"]},
    "CAP-07": {"modules": ["packages/eoip/graph/traversal.py", "packages/eoip/processing/engine.py"], "tests": ["tests/unit/test_parallel_multihop.py", "tests/processing/test_backends.py"]},
    "CAP-09": {"modules": ["packages/eoip/ontology/packages.py", "packages/eoip/ontology/induction.py"], "tests": ["tests/unit/test_ontology_packages.py", "tests/unit/test_ontology_induction.py"]},
    "CAP-10": {"modules": ["packages/eoip/validation/gate.py", "packages/eoip/validation/rules/"], "tests": ["tests/unit/test_validation_engine.py", "tests/unit/test_phase4_phase2_engines.py"]},
    "CAP-12": {"modules": ["packages/eoip/ontology/skos.py"], "tests": ["tests/unit/test_skos_taxonomy.py"]},
    "CAP-15": {"modules": ["packages/eoip/query/executor.py", "packages/eoip/query/languages.py"], "tests": ["tests/unit/test_query_languages.py", "tests/unit/test_query_executor.py"]},
    "CAP-16": {"modules": ["packages/eoip/moonshot/universal_transpiler.py", "packages/eoip/query/sql_bridge.py"], "tests": ["tests/unit/test_moonshots.py"]},
    "CAP-17": {"modules": ["packages/eoip/query/graphql_bridge.py", "apps/api/extended.py"], "tests": ["tests/unit/test_extended_api_routes.py"]},
    "CAP-18": {"modules": ["packages/eoip/query/optimizer.py", "packages/eoip/query/intelligence.py"], "tests": ["tests/unit/test_query_intelligence.py"]},
    "CAP-20": {"modules": ["packages/eoip/query/compiler.py", "packages/eoip/moonshot/universal_transpiler.py"], "tests": ["tests/unit/test_unified_query_api.py", "tests/unit/test_query_languages.py"]},
    "CAP-21": {"modules": ["packages/eoip/federation/obda.py", "packages/eoip/moonshot/universal_transpiler.py"], "tests": ["tests/unit/test_phase4_phase2_engines.py"]},
    "CAP-22": {"modules": ["packages/eoip/moonshot/bitemporal_state_machine.py", "packages/eoip/reasoning/incremental.py"], "tests": ["tests/unit/test_moonshots.py"]},
    "CAP-23": {"modules": ["packages/eoip/reasoning/subsumption.py", "packages/eoip/moonshot/ontology_induction.py"], "tests": ["tests/unit/test_phase4_phase2_engines.py", "tests/unit/test_trust_health_and_frontier_moonshots_wp62.py"]},
    "CAP-31": {"modules": ["packages/eoip/analytics/splink_er.py"], "tests": ["tests/unit/test_splink_er_engine.py"]},
    "CAP-37": {"modules": ["packages/eoip/graph/evolution.py", "packages/eoip/ontology/gitops.py"], "tests": ["tests/unit/test_ontology_evolution_family.py", "tests/unit/test_ontology_gitops.py"]},
    "CAP-41": {"modules": ["packages/eoip/governance/stewardship.py", "packages/eoip/governance/control_loops.py"], "tests": ["tests/unit/test_ontology_drift_review.py", "tests/unit/test_loops_library.py"]},
    "CAP-46": {"modules": ["packages/eoip/authz/derivation_acl.py"], "tests": ["tests/unit/test_authz.py"]},
    "CAP-47": {"modules": ["packages/eoip/tenancy/isolation_hardened.py", "packages/eoip/tenancy/service.py"], "tests": ["tests/unit/test_tenancy.py"]},
    "CAP-53": {"modules": ["packages/eoip/retrieval/vector.py", "packages/eoip/models/self_llm.py"], "tests": ["tests/unit/test_retrieval_vector.py", "tests/unit/test_self_llm_frontier.py"]},
    "CAP-63": {"modules": ["packages/eoip/embeddings/engine.py"], "tests": ["tests/unit/test_phase4_phase3_engines.py"]},
    "CAP-64": {"modules": ["packages/eoip/gnn/engine.py", "packages/eoip/moonshot/self_healing.py"], "tests": ["tests/unit/test_phase4_phase2_engines.py", "tests/unit/test_trust_health_and_frontier_moonshots_wp62.py"]}
}

for cid, info in mappings.items():
    mods_exist = [m for m in info["modules"] if (ROOT / m).exists()]
    tests_exist = [t for t in info["tests"] if (ROOT / t).exists()]
    print(f"\n{cid} ({cap_defs.get(cid, ['',''])[1]}):")
    print(f"  Existing Modules: {mods_exist}")
    print(f"  Existing Tests: {tests_exist}")
