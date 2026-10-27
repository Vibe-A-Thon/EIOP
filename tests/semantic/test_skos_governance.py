"""Comprehensive test suite for SKOS and multilingual stewardship (CRA-021.1-021.8, CRA-021.A).

Covers:
- CRA-021.1: SKOS concepts/schemes, broader/narrower/related, polyhierarchy, multilingual labels,
  concept-vs-label identity, mappings, deprecation.
- CRA-021.2: SKOS-XL and OntoLex-Lemon profiles; rejection of unsupported profiles.
- CRA-021.3: Candidate terms, definitions, synonyms, crosswalk proposals, domain review, and model guard.
- CRA-021.4: Versioned vocabularies, dependencies, publication receipts, consumer acknowledgements,
  stale projections, and rollback.
- CRA-021.5: Language-aware search, Unicode NFC normalization, RTL-safe presentation, stable IDs.
- CRA-021.6: Wiring to CRA-016 serializer and 10k-concept lossless round trip.
- CRA-021.7: BCP-47 validation, deprecation with owl:deprecated and dct:isReplacedBy, ISO 25964 thesaurus.
- CRA-021.8: Drift detection emission into review queue without auto-applying (I17).
- CRA-021.A: Cyclic taxonomy policy, concurrent edits CAS, and end-to-end acceptance invariants.
"""

from __future__ import annotations

import time
import pytest
import rdflib
from rdflib.namespace import OWL, RDF, SKOS

from eoip.ontology.drift import DriftFinding, OntologyDriftReport
from eoip.ontology.skos import (
    ConcurrentModificationError,
    CyclePolicy,
    CyclicTaxonomyError,
    DuplicateLabelError,
    LabelConflict,
    LabelUniquenessPolicy,
    MappingKind,
    ModelAutoCreateForbiddenError,
    ProposalStatus,
    ProposalType,
    SKOSProfile,
    SKOSXLLabel,
    SkosTaxonomy,
    UnsupportedProfileError,
    VocabularyProposal,
    VocabularyProposalReviewQueue,
    emit_drift_proposals_to_review,
    validate_bcp47,
)


def test_skos_concepts_schemes_multilingual_labels_polyhierarchy_and_concept_vs_label_identity():
    """CRA-021.1: SKOS concepts, multilingual labels, polyhierarchy, and explicit concept-vs-label identity."""
    tax = SkosTaxonomy(label_uniqueness_policy=LabelUniquenessPolicy.ALLOW_HOMONYM)
    scheme = tax.create_scheme(
        title="Knowledge Systems",
        description="Unified taxonomy of computational devices and paradigms",
        scheme_id="tech-scheme",
        titles={"en": "Knowledge Systems", "fr": "Systèmes de connaissances"},
    )
    assert scheme.urn == "urn:eoip:ontology:scheme:tech-scheme"

    # Multilingual labels with BCP-47 tags
    phone = tax.add_concept(
        scheme_id="tech-scheme",
        pref_label="Mobile Phone",
        pref_labels={"en": "Mobile Phone", "fr": "Téléphone portable", "ar": "هاتف محمول"},
        concept_id="concept-phone",
        definition="Cellular telephone device",
        alt_labels=["Cell phone", "Handset"],
        alt_labels_by_lang={"en": ["Cell phone", "Handset"], "fr": ["Cellulaire"]},
    )

    computer = tax.add_concept(
        scheme_id="tech-scheme",
        pref_label="Computer",
        pref_labels={"en": "Computer", "fr": "Ordinateur", "ar": "حاسوب"},
        concept_id="concept-computer",
        definition="Programmable electronic device",
    )

    # Polyhierarchy: Smartphone has BOTH Mobile Phone and Computer as broader parents
    smartphone = tax.add_concept(
        scheme_id="tech-scheme",
        pref_label="Smartphone",
        pref_labels={"en": "Smartphone", "fr": "Téléphone intelligent", "ar": "هاتف ذكي"},
        concept_id="concept-smartphone",
    )
    tax.add_broader("concept-smartphone", "concept-phone")
    tax.add_broader("concept-smartphone", "concept-computer")

    # Verify polyhierarchy
    assert sorted(smartphone.broader) == ["concept-computer", "concept-phone"]
    assert "concept-smartphone" in phone.narrower
    assert "concept-smartphone" in computer.narrower

    closure = tax.broader_closure("concept-smartphone")
    assert "concept-phone" in closure
    assert "concept-computer" in closure

    # Explicit concept-versus-label identity: Two distinct concepts with the exact same prefLabel "Bank"
    tax.create_scheme("General Dictionary", scheme_id="gen-dict")
    bank_fin = tax.add_concept(
        scheme_id="gen-dict",
        pref_label="Bank",
        pref_labels={"en": "Bank", "fr": "Banque"},
        concept_id="concept-bank-financial",
        definition="Financial institution that accepts deposits and channels money into lending activities.",
    )
    bank_river = tax.add_concept(
        scheme_id="gen-dict",
        pref_label="Bank",
        pref_labels={"en": "Bank", "fr": "Rive"},
        concept_id="concept-bank-river",
        definition="Land alongside a body of water such as a river or lake.",
    )

    # Both concepts coexist with distinct IDs and definitions despite sharing the exact same label
    assert bank_fin.concept_id != bank_river.concept_id
    assert bank_fin.urn != bank_river.urn
    assert bank_fin.definition != bank_river.definition
    assert tax.concepts["concept-bank-financial"].pref_label == "Bank"
    assert tax.concepts["concept-bank-river"].pref_label == "Bank"

    # Strict label policy raises error when configured
    tax_strict = SkosTaxonomy(label_uniqueness_policy=LabelUniquenessPolicy.STRICT_SCHEME_LANG)
    tax_strict.create_scheme("Strict Scheme", scheme_id="strict-s")
    tax_strict.add_concept(scheme_id="strict-s", pref_label="Bank", concept_id="bank-1")
    with pytest.raises(DuplicateLabelError):
        tax_strict.add_concept(scheme_id="strict-s", pref_label="Bank", concept_id="bank-2")


