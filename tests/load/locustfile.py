"""Locust Load Testing Scenarios for EOIP (TEST-002)."""

from locust import HttpUser, between, task


class EOIPUser(HttpUser):
    wait_time = between(0.05, 0.5)

    @task(3)
    def query_graph(self):
        self.client.post(
            "/api/v1/query/multi_paradigm",
            json={
                "dialect": "CYPHER",
                "query": "MATCH (n:Service) RETURN n LIMIT 10",
            },
        )

    @task(2)
    def classify_intent(self):
        self.client.post(
            "/api/v1/routing/classify",
            json={"text": "Check health of auth service cluster"},
        )

    @task(1)
    def serialize_token_payload(self):
        self.client.post(
            "/api/v1/token_formats/serialize",
            json={
                "format": "TOON",
                "payload": {"service": "AuthService", "criticality": "HIGH", "instances": 12},
            },
        )
