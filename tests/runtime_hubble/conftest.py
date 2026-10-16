"""Opt-in live tests; synthetic verification data is intentionally retained."""

import json
import os
import re
from pathlib import Path
from uuid import uuid4

import httpx
import pytest
from eoip.graph.hugegraph import HugeGraphStore

from scripts.setup_hubble import hubble_data


@pytest.fixture(scope="session", autouse=True)
def live_opt_in():
    if os.environ.get("EOIP_RUNTIME_HUBBLE") != "1":
        pytest.skip("Set EOIP_RUNTIME_HUBBLE=1 to test the running local deployment")


@pytest.fixture(scope="session")
def run_id():
    value = os.environ.get("EOIP_RUNTIME_RUN_ID", uuid4().hex)
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value):
        raise ValueError("EOIP_RUNTIME_RUN_ID must contain only letters, numbers, '_' or '-'")
    return value


@pytest.fixture(scope="session")
def api():
    token = os.environ.get("EOIP_API_TOKEN")
    if not token:
        env_file = Path(__file__).resolve().parents[2] / "deploy" / ".env"
        entries = [
            line.split("=", 1)[1]
            for line in env_file.read_text(encoding="utf-8-sig").splitlines()
            if line.startswith("EOIP_API_TOKEN=")
        ]
        if len(entries) != 1:
            raise ValueError("Expected exactly one local EOIP_API_TOKEN")
        token = entries[0]
    with httpx.Client(
        base_url=os.environ.get("EOIP_RUNTIME_API_URL", "http://localhost:8000"),
        headers={"Authorization": f"Bearer {token}"},
        timeout=120,
        trust_env=False,
    ) as client:
        client.get("/health/ready").raise_for_status()
        yield client


@pytest.fixture(scope="session")
def hubble():
    with httpx.Client(
        base_url=os.environ.get("EOIP_RUNTIME_HUBBLE_URL", "http://localhost:8088"),
        timeout=120,
        trust_env=False,
    ) as client:
        response = client.get("/actuator/health")
        response.raise_for_status()
        assert response.json()["status"] == "UP"
        response = client.get("/api/v1.2/graph-connections", params={"page_size": 100})
        matches = [
            record["id"]
            for record in hubble_data(response)["records"]
            if record["host"] == "hugegraph-server" and record["graph"] == "hugegraph"
        ]
        assert len(matches) == 1, "Expected one connection to the existing local graph"
        connection_id = matches[0]

        def query(content):
            response = client.post(
                f"/api/v1.2/graph-connections/{connection_id}/gremlin-query",
                json={"content": content},
            )
            return hubble_data(response)

        yield query


@pytest.fixture
def verify_vertex(hubble):
    def verify(canonical_id):
        result = hubble(f"g.V({json.dumps(HugeGraphStore.vertex_id(canonical_id))}).valueMap(true)")
        assert canonical_id in json.dumps(result), "Ingested vertex missing from Hubble read-back"

    return verify
