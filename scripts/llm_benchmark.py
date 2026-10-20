"""Measure an Ollama-served model on this host and record it for a release (SR-LLM-005).

Usage: python scripts/llm_benchmark.py --release 1.4.0 --config cpu-small --model llama3.2:3b \
           --quantization q4_k_m [--url http://localhost:11434] [--requests 20]
Run once per reference configuration on that hardware; the release gate is
``eoip.models.hardware.release_benchmark_gate``.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "packages"))

from eoip.models.hardware import append_release_benchmark, run_benchmark  # noqa: E402

PROMPTS = [
    "List the owners of the billing service as JSON.",
    "Summarise in two sentences: the payments API depends on the ledger database.",
    "Extract entities from: 'Team Red deploys the checkout service to us-east-1.'",
    "Classify the intent of: 'who approved the last change to auth?'",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--quantization", required=True)
    ap.add_argument("--url", default="http://localhost:11434")
    ap.add_argument("--requests", type=int, default=20)
    ap.add_argument("--out", default="benchmarks/llm/releases.jsonl")
    a = ap.parse_args()

    def invoke(prompt: str):
        body = json.dumps({"model": a.model, "prompt": prompt, "stream": False,
                           "options": {"temperature": 0, "num_predict": 128}}).encode()
        req = urllib.request.Request(f"{a.url}/api/generate", data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        return data.get("response", ""), int(data.get("eval_count", 0))

    prompts = [PROMPTS[i % len(PROMPTS)] for i in range(a.requests)]
    rec = run_benchmark(invoke, prompts, release=a.release, config_id=a.config, model=a.model,
                        quantization=a.quantization)
    append_release_benchmark(Path(a.out), rec)
    print(json.dumps({"config": rec.config_id, "p50_ms": rec.latency_ms_p50, "p95_ms": rec.latency_ms_p95,
                      "tokens_per_second": rec.tokens_per_second, "failures": rec.failures}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
