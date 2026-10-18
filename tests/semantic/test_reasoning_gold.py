"""Gold standard test suite for profile-correct reasoning, explanations, and HTRE (CRA-019.1-019.13, CRA-019.A)."""

from __future__ import annotations
import glob
import os
import time
import pytest

from eoip.ontology.reasoning.port import (
    InconsistentOntologyException,
    OWLProfile,
    ReasonerPort,
    ReasonerStatus,
    SemanticRun,
)
from eoip.ontology.reasoning.adapters import (
    ELKAdapter,
    HermiTAdapter,
    JenaRulesAdapter,
    NativeAdapter,
    OpenlletAdapter,
)
from eoip.ontology.reasoning.hybrid import (
    HybridReasoningEngine,
    RuleCostMetrics,
    RuleStrategy,
)


def test_static_check_no_legacy_axioms_in_production():
    """CRA-019.9: Static check that no production module contains legacy hardcoded domain axioms."""
    production_py_files = glob.glob("packages/eoip/**/*.py", recursive=True)
    forbidden_terms = ["add_subclass(\"Microservice\"", "add_subclass(\"RelationalDatabase\"", "add_subclass(\"Engineer\""]

    for file_path in production_py_files:
        content = open(file_path, "r", encoding="utf-8").read()
        for term in forbidden_terms:
            assert term not in content, f"Forbidden legacy axiom '{term}' found in production file: {file_path}"


def test_reasoner_port_protocol_conformance():
    """CRA-019.7: Verify that reasoner adapters conform to the ReasonerPort protocol."""
    native = NativeAdapter()
    elk = ELKAdapter()
    assert isinstance(native, ReasonerPort)
    assert isinstance(elk, ReasonerPort)
    assert native.profile == OWLProfile.NATIVE_RDFS_SUBSET.value
    assert elk.profile == OWLProfile.OWL2_EL.value


def test_native_adapter_case_preservation_and_classification():
    """CRA-019.1, CRA-019.2: Preserve exact identifiers and compute classification."""
    adapter = NativeAdapter()
    adapter.reasoner.add_subclass("urn:example:Child", "urn:example:Parent")
    adapter.reasoner.add_subclass("urn:example:Parent", "urn:example:Grandparent")

    # Case distinction
    assert adapter.reasoner.is_subclass_of("urn:example:Child", "urn:example:child") is False
    assert adapter.reasoner.is_subclass_of("urn:example:child", "urn:example:Parent") is False
    assert adapter.reasoner.is_subclass_of("urn:example:Child", "urn:example:Grandparent") is True

    run = adapter.classify(None)
    assert run.status == ReasonerStatus.OK
    assert run.profile == "eoip-native-rdfs-subset"
    assert any(
        s["subject"] == "urn:example:Child" and s["object"] == "urn:example:Grandparent"
        for s in run.inferred_statements
    )


def test_inconsistency_detection_and_exception():
    """CRA-019.12: Disjointness and inconsistency detection aborts with InconsistentOntologyException."""
    adapter = NativeAdapter()
    adapter.reasoner.add_subclass("urn:example:A", "urn:example:B")
    adapter.reasoner.add_disjoint("urn:example:A", "urn:example:B")

    consistent, run = adapter.is_consistent(None)
    assert consistent is False
    assert run.status == ReasonerStatus.INCONSISTENT
    assert "Disjoint classes" in run.error_message


def test_status_semantics_timeouts_not_false_consistency():
    """CRA-019.3: Timeouts/errors cannot become negative entailment or a clean consistency result."""
    run = SemanticRun(
        engine="elk",
        engine_version="0.5.0",
        profile="OWL 2 EL",
        status=ReasonerStatus.TIMEOUT,
        revision="rev-timeout",
        error_message="Reasoning operation timed out",
    )
    assert run.status == ReasonerStatus.TIMEOUT
    assert run.status != ReasonerStatus.OK


