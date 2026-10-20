"""Embedding service: versioning, online/batch, multilingual and code models, re-embedding (SR-LLM-007)."""

from __future__ import annotations

import pytest

from eoip.models.embedding_service import EmbeddingModel, EmbeddingService, detect_kind

pytestmark = pytest.mark.req("SR-LLM-007")


def fake(name, version, kind, seed):
    calls = []

    def embed(texts):
        calls.append(len(texts))
        return [[float(len(t) % 7 + seed), float(sum(map(ord, t)) % 11), float(seed)] for t in texts]
    m = EmbeddingModel(name=name, version=version, kind=kind, dim=3, embed=embed)
    return m, calls


def service(chunk=2):
    s = EmbeddingService(chunk_size=chunk)
    for m, _ in (fake("e5", "v1", "text", 1), fake("bge-m3", "v1", "multilingual", 2),
                 fake("codet5", "v1", "code", 3)):
        s.register(m)
        s.activate(m.name, m.version)
    return s


def test_kind_detection_routes_to_multilingual_and_code_models():
    assert detect_kind("def add(a, b):\n    return a + b") == "code"
    assert detect_kind("Объяснение отказа системы") == "multilingual"
    assert detect_kind("why did billing fail") == "text"
    s = service()
    got = s.embed(["why did billing fail", "Объяснение отказа", "import os"])
    assert [(g["kind"], g["model"]) for g in got] == [("text", "e5"), ("multilingual", "bge-m3"), ("code", "codet5")]
    assert all(g["version"] == "v1" and len(g["vector"]) == 3 for g in got)


def test_missing_multilingual_model_refuses_instead_of_silently_using_english():
    s = EmbeddingService()
    m, _ = fake("e5", "v1", "text", 1)
    s.register(m)
    s.activate("e5", "v1")
    with pytest.raises(LookupError, match="multilingual"):
        s.embed(["Объяснение отказа"])


def test_batch_mode_runs_in_resumable_chunks():
    s = service(chunk=2)
    job = s.submit_batch({f"d{i}": f"incident {i}" for i in range(5)})
    s.run_job(job.job_id, max_chunks=1)
    assert (job.status, job.done, len(s.store)) == ("paused", 2, 2)
    s.run_job(job.job_id)
    assert (job.status, job.done, len(s.store)) == ("done", 5, 5)


def test_new_version_creates_reembed_job_and_search_only_matches_same_version():
    s = service(chunk=2)
    for i in range(3):
        s.upsert(f"t{i}", f"billing incident {i}")
    s.upsert("c0", "def f(): pass")
    v2, calls = fake("e5", "v2", "text", 5)
    s.register(v2)
    job = s.activate("e5", "v2")
    assert sorted(job.pending) == ["t0", "t1", "t2"]  # code vectors untouched
    assert s.search("billing incident 1") == []  # old-version vectors are not comparable
    s.run_job(job.job_id, max_chunks=1)
    assert job.status == "paused" and len(s.search("billing incident 1")) == 2
    s.run_job(job.job_id)
    assert job.status == "done" and calls == [1, 2, 1, 1]  # query, chunk of 2, query, chunk of 1
    assert {v.version for v in s.store.values() if v.kind == "text"} == {"v2"}
    assert s.store["c0"].model == "codet5"
    assert s.activate("e5", "v2") is None  # nothing stale left
