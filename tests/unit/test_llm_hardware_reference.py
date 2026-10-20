"""SR-LLM-005: hardware reference configurations, sizing, quantization and per-release benchmarks."""
from __future__ import annotations

import pytest

from eoip.models.hardware import (
    QUANTIZATION,
    REFERENCE_CONFIGS,
    append_release_benchmark,
    estimate_memory_gb,
    recommend,
    release_benchmark_gate,
    run_benchmark,
)
from eoip.models.port import Capability, ModelCapabilities, ModelRequest, in_process_adapter

pytestmark = pytest.mark.req("SR-LLM-005")


def test_four_reference_configurations_with_quantization_options():
    assert set(REFERENCE_CONFIGS) == {"cpu-small", "single-gpu", "multi-gpu", "airgap-appliance"}
    cpu = REFERENCE_CONFIGS["cpu-small"]
    assert cpu.gpus == 0 and cpu.default_quantization in cpu.quantizations
    assert REFERENCE_CONFIGS["multi-gpu"].gpus > 1 and REFERENCE_CONFIGS["single-gpu"].gpus == 1
    assert REFERENCE_CONFIGS["airgap-appliance"].air_gapped
    for cfg in REFERENCE_CONFIGS.values():
        assert set(cfg.quantizations) <= set(QUANTIZATION)
        # the advertised largest model actually fits at the default quantization with an 8k context
        assert estimate_memory_gb(cfg.max_model_b, cfg.default_quantization) <= cfg.accelerator_gb, cfg.id


def test_sizing_guidance():
    assert estimate_memory_gb(8, "q4_k_m") < estimate_memory_gb(8, "int8") < estimate_memory_gb(8, "fp16")
    assert estimate_memory_gb(8, "fp16", context_tokens=32768) > estimate_memory_gb(8, "fp16")
    assert recommend(3)["config"] == "cpu-small"
    assert recommend(70, context_tokens=32768, concurrency=2)["config"] == "multi-gpu"
    air = recommend(8, air_gapped=True)
    assert air["config"] == "airgap-appliance" and air["estimated_gb"] <= air["available_gb"]
    assert recommend(400, context_tokens=128000, concurrency=64)["config"] is None
    with pytest.raises(ValueError):
        estimate_memory_gb(8, "fp4-magic")


def test_benchmark_harness_through_model_port_and_release_gate(tmp_path):
    adapter = in_process_adapter("det", "llama_cpp", lambda req: f"ok:{req.input}",
                                 caps=ModelCapabilities(frozenset({Capability.CHAT}), context_length=4096))
    ticks = iter(range(100))

    def invoke(prompt):
        out = adapter.invoke(ModelRequest(task="chat", capability=Capability.CHAT, input=prompt))
        return out.output, 10

    rec = run_benchmark(invoke, ["a", "b", "c", "d"], release="9.9.0", config_id="cpu-small", model="det",
                        quantization="q4_k_m", warmup=1, clock=lambda: float(next(ticks)) / 10)
    assert rec.requests == 4 and rec.failures == 0
    assert rec.latency_ms_p50 == pytest.approx(100.0) and rec.tokens_per_second == pytest.approx(100.0)
    assert rec.host["cpu_count"]
    out = tmp_path / "releases.jsonl"
    append_release_benchmark(out, rec)
    gate = release_benchmark_gate(out, "9.9.0")
    assert not gate["passed"] and set(gate["missing"]) == {"single-gpu", "multi-gpu", "airgap-appliance"}
    for cid in gate["missing"]:
        rec.config_id = cid
        append_release_benchmark(out, rec)
    assert release_benchmark_gate(out, "9.9.0")["passed"]
    assert not release_benchmark_gate(out, "10.0.0")["passed"]
    with pytest.raises(ValueError):
        run_benchmark(invoke, ["a"], release="x", config_id="laptop", model="m", quantization="q4_k_m")
