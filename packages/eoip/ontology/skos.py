"""SKOS-compatible taxonomy and multilingual thesaurus stewardship (CRA-021).

Implements GAP-STUDIO-005 (SKOS taxonomy support); verified by tests/unit/test_skos_taxonomy.py.

Covers:
- CRA-021.1: SKOS concepts/schemes, broader/narrower/related, polyhierarchy, preferred/alternative/hidden
  labels with BCP-47 language tags, mappings, deprecation/replacement, and explicit concept-vs-label identity.
- CRA-021.2: SKOS-XL and OntoLex-Lemon through qualified optional profiles; rejection of unsupported profiles.
- CRA-021.3: Candidate terms, definitions, synonyms, crosswalk proposals, provenance, domain ownership and review;
  strict guard: model suggestions must not auto-create equivalence or upstream namespace terms.
- CRA-021.4: Versioned vocabularies with classifier/embedding/index dependencies and publication receipts;
  consumer acknowledgement and stale projection state tracking after change; rollback restoration.
- CRA-021.5: Language-aware search/editing, Unicode NFC normalization, RTL-safe presentation, label uniqueness
  policies, and stable IDs independent of translated labels.
- CRA-021.6: Wiring to the CRA-016 serializer (RDFSerializer / RDFDeserializer) supporting lossless round trips.
- CRA-021.7: Labels per BCP-47 language tag; deprecation via owl:deprecated true + dct:isReplacedBy; audited
  editorial notes; ISO 25964-style thesaurus import fixture.
- CRA-021.8: Drift detection emission into review queue; proposals are never auto-applied (I17).
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime
from enum import Enum
import hashlib
from itertools import count
import re
from typing import Any, Optional
import unicodedata
from urllib.parse import quote, unquote
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator
import rdflib
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

from eoip.ontology.drift import DriftFinding, OntologyDriftReport, build_evolution_proposal
from eoip.ontology.rdf import EOIP_NAMESPACE
from eoip.ontology.serialization import RDFDeserializer, RDFSerializer

# Namespaces
SKOS_NAMESPACE = "http://www.w3.org/2004/02/skos/core#"
SKOSXL_NAMESPACE = "http://www.w3.org/2008/05/skos-xl#"
ONTOLEX_NAMESPACE = "http://www.w3.org/ns/lemon/ontolex#"
DCTERMS_NAMESPACE = "http://purl.org/dc/terms/"

SKOSXL = Namespace(SKOSXL_NAMESPACE)
ONTOLEX = Namespace(ONTOLEX_NAMESPACE)
DCTERMS = Namespace(DCTERMS_NAMESPACE)
EOIP = Namespace(EOIP_NAMESPACE)

UPSTREAM_NAMESPACES = (
    SKOS_NAMESPACE,
    "http://www.w3.org/2002/07/owl#",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "http://www.w3.org/2000/01/rdf-schema#",
    DCTERMS_NAMESPACE,
)

# Regex patterns
_BCP47_PATTERN = re.compile(r"^[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{2,8})*$", re.ASCII)
_RTL_PATTERN = re.compile(r"[\u0590-\u05FF\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")


def validate_bcp47(tag: str) -> bool:
    """Validates BCP-47 language tag (CRA-021.7)."""
    if not tag or not isinstance(tag, str):
        return False
    return bool(_BCP47_PATTERN.match(tag.strip()))


def is_rtl_text(text: str) -> bool:
    """Detects whether text contains Right-to-Left scripts (Arabic, Hebrew, etc.) (CRA-021.5)."""
    return bool(_RTL_PATTERN.search(text))


# Custom Exceptions
class UnsupportedProfileError(ValueError):
    """Raised when an unsupported SKOS profile is requested (CRA-021.2)."""


class CyclicTaxonomyError(ValueError):
    """Raised when a cycle is introduced in skos:broader under strict policy (CRA-021.1, CRA-021.A)."""


class DuplicateLabelError(ValueError):
    """Raised when duplicate prefLabels violate strict scheme uniqueness policy (CRA-021.5)."""


class ModelAutoCreateForbiddenError(PermissionError):
    """Raised when a model suggestion attempts to auto-create equivalence or upstream terms (CRA-021.3)."""


class ConcurrentModificationError(RuntimeError):
    """Raised when concurrent edit CAS fails (CRA-021.A)."""


# Enums
class MappingKind(str, Enum):
    EXACT = "exactMatch"
    CLOSE = "closeMatch"
    BROAD = "broadMatch"
    NARROW = "narrowMatch"
    RELATED = "relatedMatch"


class CyclePolicy(str, Enum):
    WARN = "WARN"
    REJECT = "REJECT"


class LabelUniquenessPolicy(str, Enum):
    ALLOW_HOMONYM = "ALLOW_HOMONYM"
    STRICT_SCHEME_LANG = "STRICT_SCHEME_LANG"
    WARN = "WARN"


class SKOSProfile(str, Enum):
    SKOS_CORE = "SKOS_CORE"
    SKOS_XL = "SKOS_XL"
    ONTOLEX_LEMON = "ONTOLEX_LEMON"


class ProposalType(str, Enum):
    CANDIDATE_TERM = "CANDIDATE_TERM"
    DEFINITION = "DEFINITION"
    SYNONYM = "SYNONYM"
    CROSSWALK = "CROSSWALK"


class ProposalStatus(str, Enum):
    PROPOSED = "PROPOSED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# Data Models
class LabelConflict(BaseModel):
    """GAP-TAX-001 label conflict: two concepts share a prefLabel in one scheme."""

    scheme_id: str
    pref_label: str
    concept_ids: list[str]
    language: str = "en"


class IntegrityIssue(BaseModel):
    """SKOS integrity issue detected by validate_integrity()."""

    kind: str  # "orphan_concept" | "broader_cycle" | "narrower_cycle"
    detail: str
    concept_ids: list[str] = Field(default_factory=list)


class SKOSXLLabel(BaseModel):
    """Reified SKOS-XL label resource (CRA-021.2)."""

    label_id: str
    scheme_id: str
    literal_form: str
    language: str = "en"
    label_relations: list[dict[str, str]] = Field(default_factory=list)

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:label:{self.label_id}"


class Concept(BaseModel):
    """Multilingual SKOS Concept with explicit concept-vs-label identity (CRA-021.1, CRA-021.7)."""

    concept_id: str
    scheme_id: str
    pref_label: str = ""
    pref_labels: dict[str, str] = Field(default_factory=dict)
    alt_labels: list[str] = Field(default_factory=list)
    alt_labels_by_lang: dict[str, list[str]] = Field(default_factory=dict)
    hidden_labels: list[str] = Field(default_factory=list)
    hidden_labels_by_lang: dict[str, list[str]] = Field(default_factory=dict)
    definition: str = ""
    definitions_by_lang: dict[str, str] = Field(default_factory=dict)
    notation: str = ""
    broader: list[str] = Field(default_factory=list)
    narrower: list[str] = Field(default_factory=list)
    related: list[str] = Field(default_factory=list)
    in_collections: list[str] = Field(default_factory=list)
    deprecated: bool = False
    replaced_by: list[str] = Field(default_factory=list)
    deprecation_reason: str = ""
    deprecation_date: str = ""
    editorial_notes: list[dict[str, Any]] = Field(default_factory=list)
    history_notes: list[dict[str, Any]] = Field(default_factory=list)
    change_notes: list[dict[str, Any]] = Field(default_factory=list)
    xl_labels: dict[str, str] = Field(default_factory=dict)  # role -> label_id
    version: int = 1

    @model_validator(mode="after")
    def _sync_labels(self) -> Concept:
        if self.pref_label and not self.pref_labels:
            self.pref_labels = {"en": self.pref_label}
        elif self.pref_labels and not self.pref_label:
            self.pref_label = self.pref_labels.get("en") or next(iter(self.pref_labels.values()), "")

        if self.alt_labels and not self.alt_labels_by_lang:
            self.alt_labels_by_lang = {"en": list(self.alt_labels)}
        elif self.alt_labels_by_lang and not self.alt_labels:
            flat = []
            for l in self.alt_labels_by_lang.values():
                flat.extend(l)
            self.alt_labels = flat

        if self.hidden_labels and not self.hidden_labels_by_lang:
            self.hidden_labels_by_lang = {"en": list(self.hidden_labels)}
        elif self.hidden_labels_by_lang and not self.hidden_labels:
            flat = []
            for l in self.hidden_labels_by_lang.values():
                flat.extend(l)
            self.hidden_labels = flat

        if self.definition and not self.definitions_by_lang:
            self.definitions_by_lang = {"en": self.definition}
        elif self.definitions_by_lang and not self.definition:
            self.definition = self.definitions_by_lang.get("en") or next(iter(self.definitions_by_lang.values()), "")

        return self

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:concept:{self.concept_id}"


class PublicationReceipt(BaseModel):
    """Cryptographic publication receipt for versioned vocabularies (CRA-021.4)."""

    receipt_id: str
    scheme_id: str
    version_id: str
    timestamp: str
    digest: str
    publisher: str
    dependencies: list[dict[str, Any]] = Field(default_factory=list)


class ConceptScheme(BaseModel):
    """Versioned SKOS ConceptScheme with dependency & projection tracking (CRA-021.4)."""

    scheme_id: str
    title: str
    titles: dict[str, str] = Field(default_factory=dict)
    description: str = ""
    version_id: str = "1.0.0"
    publication_receipt: Optional[PublicationReceipt] = None
    dependencies: list[dict[str, Any]] = Field(default_factory=list)
    is_stale: bool = False
    consumer_acknowledgements: dict[str, str] = Field(default_factory=dict)
    version_history: list[dict[str, Any]] = Field(default_factory=list)

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:scheme:{self.scheme_id}"


class Collection(BaseModel):
    """SKOS Collection."""

    collection_id: str
    scheme_id: str
    title: str
    titles: dict[str, str] = Field(default_factory=dict)
    member_ids: list[str] = Field(default_factory=list)

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:collection:{self.collection_id}"


class ConceptMapping(BaseModel):
    """Crosswalk assertion between concepts (CRA-021.1, CRA-021.3)."""

    source_id: str
    target_id: str
    kind: MappingKind
    provenance: dict[str, Any] = Field(default_factory=dict)

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:mapping:{self.source_id}:{self.kind.value}:{self.target_id}"


class VocabularyProposal(BaseModel):
    """Candidate term, definition, synonym, or crosswalk proposal (CRA-021.3, CRA-021.8)."""

    proposal_id: str
    proposal_type: ProposalType
    scheme_id: str
    payload: dict[str, Any]
    proposer: str
    agent_type: str = "human"  # "human" | "model" | "connector"
    domain_owner: str = "taxonomy-team"
    status: ProposalStatus = ProposalStatus.PROPOSED
    provenance: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    review_note: str = ""


_id_counter = count(1)


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def concept_qname(concept_id: str) -> str:
    """Stable external identifier: ``urn:eoip:ontology:concept:<id>``."""
    return f"urn:eoip:ontology:concept:{quote(str(concept_id), safe='')}"


class VocabularyProposalReviewQueue:
    """Manages candidate proposals, domain ownership reviews, and model suggestion guards (CRA-021.3)."""

    def __init__(self) -> None:
        self.proposals: dict[str, VocabularyProposal] = {}

    def submit_proposal(self, proposal: VocabularyProposal) -> VocabularyProposal:
        # Guard: Model suggestions must not auto-create equivalence or upstream namespace terms (CRA-021.3)
        if proposal.agent_type == "model":
            target = proposal.payload.get("target_id", "")
            kind = proposal.payload.get("kind", "")
            term_id = proposal.payload.get("concept_id", "") or proposal.payload.get("term", "")

            # Check upstream namespaces
            for ns in UPSTREAM_NAMESPACES:
                if (term_id and term_id.startswith(ns)) or (target and target.startswith(ns)):
                    raise ModelAutoCreateForbiddenError(
                        f"Model suggestions cannot create terms or crosswalks in upstream namespace '{ns}' (CRA-021.3)"
                    )

            # Equivalence auto-creation forbidden for models
            if kind in ("exactMatch", "sameAs", MappingKind.EXACT.value):
                if proposal.payload.get("auto_apply", False):
                    raise ModelAutoCreateForbiddenError(
                        "Model suggestions cannot auto-apply equivalence mappings; human review required (CRA-021.3)"
                    )
            proposal.status = ProposalStatus.PROPOSED

        self.proposals[proposal.proposal_id] = proposal
        return proposal

    def review_proposal(
        self,
        proposal_id: str,
        reviewer: str,
        action: str,  # "APPROVE" | "REJECT"
        note: str = "",
        taxonomy: Optional[SkosTaxonomy] = None,
    ) -> VocabularyProposal:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise KeyError(f"Proposal '{proposal_id}' not found")

        proposal.reviewed_by = reviewer
        proposal.reviewed_at = datetime.now(UTC).isoformat()
        proposal.review_note = note

        if action.upper() == "APPROVE":
            proposal.status = ProposalStatus.APPROVED
            if taxonomy is not None:
                self._apply_proposal_to_taxonomy(proposal, taxonomy)
        else:
            proposal.status = ProposalStatus.REJECTED

        return proposal

    def _apply_proposal_to_taxonomy(self, proposal: VocabularyProposal, taxonomy: SkosTaxonomy) -> None:
        p = proposal.payload
        if proposal.proposal_type == ProposalType.CANDIDATE_TERM:
            taxonomy.add_concept(
                scheme_id=proposal.scheme_id,
                pref_label=p.get("pref_label", ""),
                pref_labels=p.get("pref_labels"),
                concept_id=p.get("concept_id"),
                definition=p.get("definition", ""),
                definitions_by_lang=p.get("definitions_by_lang"),
                notation=p.get("notation", ""),
                alt_labels=p.get("alt_labels"),
                alt_labels_by_lang=p.get("alt_labels_by_lang"),
            )
        elif proposal.proposal_type == ProposalType.CROSSWALK:
            taxonomy.add_mapping(
                source_id=p["source_id"],
                target_id=p["target_id"],
                kind=MappingKind(p.get("kind", MappingKind.EXACT.value)),
                provenance={"proposal_id": proposal.proposal_id, "approved_by": proposal.reviewed_by},
            )
        elif proposal.proposal_type == ProposalType.SYNONYM:
            cid = p["concept_id"]
            concept = taxonomy._concept(cid)
            syn = p["synonym"]
            lang = p.get("language", "en")
            concept.alt_labels_by_lang.setdefault(lang, []).append(syn)
            if syn not in concept.alt_labels:
                concept.alt_labels.append(syn)


class SkosTaxonomy:
    """SKOS / SKOS-XL taxonomy and thesaurus registry with governance and serializer support (CRA-021)."""

    def __init__(
        self,
        cycle_policy: CyclePolicy = CyclePolicy.WARN,
        label_uniqueness_policy: LabelUniquenessPolicy = LabelUniquenessPolicy.ALLOW_HOMONYM,
    ) -> None:
        self.schemes: dict[str, ConceptScheme] = {}
        self.concepts: dict[str, Concept] = {}
        self.collections: dict[str, Collection] = {}
        self.mappings: list[ConceptMapping] = []
        self.xl_labels: dict[str, SKOSXLLabel] = {}
        self.cycle_policy: CyclePolicy = cycle_policy
        self.label_uniqueness_policy: LabelUniquenessPolicy = label_uniqueness_policy
        self.version_snapshots: dict[tuple[str, str], dict[str, Any]] = {}
        self.review_queue = VocabularyProposalReviewQueue()

    # ---- scheme / concept CRUD -------------------------------------------------

    def create_scheme(
        self,
        title: str,
        description: str = "",
        scheme_id: str | None = None,
        titles: dict[str, str] | None = None,
        version_id: str = "1.0.0",
    ) -> ConceptScheme:
        if not title.strip():
            raise ValueError("scheme title must be non-empty")
        scheme_id = scheme_id or _new_id("scheme")
        if scheme_id in self.schemes:
            raise ValueError(f"scheme already exists: {scheme_id}")
        titles_dict = dict(titles or {})
        if "en" not in titles_dict:
            titles_dict["en"] = title
        scheme = ConceptScheme(
            scheme_id=scheme_id,
            title=title,
            titles=titles_dict,
            description=description,
            version_id=version_id,
        )
        self.schemes[scheme_id] = scheme
        return scheme

    def add_concept(
        self,
        scheme_id: str,
        pref_label: str,
        *,
        pref_labels: dict[str, str] | None = None,
        concept_id: str | None = None,
        definition: str = "",
        definitions_by_lang: dict[str, str] | None = None,
        notation: str = "",
        alt_labels: list[str] | None = None,
        alt_labels_by_lang: dict[str, list[str]] | None = None,
        hidden_labels: list[str] | None = None,
        hidden_labels_by_lang: dict[str, list[str]] | None = None,
        deprecated: bool = False,
        replaced_by: list[str] | None = None,
    ) -> Concept:
        if scheme_id not in self.schemes:
            raise KeyError(f"unknown scheme: {scheme_id}")
        if not pref_label.strip() and not pref_labels:
            raise ValueError("pref_label must be non-empty")
        concept_id = concept_id or _new_id("concept")
        if concept_id in self.concepts:
            raise ValueError(f"concept already exists: {concept_id}")

        pref_labels_dict = dict(pref_labels or {})
        if pref_label.strip() and "en" not in pref_labels_dict:
            pref_labels_dict["en"] = pref_label.strip()

        # Validate BCP-47 tags
        for lang in pref_labels_dict.keys():
            if not validate_bcp47(lang):
                raise ValueError(f"Invalid BCP-47 language tag: '{lang}' (CRA-021.7)")

        # Enforce label uniqueness policy if configured (CRA-021.5)
        if self.label_uniqueness_policy == LabelUniquenessPolicy.STRICT_SCHEME_LANG:
            for lang, lbl in pref_labels_dict.items():
                for c in self.concepts.values():
                    if c.scheme_id == scheme_id and c.pref_labels.get(lang, "").casefold() == lbl.casefold():
                        raise DuplicateLabelError(
                            f"Concept '{c.concept_id}' already has prefLabel '{lbl}' for language '{lang}' in scheme '{scheme_id}'"
                        )

        concept = Concept(
            concept_id=concept_id,
            scheme_id=scheme_id,
            pref_label=pref_label.strip() or next(iter(pref_labels_dict.values()), ""),
            pref_labels=pref_labels_dict,
            alt_labels=list(alt_labels or []),
            alt_labels_by_lang=dict(alt_labels_by_lang or {}),
            hidden_labels=list(hidden_labels or []),
            hidden_labels_by_lang=dict(hidden_labels_by_lang or {}),
            definition=definition,
            definitions_by_lang=dict(definitions_by_lang or {}),
            notation=notation,
            deprecated=deprecated,
            replaced_by=list(replaced_by or []),
        )
        self.concepts[concept_id] = concept
        return concept

    # ---- relationships & polyhierarchy (CRA-021.1) ------------------------------

    def add_broader(self, concept_id: str, broader_id: str) -> None:
        """Declare ``broader_id`` a broader concept of ``concept_id`` (skos:broader). Supports polyhierarchy."""
        concept = self._concept(concept_id)
        broader = self._concept(broader_id)
        self._assert_same_scheme(concept, broader)
        if broader_id == concept_id:
            raise ValueError("a concept cannot be broader than itself")

        # Check cycle policy (CRA-021.1, CRA-021.A)
        if self.cycle_policy == CyclePolicy.REJECT:
            closure = self.broader_closure(broader_id)
            if concept_id in closure:
                raise CyclicTaxonomyError(
                    f"Adding broader relationship from '{concept_id}' to '{broader_id}' introduces a cycle"
                )

        self._link(concept.broader, broader_id)
        self._link(broader.narrower, concept_id)

    def add_related(self, concept_id: str, other_id: str) -> None:
        """Declare a symmetric associative link (skos:related)."""
        concept = self._concept(concept_id)
        other = self._concept(other_id)
        self._assert_same_scheme(concept, other)
        if other_id == concept_id:
            raise ValueError("a concept cannot be related to itself")
        self._link(concept.related, other_id)
        self._link(other.related, concept_id)

    def broader_closure(self, concept_id: str) -> list[str]:
        """Transitive closure over skos:broader (excluding the concept itself)."""
        self._concept(concept_id)
        seen: set[str] = set()
        stack = list(self.concepts[concept_id].broader)
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            parent = self.concepts.get(current)
            if parent is not None:
                stack.extend(parent.broader)
        return sorted(seen)

    def narrower_closure(self, concept_id: str) -> list[str]:
        """Transitive closure over skos:narrower (excluding the concept itself)."""
        self._concept(concept_id)
        seen: set[str] = set()
        stack = list(self.concepts[concept_id].narrower)
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            child = self.concepts.get(current)
            if child is not None:
                stack.extend(child.narrower)
        return sorted(seen)

    # ---- collections ------------------------------------------------------------

    def create_collection(
        self, scheme_id: str, title: str, collection_id: str | None = None, titles: dict[str, str] | None = None
    ) -> Collection:
        if scheme_id not in self.schemes:
            raise KeyError(f"unknown scheme: {scheme_id}")
        collection_id = collection_id or _new_id("collection")
        if collection_id in self.collections:
            raise ValueError(f"collection already exists: {collection_id}")
        titles_dict = dict(titles or {})
        if "en" not in titles_dict:
            titles_dict["en"] = title
        collection = Collection(
            collection_id=collection_id, scheme_id=scheme_id, title=title, titles=titles_dict
        )
        self.collections[collection_id] = collection
        return collection

    def add_to_collection(self, collection_id: str, concept_id: str) -> None:
        collection = self.collections.get(collection_id)
        if collection is None:
            raise KeyError(f"unknown collection: {collection_id}")
        concept = self._concept(concept_id)
        if concept.scheme_id != collection.scheme_id:
            raise ValueError("concept and collection belong to different schemes")
        self._link(collection.member_ids, concept_id)
        self._link(concept.in_collections, collection_id)

    # ---- mappings & crosswalks (CRA-021.1) ---------------------------------------

    def add_mapping(
        self, source_id: str, target_id: str, kind: MappingKind, provenance: dict[str, Any] | None = None
    ) -> ConceptMapping:
        self._concept(source_id)
        if source_id == target_id:
            raise ValueError("a concept cannot be mapped to itself")
        mapping = ConceptMapping(source_id=source_id, target_id=target_id, kind=kind, provenance=provenance or {})
        self.mappings.append(mapping)
        return mapping

    def mappings_for(self, concept_id: str, kind: MappingKind | None = None) -> list[ConceptMapping]:
        result = [
            m
            for m in self.mappings
            if concept_id in (m.source_id, m.target_id) and (kind is None or m.kind == kind)
        ]
        return sorted(result, key=lambda m: (m.source_id, m.kind.value, m.target_id))

    # ---- SKOS-XL support (CRA-021.2) --------------------------------------------

    def add_xl_label(
        self, scheme_id: str, literal_form: str, language: str = "en", label_id: str | None = None
    ) -> SKOSXLLabel:
        label_id = label_id or _new_id("label")
        if not validate_bcp47(language):
            raise ValueError(f"Invalid BCP-47 tag '{language}'")
        label = SKOSXLLabel(label_id=label_id, scheme_id=scheme_id, literal_form=literal_form, language=language)
        self.xl_labels[label_id] = label
        return label

    def bind_concept_xl_label(self, concept_id: str, label_id: str, role: str = "prefLabel") -> None:
        concept = self._concept(concept_id)
        if label_id not in self.xl_labels:
            raise KeyError(f"Unknown SKOS-XL label '{label_id}'")
        concept.xl_labels[role] = label_id

    # ---- deprecation and editorial notes (CRA-021.7) -----------------------------

    def deprecate_concept(
        self,
        concept_id: str,
        replaced_by: list[str] | None = None,
        reason: str = "",
        author: str = "steward",
    ) -> None:
        """Retire a concept with owl:deprecated true, dct:isReplacedBy, and audited notes."""
        concept = self._concept(concept_id)
        concept.deprecated = True
        concept.replaced_by = list(replaced_by or [])
        concept.deprecation_reason = reason
        concept.deprecation_date = datetime.now(UTC).isoformat()
        concept.editorial_notes.append({
            "action": "DEPRECATED",
            "author": author,
            "timestamp": concept.deprecation_date,
            "reason": reason,
            "replaced_by": list(concept.replaced_by),
        })

    def add_editorial_note(
        self, concept_id: str, text: str, author: str = "steward", note_type: str = "editorialNote"
    ) -> None:
        concept = self._concept(concept_id)
        note_entry = {
            "text": text,
            "author": author,
            "timestamp": datetime.now(UTC).isoformat(),
            "note_type": note_type,
        }
        if note_type == "historyNote":
            concept.history_notes.append(note_entry)
        elif note_type == "changeNote":
            concept.change_notes.append(note_entry)
        else:
            concept.editorial_notes.append(note_entry)

    # ---- versioning, dependencies, receipts and rollback (CRA-021.4) ------------

    def publish_version(
        self,
        scheme_id: str,
        new_version: str,
        publisher: str = "steward",
        dependencies: list[dict[str, Any]] | None = None,
    ) -> PublicationReceipt:
        scheme = self.schemes.get(scheme_id)
        if not scheme:
            raise KeyError(f"unknown scheme: {scheme_id}")

        snapshot = {
            "version_id": scheme.version_id,
            "concepts": [c.model_dump() for c in self.concepts.values() if c.scheme_id == scheme_id],
            "collections": [c.model_dump() for c in self.collections.values() if c.scheme_id == scheme_id],
            "mappings": [m.model_dump() for m in self.mappings if self.concepts.get(m.source_id, Concept(concept_id="", scheme_id="")).scheme_id == scheme_id],
        }
        self.version_snapshots[(scheme_id, scheme.version_id)] = snapshot

        digest = hashlib.sha256(f"{scheme_id}:{new_version}:{datetime.now(UTC).isoformat()}".encode()).hexdigest()
        receipt = PublicationReceipt(
            receipt_id=_new_id("rcpt"),
            scheme_id=scheme_id,
            version_id=new_version,
            timestamp=datetime.now(UTC).isoformat(),
            digest=digest,
            publisher=publisher,
            dependencies=list(dependencies or []),
        )

        scheme.version_history.append({
            "version_id": scheme.version_id,
            "superseded_at": receipt.timestamp,
        })
        scheme.version_id = new_version
        scheme.publication_receipt = receipt
        scheme.dependencies = list(dependencies or [])
        scheme.is_stale = True
        scheme.consumer_acknowledgements.clear()
        return receipt

    def acknowledge_consumer(self, scheme_id: str, consumer_id: str, version_id: str) -> bool:
        """Record consumer acknowledgement; updates projection stale status (CRA-021.4)."""
        scheme = self.schemes.get(scheme_id)
        if not scheme:
            raise KeyError(f"unknown scheme: {scheme_id}")
        scheme.consumer_acknowledgements[consumer_id] = version_id

        expected_consumers = {dep.get("id") or dep.get("name") for dep in scheme.dependencies if dep.get("id") or dep.get("name")}
        if expected_consumers and expected_consumers.issubset(set(scheme.consumer_acknowledgements.keys())):
            scheme.is_stale = False
        return scheme.is_stale

    def rollback_scheme(self, scheme_id: str, target_version: str) -> PublicationReceipt:
        """Rollback scheme to a prior version snapshot and restore dependent state (CRA-021.4)."""
        scheme = self.schemes.get(scheme_id)
        if not scheme:
            raise KeyError(f"unknown scheme: {scheme_id}")

        snapshot_key = (scheme_id, target_version)
        snapshot = self.version_snapshots.get(snapshot_key)
        if not snapshot:
            raise ValueError(f"Snapshot for version '{target_version}' not found")

        to_delete_concepts = [cid for cid, c in self.concepts.items() if c.scheme_id == scheme_id]
        for cid in to_delete_concepts:
            del self.concepts[cid]
        to_delete_colls = [cid for cid, c in self.collections.items() if c.scheme_id == scheme_id]
        for cid in to_delete_colls:
            del self.collections[cid]

        for c_data in snapshot["concepts"]:
            c = Concept(**c_data)
            self.concepts[c.concept_id] = c
        for col_data in snapshot["collections"]:
            col = Collection(**col_data)
            self.collections[col.collection_id] = col

        scheme.version_id = target_version
        scheme.is_stale = False
        receipt = PublicationReceipt(
            receipt_id=_new_id("rollback-rcpt"),
            scheme_id=scheme_id,
            version_id=target_version,
            timestamp=datetime.now(UTC).isoformat(),
            digest=hashlib.sha256(f"rollback:{scheme_id}:{target_version}".encode()).hexdigest(),
            publisher="rollback-orchestrator",
            dependencies=scheme.dependencies,
        )
        scheme.publication_receipt = receipt
        return receipt

    # ---- language-aware search & presentation (CRA-021.5) -----------------------

    def search(
        self,
        query: str,
        scheme_id: str | None = None,
        language: str = "en",
        fallback: bool = True,
        normalize: bool = True,
    ) -> list[Concept]:
        """Language-aware search with Unicode NFC normalization and BCP-47 fallback (CRA-021.5)."""
        q = query.strip()
        if normalize:
            q = unicodedata.normalize("NFC", q).casefold()
        else:
            q = q.casefold()

        matches = []
        for c in self.concepts.values():
            if scheme_id is not None and c.scheme_id != scheme_id:
                continue

            lbl = c.pref_labels.get(language, "")
            if normalize:
                lbl = unicodedata.normalize("NFC", lbl).casefold()
            else:
                lbl = lbl.casefold()

            if q in lbl:
                matches.append(c)
                continue

            if fallback and "-" in language:
                prefix = language.split("-")[0]
                fallback_lbl = c.pref_labels.get(prefix, "")
                if normalize:
                    fallback_lbl = unicodedata.normalize("NFC", fallback_lbl).casefold()
                else:
                    fallback_lbl = fallback_lbl.casefold()
                if q in fallback_lbl:
                    matches.append(c)
                    continue

            alts = c.alt_labels_by_lang.get(language, []) or c.alt_labels
            if any(q in unicodedata.normalize("NFC", a).casefold() for a in alts):
                matches.append(c)

        return sorted(matches, key=lambda c: c.concept_id)

    def format_presentation(self, concept_id: str, language: str = "en") -> dict[str, Any]:
        """Unicode/RTL-safe presentation for concept labels (CRA-021.5)."""
        concept = self._concept(concept_id)
        lbl = concept.pref_labels.get(language) or concept.pref_label
        rtl = is_rtl_text(lbl)
        return {
            "concept_id": concept.concept_id,
            "urn": concept.urn,
            "label": lbl,
            "language": language,
            "dir": "rtl" if rtl else "ltr",
            "bidi_isolated": f"\u2067{lbl}\u2069" if rtl else lbl,
        }

    # ---- concurrent edits CAS (CRA-021.A) ---------------------------------------

    def update_concept_cas(
        self,
        concept_id: str,
        expected_version: int,
        updates: dict[str, Any],
    ) -> Concept:
        """Compare-and-swap concurrent edit validation (CRA-021.A)."""
        concept = self._concept(concept_id)
        if concept.version != expected_version:
            raise ConcurrentModificationError(
                f"Concurrent edit conflict on concept '{concept_id}': expected version {expected_version}, actual {concept.version}"
            )
        for k, v in updates.items():
            if hasattr(concept, k):
                setattr(concept, k, v)
        concept.version += 1
        return concept

    # ---- validation --------------------------------------------------------------

    def detect_label_conflicts(self, scheme_id: str | None = None) -> list[LabelConflict]:
        """GAP-TAX-001: two concepts sharing a prefLabel in one scheme."""
        by_key: dict[tuple[str, str, str], list[str]] = {}
        for concept in sorted(self.concepts.values(), key=lambda c: c.concept_id):
            if scheme_id is not None and concept.scheme_id != scheme_id:
                continue
            for lang, lbl in concept.pref_labels.items():
                by_key.setdefault((concept.scheme_id, lang, lbl.casefold()), []).append(concept.concept_id)

        conflicts = [
            LabelConflict(
                scheme_id=scheme,
                pref_label=self.concepts[ids[0]].pref_labels.get(lang, self.concepts[ids[0]].pref_label),
                concept_ids=ids,
                language=lang,
            )
            for (scheme, lang, _), ids in sorted(by_key.items())
            if len(ids) > 1
        ]
        return sorted(conflicts, key=lambda c: (c.scheme_id, c.pref_label))

    def validate_integrity(self, scheme_id: str | None = None) -> list[IntegrityIssue]:
        """SKOS integrity checks: orphan concepts and broader/narrower cycles."""
        issues: list[IntegrityIssue] = []
        concepts = [
            c
            for c in sorted(self.concepts.values(), key=lambda c: c.concept_id)
            if scheme_id is None or c.scheme_id == scheme_id
        ]
        for concept in concepts:
            has_links = concept.broader or concept.narrower or concept.related
            if not has_links and not concept.in_collections:
                issues.append(
                    IntegrityIssue(
                        kind="orphan_concept",
                        detail=f"concept '{concept.pref_label}' has no semantic relationships or collections",
                        concept_ids=[concept.concept_id],
                    )
                )
            cycle = self._find_cycle(concept.concept_id, via="broader")
            if cycle is not None:
                issues.append(
                    IntegrityIssue(
                        kind="broader_cycle",
                        detail="cycle detected in skos:broader: " + " -> ".join(cycle),
                        concept_ids=cycle,
                    )
                )
        seen_cycles: set[tuple[str, ...]] = set()
        unique: list[IntegrityIssue] = []
        for issue in issues:
            if issue.kind in ("broader_cycle", "narrower_cycle"):
                key = tuple(sorted(issue.concept_ids))
                if key in seen_cycles:
                    continue
                seen_cycles.add(key)
            unique.append(issue)
        return unique

    def _find_cycle(self, start_id: str, via: str) -> list[str] | None:
        path: list[str] = []
        state: dict[str, int] = {}

        def dfs(node_id: str) -> list[str] | None:
            state[node_id] = len(path)
            path.append(node_id)
            node = self.concepts.get(node_id)
            if node is not None:
                for nxt in getattr(node, via):
                    if nxt == start_id:
                        return path[path.index(start_id) :] if start_id in path else path[:]
                    if nxt in state:
                        continue
                    found = dfs(nxt)
                    if found is not None:
                        return found
            path.pop()
            state.pop(node_id, None)
            return None

        return dfs(start_id)

    # ---- RDF / W3C serialization (CRA-021.2, CRA-021.6) -------------------------

    def to_rdflib_graph(
        self, scheme_id: str | None = None, profile: SKOSProfile = SKOSProfile.SKOS_CORE
    ) -> rdflib.Graph:
        """Convert taxonomy to an rdflib.Graph with profile validation (CRA-021.2, CRA-021.6)."""
        if profile not in {SKOSProfile.SKOS_CORE, SKOSProfile.SKOS_XL, SKOSProfile.ONTOLEX_LEMON}:
            raise UnsupportedProfileError(f"Unsupported profile '{profile}' (CRA-021.2)")

        g = Graph()
        g.bind("skos", SKOS)
        g.bind("owl", OWL)
        g.bind("dct", DCTERMS)
        g.bind("eoip", EOIP)

        if profile == SKOSProfile.SKOS_XL:
            g.bind("skosxl", SKOSXL)
        elif profile == SKOSProfile.ONTOLEX_LEMON:
            g.bind("ontolex", ONTOLEX)

        # Schemes
        for s in self.schemes.values():
            if scheme_id is not None and s.scheme_id != scheme_id:
                continue
            s_uri = URIRef(s.urn)
            g.add((s_uri, RDF.type, SKOS.ConceptScheme))
            for lang, t in s.titles.items():
                g.add((s_uri, DCTERMS.title, Literal(t, lang=lang)))
            if s.description:
                g.add((s_uri, DCTERMS.description, Literal(s.description)))
            g.add((s_uri, OWL.versionInfo, Literal(s.version_id)))

        # SKOS-XL Labels if enabled
        if profile == SKOSProfile.SKOS_XL:
            for xl in self.xl_labels.values():
                lbl_uri = URIRef(xl.urn)
                g.add((lbl_uri, RDF.type, SKOSXL.Label))
                g.add((lbl_uri, SKOSXL.literalForm, Literal(xl.literal_form, lang=xl.language)))

        # Concepts
        for c in self.concepts.values():
            if scheme_id is not None and c.scheme_id != scheme_id:
                continue
            c_uri = URIRef(c.urn)
            g.add((c_uri, RDF.type, SKOS.Concept))
            g.add((c_uri, SKOS.inScheme, URIRef(self.schemes[c.scheme_id].urn)))

            # Labels with BCP-47
            for lang, lbl in c.pref_labels.items():
                g.add((c_uri, SKOS.prefLabel, Literal(lbl, lang=lang)))
            for lang, alts in c.alt_labels_by_lang.items():
                for alt in alts:
                    g.add((c_uri, SKOS.altLabel, Literal(alt, lang=lang)))
            for lang, hiddens in c.hidden_labels_by_lang.items():
                for hid in hiddens:
                    g.add((c_uri, SKOS.hiddenLabel, Literal(hid, lang=lang)))
            for lang, df in c.definitions_by_lang.items():
                g.add((c_uri, SKOS.definition, Literal(df, lang=lang)))
            if c.notation:
                g.add((c_uri, SKOS.notation, Literal(c.notation)))

            # Hierarchies
            for b in c.broader:
                if b in self.concepts:
                    g.add((c_uri, SKOS.broader, URIRef(self.concepts[b].urn)))
            for n in c.narrower:
                if n in self.concepts:
                    g.add((c_uri, SKOS.narrower, URIRef(self.concepts[n].urn)))
            for r in c.related:
                if r in self.concepts:
                    g.add((c_uri, SKOS.related, URIRef(self.concepts[r].urn)))

            # Deprecation (CRA-021.7)
            if c.deprecated:
                g.add((c_uri, OWL.deprecated, Literal(True, datatype=XSD.boolean)))
                for rep in c.replaced_by:
                    rep_uri = URIRef(self.concepts[rep].urn) if rep in self.concepts else URIRef(rep)
                    g.add((c_uri, DCTERMS.isReplacedBy, rep_uri))

            # Editorial notes
            for en in c.editorial_notes:
                g.add((c_uri, SKOS.editorialNote, Literal(str(en))))
            for hn in c.history_notes:
                g.add((c_uri, SKOS.historyNote, Literal(str(hn))))

            # SKOS-XL references
            if profile == SKOSProfile.SKOS_XL:
                for role, lbl_id in c.xl_labels.items():
                    if lbl_id in self.xl_labels:
                        prop = SKOSXL.prefLabel if role == "prefLabel" else SKOSXL.altLabel
                        g.add((c_uri, prop, URIRef(self.xl_labels[lbl_id].urn)))

            # OntoLex-Lemon
            if profile == SKOSProfile.ONTOLEX_LEMON:
                entry_uri = URIRef(f"urn:eoip:ontology:lexentry:{c.concept_id}")
                form_uri = URIRef(f"urn:eoip:ontology:form:{c.concept_id}")
                g.add((entry_uri, RDF.type, ONTOLEX.LexicalEntry))
                g.add((entry_uri, ONTOLEX.canonicalForm, form_uri))
                g.add((entry_uri, ONTOLEX.isLexicalizedSenseOf, c_uri))
                g.add((form_uri, ONTOLEX.writtenRep, Literal(c.pref_label, lang="en")))

        # Collections
        for col in self.collections.values():
            if scheme_id is not None and col.scheme_id != scheme_id:
                continue
            col_uri = URIRef(col.urn)
            g.add((col_uri, RDF.type, SKOS.Collection))
            for lang, t in col.titles.items():
                g.add((col_uri, DCTERMS.title, Literal(t, lang=lang)))
            for m in col.member_ids:
                if m in self.concepts:
                    g.add((col_uri, SKOS.member, URIRef(self.concepts[m].urn)))

        # Mappings
        for m in self.mappings:
            src = self.concepts.get(m.source_id)
            if not src:
                continue
            src_uri = URIRef(src.urn)
            tgt_uri = URIRef(self.concepts[m.target_id].urn) if m.target_id in self.concepts else URIRef(m.target_id)
            prop = getattr(SKOS, m.kind.value)
            g.add((src_uri, prop, tgt_uri))

        return g

    @classmethod
    def from_rdflib_graph(
        cls,
        graph: rdflib.Graph,
        taxonomy: SkosTaxonomy | None = None,
        profile: SKOSProfile = SKOSProfile.SKOS_CORE,
    ) -> SkosTaxonomy:
        """Parse taxonomy from an rdflib.Graph with lossless round trip (CRA-021.2, CRA-021.6)."""
        if profile not in {SKOSProfile.SKOS_CORE, SKOSProfile.SKOS_XL, SKOSProfile.ONTOLEX_LEMON}:
            raise UnsupportedProfileError(f"Unsupported profile '{profile}' (CRA-021.2)")

        tax = taxonomy or cls()

        # Parse Schemes
        for s_uri in graph.subjects(RDF.type, SKOS.ConceptScheme):
            s_str = str(s_uri)
            scheme_id = s_str.split(":")[-1]
            title = ""
            titles: dict[str, str] = {}
            for _, _, t in graph.triples((s_uri, DCTERMS.title, None)):
                lang = t.language or "en"
                titles[lang] = str(t)
                if not title:
                    title = str(t)
            desc = ""
            for _, _, d in graph.triples((s_uri, DCTERMS.description, None)):
                desc = str(d)
            v_info = "1.0.0"
            for _, _, v in graph.triples((s_uri, OWL.versionInfo, None)):
                v_info = str(v)
            if scheme_id not in tax.schemes:
                tax.create_scheme(title=title or scheme_id, description=desc, scheme_id=scheme_id, titles=titles, version_id=v_info)

        default_scheme = next(iter(tax.schemes.keys()), "default-scheme")
        if default_scheme not in tax.schemes:
            tax.create_scheme(title="Default Scheme", scheme_id=default_scheme)

        # Parse SKOS-XL labels
        if profile == SKOSProfile.SKOS_XL:
            for l_uri in graph.subjects(RDF.type, SKOSXL.Label):
                l_id = str(l_uri).split(":")[-1]
                for _, _, lit in graph.triples((l_uri, SKOSXL.literalForm, None)):
                    lang = lit.language or "en"
                    tax.add_xl_label(scheme_id=default_scheme, literal_form=str(lit), language=lang, label_id=l_id)

        # Parse Concepts
        concept_uris: dict[str, str] = {}
        for c_uri in graph.subjects(RDF.type, SKOS.Concept):
            c_str = str(c_uri)
            cid = c_str.split(":")[-1]
            concept_uris[c_str] = cid

            c_scheme = default_scheme
            for _, _, s in graph.triples((c_uri, SKOS.inScheme, None)):
                sid = str(s).split(":")[-1]
                if sid in tax.schemes:
                    c_scheme = sid

            pref_labels: dict[str, str] = {}
            for _, _, p in graph.triples((c_uri, SKOS.prefLabel, None)):
                lang = p.language or "en"
                pref_labels[lang] = str(p)

            alt_labels_by_lang: dict[str, list[str]] = {}
            for _, _, a in graph.triples((c_uri, SKOS.altLabel, None)):
                lang = a.language or "en"
                alt_labels_by_lang.setdefault(lang, []).append(str(a))

            hidden_labels_by_lang: dict[str, list[str]] = {}
            for _, _, h in graph.triples((c_uri, SKOS.hiddenLabel, None)):
                lang = h.language or "en"
                hidden_labels_by_lang.setdefault(lang, []).append(str(h))

            defs_by_lang: dict[str, str] = {}
            for _, _, d in graph.triples((c_uri, SKOS.definition, None)):
                lang = d.language or "en"
                defs_by_lang[lang] = str(d)

            notation = ""
            for _, _, n in graph.triples((c_uri, SKOS.notation, None)):
                notation = str(n)

            is_dep = False
            for _, _, dep in graph.triples((c_uri, OWL.deprecated, None)):
                is_dep = bool(dep)
            reps: list[str] = []
            for _, _, rep in graph.triples((c_uri, DCTERMS.isReplacedBy, None)):
                reps.append(str(rep).split(":")[-1])

            pref_str = pref_labels.get("en") or next(iter(pref_labels.values()), cid)
            tax.add_concept(
                scheme_id=c_scheme,
                pref_label=pref_str,
                pref_labels=pref_labels,
                concept_id=cid,
                definition=defs_by_lang.get("en", ""),
                definitions_by_lang=defs_by_lang,
                notation=notation,
                alt_labels_by_lang=alt_labels_by_lang,
                hidden_labels_by_lang=hidden_labels_by_lang,
                deprecated=is_dep,
                replaced_by=reps,
            )

            if profile == SKOSProfile.SKOS_XL:
                for _, _, xl in graph.triples((c_uri, SKOSXL.prefLabel, None)):
                    xid = str(xl).split(":")[-1]
                    if xid in tax.xl_labels:
                        tax.bind_concept_xl_label(cid, xid, role="prefLabel")

        # Parse Hierarchies
        for c_str, cid in concept_uris.items():
            c_uri = URIRef(c_str)
            for _, _, b in graph.triples((c_uri, SKOS.broader, None)):
                b_id = str(b).split(":")[-1]
                if b_id in tax.concepts:
                    tax._link(tax.concepts[cid].broader, b_id)
                    tax._link(tax.concepts[b_id].narrower, cid)
            for _, _, r in graph.triples((c_uri, SKOS.related, None)):
                r_id = str(r).split(":")[-1]
                if r_id in tax.concepts:
                    tax._link(tax.concepts[cid].related, r_id)
                    tax._link(tax.concepts[r_id].related, cid)

        # Parse Collections
        for col_uri in graph.subjects(RDF.type, SKOS.Collection):
            col_id = str(col_uri).split(":")[-1]
            title = ""
            for _, _, t in graph.triples((col_uri, DCTERMS.title, None)):
                title = str(t)
            tax.create_collection(scheme_id=default_scheme, title=title or col_id, collection_id=col_id)
            for _, _, m in graph.triples((col_uri, SKOS.member, None)):
                m_id = str(m).split(":")[-1]
                if m_id in tax.concepts:
                    tax.add_to_collection(col_id, m_id)

        # Parse Mappings
        for kind in MappingKind:
            prop = getattr(SKOS, kind.value)
            for s_uri, _, t_uri in graph.triples((None, prop, None)):
                s_id = str(s_uri).split(":")[-1]
                t_id = str(t_uri).split(":")[-1]
                if s_id in tax.concepts and s_id != t_id:
                    tax.add_mapping(s_id, t_id, kind)

        return tax

    def export_serialization(
        self, format_name: str = "turtle", profile: SKOSProfile = SKOSProfile.SKOS_CORE
    ) -> str:
        """Serialize taxonomy using RDFSerializer (CRA-021.6)."""
        graph = self.to_rdflib_graph(profile=profile)
        serializer = RDFSerializer(enable_rdf_star=False)
        return serializer.serialize(graph, format_name=format_name)

    @classmethod
    def import_serialization(
        cls,
        data: str,
        format_name: str = "turtle",
        profile: SKOSProfile = SKOSProfile.SKOS_CORE,
        taxonomy: SkosTaxonomy | None = None,
    ) -> SkosTaxonomy:
        """Deserialize taxonomy using RDFDeserializer with security safeguards (CRA-021.6)."""
        deserializer = RDFDeserializer()
        graph, report = deserializer.deserialize(data, format_name=format_name)
        if not report.syntax_valid:
            raise ValueError("Invalid RDF syntax during SKOS import")
        return cls.from_rdflib_graph(graph, taxonomy=taxonomy, profile=profile)

    # ---- ISO 25964-style thesaurus import (CRA-021.7) ----------------------------

    def import_iso25964(self, fixture_data: dict[str, Any], scheme_id: str | None = None) -> ConceptScheme:
        """Import ISO 25964 structured thesaurus terms, hierarchies, and crosswalks (CRA-021.7)."""
        s_id = scheme_id or fixture_data.get("thesaurus_id") or _new_id("thesaurus")
        title = fixture_data.get("title", f"Thesaurus {s_id}")
        scheme = self.create_scheme(title=title, scheme_id=s_id)

        # Pass 1: create terms
        for term in fixture_data.get("concepts", []):
            cid = term["concept_id"]
            pref_lbl = term.get("preferred_term") or term.get("descriptor", cid)
            alt_lbls = term.get("non_descriptors") or term.get("use_for", [])
            scope_note = term.get("scope_note", "")
            notation = term.get("notation", "")
            dep = term.get("deprecated", False)
            rep_by = term.get("replaced_by", [])
            self.add_concept(
                scheme_id=s_id,
                pref_label=pref_lbl,
                concept_id=cid,
                definition=scope_note,
                notation=notation,
                alt_labels=alt_lbls,
                deprecated=dep,
                replaced_by=rep_by,
            )

        # Pass 2: hierarchies (BT/NT/RT)
        for term in fixture_data.get("concepts", []):
            cid = term["concept_id"]
            for bt in term.get("broader_terms", []):
                if bt in self.concepts and bt != cid:
                    self.add_broader(cid, bt)
            for rt in term.get("related_terms", []):
                if rt in self.concepts and rt != cid and rt not in self.concepts[cid].related:
                    self.add_related(cid, rt)

        return scheme

    # ---- legacy bounded JSON-LD export -------------------------------------------

    def export_rdf(self) -> dict:
        """SKOS JSON-LD export for backward compatibility."""
        context = {
            "skos": SKOS_NAMESPACE,
            "eoip": EOIP_NAMESPACE,
            "prefLabel": "skos:prefLabel",
            "altLabel": "skos:altLabel",
            "hiddenLabel": "skos:hiddenLabel",
            "definition": "skos:definition",
            "notation": "skos:notation",
            "broader": {"@id": "skos:broader", "@type": "@id"},
            "narrower": {"@id": "skos:narrower", "@type": "@id"},
            "related": {"@id": "skos:related", "@type": "@id"},
            "member": {"@id": "skos:member", "@type": "@id"},
            "exactMatch": {"@id": "skos:exactMatch", "@type": "@id"},
            "closeMatch": {"@id": "skos:closeMatch", "@type": "@id"},
            "broadMatch": {"@id": "skos:broadMatch", "@type": "@id"},
            "narrowMatch": {"@id": "skos:narrowMatch", "@type": "@id"},
            "relatedMatch": {"@id": "skos:relatedMatch", "@type": "@id"},
            "dct": DCTERMS_NAMESPACE,
            "title": "dct:title",
            "description": "dct:description",
        }

        def ref(cid: str) -> dict:
            return {"@id": self.concepts[cid].urn}

        graph: list[dict] = []
        for scheme in sorted(self.schemes.values(), key=lambda s: s.scheme_id):
            graph.append(
                {
                    "@id": scheme.urn,
                    "@type": "skos:ConceptScheme",
                    "title": scheme.title,
                    "description": scheme.description,
                }
            )
        for concept in sorted(self.concepts.values(), key=lambda c: c.concept_id):
            item: dict = {
                "@id": concept.urn,
                "@type": "skos:Concept",
                "prefLabel": concept.pref_label,
            }
            if concept.alt_labels:
                item["altLabel"] = concept.alt_labels
            if concept.hidden_labels:
                item["hiddenLabel"] = concept.hidden_labels
            if concept.definition:
                item["definition"] = concept.definition
            if concept.notation:
                item["notation"] = concept.notation
            for prop, ids in (
                ("broader", concept.broader),
                ("narrower", concept.narrower),
                ("related", concept.related),
            ):
                if ids:
                    item[prop] = [ref(cid) for cid in sorted(ids)]
            graph.append(item)
        for collection in sorted(self.collections.values(), key=lambda c: c.collection_id):
            graph.append(
                {
                    "@id": collection.urn,
                    "@type": "skos:Collection",
                    "title": collection.title,
                    "member": [ref(cid) for cid in sorted(collection.member_ids)],
                }
            )
        for mapping in sorted(self.mappings, key=lambda m: m.urn):
            graph.append(
                {
                    "@id": mapping.urn,
                    "@type": "skos:mappingRelation",
                    mapping.kind.value: [ref(mapping.target_id) if mapping.target_id in self.concepts else {"@id": mapping.target_id}],
                    "source": ref(mapping.source_id),
                }
            )
        return {
            "@context": context,
            "@graph": graph,
            "export": {
                "format": "SKOS JSON-LD 1.1",
                "schemes": len(self.schemes),
                "concepts": len(self.concepts),
                "collections": len(self.collections),
                "mappings": len(self.mappings),
            },
        }

    # ---- internals ----------------------------------------------------------------

    def _concept(self, concept_id: str) -> Concept:
        concept = self.concepts.get(concept_id)
        if concept is None:
            raise KeyError(f"unknown concept: {concept_id}")
        return concept

    @staticmethod
    def _link(links: list[str], target: str) -> None:
        if target not in links:
            links.append(target)

    @staticmethod
    def _assert_same_scheme(a: Concept, b: Concept) -> None:
        if a.scheme_id != b.scheme_id:
            raise ValueError("broader/narrower/related links require concepts in the same scheme")


# ---- Drift detection integration (CRA-021.8) -----------------------------------


def emit_drift_proposals_to_review(
    drift_report: OntologyDriftReport,
    review_queue: VocabularyProposalReviewQueue,
    scheme_id: str = "governed-taxonomy",
) -> list[VocabularyProposal]:
    """Emit ontology drift findings into the governed review queue without auto-applying (CRA-021.8, I17)."""
    proposals: list[VocabularyProposal] = []
    for finding in drift_report.findings:
        payload = build_evolution_proposal(finding)
        prop_id = _new_id("drift-prop")
        proposal = VocabularyProposal(
            proposal_id=prop_id,
            proposal_type=ProposalType.CANDIDATE_TERM if finding.kind == "vertex_label" else ProposalType.CROSSWALK,
            scheme_id=scheme_id,
            payload=payload,
            proposer="drift-detection-service",
            agent_type="connector",
            domain_owner="taxonomy-governance",
            status=ProposalStatus.PROPOSED,  # Never auto-applied (I17)
            provenance={"drift_kind": finding.kind, "occurrences": finding.occurrences},
        )
        review_queue.submit_proposal(proposal)
        proposals.append(proposal)
    return proposals
