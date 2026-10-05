def test_manual_import_and_hubble_readback(api, run_id, verify_vertex):
    canonical_id = f"urn:eoip:hubble:manual:{run_id}"
    body = {
        "data": {
            "canonical_id": canonical_id,
            "entity_type": "Service",
            "service_id": f"hubble-manual-{run_id}",
            "name": f"Hubble manual verification {run_id}",
        },
        "source_label": "hubble_runtime_verification",
        "pipeline_id": f"hubble_manual_{run_id}",
    }
    rejected = api.post(
        "/api/v1/admin/ingestion/json",
        json=body,
        headers={"Authorization": "Bearer invalid-runtime-verification-token"},
    )
    assert rejected.status_code in (401, 403)
    response = api.post("/api/v1/admin/ingestion/json", json=body)
    response.raise_for_status()
    result = response.json()
    assert result["error_count"] == 0, result["errors"]
    assert result["entities_created"] == 1
    verify_vertex(canonical_id)
