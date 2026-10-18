"""Contract tests for asserted-only queries, storage separation, and TriG exports (CRA-045.5)."""

from eoip.contracts.canonical import (
    CanonicalAssertion,
    KnowledgeState,
    ProducerClass,
    RDFTerm,
    TermKind,
)
from eoip.ai.boundary import export_trig_quads, filter_asserted_only


def _make_assertion(aid: str, subj: str, pred: str, obj: str, state: KnowledgeState, tenant_id: str = "tenant_alpha") -> CanonicalAssertion:
    return CanonicalAssertion(
        assertion_id=aid,
        graph_iri=f"urn:eoip:tenant:{tenant_id}" if state != KnowledgeState.PROPOSED else f"urn:eoip:proposed:{tenant_id}",
        tenant_id=tenant_id,
        subject=RDFTerm(kind=TermKind.IRI, value=subj),
        predicate=RDFTerm(kind=TermKind.IRI, value=pred),
        object=RDFTerm(kind=TermKind.IRI, value=obj),
        knowledge_state=state,
    )


def test_asserted_only_query_filter_default():
    """CRA-045.5: By default queries and endpoints return only asserted facts, excluding proposals."""
    assertions = [
        _make_assertion("a1", "urn:ent:1", "urn:rel:owner", "urn:user:1", KnowledgeState.ASSERTED),
        _make_assertion("a2", "urn:ent:2", "urn:rel:owner", "urn:user:2", KnowledgeState.INFERRED),
        _make_assertion("p1", "urn:ent:3", "urn:rel:owner", "urn:user:3", KnowledgeState.PROPOSED),
        _make_assertion("p2", "urn:ent:4", "urn:rel:owner", "urn:user:4", KnowledgeState.PROPOSED),
    ]

    # Default asserted-only query
    facts = filter_asserted_only(assertions, include_proposed=False)
    assert len(facts) == 2
    assert {f.assertion_id for f in facts} == {"a1", "a2"}
    assert "p1" not in {f.assertion_id for f in facts}

    # Explicit request for proposals
    all_items = filter_asserted_only(assertions, include_proposed=True)
    assert len(all_items) == 4


def test_trig_export_named_graph_separation():
    """CRA-045.5: TriG export places facts in tenant graph and proposals in distinct proposed graph."""
    assertions = [
        _make_assertion("fact1", "http://example.org/Alice", "http://example.org/knows", "http://example.org/Bob", KnowledgeState.ASSERTED),
        _make_assertion("prop1", "http://example.org/Alice", "http://example.org/recommends", "http://example.org/ProductX", KnowledgeState.PROPOSED),
    ]

    # Export without proposed statements: only tenant facts graph
    trig_facts_only = export_trig_quads(assertions, tenant_id="tenant_alpha", include_proposed=False)
    assert "<urn:eoip:tenant:tenant_alpha> {" in trig_facts_only
    assert "<http://example.org/Alice> <http://example.org/knows> <http://example.org/Bob> ." in trig_facts_only
    # Proposals graph must NOT exist
    assert "<urn:eoip:proposed:tenant_alpha>" not in trig_facts_only

    # Export with proposed statements included: proposals placed strictly in distinct named graph
    trig_with_proposals = export_trig_quads(assertions, tenant_id="tenant_alpha", include_proposed=True)
    assert "<urn:eoip:tenant:tenant_alpha> {" in trig_with_proposals
    assert "<urn:eoip:proposed:tenant_alpha> {" in trig_with_proposals
    assert "<http://example.org/Alice> <http://example.org/recommends> <http://example.org/ProductX> ." in trig_with_proposals
