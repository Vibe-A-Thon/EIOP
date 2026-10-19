"""Tests for Splink Probabilistic Entity Resolution Engine (WP-KG3-04, GAP-03, STR-07, CAP-31, CRA-023.2, CRA-023.6)."""

import pytest
from eoip.er.splink_engine import (
    FeatureComparisonConfig,
    MatchDecision,
    SplinkProbabilisticEREngine,
    jaro_winkler_similarity,
)


def test_jaro_winkler_metric():
    """Validates Jaro-Winkler similarity calculations on typographical variations."""
    assert jaro_winkler_similarity("Jonathan Smith", "Jonathan Smith") == 1.0
    assert jaro_winkler_similarity("Jonathan", "Jonathon") >= 0.95
    assert jaro_winkler_similarity("Katherine", "Catherine") > 0.85
    assert jaro_winkler_similarity("Apple", "Microsoft") < 0.50
    assert jaro_winkler_similarity("", "Test") == 0.0


def test_fellegi_sunter_high_confidence_match():
    """Matching name (high Jaro-Winkler), matching email, matching org produces MATCH (> 0.85)."""
    engine = SplinkProbabilisticEREngine(prior_probability=0.05, match_threshold=0.85)

    rec1 = {
        "id": "emp_001",
        "name": "Dr. Alexander Wright",
        "email": "alex.wright@corp.example",
        "org": "Core Engineering",
    }
    rec2 = {
        "id": "jira_user_992",
        "name": "Alex Wright",
        "email": "alex.wright@corp.example",
        "org": "Core Engineering",
    }

    pair = engine.score_pair(rec1, rec2)
    assert pair.decision == MatchDecision.MATCH
    assert pair.match_probability >= 0.95
    assert pair.match_weight > 10.0  # Significant positive log-odds evidence


def test_fellegi_sunter_no_match():
    """Different names, different emails, different orgs produces NO_MATCH."""
    engine = SplinkProbabilisticEREngine(prior_probability=0.05, match_threshold=0.85)

    rec1 = {
        "id": "user_a",
        "name": "Alice Johnson",
        "email": "alice.j@corp.example",
        "org": "Marketing",
    }
    rec2 = {
        "id": "user_b",
        "name": "Bob Vance",
        "email": "bvance@refrigeration.example",
        "org": "Operations",
    }

    pair = engine.score_pair(rec1, rec2)
    assert pair.decision == MatchDecision.NO_MATCH
    assert pair.match_probability < 0.10
    assert pair.match_weight < 0.0  # Negative log-odds weight (disagreement penalty)


def test_blocking_and_connected_components_clustering():
    """Tests blocking rule execution and connected components clustering into golden records."""
    engine = SplinkProbabilisticEREngine(prior_probability=0.05, match_threshold=0.80)

    dataset = [
        # Cluster 1: Alice (3 duplicates across systems)
        {"id": "c1_ldap", "name": "Alice Smith", "email": "asmith@enterprise.com", "org": "FinTech"},
        {"id": "c1_jira", "name": "Alice M. Smith", "email": "asmith@enterprise.com", "org": "FinTech"},
        {"id": "c1_slack", "name": "Alice Smith", "email": "asmith@enterprise.com", "org": "FinTech"},
        # Cluster 2: Bob (2 duplicates)
        {"id": "c2_ldap", "name": "Bob Williams", "email": "bwilliams@enterprise.com", "org": "FinTech"},
        {"id": "c2_jira", "name": "Robert Williams", "email": "bwilliams@enterprise.com", "org": "FinTech"},
        # Disjoint Person: Charlie
        {"id": "c3_ldap", "name": "Charlie Davis", "email": "cdavis@enterprise.com", "org": "FinTech"},
    ]

    candidates = engine.block_and_score(dataset, blocking_field="org")
    # All candidates in same org were scored
    assert len(candidates) > 0

    golden_records = engine.cluster_entities(dataset, candidates)
    # Expecting 3 distinct golden records: Alice (3 source records), Bob (2 source records), Charlie (1 source record)
    assert len(golden_records) == 3

    cluster_sizes = sorted([len(g.source_entity_ids) for g in golden_records])
    assert cluster_sizes == [1, 2, 3]

    # Verify golden record has provenance and warrant
    alice_golden = next(g for g in golden_records if len(g.source_entity_ids) == 3)
    assert "c1_ldap" in alice_golden.source_entity_ids
    assert "c1_jira" in alice_golden.source_entity_ids
    assert "c1_slack" in alice_golden.source_entity_ids
    assert alice_golden.properties["email"] == "asmith@enterprise.com"
    assert alice_golden.merge_warrant_id.startswith("warrant-merge-")


def test_er_precision_recall_benchmark():
    """Benchmark test verifying 95%+ precision and recall on synthetic entity duplication testbed."""
    engine = SplinkProbabilisticEREngine(prior_probability=0.10, match_threshold=0.85)

    # 10 ground truth pairs of duplicates
    known_duplicate_pairs = [
        ({"id": f"p1_{i}", "name": f"User {i} Firstname", "email": f"u{i}@test.com", "org": "Tech"},
         {"id": f"p2_{i}", "name": f"User {i} F.", "email": f"u{i}@test.com", "org": "Tech"})
        for i in range(10)
    ]
    # 10 negative non-duplicate pairs
    known_non_duplicate_pairs = [
        ({"id": f"neg1_{i}", "name": f"Unique Person {i}", "email": f"person{i}@test.com", "org": "Tech"},
         {"id": f"neg2_{i}", "name": f"Different Person {i}", "email": f"other{i}@test.com", "org": "Tech"})
        for i in range(10)
    ]

    tp = 0
    fn = 0
    for a, b in known_duplicate_pairs:
        pair = engine.score_pair(a, b)
        if pair.decision == MatchDecision.MATCH:
            tp += 1
        else:
            fn += 1

    fp = 0
    tn = 0
    for a, b in known_non_duplicate_pairs:
        pair = engine.score_pair(a, b)
        if pair.decision == MatchDecision.MATCH:
            fp += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0

    assert precision >= 0.95
    assert recall >= 0.95
