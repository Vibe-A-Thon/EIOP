import pytest
from eoip.agents.uncertainty_protocol import (
    EvidenceLink,
    EvidenceChain,
    CoverageEstimator,
    StalenessSensor,
    UncertaintySchemaEnforcer,
    UncertaintyReason,
    ConfidenceTier,
)


@pytest.mark.req("KGR-G-019")
def test_uncertainty_protocol_high_confidence():
    enforcer = UncertaintySchemaEnforcer()
    evidence = [
        EvidenceLink(source_id="doc1", source_type="document", relevance_score=0.95, freshness_days=1.0),
        EvidenceLink(source_id="graph1", source_type="graph_vertex", relevance_score=0.90, freshness_days=2.0),
        EvidenceLink(source_id="graph2", source_type="graph_edge", relevance_score=0.88, freshness_days=3.0),
    ]

    envelope = enforcer.evaluate(evidence, query_scope_size=3)
    assert not envelope.abstain
    assert envelope.confidence_score >= 0.7
    assert envelope.confidence_tier in (ConfidenceTier.CERTAIN, ConfidenceTier.CONFIDENT)
    assert envelope.staleness_indicator == "fresh"

    wrapped = enforcer.wrap_mcp_response({"answer": 42}, envelope)
    assert "uncertainty" in wrapped
    assert wrapped["uncertainty"]["confidence_score"] == round(envelope.confidence_score, 4)
    assert not wrapped["uncertainty"]["abstain"]


@pytest.mark.req("KGR-G-019")
def test_uncertainty_protocol_abstain_on_no_evidence():
    enforcer = UncertaintySchemaEnforcer(abstain_threshold=0.2)
    envelope = enforcer.evaluate([])

    assert envelope.abstain
    assert envelope.confidence_score == 0.0
    assert envelope.confidence_tier == ConfidenceTier.ABSTAIN
    assert UncertaintyReason.OUT_OF_SCOPE in envelope.uncertainty_reasons
    assert "manual investigation" in envelope.recommendation.lower()


@pytest.mark.req("KGR-G-019")
def test_uncertainty_protocol_contradictions_and_staleness():
    enforcer = UncertaintySchemaEnforcer()
    evidence = [
        EvidenceLink(source_id="sourceA", source_type="document", relevance_score=0.8, freshness_days=100.0, is_contradictory=True),
        EvidenceLink(source_id="sourceB", source_type="document", relevance_score=0.7, freshness_days=120.0, is_contradictory=False),
    ]

    envelope = enforcer.evaluate(evidence, query_scope_size=2)
    assert envelope.staleness_indicator == "expired"
    assert UncertaintyReason.CONTRADICTORY_SOURCES in envelope.uncertainty_reasons
    assert UncertaintyReason.STALE_DATA in envelope.uncertainty_reasons
    assert envelope.confidence_score < 0.7


@pytest.mark.req("KGR-G-019")
def test_coverage_and_staleness_sensors():
    cov_est = CoverageEstimator(min_sources_for_full_coverage=4)
    assert cov_est.estimate([]) == 0.0

    links = [
        EvidenceLink(source_id="s1", source_type="doc", relevance_score=0.9, freshness_days=5.0),
        EvidenceLink(source_id="s2", source_type="doc", relevance_score=0.85, freshness_days=6.0),
    ]
    cov = cov_est.estimate(links, query_scope_size=2)
    assert cov > 40.0

    sensor = StalenessSensor()
    assert sensor.classify(3.0) == "fresh"
    assert sensor.classify(20.0) == "aging"
    assert sensor.classify(60.0) == "stale"
    assert sensor.classify(150.0) == "expired"
