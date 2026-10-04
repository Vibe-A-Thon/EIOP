"""SKOS-compatible taxonomy and thesaurus management.

Covers GAP-TAX-001 (SKOS taxonomy/thesaurus management) and GAP-STUDIO-005
(SKOS authoring for governance). Supports GAP-GOV-003 crosswalks via SKOS
mapping relationships (exactMatch, closeMatch, broadMatch, narrowMatch,
relatedMatch).

Deterministic only: no model or network calls.
"""

from __future__ import annotations

from enum import Enum
from itertools import count
from urllib.parse import quote
from uuid import uuid4

from eoip.ontology.rdf import EOIP_NAMESPACE
from pydantic import BaseModel, Field

SKOS_NAMESPACE = "http://www.w3.org/2004/02/skos/core#"


class MappingKind(str, Enum):
    EXACT = "exactMatch"
    CLOSE = "closeMatch"
    BROAD = "broadMatch"
    NARROW = "narrowMatch"
    RELATED = "relatedMatch"


class LabelConflict(BaseModel):
    """GAP-TAX-001 label conflict: two concepts share a prefLabel in one scheme."""

    scheme_id: str
    pref_label: str
    concept_ids: list[str]


class IntegrityIssue(BaseModel):
    """SKOS integrity issue detected by validate_integrity()."""

    kind: str  # "orphan_concept" | "broader_cycle" | "narrower_cycle"
    detail: str
    concept_ids: list[str] = Field(default_factory=list)


class Concept(BaseModel):
    """GAP-TAX-001 SKOS Concept."""

    concept_id: str
    scheme_id: str
    pref_label: str
    alt_labels: list[str] = Field(default_factory=list)
    hidden_labels: list[str] = Field(default_factory=list)
    definition: str = ""
    notation: str = ""
    broader: list[str] = Field(default_factory=list)
    narrower: list[str] = Field(default_factory=list)
    related: list[str] = Field(default_factory=list)
    in_collections: list[str] = Field(default_factory=list)

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:concept:{self.concept_id}"


class ConceptScheme(BaseModel):
    """GAP-TAX-001 SKOS ConceptScheme."""

    scheme_id: str
    title: str
    description: str = ""

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:scheme:{self.scheme_id}"


class Collection(BaseModel):
    """SKOS Collection (ConceptGroup / OrderedCollection simplified)."""

    collection_id: str
    scheme_id: str
    title: str
    member_ids: list[str] = Field(default_factory=list)

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:collection:{self.collection_id}"


class ConceptMapping(BaseModel):
    """GAP-GOV-003 crosswalk assertion between concepts (optionally across schemes)."""

    source_id: str
    target_id: str
    kind: MappingKind

    @property
    def urn(self) -> str:
        return f"urn:eoip:ontology:mapping:{self.source_id}:{self.kind.value}:{self.target_id}"


_id_counter = count(1)


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


