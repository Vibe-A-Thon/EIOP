"""Local model abstraction (FR-RAG-002).

Pluggable local model provider that wraps Ollama or compatible endpoints.
The system remains useful when the model is stopped.
"""

from __future__ import annotations

import ipaddress
import json
import os
import socket
import urllib.parse
from collections.abc import Iterator
from dataclasses import dataclass

import httpx

ALLOWED_DEFAULT_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "local-model"})
METADATA_IPS = frozenset({"169.254.169.254", "169.254.170.2", "fd00:ec2::254"})
METADATA_HOSTNAMES = frozenset({"metadata.google.internal", "metadata", "instance-data"})


def _configured_model_hosts() -> frozenset[str]:
    """Hosts an operator explicitly approved via EOIP_ALLOWED_MODEL_HOSTS."""
    return frozenset(
        h.strip().lower().rstrip(".")
        for h in os.getenv("EOIP_ALLOWED_MODEL_HOSTS", "").split(",")
        if h.strip()
    )


def validate_model_endpoint_url(url: str, *, profile: str = "local") -> None:
    """Validate model endpoint URL to enforce strict local egress policy (CC3-001 / SR-LLM-002).

    Rejects non-HTTP(S) schemes, userinfo (scheme/authority confusion), cloud metadata endpoints,
    link-local/multicast/unspecified addresses, and any host outside the approved allowlist.
    The only supported profile is ``local``: it allows the loopback hosts plus explicitly
    configured hosts (``EOIP_OLLAMA_URL`` default ``local-model`` and ``EOIP_ALLOWED_MODEL_HOSTS``).
    """
    if profile != "local":
        raise ModelUnavailable(
            f"Egress policy violation: unsupported model profile '{profile}'. Only 'local' is permitted."
        )
    if not url:
        raise ModelUnavailable("Model URL cannot be empty")

    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ("http", "https"):
        raise ModelUnavailable(f"Egress policy violation: unsupported scheme '{parsed.scheme}'. Only http/https permitted.")
    if parsed.username or parsed.password:
        raise ModelUnavailable("Egress policy violation: userinfo is not permitted in the model URL")

    # Normalize: lowercase, strip IPv6 brackets and trailing root-label dot so that
    # "LOCALHOST.", "127.0.0.1." etc. cannot bypass the allowlist (no naive parsing).
    hostname = (parsed.hostname or "").lower().strip("[]").rstrip(".")
    if not hostname:
        raise ModelUnavailable("Egress policy violation: missing host in model URL")

    # Reject cloud metadata endpoints
    if hostname in METADATA_HOSTNAMES or hostname in METADATA_IPS:
        raise ModelUnavailable(f"Egress policy violation: access to cloud metadata endpoint '{hostname}' is denied")

    # Reject link-local, multicast and unspecified IPs; loopback is the local profile
    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        ip = None  # hostname string, checked against the allowlist below
    if ip is not None:
        if ip.is_link_local:
            raise ModelUnavailable(f"Egress policy violation: link-local IP '{hostname}' is denied")
        if ip.is_multicast:
            raise ModelUnavailable(f"Egress policy violation: multicast IP '{hostname}' is denied")
        if ip.is_unspecified:
            raise ModelUnavailable(f"Egress policy violation: unspecified IP '{hostname}' is denied")
        if ip.is_loopback:
            return  # loopback literals are always allowed in the local profile

    allowed = ALLOWED_DEFAULT_HOSTS | _configured_model_hosts()

    if hostname not in allowed:
        raise ModelUnavailable(
            f"Egress policy violation: host '{hostname}' is not in the approved local-model allowlist ({sorted(allowed)})"
        )


