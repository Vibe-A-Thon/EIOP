# Generated Repository Inventory

`repository-inventory.json` is produced by `python -m scripts.repository_inventory --write` from the repository root. It records source HEAD, working-tree dirtiness, generation time, per-file hashes/line counts, explicit exclusions and Python AST discovery. It includes Git-listed nonignored untracked files as well as tracked files.

It is a mechanical content scan, not a complete semantic audit. JavaScript/TypeScript are read and hashed, not executed or semantically parsed. Python route candidates omit dynamic routes and router prefixes; use actual deployed OpenAPI for HTTP contracts. Binary files are hashed only. Secrets, runtime/dependency directories, symlinks and oversized files are not read; exclusions remain visible.

The inventory does not emit source bodies, credential values or feature completion claims. It excludes its own output to avoid self-reference. Re-run after settled source/doc changes; do not treat the snapshot as live status or routinely commit timestamp-only churn.

The separate requirement-discovery audit under `EOIP-engg-doc-pkg/audits/generated/` has a different generator and semantics. See [documentation policy](../documentation-policy.md) and [review report](../documentation-review-2026-10-18.md).