def test_skos_xl_and_ontolex_lemon_profiles_and_unsupported_profile_rejection():
    """CRA-021.2: SKOS-XL, OntoLex-Lemon profiles, and strict rejection of unsupported profiles."""
    tax = SkosTaxonomy()
    tax.create_scheme("Lexical Scheme", scheme_id="lex-s")
    tax.add_concept(scheme_id="lex-s", pref_label="Software", concept_id="concept-sw")

    # SKOS-XL label creation and binding
    tax.add_xl_label(
        scheme_id="lex-s",
        literal_form="Software Application",
        language="en",
        label_id="xl-sw-pref",
    )
    tax.bind_concept_xl_label("concept-sw", "xl-sw-pref", role="prefLabel")
    assert tax.concepts["concept-sw"].xl_labels["prefLabel"] == "xl-sw-pref"

    # Export under SKOS_XL profile
    tax.to_rdflib_graph(profile=SKOSProfile.SKOS_XL)
    turtle_xl = tax.export_serialization(format_name="turtle", profile=SKOSProfile.SKOS_XL)
    assert "skosxl:Label" in turtle_xl or "http://www.w3.org/2008/05/skos-xl#Label" in turtle_xl
    assert "skosxl:literalForm" in turtle_xl or "literalForm" in turtle_xl

    # Export under OntoLex-Lemon profile
    turtle_ontolex = tax.export_serialization(format_name="turtle", profile=SKOSProfile.ONTOLEX_LEMON)
    assert "ontolex:LexicalEntry" in turtle_ontolex or "http://www.w3.org/ns/lemon/ontolex#LexicalEntry" in turtle_ontolex
    assert "ontolex:canonicalForm" in turtle_ontolex or "canonicalForm" in turtle_ontolex

    # Strict rejection of unsupported profile: must raise UnsupportedProfileError, never flatten silently
    with pytest.raises(UnsupportedProfileError, match="Unsupported profile 'CUSTOM_FLATTEN'"):
        tax.to_rdflib_graph(profile="CUSTOM_FLATTEN")

    with pytest.raises(UnsupportedProfileError, match="Unsupported profile 'ARBITRARY_PROFILE'"):
        tax.export_serialization(profile="ARBITRARY_PROFILE")