def validate_resolved_model_host(hostname: str) -> None:
    """Resolve the model host and reject denied answers (DNS-rebinding guard, CC3-001).

    Fail-closed: an unresolvable host raises. Every resolved address must be loopback or
    private (local profile destinations); link-local/multicast/unspecified/metadata answers
    are always rejected, and a public address is accepted only for a host the operator
    explicitly configured in EOIP_ALLOWED_MODEL_HOSTS.
    """
    hostname = hostname.lower().strip("[]").rstrip(".")
    try:
        infos = socket.getaddrinfo(hostname, None)
    except OSError as exc:
        raise ModelUnavailable(f"Egress policy violation: model host '{hostname}' cannot be resolved") from exc
    for info in infos:
        addr = str(info[4][0]).split("%", 1)[0]
        try:
            ip = ipaddress.ip_address(addr)
        except ValueError:
            continue
        if ip.is_link_local or ip.is_multicast or ip.is_unspecified or str(ip) in METADATA_IPS:
            raise ModelUnavailable(
                f"Egress policy violation: model host '{hostname}' resolves to denied address '{addr}'"
            )
        if ip.is_loopback or ip.is_private:
            continue  # local profile destination
        if hostname not in _configured_model_hosts():
            raise ModelUnavailable(
                f"Egress policy violation: model host '{hostname}' resolves to non-local address '{addr}'; "
                "remote egress requires an explicit EOIP_ALLOWED_MODEL_HOSTS entry"
            )


@dataclass(frozen=True)
class ModelResponse:
    content: str
    model: str
    generation: str
    tokens_used: int | None = None


def _reject_redirect(response: httpx.Response) -> None:
    """Refuse redirects outright: the model endpoint must answer directly (CC3-001)."""
    if 300 <= response.status_code < 400:
        raise ModelUnavailable(
            f"Egress policy violation: model endpoint attempted a redirect (HTTP {response.status_code})"
        )


