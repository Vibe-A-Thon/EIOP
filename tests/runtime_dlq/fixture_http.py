"""Shared response plumbing for internal source-protocol fixtures."""

import json
from http.server import BaseHTTPRequestHandler


class ProtocolFixtureHandler(BaseHTTPRequestHandler):
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
