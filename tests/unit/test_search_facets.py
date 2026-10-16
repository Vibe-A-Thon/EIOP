"""Unit tests for faceted enterprise search (GAP-SEARCH-001 / GAP-SEARCH-002)."""

from __future__ import annotations

import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.search import FacetedSearch, SearchRequest, search

NOW_DAYS = 20_000.0  # fixed epoch-days clock for deterministic freshness buckets


@pytest.fixture
def store() -> MemoryGraphStore:
    s = MemoryGraphStore()
    alice = s.upsert_vertex(
        "Person",
        {
            "canonical_id": "urn:eoip:identity:person:alice",
            "display_name": "Alice Wang",
            "email": "alice@example.com",
        },
    )
    s.upsert_vertex(
        "WorkItem",
        {
            "canonical_id": "urn:eoip:work:issue:AUTH-1",
            "issue_key": "AUTH-1",
            "summary": "Authentication login bug in SSO gateway",
            "description": "Users cannot log in via the SSO gateway",
            "status": "open",
            "source_system": "jira",
            "trust_state": "verified",
            "author_name": "Alice Wang",
            "modified_at": _iso(NOW_DAYS - 5),  # fresh
        },
    )
    s.upsert_vertex(
        "WorkItem",
        {
            "canonical_id": "urn:eoip:work:issue:PAY-7",
            "issue_key": "PAY-7",
            "summary": "Payment retry loop",
            "status": "open",
            "source_system": "jira",
            "trust_state": "quarantined",
            "modified_at": _iso(NOW_DAYS - 200),  # stale
        },
    )
    s.upsert_vertex(
        "File",
        {
            "canonical_id": "urn:eoip:code:file:sso_login",
            "repo_id": "auth-service",
            "path": "src/auth/sso_login.py",
            "language": "python",
            "source_system": "gitlab",
            "modified_at": _iso(NOW_DAYS - 60),  # recent
        },
    )
    s.upsert_vertex(
        "Document",
        {
            "canonical_id": "urn:eoip:knowledge:doc:runbook",
            "name": "SSO gateway runbook",
            "path": "kb/sso-runbook.md",
            "doc_format": "markdown",
            "source_system": "confluence",
            "trust_state": "verified",
            "modified_at": _iso(NOW_DAYS - 100),  # aging
        },
    )
    # Provenance: the login bug was reported in AUTH-1 with a source ref.
    s.upsert_edge(
        "REFERENCES",
        "urn:eoip:work:issue:AUTH-1",
        "urn:eoip:code:file:sso_login",
        {"source_ref": "jira://AUTH-1#comment-42", "evidence_key": "ev-42"},
    )
    # Ownership via AUTHORED_BY edge (Comment -> Person is the valid signature).
    s.upsert_vertex(
        "Comment",
        {
            "canonical_id": "urn:eoip:work:comment:42",
            "comment_id": "42",
            "content": "Reproduced the SSO gateway login failure",
            "source_system": "jira",
            "created_at": _iso(NOW_DAYS - 4),
        },
    )
    s.upsert_edge(
        "AUTHORED_BY",
        "urn:eoip:work:comment:42",
        alice["canonical_id"],
        {"source_ref": "jira://AUTH-1#comment-42"},
    )
    return s


def _iso(epoch_days: float) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(epoch_days * 86400.0, tz=timezone.utc).isoformat()


def test_keyword_search_finds_sso_entities(store):
    resp = search(store, SearchRequest(query="sso"), now=NOW_DAYS)
    ids = {h.canonical_id for h in resp.hits}
    assert "urn:eoip:work:issue:AUTH-1" in ids
    assert "urn:eoip:code:file:sso_login" in ids
    assert "urn:eoip:knowledge:doc:runbook" in ids
    assert "urn:eoip:work:issue:PAY-7" not in ids


def test_hits_preserve_identity_and_provenance(store):
    """GAP-SEARCH-002: every hit carries canonical_id and evidence pointers."""
    resp = search(store, SearchRequest(query="sso"), now=NOW_DAYS)
    assert resp.total == 4
    for hit in resp.hits:
        assert hit.canonical_id.startswith("urn:eoip:")
        assert hit.label
        assert hit.why
    by_id = {h.canonical_id: h for h in resp.hits}
    auth = by_id["urn:eoip:work:issue:AUTH-1"]
    assert "jira://AUTH-1#comment-42" in auth.evidence
    assert auth.authority == "Alice Wang"  # resolved via AUTHORED_BY edge


def test_facets_have_counts(store):
    resp = search(store, SearchRequest(query=""), now=NOW_DAYS)
    assert resp.total == 6  # filter-only search matches everything

    def as_map(buckets):
        return {b.value: b.count for b in buckets}

    types = as_map(resp.facets.entity_type)
    assert types == {"WorkItem": 2, "File": 1, "Document": 1, "Person": 1, "Comment": 1}

    domains = as_map(resp.facets.domain)
    assert domains["WORK"] == 3 and domains["CODE"] == 1 and domains["KNOWLEDGE"] == 1

    sources = as_map(resp.facets.source_system)
    assert sources["jira"] == 3 and sources["gitlab"] == 1 and sources["confluence"] == 1

    freshness = as_map(resp.facets.freshness)
    assert freshness == {"fresh": 2, "recent": 1, "aging": 1, "stale": 1, "unknown": 1}

    projects = as_map(resp.facets.project)
    assert projects["auth-service"] == 1 and projects["none"] == 5

    owners = as_map(resp.facets.owner)
    assert owners["Alice Wang"] == 2


def test_facet_filters_narrow_results(store):
    resp = search(
        store,
        SearchRequest(query="", source_systems=["jira"], trust_states=["verified"]),
        now=NOW_DAYS,
    )
    assert resp.total == 1
    assert resp.hits[0].canonical_id == "urn:eoip:work:issue:AUTH-1"
    assert resp.hits[0].trust_state == "verified"


def test_freshness_filter(store):
    resp = search(store, SearchRequest(query="", freshness=["stale"]), now=NOW_DAYS)
    assert [h.canonical_id for h in resp.hits] == ["urn:eoip:work:issue:PAY-7"]
    assert resp.hits[0].freshness == "stale"
    assert resp.hits[0].trust_state == "quarantined"


def test_matched_fields_and_terms(store):
    resp = search(store, SearchRequest(query="login gateway"), now=NOW_DAYS)
    by_id = {h.canonical_id: h for h in resp.hits}
    auth = by_id["urn:eoip:work:issue:AUTH-1"]
    assert set(auth.matched_terms) == {"login", "gateway"}
    assert "summary" in auth.matched_fields
    assert "login" in auth.why
    # Name-bearing fields outrank body-only matches.
    assert auth.score > by_id["urn:eoip:knowledge:doc:runbook"].score


def test_limit_pages_hits_but_total_and_facets_stay_global(store):
    resp = search(store, SearchRequest(query="", limit=2), now=NOW_DAYS)
    assert len(resp.hits) == 2
    assert resp.total == 6
    assert sum(b.count for b in resp.facets.entity_type) == 6


def test_entity_type_filter(store):
    engine = FacetedSearch(store)
    resp = engine.search(SearchRequest(query="", entity_types=["Document"]), now=NOW_DAYS)
    assert resp.total == 1
    assert resp.hits[0].label == "Document"
    buckets = {b.value: b.count for b in resp.facets.entity_type}
    assert buckets == {"Document": 1}
