"""CRA-026: retrieval synthesis runs through the evidence-bound GraphRAG pipeline with a cited-span
claim-support check (unsupported generated statements are removed and reported). The live case runs against
the local CPU reference model when EOIP_LIVE_OLLAMA_MODEL is set (CI job llm-cpu-reference)."""
from __future__ import annotations

import os

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.retrieval import service as svc
from eoip.retrieval.service import retrieve

pytestmark = pytest.mark.req("CRA-026")


def _store():
    store = MemoryGraphStore()
    issue = store.upsert_vertex("WorkItem", {"canonical_id": "issue:1", "issue_key": "PAY-1",
                                             "summary": "Payments outage in region us-east-1",
                                             "description": "Payments outage caused by an expired TLS certificate"})
    commit = store.upsert_vertex("Commit", {"canonical_id": "commit:1", "commit_sha": "abc",
                                            "message": "Rotate the expired TLS certificate"})
    store.upsert_edge("IMPLEMENTS", commit["vid"], issue["vid"], {"source_ref": "git://demo/abc"})
    return store


class _FakeRuntime:
    """Deterministic stand-in with the runtime contract (model_info/count_tokens/generate_raw)."""

    available = True
    model_name = "fake-cpu"

    def __init__(self, content):
        self.content, self.prompts = content, []

    def model_info(self):
        return {"context_length": 4096, "tokenizer": "words", "digest": "sha256:feedface"}

    def count_tokens(self, text):
        return len(text.split())

    def generate_raw(self, prompt, max_tokens=256):
        self.prompts.append(prompt)
        return {"content": self.content, "prompt_tokens": len(prompt.split())}


def test_supported_sentence_kept_unsupported_removed(monkeypatch):
    runtime = _FakeRuntime("The outage was caused by an expired TLS certificate. It cost 4 million dollars.")
    monkeypatch.setattr(svc, "LocalModelProvider", lambda timeout=90.0: runtime)
    res = retrieve(_store(), "issue:1", "Why was there a payments outage?", synthesize=True)
    assert res.generation == "local_model"
    assert "expired TLS certificate" in res.answer and "4 million" not in res.answer
    assert any("removed" in w for w in res.warnings)
    cited = res.answer_citations
    assert cited and cited[0]["assertion_id"] == "issue:1"
    for c in cited:  # exact span of the evidence built from the cited graph entity's own properties
        assert c["evidence_text"][c["span"]["start"]:c["span"]["end"]] == c["span"]["text"]
    assert "expired TLS certificate" in cited[0]["span"]["text"] and res.answer.count("[issue:1]") == 1
    assert "<<<UNTRUSTED_DOCUMENT_CONTENT>>>" in runtime.prompts[0]  # context is fenced


def test_entirely_unsupported_generation_falls_back_to_cited_evidence(monkeypatch):
    monkeypatch.setattr(svc, "LocalModelProvider", lambda timeout=90.0: _FakeRuntime("Revenue grew in Europe."))
    res = retrieve(_store(), "issue:1", "Why was there a payments outage?", synthesize=True)
    assert res.generation == "extractive" and "Revenue" not in res.answer
    assert any("not supported" in w for w in res.warnings) and res.answer_citations


@pytest.mark.skipif(not os.getenv("EOIP_LIVE_OLLAMA_MODEL"), reason="no live local model")
def test_live_model_retrieval_answer_is_span_cited(monkeypatch):
    monkeypatch.setenv("EOIP_OLLAMA_MODEL", os.environ["EOIP_LIVE_OLLAMA_MODEL"])
    monkeypatch.setenv("EOIP_OLLAMA_URL", os.getenv("EOIP_LIVE_OLLAMA_URL", "http://127.0.0.1:11434"))
    res = retrieve(_store(), "issue:1", "What caused the payments outage?", synthesize=True, max_model_tokens=96)
    assert res.generation in ("local_model", "extractive") and res.answer_citations
    for c in res.answer_citations:
        assert c["evidence_text"][c["span"]["start"]:c["span"]["end"]] == c["span"]["text"]
        assert c["support_score"] >= 0.6 and c["assertion_id"]
