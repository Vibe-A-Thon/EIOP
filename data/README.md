# Data Assets

`manifest.json`, `ontology/` and `seed/` contain checked-in data inputs. `autodemo/raw/` contains historical captured demo records; do not confuse them with the active `EOIP_DATA_DIR` of a running deployment.

Loading behavior is owned by the actual loader and configuration, not by a file's presence. Confirm schema, dataset version, canonical IDs, provenance and destination before ingestion. Use synthetic or explicitly authorized data in tests.

Do not place private customer exports, credentials, new runtime checkpoints or ad hoc backups here. Runtime state belongs in the configured private data root; release evidence belongs in controlled artifact storage. Preserve historical capture provenance and do not edit it to manufacture successful results.

See [demo guide](../demo/README.md), [configuration](../docs/configuration-reference.md) and [operations](../docs/operations-runbook.md).