class SkosTaxonomy:
    """GAP-TAX-001 in-memory SKOS taxonomy/thesaurus registry."""

    def __init__(self) -> None:
        self.schemes: dict[str, ConceptScheme] = {}
        self.concepts: dict[str, Concept] = {}
        self.collections: dict[str, Collection] = {}
        self.mappings: list[ConceptMapping] = []

    # ---- scheme / concept CRUD -------------------------------------------------

    def create_scheme(self, title: str, description: str = "", scheme_id: str | None = None) -> ConceptScheme:
        if not title.strip():
            raise ValueError("scheme title must be non-empty")
        scheme_id = scheme_id or _new_id("scheme")
        if scheme_id in self.schemes:
            raise ValueError(f"scheme already exists: {scheme_id}")
        scheme = ConceptScheme(scheme_id=scheme_id, title=title, description=description)
        self.schemes[scheme_id] = scheme
        return scheme

    def add_concept(
        self,
        scheme_id: str,
        pref_label: str,
        *,
        concept_id: str | None = None,
        definition: str = "",
        notation: str = "",
        alt_labels: list[str] | None = None,
        hidden_labels: list[str] | None = None,
    ) -> Concept:
        if scheme_id not in self.schemes:
            raise KeyError(f"unknown scheme: {scheme_id}")
        if not pref_label.strip():
            raise ValueError("pref_label must be non-empty")
        concept_id = concept_id or _new_id("concept")
        if concept_id in self.concepts:
            raise ValueError(f"concept already exists: {concept_id}")
        concept = Concept(
            concept_id=concept_id,
            scheme_id=scheme_id,
            pref_label=pref_label.strip(),
            alt_labels=list(alt_labels or []),
            hidden_labels=list(hidden_labels or []),
            definition=definition,
            notation=notation,
        )
        self.concepts[concept_id] = concept
        return concept

    # ---- relationships ----------------------------------------------------------

    def add_broader(self, concept_id: str, broader_id: str) -> None:
        """Declare ``broader_id`` a broader concept of ``concept_id`` (skos:broader)."""
        concept = self._concept(concept_id)
        broader = self._concept(broader_id)
        self._assert_same_scheme(concept, broader)
        if broader_id == concept_id:
            raise ValueError("a concept cannot be broader than itself")
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

    def create_collection(self, scheme_id: str, title: str, collection_id: str | None = None) -> Collection:
        if scheme_id not in self.schemes:
            raise KeyError(f"unknown scheme: {scheme_id}")
        collection_id = collection_id or _new_id("collection")
        if collection_id in self.collections:
            raise ValueError(f"collection already exists: {collection_id}")
        collection = Collection(collection_id=collection_id, scheme_id=scheme_id, title=title)
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

    # ---- mappings (GAP-GOV-003 crosswalks) ---------------------------------------

    def add_mapping(self, source_id: str, target_id: str, kind: MappingKind) -> ConceptMapping:
        self._concept(source_id)
        self._concept(target_id)
        if source_id == target_id:
            raise ValueError("a concept cannot be mapped to itself")
        mapping = ConceptMapping(source_id=source_id, target_id=target_id, kind=kind)
        self.mappings.append(mapping)
        return mapping

    def mappings_for(self, concept_id: str, kind: MappingKind | None = None) -> list[ConceptMapping]:
        result = [
            m
            for m in self.mappings
            if concept_id in (m.source_id, m.target_id) and (kind is None or m.kind == kind)
        ]
        return sorted(result, key=lambda m: (m.source_id, m.kind.value, m.target_id))

    # ---- validation --------------------------------------------------------------

    def detect_label_conflicts(self, scheme_id: str | None = None) -> list[LabelConflict]:
        """GAP-TAX-001: two concepts sharing a prefLabel in one scheme."""
        by_key: dict[tuple[str, str], list[str]] = {}
        for concept in sorted(self.concepts.values(), key=lambda c: c.concept_id):
            if scheme_id is not None and concept.scheme_id != scheme_id:
                continue
            by_key.setdefault((concept.scheme_id, concept.pref_label.casefold()), []).append(concept.concept_id)
        conflicts = [
            LabelConflict(
                scheme_id=scheme,
                pref_label=self.concepts[ids[0]].pref_label,
                concept_ids=ids,
            )
            for (scheme, _), ids in sorted(by_key.items())
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
        # dedupe cycle reports (each cycle reported once, from its smallest member)
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

    # ---- RDF export --------------------------------------------------------------

    def export_rdf(self) -> dict:
        """SKOS JSON-LD export, following the bounded JSON-LD patterns of ontology/rdf.py."""
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
            "dct": "http://purl.org/dc/terms/",
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
                    mapping.kind.value: [ref(mapping.target_id)],
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


def concept_qname(concept_id: str) -> str:
    """Stable external identifier: ``urn:eoip:ontology:concept:<id>``."""
    return f"urn:eoip:ontology:concept:{quote(str(concept_id), safe='')}"
