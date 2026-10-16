# EOIP-1 requirement trace

`service.py` implements EOIP-1. `compute_impact` calls `normalize`, which uses
the Python math module. EOIP-2 requires the path to retain source evidence.

This tiny repository is ingested by EOIP's local Git/code graph path to prove the
end-to-end requirement-to-code story: work item -> commit/file/symbol -> impact
and evidence. It is intentionally small so tests and the VS Code extension can
exercise symbol ranges, provenance, and safe workspace-relative navigation
without relying on external repositories.

The same ingested facts can now be cited by evidence-addressable GraphRAG,
exported through the JSON-LD/RDF/SHACL adapter, and included in semantic
federation plans when the local graph source is queried. This repository remains
a local fixture and is never treated as production code unless a user explicitly
ingests it into a selected environment.