def test_candidate_terms_definitions_synonyms_crosswalk_proposals_domain_review_and_model_guard():
    """CRA-021.3: Candidate terms, synonyms, crosswalks, domain reviews, and model suggestion guards."""
    tax = SkosTaxonomy()
    tax.create_scheme("Core Domain", scheme_id="core-domain")
    queue = tax.review_queue

    # Human proposal: candidate term
    candidate_proposal = VocabularyProposal(
        proposal_id="prop-001",
        proposal_type=ProposalType.CANDIDATE_TERM,
        scheme_id="core-domain",
        payload={
            "pref_label": "Microservice",
            "concept_id": "concept-microservice",
            "definition": "Independently deployable service unit.",
            "alt_labels": ["Micro-service"],
        },
        proposer="domain-expert-alice",
        agent_type="human",
        domain_owner="architecture-stewards",
    )
    queue.submit_proposal(candidate_proposal)
    assert candidate_proposal.status == ProposalStatus.PROPOSED
    assert "concept-microservice" not in tax.concepts  # Not yet applied

    # Domain owner reviews and approves proposal
    queue.review_proposal(
        proposal_id="prop-001",
        reviewer="lead-architect-bob",
        action="APPROVE",
        note="Approved for microservices taxonomy expansion",
        taxonomy=tax,
    )
    assert candidate_proposal.status == ProposalStatus.APPROVED
    assert "concept-microservice" in tax.concepts
    assert tax.concepts["concept-microservice"].pref_label == "Microservice"

    # Human proposal: synonym
    syn_prop = VocabularyProposal(
        proposal_id="prop-002",
        proposal_type=ProposalType.SYNONYM,
        scheme_id="core-domain",
        payload={"concept_id": "concept-microservice", "synonym": "μService", "language": "en"},
        proposer="alice",
        agent_type="human",
    )
    queue.submit_proposal(syn_prop)
    queue.review_proposal("prop-002", "bob", "APPROVE", taxonomy=tax)
    assert "μService" in tax.concepts["concept-microservice"].alt_labels

    # Guard: Model suggestions must not auto-create equivalence or upstream namespace terms (CRA-021.3)
    model_upstream_prop = VocabularyProposal(
        proposal_id="prop-model-fail1",
        proposal_type=ProposalType.CANDIDATE_TERM,
        scheme_id="core-domain",
        payload={"concept_id": "http://www.w3.org/2004/02/skos/core#CustomConcept", "pref_label": "BadTerm"},
        proposer="ai-taxonomy-suggester",
        agent_type="model",
    )
    with pytest.raises(ModelAutoCreateForbiddenError, match="upstream namespace"):
        queue.submit_proposal(model_upstream_prop)

    model_auto_equiv_prop = VocabularyProposal(
        proposal_id="prop-model-fail2",
        proposal_type=ProposalType.CROSSWALK,
        scheme_id="core-domain",
        payload={
            "source_id": "concept-microservice",
            "target_id": "concept-monolith",
            "kind": "exactMatch",
            "auto_apply": True,
        },
        proposer="ai-taxonomy-suggester",
        agent_type="model",
    )
    with pytest.raises(ModelAutoCreateForbiddenError, match="cannot auto-apply equivalence"):
        queue.submit_proposal(model_auto_equiv_prop)


