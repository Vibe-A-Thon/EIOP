"""Locust load scenarios for EOIP (TEST-002).

FT-X07: scenarios target routes that exist in /openapi.json and authenticate
with a bearer token read from EOIP_LOAD_TOKEN (never hard-coded). Run, e.g.:

    EOIP_LOAD_TOKEN=... locust -f tests/load/locustfile.py --headless \
        -u 5 -r 5 -t 30s --host http://127.0.0.1:8000 --csv test-results/load
"""

import os

from locust import HttpUser, between, task

# Route -> sample request body. Kept as plain data so tests can check them
# against create_app().openapi() without importing locust.
QUERY_MULTI_PARADIGM = "/api/v1/query/multi-paradigm"
ROUTING_CLASSIFY = "/api/v1/platform/routing/classify-and-route"
TOKEN_FORMATS_SERIALIZE = "/api/v1/platform/token-formats/serialize"

SCENARIOS = {
    QUERY_MULTI_PARADIGM: {"query": "MATCH (n:Service) RETURN n LIMIT 10", "max_depth": 2},
    ROUTING_CLASSIFY: {"query": "Check health of auth service cluster", "context": {}},
    TOKEN_FORMATS_SERIALIZE: {
        "format_name": "TOON",
        "payload": {"service": "AuthService", "criticality": "HIGH", "instances": 12},
    },
}


class EOIPUser(HttpUser):
    wait_time = between(0.05, 0.5)

    def on_start(self):
        token = os.environ.get("EOIP_LOAD_TOKEN", "")
        if not token:
            raise RuntimeError("EOIP_LOAD_TOKEN is required (bearer token for the target stack)")
        self.client.headers["Authorization"] = f"Bearer {token}"
        with self.client.get("/openapi.json", name="openapi (preflight)", catch_response=True) as resp:
            paths = resp.json().get("paths", {}) if resp.ok else {}
            missing = [route for route in SCENARIOS if route not in paths]
            if missing:
                resp.failure(f"routes missing from /openapi.json: {missing}")
                raise RuntimeError(f"routes missing from /openapi.json: {missing}")

    @task(3)
    def query_graph(self):
        self.client.post(QUERY_MULTI_PARADIGM, json=SCENARIOS[QUERY_MULTI_PARADIGM])

    @task(2)
    def classify_intent(self):
        self.client.post(ROUTING_CLASSIFY, json=SCENARIOS[ROUTING_CLASSIFY])

    @task(1)
    def serialize_token_payload(self):
        self.client.post(TOKEN_FORMATS_SERIALIZE, json=SCENARIOS[TOKEN_FORMATS_SERIALIZE])
