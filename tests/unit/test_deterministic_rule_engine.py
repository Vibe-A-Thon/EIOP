import pytest

from eoip.future_scope import (
    FACT_STATUSES,
    DeterministicRuleEngine,
    Fact,
    RuleDefinition,
)


@pytest.fixture
def rules():
    return [
        RuleDefinition(
            rule_id="rule-owns-expert",
            version="1.0.0",
            when={"predicate": "OWNS"},
            infer={"predicate": "IS_EXPERT_IN", "object": "owned-component"},
            source_policy="all",
        ),
        RuleDefinition(
            rule_id="rule-expert-reviewer",
            version="1.0.0",
            when={"predicate": "IS_EXPERT_IN"},
            infer={"predicate": "CAN_REVIEW", "object": "review-eligible"},
            source_policy="INFERRED",
        ),
        RuleDefinition(
            rule_id="rule-strict-policy",
            version="2.0.0",
            when={"predicate": "OWNS"},
            infer={"predicate": "IS_CERTIFIED_LEAD", "object": "lead-component"},
            source_policy="HUMAN_CONFIRMED",
        ),
    ]


@pytest.mark.req("GAP-RULE")
def test_versioned_inference_policies(rules):
    engine = DeterministicRuleEngine(rules)

    fact_asserted = Fact(
        subject="urn:person:ada",
        predicate="OWNS",
        object="urn:service:billing",
        source_id="src:git:1",
        status="ASSERTED",
    )

    # v1.0.0 infers expert (hop 1) and then reviewer (hop 2 via forward chaining)
    inferred_v1 = engine.infer([fact_asserted], version="1.0.0")
    predicates_v1 = {f.predicate for f in inferred_v1}
    assert "IS_EXPERT_IN" in predicates_v1
    assert "CAN_REVIEW" in predicates_v1
    assert all(f.status == "INFERRED" for f in inferred_v1)
    assert all("1.0.0" in f.rule_id for f in inferred_v1)

    # v2.0.0 requires HUMAN_CONFIRMED, so ASSERTED fact produces no inferences
    inferred_v2 = engine.infer([fact_asserted], version="2.0.0")
    assert len(inferred_v2) == 0


@pytest.mark.req("GAP-RULE")
def test_distinguishes_fact_statuses(rules):
    engine = DeterministicRuleEngine(rules)
    assert {"ASSERTED", "INFERRED", "MODEL_GENERATED", "HUMAN_CONFIRMED"} == FACT_STATUSES

    fact_model = Fact(
        subject="urn:person:grace",
        predicate="OWNS",
        object="urn:service:auth",
        source_id="src:ai:llm-extract",
        status="MODEL_GENERATED",
    )
    fact_human = Fact(
        subject="urn:person:grace",
        predicate="OWNS",
        object="urn:service:auth",
        source_id="src:human:review-1",
        status="HUMAN_CONFIRMED",
    )

    # v2.0.0 strict policy only triggers on HUMAN_CONFIRMED
    res_model = engine.infer([fact_model], version="2.0.0")
    assert len(res_model) == 0

    res_human = engine.infer([fact_human], version="2.0.0")
    assert len(res_human) == 1
    assert res_human[0].predicate == "IS_CERTIFIED_LEAD"


@pytest.mark.req("GAP-RULE")
def test_retraction_and_recomputation(rules):
    engine = DeterministicRuleEngine(rules)

    f1 = Fact(
        subject="urn:person:ada",
        predicate="OWNS",
        object="urn:service:billing",
        source_id="src:git:1",
        status="ASSERTED",
    )
    f2 = Fact(
        subject="urn:person:linus",
        predicate="OWNS",
        object="urn:service:kernel",
        source_id="src:git:2",
        status="ASSERTED",
    )

    # Both facts infer
    initial_inferred = engine.infer([f1, f2], version="1.0.0")
    subjects = {f.subject for f in initial_inferred}
    assert "urn:person:ada" in subjects
    assert "urn:person:linus" in subjects

    # Retract source for ada
    recomputed = engine.recompute_after_retraction(
        [f1, f2],
        retracted_source_ids={"src:git:1"},
        version="1.0.0",
    )

    remaining_subjects = {f["subject"] for f in recomputed["inferred"]}
    assert "urn:person:ada" not in remaining_subjects
    assert "urn:person:linus" in remaining_subjects
    assert "src:git:1" in recomputed["retracted_source_ids"]
    assert len(recomputed["asserted"]) == 1
    assert recomputed["asserted"][0]["source_id"] == "src:git:2"
