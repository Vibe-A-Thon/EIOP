"""SR-LLM-005 cpu-small reference measurement: a real CPU-only run of a small local model through the
benchmark harness, recorded per release. Runs in the CI job llm-cpu-reference (EOIP_LIVE_OLLAMA_MODEL)."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from eoip.models.hardware import REFERENCE_CONFIGS, append_release_benchmark, release_benchmark_gate, run_benchmark
from eoip.models.provider import LocalModelProvider

MODEL = os.getenv("EOIP_LIVE_OLLAMA_MODEL", "")
pytestmark = [pytest.mark.req("SR-LLM-005"),
              pytest.mark.skipif(not MODEL, reason="no live local model (set EOIP_LIVE_OLLAMA_MODEL)")]


def test_cpu_small_reference_benchmark_is_measured_and_recorded_for_the_release():
    provider = LocalModelProvider(model=MODEL, url=os.getenv("EOIP_LIVE_OLLAMA_URL", "http://localhost:11434"),
                                  timeout=120)
    release = os.getenv("EOIP_RELEASE_ID", "dev")

    def invoke(prompt):
        out = provider.generate_raw(f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n", max_tokens=48)
        return out["content"], int(out["output_tokens"] or 0)

    prompts = ["List the owners of the billing service as JSON.",
               "Summarise: the payments API depends on the ledger database.",
               "Extract entities from: 'Team Red deploys checkout to us-east-1.'",
               "Classify the intent of: 'who approved the last change to auth?'"] * 3
    rec = run_benchmark(invoke, prompts, release=release, config_id="cpu-small", model=MODEL,
                        quantization="q4_k_m", warmup=2)
    assert rec.failures == 0 and rec.tokens_per_second > 0 and rec.latency_ms_p95 >= rec.latency_ms_p50 > 0
    assert rec.host["cpu_count"] and REFERENCE_CONFIGS["cpu-small"].gpus == 0
    out = Path(os.getenv("EOIP_BENCH_OUT", "test-results")) / "llm" / "releases.jsonl"
    append_release_benchmark(out, rec)
    gate = release_benchmark_gate(out, release, required_configs=("cpu-small",))
    assert gate["passed"] and gate["measured"]["cpu-small"]["tokens_per_second"] == rec.tokens_per_second
    # GPU and appliance configurations stay external: the full gate reports them missing
    assert set(release_benchmark_gate(out, release)["missing"]) == {"single-gpu", "multi-gpu", "airgap-appliance"}
