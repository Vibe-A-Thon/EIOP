"""Hardware reference configurations, sizing guidance and per-release LLM benchmarks (SR-LLM-005).

Four reference configurations (CPU-only small model, single GPU, multi GPU, air-gapped appliance)
with quantization options and a sizing estimator; a benchmark harness that measures throughput and
latency through any ModelPort adapter and appends one record per (release, configuration) to
``benchmarks/llm/releases.jsonl``; and a release gate that refuses a release whose benchmark set
is incomplete.

The sizing numbers are planning estimates (weights x bytes/parameter + GQA KV cache + runtime
overhead), not measurements. Measured numbers on each reference configuration come only from
running ``scripts/llm_benchmark.py`` on that hardware for the release.
"""
from __future__ import annotations

import json
import os
import platform
import statistics
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

#: bytes per parameter for each supported weight format
QUANTIZATION: dict[str, dict[str, Any]] = {
    "fp16": {"bytes_per_param": 2.0, "quality": "reference", "runtimes": ["vllm", "tgi", "ollama"]},
    "int8": {"bytes_per_param": 1.0, "quality": "near-reference", "runtimes": ["vllm", "tgi", "llama_cpp"]},
    "q5_k_m": {"bytes_per_param": 0.69, "quality": "small loss", "runtimes": ["llama_cpp", "ollama"]},
    "q4_k_m": {"bytes_per_param": 0.56, "quality": "moderate loss; default for CPU", "runtimes": ["llama_cpp", "ollama"]},
}

KV_GB_PER_1K_TOKENS_PER_B_PARAMS = 0.016  # grouped-query attention, fp16 KV cache
RUNTIME_OVERHEAD = 1.10
RUNTIME_FIXED_GB = 0.5


@dataclass(frozen=True)
class ReferenceConfig:
    id: str
    title: str
    cpu_cores: int
    ram_gb: int
    gpus: int
    gpu_vram_gb: int
    quantizations: tuple[str, ...]
    max_model_b: float  # largest model (billions of params) supported at the default quantization
    default_quantization: str
    runtime: str
    air_gapped: bool = False
    notes: str = ""

    @property
    def accelerator_gb(self) -> float:
        return self.gpus * self.gpu_vram_gb if self.gpus else self.ram_gb * 0.75  # leave RAM for the platform


REFERENCE_CONFIGS: dict[str, ReferenceConfig] = {c.id: c for c in (
    ReferenceConfig("cpu-small", "CPU-only small model", cpu_cores=16, ram_gb=64, gpus=0, gpu_vram_gb=0,
                    quantizations=("q4_k_m", "q5_k_m", "int8"), max_model_b=8, default_quantization="q4_k_m",
                    runtime="ollama", notes="3-8B instruct models; interactive NLQ planning and short synthesis"),
    ReferenceConfig("single-gpu", "Single GPU", cpu_cores=16, ram_gb=128, gpus=1, gpu_vram_gb=48,
                    quantizations=("fp16", "int8", "q5_k_m", "q4_k_m"), max_model_b=34, default_quantization="int8",
                    runtime="vllm", notes="up to ~34B at int8 or 70B at q4 with reduced context"),
    ReferenceConfig("multi-gpu", "Multi GPU (tensor parallel)", cpu_cores=64, ram_gb=512, gpus=4, gpu_vram_gb=80,
                    quantizations=("fp16", "int8"), max_model_b=120, default_quantization="fp16",
                    runtime="vllm", notes="70B-class fp16 with long context and high concurrency"),
    ReferenceConfig("airgap-appliance", "Air-gapped appliance", cpu_cores=32, ram_gb=256, gpus=1, gpu_vram_gb=24,
                    quantizations=("q4_k_m", "q5_k_m", "int8"), max_model_b=14, default_quantization="q5_k_m",
                    runtime="ollama", air_gapped=True,
                    notes="no egress; models installed from signed bundles (eoip.models.catalog)"),
)}


