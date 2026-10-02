import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.traversal import GraphTraversal


def _vertex(store: MemoryGraphStore, label: str, canonical_id: str) -> dict:
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id})


def test_find_path_returns_shortest_ordered_path_in_both_directions() -> None:
    store = MemoryGraphStore()
    issue = _vertex(store, "WorkItem", "issue:EOIP-1")
    commit = _vertex(store, "Commit", "commit:abc")
    file = _vertex(store, "File", "file:src/app.py")
    symbol = _vertex(store, "CodeSymbol", "symbol:src/app.py:run")
    store.upsert_edge("IMPLEMENTS", commit["vid"], issue["vid"], {})
    store.upsert_edge("MODIFIES", commit["vid"], file["vid"], {})
    store.upsert_edge("DECLARES", file["vid"], symbol["vid"], {})

    result = GraphTraversal(store).find_path(issue["canonical_id"], symbol["canonical_id"])

    assert [vertex["canonical_id"] for vertex in result["vertices"]] == [
        "issue:EOIP-1",
        "commit:abc",
        "file:src/app.py",
        "symbol:src/app.py:run",
    ]
    assert [edge["label"] for edge in result["edges"]] == ["IMPLEMENTS", "MODIFIES", "DECLARES"]


def test_impact_is_bounded_and_excludes_non_allowlisted_edges() -> None:
    store = MemoryGraphStore()
    root = _vertex(store, "CodeSymbol", "symbol:root")
    child = _vertex(store, "CodeSymbol", "symbol:child")
    domain = _vertex(store, "GraphDomain", "domain:CODE")
    store.upsert_edge("CALLS", root["vid"], child["vid"], {})
    store.upsert_edge("BELONGS_TO_DOMAIN", root["vid"], domain["vid"], {})

    result = GraphTraversal(store, max_depth=1).impact(root["canonical_id"])

    assert [item["vertex"]["canonical_id"] for item in result["impacted"]] == ["symbol:child"]
    assert result["truncated"] is False


def test_query_limits_cannot_exceed_configured_depth() -> None:
    traversal = GraphTraversal(MemoryGraphStore(), max_depth=3)

    with pytest.raises(ValueError, match="max_depth"):
        traversal.find_path("missing", "also-missing", max_depth=4)


def test_impact_stops_when_configured_time_budget_expires(monkeypatch) -> None:
    store = MemoryGraphStore()
    root = _vertex(store, "CodeSymbol", "symbol:root")
    child = _vertex(store, "CodeSymbol", "symbol:child")
    store.upsert_edge("CALLS", root["vid"], child["vid"], {})
    clock = [0.0]
    monkeypatch.setattr("eoip.graph.traversal.monotonic", lambda: clock[0])
    traversal = GraphTraversal(store, timeout_seconds=1.0)
    original_neighbors = traversal._neighbors

    def slow_neighbors(vid, direction, deadline):
        clock[0] += 2.0
        return original_neighbors(vid, direction, deadline)

    monkeypatch.setattr(traversal, "_neighbors", slow_neighbors)

    result = traversal.impact(root["canonical_id"])

    assert result["truncated"] is True
    assert result["impacted"] == []


def test_path_stops_when_configured_time_budget_expires(monkeypatch) -> None:
    store = MemoryGraphStore()
    root = _vertex(store, "CodeSymbol", "symbol:root")
    child = _vertex(store, "CodeSymbol", "symbol:child")
    store.upsert_edge("CALLS", root["vid"], child["vid"], {})
    clock = [0.0]
    monkeypatch.setattr("eoip.graph.traversal.monotonic", lambda: clock[0])
    traversal = GraphTraversal(store, timeout_seconds=1.0)
    original_neighbors = traversal._neighbors

    def slow_neighbors(vid, direction, deadline):
        clock[0] += 2.0
        return original_neighbors(vid, direction, deadline)

    monkeypatch.setattr(traversal, "_neighbors", slow_neighbors)

    with pytest.raises(ValueError, match="traversal budget"):
        traversal.find_path(root["canonical_id"], child["canonical_id"])


@pytest.mark.parametrize("timeout_seconds", [0, -1, float("inf"), float("nan")])
def test_timeout_budget_must_be_a_positive_finite_number(timeout_seconds) -> None:
    with pytest.raises(ValueError, match="timeout_seconds"):
        GraphTraversal(MemoryGraphStore(), timeout_seconds=timeout_seconds)
