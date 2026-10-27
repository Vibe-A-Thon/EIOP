"""Test that OpenAPI schema has zero duplicate operation IDs (CC3-009)."""

from _principals import provision_api_token
from eoip.graph.memory import MemoryGraphStore


def test_openapi_no_duplicate_operation_ids(monkeypatch, tmp_path):
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("EOIP_API_TOKEN", "test-token-minimum-24-characters!!")
    provision_api_token(None, "test-token-minimum-24-characters!!")

    from apps.api import main
    monkeypatch.setattr(main, "create_store", lambda: MemoryGraphStore())

    app = main.create_app()
    openapi = app.openapi()

    ops = {}
    dups = []
    for p, pdata in openapi.get("paths", {}).items():
        for m, mdata in pdata.items():
            if isinstance(mdata, dict) and "operationId" in mdata:
                op_id = mdata["operationId"]
                if op_id in ops:
                    dups.append((op_id, ops[op_id], (m, p)))
                else:
                    ops[op_id] = (m, p)

    assert dups == [], f"Found duplicate operation IDs in OpenAPI schema: {dups}"
