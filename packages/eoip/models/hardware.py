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

#: Reference configurations are deployment data (D-SR-LLM-005-01): deploy/hardware/llm-reference-configs.json
CONFIG_PATH = Path(__file__).resolve().parents[3] / "deploy" / "hardware" / "llm-reference-configs.json"
_DATA = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

#: bytes per parameter for each supported weight format
QUANTIZATION: dict[str, dict[str, Any]] = _DATA["quantization"]
KV_GB_PER_1K_TOKENS_PER_B_PARAMS = float(_DATA["sizing"]["kv_gb_per_1k_tokens_per_b_params"])
RUNTIME_OVERHEAD = float(_DATA["sizing"]["runtime_overhead"])
RUNTIME_FIXED_GB = float(_DATA["sizing"]["runtime_fixed_gb"])


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


REFERENCE_CONFIGS: dict[str, ReferenceConfig] = {
    c["id"]: ReferenceConfig(**{**c, "quantizations": tuple(c["quantizations"])}) for c in _DATA["configs"]}


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
