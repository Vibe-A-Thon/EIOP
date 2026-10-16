import json
import re

mapping = {
    # G2-CAUSE
    "G2-CAUSE-002": {
        "tests": ["tests/unit/test_causal_reasoning.py::test_causal_relationship_classes_and_hypotheses"],
        "test_files": ["tests/unit/test_causal_reasoning.py"],
        "code_paths": ["packages/eoip/graph/causal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_causal_reasoning.py::test_causal_relationship_classes_and_hypotheses (passed)",
    },
    "G2-CAUSE-003": {
        "tests": ["tests/unit/test_causal_reasoning.py::test_causal_hypotheses_no_silent_promotion_to_confirmed"],
        "test_files": ["tests/unit/test_causal_reasoning.py"],
        "code_paths": ["packages/eoip/graph/causal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_causal_reasoning.py::test_causal_hypotheses_no_silent_promotion_to_confirmed (passed)",
    },
    "G2-CAUSE-004": {
        "tests": ["tests/unit/test_causal_reasoning.py::test_causal_hypothesis_structure_and_alternatives"],
        "test_files": ["tests/unit/test_causal_reasoning.py"],
        "code_paths": ["packages/eoip/graph/causal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_causal_reasoning.py::test_causal_hypothesis_structure_and_alternatives (passed)",
    },
    "G2-CAUSE-005": {
        "tests": ["tests/unit/test_causal_reasoning.py::test_temporal_correlations_and_time_ordering"],
        "test_files": ["tests/unit/test_causal_reasoning.py"],
        "code_paths": ["packages/eoip/graph/causal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_causal_reasoning.py::test_temporal_correlations_and_time_ordering (passed)",
    },
    "G2-CAUSE-006": {
        "tests": ["tests/unit/test_causal_reasoning.py::test_human_confirmation_and_rejection_preserved"],
        "test_files": ["tests/unit/test_causal_reasoning.py"],
        "code_paths": ["packages/eoip/graph/causal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_causal_reasoning.py::test_human_confirmation_and_rejection_preserved (passed)",
    },

    # G2-EVOL
    "G2-EVOL-002": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_evolve_relationship_validity_interval"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_evolve_relationship_validity_interval (passed)",
    },
    "G2-EVOL-003": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_observation_time_separated_from_event_time"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_observation_time_separated_from_event_time (passed)",
    },
    "G2-EVOL-004": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_relationship_removal_expires_assertion_without_erasing_history"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_relationship_removal_expires_assertion_without_erasing_history (passed)",
    },
    "G2-EVOL-005": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_relationship_update_represented_as_new_revision"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_relationship_update_represented_as_new_revision (passed)",
    },
    "G2-EVOL-006": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_current_views_exclude_expired_facts"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_current_views_exclude_expired_facts (passed)",
    },
    "G2-EVOL-007": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_historical_as_of_reconstruction"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_historical_as_of_reconstruction (passed)",
    },
    "G2-EVOL-008": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_graph_diff_between_timestamps"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_graph_diff_between_timestamps (passed)",
    },
    "G2-EVOL-009": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_graph_mutation_source_references"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py", "packages/eoip/contracts/revision.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_graph_mutation_source_references (passed)",
    },
    "G2-EVOL-010": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_atomic_batch_isolation"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_atomic_batch_isolation (passed)",
    },
    "G2-EVOL-011": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_failed_batch_does_not_advance_checkpoint"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_failed_batch_does_not_advance_checkpoint (passed)",
    },
    "G2-EVOL-012": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_relationship_preservation_means_history_not_stale_edges"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_relationship_preservation_means_history_not_stale_edges (passed)",
    },
    "G2-EVOL-013": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_previous_revision_links"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_previous_revision_links (passed)",
    },
    "G2-EVOL-014": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_tombstone_retired_status"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_tombstone_retired_status (passed)",
    },
    "G2-EVOL-015": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_rollback_and_replay_strategy"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_rollback_and_replay_strategy (passed)",
    },
    "G2-EVOL-016": {
        "tests": ["tests/unit/test_graph_evolution_family.py::test_schema_ontology_migration_strategy"],
        "test_files": ["tests/unit/test_graph_evolution_family.py"],
        "code_paths": ["packages/eoip/graph/schema_migration.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_graph_evolution_family.py::test_schema_ontology_migration_strategy (passed)",
    },

    # G2-JOURNAL
    "G2-JOURNAL-002": {
        "tests": ["tests/unit/test_change_journal_family.py::test_journal_record_schema_and_integrity"],
        "test_files": ["tests/unit/test_change_journal_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_change_journal_family.py::test_journal_record_schema_and_integrity (passed)",
    },
    "G2-JOURNAL-003": {
        "tests": ["tests/unit/test_change_journal_family.py::test_journal_query_by_entity_time_and_run"],
        "test_files": ["tests/unit/test_change_journal_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_change_journal_family.py::test_journal_query_by_entity_time_and_run (passed)",
    },
    "G2-JOURNAL-004": {
        "tests": ["tests/unit/test_change_journal_family.py::test_journal_replay_into_derived_indices"],
        "test_files": ["tests/unit/test_change_journal_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_change_journal_family.py::test_journal_replay_into_derived_indices (passed)",
    },
    "G2-JOURNAL-005": {
        "tests": ["tests/unit/test_change_journal_family.py::test_journal_configurable_retention"],
        "test_files": ["tests/unit/test_change_journal_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_change_journal_family.py::test_journal_configurable_retention (passed)",
    },
    "G2-JOURNAL-006": {
        "tests": ["tests/unit/test_change_journal_family.py::test_journal_audit_incident_troubleshooting"],
        "test_files": ["tests/unit/test_change_journal_family.py"],
        "code_paths": ["packages/eoip/graph/evolution.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_change_journal_family.py::test_journal_audit_incident_troubleshooting (passed)",
    },

    # G2-OEVO
    "G2-OEVO-002": {
        "tests": ["tests/unit/test_ontology_evolution_family.py::test_propose_new_ontology_definitions"],
        "test_files": ["tests/unit/test_ontology_evolution_family.py"],
        "code_paths": ["packages/eoip/ontology/drift.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_ontology_evolution_family.py::test_propose_new_ontology_definitions (passed)",
    },
    "G2-OEVO-003": {
        "tests": ["tests/unit/test_ontology_evolution_family.py::test_proposal_contents_and_impact_analysis"],
        "test_files": ["tests/unit/test_ontology_evolution_family.py"],
        "code_paths": ["packages/eoip/ontology/drift.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_ontology_evolution_family.py::test_proposal_contents_and_impact_analysis (passed)",
    },
    "G2-OEVO-004": {
        "tests": ["tests/unit/test_ontology_evolution_family.py::test_ontology_changes_require_human_review_and_governance"],
        "test_files": ["tests/unit/test_ontology_evolution_family.py"],
        "code_paths": ["packages/eoip/ontology/drift.py", "packages/eoip/ontology/gitops.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_ontology_evolution_family.py::test_ontology_changes_require_human_review_and_governance (passed)",
    },
    "G2-OEVO-005": {
        "tests": ["tests/unit/test_ontology_evolution_family.py::test_approved_ontology_changes_enter_gitops_workflow"],
        "test_files": ["tests/unit/test_ontology_evolution_family.py"],
        "code_paths": ["packages/eoip/ontology/gitops.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_ontology_evolution_family.py::test_approved_ontology_changes_enter_gitops_workflow (passed)",
    },
    "G2-OEVO-006": {
        "tests": ["tests/unit/test_ontology_evolution_family.py::test_rejected_suggestions_preserved_as_feedback"],
        "test_files": ["tests/unit/test_ontology_evolution_family.py"],
        "code_paths": ["packages/eoip/ontology/drift.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_ontology_evolution_family.py::test_rejected_suggestions_preserved_as_feedback (passed)",
    },

    # G2-TIME
    "G2-TIME-002": {
        "tests": ["tests/unit/test_temporal_model_family.py::test_time_machine_state_as_of_t"],
        "test_files": ["tests/unit/test_temporal_model_family.py"],
        "code_paths": ["packages/eoip/graph/bitemporal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_temporal_model_family.py::test_time_machine_state_as_of_t (passed)",
    },
    "G2-TIME-003": {
        "tests": ["tests/unit/test_temporal_model_family.py::test_time_machine_compare_t1_vs_t2"],
        "test_files": ["tests/unit/test_temporal_model_family.py"],
        "code_paths": ["packages/eoip/graph/bitemporal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_temporal_model_family.py::test_time_machine_compare_t1_vs_t2 (passed)",
    },
    "G2-TIME-004": {
        "tests": ["tests/unit/test_temporal_model_family.py::test_time_machine_highlights_semantic_changes"],
        "test_files": ["tests/unit/test_temporal_model_family.py"],
        "code_paths": ["packages/eoip/graph/bitemporal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_temporal_model_family.py::test_time_machine_highlights_semantic_changes (passed)",
    },
    "G2-TIME-005": {
        "tests": ["tests/unit/test_temporal_model_family.py::test_release_based_snapshots"],
        "test_files": ["tests/unit/test_temporal_model_family.py"],
        "code_paths": ["packages/eoip/graph/bitemporal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_temporal_model_family.py::test_release_based_snapshots (passed)",
    },
    "G2-TIME-006": {
        "tests": ["tests/unit/test_temporal_model_family.py::test_time_travel_schema_version_context"],
        "test_files": ["tests/unit/test_temporal_model_family.py"],
        "code_paths": ["packages/eoip/graph/bitemporal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_temporal_model_family.py::test_time_travel_schema_version_context (passed)",
    },
    "G2-TIME-007": {
        "tests": ["tests/unit/test_temporal_model_family.py::test_historical_mode_evidence_reflects_valid_time"],
        "test_files": ["tests/unit/test_temporal_model_family.py"],
        "code_paths": ["packages/eoip/graph/bitemporal.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_temporal_model_family.py::test_historical_mode_evidence_reflects_valid_time (passed)",
    },

    # Governed agents (WP 3.3)
    "FR-AGENT-001": {
        "tests": ["tests/unit/test_governed_agents.py::test_agent_contract_validation"],
        "test_files": ["tests/unit/test_governed_agents.py"],
        "code_paths": ["packages/eoip/contracts/agent.py", "packages/eoip/agents/catalog.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_governed_agents.py::test_agent_contract_validation (passed)",
    },
    "FR-AGENT-002": {
        "tests": ["tests/unit/test_governed_agents.py::test_bounded_agent_runtime"],
        "test_files": ["tests/unit/test_governed_agents.py"],
        "code_paths": ["packages/eoip/agents/runtime.py", "packages/eoip/loops/core.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_governed_agents.py::test_bounded_agent_runtime (passed)",
    },
    "FR-AGENT-003": {
        "tests": ["tests/unit/test_governed_agents.py::test_trace_impact_agent"],
        "test_files": ["tests/unit/test_governed_agents.py"],
        "code_paths": ["packages/eoip/agents/trace_impact.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_governed_agents.py::test_trace_impact_agent (passed)",
    },
    "FR-AGENT-004": {
        "tests": ["tests/unit/test_governed_agents.py::test_write_action_approval_boundary"],
        "test_files": ["tests/unit/test_governed_agents.py"],
        "code_paths": ["packages/eoip/contracts/agent.py", "packages/eoip/agents/catalog.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_governed_agents.py::test_write_action_approval_boundary (passed)",
    },
    "FR-AGENT-005": {
        "tests": ["tests/unit/test_governed_agents.py::test_controlled_self_modification"],
        "test_files": ["tests/unit/test_governed_agents.py"],
        "code_paths": ["packages/eoip/contracts/agent.py", "packages/eoip/agents/catalog.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_governed_agents.py::test_controlled_self_modification (passed)",
    },
    "MVP-FR-021": {
        "tests": ["tests/unit/test_governed_agents.py::test_useful_read_only_agent_workflow"],
        "test_files": ["tests/unit/test_governed_agents.py"],
        "code_paths": ["packages/eoip/agents/trace_impact.py", "packages/eoip/agents/runtime.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_governed_agents.py::test_useful_read_only_agent_workflow (passed)",
    },
}

# 1. Update requirements-test-map.json
with open("requirements-test-map.json", "r", encoding="utf-8") as f:
    test_map = json.load(f)

for req_id, data in mapping.items():
    test_map[req_id] = data["tests"]

with open("requirements-test-map.json", "w", encoding="utf-8") as f:
    json.dump(test_map, f, indent=2, ensure_ascii=False)
print("Updated requirements-test-map.json")

# 2. Update requirements-registry.json
with open("requirements-registry.json", "r", encoding="utf-8") as f:
    registry = json.load(f)

for item in registry:
    req_id = item["id"]
    if req_id in mapping:
        data = mapping[req_id]
        item["status"] = "FULLY_DEVELOPED"
        item["code_paths"] = data["code_paths"]
        item["test_files"] = data["test_files"]
        item["evidence_receipt"] = data["evidence_receipt"]

with open("requirements-registry.json", "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)
print("Updated requirements-registry.json")

# 3. Update kgf-progress-2026-10-11.json
with open("kgf-progress-2026-10-11.json", "r", encoding="utf-8") as f:
    progress = json.load(f)

if "s" not in progress:
    progress["s"] = {}

for req_id in mapping.keys():
    progress["s"][req_id] = "done"

with open("kgf-progress-2026-10-11.json", "w", encoding="utf-8") as f:
    json.dump(progress, f, indent=2, ensure_ascii=False)
print(f"Updated kgf-progress-2026-10-11.json: total done in s = {len(progress['s'])}")

# 4. Update KGF-MASTER-BACKLOG.md
with open("KGF-MASTER-BACKLOG.md", "r", encoding="utf-8") as f:
    backlog = f.read()

for req_id in mapping.keys():
    # Replace - [ ] **`req_id`** or - [ ] `req_id` or | [ ] | `req_id`
    backlog = re.sub(rf"\|\s*\[ \]\s*\|\s*`{req_id}`", rf"| [x] | `{req_id}`", backlog)
    pattern = rf"- \[ \] (\*\*`?{req_id}`?\*\*|`{req_id}`)"
    backlog = re.sub(pattern, rf"- [x] \1", backlog)

with open("KGF-MASTER-BACKLOG.md", "w", encoding="utf-8") as f:
    f.write(backlog)
print("Updated KGF-MASTER-BACKLOG.md")
