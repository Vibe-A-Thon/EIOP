# Acceptance, Claims and Research Tools

These command-line helpers support evidence and research workflows; they are not part of the serving API. Run from repository root with the environment required by the command under test.

| Directory | Purpose |
|---|---|
| `acceptance/` | Execute a command, collect receipts, review receipts, seed/verify a ledger and validate declared schemas |
| `claims/` | Check the claims register against its policy |
| `research/` | Seed and validate competitive research records |

`acceptance/run_and_receipt.py` requires a clause, profile (`P0`, `P1` or `P2`), backend and a glob resolving to exactly one built artifact, then a command after `--`. It captures stdout/stderr, JUnit and source/artifact metadata under `.audit-scratch`. Read `--help` and its source before running it. Selecting an artifact is not enough: the test must actually exercise that artifact, and the independent verifier must establish that relationship.

Do not auto-approve your own receipts, replace missing evidence with booleans or seed a ledger to declare implementation complete. Keep raw evidence in durable controlled storage rather than only an ignored local directory. Follow the owning requirement plan and [testing guide](../docs/testing-guide.md).

Research tooling has different semantics from acceptance. A researched competitor capability, score or source citation is neither an EOIP implementation claim nor a benchmark result. Preserve dataset separation in [research datasets](../research/datasets/README.md).
