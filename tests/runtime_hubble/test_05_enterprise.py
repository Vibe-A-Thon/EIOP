"""Read the enriched typed graph through both application and Hubble surfaces."""

import json
from pathlib import Path

from eoip.demo_scenarios import demo_display_name
from eoip.graph.hugegraph import HugeGraphStore

ROOT = Path(__file__).resolve().parents[2]


def test_enriched_scenarios_and_names_match_the_live_application(api, hubble):
    pack = json.loads((ROOT / "demo" / "demodata" / "enterprise" / "scenario-pack.json").read_text())
    response = api.get("/api/v1/demo/scenarios")
    response.raise_for_status()
    scenarios = response.json()["scenarios"]
    assert {s["id"] for s in scenarios} == {s["id"] for s in pack["scenarios"]}
    assert all(s["ready"] for s in scenarios)
    expected = {v["properties"]["canonical_id"]: v for v in pack["vertices"]}
    actual = {}
    for offset in range(0, len(pack["vertices"]), 25):
        batch = pack["vertices"][offset:offset + 25]
        ids = ",".join(json.dumps(HugeGraphStore.vertex_id(v["properties"]["canonical_id"])) for v in batch)
        graph = hubble(f"g.V({ids})")["graph_view"]
        actual.update({v["properties"]["canonical_id"]: v for v in graph["vertices"]})
    assert set(actual) == set(expected)
    for cid, vertex in expected.items():
        assert actual[cid]["properties"]["display_name"] == demo_display_name(vertex["label"], vertex["properties"])
    for vertex in pack["vertices"][:14]:
        cid = vertex["properties"]["canonical_id"]
        response = api.get(f"/api/v1/entities/{cid}")
        response.raise_for_status()
        assert cid in response.text
        assert actual[cid]["properties"]["display_name"] in response.text


def test_enriched_relationships_are_queryable_without_duplicate_legacy_facts(hubble):
    pack = json.loads((ROOT / "demo" / "demodata" / "enterprise" / "scenario-pack.json").read_text())
    graphs = {}
    legacy_index = 0
    for item in pack["edges"]:
        source = HugeGraphStore.vertex_id(item["from"])
        target = HugeGraphStore.vertex_id(item["to"])
        if source not in graphs:
            graphs[source] = hubble(f"g.V({json.dumps(source)}).outE().limit(500)")["graph_view"]
        graph = graphs[source]
        fact_key = item.get("properties", {}).get("fact_key")
        if not fact_key:
            fact_key = f"demo:1.0.0:{legacy_index}:{item['label']}"
            legacy_index += 1
        matching = [e for e in graph["edges"] if e["target"] == target
                    and e["label"].split("__")[0] == item["label"]
                    and e["properties"].get("fact_key") == fact_key]
        assert len(matching) == 1, fact_key
    facts = hubble("g.E().values('fact_key').fold()")["json_view"]["data"][0]
    legacy = [key for key in facts if key.startswith("demo:1.0.0:")]
    assert len(legacy) == len(set(legacy)) == 92
