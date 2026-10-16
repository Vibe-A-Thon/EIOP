import json

from eoip.graph.hugegraph import HugeGraphStore


def test_retained_manual_and_pipeline_records(run_id, hubble, verify_vertex):
    for suffix in ("manual", "pipeline"):
        canonical_id = f"urn:eoip:hubble:{suffix}:{run_id}"
        if suffix == "pipeline":
            canonical_id += ":source"
        verify_vertex(canonical_id)
    source = f"urn:eoip:hubble:pipeline:{run_id}:source"
    target = f"urn:eoip:hubble:pipeline:{run_id}:target"
    result = hubble(f"g.V({json.dumps(HugeGraphStore.vertex_id(source))}).out().values('canonical_id')")
    assert target in json.dumps(result)
