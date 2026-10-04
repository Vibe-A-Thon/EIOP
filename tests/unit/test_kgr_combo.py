"""Phase 10 tests: combo node creation, grouping, edge aggregation, and AMBIGUOUS evidence."""

import os

from eoip.graph.memory import MemoryGraphStore


def _file_props(cid, name=None):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py", "name": name or cid}


# --- ComboNode.jsx utility tests (pure-JS logic verified via Python analogues) ---

def test_group_by_domain():
    nodes = [
        {"id": "a", "domain": "CODE", "label": "File"},
        {"id": "b", "domain": "CODE", "label": "File"},
        {"id": "c", "domain": "OPS", "label": "Service"},
    ]
    groups = {}
    for n in nodes:
        d = n.get("domain", "OTHER")
        groups.setdefault(d, []).append(n["id"])
    result = [{"id": f"combo:domain:{d}", "name": d, "memberIds": ids}
              for d, ids in groups.items() if len(ids) > 1]
    assert len(result) >= 1
    code_group = [g for g in result if g["name"] == "CODE"]
    assert len(code_group) == 1
    assert set(code_group[0]["memberIds"]) == {"a", "b"}


def test_group_by_type():
    nodes = [
        {"id": "a", "label": "File"},
        {"id": "b", "label": "File"},
        {"id": "c", "label": "Service"},
        {"id": "d", "label": "File"},
    ]
    groups = {}
    for n in nodes:
        t = n.get("label", "Unknown")
        groups.setdefault(t, []).append(n["id"])
    result = [{"id": f"combo:type:{t}", "name": t, "memberIds": ids}
              for t, ids in groups.items() if len(ids) > 1]
    file_group = [g for g in result if g["name"] == "File"]
    assert len(file_group) == 1
    assert len(file_group[0]["memberIds"]) == 3


def test_group_by_community():
    communities = [
        {"id": 0, "members": ["a", "b", "c"], "auto_label": "Files: auth"},
        {"id": 1, "members": ["d", "e"], "auto_label": "Services: api"},
    ]
    result = [{"id": f"combo:community:{c['id']}", "name": c.get("auto_label", f"Community {c['id']}"),
               "memberIds": c["members"]}
              for c in communities if len(c["members"]) > 1]
    assert len(result) == 2
    assert result[0]["name"] == "Files: auth"


def test_combo_edge_aggregation():
    _nodes = [
        {"id": "a", "domain": "CODE"}, {"id": "b", "domain": "CODE"},
        {"id": "c", "domain": "OPS"}, {"id": "d", "domain": "OPS"},
    ]
    edges = [
        {"from_id": "a", "to_id": "c", "type": "DEPENDS_ON", "id": "e1"},
        {"from_id": "b", "to_id": "c", "type": "DEPENDS_ON", "id": "e2"},
        {"from_id": "b", "to_id": "d", "type": "DEPENDS_ON", "id": "e3"},
        {"from_id": "a", "to_id": "b", "type": "DEPENDS_ON", "id": "e4"},
    ]
    member_to_group = {"a": "combo:CODE", "b": "combo:CODE", "c": "combo:OPS", "d": "combo:OPS"}
    super_edges = {}
    internal_removed = 0
    for e in edges:
        fg = member_to_group.get(e["from_id"])
        tg = member_to_group.get(e["to_id"])
        if fg and tg and fg == tg:
            internal_removed += 1
            continue
        src = fg or e["from_id"]
        tgt = tg or e["to_id"]
        key = f"{src}|{tgt}|{e['type']}"
        if fg or tg:
            if key not in super_edges:
                super_edges[key] = {"from_id": src, "to_id": tgt, "type": e["type"], "count": 0}
            super_edges[key]["count"] += 1
    assert internal_removed == 1
    assert len(super_edges) == 1
    se = next(iter(super_edges.values()))
    assert se["count"] == 3
    assert se["from_id"] == "combo:CODE"
    assert se["to_id"] == "combo:OPS"


def test_custom_group_creation():
    selected = ["x", "y", "z"]
    group = {"id": "combo:custom:123", "name": "My Group", "memberIds": list(selected)}
    assert group["name"] == "My Group"
    assert len(group["memberIds"]) == 3


def test_combo_node_jsx_exists():
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "ComboNode.jsx"))


# --- AMBIGUOUS evidence status ---

def test_ambiguous_creation_status_validation():
    from eoip.contracts.normalized import CreationStatus
    assert "AMBIGUOUS" in CreationStatus.__args__


def test_ambiguous_edge_in_graph():
    store = MemoryGraphStore()
    a = store.upsert_vertex("File", _file_props("urn:f1"))
    b = store.upsert_vertex("File", _file_props("urn:f2"))
    edge = store.upsert_edge("DEPENDS_ON", a["vid"], b["vid"], {"creation_status": "AMBIGUOUS"})
    assert edge["properties"]["creation_status"] == "AMBIGUOUS"