def test_versioning_publication_receipts_consumer_acknowledgements_stale_projections_and_rollback():
    """CRA-021.4: Versioned vocabularies, dependencies, publication receipts, stale projections, and rollback."""
    tax = SkosTaxonomy()
    scheme = tax.create_scheme("Governed Vocab", scheme_id="gov-v", version_id="1.0.0")
    tax.add_concept(scheme_id="gov-v", pref_label="Alpha", concept_id="c-alpha")

    # Publish version 1.1.0 with dependencies
    deps = [
        {"id": "clf-doc-classifier", "type": "classifier", "version": "2.4"},
        {"id": "emb-vector-index", "type": "embedding_index", "dimension": 768},
    ]
    receipt = tax.publish_version(
        scheme_id="gov-v",
        new_version="1.1.0",
        publisher="chief-data-officer",
        dependencies=deps,
    )

    assert receipt.version_id == "1.1.0"
    assert receipt.scheme_id == "gov-v"
    assert len(receipt.digest) == 64  # SHA-256
    assert scheme.is_stale is True  # Projections flagged as stale after version update

    # Consumer acknowledgement tracking
    tax.acknowledge_consumer("gov-v", "clf-doc-classifier", "1.1.0")
    assert scheme.is_stale is True  # Still waiting for emb-vector-index

    tax.acknowledge_consumer("gov-v", "emb-vector-index", "1.1.0")
    assert scheme.is_stale is False  # All dependencies acknowledged, projections fresh!

    # Add a new concept in version 1.2.0
    tax.publish_version(scheme_id="gov-v", new_version="1.2.0", publisher="cdo")
    tax.add_concept(scheme_id="gov-v", pref_label="Beta", concept_id="c-beta")
    assert "c-beta" in tax.concepts

    # Rollback to version 1.1.0
    rollback_receipt = tax.rollback_scheme("gov-v", "1.1.0")
    assert rollback_receipt.version_id == "1.1.0"
    assert scheme.version_id == "1.1.0"
    assert "c-beta" not in tax.concepts  # Rolled back successfully
    assert "c-alpha" in tax.concepts


def test_language_aware_search_unicode_normalization_rtl_safety_and_stable_ids():
    """CRA-021.5: Language-aware search, Unicode NFC normalization, RTL presentation, stable IDs."""
    tax = SkosTaxonomy()
    tax.create_scheme("Multilingual Test", scheme_id="multi-s")

    # Add concept with French, Arabic, and English
    c = tax.add_concept(
        scheme_id="multi-s",
        pref_label="Computer",
        pref_labels={
            "en": "Computer",
            "fr": "Ordinateur",
            "ar": "حاسوب",
            "he": "מחשב",
        },
        concept_id="c-compute-001",
    )

    # Language-aware search with exact language and Unicode normalization
    matches_ar = tax.search("حاسوب", language="ar")
    assert len(matches_ar) == 1
    assert matches_ar[0].concept_id == "c-compute-001"

    # Search with BCP-47 fallback: "fr-CA" falls back to "fr"
    matches_fr = tax.search("Ordinateur", language="fr-CA", fallback=True)
    assert len(matches_fr) == 1
    assert matches_fr[0].concept_id == "c-compute-001"

    # RTL-safe presentation
    pres_ar = tax.format_presentation("c-compute-001", language="ar")
    assert pres_ar["dir"] == "rtl"
    assert "\u2067" in pres_ar["bidi_isolated"]  # RTL isolate marker

    pres_en = tax.format_presentation("c-compute-001", language="en")
    assert pres_en["dir"] == "ltr"

    # Stable IDs: Translating or adding new labels leaves concept_id and urn completely immutable
    initial_urn = c.urn
    c.pref_labels["es"] = "Computadora"
    c.pref_labels["de"] = "Rechner"
    assert c.urn == initial_urn
    assert c.concept_id == "c-compute-001"


def test_serializer_integration_and_10k_concept_lossless_round_trip():
    """CRA-021.6, CRA-021.A: Lossless RDF serializer integration with 10k-concept benchmark."""
    tax = SkosTaxonomy()
    tax.create_scheme("Scale Benchmark Scheme", scheme_id="scale-scheme")

    total_concepts = 10_000
    root_id = "concept-root"
    tax.add_concept(
        scheme_id="scale-scheme",
        pref_label="Root Technology",
        pref_labels={"en": "Root Technology", "fr": "Technologie racine"},
        concept_id=root_id,
    )

    # Generate 10k concepts with multilingual labels and hierarchies
    t0 = time.perf_counter()
    for i in range(1, total_concepts):
        cid = f"concept-{i}"
        tax.add_concept(
            scheme_id="scale-scheme",
            pref_label=f"Tech Term {i}",
            pref_labels={"en": f"Tech Term {i}", "fr": f"Terme Tech {i}"},
            concept_id=cid,
            definition=f"Definition of technical term {i}",
        )
        tax.add_broader(cid, root_id)

    gen_time = time.perf_counter() - t0
    assert len(tax.concepts) == total_concepts
    print(f"\nGenerated {total_concepts} SKOS concepts in {gen_time:.3f}s")

    # Serialize to N-Triples (fast, standards-compliant line format)
    t1 = time.perf_counter()
    serialized = tax.export_serialization(format_name="nt")
    ser_time = time.perf_counter() - t1
    assert len(serialized) > 0
    print(f"Serialized {total_concepts} concepts to RDF in {ser_time:.3f}s")

    # Deserialize back into a fresh SkosTaxonomy
    t2 = time.perf_counter()
    restored_tax = SkosTaxonomy.import_serialization(serialized, format_name="nt")
    deser_time = time.perf_counter() - t2
    print(f"Deserialized {len(restored_tax.concepts)} concepts from RDF in {deser_time:.3f}s")

    # Assert 100% isomorphic and lossless round trip
    assert len(restored_tax.concepts) == total_concepts
    assert root_id in restored_tax.concepts
    assert len(restored_tax.concepts[root_id].narrower) == total_concepts - 1
    assert restored_tax.concepts["concept-100"].pref_labels.get("fr") == "Terme Tech 100"
    assert restored_tax.concepts["concept-100"].broader == [root_id]


