# Tests and Qualification

The test suite covers unit, integration, security, semantic, runtime/recovery, neural and acceptance concerns. Test presence is not completion evidence. See [Testing Guide](../docs/testing-guide.md) for exact commands, optional dependencies, profile selection and evidence requirements.

## Bootstrap

`conftest.py` exposes repository/package paths to subprocesses and registers the pytest evidence plugin. `pyproject.toml` defines strict markers, test roots and default options. Install `.[dev]` first; add only the extras needed by your selected tests. Tests marked `slow` are not excluded automatically by the current default options.

```powershell
python -m pytest tests/unit/test_provenance.py -q
python -m pytest tests/unit/test_repository_inventory.py -q
```

Choose integration tests by required service/profile, not just by filename. Browser tests live primarily under `apps/web/tests`; extension-host tests live under `apps/vscode-extension/test`. Their fixtures and live-system requirements differ from Python unit tests.

## Adding Coverage

Test an observable owning boundary and relevant negative cases. Use real protocol/storage execution when the requirement demands it; use fixtures for component isolation without presenting them as live-vendor evidence. Durability changes need restart/interruption/replay tests. Authorization changes need cross-tenant and direct-object denial cases. Models need the programme's statistical and anti-stub probes.

Retain failures, skips and process exit codes honestly. Use `--run-evidence` and JUnit where suitable, then independently verify consequential effects. Do not loosen assertions or alter a requirement merely to produce green output.

## CI Sharding

CI runs `tests/unit` (EOIP CI) and the full Windows regression (Validation evidence) as parallel file-level shards. `eoip.verification.pytest_shard` acts only when `EOIP_TEST_SHARD=i/n` is set; each shard is an ordinary single-coordinator pytest run, so `--run-evidence` receipts stay valid per shard. The gate jobs (`test`, `regression`) run `scripts/ci/check_test_shards.py` over the shard manifests and fail unless every collected test file ran in exactly one shard with all of its tests. A shard that crashed before collecting fails the gate.

- Reproduce one shard locally: `EOIP_TEST_SHARD=2/4 python -m pytest tests/unit`.
- Rebalance after large test changes: `python scripts/ci/update_shard_weights.py test-results/*.xml` rewrites `tests/ci-shard-weights.json` (seconds per file). Weights affect balance only, never which tests run; new files get the median weight.
- Change the shard count by editing the matrix in the workflow (the `i/n` values and the shard list together).
- Keep parametrize ids deterministic (no `time.time()`, random or object reprs in ids). The gate warns about ids that differ between processes; such tests also cannot be quarantined or traced in receipts.

## Existing Fixture Dependency

`acceptance/test_baseline_facts.py` reads two tracked baseline files under `.audit-scratch/baseline/`. The directory is now ignored for new files, but tracked entries remain. Relocate those fixtures and update the test contract before removing all tracked scratch files. The documentation refresh does not delete or relocate them.
