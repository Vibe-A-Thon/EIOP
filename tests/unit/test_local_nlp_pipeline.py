import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.nlp.pipeline import (
    ConceptRecommender,
    EntityExtractor,
    Gazetteer,
    KeyphraseTagger,
    LocalNLPPipeline,
    NaiveBayesClassifier,
    TfidfModel,
    split_identifier,
    tokenize,
)

TRAIN = [
    ("checkout fails with timeout error in payment gateway", "incident"),
    ("production outage after deployment rollback needed", "incident"),
    ("service down alert latency spike errors", "incident"),
    ("add new feature to export reports as csv", "feature"),
    ("implement user story for dashboard filters", "feature"),
    ("enhancement request: support dark mode in the ui", "feature"),
    ("update the runbook documentation for onboarding", "documentation"),
    ("document the api guide and architecture overview", "documentation"),
]


@pytest.fixture
def store():
    s = MemoryGraphStore()
    s.upsert_vertex("Service", {"canonical_id": "svc:pay", "service_id": "pay", "name": "Payment Gateway",
                                "description": "processes card payments and refunds"})
    s.upsert_vertex("Service", {"canonical_id": "svc:auth", "service_id": "auth", "name": "Auth Service",
                                "description": "login tokens identity"})
    s.upsert_vertex("WorkItem", {"canonical_id": "wi:1", "issue_key": "PAY-12", "summary": "Fix refund bug"})
    return s


@pytest.mark.req("GAP-NLP")
def test_tokenization_and_identifier_splitting():
    assert tokenize("The Payment-Gateway is DOWN!") == ["payment-gateway", "down"]
    assert split_identifier("PaymentGateway_v2") == ["payment", "gateway", "v2"]


@pytest.mark.req("GAP-NLP")
def test_entity_extraction_patterns_and_gazetteer(store):
    ex = EntityExtractor(Gazetteer.from_store(store))
    text = "PAY-12 broke Payment Gateway; mail ops@corp.io, see https://wiki.corp.io/x in src/pay/api.py v2.3.1"
    ents = {(e.kind, e.text) for e in ex.extract(text)}
    assert ("Service", "Payment Gateway") in ents
    assert ("EMAIL", "ops@corp.io") in ents
    assert ("URL", "https://wiki.corp.io/x") in ents
    assert ("FILE_PATH", "src/pay/api.py") in ents
    assert ("VERSION", "v2.3.1") in ents
    linked = [e for e in ex.extract(text) if e.canonical_id == "svc:pay"]
    assert linked and linked[0].confidence >= 0.9
    # issue key resolved by gazetteer takes precedence over regex, no duplicates
    assert sum(1 for e in ex.extract(text) if e.text == "PAY-12") == 1


@pytest.mark.req("GAP-NLP")
def test_keyphrase_tagging_prefers_rare_terms():
    docs = ["the payment gateway handles refunds", "the auth service issues tokens", "the report service"]
    tagger = KeyphraseTagger(TfidfModel().fit(docs))
    tags = [t for t, _ in tagger.tag("refund refund gateway timeout in the gateway retry logic", top_k=4)]
    assert "refund" in tags and "gateway" in tags or "refund refund" in tags
    assert "the" not in tags


@pytest.mark.req("GAP-NLP")
def test_classifier_trains_locally_and_abstains():
    clf = NaiveBayesClassifier().fit(TRAIN)
    assert clf.predict("payment timeout outage")[0] == "incident"
    assert clf.predict("add csv export feature for reports")[0] == "feature"
    assert clf.predict("write documentation guide")[0] == "documentation"
    probs = clf.predict_proba("outage latency")
    assert sum(probs.values()) == pytest.approx(1.0)
    assert clf.predict("zzz qqq", min_confidence=0.9)[0] is None
    with pytest.raises(ValueError):
        NaiveBayesClassifier().predict_proba("x")


@pytest.mark.req("GAP-NLP")
def test_concept_recommendation_from_graph(store):
    rec = ConceptRecommender.from_store(store)
    top = rec.recommend("customer refund failed on card payment")
    assert top and top[0].concept_id == "svc:pay" and top[0].matched_terms
    assert rec.recommend("quantum entanglement") == []
    seeded = ConceptRecommender().fit([
        {"id": "c1", "label": "BlastRadius", "alt_labels": ["impact radius"], "definition": "scope of change impact"},
    ])
    assert seeded.recommend("blast radius of a change")[0].concept_id == "c1"


@pytest.mark.req("GAP-NLP")
def test_end_to_end_pipeline_is_local_and_serialisable(store):
    pipe = LocalNLPPipeline.from_store(store, classifier=NaiveBayesClassifier().fit(TRAIN))
    out = pipe.analyze("Payment Gateway timeout outage, refund failing (PAY-12)").to_dict()
    assert out["classification"]["label"] == "incident"
    assert any(e["canonical_id"] == "svc:pay" for e in out["entities"])
    assert out["tags"] and out["concepts"][0]["concept_id"] == "svc:pay"
