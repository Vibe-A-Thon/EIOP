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

## Existing Fixture Dependency

`acceptance/test_baseline_facts.py` reads two tracked baseline files under `.audit-scratch/baseline/`. The directory is now ignored for new files, but tracked entries remain. Relocate those fixtures and update the test contract before removing all tracked scratch files. The documentation refresh does not delete or relocate them.
