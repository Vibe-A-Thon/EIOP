"""Reasoning strategies never pass off heuristic text as an LLM answer (AI-007).

When an LLM hook is configured and a call raises or returns nothing, the strategy substitutes its
heuristic text for that step and the result is marked ``mode="llm-degraded"`` with reasons. The live
tests drive the strategies with the local CPU reference model (Ollama), and with the same provider
pointed at a dead endpoint (CI job llm-cpu-reference; skipped without EOIP_LIVE_OLLAMA_MODEL).
"""
from __future__ import annotations

import os

import pytest

from eoip.models.provider import LocalModelProvider
from eoip.reasoning.memory import EpisodicMemory, HierarchicalMemory
from eoip.reasoning.strategies import ReasoningHooks, ReasoningProblem, default_registry

pytestmark = pytest.mark.req("AI-007")

PROBLEM = ReasoningProblem(prompt="Why did the nightly billing export fail?", max_steps=3,
                           candidate_actions=["check logs", "rerun export"], context={"tools": ["logs"]})
LLM_STRATEGIES = ["react", "tot", "got"]


def test_no_hook_is_labelled_deterministic():
    for name in LLM_STRATEGIES + ["best-first", "htn"]:
        res = default_registry().run(name, PROBLEM)
        assert res.mode == "deterministic" and not res.degraded and res.llm_calls == 0, name


@pytest.mark.parametrize("name", LLM_STRATEGIES)
def test_working_llm_is_labelled_llm(name):
    seen: list[str] = []
    hooks = ReasoningHooks(llm=lambda p: seen.append(p) or f"model says: {p[:20]}")
    res = default_registry().run(name, PROBLEM, hooks)
    assert res.mode == "llm" and not res.degraded and res.llm_calls == len(seen) > 0
    assert any("model says" in s.content for s in res.steps)


@pytest.mark.parametrize("name", LLM_STRATEGIES)
def test_failing_llm_marks_result_degraded_not_silent(name):
    def boom(_p: str) -> str:
        raise TimeoutError("model timed out")

    res = default_registry().run(name, PROBLEM, ReasoningHooks(llm=boom))
    assert res.degraded and res.mode == "llm-degraded" and res.llm_calls > 0
    assert res.degradation_reasons and all("TimeoutError" in r for r in res.degradation_reasons)


def test_partial_failure_and_empty_response_are_reported():
    calls = {"n": 0}

    def flaky(p: str) -> str:
        calls["n"] += 1
        return "" if calls["n"] == 2 else "ok answer"

    res = default_registry().run("react", PROBLEM, ReasoningHooks(llm=flaky))
    assert res.mode == "llm-degraded" and len(res.degradation_reasons) == 1
    assert "empty LLM response" in res.degradation_reasons[0]


def test_meta_strategy_propagates_inner_degradation():
    def boom(_p: str) -> str:
        raise RuntimeError("x")

    res = default_registry().select_and_run(PROBLEM, ReasoningHooks(llm=boom))
    assert res.strategy.startswith("meta->") and res.degraded


def test_memory_summarizer_failure_is_labelled():
    def bad(_texts):
        raise ConnectionError("summarizer down")

    mem = EpisodicMemory(consolidate_after=2, summarize=bad)
    for i in range(5):
        mem.record("event", f"episode {i}")
    mem.consolidate()
    eps = [e for e in mem.all() if e.consolidated]
    assert eps and all(e.summary_method == "truncation-degraded" for e in eps)
    assert mem.degradations and "ConnectionError" in mem.degradations[0]
    plain = EpisodicMemory(consolidate_after=2)
    for i in range(5):
        plain.record("event", f"e{i}")
    plain.consolidate()
    assert {e.summary_method for e in plain.all() if e.consolidated} == {"truncation"} and not plain.degradations
    h = HierarchicalMemory(l0_capacity=8, summarize=lambda b: "")
    for i in range(4):
        h.add_raw(f"item {i}")
    h.promote()
    assert h.last_summary_method == "truncation-degraded" and h.degradations == ["empty summary"]


# --------------------------------------------------------------------------- live (local CPU model)
MODEL = os.getenv("EOIP_LIVE_OLLAMA_MODEL", "")
URL = os.getenv("EOIP_LIVE_OLLAMA_URL", "http://localhost:11434")
live = pytest.mark.skipif(not MODEL, reason="no live local model (set EOIP_LIVE_OLLAMA_MODEL)")


def _hook(provider: LocalModelProvider):
    def llm(prompt: str) -> str:
        return provider.generate("You are a concise SRE assistant. Answer in one sentence.", prompt,
                                 max_tokens=48).content
    return ReasoningHooks(llm=llm)


@live
def test_live_model_drives_react_and_is_labelled_llm():
    res = default_registry().run("react", PROBLEM, _hook(LocalModelProvider(model=MODEL, url=URL, timeout=120)))
    assert res.mode == "llm" and not res.degraded and res.llm_calls >= 2


@live
def test_live_model_outage_is_reported_as_degraded():
    dead = LocalModelProvider(model=MODEL, url="http://127.0.0.1:9", timeout=2)
    res = default_registry().run("react", PROBLEM, _hook(dead))
    assert res.degraded and res.mode == "llm-degraded"
    assert all("ModelUnavailable" in r for r in res.degradation_reasons)
