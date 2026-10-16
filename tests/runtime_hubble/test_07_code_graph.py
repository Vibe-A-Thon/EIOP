"""Authenticated source export ingestion and actual Hubble/RocksDB read-back."""

import json
from pathlib import Path

import pytest
from eoip.graph.hugegraph import HugeGraphStore


@pytest.mark.parametrize("mode", ["manual", "pipelines"])
def test_code_export_ingestion_and_hubble_readback(api, hubble, verify_vertex, mode):
    root = Path(__file__).resolve().parents[2]
    data = json.loads((root / "demo" / "demodata" / mode / "code-graph.json").read_text())
    repository = data["repository"]
    repo_id = repository if isinstance(repository, str) else repository["repo_id"]
    body = {"data": data, "source_label": f"live_code_{mode}", "pipeline_id": "live_code_export"}
    rejected = api.post(
        "/api/v1/admin/ingestion/json", json=body,
        headers={"Authorization": "Bearer invalid-code-export-token"},
    )
    assert rejected.status_code in (401, 403)
    for _ in range(2):
        response = api.post("/api/v1/admin/ingestion/json", json=body)
        response.raise_for_status()
        receipt = response.json()
        assert receipt["error_count"] == 0, receipt["errors"]
        assert receipt["entities_created"] == (
            2 + len(data["files"]) + len(data["symbols"]) +
            len(data.get("dependencies", [])) + len(data["runtime_dependencies"])
        )
        assert receipt["relationships_created"] == len(data["files"]) + len(data["symbols"]) + len(data["edges"])
        symbol = data["symbols"][0]["qualified_name"]
        verify_vertex(f"CodeSymbol:{repo_id}:{symbol}")
        first_edge = data["edges"][0]
        assert (first_edge.get("kind") or first_edge.get("edge_type")) == "calls"
        source = first_edge.get("from_symbol") or first_edge.get("source")
        source_id = HugeGraphStore.vertex_id(f"CodeSymbol:{repo_id}:{source}")
        result = hubble(
            f"g.V({json.dumps(source_id)}).outE('CALLS__CodeSymbol__CodeSymbol').valueMap('payload_json')"
        )
        payload = json.dumps(first_edge, sort_keys=True)
        matches = [edge for edge in result["json_view"]["data"] if edge.get("payload_json") == payload]
        assert len(matches) == 1, result
