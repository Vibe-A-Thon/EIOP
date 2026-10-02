"""Local model abstraction (FR-RAG-002).

Pluggable local model provider that wraps Ollama or compatible endpoints.
The system remains useful when the model is stopped.
"""

from __future__ import annotations

import json
import os
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

    def health(self) -> bool:
        if not self._model:
            return False
        try:
            with httpx.Client(timeout=5, trust_env=False) as client:
                response = client.get(f"{self._url}/api/tags")
                return response.status_code == 200
        except httpx.HTTPError:
            return False


class ModelUnavailable(Exception):
    pass
