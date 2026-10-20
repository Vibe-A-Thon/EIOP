"""FT-X07: every Locust scenario targets a real, authenticated route with a valid body."""

from __future__ import annotations

import ast
import secrets
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

LOCUSTFILE = Path(__file__).resolve().parents[2] / "tests" / "load" / "locustfile.py"


def _scenarios() -> dict:
    tree = ast.parse(LOCUSTFILE.read_text(encoding="utf-8"))
    consts, scenarios = {}, None
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if isinstance(node.value, ast.Constant):
                consts[name] = node.value.value
            elif name == "SCENARIOS":
                scenarios = node.value
    assert scenarios is not None
    return {consts[k.id]: ast.literal_eval(v) for k, v in zip(scenarios.keys, scenarios.values)}


def test_locustfile_has_no_hard_coded_token():
    text = LOCUSTFILE.read_text(encoding="utf-8")
    assert "EOIP_LOAD_TOKEN" in text
    assert "Bearer " not in text.replace('f"Bearer {token}"', "")


@pytest.fixture()
def api(monkeypatch, tmp_path):
    from apps.api import main as api_main

    token = secrets.token_urlsafe(32)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("EOIP_GRAPH_BACKEND", "memory")
    monkeypatch.setattr(api_main, "api_token", lambda: token)
    return TestClient(api_main.create_app()), token


def test_scenario_routes_exist_require_auth_and_accept_bodies(api):
    client, token = api
    paths = client.get("/openapi.json").json()["paths"]
    for route, body in _scenarios().items():
        assert route in paths and "post" in paths[route], route
        assert client.post(route, json=body).status_code == 401, route
        response = client.post(route, json=body, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200, (route, response.status_code, response.text[:200])
