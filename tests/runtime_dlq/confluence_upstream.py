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
            r"/([a-f0-9]{32})/(valid|rejected|schema-drift|invalid-response|label-invalid)"
            r"/(requests|rest/api/space|rest/api/content/search|rest/api/content/[a-f0-9]{32}-page-[01]/label)", url.path
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
            elif action.endswith("/label"):
                assert action.split("/")[-2] in {f"{run_id}-page-0", f"{run_id}-page-1"}
                if mode == "label-invalid":
                    self.respond(200, {"results": {}})
                    return
                records = [
                    {"name": "runbook", "prefix": "global"},
                    {"name": "deploy", "prefix": "global"},
                    {"name": "operations", "prefix": "team"},
                ]
            else:
                query = params["cql"][0]
                assert f'space = "{space_key}"' in query
                upper = re.search(r'lastModified <= "([^"]+)"', query)
                lower = re.search(r'lastModified >= "([^"]+)"', query)
                assert upper is not None
                version = {"number": 1, "when": "2026-10-01T00:00:00Z"}
                if "type = page" in query:
                    assert params["expand"] == ["space,version,body.storage,ancestors,metadata.labels,history"]
                    records = [{
                        "id": f"{run_id}-page-{index}", "title": f"Acceptance page {index}",
                        "space": {"key": space_key},
                        "version": {**version, "by": {
                            "type": "known", "userKey": "editor-key", "displayName": "Fixture Editor",
                        }},
                        "history": {
                            "createdBy": {"type": "known", "userKey": "author-key",
                                          "username": "fixture-author", "displayName": "Fixture Author"},
                            "createdDate": "2026-09-30T00:00:00Z",
                        },
                        "metadata": {"labels": {
                            "results": [{"name": "runbook", "prefix": "global"}],
                            "_links": {"next": f"/rest/api/content/{run_id}-page-{index}/label?start=1"},
                        }},
                        "body": {"storage": {"value": (
                            f'<h2 id="fixture-{index}">Fixture page {index}</h2>'
                            '<a href="#checks">Checks</a>'
                            '<ac:structured-macro ac:name="anchor">'
                            '<ac:parameter ac:name="">checks</ac:parameter></ac:structured-macro>'
                            '<a href="https://example.org/runbook">Runbook</a>'
                            '<ac:link><ri:page ri:content-title="Acceptance page 0"/></ac:link>'
                            '<ac:structured-macro ac:name="code">'
                            '<ac:parameter ac:name="language">python</ac:parameter>'
                            '<ac:plain-text-body><![CDATA[print("ready")]]></ac:plain-text-body>'
                            '</ac:structured-macro>'
                            '<table><tr><th>State</th></tr><tr><td>Ready</td></tr></table>'
                        )}},
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
