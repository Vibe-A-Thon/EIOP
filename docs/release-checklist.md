# Release Checklist and Evidence Gate

Last documentation review: 2026-10-18. **No release is certified by this file.** Previous unbound `PASSED` entries have been removed. The gates below are requirements to verify against the exact release artifact/profile, not execution results from this documentation refresh.

## Release Identity and Evidence

Record immutable commit/artifact digests, dirty-source fingerprint when applicable, operating system/hardware, dependency/configuration profile, dataset/source identity, UTC time, exact command, process exit, logs and structured results. Keep credentials and private source data out of public evidence. Reference durable controlled artifacts and independent verification; `HEAD` and a local filename alone are insufficient.

Use the owning programme's exact status vocabulary. For this checklist, each gate remains **UNVERIFIED** until evidence is reviewed. An unavailable required environment is blocked, a failing execution is failed, and a skipped test is not a pass. Preserve earlier failures and historical receipts without rewriting them.

## Required Gate Matrix

| Gate | Scope | Required verification | Current certification |
|---|---|---|---|
| REL-01 | Checklist completeness | Required IDs and evidence procedure present; this is only a document-structure check | UNVERIFIED |
| REL-02 | Regression and builds | Applicable Python suite, default web type/unit/build, affected alternate frontend and distribution builds | UNVERIFIED |
| REL-03 | Requirement coverage | Registry/coverage reconciliation plus actual acceptance evidence, not literal-ID counts | UNVERIFIED |
| REL-04 | Product capability | Real registered behavior and unavailable-capability refusal; scanner output alone is insufficient | UNVERIFIED |
| REL-05 | Documentation | Fresh inventory, reviewed current guides, explicit exclusions and correct commands | UNVERIFIED |
| REL-06 | Live connectors | Authorized vendor sandbox credentials, pagination/cursors, retries, ingestion and independent reconciliation | UNVERIFIED |
| REL-07 | Graph/Hubble | Actual selected backend, authenticated graph/schema/visualization and source-bound results | UNVERIFIED |
| REL-08 | Browser workflows | Built app with real backend, authorization, errors, accessibility and visual inspection | UNVERIFIED |
| REL-09 | VS Code | Extension-host checks plus supported live profile and separately tested packaged VSIX | UNVERIFIED |
| REL-10 | HA/recovery | Profile-specific failover, interrupted writes, replay safety and isolated restore with measured recovery | UNVERIFIED |
| REL-11 | Security | Applicable authentication/tenant/egress/injection tests, dependency and secret review, deployment hardening | UNVERIFIED |
| REL-12 | Performance | Owning workload/budget on declared hardware, datasets, concurrency and raw percentile evidence | UNVERIFIED |
| REL-13 | Documentation links | Scoped local path checks with exclusions and remaining failures explicitly reported | UNVERIFIED |
| REL-14 | End-to-end demo | Live source-to-graph-to-client journey with bounded coverage and independent results | UNVERIFIED |
| REL-15 | Closeout | Reconcile current scoped requirements and evidence; release approval/tag is a separate authorized action | UNVERIFIED |
| MVP-FR-028 | Cross-domain traceability | Actual evidence-backed source/work/code/CI/document path for the declared profile | UNVERIFIED |
| CG-GAP-008 | External receipts | Verify all required live/external receipts and reject missing, stale or tampered evidence | UNVERIFIED |

## Commands and Their Limits

These are starting points, not a pre-certified release pipeline. Run from repository root with the required dependencies/services.

```powershell
python -m eoip.verification.release_gate --checklist
python -m scripts.build_requirements_registry --check
python -m pytest tests/unit/test_qa_gate_integrity.py -q
npm --prefix apps/web run typecheck
npm --prefix apps/web run test:unit
npm --prefix apps/web run build
python -m scripts.repository_inventory
python scripts/check_markdown_links.py
```

Use [Testing Guide](testing-guide.md), [Deployment](../deploy/README.md) and [Operations](operations-runbook.md) to select actual integration, browser, connector, recovery and offline commands. Some checks mutate demo/test state or require downloads. Use isolated profiles. Main CI and local component tests are not a substitute for every supported release profile.

## Known Verifier Limitations

Source inspection of `packages/eoip/verification/release_gate.py` shows that its CLI currently wires `--checklist` to a document/ID-presence check. Although `--evaluate` and `--output` are parsed, the current `main()` does not execute a full gate evaluation or write that requested output. Do not interpret a zero exit from those paths as full release verification.

Previously documented `--verify-connectors`, `--verify-hubble`, `--reconcile` and `--aggregate` are not registered CLI options. Some Python receipt helpers accept supplied measurements/booleans and defaults rather than independently collecting live evidence. Those helpers and their unit tests do not certify a vendor deployment or completed backlog.

Full independent release verification remains implementation/qualification work. Do not restore unsupported pass claims to make this document agree with a permissive helper.

## Release Approval Checklist

1. Select the supported app/API/MCP/extension, database, dependency and deployment versions.
2. Verify installation, configuration, secrets, identity and exact tenant/data boundaries.
3. Run relevant component checks, then real integration and independent-effect checks.
4. Exercise fresh install, upgrade, interrupted work, rollback/recovery and optional-module absence.
5. Reconcile every scoped requirement with current evidence; retain unknown/blocked items visibly.
6. Review first-party terms, third-party notices, bundled native/model assets and unresolved distribution issues.
7. Retain the reviewed evidence manifest and approval in durable controlled storage.
8. Create/sign/publish the release only through the owner's approved release process.

A successful demo, a populated ledger or a stated count such as 516 closed tasks is not a substitute for this process. Do not tag or publish a release merely because this documentation has been updated.
