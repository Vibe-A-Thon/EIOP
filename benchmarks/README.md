# Benchmark Profiles

`profiles/P0.yaml`, `P1.yaml` and `P2.yaml` describe declared workload/reference-compute profiles used by acceptance work. A profile file is an input, not a measurement or a capacity guarantee.

Before running a benchmark, read the owning requirement and harness, select the actual backend/model tier, install its optional dependencies and identify data/seed/version. Record hardware, OS, Python/native-library versions, thread/resource settings, dataset size, warmup, repetitions, concurrency and percentile definitions.

Retain raw measurements, failure/skip counts and the exact command/build identity. Report numerical correctness, performance and uncertainty separately. Do not compare runs with different datasets/hardware as equivalent or replace a missed budget with a new threshold without the required decision.

See [neural tier limits](../docs/install-neural.md), [testing](../docs/testing-guide.md), `scripts/benchmark.py`, `scripts/benchmark_data.py` and the relevant programme benchmark gates. The documented Windows N0 result is not a Linux/offline/GPU qualification.
