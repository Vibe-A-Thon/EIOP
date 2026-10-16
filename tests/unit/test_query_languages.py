"""Tests for extended query language parsers: EOQL, OSQL, Semantic QL."""

from eoip.graph.memory import MemoryGraphStore


def _vertex(store, label, canonical_id, **props):
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id, **props})


def _build_store():
    store = MemoryGraphStore()
    a = _vertex(store, "WorkItem", "item:A", issue_key="A-1", status="open", priority="high")
    b = _vertex(store, "WorkItem", "item:B", issue_key="B-1", status="closed", priority="low")
    c = _vertex(store, "Commit", "commit:C", commit_sha="abc123")
    d = _vertex(store, "File", "file:D", repo_id="repo1", path="d.py")
    store.upsert_edge("IMPLEMENTS", c["vid"], a["vid"], {})
    store.upsert_edge("MODIFIES", c["vid"], d["vid"], {})
    store.upsert_edge("IMPLEMENTS", c["vid"], b["vid"], {})
    return store


# --- EOQL ---

def test_eoql_select_all_fields():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "SELECT * FROM WorkItem")
    assert result["language"] == "EOQL"
    assert result["operation"] == "SELECT"
    assert result["count"] >= 2


def test_eoql_select_specific_fields():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "SELECT issue_key, status FROM WorkItem")
    assert result["count"] >= 2
    for row in result["results"]:
        assert "issue_key" in row


def test_eoql_select_where():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "SELECT * FROM WorkItem WHERE status = open")
    assert result["count"] >= 1
    for row in result["results"]:
        assert row.get("status") == "open"


def test_eoql_select_where_not_equal():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "SELECT * FROM WorkItem WHERE status != closed")
    for row in result["results"]:
        assert row.get("status") != "closed"


def test_eoql_select_with_limit():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "SELECT * FROM WorkItem LIMIT 1")
    assert result["count"] <= 1


def test_eoql_select_with_join():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "SELECT * FROM Commit JOIN IMPLEMENTS")
    assert result["count"] >= 1
    for row in result["results"]:
        assert "joined_IMPLEMENTS" in row


def test_eoql_traverse():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "TRAVERSE FROM commit:C DEPTH 2")
    assert result["language"] == "EOQL"
    assert result["operation"] == "TRAVERSE"


def test_eoql_aggregate():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "AGGREGATE WorkItem BY status")
    assert result["language"] == "EOQL"
    assert result["operation"] == "AGGREGATE"
    assert "buckets" in result


def test_eoql_empty_query():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "")
    assert "error" in result


def test_eoql_invalid_syntax():
    from eoip.query.languages import parse_eoql
    store = _build_store()
    result = parse_eoql(store, "INVALID QUERY")
    assert "error" in result


# --- OSQL ---

def test_osql_list_types():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "LIST TYPES")
    assert result["language"] == "OSQL"
    assert result["operation"] == "LIST_TYPES"
    assert isinstance(result["types"], list)
    assert result["count"] > 0


def test_osql_list_domains():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "LIST DOMAINS")
    assert result["language"] == "OSQL"
    assert result["operation"] == "LIST_DOMAINS"


def test_osql_list_relationships():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "LIST RELATIONSHIPS")
    assert result["language"] == "OSQL"
    assert result["operation"] == "LIST_RELATIONSHIPS"
    assert isinstance(result["relationships"], list)


def test_osql_describe():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "DESCRIBE WorkItem")
    assert result["language"] == "OSQL"
    assert result["operation"] == "DESCRIBE"
    assert result["type"] == "WorkItem"
    assert "properties" in result


def test_osql_describe_unknown_type():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "DESCRIBE NonExistent")
    assert "error" in result


def test_osql_schema_for():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "SCHEMA FOR WorkItem")
    assert result["language"] == "OSQL"
    assert result["type"] == "WorkItem"


def test_osql_instances_of():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "INSTANCES OF WorkItem")
    assert result["language"] == "OSQL"
    assert result["operation"] == "INSTANCES"
    assert result["count"] >= 2


def test_osql_instances_with_limit():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "INSTANCES OF WorkItem LIMIT 1")
    assert result["count"] <= 1


def test_osql_unknown_command():
    from eoip.query.languages import parse_osql
    store = _build_store()
    result = parse_osql(store, "DROP TABLE WorkItem")
    assert "error" in result


# --- Semantic Query Language ---

def test_semantic_meaning_entity_type():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "MEANING OF WorkItem")
    assert result["language"] == "SemanticQL"
    assert result["operation"] == "MEANING"
    assert result["count"] >= 1


def test_semantic_meaning_name_search():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "MEANING OF item:A")
    assert result["language"] == "SemanticQL"


def test_semantic_related():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "RELATED TO commit:C")
    assert result["language"] == "SemanticQL"
    assert result["operation"] == "RELATED"
    assert result["count"] >= 1


def test_semantic_related_filtered():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "RELATED TO commit:C BY IMPLEMENTS")
    assert result["language"] == "SemanticQL"
    assert result["filter"] == "IMPLEMENTS"


def test_semantic_explain():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "EXPLAIN commit:C")
    assert result["language"] == "SemanticQL"
    assert result["operation"] == "EXPLAIN"
    assert result["canonical_id"] == "commit:C"
    assert result["total_connections"] >= 1


def test_semantic_explain_not_found():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "EXPLAIN nonexistent:X")
    assert "error" in result


def test_semantic_compare():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "COMPARE item:A AND item:B")
    assert result["language"] == "SemanticQL"
    assert result["operation"] == "COMPARE"
    assert result["same_type"] is True
    assert isinstance(result["shared_properties"], list)


def test_semantic_classify():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "CLASSIFY commit:C")
    assert result["language"] == "SemanticQL"
    assert result["operation"] == "CLASSIFY"
    assert result["entity_type"] == "Commit"
    assert result["degree"] >= 1


def test_semantic_classify_not_found():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "CLASSIFY nonexistent:X")
    assert "error" in result


def test_semantic_unknown_command():
    from eoip.query.languages import parse_semantic_query
    store = _build_store()
    result = parse_semantic_query(store, "DELETE everything")
    assert "error" in result