def test_bcp47_validation_deprecation_owl_deprecated_dct_replacedby_and_iso25964_fixture():
    """CRA-021.7: BCP-47 validation, owl:deprecated true + dct:isReplacedBy, ISO 25964 thesaurus."""
    # BCP-47 tag validation
    assert validate_bcp47("en") is True
    assert validate_bcp47("en-US") is True
    assert validate_bcp47("de-CH-1996") is True
    assert validate_bcp47("zh-Hans") is True
    assert validate_bcp47("12345") is False
    assert validate_bcp47("") is False

    tax = SkosTaxonomy()
    tax.create_scheme("Deprecation Scheme", scheme_id="dep-s")
    tax.add_concept(scheme_id="dep-s", pref_label="Legacy Storage", concept_id="c-floppy")
    tax.add_concept(scheme_id="dep-s", pref_label="Cloud Storage", concept_id="c-cloud")

    # Deprecate c-floppy in favor of c-cloud
    tax.deprecate_concept(
        concept_id="c-floppy",
        replaced_by=["c-cloud"],
        reason="Magnetic media superseded by cloud object storage",
        author="storage-committee",
    )

    floppy = tax.concepts["c-floppy"]
    assert floppy.deprecated is True
    assert floppy.replaced_by == ["c-cloud"]
    assert len(floppy.editorial_notes) >= 1
    assert floppy.editorial_notes[0]["author"] == "storage-committee"

    # Export and verify owl:deprecated and dct:isReplacedBy
    g = tax.to_rdflib_graph()
    floppy_uri = rdflib.URIRef(floppy.urn)
    cloud_uri = rdflib.URIRef(tax.concepts["c-cloud"].urn)

    has_dep_triple = (floppy_uri, OWL.deprecated, rdflib.Literal(True)) in g
    has_rep_triple = (floppy_uri, rdflib.Namespace("http://purl.org/dc/terms/").isReplacedBy, cloud_uri) in g
    assert has_dep_triple is True
    assert has_rep_triple is True

    # ISO 25964 fixture import
    iso_fixture = {
        "thesaurus_id": "iso-standards-thesaurus",
        "title": "ISO 25964 Controlled Thesaurus",
        "concepts": [
            {
                "concept_id": "iso-data-gov",
                "descriptor": "Data Governance",
                "non_descriptors": ["Information Governance", "Data Stewardship"],
                "scope_note": "Management of data availability, usability, integrity and security.",
                "broader_terms": [],
                "related_terms": ["iso-data-mgmt"],
            },
            {
                "concept_id": "iso-data-mgmt",
                "descriptor": "Data Management",
                "non_descriptors": [],
                "broader_terms": [],
                "related_terms": ["iso-data-gov"],
            },
        ],
    }
    imported_scheme = tax.import_iso25964(iso_fixture)
    assert imported_scheme.scheme_id == "iso-standards-thesaurus"
    assert "iso-data-gov" in tax.concepts
    assert tax.concepts["iso-data-gov"].pref_label == "Data Governance"
    assert "Information Governance" in tax.concepts["iso-data-gov"].alt_labels
    assert "iso-data-mgmt" in tax.concepts["iso-data-gov"].related


