"""Embedding provider abstraction and Ollama integration (GAP-SEARCH-001/§7.3).

Defines the ``EmbeddingProvider`` port used by the retrieval vector index
together with an Ollama-backed implementation that calls Ollama's
``/api/embed`` endpoint. Provider failures degrade gracefully: callers can
fall back to the deterministic ``HashingEmbedder`` (see
``eoip.retrieval.vectors``) when a provider is unavailable, keeping search
functional without a running model.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Protocol, runtime_checkable

from eoip.models.provider import ModelUnavailable

_DEFAULT_OLLAMA_URL = "http://localhost:11434"
_DEFAULT_EMBED_MODEL = "nomic-embed-text"
_DEFAULT_TIMEOUT = 5.0


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Port for text embedding backends (GAP-SEARCH-001/§7.3)."""

    @property
    def dim(self) -> int:
        """Output vector dimension."""
        ...

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts into vectors of length ``dim``."""
        ...

    def health(self) -> bool:
        """Whether the backend is reachable and usable."""
        ...


class OllamaEmbeddingProvider:
    """EmbeddingProvider backed by Ollama's ``/api/embed`` endpoint.

    Configuration: ``EOIP_OLLAMA_URL`` (default ``http://localhost:11434``)
    and ``EOIP_OLLAMA_EMBED_MODEL`` (default ``nomic-embed-text``). Uses
    stdlib ``urllib`` only. All transport/parsing failures raise
    ``ModelUnavailable`` so callers can fall back to hashing embeddings.
    """

    def __init__(
        self,
        model: str | None = None,
        url: str | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        self._model = model or os.getenv("EOIP_OLLAMA_EMBED_MODEL", _DEFAULT_EMBED_MODEL)
        self._url = (url or os.getenv("EOIP_OLLAMA_URL", _DEFAULT_OLLAMA_URL)).rstrip("/")
        self._timeout = timeout
        self._dim: int | None = None

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def dim(self) -> int:
        """Vector dimension reported by the model (0 before first embed)."""
        return self._dim or 0

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        payload = json.dumps({"model": self._model, "input": list(texts)}).encode("utf-8")
        request = urllib.request.Request(
            f"{self._url}/api/embed",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise ModelUnavailable(
                f"Embedding request failed: {type(exc).__name__}"
            ) from exc
        embeddings = data.get("embeddings")
        if not isinstance(embeddings, list) or not embeddings:
            raise ModelUnavailable("Embedding response missing 'embeddings'")
        vectors: list[list[float]] = []
        for row in embeddings:
            if not isinstance(row, list):
                raise ModelUnavailable("Embedding response contains non-numeric row")
            vectors.append([float(v) for v in row])
        if any(len(v) != len(vectors[0]) for v in vectors):
            raise ModelUnavailable("Embedding response has inconsistent dimensions")
        self._dim = len(vectors[0])
        return vectors

    def embed_one(self, text: str) -> list[float]:
        """Embed a single text; convenience for single-text consumers."""
        return self.embed([text])[0]

    def health(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self._url}/api/tags", timeout=min(self._timeout, 5)):
                return True
        except (urllib.error.URLError, TimeoutError, OSError):
            return False


class SentenceTransformersEmbeddingProvider:
    """EmbeddingProvider backed by local sentence-transformers models (H-02)."""

    def __init__(self, model_name: str | None = None) -> None:
        self._model_name = model_name or os.getenv("EOIP_SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")
        self._model = None
        self._dim = 384

    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self._model_name)
                dim = getattr(self._model, "get_sentence_embedding_dimension", None)
                if callable(dim):
                    self._dim = int(dim())
            except Exception as exc:
                raise ModelUnavailable(f"sentence-transformers failed to load: {exc}") from exc
        return self._model

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dim(self) -> int:
        return self._dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        model = self._get_model()
        vecs = model.encode(texts, convert_to_numpy=True).tolist()
        return [[float(x) for x in v] for v in vecs]

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]

    def health(self) -> bool:
        try:
            self._get_model()
            return True
        except Exception:
            return False


def build_embedding_provider() -> EmbeddingProvider | None:
    """Construct an embedding provider from the environment (H-02, GAP-SEARCH-001).

    Checks for:
    1. EOIP_SENTENCE_TRANSFORMER_MODEL or EOIP_EMBEDDING_PROVIDER == 'sentence-transformers'
    2. EOIP_OLLAMA_EMBED_MODEL (defaults to Ollama)
    Returns None when no provider is explicitly enabled, falling back to local deterministic embeddings.
    """
    provider_type = os.getenv("EOIP_EMBEDDING_PROVIDER", "").lower()
    if provider_type == "sentence-transformers" or os.getenv("EOIP_SENTENCE_TRANSFORMER_MODEL"):
        return SentenceTransformersEmbeddingProvider()
    if os.getenv("EOIP_OLLAMA_EMBED_MODEL") or provider_type == "ollama":
        return OllamaEmbeddingProvider()
    return None

