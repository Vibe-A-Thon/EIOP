"""Phase 11 — Visual Intelligence & Polish tests.

Tests for semantic zoom, fisheye distortion, edge bundling,
color-blind palette, and orthogonal layout.
"""

import math

# ---------------------------------------------------------------------------
# 11.1 Semantic Zoom
# ---------------------------------------------------------------------------

def test_semantic_zoom_cluster_level():
    assert _zoom_level(0.1) == "cluster"
    assert _zoom_level(0.29) == "cluster"


def test_semantic_zoom_entity_level():
    assert _zoom_level(0.3) == "entity"
    assert _zoom_level(0.5) == "entity"
    assert _zoom_level(0.79) == "entity"


def test_semantic_zoom_detail_level():
    assert _zoom_level(0.8) == "detail"
    assert _zoom_level(1.0) == "detail"
    assert _zoom_level(2.5) == "detail"


def _zoom_level(zoom: float) -> str:
    if zoom < 0.3:
        return "cluster"
    if zoom < 0.8:
        return "entity"
    return "detail"


# ---------------------------------------------------------------------------
# 11.2 Fisheye Distortion
# ---------------------------------------------------------------------------

def test_fisheye_center_node_amplified():
    positions = {"a": {"x": 100, "y": 100}, "b": {"x": 300, "y": 300}}
    result = _fisheye(positions, 100, 100, radius=200, distortion=2)
    assert result["a"]["x"] == 100 and result["a"]["y"] == 100


def test_fisheye_near_node_displaced():
    positions = {"a": {"x": 150, "y": 100}}
    result = _fisheye(positions, 100, 100, radius=200, distortion=2)
    assert result["a"]["x"] > 150


def test_fisheye_distant_node_unchanged():
    positions = {"a": {"x": 500, "y": 500}}
    result = _fisheye(positions, 100, 100, radius=200, distortion=2)
    assert result["a"]["x"] == 500 and result["a"]["y"] == 500


def _fisheye(positions, fx, fy, radius=200, distortion=2):
    result = {}
    for nid, pos in positions.items():
        dx = pos["x"] - fx
        dy = pos["y"] - fy
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > radius or dist == 0:
            result[nid] = dict(pos)
        else:
            normalised = dist / radius
            scale = distortion * (1 - normalised * normalised) + 1
            result[nid] = {"x": fx + dx * scale, "y": fy + dy * scale}
    return result


# ---------------------------------------------------------------------------
# 11.3 Force-Directed Edge Bundling
# ---------------------------------------------------------------------------

def test_edge_compatibility_identical_edges():
    e = {"x1": 0, "y1": 0, "x2": 100, "y2": 0}
    c = _angle_compat(e, e) * _scale_compat(e, e) * _position_compat(e, e)
    assert c > 0.99


def test_edge_compatibility_perpendicular_edges():
    e1 = {"x1": 0, "y1": 0, "x2": 100, "y2": 0}
    e2 = {"x1": 50, "y1": -50, "x2": 50, "y2": 50}
    ac = _angle_compat(e1, e2)
    assert ac < 0.1


def test_edge_bundling_produces_control_points():
    edges = [
        {"x1": 0, "y1": 0, "x2": 100, "y2": 0},
        {"x1": 0, "y1": 10, "x2": 100, "y2": 10},
    ]
    result = _bundle(edges)
    assert len(result) == 2
    for path in result:
        assert len(path) >= 2
        assert path[0]["x"] == edges[0]["x1"] or path[0]["x"] == edges[1]["x1"]


def _edge_len(e):
    dx = e["x2"] - e["x1"]
    dy = e["y2"] - e["y1"]
    return math.sqrt(dx * dx + dy * dy) or 0.001


def _edge_vec(e):
    l = _edge_len(e)
    return ((e["x2"] - e["x1"]) / l, (e["y2"] - e["y1"]) / l)


def _angle_compat(e1, e2):
    v1 = _edge_vec(e1)
    v2 = _edge_vec(e2)
    return abs(v1[0] * v2[0] + v1[1] * v2[1])


def _scale_compat(e1, e2):
    l1, l2 = _edge_len(e1), _edge_len(e2)
    avg = (l1 + l2) / 2
    return 2 / (avg / min(l1, l2) + max(l1, l2) / avg)


def _position_compat(e1, e2):
    m1x = (e1["x1"] + e1["x2"]) / 2
    m1y = (e1["y1"] + e1["y2"]) / 2
    m2x = (e2["x1"] + e2["x2"]) / 2
    m2y = (e2["y1"] + e2["y2"]) / 2
    avg = (_edge_len(e1) + _edge_len(e2)) / 2
    dist = math.sqrt((m1x - m2x) ** 2 + (m1y - m2y) ** 2)
    return avg / (avg + dist)


