# Audit scripts (implemented)

Python 3.10+ recommended. Optional: `pip install -r ../requirements.txt` for `jsonschema`.

Shared closure logic: `proof_policy.py` (**proof policy 1.1.0**).

| Script | Purpose |
|---|---|
| `parse_md_requirements.py` | Walk `.md`, extract REQ blocks / headings → `requirements_index.json` |
| `generate_traceability.py` | Search code for req ids/tokens → `traceability_matrix.csv` |
| `run_tests_and_map.py` | Run pytest/npm if present; map junit; `missing_tests.json` |
| `run_static_analysis.sh` | ruff/flake8/bandit/pip-audit/npm audit/gitleaks when installed |
| `generate_audit_report.py` | Build `audit_gaps_requirements.md` |
| `generate_tracker.py` | Emit `tracker_data.json` + standalone HTML with embedded data |
| `redact_sensitive.py` | Redact secrets/PII → out + log |
| `validate_evidence.py` | Schema + proof policy 1.1 enforcement |
| `update_audit_memory.py` | Merge evidence into `audit-memory.json` |
| `proof_policy.py` | Canonical status computation (importable) |

## CLI examples

```bash
python3 parse_md_requirements.py --root ../fixtures/sample-reqs --out /tmp/req.json --commit abcdef1 --csv /tmp/req.csv
python3 generate_traceability.py --repo-root ../fixtures/sample-reqs --requirements /tmp/req.json --out /tmp/trace.csv --commit abcdef1
python3 run_tests_and_map.py --repo-root ../fixtures/sample-reqs --requirements /tmp/req.json --out /tmp/test_results
./run_static_analysis.sh --repo-root ../fixtures/sample-reqs
python3 validate_evidence.py --schema ../schemas/evidence.schema.json --in ../examples/evidence.json --memory ../examples/audit-memory.json
python3 update_audit_memory.py --mode full --memory /tmp/mem.json --evidence ../examples/evidence.json --commit a1b2c3d4e5f6789012345678901234567890abcd --repo local
python3 generate_audit_report.py --requirements /tmp/req.json --traceability /tmp/trace.csv --evidence ../examples --out /tmp/report.md --commit abcdef1 --memory ../examples/audit-memory.json
python3 generate_tracker.py --evidence-json ../examples/evidence.json --audit-memory ../examples/audit-memory.json --out /tmp/tracker.html
python3 redact_sensitive.py --in sample.txt --out redacted.txt --log redaction.json
```

All scripts accept `--help`. They must not print secrets; `update_audit_memory` / `validate_evidence` refuse secret-like payloads.
