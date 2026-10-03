"""Internal-only, deterministic Table API protocol fixture; not a tenant emulator."""

import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
from typing import ClassVar
from urllib.parse import parse_qs, urlsplit


class TableAPIHandler(BaseHTTPRequestHandler):
    requests: ClassVar[dict[str, list[dict]]] = {}
    lock = Lock()

    def log_message(self, format, *args):
        # Never log credential-bearing request headers.
        return

    def respond(self, status, document):
        body = json.dumps(document).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/health":
            self.respond(200, {"status": "ready"})
            return
        match = re.fullmatch(
            r"/([a-f0-9]{32})/(valid|rejected)/(requests|api/now/table/(\w+))", url.path
        )
        if not match:
            self.respond(404, {"error": "unknown fixture route"})
            return
        run_id, mode, action, table = match.groups()
        if action == "requests":
            with self.lock:
                requests = list(self.requests.get(run_id, []))
            self.respond(200, requests)
            return
        params = parse_qs(url.query)
        authorized = self.headers.get("Authorization") == (
            "Bearer " + os.environ["EOIP_ACCEPTANCE_SOURCE_TOKEN"]
        )
        with self.lock:
            self.requests.setdefault(run_id, []).append({
                "table": table, "params": params, "authorized": authorized,
                "correlation_id": self.headers.get("X-Correlation-ID"),
            })
        if not authorized:
            self.respond(401, {"error": "fixture authentication failed"})
            return
        if table not in {"incident", "problem", "change_request", "kb_knowledge"}:
            self.respond(404, {"error": "unknown fixture table"})
            return
        try:
            offset = int(params["sysparm_offset"][0])
            limit = int(params["sysparm_limit"][0])
            query = params["sysparm_query"][0]
            assert offset >= 0 and limit > 0
            assert params["sysparm_display_value"] == ["false"]
            assert params["sysparm_exclude_reference_link"] == ["true"]
            assert "ORDERBYsys_updated_on" in query and "ORDERBYsys_id" in query
            assert "sys_updated_on<=" in query
        except (KeyError, ValueError, AssertionError):
            self.respond(400, {"error": "invalid Table API acquisition parameters"})
            return
        records = [{
            "sys_id": f"{run_id}-{table}-{index}",
            "number": f"{table.upper()}-{run_id}-{index}",
            "short_description": f"Acceptance {table} {index}",
            "description": "Fixture evidence", "state": "open",
            "sys_updated_on": "2026-10-01 00:00:00",
        } for index in range(2 if table == "incident" else 1)]
        if mode == "rejected" and table == "incident":
            del records[-1]["number"]
        for part in query.split("^"):
            if part.startswith("sys_updated_on>="):
                records = [r for r in records if r["sys_updated_on"] >= part.split(">=", 1)[1]]
            elif part.startswith("sys_updated_on<="):
                records = [r for r in records if r["sys_updated_on"] <= part.split("<=", 1)[1]]
        self.respond(200, {"result": records[offset:offset + limit]})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8090), TableAPIHandler).serve_forever()