def estimate_memory_gb(params_b: float, quantization: str, *, context_tokens: int = 8192,
                       concurrency: int = 1) -> float:
    """Planning estimate of accelerator memory for one model replica."""
    if quantization not in QUANTIZATION:
        raise ValueError(f"unknown quantization {quantization!r}; supported: {sorted(QUANTIZATION)}")
    weights = params_b * QUANTIZATION[quantization]["bytes_per_param"]
    kv = KV_GB_PER_1K_TOKENS_PER_B_PARAMS * params_b * (context_tokens / 1000) * concurrency
    return round((weights + kv) * RUNTIME_OVERHEAD + RUNTIME_FIXED_GB, 2)


def recommend(params_b: float, *, context_tokens: int = 8192, concurrency: int = 1,
              air_gapped: bool = False) -> dict[str, Any]:
    """Smallest reference configuration (and best quantization) that fits the workload."""
    order = ["cpu-small", "airgap-appliance", "single-gpu", "multi-gpu"]
    for cid in order:
        cfg = REFERENCE_CONFIGS[cid]
        if air_gapped and not cfg.air_gapped:
            continue
        for quant in sorted(cfg.quantizations, key=lambda q: -QUANTIZATION[q]["bytes_per_param"]):
            need = estimate_memory_gb(params_b, quant, context_tokens=context_tokens, concurrency=concurrency)
            if need <= cfg.accelerator_gb:
                return {"config": cid, "quantization": quant, "estimated_gb": need,
                        "available_gb": cfg.accelerator_gb}
    return {"config": None, "reason": "no reference configuration fits; reduce context/concurrency or quantize"}


@dataclass
class BenchmarkRecord:
    release: str
    config_id: str
    model: str
    quantization: str
    requests: int
    warmup: int
    latency_ms_p50: float
    latency_ms_p95: float
    tokens_per_second: float
    failures: int
    host: dict[str, Any] = field(default_factory=dict)
    measured_at: float = field(default_factory=time.time)


def host_fingerprint() -> dict[str, Any]:
    return {"machine": platform.machine(), "system": platform.system(), "python": platform.python_version(),
            "cpu_count": os.cpu_count()}


def _percentile(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    k = max(0, min(len(ordered) - 1, round(pct / 100 * (len(ordered) - 1))))
    return round(ordered[k], 3)


def run_benchmark(invoke: Callable[[str], tuple[str, int]], prompts: list[str], *, release: str,
                  config_id: str, model: str, quantization: str, warmup: int = 2,
                  clock: Callable[[], float] = time.perf_counter) -> BenchmarkRecord:
    """``invoke(prompt) -> (text, tokens_out)``; warmup calls are excluded from the measurements."""
    if config_id not in REFERENCE_CONFIGS:
        raise ValueError(f"unknown reference configuration {config_id!r}")
    for p in prompts[:warmup]:
        invoke(p)
    latencies, tokens, failures, busy = [], 0, 0, 0.0
    for p in prompts:
        t0 = clock()
        try:
            _, n = invoke(p)
        except Exception:
            failures += 1
            continue
        dt = clock() - t0
        latencies.append(dt * 1000)
        tokens += n
        busy += dt
    if not latencies:
        raise RuntimeError("every benchmark request failed")
    return BenchmarkRecord(release=release, config_id=config_id, model=model, quantization=quantization,
                           requests=len(prompts), warmup=warmup, latency_ms_p50=_percentile(latencies, 50),
                           latency_ms_p95=_percentile(latencies, 95),
                           tokens_per_second=round(tokens / busy, 2) if busy else 0.0, failures=failures,
                           host=host_fingerprint())


def append_release_benchmark(path: Path, record: BenchmarkRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(record), sort_keys=True) + "\n")


def release_benchmark_gate(path: Path, release: str,
                           required_configs: tuple[str, ...] = tuple(REFERENCE_CONFIGS)) -> dict[str, Any]:
    """A release passes only when every required configuration has a benchmark record for it."""
    have: dict[str, dict] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                if rec.get("release") == release:
                    have[rec["config_id"]] = rec
    missing = [c for c in required_configs if c not in have]
    return {"release": release, "passed": not missing, "missing": missing,
            "measured": {c: {k: have[c][k] for k in ("latency_ms_p50", "latency_ms_p95", "tokens_per_second")}
                         for c in have}}
