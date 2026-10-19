# Documentation Maintenance Policy

## Ownership and Authority

| Artifact | Responsibility |
|---|---|
| Root README | Product entry, current startup paths, repository map, limitations and links |
| Component README | Purpose, entry points, dependencies, configuration, commands, data/security boundaries and related tests |
| `docs/` guides | Cross-component procedures and current architecture |
| Requirements/plans | Normative behavior, dependencies and evidence gates; changes require the applicable decision process |
| Decision records | Context, alternatives, decision, acceptance and consequences |
| Generated inventories/audits | Reproducible snapshots with source identity, scope and exclusions; not proof of completion |
| Demo/research READMEs | Synthetic/reference-data purpose, loading and methodological limitations |

When code and a guide disagree, investigate the code and actual runtime, correct the guide and record any requirement gap. Do not weaken a normative requirement just because current code does not meet it. Keep archived audits historical rather than rewriting their outcomes.

## Every Behavior-Changing Pull Request

Update the owning component README and any affected setup/API/config/operations guide. Include exact working directory, prerequisites, environment variables by name, expected behavior, failure modes and data-loss warnings for commands. Link to the source of complex defaults rather than duplicating hundreds of values.

Maintain safe relative Markdown links. Do not embed credentials, private deployment URLs, raw customer records or personal access tokens. CLI snippets use disposable local values or environment variables, never a real token. Describe unavailable profiles explicitly.

Distinguish source inspection, executed component tests, live integration, independent verification and production qualification. Record dates/build profiles for measurements. Do not write timeless completion percentages or unqualified `PASSED` tables without fresh immutable evidence.

## Refresh and Validation

```powershell
python -m scripts.repository_inventory
python -m scripts.repository_inventory --write
python -m pytest tests/unit/test_repository_inventory.py -q
python scripts/check_markdown_links.py
```

The first inventory command prints counts only. `--write` regenerates `docs/generated/repository-inventory.json`. It inspects Git-listed tracked and nonignored untracked files, excludes potential secrets/runtime/dependency directories and itself, and records explicit exclusions. It reads text fully and discovers Python AST symbols/imports/route candidates without executing modules. It does not perform a complete semantic review or prove requirements implemented.

The existing link checker excludes the historical engineering package and has simple Markdown parsing; a successful run is not a check of remote URLs, all anchors, or every code path in prose. Review new/changed links separately and distinguish pre-existing failures from regressions. The older `scripts.documentation_audit` indexes requirement discovery leads and writes different artifacts under the engineering package; do not confuse it with a runtime verifier.

Regenerate inventories after changes are settled. Compare meaningful content rather than committing timestamp churn routinely. Never use inventory statistics to infer test completeness or production readiness.

## Component README Template

1. Purpose and explicit non-goals.
2. Entry points and neighboring components.
3. Installation/run commands and working directory.
4. Configuration and secret handling.
5. Persistence, permissions and external-effect boundaries.
6. Test commands and their coverage limitations.
7. Known unsupported profiles and troubleshooting links.
8. Change/migration procedure and owning requirements.

Keep detailed procedures in one maintained guide and link from component READMEs. This reduces contradictory setup instructions while keeping each directory understandable to a new maintainer.
