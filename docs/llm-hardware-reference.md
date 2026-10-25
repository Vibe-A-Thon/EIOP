# LLM hardware reference configurations (SR-LLM-005)

Source of truth: `deploy/hardware/llm-reference-configs.json` (loaded by `eoip.models.hardware`).

| Config | Hardware | Default quantization | Largest model | Runtime |
|---|---|---|---|---|
| `cpu-small` | 16 cores, 64 GB RAM, no GPU | q4_k_m | ~8B | Ollama |
| `single-gpu` | 16 cores, 128 GB RAM, 1x48 GB GPU | int8 | ~34B | vLLM |
| `multi-gpu` | 64 cores, 512 GB RAM, 4x80 GB GPU | fp16 | ~120B | vLLM (tensor parallel) |
| `airgap-appliance` | 32 cores, 256 GB RAM, 1x24 GB GPU, no egress | q5_k_m | ~14B | Ollama, signed bundles |

## Sizing

`estimate_memory_gb(params_b, quantization, context_tokens=, concurrency=)` is
`(params x bytes/param + GQA KV cache) x 1.10 + 0.5 GB`. `recommend(...)` picks the smallest
configuration and the highest-precision quantization that fit. These are planning estimates,
not measurements.

## Per-release benchmarks

On each reference configuration, for each release:

```
python scripts/llm_benchmark.py --release <version> --config <config-id> --model <model> --quantization <q>
```

This appends p50/p95 latency, tokens/s, failures and a host fingerprint to
`benchmarks/llm/releases.jsonl`. `release_benchmark_gate(path, release)` passes only when every
configuration has a record for that release. The repository's CI checks the harness and the gate;
the measured numbers have to come from the real hardware.
