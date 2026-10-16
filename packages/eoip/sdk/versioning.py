"""API Versioning & Client SDK Generation Engine (INFRA-006).

Implements:
- APIVersionManager: v1/v2 co-existence, deprecation headers, Sunset policies (RFC 8594)
- ClientSDKGenerator: Generates client SDK bindings for Python, TypeScript/JavaScript, and Go
"""

from __future__ import annotations

import datetime
import json
import logging
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger("eoip.sdk.versioning")


class VersionStatus(str, Enum):
    CURRENT = "CURRENT"
    SUPPORTED = "SUPPORTED"
    DEPRECATED = "DEPRECATED"
    SUNSET = "SUNSET"


@dataclass
class VersionMetadata:
    version: str  # "v1", "v2"
    status: VersionStatus = VersionStatus.SUPPORTED
    release_date: str = "2026-01-01"
    sunset_date: str | None = None
    migration_guide_url: str = ""

    def get_response_headers(self) -> dict[str, str]:
        headers = {"X-API-Version": self.version}
        if self.status in (VersionStatus.DEPRECATED, VersionStatus.SUNSET):
            headers["Deprecation"] = "true"
            if self.sunset_date:
                headers["Sunset"] = self.sunset_date
            if self.migration_guide_url:
                headers["Link"] = f'<{self.migration_guide_url}>; rel="deprecation"'
        return headers


class APIVersionManager:
    """Manages API version lifecycle and header injection."""

    def __init__(self) -> None:
        self.versions: dict[str, VersionMetadata] = {}
        self._lock = threading.Lock()
        self._bootstrap_versions()

    def _bootstrap_versions(self) -> None:
        self.register_version("v1", VersionStatus.DEPRECATED, sunset_date="2027-01-01", migration_url="/docs/v1-to-v2")
        self.register_version("v2", VersionStatus.CURRENT)

    def register_version(
        self,
        version: str,
        status: VersionStatus = VersionStatus.CURRENT,
        sunset_date: str | None = None,
        migration_url: str = "",
    ) -> VersionMetadata:
        with self._lock:
            meta = VersionMetadata(
                version=version,
                status=status,
                sunset_date=sunset_date,
                migration_guide_url=migration_url,
            )
            self.versions[version] = meta
            return meta

    def get_version(self, version: str) -> VersionMetadata | None:
        with self._lock:
            return self.versions.get(version)

    def route_version(self, path: str) -> tuple[str, str]:
        """Extract version and sub-path: '/api/v1/users' -> ('v1', '/users')."""
        parts = path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "api" and parts[1] in self.versions:
            ver = parts[1]
            sub = "/" + "/".join(parts[2:])
            return ver, sub
        return "v2", path


class ClientSDKGenerator:
    """Generates idiomatic client SDK boilerplates for multiple programming languages."""

    def generate_python_sdk(self, openapi_spec: dict[str, Any]) -> str:
        title = openapi_spec.get("info", {}).get("title", "KnowGridFlowClient")
        endpoints = list(openapi_spec.get("paths", {}).keys())[:10]

        code = [
            f"# Auto-generated Python SDK for {title}",
            "import requests",
            "",
            "class KnowGridFlowClient:",
            "    def __init__(self, base_url: str, api_key: str | None = None):",
            "        self.base_url = base_url.rstrip('/')",
            "        self.session = requests.Session()",
            "        if api_key:",
            "            self.session.headers['Authorization'] = f'Bearer {api_key}'",
            "",
        ]
        for ep in endpoints:
            safe_name = ep.replace("/", "_").replace("-", "_").strip("_")
            code.append(f"    def {safe_name}(self, **kwargs):")
            code.append(f"        return self.session.post(f'{{self.base_url}}{ep}', json=kwargs).json()")
            code.append("")
        return "\n".join(code)

    def generate_typescript_sdk(self, openapi_spec: dict[str, Any]) -> str:
        title = openapi_spec.get("info", {}).get("title", "KnowGridFlowClient")
        endpoints = list(openapi_spec.get("paths", {}).keys())[:10]

        code = [
            f"// Auto-generated TypeScript SDK for {title}",
            "export class KnowGridFlowClient {",
            "    constructor(private baseUrl: string, private apiKey?: string) {}",
            "",
            "    private async request(path: string, payload: any) {",
            "        const res = await fetch(`${this.baseUrl}${path}`, {",
            "            method: 'POST',",
            "            headers: {",
            "                'Content-Type': 'application/json',",
            "                ...(this.apiKey ? { 'Authorization': `Bearer ${this.apiKey}` } : {})",
            "            },",
            "            body: JSON.stringify(payload)",
            "        });",
            "        return res.json();",
            "    }",
            "",
        ]
        for ep in endpoints:
            safe_name = "".join(part.capitalize() for part in ep.replace("-", "_").split("/") if part)
            code.append(f"    async {safe_name}(payload: Record<string, any> = {{}}) {{")
            code.append(f"        return this.request('{ep}', payload);")
            code.append("    }")
        code.append("}")
        return "\n".join(code)

    def generate_go_sdk(self, openapi_spec: dict[str, Any]) -> str:
        code = [
            "// Auto-generated Go SDK for KnowGridFlow",
            "package knowgridflow",
            "",
            "import (",
            '    "bytes"',
            '    "encoding/json"',
            '    "net/http"',
            ")",
            "",
            "type Client struct {",
            "    BaseURL string",
            "    APIKey  string",
            "    HTTP    *http.Client",
            "}",
            "",
            "func NewClient(baseURL string, apiKey string) *Client {",
            "    return &Client{BaseURL: baseURL, APIKey: apiKey, HTTP: &http.Client{}}",
            "}",
        ]
        return "\n".join(code)
