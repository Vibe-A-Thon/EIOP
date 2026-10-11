import json

with open("requirements-test-map.json", encoding="utf-8") as f:
    tmap = json.load(f)

with open("requirements-registry.json", encoding="utf-8") as f:
    reg = json.load(f)

updates = {
    "G2-EVENT-002": {
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once",
        ],
    },
    "G2-EVENT-003": {
        "code_paths": ["packages/eoip/graph/consumers.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once",
        ],
    },
    "G2-EVENT-004": {
        "code_paths": ["packages/eoip/graph/evolution.py", "packages/eoip/graph/consumers.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once",
        ],
    },
    "G2-EVENT-005": {
        "code_paths": ["packages/eoip/graph/consumers.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once",
        ],
    },
    "G2-EVENT-006": {
        "code_paths": ["packages/eoip/graph/consumers.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_consumer_failure_does_not_corrupt_graph_state",
        ],
    },
    "G2-EVENT-007": {
        "code_paths": ["packages/eoip/graph/evolution.py", "packages/eoip/graph/consumers.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once",
        ],
    },
    "G2-SYNC-002": {
        "code_paths": ["packages/eoip/connectors/acquisition.py"],
        "tests": [
            "tests/unit/test_acquisition_fabric.py",
            "tests/unit/test_acquisition_fabric.py::test_baseline_controller_persists_ordered_restart_manifest",
        ],
    },
    "G2-SYNC-003": {
        "code_paths": ["packages/eoip/connectors/reconciliation.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_reconciler_detects_and_repairs_missing_stale_and_orphaned_records",
        ],
    },
    "G2-SYNC-004": {
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "tests": [
            "tests/unit/test_graph_evolution.py",
            "tests/unit/test_graph_evolution.py::test_deletion_is_a_temporal_barrier_for_entity_and_relationship_replay",
        ],
    },
    "G2-SYNC-005": {
        "code_paths": ["packages/eoip/connectors/reconciliation.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_reconciler_detects_and_repairs_missing_stale_and_orphaned_records",
        ],
    },
    "G2-SYNC-006": {
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "tests": [
            "tests/unit/test_graph_evolution.py",
            "tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe",
        ],
    },
    "G2-SYNC-007": {
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "tests": [
            "tests/unit/test_graph_evolution.py",
            "tests/unit/test_graph_evolution.py::test_entity_evolution_is_idempotent_temporal_and_late_event_safe",
        ],
    },
    "G2-SYNC-008": {
        "code_paths": ["packages/eoip/graph/consumers.py"],
        "tests": [
            "tests/unit/test_semantic_consumers_reconciliation.py",
            "tests/unit/test_semantic_consumers_reconciliation.py::test_default_semantic_consumers_process_each_cursor_once",
        ],
    },
    "G2-SYNC-009": {
        "code_paths": [
            "packages/eoip/connectors/confluence.py",
            "packages/eoip/connectors/servicenow.py",
            "packages/eoip/ingestion/source_sync.py",
        ],
        "tests": [
            "tests/unit/test_phase2_api.py",
            "tests/unit/test_phase2_api.py::test_source_sync_admin_routes_enqueue_only_safe_sync_options",
        ],
    },
    "G2-SYNC-010": {
        "code_paths": ["packages/eoip/connectors/acquisition.py"],
        "tests": [
            "tests/unit/test_acquisition_sync_semantics.py",
            "tests/unit/test_acquisition_sync_semantics.py::test_full_rebuild_requires_explicit_maintenance_authorization",
        ],
    },
    "G2-SYNC-011": {
        "code_paths": ["packages/eoip/ingestion/replay.py"],
        "tests": [
            "tests/unit/test_file_ingestion.py",
            "tests/unit/test_file_ingestion.py::test_capture_graph_retrieval_and_idempotent_replay",
        ],
    },
    "G2-SYNC-012": {
        "code_paths": ["packages/eoip/connectors/acquisition.py"],
        "tests": [
            "tests/unit/test_acquisition_fabric.py",
            "tests/unit/test_acquisition_fabric.py::test_scheduler_admits_all_operation_types_and_enforces_controls",
        ],
    },
    "G2-SYNC-013": {
        "code_paths": ["packages/eoip/connectors/acquisition.py"],
        "tests": [
            "tests/unit/test_acquisition_sync_semantics.py",
            "tests/unit/test_acquisition_sync_semantics.py::test_bounded_historical_backfill_submits_bounded_specification",
        ],
    },
    "G2-SYNC-014": {
        "code_paths": ["packages/eoip/connectors/acquisition.py"],
        "tests": [
            "tests/unit/test_acquisition_sync_semantics.py",
            "tests/unit/test_acquisition_sync_semantics.py::test_selective_rescan_submits_filters_by_criteria",
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

print("Successfully updated requirements-test-map.json and requirements-registry.json for WP 2.2")
