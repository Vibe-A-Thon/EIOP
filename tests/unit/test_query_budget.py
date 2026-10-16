from itertools import pairwise

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.traversal import GraphTraversal


def test_path_and_impact_stop_when_the_visit_budget_is_exhausted():
    store = MemoryGraphStore()
    vertices = [
        store.upsert_vertex(
            "CodeSymbol",
            {"canonical_id": f"symbol:{i}", "qualified_name": f"s{i}", "symbol_kind": "function"},
        )
        for i in range(4)
    ]
    for a, b in pairwise(vertices):
        store.upsert_edge("CALLS", a["vid"], b["vid"], {})
    traversal = GraphTraversal(store)
    traversal._max_visited = 2
    with pytest.raises(ValueError, match="traversal budget"):
        traversal.find_path("symbol:0", "symbol:3")
    result = traversal.impact("symbol:0")
    assert result["truncated"]
    assert len(result["impacted"]) == 1


def test_current_traversals_exclude_tombstoned_endpoints():
    store = MemoryGraphStore()
    a = store.upsert_vertex(
        "CodeSymbol", {"canonical_id": "a", "qualified_name": "a", "symbol_kind": "function"}
    )
    b = store.upsert_vertex(
        "CodeSymbol", {"canonical_id": "b", "qualified_name": "b", "symbol_kind": "function"}
    )
    store.upsert_edge("CALLS", a["vid"], b["vid"], {})
    store.tombstone_vertex("b")
    traversal = GraphTraversal(store)
    assert traversal.find_path("a", "b") is None
    assert traversal.impact("a")["impacted"] == []
    assert traversal.impact("b")["source"] is None
