"""Enterprise keyword search with semantic facet aggregation.

Implements GAP-SEARCH-001 (search over graph entities with counts facets:
entity type, domain, owner, source system, trust state, freshness bucket,
project) and GAP-SEARCH-002 (every hit preserves graph identity — the
canonical vertex ID — plus provenance pointers to its evidence/source).

Deterministic only: a local keyword matcher scores vertices on graph text
fields; no LLM or embedding calls. Works against the GraphStore port, so the
production HugeGraph store and the in-memory test store behave identically.

Facet fields map onto ontology property keys:
- entity type  -> vertex label
- domain       -> `graph_domain` (WORK / CODE / KNOWLEDGE / IDENTITY / META / CICD / OPS)
- owner        -> `author_name` / `actor_id`, else Person at the other end of AUTHORED_BY
- source system-> `source_system`
- trust state  -> `trust_state` (defaults to "unverified")
- freshness    -> bucketed from `last_seen` / `modified_at` / `created_at`
- project      -> `repo_id` / `space_key` / `service_id`
"""

from __future__ import annotations

import re
from datetime import datetime
from time import time
from typing import Any

from pydantic import BaseModel, Field

from eoip.graph.store import GraphStore

#: Vertex property keys scanned by the keyword matcher, most specific first.
#: All keys are members of the ontology PROPERTY_KEYS manifest.
_TEXT_FIELDS = (
    "name",
    "display_name",
    "qualified_name",
    "issue_key",
    "mr_title",
    "commit_sha",
    "path",
    "service_id",
    "repo_id",
    "summary",
    "description",
    "content",
    "message",
)

#: Bucket boundaries in days for freshness facets (GAP-FRESH conventions).
_FRESH_BUCKETS = (
    ("fresh", 30.0),
    ("recent", 90.0),
    ("aging", 180.0),
    ("stale", float("inf")),
)

_TOKEN_RE = re.compile(r"[a-z0-9_]+")


class SearchHit(BaseModel):
    """One search result. GAP-SEARCH-002: identity + provenance preserved."""

    canonical_id: str  # stable graph identity, e.g. urn:eoip:<area>:<type>:<id>
    label: str  # graph entity type (vertex label)
    name: str
    score: float
    authority: str | None = None  # owner / responsible party
    trust_state: str = "unverified"
    freshness: str = "unknown"  # fresh | recent | aging | stale | unknown
    last_seen: str | None = None
    evidence: list[str] = Field(default_factory=list)  # provenance pointers
    matched_fields: list[str] = Field(default_factory=list)
    matched_terms: list[str] = Field(default_factory=list)
    why: str = ""  # human-readable "why this result"


class FacetBucket(BaseModel):
    value: str
    count: int


class SearchFacets(BaseModel):
    entity_type: list[FacetBucket] = Field(default_factory=list)
    domain: list[FacetBucket] = Field(default_factory=list)
    owner: list[FacetBucket] = Field(default_factory=list)
    source_system: list[FacetBucket] = Field(default_factory=list)
    trust_state: list[FacetBucket] = Field(default_factory=list)
    freshness: list[FacetBucket] = Field(default_factory=list)
    project: list[FacetBucket] = Field(default_factory=list)


class SearchRequest(BaseModel):
    query: str = ""
    entity_types: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    owners: list[str] = Field(default_factory=list)
    source_systems: list[str] = Field(default_factory=list)
    trust_states: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    freshness: list[str] = Field(default_factory=list)
    limit: int = Field(default=25, ge=1, le=500)


class SearchResponse(BaseModel):
    query: str
    total: int  # total hits before paging (limit applied to hits only)
    hits: list[SearchHit]
    facets: SearchFacets


def _tokens(text: str) -> list[str]:
    tokens = _TOKEN_RE.findall(text.lower())
    expanded: list[str] = []
    for token in tokens:
        expanded.append(token)
        if "_" in token:
            expanded.extend(part for part in token.split("_") if part)
    return expanded


def _display_name(vertex: dict) -> str:
    props = vertex["properties"]
    return (
        props.get("name")
        or props.get("display_name")
        or props.get("mr_title")
        or props.get("qualified_name")
        or props.get("issue_key")
        or props.get("commit_sha")
        or props.get("path")
        or vertex["label"]
    )


def _iso_age_days(iso_value: Any, now_days: float) -> float | None:
    if not iso_value or not isinstance(iso_value, str):
        return None
    try:
        parsed = datetime.fromisoformat(iso_value.replace("Z", "+00:00"))
        return now_days - parsed.timestamp() / 86400.0
    except (ValueError, OSError, OverflowError):
        return None


def _freshness_bucket(vertex: dict, now_days: float) -> tuple[str, str | None]:
    props = vertex["properties"]
    last_seen = (
        props.get("last_seen")
        or props.get("modified_at")
        or props.get("created_at")
    )
    age = _iso_age_days(last_seen, now_days)
    if age is None:
        return "unknown", last_seen
    for bucket, ceiling in _FRESH_BUCKETS:
        if age < ceiling:
            return bucket, last_seen
    return "stale", last_seen


def _first_prop(props: dict, *keys: str) -> str | None:
    for key in keys:
        value = props.get(key)
        if value:
            return str(value)
    return None


