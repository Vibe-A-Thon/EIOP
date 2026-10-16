import sys
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))
from _mark_done import mark_done

entries = {
    # Capsules (5)
    "G2-CAP-002": {"test_file": "tests/unit/test_capsules.py", "code_paths": ["packages/eoip/graph/capsules.py"]},
    "G2-CAP-003": {"test_file": "tests/unit/test_capsules.py", "code_paths": ["packages/eoip/graph/capsules.py"]},
    "G2-CAP-004": {"test_file": "tests/unit/test_capsules.py", "code_paths": ["packages/eoip/graph/capsules.py"]},
    "G2-CAP-005": {"test_file": "tests/unit/test_capsules.py", "code_paths": ["packages/eoip/graph/capsules.py"]},
    "G2-CAP-006": {"test_file": "tests/unit/test_capsules.py", "code_paths": ["packages/eoip/graph/capsules.py"]},

    # Knowledge Debt (5)
    "G2-KD-002": {"test_file": "tests/unit/test_knowledge_debt.py", "code_paths": ["packages/eoip/graph/knowledge_debt.py"]},
    "G2-KD-003": {"test_file": "tests/unit/test_knowledge_debt.py", "code_paths": ["packages/eoip/graph/knowledge_debt.py"]},
    "G2-KD-004": {"test_file": "tests/unit/test_knowledge_debt.py", "code_paths": ["packages/eoip/graph/knowledge_debt.py"]},
    "G2-KD-005": {"test_file": "tests/unit/test_knowledge_debt.py", "code_paths": ["packages/eoip/graph/knowledge_debt.py"]},
    "G2-KD-006": {"test_file": "tests/unit/test_knowledge_debt.py", "code_paths": ["packages/eoip/graph/knowledge_debt.py"]},

    # Intent to Retrieval / Runtime (4)
    "G2-I2R-002": {"test_file": "tests/unit/test_i2r_intelligence.py", "code_paths": ["packages/eoip/graph/business_intent.py"]},
    "G2-I2R-003": {"test_file": "tests/unit/test_i2r_intelligence.py", "code_paths": ["packages/eoip/graph/twin.py"]},
    "G2-I2R-004": {"test_file": "tests/unit/test_i2r_intelligence.py", "code_paths": ["packages/eoip/graph/business_intent.py"]},
    "G2-I2R-005": {"test_file": "tests/unit/test_i2r_intelligence.py", "code_paths": ["packages/eoip/graph/business_intent.py"]},

    # Domain Graphs (16)
    "G2-GRAPH-API-002": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/api_contracts.py"]},
    "G2-GRAPH-API-003": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/api_contracts.py"]},
    "G2-GRAPH-BIZ-002": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/business_intent.py"]},
    "G2-GRAPH-BIZ-003": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/business_intent.py"]},
    "G2-GRAPH-DEC-002": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/decisions.py"]},
    "G2-GRAPH-DEC-003": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/decisions.py"]},
    "G2-GRAPH-OBS-002": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/gaps/g2_observability.py"]},
    "G2-GRAPH-OBS-003": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/gaps/g2_observability.py"]},
    "G2-GRAPH-PROC-002": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/process_mining.py"]},
    "G2-GRAPH-PROC-003": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/process_mining.py"]},
    "G2-GRAPH-RUNTIME-002": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/runtime_topology.py"]},
    "G2-GRAPH-RUNTIME-003": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/runtime_topology.py"]},
    "G2-GRAPH-SEC-002": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/security_graph.py"]},
    "G2-GRAPH-SEC-003": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/security_graph.py"]},
    "G2-GRAPH-TEST-002": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/test_intelligence.py"]},
    "G2-GRAPH-TEST-003": {"test_file": "tests/unit/test_g2_domain_graphs.py", "code_paths": ["packages/eoip/graph/test_intelligence.py"]},
}

mark_done(entries)
print("WP 4.4 all 30 tasks marked done and synced successfully!")
