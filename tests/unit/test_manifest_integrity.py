"""Ontology manifest integrity: HugeGraph rejects edge labels that reference
undefined vertex labels or property keys, so the manifest must stay internally
consistent (regression test for the schema-init bootstrap failure)."""

import pytest
from eoip.ontology.manifest import (
    DOMAINS,
    EDGE_LABELS,
    PROPERTY_KEYS,
    VERTEX_LABELS,
    edge_endpoints_valid,
)


@pytest.mark.req("FR-ONTO-001", "FR-ONTO-002")
def test_every_edge_endpoint_is_a_known_vertex_label():
    labels = set(VERTEX_LABELS)
    for edge_label, (outs, ins, _props) in EDGE_LABELS.items():
        for out_label in outs:
            assert out_label in labels, f"{edge_label} out endpoint {out_label} undefined"
        for in_label in ins:
            assert in_label in labels, f"{edge_label} in endpoint {in_label} undefined"


def test_every_label_property_is_a_declared_property_key():
    for label, (_domain, required, optional) in VERTEX_LABELS.items():
        for prop in [*required, *optional]:
            assert prop in PROPERTY_KEYS, f"{label}.{prop} missing from PROPERTY_KEYS"


def test_edge_endpoint_validation_matches_manifest():
    for edge_label, (outs, ins, _props) in EDGE_LABELS.items():
        assert edge_endpoints_valid(edge_label, outs[0], ins[0])


def test_every_vertex_domain_is_declared():
    for label, (domain, _required, _optional) in VERTEX_LABELS.items():
        assert domain in DOMAINS, f"{label} uses undeclared domain {domain}"


def test_belongs_to_domain_targets_graph_domain():
    outs, ins, _ = EDGE_LABELS["BELONGS_TO_DOMAIN"]
    assert ins == ["GraphDomain"]
    assert "GraphDomain" in VERTEX_LABELS
    assert outs
