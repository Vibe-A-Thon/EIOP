"""Typed Python client SDK (proposed package 'eoip-python') (CRA-039.6)."""

from __future__ import annotations

import logging
from typing import Any
from collections.abc import Mapping

import httpx

logger = logging.getLogger("eoip.sdk.python_client")


class EOIPClientError(Exception):
    """Base class for EOIP client exceptions."""

    def __init__(self, message: str, code: str = "CLIENT_ERROR", details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.details = details or {}


class AuthenticationError(EOIPClientError):
    """Raised when authentication fails."""


class NotFoundError(EOIPClientError):
    """Raised when an entity or resource is not found."""


class GovernanceViolationError(EOIPClientError):
    """Raised when a governed action violates policy or autonomy."""


class EOIPClient:
    """Official typed client SDK for EOIP public APIs."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_token: str | None = None,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout
        headers = {"Accept": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=self.timeout,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> EOIPClient:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            data = {"message": response.text}

        if response.is_success:
            return data

        error_obj = data.get("error", {})
        code = error_obj.get("code", "HTTP_ERROR")
        msg = error_obj.get("message", response.text)
        details = error_obj.get("details", {})

        if response.status_code == 401:
            raise AuthenticationError(msg, code=code, details=details)
        elif response.status_code == 404:
            raise NotFoundError(msg, code=code, details=details)
        elif response.status_code in (403, 422) and "GOVERNANCE" in code:
            raise GovernanceViolationError(msg, code=code, details=details)
        else:
            raise EOIPClientError(msg, code=code, details=details)

    def search(self, query: str, limit: int = 25) -> list[dict[str, Any]]:
        """Search entities by text or canonical ID."""
        resp = self._client.get("/api/v1/search", params={"q": query, "limit": limit})
        return self._handle_response(resp).get("results", [])

    def get_entity(self, canonical_id: str) -> dict[str, Any]:
        """Fetch entity by canonical ID."""
        from urllib.parse import quote
        resp = self._client.get(f"/api/v1/entities/{quote(canonical_id, safe='')}")
        return self._handle_response(resp)

    def query(self, plan: dict[str, Any]) -> dict[str, Any]:
        """Execute a structured query plan."""
        resp = self._client.post("/api/v1/query", json=plan)
        return self._handle_response(resp)

    def propose_action(self, intent: dict[str, Any]) -> dict[str, Any]:
        """Propose a governed action."""
        resp = self._client.post("/api/v1/actions/propose", json=intent)
        return self._handle_response(resp)

    def get_capabilities(self) -> dict[str, Any]:
        """Inspect platform capabilities and states."""
        resp = self._client.get("/api/v1/capabilities")
        return self._handle_response(resp)
