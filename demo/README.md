# Synthetic Demonstrations

All demonstration organizations, records, timings and outcomes are synthetic unless an individual artifact explicitly states otherwise. Never load the corpus into a customer deployment merely to make a readiness screen green.

| Area | Purpose |
|---|---|
| [autodemo](autodemo/README.md) | Browser/VS Code/Hubble presentations, launchers and receipts |
| [core demo repository](demodata/core/demo-repo/README.md) | Tiny ingested source repository for requirement-to-code traceability |
| [enterprise](demodata/enterprise/README.md) | Northstar scenario pack, source fixtures, project code and linked documents |
| [manual](demodata/manual/README.md) | Meridian PAY manual-ingestion JSON fixtures |
| [pipelines](demodata/pipelines/README.md) | Meridian FRD batch/pipeline JSON fixtures, not live upstream polling |
| [code](demodata/code/README.md) | Code-as-JSON representations, not a full compiler/code parser evaluation |
| [crawler](demodata/crawler/README.md) | Captured-page-shaped fixtures, not live network crawling qualification |

The worker may automatically enqueue demo loading when `EOIP_LOAD_DEMO=true`; disable it explicitly for non-demo environments. The container helpers also expose additive loading. Read [operations](../docs/operations-runbook.md) before any reset, restore or replay.

Demo success proves only the executed scenario/profile. Model routing is not model inference; fixture ingestion is not vendor qualification; proposal display is not external-effect execution. Inspect uncovered-operation lists and real receipts.

When fixtures change, preserve canonical IDs unless intentionally migrating them, validate schemas, check relationship endpoints and update scenario expectations. A README inside an ingested fixture repository is itself source data and changes its captured content/hash. Keep fixture maintenance distinct from ordinary guide cleanup.