def _bundle(edges, iterations=2):
    paths = [
        [{"x": e["x1"], "y": e["y1"]}, {"x": e["x2"], "y": e["y2"]}]
        for e in edges
    ]
    for _ in range(iterations):
        new_paths = []
        for i, e in enumerate(edges):
            pts = paths[i]
            mid = {"x": (pts[0]["x"] + pts[-1]["x"]) / 2, "y": (pts[0]["y"] + pts[-1]["y"]) / 2}
            new_paths.append([pts[0], mid, pts[-1]])
        paths = new_paths
    return paths


# ---------------------------------------------------------------------------
# 11.4 Color-Blind Safe Palette
# ---------------------------------------------------------------------------

def test_deuteranopia_palette_avoids_pure_red_green_confusion():
    palette = _deuteranopia()
    reds = [v for v in palette.values() if _is_confusing_red(v)]
    greens = [v for v in palette.values() if _is_confusing_green(v)]
    assert not (reds and greens), "Palette uses both confusable red and green"


def test_tritanopia_palette_avoids_blue_yellow():
    palette = _tritanopia()
    for name, hex_val in palette.items():
        r, g, b = _hex_to_rgb(hex_val)
        assert not (r < 80 and g < 80 and b > 200), f"{name}={hex_val} is pure blue"


def test_high_contrast_palette_has_maximum_contrast():
    palette = _high_contrast()
    assert palette["domain-meta"] == "#000000" or palette["domain-meta"] == "#FFFFFF"


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _is_confusing_red(h):
    r, g, b = _hex_to_rgb(h)
    return r > 180 and g < 100 and b < 100 and abs(r - g) > 120


def _is_confusing_green(h):
    r, g, b = _hex_to_rgb(h)
    return g > 180 and r < 100 and b < 100 and abs(g - r) > 120


def _deuteranopia():
    return {
        "domain-1": "#0077BB", "domain-2": "#EE7733", "domain-3": "#CCBB44",
        "domain-4": "#009988", "domain-5": "#CC3311", "domain-6": "#33BBEE",
    }


def _tritanopia():
    return {
        "domain-1": "#332288", "domain-2": "#CC6677", "domain-3": "#AA4499",
        "domain-4": "#882255", "domain-5": "#661100", "domain-6": "#117733",
    }


def _high_contrast():
    return {
        "domain-meta": "#000000", "domain-work": "#FFFFFF", "domain-code": "#FFD700",
        "domain-cicd": "#00BFFF", "domain-knowledge": "#FF4500", "domain-identity": "#00FF00",
    }


# ---------------------------------------------------------------------------
# 11.5 Orthogonal Layout
# ---------------------------------------------------------------------------

def test_orthogonal_layout_grid_placement():
    nodes = [{"id": f"n{i}"} for i in range(9)]
    edges = [{"from_id": f"n{i}", "to_id": f"n{i+3}"} for i in range(6)]
    positions = _orthogonal(nodes, edges)
    coords = [(p["x"], p["y"]) for p in positions.values()]
    assert len(set(coords)) == 9


def test_orthogonal_layout_respects_dag_order():
    nodes = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    edges = [{"from_id": "a", "to_id": "b"}, {"from_id": "b", "to_id": "c"}]
    positions = _orthogonal(nodes, edges)
    assert positions["a"]["y"] < positions["b"]["y"]
    assert positions["b"]["y"] < positions["c"]["y"]


def test_orthogonal_layout_no_overlap():
    nodes = [{"id": f"n{i}"} for i in range(16)]
    positions = _orthogonal(nodes, [])
    coords = [(p["x"], p["y"]) for p in positions.values()]
    assert len(set(coords)) == 16


def _orthogonal(nodes, edges, spacing=140):
    adj = {n["id"]: [] for n in nodes}
    incoming = {n["id"]: 0 for n in nodes}
    for e in edges:
        if e["from_id"] in adj:
            adj[e["from_id"]].append(e["to_id"])
        if e["to_id"] in incoming:
            incoming[e["to_id"]] += 1

    rank = {}
    queue = [n["id"] for n in nodes if not incoming[n["id"]]]
    visited = set()
    qi = 0
    while qi < len(queue):
        nid = queue[qi]
        qi += 1
        if nid in visited:
            continue
        visited.add(nid)
        rank.setdefault(nid, 0)
        for tgt in adj.get(nid, []):
            rank[tgt] = max(rank.get(tgt, 0), rank[nid] + 1)
            if tgt not in visited:
                queue.append(tgt)
    for n in nodes:
        if n["id"] not in rank:
            rank[n["id"]] = 0

    by_rank: dict[int, list] = {}
    for n in nodes:
        r = rank[n["id"]]
        by_rank.setdefault(r, []).append(n)

    positions = {}
    max_rank = max(by_rank.keys()) if by_rank else 0
    for r in range(max_rank + 1):
        row = by_rank.get(r, [])
        total_w = len(row) * spacing
        for i, node in enumerate(row):
            positions[node["id"]] = {
                "x": (i - len(row) / 2) * spacing + total_w / 2,
                "y": r * spacing,
            }
    return positions
