"""Embedding service (SR-LLM-007, feeds SR-VDB-005 re-embedding).

* Model versioning: every vector is stored with the ``(model, version)`` that produced it; queries
  are embedded with the active version for the content kind, and only same-version vectors match.
* Online mode (``embed``) and batch mode (``submit_batch`` + ``run_batch`` in chunks).
* Content kinds: ``text`` (English), ``multilingual`` and ``code`` - each kind routes to the model
  registered for it; ``kind="auto"`` detects code and non-English text.
* Re-embedding jobs: activating a new version for a kind creates a resumable job that re-embeds
  every stored vector of that kind still on an old version, in bounded chunks.
"""

from __future__ import annotations

import math
import re
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

KINDS = ("text", "multilingual", "code")
_CODE_HINT = re.compile(r"(\bdef \w+\(|\bclass \w+[:(]|\bfunction \w+\(|[;{}]\s*$|^\s*(import|from|#include)\b)",
                        re.MULTILINE)


def detect_kind(text: str) -> str:
    if _CODE_HINT.search(text):
        return "code"
    letters = [c for c in text if c.isalpha()]
    if letters and sum(not c.isascii() for c in letters) / len(letters) > 0.3:
        return "multilingual"
    return "text"


@dataclass(frozen=True)
class EmbeddingModel:
    name: str
    version: str
    kind: str
    dim: int
    embed: Callable[[list[str]], list[list[float]]]


@dataclass
class StoredVector:
    doc_id: str
    text: str
    kind: str
    model: str
    version: str
    vector: list[float]


@dataclass
class Job:
    job_id: str
    kind: str  # batch | reembed
    pending: list[str]
    done: int = 0
    status: str = "queued"
    target: tuple[str, str] | None = None
    errors: list[str] = field(default_factory=list)


class EmbeddingService:
    def __init__(self, *, chunk_size: int = 64) -> None:
        self.models: dict[tuple[str, str], EmbeddingModel] = {}
        self.active: dict[str, tuple[str, str]] = {}
        self.store: dict[str, StoredVector] = {}
        self.jobs: dict[str, Job] = {}
        self.chunk_size = chunk_size
        self._batch_inputs: dict[str, dict[str, tuple[str, str]]] = {}

    def register(self, model: EmbeddingModel) -> None:
        if model.kind not in KINDS:
            raise ValueError(f"unknown kind {model.kind}")
        self.models[(model.name, model.version)] = model

    def activate(self, name: str, version: str) -> Job | None:
        """Make a version active for its kind; returns the re-embedding job if old vectors exist."""
        model = self.models[(name, version)]
        self.active[model.kind] = (name, version)
        stale = [d for d, v in self.store.items() if v.kind == model.kind and (v.model, v.version) != (name, version)]
        if not stale:
            return None
        job = Job(job_id=str(uuid.uuid4()), kind="reembed", pending=stale, target=(name, version))
        self.jobs[job.job_id] = job
        return job

    def _model_for(self, kind: str) -> EmbeddingModel:
        if kind not in self.active:
            if kind == "multilingual" and "text" in self.active:
                raise LookupError("no multilingual model is active; refusing to embed non-English text with an "
                                  "English-only model")
            raise LookupError(f"no active embedding model for kind {kind}")
        return self.models[self.active[kind]]

    def embed(self, texts: list[str], *, kind: str = "auto") -> list[dict[str, Any]]:
        """Online mode: returns vectors tagged with the model/version that produced them."""
        out = []
        for text in texts:
            k = detect_kind(text) if kind == "auto" else kind
            m = self._model_for(k)
            vec = m.embed([text])[0]
            if len(vec) != m.dim:
                raise ValueError(f"model {m.name}@{m.version} returned dim {len(vec)} != {m.dim}")
            out.append({"kind": k, "model": m.name, "version": m.version, "vector": vec})
        return out

    def upsert(self, doc_id: str, text: str, *, kind: str = "auto") -> StoredVector:
        e = self.embed([text], kind=kind)[0]
        sv = StoredVector(doc_id, text, e["kind"], e["model"], e["version"], e["vector"])
        self.store[doc_id] = sv
        return sv

    def submit_batch(self, items: dict[str, str], *, kind: str = "auto") -> Job:
        job = Job(job_id=str(uuid.uuid4()), kind="batch", pending=list(items))
        self._batch_inputs[job.job_id] = {d: (t, kind) for d, t in items.items()}
        self.jobs[job.job_id] = job
        return job

    def run_job(self, job_id: str, *, max_chunks: int | None = None) -> Job:
        """Process a batch or re-embed job chunk by chunk; resumable (call again to continue)."""
        job = self.jobs[job_id]
        job.status = "running"
        chunks = 0
        while job.pending and (max_chunks is None or chunks < max_chunks):
            chunk, job.pending = job.pending[: self.chunk_size], job.pending[self.chunk_size:]
            if job.kind == "batch":
                inputs = self._batch_inputs[job_id]
                for doc_id in chunk:
                    text, kind = inputs[doc_id]
                    self.upsert(doc_id, text, kind=kind)
            else:
                model = self.models[job.target]
                docs = [self.store[d] for d in chunk if d in self.store]
                vectors = model.embed([d.text for d in docs])
                for d, vec in zip(docs, vectors, strict=True):
                    self.store[d.doc_id] = StoredVector(d.doc_id, d.text, d.kind, model.name, model.version, vec)
            job.done += len(chunk)
            chunks += 1
        job.status = "done" if not job.pending else "paused"
        return job

    def search(self, query: str, *, kind: str = "auto", k: int = 5) -> list[tuple[str, float]]:
        """Only vectors from the query's model version are comparable."""
        q = self.embed([query], kind=kind)[0]
        scored = []
        for v in self.store.values():
            if (v.model, v.version) != (q["model"], q["version"]):
                continue
            dot = sum(a * b for a, b in zip(q["vector"], v.vector, strict=True))
            norm = math.sqrt(sum(a * a for a in q["vector"])) * math.sqrt(sum(b * b for b in v.vector)) or 1.0
            scored.append((v.doc_id, dot / norm))
        return sorted(scored, key=lambda x: -x[1])[:k]
