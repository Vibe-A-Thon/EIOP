"""API surface mining from HAR, access logs, and OTLP traces (T-601 / REVA-AS-001..005)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse


@dataclass
class ObservedApiCall:
    method: str
    url: str
    path: str
    status_code: int
    content_type: Optional[str] = None
    request_headers: Dict[str, str] = field(default_factory=dict)
    response_headers: Dict[str, str] = field(default_factory=dict)
    caller_ip: Optional[str] = None
    service_name: Optional[str] = None


def parse_har_entries(har_content: Union[str, bytes, dict]) -> List[ObservedApiCall]:
    """Parse HAR 1.2 JSON export for observed HTTP requests and responses."""
    if isinstance(har_content, (str, bytes)):
        data = json.loads(har_content)
    else:
        data = har_content

    entries = data.get("log", {}).get("entries", [])
    calls: List[ObservedApiCall] = []

    for e in entries:
        req = e.get("request", {})
        resp = e.get("response", {})

        url = req.get("url", "")
        parsed_url = urlparse(url)
        method = req.get("method", "GET").upper()
        status_code = resp.get("status", 200)

        # Content-type
        ct = None
        for h in resp.get("headers", []):
            if h.get("name", "").lower() == "content-type":
                ct = h.get("value")
                break

        calls.append(
            ObservedApiCall(
                method=method,
                url=url,
                path=parsed_url.path or "/",
                status_code=status_code,
                content_type=ct,
            )
        )

    return calls


def parse_combined_access_log(log_text: str) -> List[ObservedApiCall]:
    """Parse NGINX / Apache combined log format."""
    # Pattern: IP - - [date] "METHOD PATH HTTP/1.x" status bytes ...
    pattern = re.compile(
        r'^(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"([A-Z]+)\s+([^\s"]+)[^"]*"\s+(\d{3})\s+(\S+)'
    )
    calls: List[ObservedApiCall] = []

    for line in log_text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if m:
            ip, date_str, method, path, status, size = m.groups()
            calls.append(
                ObservedApiCall(
                    method=method,
                    url=path,
                    path=path.split("?")[0],
                    status_code=int(status),
                    caller_ip=ip,
                )
            )

    return calls


def generate_openapi_skeleton(calls: List[ObservedApiCall], title: str = "Mined API") -> Dict[str, Any]:
    """Infer candidate OpenAPI 3.1 specification from observed traffic."""
    paths: Dict[str, Any] = {}

    for c in calls:
        p = c.path
        m = c.method.lower()

        if p not in paths:
            paths[p] = {}
        if m not in paths[p]:
            paths[p][m] = {
                "summary": f"Observed {c.method} {p}",
                "responses": {},
            }

        status_str = str(c.status_code)
        if status_str not in paths[p][m]["responses"]:
            paths[p][m]["responses"][status_str] = {
                "description": f"HTTP {status_str}",
            }

    return {
        "openapi": "3.1.0",
        "info": {
            "title": title,
            "version": "1.0.0",
        },
        "paths": paths,
    }