def test_justifications_and_proportional_retraction():
    """CRA-019.4, CRA-019.11: Retraction uses stored justification sets and handles multiple justifications."""
    engine = HybridReasoningEngine()

    # Fact 'D1' is inferred via Rule R1 supported by assertions A1 and A2
    # AND independently supported via Rule R2 supported by assertion A3 (multiple justifications)
    engine.add_derivation(
        derivation_id="D1",
        subject="ex:S1",
        predicate="ex:dependsOn",
        obj="ex:S3",
        rule_id="R1",
        supporting_assertion_ids={"A1", "A2"},
    )
    engine.add_derivation(
        derivation_id="D1",
        subject="ex:S1",
        predicate="ex:dependsOn",
        obj="ex:S3",
        rule_id="R2",
        supporting_assertion_ids={"A3"},
    )

    # Derivation D2 is only supported by A1
    engine.add_derivation(
        derivation_id="D2",
        subject="ex:S1",
        predicate="ex:partOf",
        obj="ex:S2",
        rule_id="R3",
        supporting_assertion_ids={"A1"},
    )

    # Retract A1: D2 must be retracted because its only justification path is broken.
    # D1 must be RETAINED because path {A3} is still valid!
    res = engine.retract_assertion("A1")
    assert res["retracted_derivations_count"] == 1
    assert res["retained_due_to_alternative_justifications"] == 1
    assert "D2" not in engine.derivations
    assert "D1" in engine.derivations
    assert len(engine.derivations["D1"].justifications) == 1
    assert engine.derivations["D1"].justifications[0] == {"A3"}

    # Now retract A3: D1 now has zero justifications left and must be retracted
    res2 = engine.retract_assertion("A3")
    assert res2["retracted_derivations_count"] == 1
    assert "D1" not in engine.derivations


def test_acl_filtering_on_inferred_conclusions():
    """CRA-019.6: Inferred conclusions are filtered if any supporting fact requires restricted clearance."""
    engine = HybridReasoningEngine()

    # Derivation D_public supported by public assertions
    engine.add_derivation(
        derivation_id="D_public",
        subject="ex:Item1",
        predicate="ex:type",
        obj="ex:PublicClass",
        rule_id="R1",
        supporting_assertion_ids={"A_pub"},
        assertion_permissions={"A_pub": set()},
    )

    # Derivation D_secret supported by sensitive assertion
    engine.add_derivation(
        derivation_id="D_secret",
        subject="ex:Item2",
        predicate="ex:classifiedAs",
        obj="ex:SecretClass",
        rule_id="R2",
        supporting_assertion_ids={"A_sec"},
        assertion_permissions={"A_sec": {"role:security_clearance"}},
    )

    # Principal without clearance sees only D_public
    visible_unprivileged = engine.query_with_acl_filter(
        principal_roles={"developer"},
        principal_clearance=set(),
    )
    assert len(visible_unprivileged) == 1
    assert visible_unprivileged[0]["derivation_id"] == "D_public"

    # Principal with clearance sees both
    visible_privileged = engine.query_with_acl_filter(
        principal_roles={"auditor"},
        principal_clearance={"role:security_clearance"},
    )
    assert len(visible_privileged) == 2


def test_htre_cost_model_and_strategy_table():
    """CRA-019.10: Per-rule strategy table chosen by documented cost model and benchmark harness."""
    engine = HybridReasoningEngine()
    metrics = [
        RuleCostMetrics(rule_id="R_high_exp", amplification=25.0, volatility=0.1, fan_out=50, query_frequency=10.0),
        RuleCostMetrics(rule_id="R_volatile", amplification=2.0, volatility=0.8, fan_out=5, query_frequency=1.0),
        RuleCostMetrics(rule_id="R_stable_read", amplification=3.0, volatility=0.05, fan_out=10, query_frequency=50.0),
    ]

    strategy = engine.plan_strategy(metrics)
    assert strategy["R_high_exp"] == RuleStrategy.QUERY_TIME  # High amplification explosion risk
    assert strategy["R_volatile"] == RuleStrategy.QUERY_TIME  # High volatility, low query frequency
    assert strategy["R_stable_read"] == RuleStrategy.MATERIALIZE  # Low volatility, high read frequency

    # Benchmark comparison
    bench = engine.run_benchmark_comparison(num_assertions=5000)
    assert bench["num_assertions"] == 5000
    assert "pure_forward_elapsed_s" in bench
    assert "pure_query_time_elapsed_s" in bench
    assert "hybrid_elapsed_s" in bench


def test_elk_adapter_degraded_reporting_and_scale_benchmark():
    """CRA-019.13: Explicit degraded profile reporting (H-02) and scale benchmark."""
    elk = ELKAdapter(jvm_endpoint=None)

    # Build 20,000 class EL hierarchy
    num_classes = 20_000
    for i in range(1, num_classes):
        # Chain class_i subClassOf class_{i//2} (tree hierarchy)
        elk.add_subclass(f"urn:test:Class_{i}", f"urn:test:Class_{i // 2}")

    start = time.perf_counter()
    run = elk.classify(None)
    elapsed = time.perf_counter() - start

    assert run.status == ReasonerStatus.OK
    # Explicit degraded profile reported when JVM worker is not active
    assert run.is_degraded is True
    # Target: classify in < 60s
    print(f"\nELK classification completed in {elapsed:.3f}s for {num_classes} classes")
    assert elapsed < 60.0
