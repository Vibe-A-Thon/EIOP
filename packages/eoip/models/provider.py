"""Local model abstraction (FR-RAG-002).

Pluggable local model provider that wraps Ollama or compatible endpoints.
The system remains useful when the model is stopped.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class ModelResponse:
    content: str
    model: str
    generation: str
    tokens_used: int | None = None


class LocalModelProvider:
    def __init__(
        self,
        model: str | None = None,
        url: str | None = None,
        timeout: float = 90.0,
    ) -> None:
        self._model = model or os.getenv("EOIP_OLLAMA_MODEL", "")
        self._url = url or os.getenv("EOIP_OLLAMA_URL", "http://local-model:11434")
        self._timeout = timeout

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

        try:
            with httpx.Client(timeout=self._timeout, trust_env=False) as client:
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
        try:
            with httpx.Client(timeout=self._timeout, trust_env=False) as client:
                r = client.post(f"{self._url}/api/generate", json={
                    "model": self._model, "raw": True, "stream": False, "prompt": prompt,
                    "options": {"temperature": temperature, "num_predict": max_tokens, "seed": 7}})
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
        try:
            with httpx.Client(timeout=self._timeout, trust_env=False) as client:
                with client.stream("POST", f"{self._url}/api/generate", json={
                        "model": self._model, "raw": True, "stream": True, "prompt": prompt,
                        "options": {"temperature": temperature, "num_predict": max_tokens, "seed": 7}}) as r:
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
        try:
            with httpx.Client(timeout=self._timeout, trust_env=False) as client:
                r = client.post(f"{self._url}/api/show", json={"model": self._model})
                r.raise_for_status()
                d = r.json()
                tags = client.get(f"{self._url}/api/tags").json().get("models", [])
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
            with httpx.Client(timeout=min(self._timeout, 5), trust_env=False) as client:
                response = client.get(f"{self._url}/api/tags")
                return response.status_code == 200
        except httpx.HTTPError:
            return False


class ModelUnavailable(Exception):
    pass
