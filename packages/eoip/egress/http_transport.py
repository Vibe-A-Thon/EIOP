"""Production HTTP transport for the EgressGateway: OpenAI-compatible chat + embeddings.

The gateway decides *whether* and *what* may leave (policy, DLP, canaries, consent, budgets); this
transport only performs the already-approved call and is deliberately strict about *where*:

* the request URL is built from the endpoint's pinned ``url_allowlist[0]`` and re-checked against the
  allowlist; redirects are refused (a 3xx would let a provider move the data elsewhere);
* HTTPS is mandatory - plain HTTP is accepted only for loopback hosts when ``allow_loopback_http`` is
  set explicitly (local Ollama / vLLM sidecars in dev and CI);
* an endpoint flagged ``mtls=True`` fails closed unless a client certificate is configured;
* the API key is resolved per call from a credential callback (default: the environment variable
  ``EOIP_EGRESS_KEY_<ENDPOINT_ID>``) and never stored on the transport or echoed in errors;
* ``trust_env=False`` so ambient proxy variables cannot silently reroute traffic; the deployment's
  egress proxy is configured explicitly via ``proxy``;
* 429/5xx are retried a bounded number of times honouring ``Retry-After``; 401/403 raise
  :class:`EgressTransportAuthError`; oversized responses are rejected.

Any exception raised here is converted by the gateway into ``EgressOutage`` with a sealed manifest
and a local-model fallback notice (SR-LLM-019).

Validation status: contract-tested against an OpenAI-compatible mock and live against the local
Ollama OpenAI-compatible API in CI; live validation with a customer's provider account is pending.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import time
from typing import Any, Callable
from urllib.parse import urlsplit

import httpx

from eoip.egress.gateway import EndpointConfig

CredentialFn = Callable[[EndpointConfig], "str | None"]


class EgressTransportError(RuntimeError):
    """The approved call could not be completed (gateway maps this to EgressOutage)."""


class EgressTransportAuthError(EgressTransportError):
    """Provider rejected the credentials (401/403)."""


def env_credentials(endpoint: EndpointConfig) -> str | None:
    """Default credential lookup: ``EOIP_EGRESS_KEY_<ENDPOINT_ID>`` (non-alnum -> ``_``)."""
    name = "EOIP_EGRESS_KEY_" + re.sub(r"[^A-Za-z0-9]", "_", endpoint.id).upper()
    return os.environ.get(name) or None


def _is_loopback(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


class OpenAICompatibleTransport:
    """``Transport`` for :class:`~eoip.egress.gateway.EgressGateway` speaking the OpenAI wire API."""

    PATHS = {"chat": "/v1/chat/completions", "embed": "/v1/embeddings"}

    def __init__(self, *, models: dict[str, str], credentials: CredentialFn | None = None,
                 timeout: float = 30.0, max_retries: int = 2, max_response_bytes: int = 4 * 1024 * 1024,
                 allow_loopback_http: bool = False, client_cert: str | tuple[str, str] | None = None,
                 proxy: str | None = None, transport: httpx.BaseTransport | None = None,
                 sleep: Callable[[float], None] = time.sleep, max_tokens: int = 512) -> None:
        self.models = dict(models)
        self.credentials = credentials or env_credentials
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))
        self.max_response_bytes = max_response_bytes
        self.allow_loopback_http = allow_loopback_http
        self.client_cert = client_cert
        self.proxy = proxy
        self._transport = transport
        self._sleep = sleep
        self.max_tokens = max_tokens
        self.last_request: dict[str, Any] | None = None  # url/model/kind only - no payload, no key

    # -------------------------------------------------------------- Transport protocol
    def __call__(self, payload: dict, endpoint: EndpointConfig) -> dict:
        kind = endpoint.kind
        if kind not in self.PATHS:
            raise EgressTransportError(f"endpoint kind {kind!r} has no OpenAI-compatible transport")
        model = self.models.get(endpoint.id)
        if not model:
            raise EgressTransportError(f"no model configured for endpoint {endpoint.id}")
        url = self._resolve_url(endpoint, self.PATHS[kind])
        body = self._chat_body(payload, model) if kind == "chat" else self._embed_body(payload, model)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        key = self.credentials(endpoint)
        if key:
            headers["Authorization"] = f"Bearer {key}"
        self.last_request = {"url": url, "model": model, "kind": kind}
        data = self._post(url, body, headers)
        return self._parse_chat(data) if kind == "chat" else self._parse_embed(data)

    # -------------------------------------------------------------- URL pinning
    def _resolve_url(self, endpoint: EndpointConfig, path: str) -> str:
        if not endpoint.url_allowlist:
            raise EgressTransportError(f"endpoint {endpoint.id} has no pinned URL (url_allowlist empty)")
        base = endpoint.url_allowlist[0].rstrip("/")
        if base.endswith("/v1"):
            base = base[:-3]
        url = base + path
        parts = urlsplit(url)
        host = parts.hostname or ""
        if parts.scheme != "https":
            if not (parts.scheme == "http" and self.allow_loopback_http and _is_loopback(host)):
                raise EgressTransportError("egress requires https (plain http only for opted-in loopback)")
        if parts.username or parts.password:
            raise EgressTransportError("credentials in endpoint URL are not allowed")
        if not any(url.startswith(a.rstrip("/")) for a in endpoint.url_allowlist):
            raise EgressTransportError("resolved URL is outside the endpoint allowlist")
        if endpoint.mtls and self.client_cert is None:
            raise EgressTransportError(f"endpoint {endpoint.id} requires mTLS but no client certificate is configured")
        return url

    # -------------------------------------------------------------- request bodies
    def _chat_body(self, payload: dict, model: str) -> dict:
        messages = payload.get("messages")
        if not isinstance(messages, list) or not messages:
            system = payload.get("system")
            prompt = payload.get("prompt") if isinstance(payload.get("prompt"), str) else None
            if prompt is None:
                fields = {k: v for k, v in payload.items() if k not in {"system", "max_tokens", "temperature"}}
                prompt = json.dumps(fields, sort_keys=True, default=str)
            messages = ([{"role": "system", "content": str(system)}] if system else []) + [
                {"role": "user", "content": prompt}]
        body: dict[str, Any] = {"model": model, "messages": messages, "stream": False,
                                "max_tokens": int(payload.get("max_tokens") or self.max_tokens)}
        if "temperature" in payload:
            body["temperature"] = float(payload["temperature"])
        return body

    @staticmethod
    def _embed_body(payload: dict, model: str) -> dict:
        texts = payload.get("input", payload.get("texts", payload.get("text")))
        if isinstance(texts, str):
            texts = [texts]
        if not isinstance(texts, list) or not texts or not all(isinstance(t, str) for t in texts):
            raise EgressTransportError("embed payload needs 'input'/'texts' (str or list[str])")
        return {"model": model, "input": texts}

    # -------------------------------------------------------------- HTTP
    def _post(self, url: str, body: dict, headers: dict[str, str]) -> dict:
        client_kwargs: dict[str, Any] = {"timeout": self.timeout, "trust_env": False, "follow_redirects": False}
        if self.client_cert is not None:
            client_kwargs["cert"] = self.client_cert
        if self.proxy:
            client_kwargs["proxy"] = self.proxy
        if self._transport is not None:
            client_kwargs["transport"] = self._transport
        attempt = 0
        with httpx.Client(**client_kwargs) as client:
            while True:
                try:
                    resp = client.post(url, json=body, headers=headers)
                except httpx.HTTPError as exc:
                    if attempt < self.max_retries:
                        attempt += 1
                        self._sleep(min(2.0 ** attempt, 10.0))
                        continue
                    raise EgressTransportError(f"network error: {type(exc).__name__}") from None
                status = resp.status_code
                if status in (401, 403):
                    raise EgressTransportAuthError(f"provider rejected credentials (HTTP {status})")
                if 300 <= status < 400:
                    raise EgressTransportError(f"redirect refused (HTTP {status})")
                if status == 429 or status >= 500:
                    if attempt < self.max_retries:
                        attempt += 1
                        self._sleep(self._retry_after(resp, attempt))
                        continue
                    raise EgressTransportError(f"provider unavailable after {attempt + 1} attempts (HTTP {status})")
                if status >= 400:
                    raise EgressTransportError(f"provider refused request (HTTP {status}{self._error_type(resp)})")
                if len(resp.content) > self.max_response_bytes:
                    raise EgressTransportError("provider response exceeds max_response_bytes")
                try:
                    return resp.json()
                except ValueError:
                    raise EgressTransportError("provider returned non-JSON response") from None

    @staticmethod
    def _retry_after(resp: httpx.Response, attempt: int) -> float:
        try:
            return min(float(resp.headers.get("Retry-After", "")), 30.0)
        except ValueError:
            return min(2.0 ** attempt, 10.0)

    @staticmethod
    def _error_type(resp: httpx.Response) -> str:
        try:
            err = resp.json().get("error")
            kind = err.get("type") or err.get("code") if isinstance(err, dict) else None
        except (ValueError, AttributeError):
            kind = None
        return f", {str(kind)[:60]}" if kind else ""

    # -------------------------------------------------------------- response parsing
    @staticmethod
    def _parse_chat(data: dict) -> dict:
        try:
            choice = data["choices"][0]
            text = choice["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise EgressTransportError("malformed chat completion response") from None
        if not isinstance(text, str):
            raise EgressTransportError("chat completion has no text content")
        return {"text": text, "model": data.get("model"), "finish_reason": choice.get("finish_reason"),
                "usage": data.get("usage") or {}}

    @staticmethod
    def _parse_embed(data: dict) -> dict:
        try:
            rows = sorted(data["data"], key=lambda r: r.get("index", 0))
            vectors = [[float(x) for x in r["embedding"]] for r in rows]
        except (KeyError, TypeError, ValueError):
            raise EgressTransportError("malformed embeddings response") from None
        if not vectors:
            raise EgressTransportError("embeddings response is empty")
        return {"embeddings": vectors, "model": data.get("model"), "usage": data.get("usage") or {}}


def transport_from_env(env: dict[str, str] | None = None) -> OpenAICompatibleTransport | None:
    """Opt-in API wiring: ``EOIP_EGRESS_TRANSPORT=openai-compatible`` (else ``None`` = no network)."""
    env = dict(os.environ if env is None else env)
    if env.get("EOIP_EGRESS_TRANSPORT", "").strip().lower() != "openai-compatible":
        return None
    models = json.loads(env.get("EOIP_EGRESS_MODELS") or "{}")
    if not isinstance(models, dict) or not all(isinstance(v, str) for v in models.values()):
        raise ValueError("EOIP_EGRESS_MODELS must be a JSON object of endpoint-id -> model name")
    return OpenAICompatibleTransport(models=models, proxy=env.get("EOIP_EGRESS_PROXY") or None,
                                     client_cert=env.get("EOIP_EGRESS_CLIENT_CERT") or None)