class LocalModelProvider:
    """Hardened local model provider (CC3-001 / SR-LLM-002).

    The endpoint URL is validated at construction and re-validated (including DNS resolution)
    before every request. Only the ``local`` profile exists: loopback plus explicitly
    configured hosts. Redirects are refused, ``trust_env=False`` disables ambient proxies.
    Construct via ``create_model_provider`` so every call site shares this policy.
    """

    def __init__(
        self,
        model: str | None = None,
        url: str | None = None,
        timeout: float = 90.0,
        profile: str | None = None,
    ) -> None:
        self._model = model or os.getenv("EOIP_OLLAMA_MODEL", "")
        self._url = url or os.getenv("EOIP_OLLAMA_URL", "http://local-model:11434")
        self._timeout = timeout
        self._profile = profile or os.getenv("EOIP_MODEL_PROFILE", "local")
        validate_model_endpoint_url(self._url, profile=self._profile)

    def _check_endpoint(self) -> None:
        """Re-validate scheme/host/allowlist and resolve the host before each request.

        Resolution is repeated per request so a host that rebinds to a denied address
        (link-local, cloud metadata, or a non-allowlisted public IP) is refused even if it
        passed construction-time validation.
        """
        validate_model_endpoint_url(self._url, profile=self._profile)
        hostname = urllib.parse.urlsplit(self._url).hostname or ""
        validate_resolved_model_host(hostname)

    @property
    def available(self) -> bool:
        return bool(self._model)

    @property
    def model_name(self) -> str | None:
        """Configured local model identifier without exposing its service URL."""
        return self._model or None

    def generate(
        self,
        system_prompt: str,
        user_content: str,
        *,
        temperature: float = 0,
        max_tokens: int = 512,
    ) -> ModelResponse:
        if not self._model:
            raise ModelUnavailable("No local model is configured")

        self._check_endpoint()
        try:
            with httpx.Client(timeout=self._timeout, trust_env=False, follow_redirects=False) as client:
                response = client.post(
                    f"{self._url}/api/chat",
                    json={
                        "model": self._model,
                        "stream": False,
                        "options": {"temperature": temperature, "num_predict": max_tokens},
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content},
                        ],
                    },
                )
                _reject_redirect(response)
                response.raise_for_status()
                data = response.json()
                return ModelResponse(
                    content=data["message"]["content"],
                    model=self._model,
                    generation="local_model",
                    tokens_used=data.get("eval_count"),
                )
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            raise ModelUnavailable(f"Local model request failed: {type(exc).__name__}") from exc

    # -- raw prompt API: the caller renders the exact prompt, so its token count is reproducible ----
    def generate_raw(self, prompt: str, *, temperature: float = 0, max_tokens: int = 512) -> dict:
        """One completion of an already-rendered prompt. Returns content plus the model's own
        ``prompt_eval_count`` (tokens the model's tokenizer produced for the prompt)."""
        if not self._model:
            raise ModelUnavailable("No local model is configured")
        self._check_endpoint()
        try:
            with httpx.Client(timeout=self._timeout, trust_env=False, follow_redirects=False) as client:
                r = client.post(f"{self._url}/api/generate", json={
                    "model": self._model, "raw": True, "stream": False, "prompt": prompt,
                    "options": {"temperature": temperature, "num_predict": max_tokens, "seed": 7}})
                _reject_redirect(r)
                r.raise_for_status()
                d = r.json()
                return {"content": d["response"], "prompt_tokens": d.get("prompt_eval_count"),
                        "output_tokens": d.get("eval_count")}
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            raise ModelUnavailable(f"Local model request failed: {type(exc).__name__}") from exc

    def stream_raw(self, prompt: str, *, temperature: float = 0, max_tokens: int = 512) -> Iterator[str]:
        """Real token streaming from the model. Closing the generator closes the HTTP stream, which
        stops generation server-side (cancellation cleanup)."""
        if not self._model:
            raise ModelUnavailable("No local model is configured")
        self._check_endpoint()
        try:
            with httpx.Client(timeout=self._timeout, trust_env=False, follow_redirects=False) as client:
                with client.stream("POST", f"{self._url}/api/generate", json={
                        "model": self._model, "raw": True, "stream": True, "prompt": prompt,
                        "options": {"temperature": temperature, "num_predict": max_tokens, "seed": 7}}) as r:
                    _reject_redirect(r)
                    r.raise_for_status()
                    for line in r.iter_lines():
                        if not line:
                            continue
                        d = json.loads(line)
                        if d.get("response"):
                            yield d["response"]
                        if d.get("done"):
                            return
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            raise ModelUnavailable(f"Local model request failed: {type(exc).__name__}") from exc

    def count_tokens(self, text: str) -> int:
        """Exact token count with the served model's own tokenizer (raw prompt evaluation)."""
        return int(self.generate_raw(text, max_tokens=1)["prompt_tokens"] or 0)

    def model_info(self) -> dict:
        """Context length, tokenizer family and digest of the served model."""
        if not self._model:
            raise ModelUnavailable("No local model is configured")
        self._check_endpoint()
        try:
            with httpx.Client(timeout=self._timeout, trust_env=False, follow_redirects=False) as client:
                r = client.post(f"{self._url}/api/show", json={"model": self._model})
                _reject_redirect(r)
                r.raise_for_status()
                d = r.json()
                tags_response = client.get(f"{self._url}/api/tags")
                _reject_redirect(tags_response)
                tags = tags_response.json().get("models", [])
        except (httpx.HTTPError, ValueError) as exc:
            raise ModelUnavailable(f"Local model request failed: {type(exc).__name__}") from exc
        info = d.get("model_info", {})
        ctx = next((v for k, v in info.items() if k.endswith(".context_length")), None)
        digest = next((t.get("digest") for t in tags if t.get("name", "").split(":")[0] == self._model.split(":")[0]),
                      None)
        return {"context_length": ctx, "tokenizer": info.get("tokenizer.ggml.model"), "digest": digest}

    def health(self) -> bool:
        if not self._model:
            return False
        try:
            self._check_endpoint()
        except ModelUnavailable:
            return False
        try:
            with httpx.Client(timeout=min(self._timeout, 5), trust_env=False, follow_redirects=False) as client:
                response = client.get(f"{self._url}/api/tags")
                return response.status_code == 200
        except httpx.HTTPError:
            return False


def create_model_provider(
    model: str | None = None,
    url: str | None = None,
    timeout: float = 90.0,
    profile: str | None = None,
) -> LocalModelProvider:
    """Shared factory for the hardened local model provider (CC3-001).

    Every live call site (API admin status, NLQ planning, retrieval synthesis) constructs
    the provider here so endpoint validation, the local profile, redirect refusal and
    DNS-rebinding checks apply uniformly.
    """
    return LocalModelProvider(model=model, url=url, timeout=timeout, profile=profile)


class ModelUnavailable(Exception):
    pass
