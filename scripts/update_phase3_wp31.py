import json
import re

mapping = {
    "KGR-G-014": {
        "tests": [
            "tests/unit/test_streaming_agent_memory.py::test_streaming_agent_memory_sliding_window_and_temporal_decay",
            "tests/unit/test_streaming_agent_memory.py::test_streaming_agent_memory_episodes_and_retrieval",
            "tests/unit/test_streaming_agent_memory.py::test_streaming_agent_memory_importance_cutoff",
            "tests/unit/test_streaming_agent_memory.py::test_streaming_agent_memory_clear",
        ],
        "test_files": ["tests/unit/test_streaming_agent_memory.py"],
        "code_paths": [
            "packages/eoip/agents/memory.py",
            "packages/eoip/moonshot/streaming_agent_memory.py",
        ],
        "evidence_receipt": "python -m pytest tests/unit/test_streaming_agent_memory.py (4 passed)",
    },
    "KGR-G-015": {
        "tests": [
            "tests/unit/test_ontology_induction.py::test_ontology_induction_flow",
            "tests/unit/test_ontology_induction.py::test_ontology_induction_drift_detection",
            "tests/unit/test_ontology_induction.py::test_ontology_induction_shacl_validation",
        ],
        "test_files": ["tests/unit/test_ontology_induction.py"],
        "code_paths": ["packages/eoip/moonshot/ontology_induction.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_ontology_induction.py (3 passed)",
    },
    "KGR-G-016": {
        "tests": [
            "tests/unit/test_vector_graph.py::test_hnsw_index_insert_and_search",
            "tests/unit/test_vector_graph.py::test_hnsw_index_remove",
            "tests/unit/test_vector_graph.py::test_unified_vector_then_traverse_colocated",
            "tests/unit/test_vector_graph.py::test_traverse_then_vector_filter",
        ],
        "test_files": ["tests/unit/test_vector_graph.py"],
        "code_paths": ["packages/eoip/graph/vector_graph.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_vector_graph.py (4 passed)",
    },
    "KGR-G-017": {
        "tests": [
            "tests/unit/test_mcp_pr_tools.py::test_mcp_pr_tools_registration",
            "tests/unit/test_mcp_pr_tools.py::test_mcp_pr_tools_list_and_impact",
            "tests/unit/test_mcp_pr_tools.py::test_mcp_pr_tools_triage",
            "tests/unit/test_mcp_pr_tools.py::test_pr_impact_calculator_with_graph_store",
        ],
        "test_files": ["tests/unit/test_mcp_pr_tools.py"],
        "code_paths": [
            "packages/eoip/agents/mcp_pr_tools.py",
            "packages/eoip/agents/tools.py",
        ],
        "evidence_receipt": "python -m pytest tests/unit/test_mcp_pr_tools.py (4 passed)",
    },
    "KGR-G-018": {
        "tests": [
            "tests/unit/test_parallel_multihop.py::test_sparse_graph_builder_and_csr",
            "tests/unit/test_parallel_multihop.py::test_parallel_multihop_bfs_deep_traversal",
            "tests/unit/test_parallel_multihop.py::test_influence_propagation",
            "tests/unit/test_parallel_multihop.py::test_subgraph_partitioning_and_fraud_ring_detector",
            "tests/unit/test_parallel_multihop.py::test_from_graph_store",
        ],
        "test_files": ["tests/unit/test_parallel_multihop.py"],
        "code_paths": ["packages/eoip/analytics/parallel_multihop.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_parallel_multihop.py (5 passed)",
    },
    "KGR-G-019": {
        "tests": [
            "tests/unit/test_uncertainty_protocol.py::test_uncertainty_protocol_high_confidence",
            "tests/unit/test_uncertainty_protocol.py::test_uncertainty_protocol_abstain_on_no_evidence",
            "tests/unit/test_uncertainty_protocol.py::test_uncertainty_protocol_contradictions_and_staleness",
            "tests/unit/test_uncertainty_protocol.py::test_coverage_and_staleness_sensors",
        ],
        "test_files": ["tests/unit/test_uncertainty_protocol.py"],
        "code_paths": ["packages/eoip/agents/uncertainty_protocol.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_uncertainty_protocol.py (4 passed)",
    },
    "KGR-G-020": {
        "tests": [
            "tests/unit/test_mutation_stream.py::test_mutation_event_sse_and_serialization",
            "tests/unit/test_mutation_stream.py::test_subscription_filter",
            "tests/unit/test_mutation_stream.py::test_mutation_event_bus_sse_delivery_and_replay",
            "tests/unit/test_mutation_stream.py::test_webhook_registration",
        ],
        "test_files": ["tests/unit/test_mutation_stream.py"],
        "code_paths": ["packages/eoip/streaming/mutation_stream.py"],
        "evidence_receipt": "python -m pytest tests/unit/test_mutation_stream.py (4 passed)",
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

# 2. Update requirements-registry.json (it's a list)
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
    pattern = rf"- \[ \] (\*\*`?{req_id}`?\*\*|`{req_id}`)"
    backlog = re.sub(pattern, r"- [x] \1", backlog)

with open("KGF-MASTER-BACKLOG.md", "w", encoding="utf-8") as f:
    f.write(backlog)
print("Updated KGF-MASTER-BACKLOG.md")
