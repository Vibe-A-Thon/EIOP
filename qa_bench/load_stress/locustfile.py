"""Locust Distributed Load Testing Scenario for KnowGridFlow / EOIP.

Usage:
  locust -f qa_bench/load_stress/locustfile.py --host http://localhost:8001
  locust -f qa_bench/load_stress/locustfile.py --headless -u 20 -r 5 -t 30s --host http://localhost:8001
"""

from locust import HttpUser, task, between
import os

TOKEN = os.environ.get("QA_TOKEN_SUPERADMIN") or os.environ.get("EOIP_API_TOKEN")
if not TOKEN:
    raise RuntimeError("Set QA_TOKEN_SUPERADMIN (or EOIP_API_TOKEN) to a provisioned principal's token")
TENANT = os.environ.get("EOIP_TENANT", "default")


class GraphReaderUser(HttpUser):
    """Simulates frequent read operations (60% weight)."""
    weight = 6
    wait_time = between(0.2, 1.0)

    def on_start(self):
        self.client.headers.update({
            "Authorization": f"Bearer {TOKEN}",
            "X-Tenant-Id": TENANT,
            "Accept": "application/json",
        })

    @task(3)
    def get_schema(self):
        self.client.get("/api/v1/graph/schema")

    @task(2)
    def get_backend(self):
        self.client.get("/api/v1/graph/backend")

    @task(1)
    def check_whoami(self):
        self.client.get("/api/v1/auth/whoami")


class AnalystUser(HttpUser):
    """Simulates active query executions (40% weight)."""
    weight = 4
    wait_time = between(0.5, 2.0)

    def on_start(self):
        self.client.headers.update({
            "Authorization": f"Bearer {TOKEN}",
            "X-Tenant-Id": TENANT,
            "Accept": "application/json",
        })

    @task(2)
    def query_history(self):
        self.client.get("/api/v1/query/history")

    @task(1)
    def execute_eql(self):
        self.client.post("/api/v1/query/eql", json={"query": "find all requirements"})
