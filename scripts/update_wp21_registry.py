import json

with open("requirements-test-map.json", encoding="utf-8") as f:
    tmap = json.load(f)

with open("requirements-registry.json", encoding="utf-8") as f:
    reg = json.load(f)

updates = {
    "G2-EKAF-003": {
        "code_paths": ["packages/eoip/contracts/source_event.py"],
        "tests": [
            "tests/contract/test_g2_contracts.py",
            "tests/contract/test_g2_contracts.py::test_v2_event_exposes_g2_envelope_aliases",
        ],
    },
    "G2-EKAF-010": {
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "tests": [
            "tests/unit/test_graph_evolution.py",
            "tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe",
        ],
    },
    "G2-EKAF-014": {
        "code_paths": ["packages/eoip/ingestion/dlq.py"],
        "tests": [
            "tests/unit/test_phase2_ingestion.py",
            "tests/unit/test_phase2_ingestion.py::test_dead_letter_handling_contract",
        ],
    },
    "G2-EKAF-016": {
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "tests": [
            "tests/unit/test_graph_evolution.py",
            "tests/unit/test_graph_evolution.py::test_deletion_is_a_temporal_barrier_for_entity_and_relationship_replay",
        ],
    },
    "G2-EKAF-023": {
        "code_paths": ["packages/eoip/contracts/source_event.py"],
        "tests": [
            "tests/contract/test_g2_contracts.py",
            "tests/contract/test_g2_contracts.py::test_v1_source_event_upgrade_preserves_identity_and_hash",
        ],
    },
    "G2-EKAF-024": {
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "tests": [
            "tests/unit/test_graph_evolution.py",
            "tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe",
        ],
    },
    "G2-EKAF-025": {
        "code_paths": ["packages/eoip/connectors/files.py", "packages/eoip/ingestion/files.py"],
        "tests": [
            "tests/unit/test_file_ingestion.py",
            "tests/unit/test_file_ingestion.py::test_binary_connector_scope_and_limits",
        ],
    },
    "G2-EKAF-026": {
        "code_paths": ["packages/eoip/identity/resolver.py"],
        "tests": [
            "tests/unit/test_identity_resolver.py",
            "tests/unit/test_identity_resolver.py::test_same_person_by_email",
        ],
    },
}

for tid, info in updates.items():
    tmap[tid] = info["tests"]

for item in reg:
    if isinstance(item, dict) and item.get("id") in updates:
        tid = item["id"]
        info = updates[tid]
        item["status"] = "DEVELOPED"
        item["code_paths"] = info["code_paths"]
        item["test_files"] = [t.split("::")[0] for t in info["tests"]]

with open("requirements-test-map.json", "w", encoding="utf-8") as f:
    json.dump(tmap, f, indent=2, sort_keys=True)
    f.write("\n")

with open("requirements-registry.json", "w", encoding="utf-8") as f:
    json.dump(reg, f, indent=2)
    f.write("\n")

print("Successfully updated requirements-test-map.json and requirements-registry.json")