def _match_vertex(
    vertex: dict, terms: list[str]
) -> tuple[float, list[str], list[str]] | None:
    """Score a vertex against query terms; return (score, fields, terms) or None."""
    props = vertex["properties"]
    matched_fields: list[str] = []
    matched_terms: list[str] = []
    score = 0.0
    for field in _TEXT_FIELDS:
        raw = props.get(field)
        if not raw or not isinstance(raw, str):
            continue
        field_tokens = set(_tokens(raw))
        if not field_tokens:
            continue
        field_hits = [t for t in terms if t in field_tokens]
        if field_hits:
            # Title/name matches weigh more than body matches.
            weight = (
                3.0
                if field in ("name", "display_name", "mr_title", "qualified_name", "issue_key")
                else 2.0
                if field in ("summary", "path")
                else 1.0
            )
            score += weight * len(field_hits)
            matched_fields.append(field)
            matched_terms.extend(t for t in field_hits if t not in matched_terms)
    if score <= 0.0:
        return None
    return score, matched_fields, matched_terms


class FacetedSearch:
    """Keyword + filter search over graph vertices with facet aggregation."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def search(self, request: SearchRequest, *, now: float | None = None) -> SearchResponse:
        now_days = time() / 86400.0 if now is None else now
        terms = _tokens(request.query)

        candidates = self._store.find_vertices(limit=50_000)
        hits: list[SearchHit] = []
        facet_source: dict[str, list[str]] = {
            key: []
            for key in (
                "entity_type",
                "domain",
                "owner",
                "source_system",
                "trust_state",
                "freshness",
                "project",
            )
        }

        for vertex in candidates:
            props = vertex["properties"]
            freshness, last_seen = _freshness_bucket(vertex, now_days)
            facet_values = {
                "entity_type": vertex["label"],
                "domain": str(props.get("graph_domain") or "unclassified"),
                "owner": self._owner_of(vertex) or "unassigned",
                "source_system": str(props.get("source_system") or "unknown"),
                "trust_state": str(props.get("trust_state") or "unverified"),
                "freshness": freshness,
                "project": _first_prop(props, "repo_id", "space_key", "service_id") or "none",
            }
            if not self._passes_filters(request, facet_values):
                continue
            if terms:
                match = _match_vertex(vertex, terms)
                if match is None:
                    continue
                score, matched_fields, matched_terms = match
            else:
                score, matched_fields, matched_terms = 0.0, [], []
            for key, value in facet_values.items():
                facet_source[key].append(value)
            hits.append(
                SearchHit(
                    canonical_id=vertex["canonical_id"],
                    label=vertex["label"],
                    name=_display_name(vertex),
                    score=round(score, 3),
                    authority=facet_values["owner"] if facet_values["owner"] != "unassigned" else None,
                    trust_state=facet_values["trust_state"],
                    freshness=freshness,
                    last_seen=last_seen,
                    evidence=self._evidence_pointers(vertex),
                    matched_fields=matched_fields,
                    matched_terms=matched_terms,
                    why=self._why(vertex, matched_fields, matched_terms, score),
                )
            )

        hits.sort(key=lambda h: (-h.score, h.canonical_id))
        total = len(hits)
        return SearchResponse(
            query=request.query,
            total=total,
            hits=hits[: request.limit],
            facets=SearchFacets(
                **{key: _bucketize(values) for key, values in facet_source.items()}
            ),
        )

    def _owner_of(self, vertex: dict) -> str | None:
        props = vertex["properties"]
        direct = _first_prop(props, "author_name", "actor_id")
        if direct:
            return direct
        for edge in self._store.edges_from(vertex["vid"], labels=["AUTHORED_BY"], limit=5):
            person = self._store.get_vertex_by_canonical_id(edge["in_cid"])
            if person is not None:
                return _first_prop(person["properties"], "display_name", "name")
        return None

    def _evidence_pointers(self, vertex: dict, limit: int = 10) -> list[str]:
        """Provenance pointers: source refs carried by edges touching the vertex."""
        refs: list[str] = []
        for edge in self._store.edges_from(vertex["vid"], limit=limit) + self._store.edges_to(
            vertex["vid"], limit=limit
        ):
            props = edge["properties"]
            for key in ("source_ref", "evidence_key", "source_event_id"):
                value = props.get(key)
                if value and value not in refs:
                    refs.append(str(value))
            if len(refs) >= limit:
                break
        return refs

    @staticmethod
    def _passes_filters(request: SearchRequest, values: dict[str, str]) -> bool:
        checks = (
            ("entity_types", "entity_type"),
            ("domains", "domain"),
            ("owners", "owner"),
            ("source_systems", "source_system"),
            ("trust_states", "trust_state"),
            ("projects", "project"),
            ("freshness", "freshness"),
        )
        for attr, key in checks:
            selected = getattr(request, attr)
            if selected and values[key] not in selected:
                return False
        return True

    @staticmethod
    def _why(vertex: dict, fields: list[str], terms: list[str], score: float) -> str:
        if not terms:
            return (
                f"Matched by filters only (entity type {vertex['label']}); "
                "no keyword terms supplied."
            )
        return (
            f"Matched terms [{', '.join(terms)}] in fields [{', '.join(fields)}] "
            f"of {vertex['label']} (score {score:.1f})."
        )


def _bucketize(values: list[str]) -> list[FacetBucket]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [FacetBucket(value=value, count=count) for value, count in ordered]


def search(
    store: GraphStore, request: SearchRequest, *, now: float | None = None
) -> SearchResponse:
    """Convenience one-shot faceted search (GAP-SEARCH-001)."""
    return FacetedSearch(store).search(request, now=now)
