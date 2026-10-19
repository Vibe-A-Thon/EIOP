# Repository Scripts

Run Python modules from repository root after installing the appropriate project extras. A script filename is not a support guarantee; inspect its arguments and effects before execution.

## Supported Entry Points and Categories

| Scripts | Responsibility | Caution |
|---|---|---|
| `container.ps1`, `container.sh`, `docker.ps1` | Container lifecycle helpers | Builds, ingestion, credential changes and acceptance cleanup are action-specific |
| `detect_runtime.py` | Runtime discovery | Discovery is not a complete deployment check |
| `bootstrap_schema.py`, `setup_hubble.py` | Graph/admin initialization | Database/schema effects; require correct target and credentials |
| `backup.py`, `restore.py`, `verify_restore.py`, `verify_recovery_bundle.py` | Recovery utilities | Restore only into isolated empty targets after reviewing contracts |
| `load_demo_corpus.py`, `demo_reset.py` | Synthetic demo loading/reset | Reset/loading is not a read-only operation; use a dedicated environment |
| `smoke_test.py`, `verify_live_dlq.py`, `verify_seeded_gate.py` | Selected live verification | May create jobs/data and need an integrated stack |
| `build_requirements_registry.py`, `documentation_audit.py`, `gap_coverage.py` | Requirement discovery/reconciliation | References and literal IDs are not acceptance evidence |
| `repository_inventory.py` | Content-free static repository inventory | Full text reads/AST discovery, not semantic audit or runtime qualification |
| `check_markdown_links.py`, `audit_gui.mjs` | Documentation/UI intake checks | Scope and parsing limitations remain explicit |
| `verify_aspeii_evidence.py`, `verify_requirement_evidence.py` | Evidence validation helpers | Apply the owning programme's independent-verification rules |
| `benchmark.py`, `benchmark_data.py`, `rag_eval.py` | Measurement/evaluation | Record hardware, dataset, seeds and actual profile; no universal scale claims |

Many `batch_*`, `tick_*`, `update_*`, `_mark_*`, `_read_*`, `_inspect_*` and `list_*` files are historical one-off backlog/audit helpers. They can rewrite trackers or assume old document structures. They are not a production deployment pipeline and should not be run to manufacture completion.

## Documentation Refresh

```powershell
python -m scripts.repository_inventory
python -m scripts.repository_inventory --write
python -m pytest tests/unit/test_repository_inventory.py -q
python scripts/check_markdown_links.py
```

The generated inventory excludes potential credentials and runtime/dependency directories, records the exclusions, and does not execute inspected Python modules. See [policy](../docs/documentation-policy.md). Review any generated diff before committing; do not overwrite historical evidence to reflect a different run.