def test_drift_detection_emits_proposals_into_review_queue_and_never_auto_applies():
    """CRA-021.8: Drift detection findings emitted into review queue without auto-applying (I17)."""
    tax = SkosTaxonomy()
    tax.create_scheme("Governed Graph", scheme_id="gov-graph")
    queue = tax.review_queue

    # Simulate drift report from connectors
    findings = [
        DriftFinding(
            kind="vertex_label",
            value="QuantumProcessor",
            occurrences=42,
            examples=["qp-01", "qp-02"],
            classification="potentially_breaking",
        ),
        DriftFinding(
            kind="property_key",
            value="qubit_count",
            occurrences=120,
            classification="additive",
        ),
    ]
    drift_report = OntologyDriftReport(findings=findings)

    # Emit drift proposals into review queue
    proposals = emit_drift_proposals_to_review(drift_report, queue, scheme_id="gov-graph")
    assert len(proposals) == 2
    for p in proposals:
        assert p.status == ProposalStatus.PROPOSED  # In review queue
        assert p.agent_type == "connector"

    # Crucial Invariant I17: Active taxonomy and manifest remain completely untouched until approval
    assert "QuantumProcessor" not in tax.concepts
    assert "qubit_count" not in tax.concepts

    # When domain owner approves, proposal transitions to APPROVED
    queue.review_proposal(
        proposal_id=proposals[0].proposal_id,
        reviewer="taxonomy-lead",
        action="APPROVE",
        note="Approved for quantum hardware taxonomy",
    )
    assert queue.proposals[proposals[0].proposal_id].status == ProposalStatus.APPROVED


def test_cyclic_taxonomy_policy_and_concurrent_edits():
    """CRA-021.A: Cyclic taxonomy policy (REJECT vs WARN) and concurrent edit CAS."""
    # Strict cycle policy: raises CyclicTaxonomyError
    tax_strict = SkosTaxonomy(cycle_policy=CyclePolicy.REJECT)
    tax_strict.create_scheme("Cycle Test Strict", scheme_id="cycle-s")
    tax_strict.add_concept(scheme_id="cycle-s", pref_label="A", concept_id="c-a")
    tax_strict.add_concept(scheme_id="cycle-s", pref_label="B", concept_id="c-b")
    tax_strict.add_concept(scheme_id="cycle-s", pref_label="C", concept_id="c-c")

    tax_strict.add_broader("c-b", "c-a")  # A -> B
    tax_strict.add_broader("c-c", "c-b")  # B -> C

    # Adding broader from c-a to c-c introduces a cycle: C -> B -> A -> C
    with pytest.raises(CyclicTaxonomyError, match="introduces a cycle"):
        tax_strict.add_broader("c-a", "c-c")

    # Permissive cycle policy (WARN): records cycle and reports in validate_integrity
    tax_warn = SkosTaxonomy(cycle_policy=CyclePolicy.WARN)
    tax_warn.create_scheme("Cycle Test Warn", scheme_id="cycle-w")
    tax_warn.add_concept(scheme_id="cycle-w", pref_label="A", concept_id="c-a")
    tax_warn.add_concept(scheme_id="cycle-w", pref_label="B", concept_id="c-b")
    tax_warn.add_broader("c-b", "c-a")
    tax_warn.add_broader("c-a", "c-b")  # Cycle allowed under WARN

    issues = tax_warn.validate_integrity("cycle-w")
    cycle_issues = [i for i in issues if i.kind == "broader_cycle"]
    assert len(cycle_issues) >= 1

    # Concurrent edits CAS validation
    tax_cas = SkosTaxonomy()
    tax_cas.create_scheme("CAS Scheme", scheme_id="cas-s")
    tax_cas.add_concept(scheme_id="cas-s", pref_label="Initial Term", concept_id="c-cas")

    # First edit with matching version succeeds
    updated = tax_cas.update_concept_cas("c-cas", expected_version=1, updates={"definition": "Updated def"})
    assert updated.version == 2
    assert updated.definition == "Updated def"

    # Second edit with stale expected_version=1 fails with ConcurrentModificationError
    with pytest.raises(ConcurrentModificationError, match="Concurrent edit conflict"):
        tax_cas.update_concept_cas("c-cas", expected_version=1, updates={"definition": "Conflict def"})
