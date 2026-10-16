import json

from eoip.graph.hugegraph import HugeGraphStore


def test_batch_pipeline_entities_relationships_and_hubble_readback(api, run_id, hubble, verify_vertex):
    source = f"urn:eoip:hubble:pipeline:{run_id}:source"
    target = f"urn:eoip:hubble:pipeline:{run_id}:target"
    data = {
        "entities": [
            {
                "canonical_id": source,
                "entity_type": "Service",
                "service_id": source,
                "name": f"Hubble source {run_id}",
            },
            {
                "canonical_id": target,
                "entity_type": "Service",
                "service_id": target,
                "name": f"Hubble target {run_id}",
            },
        ],
        "relationships": [{"from_id": source, "to_id": target, "type": "DEPENDS_ON"}],
    }
    body = {
        "files": [{"data": data, "source_label": "hubble_runtime_verification"}],
        "pipeline_id": f"hubble_pipeline_{run_id}",
    }
    rejected = api.post(
        "/api/v1/admin/ingestion/json/batch",
        json=body,
        headers={"Authorization": "Bearer invalid-runtime-verification-token"},
    )
    assert rejected.status_code in (401, 403)
    response = api.post("/api/v1/admin/ingestion/json/batch", json=body)
    response.raise_for_status()
    result = response.json()
    assert result["error_count"] == 0, result["errors"]
    assert result["entities_created"] == 2
    assert result["relationships_created"] == 1
    verify_vertex(source)
    verify_vertex(target)
    result = hubble(f"g.V({json.dumps(HugeGraphStore.vertex_id(source))}).out().values('canonical_id')")
    assert target in json.dumps(result), "Pipeline edge missing from Hubble"
