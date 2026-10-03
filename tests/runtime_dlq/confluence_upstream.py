"""Internal Data Center REST fixture; not a Confluence tenant emulator."""

import os
import re
from http.server import ThreadingHTTPServer
from threading import Lock
from typing import ClassVar
from urllib.parse import parse_qs, urlsplit

from tests.runtime_dlq.fixture_http import ProtocolFixtureHandler


class ConfluenceAPIHandler(ProtocolFixtureHandler):
    requests: ClassVar[dict[str, list[dict]]] = {}
    lock = Lock()

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/health":
            self.respond(200, {"status": "ready"})
            return
        match = re.fullmatch(
            r"/([a-f0-9]{32})/(valid|rejected|schema-drift|invalid-response)"
            r"/(requests|rest/api/space|rest/api/content/search)", url.path
        )
        if not match:
            self.respond(404, {"error": "unknown fixture route"})
            return
        run_id, mode, action = match.groups()
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
                "path": action, "params": params, "authorized": authorized,
                "correlation_id": self.headers.get("X-Correlation-ID"),
            })
        if not authorized:
            self.respond(401, {"error": "fixture authentication failed"})
            return
        try:
            start = int(params["start"][0])
            limit = int(params["limit"][0])
            assert start >= 0 and limit > 0
            space_key = f"SPACE-{run_id}"
            if action == "rest/api/space":
                assert params["expand"] == ["description.plain"]
                records = [{
                    "key": space_key, "name": "Acceptance knowledge",
                    "description": {"plain": {"value": "Fixture space"}},
                }]
            else:
                query = params["cql"][0]
                assert f'space = "{space_key}"' in query
                upper = re.search(r'lastModified <= "([^"]+)"', query)
                lower = re.search(r'lastModified >= "([^"]+)"', query)
                assert upper is not None
                version = {"number": 1, "when": "2026-10-01T00:00:00Z"}
                if "type = page" in query:
                    assert params["expand"] == ["space,version,body.storage,ancestors,metadata.labels"]
                    records = [{
                        "id": f"{run_id}-page-{index}", "title": f"Acceptance page {index}",
                        "space": {"key": space_key}, "version": version,
                        "body": {"storage": {"value": f"<p>Fixture page {index}</p>"}},
                        "ancestors": [] if index == 0 else [{"id": f"{run_id}-page-0"}],
                        "_links": {"webui": f"/pages/{run_id}-page-{index}"},
                    } for index in range(2)]
                    if mode == "rejected":
                        del records[-1]["title"]
                    if mode == "schema-drift":
                        del records[0]["id"]
                else:
                    assert "type = attachment" in query
                    assert params["expand"] == ["space,version,container,extensions"]
                    records = [{
                        "id": f"{run_id}-attachment", "title": "fixture.txt",
                        "space": {"key": space_key}, "version": version,
                        "container": {"id": f"{run_id}-page-0"},
                        "extensions": {"mediaType": "text/plain", "fileSize": 12},
                    }]
                modified = "2026-10-01 00:00"
                if modified > upper.group(1) or (lower and modified < lower.group(1)):
                    records = []
        except (KeyError, ValueError, AssertionError):
            self.respond(400, {"error": "invalid Confluence acquisition parameters"})
            return
        if mode == "invalid-response":
            self.respond(200, {"results": {"not": "a list"}})
            return
        page = records[start:start + limit]
        self.respond(200, {"results": page, "size": len(page)})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8091), ConfluenceAPIHandler).serve_forever()
