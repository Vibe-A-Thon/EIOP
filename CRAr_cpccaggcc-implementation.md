# CRAr_cpccaggcc — Implementation and Integration Guide for EOIP / KnowGridFlow

| Field | Value |
|---|---|
| Document | `CRAr_cpccaggcc-implementation.md` |
| Implements | `CRAr_cpccaggcc-requirements.md` v3.0-COMBINED (42 requirements, all clauses `CRA-xxx.n`, acceptance obligations `CRA-xxx.A`) |
| Progress view | `CRAr_cpccaggcc-tracker.html` (imports/exports the ledger format of section 2) |
| Date | 2026-10-17 |
| Audience | Any AI coding agent or engineer implementing EOIP/KGF |

## 0. Rules That Override Everything Else in This Guide

1. **Proof is execution, not text.** A clause is complete only when the real implementation ran, produced a receipt (section 2.3) and an independent reviewer accepted it. File paths, class names, test names, routes, screenshots, commit messages, tracker states and this guide's checklists are never proof.
2. **No assumptions.** When this guide names an existing file or symbol, it is a *search lead* taken from the source analyses. Verify it exists at the pinned commit before relying on it (section 1.3). When something required is missing (credentials, sandbox, product identity, legal approval, human decision `H-xx`), do the safe local work, set the clause to `BLOCKED` or `UNQUALIFIED` in the ledger with the exact missing input, and continue with independent work.
3. **No silent substitution.** Never replace a real engine/provider/backend with a mock, hashing embedder, in-memory store, canned answer or feature flag to make a gate pass. Mocks are allowed only in tests labelled `mock` and never count toward VERIFIED.
4. **No scope reduction.** Every clause of every requirement stays in the ledger. Deferring is allowed only as a visible `DEFERRED` state with an owner.
5. **Never weaken a test to pass.** Changing expected values without an independent oracle, adding `skip`/`xfail`, widening tolerances or catching broad exceptions to turn red green is prohibited; the ledger verifier treats these as failures.
6. **Preserve the moat.** `packages/eoip/ontology/gitops.py`, `manifest.py` and `packs.py` are extended through ports only; any edit requires a recorded Lead Developer review (`CRA-022.6`).
7. **Respect authorization boundaries.** No production crawling, customer-data export, write-back, paid provisioning, publication of claims or disclosure of patent-candidate mechanisms without the gates in CRA-027, CRA-040 and CRA-041.
8. **Licensing.** Never link or bundle GPL/AGPL code into the distributed core; never relabel third-party files; never remove upstream notices (CRA-035).

## 1. Pre-Flight (do this before writing any production code)

### 1.1 Capture the baseline

```bash
git status --porcelain=v1 > .audit-scratch/baseline/git-status.txt
git rev-parse HEAD > .audit-scratch/baseline/head.txt
git ls-files -s | sha256sum > .audit-scratch/baseline/source-fingerprint.txt
python --version > .audit-scratch/baseline/python.txt
pip freeze > .audit-scratch/baseline/pip-freeze.txt
(cd apps/web 2>/dev/null || cd frontend 2>/dev/null; npm ls --all --json > ../.audit-scratch/baseline/npm-ls.json 2>/dev/null || true)
```

Create `.audit-scratch/` first and add it to `.gitignore` except for `ledger.json` and `receipts/` if the team wants them versioned (decision recorded in `docs/decisions/ADR-0001-evidence-storage.md`). If the working tree is dirty, do not stash or discard others' work: record it and continue; receipts from a dirty tree carry `source_tree_dirty: true` and cannot qualify a release.

### 1.2 Read before editing

Read completely: `CRAr_cpccaggcc-requirements.md`, this guide, `LICENSING.md`, `GUI-UIX-implementation-plan.md`, `GUI-UIX-audit-2026-10-16.md` and any existing CP/GUI requirement files. Do not infer completion from earlier audit labels.

### 1.3 Verify every search lead (re-measure, CRA-001.11)

Run and save outputs to `.audit-scratch/baseline/inventory/`:

```bash
# Python requirement and dependencies
grep -nE "requires-python|rdflib|pyshacl|owlready|fastapi|pydantic" pyproject.toml
# Package size and modules named by the sources
find packages -name "*.py" | wc -l
ls packages/eoip/ontology packages/eoip/connectors packages/eoip/fileparse packages/eoip/qlang packages/eoip/graph packages/eoip/contracts 2>&1
wc -l packages/eoip/ontology/*.py packages/eoip/connectors/factory.py
# Symbols named by the sources
grep -rn "def _bootstrap_core_axioms\|class OWLReasoner\|def is_subclass_of\|def export_shacl_shapes\|def jsonld_to_property_graph" packages/eoip/ontology
grep -rn "class SHACLValidator\|class SHACLShape\|min_counts\|max_counts\|def _check_datatype" packages/eoip/ontology
grep -rn "def compute_next_semver\|def generate_ontology_migration_script\|class RollbackReceipt\|def run_ontology_impact_analysis" packages/eoip/ontology
grep -rn "api/entities\|except Exception" packages/eoip/connectors/factory.py
grep -rn "_chunk_text" packages/eoip
grep -rn "class AutonomyLevel\|HCTL" packages/eoip
grep -rn "token_budget" packages/eoip | head
# Routes and tests
python - <<'PY'
import importlib, json
for mod in ("eoip.platform_router", "apps.api.main", "eoip.api"):
    try:
        m = importlib.import_module(mod)
        print(mod, "ok")
    except Exception as e:
        print(mod, "not importable:", type(e).__name__)
PY
find tests -name "test_*.py" | wc -l
```

For each asserted fact in requirements section 4.1 record `asserted`, `measured`, `match` in `.audit-scratch/baseline/facts.json`. A mismatch is data, not an error to "fix" in documents.

### 1.4 Reproduce the baseline defects (CRA-001.12)

Run the probe from requirements section 20 (`PYTHONPATH=.:packages` on Linux/macOS, `$env:PYTHONPATH='.;packages'` on Windows) and store raw stdout as `.audit-scratch/baseline/g01-g03-probe.txt`. Expected at baseline: zero violations, unknown datatype accepted, case-distinct subclass true. If the output differs, record it — do not assume the defect is fixed.

### 1.5 Establish the toolchain

- Python: the version in `pyproject.toml` (`>=3.11` per sources); create an isolated venv; install with hashes where the project uses a lock file.
- Pin new dependencies in the project's existing dependency file with exact versions and record them in `docs/decisions/` plus the SBOM (CRA-035). Candidate pins to evaluate (verify latest stable at implementation time and record the chosen version): `rdflib`, `pyshacl`, `defusedxml`, `hypothesis`, `pytest-timeout`, `jsonschema`, `cyclonedx-bom` or `syft` (binary).
- JVM workers (ELK, OWL API, ROBOT, optional TopBraid SHACL API): pinned JDK in a separate worker image; never on the API host process (subject to H-02).
- Frontend: existing React/Vite toolchain; add Playwright and `@axe-core/playwright` as dev dependencies if absent.

## 2. Acceptance Infrastructure (Work Package WP-00 — first thing to build)

WP-00 implements CRA-001.3, CRA-001.9, CRA-001.10, CRA-037.4 and is a prerequisite for recording any other clause as VERIFIED.

### 2.1 Files to create

| Path | Purpose |
|---|---|
| `tools/acceptance/schemas/receipt.schema.json` | JSON Schema of the receipt (requirements section 2.3) |
| `tools/acceptance/schemas/ledger.schema.json` | JSON Schema of the ledger (requirements section 2.4) |
| `tools/acceptance/seed_ledger.py` | Creates `.audit-scratch/ledger.json` with every clause, acceptance, scenario, decision, conflict and research item in state OPEN (reads `CRAr_cpccaggcc-requirements.md`) |
| `tools/acceptance/run_and_receipt.py` | Wraps a test command: fingerprints source before/after, records artifact digest, parses JUnit XML, writes a receipt |
| `tools/acceptance/verify_ledger.py` | Validates ledger + receipts; refuses invalid states; exit code non-zero on any violation |
| `tools/acceptance/review_receipt.py` | Records an independent reviewer signature (reviewer != producer) |
| `tests/acceptance/test_verify_ledger.py` | Negative fixtures proving the verifier refuses tampered/stale/skipped/unsigned evidence |

### 2.2 `seed_ledger.py` (reference implementation)

```python
"""Seed .audit-scratch/ledger.json from the combined requirements document."""
from __future__ import annotations
import json, re, sys
from datetime import datetime, timezone
from pathlib import Path

REQ = Path(sys.argv[1] if len(sys.argv) > 1 else "CRAr_cpccaggcc-requirements.md")
OUT = Path(".audit-scratch/ledger.json")

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

text = REQ.read_text(encoding="utf-8")
items: list[dict] = []
for m in re.finditer(r"^- \*\*(CRA-\d{3})\.(\d+)\*\* `\[(\w+)\]` (.+)$", text, re.M):
    items.append({"id": f"{m[1]}.{m[2]}", "kind": "clause", "parent": m[1], "origin": m[3],
                  "state": "OPEN", "owner": None, "blocked_by": [], "receipts": [], "notes": "", "updated_at": now()})
for rid in sorted({i["parent"] for i in items}):
    items.append({"id": f"{rid}.A", "kind": "acceptance", "parent": rid, "state": "OPEN", "owner": None,
                  "blocked_by": [], "receipts": [], "notes": "", "updated_at": now()})
for kind, pat in (("scenario", r"^\| (E\d{2}) \|"), ("decision", r"^\| (H-\d{2}) \|"),
                  ("conflict", r"^\| (X-\d{2}) \|"), ("research", r"^\| (C\d{2}) \| ")):
    for m in re.finditer(pat, text, re.M):
        iid = m[1] if kind != "research" else f"R-{m[1]}"
        items.append({"id": iid, "kind": kind, "parent": None, "state": "OPEN", "owner": None,
                      "blocked_by": [], "receipts": [], "notes": "", "updated_at": now()})
seen, unique = set(), []
for it in items:
    if it["id"] not in seen:
        seen.add(it["id"]); unique.append(it)
OUT.parent.mkdir(parents=True, exist_ok=True)
if OUT.exists():
    sys.exit(f"{OUT} exists; refusing to overwrite. Use a migration script to add new items.")
OUT.write_text(json.dumps({"schema": "eoip-ledger-v3", "created_at": now(), "items": unique}, indent=2), encoding="utf-8")
print(f"seeded {len(unique)} items")
```

Expected count after seeding equals the tracker's item count (528 in v3.0: 372 clauses + 42 acceptance + 12 scenarios + 14 decisions + 33 conflicts + 55 research). A different count means the parser or the document changed; investigate before continuing.

### 2.3 `run_and_receipt.py` (reference implementation)

```python
"""Run a verification command and emit a receipt. Usage:
python tools/acceptance/run_and_receipt.py --clause CRA-020.2 --profile P0 \
    --artifact dist/eoip-*.whl --backend memory-harness -- python -m pytest tests/semantic/test_shacl_strict.py \
    --junitxml {junit}
"""
from __future__ import annotations
import argparse, glob, hashlib, json, os, platform, subprocess, sys, uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def source_fingerprint() -> tuple[str, str, bool]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    staged = subprocess.check_output(["git", "ls-files", "-s"], text=True)
    dirty = subprocess.check_output(["git", "status", "--porcelain"], text=True)
    # include content of modified tracked files so a dirty run is content-bound
    h = hashlib.sha256(staged.encode())
    for line in sorted(dirty.splitlines()):
        path = line[3:]
        if os.path.isfile(path):
            h.update(path.encode()); h.update(sha256_file(Path(path)).encode())
    return commit, h.hexdigest(), bool(dirty.strip())

def parse_junit(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    tot = {"tests_total": 0, "tests_failed": 0, "tests_errors": 0, "tests_skipped": 0}
    for s in suites:
        tot["tests_total"] += int(s.get("tests", 0))
        tot["tests_failed"] += int(s.get("failures", 0))
        tot["tests_errors"] += int(s.get("errors", 0))
        tot["tests_skipped"] += int(s.get("skipped", 0))
    xfailed = sum(1 for tc in root.iter("testcase") for sk in tc.findall("skipped") if "xfail" in (sk.get("type", "") + sk.get("message", "")).lower())
    tot["tests_xfailed"] = xfailed
    tot["tests_passed"] = tot["tests_total"] - tot["tests_failed"] - tot["tests_errors"] - tot["tests_skipped"]
    return tot

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clause", required=True)
    ap.add_argument("--profile", required=True, choices=["P0", "P1", "P2"])
    ap.add_argument("--artifact", required=True, help="glob of the built artifact actually exercised")
    ap.add_argument("--backend", required=True)
    ap.add_argument("--engine", default="")
    ap.add_argument("--engine-version", default="")
    ap.add_argument("--fixture", default="")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = [c for c in a.cmd if c != "--"]
    run_id = f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    ev_dir = Path(".audit-scratch/evidence") / a.clause / run_id
    ev_dir.mkdir(parents=True, exist_ok=True)
    junit = ev_dir / "junit.xml"
    cmd = [c.replace("{junit}", str(junit)) for c in cmd]
    arts = sorted(glob.glob(a.artifact))
    if len(arts) != 1:
        print(f"expected exactly one artifact for {a.artifact}, found {arts}", file=sys.stderr); return 2
    artifact = Path(arts[0])
    commit0, fp0, dirty0 = source_fingerprint()
    started = datetime.now(timezone.utc)
    with (ev_dir / "stdout.txt").open("w") as out, (ev_dir / "stderr.txt").open("w") as err:
        rc = subprocess.call(cmd, stdout=out, stderr=err)
    completed = datetime.now(timezone.utc)
    commit1, fp1, dirty1 = source_fingerprint()
    results = parse_junit(junit) if junit.exists() else {"tests_total": 0}
    files = [{"path": str(p), "sha256": sha256_file(p)} for p in sorted(ev_dir.iterdir()) if p.is_file()]
    receipt = {
        "$schema": "https://eoip.enterprise.internal/schemas/verification-receipt-v3.json",
        "receipt_id": f"rcpt-{uuid.uuid4()}", "requirement_clause": a.clause, "state_claimed": "VERIFIED",
        "profile": a.profile, "source_commit": commit0, "source_tree_dirty": dirty0 or dirty1,
        "source_fingerprint": fp0, "source_unchanged_during_run": (commit0, fp0) == (commit1, fp1),
        "artifact_digest": sha256_file(artifact), "artifact_path": str(artifact),
        "artifact_mtime": datetime.fromtimestamp(artifact.stat().st_mtime, timezone.utc).isoformat(),
        "runtime": {"os": platform.platform(), "python_version": platform.python_version(),
                    "backend": a.backend, "engine": a.engine, "engine_version": a.engine_version},
        "fixture": {"id": a.fixture},
        "execution": {"command": cmd, "exit_code": rc, "started_at": started.isoformat(), "completed_at": completed.isoformat()},
        "results": results, "evidence_files": files, "verified_invariants": [], "negative_cases": [],
        "evidence_categories": {}, "limitations": [], "producer": os.environ.get("EOIP_AGENT_ID", "unknown-agent"),
        "reviewer": None, "review_signature": None,
    }
    out = Path(".audit-scratch/receipts") / a.clause / f"{run_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2))
    print(out)
    return rc

if __name__ == "__main__":
    sys.exit(main())
```

After the run, the agent fills `verified_invariants`, `negative_cases` and `evidence_categories` from the actual test outputs (never from intentions), then links the receipt in the ledger with its SHA-256.

### 2.4 `verify_ledger.py` (rules it must enforce)

| Rule | Reason code |
|---|---|
| Every item has a known state | `UNKNOWN_STATE` |
| VERIFIED/ACCEPTED item has >= 1 receipt and each receipt file exists with matching SHA-256 | `MISSING_RECEIPT`, `RECEIPT_HASH_MISMATCH` |
| Receipt passes JSON Schema | `RECEIPT_SCHEMA` |
| Each `evidence_files` entry exists and matches hash | `EVIDENCE_MISSING`, `EVIDENCE_HASH_MISMATCH` |
| `execution.exit_code == 0` | `NONZERO_EXIT` |
| `tests_total > 0` and failed/errors/skipped/xfailed all 0 | `NO_TESTS`, `TEST_FAILURE`, `SKIPPED_REQUIRED` |
| `source_unchanged_during_run` true | `SOURCE_CHANGED` |
| `completed_at` later than `artifact_mtime` | `STALE_ARTIFACT` |
| ACCEPTED: reviewer non-null, reviewer != producer, signature present | `UNREVIEWED`, `SELF_REVIEW` |
| Release mode: `source_tree_dirty` false and `source_commit` equals the release commit | `DIRTY_TREE`, `WRONG_COMMIT` |
| Parent `CRA-xxx.A` ACCEPTED only if all clauses ACCEPTED | `CHILD_OPEN` |
| Item with `blocked_by` cannot be VERIFIED/ACCEPTED while the blocker is not ACCEPTED/recorded | `BLOCKED` |
| `SUPPORTED_QUALIFIED` capability (CRA-001.7) only for capabilities whose clauses are ACCEPTED | `CAPABILITY_OVERCLAIM` |

`tests/acceptance/test_verify_ledger.py` builds fixture ledgers violating each rule and asserts the specific reason code. This test file is itself evidence for CRA-001.3/CRA-037.4 only after a receipt from `run_and_receipt.py` is reviewed.

### 2.5 Tracker interoperability

`CRAr_cpccaggcc-tracker.html` exports `{"schema":"eoip-ledger-v3","items":[...]}` with the same `id`, `state`, `owner`, `receipts`, `notes`. Importing a ledger into the tracker shows state; the tracker refuses to move an item to VERIFIED/ACCEPTED without a receipt path, commit SHA and (for ACCEPTED) a reviewer different from the producer, but the tracker is still only a view: `verify_ledger.py` is the authority.

### 2.6 Standard command patterns

```bash
# unit or integration verification producing a receipt
python tools/acceptance/run_and_receipt.py --clause CRA-016.3 --profile P0 --artifact "dist/eoip-*.whl" \
  --backend memory-harness -- python -m pytest tests/semantic/test_rdf_terms.py -p no:cacheprovider --timeout=300 --junitxml {junit}
# verify everything
python tools/acceptance/verify_ledger.py --ledger .audit-scratch/ledger.json --mode development
python tools/acceptance/verify_ledger.py --ledger .audit-scratch/ledger.json --mode release --release-commit "$(git rev-parse HEAD)"
```

`--backend memory-harness` receipts can only support clauses whose evidence category is explicitly unit-level; integration, authorization, recovery and performance categories require the real configured backend for the declared profile.

## 3. Work Package Catalogue

Each work package (WP) below names: clauses covered, inspect-first leads, build steps, interfaces, tests (positive and negative), commands, evidence and the definition of done. Test file names are proposals — if an equivalent test module already exists, extend it and record the mapping in the ledger notes. Build in gate order; within a gate, follow the listed order unless an independent clause can proceed in parallel.

**Definition of done for every WP:** all clauses of the requirement reach VERIFIED with receipts produced by `run_and_receipt.py`; `CRA-xxx.A` acceptance test executed against the real backend for the stated profile; an independent reviewer signs; `verify_ledger.py` passes; documentation updated with actual outcomes and limitations.

## 3.0 Work Package Index (execution order)

| WP | Gate | Requirement | Title | P | Clauses | Depends on | Human decisions |
|---|---|---|---|---|---|---|---|
| WP-001 | A | CRA-001 | Baseline, Decisions and Acceptance Ledger | P0 | 12 | none | — |
| WP-042 | A | CRA-042 | Competitive Research Qualification and Maintenance | P1 | 7 | CRA-001 | — |
| WP-002 | B | CRA-002 | Modularity and Safe Plugin Runtime | P0 | 11 | CRA-001 | — |
| WP-003 | B | CRA-003 | Identity, Scope and Derived-Data Authorization | P0 | 12 | CRA-001/002 | — |
| WP-031 | B | CRA-031 | Durable Jobs, Publication and Event Delivery | P0 | 7 | CRA-002/003 | — |
| WP-032 | B | CRA-032 | Observability and Operational Truth | P0 | 8 | CRA-001/003/031 | — |
| WP-035 | B | CRA-035 | Commercial Packaging and Supply-Chain Compliance | P0 | 8 | CRA-001/002 | H-04 |
| WP-040 | B | CRA-040 | Privacy, Retention, Deletion and No-Egress Guarantees | P0 | 7 | CRA-003/010/018/031 | — |
| WP-004 | C | CRA-004 | Connection Factory and Conformance SDK | P0 | 12 | CRA-002/003 | — |
| WP-010 | C | CRA-010 | Durable Source Events and Incremental Synchronization | P0 | 8 | CRA-003/004/031 | H-14 |
| WP-011 | C | CRA-011 | Safe Push, Crawl and Network Access | P0 | 8 | CRA-003/004 | — |
| WP-012 | C | CRA-012 | Safe Text, Structured Data and Office Parsing | P0 | 9 | CRA-002/010/011 | — |
| WP-013 | C | CRA-013 | Email, Containers and Nested Provenance | P0 | 8 | CRA-012/035/040 | H-09 |
| WP-016 | D | CRA-016 | RDF Terms, Parsing and Standards Fidelity | P0 | 10 | CRA-002/003 | — |
| WP-017 | D | CRA-017 | Mapping IR, RDF/LPG Projection and OBDA Inputs | P0 | 11 | CRA-010/016 | — |
| WP-018 | D | CRA-018 | Durable Ontology Registry and Packages | P0 | 8 | CRA-016/031/035 | — |
| WP-019 | D | CRA-019 | Profile-Correct Reasoning and Explanations | P0 | 13 | CRA-002/016/018 | H-02 |
| WP-020 | D | CRA-020 | Transactional Shape Validation | P0 | 11 | CRA-002/016/018/031 | — |
| WP-021 | E | CRA-021 | Vocabulary, Taxonomy and Multilingual Stewardship | P1 | 8 | CRA-018/020/022 | — |
| WP-022 | E | CRA-022 | Ontology and Mapping Change Governance | P1 | 9 | CRA-003/018/019/020/031 | — |
| WP-023 | E | CRA-023 | Canonical Identity, Alignment and Reversible Resolution | P1 | 8 | CRA-003/010/016/019/022 | — |
| WP-028 | E | CRA-028 | Temporal Knowledge, Impact and Simulation | P1 | 8 | CRA-010/019/023/031 | — |
| WP-029 | E | CRA-029 | Catalog, Lineage and Enterprise Context | P1 | 8 | CRA-003/010/017/018/024/031 | — |
| WP-024 | F | CRA-024 | Typed Query, Federation and Semantic Planning | P1 | 11 | CRA-003/016/017/019/031 | — |
| WP-025 | F | CRA-025 | Search, Embeddings and Projection Fidelity | P1 | 7 | CRA-003/010/018/023/031 | — |
| WP-026 | F | CRA-026 | Evidence-Bound AI and Ontology Learning | P1 | 9 | CRA-003/014/019/020/023/025/040 | — |
| WP-030 | F | CRA-030 | Modular, Accessible and Truthful GUI | P1 | 9 | CRA-001/003 and the domain requirement exposed by each screen | — |
| WP-005 | G | CRA-005 | Work-Tracking and Test-System Adapters | P1 | 9 | CRA-004/010/011 | H-11 |
| WP-006 | G | CRA-006 | Wiki, Content, Chat and Document Repositories | P1 | 8 | CRA-004/010/011/012/013 | H-11, H-13 |
| WP-007 | G | CRA-007 | Code, Build, Artifact and API-Portal Adapters | P1 | 9 | CRA-004/010/011 | H-07, H-11 |
| WP-008 | G | CRA-008 | Observability and Operational-System Adapters | P1 | 9 | CRA-004/010/011/040 | H-11 |
| WP-009 | G | CRA-009 | Warehouses, Catalog Federation and Custom Systems | P1 | 8 | CRA-004/024/029 | H-06, H-11 |
| WP-014 | G | CRA-014 | Images, Audio and Video | P1 | 8 | CRA-002/012/026/035/040 | — |
| WP-015 | G | CRA-015 | Engineering Diagram Semantics | P1 | 8 | CRA-012/014/016/017 | — |
| WP-027 | G | CRA-027 | Governed Actions and Write-Back | P1 | 9 | CRA-003/004/022/031/040 | H-03 |
| WP-033 | H | CRA-033 | Backup, Restore and Failure Recovery | P0 | 7 | CRA-018/031/032/040 | — |
| WP-034 | H | CRA-034 | Migration, Portability and Rollback | P1 | 8 | CRA-016/017/018/022/033/035 | — |
| WP-039 | H | CRA-039 | Public APIs, SDKs and Developer Ecosystem | P1 | 8 | CRA-001/002/003/035/037 | — |
| WP-036 | I | CRA-036 | Correctness, Performance and Scale Qualification | P0 | 9 | the feature under qualification and CRA-001/032/037 | H-01 |
| WP-037 | I | CRA-037 | Independent QA and Evidence Verification | P0 | 10 | CRA-001 and each changed feature | — |
| WP-038 | I | CRA-038 | Support, Service Objectives and Operator Readiness | P1 | 8 | CRA-032/033/035/037 | H-08 |
| WP-041 | I | CRA-041 | Truthful Positioning, Competitive Claims and Disclosure Governance | P1 | 7 | CRA-001/035/036/037/042 | H-05, H-12 |

WP-00 (acceptance infrastructure, section 2) precedes all of them.

### Gate A — Truthful baseline

#### WP-001 — Capability registry, decisions and ledger (CRA-001.1-001.12, CRA-001.A)

- **Inspect first:** `packages/eoip/graph/backends.py` (capability/export lists, lines ~189-245), any existing `/capabilities`, `/health` or feature-flag routes, `packages/eoip/contracts/`, provider registries for models/connectors/parsers.
- **Build:**
  1. `packages/eoip/capabilities/model.py`: `CapabilityState` enum (`SUPPORTED_QUALIFIED`, `SUPPORTED_UNQUALIFIED`, `DISABLED`, `UNAVAILABLE`, `UNLICENSED`, `UNSUPPORTED`) and `CapabilityEntry` (requirements section 6).
  2. `packages/eoip/capabilities/registry.py`: thread-safe singleton `CapabilityRegistry` with `register(provider_id, version, capabilities: dict[str, Probe])`, `probe_all()` (runs each provider's health probe with a 5 s timeout, never raising), `get(capability_id) -> CapabilityEntry`, `require(capability_id, construct: str | None)` raising typed errors mapped to HTTP 422/503/403/409 as in CRA-001.8.
  3. `SUPPORTED_QUALIFIED` is computed only by reading `.audit-scratch/ledger.json` (or a signed release capability manifest in installed deployments): a capability is qualified only if every clause listed in its manifest entry `qualifying_clauses` is ACCEPTED. Configuration can request `DISABLED`, never `SUPPORTED_QUALIFIED`.
  4. Each adapter family registers at startup: graph backends, RDF parser/serializer, SHACL validator, reasoners, query dialects, connectors (per capability from CRA-004), parsers (per format), OCR/ASR/vision, embedding providers, LLM providers, action targets.
  5. Route `GET /api/v1/capabilities` (scoped by TrustedScope; tenant entitlements applied) returning entries; UI badge component rendering the six states with text labels (not colour alone).
  6. Decision records in `docs/decisions/ADR-00xx-*.md` for: profiles, semantic engines, storage authority, event durability backbone (H-14), identity, plugin execution, retention, model policy, evidence storage. Each states tradeoffs and replacement path and pins artifact versions/checksums.
  7. Profile manifests `benchmarks/profiles/P0.yaml`, `P1.yaml`, `P2.yaml` copying requirements section 5.2 (binding columns) and a separate `stretch` block; measured results never written into these files.
  8. Baseline facts (`.audit-scratch/baseline/facts.json`) and probe output from pre-flight steps 1.3-1.4.
- **Tests:** `tests/unit/test_capability_registry.py` (all six states; config cannot set QUALIFIED; probe exceptions become UNAVAILABLE; unsupported construct error payload names the construct); `tests/integration/test_capabilities_route.py` (disabled vs unavailable vs healthy provider on a real instance; tenant without entitlement sees UNLICENSED); `tests/acceptance/test_verify_ledger.py` (section 2.4 rules).
- **Acceptance run:** start the real API with one provider disabled, one pointing at a stopped service and one healthy; capture `GET /api/v1/capabilities`; corrupt a receipt and edit a source file during a run — verifier rejects both.
- **Not done if:** any capability claims SUPPORTED_QUALIFIED without ledger backing; any route returns an empty 200 for an unsupported construct.

#### WP-042 — Competitive research records (CRA-042.1-042.7, CRA-042.A)

- **Build:** `research/competitive/C01.yaml` ... `C55.yaml` seeded from `competitive-research-matrix.csv` (scores, ND, evidence URL, inversion, requirements) with fields `pinned_artifact`, `license_snapshot`, `reviewed_at`, `rationale` per dimension; `research/datasets/` holding the three datasets as separate files with a README stating they must not be merged; `tools/research/validate_research.py` enforcing CRA-042.A rules (score in 1..5 with rationale or `ND` with named gap; reviewed date present; dependency tools pinned; STALE after 183 days).
- **Order:** pin first the tools EOIP will depend on (rdflib, pySHACL, OWL API, ELK, Jena/Fuseki, Ontop, Morph-KGC, DeepOnto, spaCy, OCR/ASR engines) because Gate D needs them.
- **Tests:** `tests/research/test_validate_research.py` with fixtures: blank score, averaged score (e.g. `3.5`), unpinned dependency, missing reviewed date -> all rejected.
- **Human/external:** license verification for X-01, X-02, X-16, X-21, X-30 needs Legal; record outcomes as decision/conflict updates.

### Gate B — Safe platform

#### WP-002 — Plugin runtime and isolated workers (CRA-002.1-002.11, CRA-002.A)

- **Inspect first:** existing plugin system, `packages/eoip/graph/backends.py`, any subprocess/worker pools, `fileparse/engine.py` budgets, Docker/K8s manifests.
- **Build:**
  1. Versioned interfaces (`typing.Protocol` + semantic version + capability negotiation) in `packages/eoip/plugins/contracts.py` for: connector, parser, mapper, graph store, semantic engine, search/vector index, model provider, workflow/action, UI contribution. Negotiation: host declares supported contract range; plugin declares implemented version; mismatch -> `PLUGIN_CONTRACT_INCOMPATIBLE`.
  2. Signed plugin manifest `eoip-plugin.json` (publisher, digest of every file, dependencies, permissions, config schema, migrations, uninstall). Verify with Ed25519 (or the project's existing signing approach) before activation and after retrieval; unsigned/modified -> refuse.
  3. `packages/eoip/workers/supervisor.py`: spawns workers per resource class (`standard`, `heavy`) using OS limits (Linux: cgroups v2 via systemd-run or container runtime; fallback `resource.setrlimit` + process-group kill for development only, labelled as such); wall-clock watchdog; kill whole process group within 1 s; cleans temp dir; records outcome enum; respawns. No network for workers unless the plugin manifest grants an egress policy evaluated by CRA-011 rules.
  4. Worker protocol `packages/eoip/workers/protocol.py`: JSON-RPC over stdio (or gRPC) messages `{request_id, deadline_ms, resource_class, engine, engine_version, profile, inputs:[{name, sha256, ref}]}` -> `{request_id, status, outputs, metrics, error}`. JVM engines run in a separate image `workers/semantic-jvm/`.
  5. Declarative configuration only for ordinary customization; config schemas reject keys that look like code references (`module:function`, `__import__`, shell metacharacters in command fields).
  6. Plugin state repositories scoped by tenant/workspace with schema migrations; disable/uninstall revokes permissions, cancels jobs (CRA-031) and migrates or retains data per manifest.
  7. RDF-store backend port (`graph/backends.py` extension) with Fuseki reference and GraphDB certified adapter skeletons registering capabilities honestly (UNQUALIFIED until CRA-024 receipts).
- **Tests:** `tests/security/test_worker_isolation.py` (fork bomb, memory balloon, infinite loop, outbound socket, `../../etc/passwd`, symlink escape); `tests/unit/test_plugin_manifest.py` (bad signature, digest mismatch, incompatible contract); `tests/integration/test_plugin_lifecycle.py` (crash/restart worker, disable plugin with pending job, no orphan side effects, no cross-tenant state).
- **Commands:** run the attack tests while `tests/perf/health_probe.py` samples `/health` p95; store both outputs in the same receipt.
- **Not done if:** any attack test is skipped on the CI OS; limits only exist in a docker-compose file never exercised.

#### WP-003 — Identity, scope and derived-data authorization (CRA-003.1-003.12, CRA-003.A)

- **Inspect first:** `authz/`, tenancy modules, session/JWT code, existing deployment-token access, caches, saved views, browser local state in the frontend.
- **Build:**
  1. `TrustedScope` dependency for FastAPI (`Depends(get_trusted_scope)`) built only from validated credentials; distinguish deployment tokens (service scope) from user sessions; agent principals carry `autonomy_level`.
  2. Policy decision point `packages/eoip/authz/pdp.py`: `can_read(scope, resource_acl_vector, classification) -> bool`; deny by default; used by every canonical read/write, traversal step, count, search/vector candidate scan, semantic job, event stream, report/export, raw download, administration and action.
  3. Justification-aware visibility (CRA-003.8): `visible(fact) = any(all(can_read(p) for p in j) for j in fact.justifications)` for inferred facts; asserted facts use their own ACL. Explanations select a fully visible justification only.
  4. `policy_epoch` table per tenant; increment on ACL/membership/policy change via the source event pipeline (ACL_UPDATE events) and admin changes; every cache key and projection row stores the epoch; read path compares and re-filters/denies.
  5. Plan-level scope injection for every dialect (EQL/EOQL/OSQL now; SPARQL/SQL/Cypher later in CRA-024): rewrite the typed AST to add tenant graph and ACL predicates before execution; reject user-supplied graph/index outside scope with 403.
  6. Long-running downloads/jobs/actions re-authorize immediately before delivery/commit.
  7. Frontend: scope-bound caches and drafts keyed by tenant/workspace/policy epoch; abort pending requests on scope switch; migrate ambiguous legacy local data without inferring ownership (move to quarantine and prompt).
  8. 404-indistinguishable response for cross-tenant probes (same body shape, same status).
- **Tests:** `tests/security/test_tenancy_and_derivation_acls.py` using two real principals/tenants with colliding external IDs, hidden intermediate nodes, aggregate counts, inferred links, vector neighbours, raw artifacts, exports and event streams; revocation during a job and an active UI session (Playwright) — previously visible data must not reappear via late results.
- **Backend rule:** run on the actual persistence, cache and event backends of the profile; memory-store runs are labelled unit-only.

#### WP-031 — Durable jobs, publication and event delivery (CRA-031.1-031.7, CRA-031.A)

- **Inspect first:** existing job/control plane, outbox or event modules, SSE/WebSocket streams.
- **Build:** durable `jobs` table (id, tenant, kind, payload_ref, state, attempts, lease_owner, lease_expires_at, heartbeat_at, deadline, cancel_requested, fence_token, result_ref); claim with `SELECT ... FOR UPDATE SKIP LOCKED` (PostgreSQL) or the project's equivalent; heartbeat every 10 s, lease TTL 30 s; fencing token incremented per claim and checked on every commit so an expired worker cannot commit; publication intent + mutation digest + outbox row written in one transaction where the store supports it, otherwise intent -> idempotent apply -> reconcile loop with visible `INCOMPLETE` state; event consumers with cursor, replay, retention and gap semantics; per-principal authorization on streams; no bearer tokens in URLs (use short-lived stream tickets); retry policy by operation safety (idempotent only); governed DLQ (reason, redacted diagnostics, attempts, requeue authority, audit).
- **Tests:** `tests/integration/test_durable_jobs.py` (kill worker/process/network/store at each commit boundary; two-worker race; cancel and revoke mid-job; DLQ replay); `tests/unit/test_job_queue_tenancy.py`.
- **Evidence:** independent read-back of expected effects, event sequence, cursor and job state after each fault.

#### WP-032 — Observability and operational truth (CRA-032.1-032.8, CRA-032.A)

- **Build:** correlation IDs propagated source event -> job -> parser -> semantic run -> publication -> projection -> query/action using OpenTelemetry context; metrics listed in CRA-032.6 with bounded labels; `traceparent` on every response; structured audit log sink separate from best-effort telemetry; dashboards (Grafana JSON committed under `ops/dashboards/`) and alert rules (`ops/alerts/*.yaml`) each linked to a runbook; unknown/stale telemetry rendered as UNKNOWN, never zero; redaction filters for credentials, query literals and prompts.
- **Tests:** trigger a real failed connector, a validator timeout, a stuck lease and a policy-stale index; assert trace correlation, alert firing and absence of secrets in logs/metrics/bundles (`tests/integration/test_observability_truth.py`); collector absent/backpressure test proving no critical-path failure.

#### WP-035 — Packaging and supply chain (CRA-035.1-035.8, CRA-035.A)

- **Build:** SBOM generation in CI for wheel, container images, browser bundle, VSIX (if shipped), JVM worker image, models and datasets (CycloneDX JSON); license policy file `compliance/license-policy.yaml` derived from requirements section 13; CI gate failing on denied licenses or unknown licenses in shipped artifacts; NOTICE aggregation (online and offline); artifact signing and provenance (e.g. Sigstore/cosign or the project's PKI) with verification on install; air-gap bundle build without runtime downloads; entitlement flags that disable modules truthfully (capability state UNLICENSED).
- **Tests:** tamper with a plugin/artifact -> activation refused; add an AGPL test dependency -> gate fails; compare embedded inventories with SBOM.
- **Human gates:** Legal approvals for open items (H-04, H-09, X-01, X-02, X-21, X-30) — clauses depending on them stay BLOCKED; agent-written license text never clears rights.

#### WP-040 — Privacy, retention, deletion and no-egress (CRA-040.1-040.7, CRA-040.A)

- **Build:** classification model on source data and every derivative; retention/hold policy store; egress policy enforced in one outbound HTTP/DNS layer used by connectors, parsers, model calls, linting, telemetry, docs and support bundles (no direct `requests`/`httpx` use outside it — add a lint rule); derivative inventory index (subject/source -> every assertion, inference, raw object, index/vector entry, cache, answer, export, job, trace, backup reference); deletion workflow job with legal-hold conflict escalation and scoped report; replay/restore/re-embed guards consulting a tombstone registry so deleted content is never resurrected.
- **Tests:** delete and revoke a subject while jobs and streams are active; restore an older backup and replay events; sweep every store; run a packet/socket monitor (e.g. `nsenter` + `ss`/eBPF or a recording proxy) during full ingestion + GraphRAG in no-egress mode and assert zero external bytes (`tests/integration/test_no_egress.py`, `tests/integration/test_erasure_cascade.py`).

### Gate C — First acquisition slice

#### WP-004 — Connection factory and conformance SDK (CRA-004.1-004.12, CRA-004.A)

- **Inspect first:** `packages/eoip/connectors/factory.py` (1,135 LOC, 8 categories), `base.py`, registry, the 38 connector modules; find the broad `except` around specialization and the `api/entities` default.
- **Build:**
  1. Connector qualification table `docs/connectors/qualification.md` generated from code: provider, versions, capability states, mapping location, receipts.
  2. `ConnectorDescriptor` (CRA-004.7) as Pydantic model; every existing connector declares it; `is_certified` computed from receipts.
  3. `BaseConnector` abstract methods (CRA-004.9); entry-point discovery group `eoip.connectors`; signed manifest check from WP-002.
  4. Config/secret-reference validation before instantiation (JSON Schema + secret resolver that never logs values); typed errors `CONNECTOR_AUTH_FAILED`, `CONNECTOR_VERSION_UNSUPPORTED`, `UNSUPPORTED_CAPABILITY`, `CONNECTOR_SPECIALIZATION_FAILED`.
  5. Remove broad exception swallowing; implement `fallback_policy: explicit` with a capability downgrade event.
  6. Generic protocol adapters (REST/OpenAPI, GraphQL, SOAP 1.2, JDBC/ODBC, SFTP/object storage, Kafka/RabbitMQ/CDC) running in workers; unsupported protocol -> UNSUPPORTED with remediation text.
  7. Rate limiter (token bucket per source instance; honours `Retry-After`, `X-RateLimit-*`; full-jitter backoff base 1 s cap 300 s).
  8. Conformance runner `tools/connectors/conformance.py` + fixtures covering auth, pagination, rate limits, retry, rename/delete, ACL change, ordering, duplicates, cursor durability, attachments and budgets; outputs a receipt per capability.
  9. Authoring template `templates/connector/` with a synthetic custom provider.
- **Tests:** `tests/unit/test_connection_factory.py`, `tests/integration/connectors/test_conformance_runner.py`, restart-resume without duplicates or gaps.

#### WP-010 — Durable source events and incremental sync (CRA-010.1-010.8, CRA-010.A)

- **Build:** `SourceEvent` v1 contract (requirements section 6) with operations upsert/delete/acl_update/rename/reconcile; append-only journal table/log with per-source hash chain (`prev_sha256`); dedup key (source_instance_id, event_id) plus conflict handling for opaque revisions; checkpoints/leases; acknowledgement only after the declared durable boundary; reconciliation/backfill states for partial pages, invalid cursors and expired history (absence in a partial baseline is never deletion); assertions bound to source/ontology/policy revisions with watermarks exposed in QueryResult.
- **Tests:** `tests/integration/test_event_journal_crash.py` injecting crashes before/after raw persistence, publication, outbox delivery and cursor ack; duplicate/reordered/ACL/delete replay compared with an independently computed expected state (`tests/oracles/expected_state.py` written without importing production code).

#### WP-011 — Safe push, crawl and network access (CRA-011.1-011.8, CRA-011.A)

- **Build:** webhook gateway routes per provider verifying signatures (CRA-011.6) with constant-time comparison; replay cache; body limits; backpressure (bounded queue -> 429/503 with Retry-After); crawler with allowlist, scheme/port restrictions, depth/page/byte/time/concurrency budgets, per-request DNS resolution pinned to the connection, redirect revalidation, credential-forwarding prohibition across origins, scripting disabled; coverage report (fetched, denied, skipped, failed with reasons); pause/cancel releasing leases without auto-restart.
- **Tests:** `tests/security/test_webhook_and_crawler.py`: forged HMAC, expired timestamp, replayed delivery, oversized body, redirect to 169.254.169.254, DNS rebinding (test resolver), IPv6 `::1`/ULA, proxy env vars, zip attachment, cross-origin credential forwarding.

#### WP-012 — Text, structured and office parsing (CRA-012.1-012.9, CRA-012.A)

- **Inspect first:** `packages/eoip/fileparse/engine.py` and adapters; `_chunk_text` in the multimodal module (G11).
- **Build:** extend the existing engine (no duplicate parser stack): format detection by content (magic bytes) not extension; adapters for the core format set with dependency readiness (UNAVAILABLE when a converter is missing, never an empty success); locators per CRA-012.8; formulas versus cached values separated; macros never executed; safe XML/HTML; global budgets across nesting; partial-extraction model with warnings; raw bytes retained for rebuild.
- **G11 fix (algorithm):**

```python
def chunk_text(text: str, size: int, overlap: int) -> list[tuple[int, int]]:
    if not (0 <= overlap < size):
        raise ValueError("require 0 <= overlap < size")
    spans, start, n = [], 0, len(text)
    while start < n:
        end = min(start + size, n)
        spans.append((start, end))
        if end == n:          # final chunk exits
            break
        start = end - overlap  # strictly increases because overlap < size
    return spans
```

  Adjust `end` to a grapheme/word boundary only if the adjusted end stays `> start + overlap`, preserving progress.
- **Tests:** golden files per format authored independently (`tests/fixtures/formats/`), corrupted/encrypted/malformed/oversized inputs, Hypothesis property tests for the chunker (termination, coverage, no duplicate suffix loops), the original long-input reproduction executed under `pytest-timeout` in a subprocess before and after the fix; P0 performance target for 10 MB DOCX and 50-sheet XLSX recorded as a measured receipt.

#### WP-013 — Email, containers, nested provenance (CRA-013.1-013.8, CRA-013.A)

- **Build:** EML/MIME/MBOX parser with stable message/thread/part identity; MSG adapter behind license gate (disabled, capability UNLICENSED until H-09); parent/child chain with hashes, original names, locators, inherited ACL/retention/hold; archive expansion with combined limits (CRA-013.8) and path safety; per-item diagnostics with aggregate partial/failed status; remote images and active HTML disabled; every attachment download re-authorized.
- **Tests:** nested EML->ZIP->(PDF, XLSX) provenance; zip bomb, nested bomb, traversal, duplicate names, symlinks, format confusion, malformed encodings, restricted attachment; source email deletion and legal hold cascade across derivatives.

### Gate D — Semantic core (closes F1, F2, F3, G01-G05)

#### WP-016 — RDF terms, parsing and standards fidelity (CRA-016.1-016.10, CRA-016.A)

- **Inspect first:** `packages/eoip/ontology/rdf.py` (JSON-LD export/import, `jsonld_to_property_graph`, lowercasing in `OWLReasoner`), any IRI normalization helpers (`.lower()`, `casefold()` on identifiers anywhere in `packages/eoip`).
- **Build:**
  1. Add pinned `rdflib` (record version and license in ADR + SBOM).
  2. `packages/eoip/ontology/serialization.py`: `RDFDeserializer.parse(data: bytes, fmt: Literal["turtle","xml","nt","nquads","json-ld","trig"], base_iri: str | None, limits: ParseLimits) -> Dataset` and `RDFSerializer.serialize(ds, fmt) -> bytes`. Run inside a `standard` worker for untrusted input. RDF/XML: parse through `defusedxml` pre-check (reject DTDs/entities) before rdflib; enforce byte, triple and time limits.
  3. Term model: wrap rdflib terms into `RDFTerm` without altering lexical forms; blank nodes scoped per document/import; language tags and datatypes preserved; lists and named graphs preserved.
  4. JSON-LD: standard processing with a context resolver that only loads hash-pinned approved contexts from a local cache (no network at parse time); remote contexts not in the allowlist -> `JSONLD_CONTEXT_NOT_ALLOWED`.
  5. Separate outcomes: `SYNTAX_OK|SYNTAX_ERROR`, `PROFILE_MEMBER|PROFILE_VIOLATION` (via OWL API worker), `CONSISTENT|INCONSISTENT` (CRA-019), `CONFORMS|VIOLATIONS` (CRA-020).
  6. Routes `POST /ontology/import` and `GET /ontology/export` per CRA-016.7 with an import report (counts per graph, losses, unsupported constructs, timing). Tenant graphs preserved in TriG/N-Quads exports.
  7. Remove every case-folding of canonical identifiers; display normalization uses separate fields.
  8. Optional `rdf-star` profile (disabled; separate tests) using rdflib's RDF-star support only after verifying the pinned version supports it; otherwise UNSUPPORTED.
  9. Round-trip certification job `tools/semantic/roundtrip_certify.py`: corpus manifest `tests/fixtures/roundtrip/corpus.yaml` (pinned URLs/hashes for gist, schema.org, FOAF, Dublin Core, a >= 10k-triple SKOS thesaurus, FIBO subset), isomorphism via `rdflib.compare.isomorphic` plus an independent second parser (e.g. Jena `riot` in the JVM worker) for differential checking; fidelity report JSON; CI gate on > 1 point regression; Protégé 5.6 manual load recorded as a review record and OWL API automated load in the worker.
- **Tests:** `tests/semantic/test_rdf_terms.py` (case-distinct IRIs, blank-node relabelling isomorphism, datatype/lexical distinctions e.g. `"01"^^xsd:integer` vs `"1"^^xsd:integer` kept lexically, language tags, named graphs); `tests/security/test_rdf_parsing_hostile.py` (XXE, billion laughs, cyclic/remote JSON-LD contexts, malformed literals, oversized input); `tests/semantic/test_roundtrip_corpus.py`.

#### WP-017 — Mapping IR, CML, LPG/RDF projection, OBDA inputs (CRA-017.1-017.11, CRA-017.A)

- **Inspect first:** how each of the 38 connectors maps payloads today; `graph_graph/`; any existing R2RML/RML handling.
- **Build:**
  1. `mapping/ir.py`: engine-neutral IR — `SourceSpec` (kind, schema/version), `SubjectMap` (template, class, identity scope), `PredicateObjectMap` (path, predicate, term type, datatype, language, required), `RelationMap`, `JoinCondition`, `GraphMap` (tenant/assertion graph policy), `ProvenanceSpec`, `GovernanceSpec` (classification, pii paths), `Functions` (whitelisted only).
  2. `mapping/language.py`: CML YAML parser with JSON Schema validation; JSONPath subset (`$.a.b`, `[*]`, `[n]` only); template grammar `{field}` with mandatory IRI-safe percent-encoding; function whitelist (lower, upper, trim, concat, split, date_parse, iri_safe). Never call `eval`, `exec`, `format_map` on untrusted objects or Jinja with attribute access.
  3. `mapping/compiler.py` CML -> IR; `mapping/r2rml_import.py` R2RML/RML -> IR with unsupported-construct report (ONT-017).
  4. `mapping/executor.py`: IR + payload -> staged `CanonicalAssertion` candidates (knowledge_state=proposed or asserted per policy) with EvidenceLocators and PROV-O triples (`mapping/provenance.py`).
  5. `mapping/lpg_rdf.py`: LPG<->RDF scheme exactly as CRA-017.8; parallel edges keep assertion IDs; loss ledger for unsupported conversions; lossless claims blocked when any loss exists.
  6. Virtual vs materialized modes declared per source with snapshot/freshness semantics; virtual execution delegated to CRA-024 OBDA adapter (Ontop qualified in a JVM worker).
  7. Mapping test cases, dry-run preview (`POST /ontology/mapping`), field diagnostics, source-drift analysis; approval bound to source schema + ontology + mapping revisions.
  8. `mapping/suggest.py` (ONT-006): sample <= N (default 200) redacted payloads; infer field types; propose class/property/relation candidates using the configured local model or heuristic matcher; per-field confidence; output is a draft CML file in governance review; never activated automatically.
  9. Migrate Jira, Confluence and ServiceNow connector mappings to CML with parity tests against the existing implementation's output on fixture corpora.
- **Tests:** `tests/mapping/test_cml_language.py` (schema, injection attempts `{0.__class__}`, `__import__`, oversized templates), `tests/mapping/test_ir_equivalence.py` (independent expected RDF for nulls, multi-value joins, language/datatype literals, blank nodes, duplicate/parallel edges, restricted fields), `tests/mapping/test_two_adapters.py` (same IR through two qualified adapters, documented differences), `tests/mapping/test_suggest_eval.py` (acceptance-rate evaluation on labelled corpora, reported not asserted), parity tests; throughput benchmarks recorded under CRA-036.

#### WP-018 — Ontology registry and packages (CRA-018.1-018.8, CRA-018.A)

- **Inspect first:** `packs.py`, `domain_pack_manager.py`, `industry_templates.py`, `gitops.py` release packaging and `OntologyVersionStore`.
- **Build:** durable registry tables (ontology IRI, version IRI, profile, imports with SHA-256, axioms/shapes/mappings references, namespace ownership, license/attribution); immutable release bundles (tar with manifest + signature) built from GitOps releases; drafts vs releases vs graph revisions kept separate; no browser localStorage or global singleton as authority; atomic install with compatibility/signature checks, approved repositories and offline availability; SemVer computation via existing `compute_next_semver` verified with fixtures for major/minor/patch cases; domain packs for gist (pinned, CC BY 4.0 attribution in NOTICE/docs), FIBO and schema.org after license verification (X-30), SNOMED import path for customer-provided files only.
- **Tests:** `tests/semantic/test_ontology_registry.py` (restart and fresh-node restore retrieve the same package by hash; missing import; changed remote document; incompatible engine; tampered member -> signature failure); `tests/semantic/test_semver_from_diff.py`; pack install/validate tests.

#### WP-019 — Profile-correct reasoning and explanations (CRA-019.1-019.13, CRA-019.A)

- **Inspect first:** `OWLReasoner` (`rdf.py:598-700`), `_bootstrap_core_axioms`, `infer_triples`, `is_subclass_of`, property-chain code, every caller.
- **Build:**
  1. `reasoning/port.py`: `ReasonerPort` Protocol (CRA-019.7) returning `SemanticRun` results.
  2. JVM worker `workers/semantic-jvm/` exposing OWL API profile checking, ELK classification, optional Openllet/HermiT (installed separately when licensed), ROBOT `reason/report/explain`; Python adapters `elk_adapter.py`, `openllet_adapter.py`, `hermit_adapter.py` (plugin), `jena_rules_adapter.py` (RL/RDFS), `native_adapter.py` (existing code restricted to profile `eoip-native-rdfs-subset`, exact-IRI comparisons, no lowercasing).
  3. Remove hardcoded domain axioms from production; move them to `tests/fixtures/semantic/legacy_demo_axioms.ttl`.
  4. Inferred assertions written to a separate inferred graph per ontology revision with `justifications`; dependency-aware invalidation on source, ontology, identity or ACL change; multiple justifications handled; ACL composition per CRA-003.8 applied to inputs, outputs and explanations.
  5. `reasoning/hybrid.py`: per-rule strategy table persisted with the ontology revision; cost model inputs (estimated amplification from a dry run, volatility from change history, fan-out, query frequency); TBox change -> recompute affected rules only; benchmark harness comparing pure forward, pure query-time and hybrid.
  6. Status semantics: timeout, cancellation, unsupported construct and error are never reported as consistent or as negative entailment.
  7. Degraded profile reporting when JVM workers are not permitted (H-02).
- **Tests:** `tests/semantic/test_reasoning_gold.py` with an independently authored corpus (entailments, non-entailments, incoherence, profile violations, chains/cycles, duplicate support, retraction), the requirements section 20 fixture, differential comparison against a second engine on the common profile with differences retained, the G03 probe returning false, a static check that no production module contains the legacy axiom IRIs, classification benchmark receipt (20k classes / 150k axioms < 60 s with ELK).

#### WP-020 — Transactional SHACL validation (CRA-020.1-020.11, CRA-020.A)

- **Inspect first:** `shacl_validator.py:77-193`, `rdf.py:369-425 export_shacl_shapes`, `/ontology/validate` route and callers.
- **Build:**
  1. pySHACL worker adapter: input data graph (+ optional ontology for inference mode, explicitly declared), shapes graph, profile `shacl-core-2017`; advanced features (SHACL-SPARQL, SHACL-JS, rules) disabled unless a named profile is enabled and qualified; remote imports blocked.
  2. Pre-validation shape scan: any constraint component not in the declared profile -> `UNSUPPORTED_CONSTRAINT` (never `conforms=true`); unknown datatype IRIs -> setup error.
  3. Report normalization to W3C `sh:ValidationReport` + EOIP fields (revision, engine/version/config, truncation).
  4. Publication path: validate the candidate *with* required existing data at the expected base revision; commit with revision check (compare-and-swap on base revision) or serializable transaction so two individually valid concurrent writes cannot jointly violate a constraint; on any failure, timeout, cancellation or unavailability, commit zero triples.
  5. Shape-change revalidation job (full or declared-incremental) with explicit mode in the result.
  6. Fix `export_shacl_shapes` per CRA-020.8; public `SHACLValidationReport` retained; new routes per CRA-020.9; HTTP semantics per CRA-020.10.
  7. Differential oracle: TopBraid SHACL API in the JVM worker for the common profile.
- **Tests:** `tests/semantic/test_shacl_strict.py` (G01 and G02 reproduced separately then fixed; zero and multi-values; paths; datatypes; node kinds; `sh:in`; patterns; language; numeric bounds; logical constraints), `tests/integration/test_shacl_transactional.py` (concurrent conflicting writes; canonical graph unchanged after failure; validator outage -> 503 and no commit), `tests/contract/test_ontology_validate_contract.py` (existing callers unchanged), differential test vs TopBraid on the shared fixture set; throughput benchmark receipt.

### Gate E — Governed knowledge

#### WP-021 — Vocabulary and multilingual stewardship (CRA-021.1-021.8, CRA-021.A)

- **Build:** wire `skos.py` to the WP-016 serializer (SKOS and SKOS-XL import/export; OntoLex-Lemon as optional profile); concept vs label identity; polyhierarchy and cycle policy; candidate terms/definitions/synonyms/crosswalks with provenance and review; deprecation (`owl:deprecated`, `dct:isReplacedBy`); versions linked to classifier/embedding/index dependencies with publication receipts and consumer acknowledgement; language-aware search/editing (BCP-47), Unicode/RTL-safe rendering; drift proposals from `drift.py`/`embedding_drift.py` routed to review.
- **Tests:** `tests/semantic/test_skos_governance.py` (10k-concept multilingual round trip isomorphic; same-label distinct concepts; cyclic taxonomy policy; retired terms; concurrent edits; vocabulary change -> dependent classifier/search output updated and rollback restores).

#### WP-022 — Change governance, lint and PR gates (CRA-022.1-022.9, CRA-022.A)

- **Build:** lifecycle draft -> validation -> review -> approval -> publication -> superseded/rollback through the existing GitOps workflow (ports only); semantic diff over statements, imports, shapes, mappings, labels and policy implications; bounded impact analysis on data, queries, indexes, sources and actions; approvals bound to exact candidate/base/ontology/shapes/mapping/policy revisions (stale approval invalid); scheduled atomic publication with consumer acknowledgement and explicit partial failure/repair; release gates (competency questions, profile, consistency, shapes, lint, migration dry-run); dual-steward approval for production branch; Lead Developer review record for touches to `gitops.py`/`manifest.py`/`packs.py`.
- **Pitfall scanner (`ontology/lint/`):** rule plug-ins, each with ID, severity, description, remediation hint and gold fixtures. Minimum 20 rules, e.g.: P01 missing rdfs:label; P02 missing definition/comment; P03 missing domain; P04 missing range; P05 circular subclass hierarchy; P06 equivalent-class loop; P07 class with no instances/subclasses/references (unconnected); P08 property with no usage; P09 inverse-property conflict; P10 deprecated term used in active axioms; P11 naming convention violation (configurable); P12 duplicate labels within scheme/language; P13 multiple domains intended as union (warning); P14 literal used where IRI expected; P15 undeclared namespace prefix use; P16 import not pinned; P17 functional property with multiple values in fixtures; P18 disjointness contradiction with subclassing; P19 orphan SHACL shape (target class absent); P20 shape targeting deprecated class; P21 label language tag missing. Runs offline only.
- **Tests:** `tests/semantic/test_lint_rules.py` (each rule positive/negative), `tests/integration/test_gitops_pr_gate.py` (unsatisfiable class PR blocked with report; two editors conflict; reviewer denies; approval expires; policy changes; publication crash; consumer fails; rollback restores business queries without claiming to undo external actions).

#### WP-023 — Identity, alignment and reversible resolution (CRA-023.1-023.8, CRA-023.A)

- **Build:** scoped source identity table (source_instance, external_id, tenant) -> canonical ID with aliases; candidate generator combining deterministic keys and probabilistic features (CRA-023.6) with NIL; never `owl:sameAs` from label/vector similarity alone; approval for high-impact merges; consistency/constraint checks on proposed mappings; conflicting source claims preserved; `IdentityMergeLedger` with atomic merge/split (relationships, evidence, provenance, temporal history) and dependent inference/index rebuild; DeepOnto alignment worker (ONT-015) for schema/pack alignment; spaCy EntityLinker with tenant-scoped KB built from the graph for text mentions.
- **Tests:** `tests/semantic/test_identity_resolution.py` (ambiguous abbreviations, same-name entities, conflicting identifiers, wrong high-confidence match rejected; merge then split across restart compares every edge/evidence/reference with the original; rejected candidates never appear as facts); evaluation report against the linking gate (precision >= 0.99, recall >= 0.80) per tenant/domain/language.

#### WP-028 — Temporal knowledge, impact and simulation (CRA-028.1-028.8, CRA-028.A)

- **Build:** valid time and transaction/observation time on assertions; corrections and retractions as new records (never in-place overwrite); authorized `as_of` reads (API parameter; SPARQL service parameter `eoip:asOf`) constrained by retention/holds; version diffs; separation in API/GUI of observed relationships, deterministic impact, heuristic paths, stochastic estimates and simulation outputs; deterministic algorithms (BFS, Dijkstra, PageRank, Tarjan SCC) via existing `graph/` modules; simulations require versioned assumptions, inputs, seed, uncertainty and validation; path evidence preserved hop by hop; simulated facts never enter asserted knowledge without review.
- **Tests:** `tests/semantic/test_temporal_simulation.py` (late events, corrections, clock skew, merges/splits, permission changes, retention across historical reads; seeded repeatability; cancellation of expensive work).

#### WP-029 — Catalog, lineage and enterprise context (CRA-029.1-029.8, CRA-029.A)

- **Build:** typed linked entities for assets, terms, owners, classifications, quality observations and lineage with source/freshness/scope; base/edit/merged layers with field-level precedence, conflict indicators and reset-to-source; lineage parsing only for supported SQL/dialects with uncertainty for dynamic statements; distinct data/schema/provenance/security graph views; external catalog federation (OpenMetadata, DataHub, Atlas) through public versioned APIs with ownership rules and deletion/ACL propagation; propagated classifications with reversible provenance.
- **Tests:** `tests/integration/test_catalog_layers.py` (source rename after human override; stale owner; conflicting glossary; denied lineage source; failed projection repaired after replay; permitted results through API/UI/MCP).

### Gate F — Usable value

#### WP-024 — Typed query, federation, SPARQL endpoint, RDF backend port (CRA-024.1-024.11, CRA-024.A)

- **Inspect first:** `packages/eoip/qlang/` (EQL/EOQL/OSQL/JQLite/JSONPath/Lucene/taxonomy DSL), existing query routes, `token_budget/`, backend query capability lists (G06).
- **Build:**
  1. Grammar/capability manifest per dialect and backend (`qlang/manifests/*.yaml`) listing exactly supported constructs; queries using anything else fail with `UNSUPPORTED_CAPABILITY` naming the construct.
  2. Typed parse -> AST -> logical plan -> scope injection (WP-003) -> physical plan; parameters bound, never concatenated.
  3. Endpoints: validate, explain (actual plan + reasoning mode), cost, profile, execute, cancel; budgets (30 s, 4 GiB, 10,000 rows/page, depth 3) enforced with backend resource release on cancel.
  4. SPARQL 1.1 Protocol endpoint `GET/POST /sparql` (query; update only when explicitly enabled and governed through publication): parse with rdflib's SPARQL parser to algebra; execute on the qualified RDF backend when configured (Fuseki/GraphDB via HTTP protocol), or translate the supported algebra subset to the LPG plan; unbounded property paths rejected.
  5. RDF backend port: `FusekiStore` (reference) and `GraphDBStore` (certified option) implementing the GraphStore/RDF port; configuration-only targeting of an existing customer GraphDB.
  6. OBDA/federation: Ontop adapter in the JVM worker for qualified relational sources; source auth delegation; null/bag/set semantics documented; join pushdown; partial-source outcomes; snapshot/freshness and schema-drift handling.
  7. Optional adapters with their own manifests: SQL views (DataFusion or Trino), openCypher/GQL over the projection, GraphQL from shapes (extend `schema_gen.py`).
  8. Scoped templates/history/results/caches; redact sensitive literals in history and logs.
  9. BI connectivity test procedure for Tableau and Power BI (recorded session, receipt with screenshots *plus* query logs; screenshots alone insufficient).
- **Tests:** `tests/query/test_query_semantics_oracle.py` (independent result corpus: optional/join/null/cardinality/path/aggregate/order/limit, source failures, injection), W3C SPARQL protocol tests in scope, SP2Bench in-scope queries under 30 s, cost-limit and cancellation releasing backend resources, federated Jira x Snowflake join, warmed-endpoint benchmarks separate from CLI startup.

#### WP-025 — Search, embeddings and projection fidelity (CRA-025.1-025.7, CRA-025.A)

- **Build:** index metadata (scope, source/ontology/policy revision, provider/model/tokenizer, dimension, normalization, metric); provider registry with `test-hashing` refused in production profile; dimension mismatch -> hard error; ACL filtering during candidate generation and at delivery; scoped caches with policy epoch; resumable indexing, deletion, re-embedding into a shadow index, evaluation, atomic cutover/rollback; watermarks and stale/unavailable states; BM25 + dense fusion with RRF (k=60) and optional graph-centrality feature.
- **Tests:** `tests/retrieval/test_hybrid_vector_search.py` (real configured provider; missing provider; vector shape errors; source delete/ACL change; re-embedding crash and rollback; no cross-tenant neighbours/counts/answers; read-back after restart/rebuild); evaluation report recall@k/nDCG/latency by domain/language/ACL selectivity on a labelled corpus.

#### WP-026 — Evidence-bound AI and ontology learning (CRA-026.1-026.9, CRA-026.A)

- **Build:** knowledge_state separation (proposed vs asserted vs inferred) for every model output with provider/model/prompt/tool/config revisions and evidence spans; bounded authorized context builder (token budget, evidence prioritization, freshness, conflicts) using GraphRAG traversal defaults (depth 2, max 200 nodes); clause-level citations to `assertion_id` + EvidenceLocator verified visible at delivery; abstention per CRA-026.8; true streaming with cancellation (no timer-simulated tokens; cancelled partial output never saved as complete); egress/DLP policy before any provider call; retrieved documents and tool outputs treated as untrusted data (system prompt and tool policy unaffected by content); local model serving option (vLLM/Ollama/TGI) for air-gap; usage/cost metering without raw data.
- **Tests:** `tests/ai/test_graphrag_grounding.py` with real local or approved model traces: malicious documents (prompt injection), missing evidence (abstain), contradictory sources (report conflict), unavailable provider (UNAVAILABLE), cancellation; evaluation harness computing evidence precision/coverage, abstention, calibration and drift on held-out data; a check that each cited span supports the claim (human-adjudicated sample + automated entailment check where available).

#### WP-030 — Modular, accessible, truthful GUI (CRA-030.1-030.9, CRA-030.A)

- **Inspect first:** the React app, the 27-screen obligations in GUI plans, shared transport/shell, legacy modules, existing tests; `GUI-UIX-audit-2026-10-16.md`.
- **Build:** task routes (sources, ingestion review, ontology/vocabulary authoring, validation/reasoning, graph/entity/evidence, query/answer, changes/impact, actions/jobs, governance, reports, settings, support) on shared typed API clients generated from OpenAPI (CRA-039); capability-aware navigation (WP-001 states); explicit loading/empty/partial/stale/denied/error/success states; no example data presented as real; simple forms and expert views (Manchester syntax editor, SPARQL workbench) over the same server state; graph/table/tree equivalence with bounded scenes, keyboard navigation, focus identity, screen-reader names; i18n framework with pseudo-locale and RTL; reduced motion honoured in CSS and JS graph animation; versioned scoped preferences (theme, density, locale, white-label) with asset validation and contrast checks; Playwright E2E and axe suites as `npm run test:e2e` and `npm run test:a11y`.
- **Tests:** real browser against real services and the built artifact (desktop and mobile; four supported themes; reduced motion; keyboard); journeys source -> review -> publish -> ask -> evidence -> authorized export/action with failure/restart cases; manual AT review records (NVDA/JAWS/VoiceOver as available) — automated axe passes are necessary but not sufficient.

### Gate G — Named sources, media and actions

All adapters below reuse WP-004 (factory/SDK), WP-010 (events), WP-011 (push/crawl), WP-017 (CML) and WP-003 (ACL). Each product needs a licensed sandbox or real permitted instance (H-11); without one, implement contract code and mock tests, mark integration clauses UNQUALIFIED/BLOCKED, and continue elsewhere.

#### WP-005 — Jira, Rally, qTest (CRA-005.1-005.9, CRA-005.A)

- **Build:** official API research recorded in `docs/connectors/<product>/api.md` (versions, auth, scopes, pagination, rate limits, webhooks, permission APIs) with dated links; compatibility manifest; adapters per CRA-005.6-005.9; CML mappings; vendor-response fixtures with secrets removed; ACL-only change handling; deleted/renamed items; attachments.
- **Tests:** `tests/integration/connectors/test_jira.py`, `test_rally.py`, `test_qtest.py` against sandboxes: bounded baseline and incremental acquisition, overlap dedup, rate limits, ACL-only change, delete/rename, attachments, replay after restart, access revocation.

#### WP-006 — Confluence/wiki, Slack, Documentum (CRA-006.1-006.8, CRA-006.A)

- **Build:** per CRA-006.6-006.8; macro/body fidelity diagnostics; independent permission sync; nested parsing provenance; redaction before indexing/provider calls; Slack private/DM refusal without approval reference (H-13); Documentum object identity never reduced to filename/URL.
- **Tests:** restricted page/channel/document cannot appear via raw downloads, graph neighbours, counts or answers; modify/delete/rename/ACL change verified after restart.

#### WP-007 — GitHub, GitLab, Artifactory, API Portal (CRA-007.1-007.9, CRA-007.A)

- **Build:** per CRA-007.6-007.9; immutable commit references separated from moving branch observations; signed webhook verification and replay protection; credentials never extracted from build metadata; API Portal provider family with candidate profiles kept UNQUALIFIED until H-07; unsupported binaries and executable content rejected.
- **Tests:** source change linked to API/artifact/business entity with exact revision evidence; private repository revocation disappears from retrieval and exports; Artifactory -> commit -> Jira multi-hop.

#### WP-008 — ServiceNow, Splunk, Kibana, Grafana (CRA-008.1-008.9, CRA-008.A)

- **Build:** per CRA-008.6-008.9; least-privilege profiles; domain separation; query/time/result budgets for Splunk; Kibana saved objects distinct from index data authority; Grafana never exposes data-source secrets; observed telemetry separate from inferred causality; redaction receipts; cycle reporting.
- **Tests:** incident -> service -> deployment -> dashboard/log evidence journey; data-source denial; partial/stale telemetry; truncation; ACL revocation; secrets-fixture sweep.

#### WP-009 — Snowflake, catalogs, Fortuna, custom systems (CRA-009.1-009.8, CRA-009.A)

- **Build:** per CRA-009.6-009.8; metadata-only, sampled and virtual modes with separate permissions; sampling and query history opt-in and redacted; cost cancellation; external catalog integration through public APIs with precedence mapping; generic protocol adapters certified through the conformance runner; Fortuna blocked with missing-input reason until H-06.
- **Tests:** virtual vs materialized equivalence under masking/null/join; source denial; drift; cost cancellation.

#### WP-014 — Images, audio, video (CRA-014.1-014.8, CRA-014.A)

- **Build:** capability per task (image metadata, OCR, ASR, video decode/frame sampling, visual extraction) rather than one multimodal flag; heavy workers with duration/resolution/frame/sample/output budgets; offline hash-pinned model bundles; progress based on actual work; explicit partial output; unsupported/low-quality segments preserved; outputs proposed unless policy approves.
- **Tests:** permitted real media, degraded scans/noise/unsupported codecs, large/hostile inputs; no external calls in no-egress mode (WP-040 monitor); locators correct; timeout cleanup; WER/CER and entity precision/recall on licensed held-out corpora against section 5.3 gates.

#### WP-015 — Engineering diagram semantics (CRA-015.1-015.8, CRA-015.A)

- **Inspect first:** existing diagram parser that maps unmatched relations to CALLS and vertices to Service (G10).
- **Build:** notation-specific parsers (draw.io/Chowlk XML, Mermaid/PlantUML subsets; VSDX P2) into a diagram AST; parser coverage declared; configurable mapping table producing proposals; generic `eoip:connectsTo` with loss ledger for unknowns; source-versus-graph diff UI; round-trip to editable diagram or documented non-round-trippable status; escaped/sanitized labels; visual extraction (vision model) only as reviewed candidates with bounding regions.
- **Tests:** independently specified gold diagrams with parallel/directed edges, labels with metacharacters, nesting, intentionally unsupported constructs; comparison of formal axioms and meaning (not vertex counts or screenshots); correction/rejection propagates to graph/provenance/indexes.

#### WP-027 — Governed actions and write-back (CRA-027.1-027.9, CRA-027.A)

- **Inspect first:** `AutonomyLevel` enum and HCTL level, `tools_contract/`, `verification/`, any outbox.
- **Build:** declarative action types as SHACL action shapes (argument schema, preconditions, risk class, target capability, approval rules, compensation/read-back); default read-only for all sources until H-03 and per-source write enablement; ActionIntent lifecycle (CRA-027.6) persisted with journals; exact-digest approvals with nonce and 5-minute expiry; re-authorization immediately before execution; idempotency keys at both EOIP and target (vendor idempotency header where available); read-back query confirms effect before COMPLETED; UNKNOWN_OUTCOME when remote result uncertain with operator recovery; dry-run/impact preview; cancellation before commit; irreversible-action warnings; canonical routes plus aliases (CRA-027.9).
- **Tests:** `tests/integration/test_action_outbox.py` against a vendor sandbox: changed arguments after approval, denied permission, revoked credential, stale source, duplicate request, remote timeout after commit, compensation failure; exactly one intended effect confirmed via vendor read-back and complete audit.

### Gate H — Deploy and migrate

#### WP-033 — Backup, restore and recovery (CRA-033.1-033.7, CRA-033.A)

- **Build:** authoritative state inventory (canonical graph, control DB, ontology packages/import locks, raw references, identity/policy, outbox/cursors, secrets/KMS recovery metadata, projection watermarks); encrypted, access-controlled, retention-aware backups with off-site separation per deployment/backend; PITR (default 30 days, policy-limited); clean-environment restore with revision/checksum/query/ACL checks and projection rebuild; secrets restored through the approved process; old writers fenced; tombstone-aware replay.
- **Tests:** timed restore drill measuring RPO/RTO for P1 (<= 15 min / <= 4 h) with business queries, ontology revisions, cursors and adversarial authorization checks; partial backup failure, corrupt snapshot, lost key, concurrent writes, failed upgrade.

#### WP-034 — Migration, portability, rollback (CRA-034.1-034.8, CRA-034.A)

- **Build:** `eoip-migrate` CLI (Typer/Click per project convention) with subcommands discover/export/convert/validate/compare/replay/cutover/rollback, dry-run defaults and explicit scope; fidelity profiles; feature/loss ledger; reconciliation counts plus independent semantic/query comparisons; watermark-pinned staging and shadow reads; delta replay including ACL/delete events; cutover approval bound to source/mapping/target/policy revisions; routing rollback and compatible data rollback; R2RML/RML import (ONT-017). Documentation marks commands PROPOSED until receipts exist.
- **Tests:** migrate a standards ontology and a named property-graph corpus through two qualified stores; inject mapping failure, drift, denied record, partial cutover, rollback; synthetic 50M-triple GraphDB-format migration with zero dropped triples within the declared profile.

#### WP-039 — Public APIs, SDKs, MCP, docs (CRA-039.1-039.8, CRA-039.A)

- **Build:** OpenAPI from the composed real application, versioned public API separate from internal endpoints; generated Python and TypeScript SDKs (names verified); MCP server over `tools_contract/` and `sdk/` exposing typed tools with provenance and budgets, enforcing TrustedScope and autonomy/approval gates identical to direct calls; plugin/connector templates, synthetic fixtures, conformance runner, supported-version tables; offline ontology documentation generator from signed releases (WIDOCO-class; LODE/WIDOCO licenses verified); contribution, vulnerability disclosure and marketplace policies consistent with proprietary core.
- **Tests:** independently build a client and sample plugin from released schemas/templates; run a scoped task; deprecated/incompatible/unauthorized calls rejected; external agent via MCP answers a business query and a destructive action is held for approval; generated docs/SDKs match runtime and artifact digest.

### Gate I — Independent acceptance

#### WP-036 — Correctness, performance and scale qualification (CRA-036.1-036.9, CRA-036.A)

- **Build:** workload harness `benchmarks/` with pinned dataset generators (LUBM, BSBM, SP2Bench, WatDiv after license verification; synthetic enterprise/ACL corpus), seeds, expected-answer oracles, hardware/OS/runtime/engine/config/artifact manifests; P0 -> P1 -> P2 qualification in order; measurement of p50/p95/p99, throughput, failures, cancels, lag, peak resources, amplification, cost; cold/warm, concurrency, skew, ACL selectivity, updates/deletes, failure/restart; >= 3 trials with variability; 4-hour sustained load (wrk/Locust); CI regression gate (> 10% p95).
- **Rule:** any wrong answer, leak, required timeout or missing artifact fails the gate even if latency is fast; stretch objectives reported separately.

#### WP-037 — Independent QA and evidence verification (CRA-037.1-037.10, CRA-037.A)

- **Build:** test suites labelled by scope (unit, property/fuzz, differential, contract, real-backend, vendor, security, browser, migration/restore, chaos, performance); independent oracles in `tests/oracles/` that never import production code; build-once/promote-digest pipeline; WP-00 verifier wired as the final CI stage; Hypothesis fuzzing and mutation testing (e.g. `mutmut`) on semantic core; coverage/mutation hygiene thresholds (85%/80%) reported, not used as acceptance; zero-skip enforcement; collection-time tracking; quarantine list with defect IDs for pre-existing failures.
- **Tests:** deliberately tamper with a result, reuse a stale artifact, skip a required test, run against memory instead of the production backend, edit source mid-run and fail a negative case: the gate refuses each time.

#### WP-038 — Support and operator readiness (CRA-038.1-038.8, CRA-038.A)

- **Build:** supported versions/deployments and lifecycle policy; runbooks (requirements section 15 list) with prerequisites, stop and rollback conditions; `eoip-admin support-bundle` (redacted, encrypted, consented, retention-tagged); offline documentation; SLA/support tables presented as proposals pending H-08.
- **Tests:** drills by an operator other than the implementer: source credential compromise, stuck publication, lost store, split-brain; raw observations recorded; unresolved failures listed.

#### WP-041 — Claims, positioning and disclosure governance (CRA-041.1-041.7, CRA-041.A)

- **Build:** `docs/claims/claims-register.yaml` schema (id, wording, scope, evidence refs, owner, approvals, expiry, status); `tools/claims/check_claims.py` CI job scanning `docs/`, release notes, website sources and README files for standards/performance/competitive phrases (configurable patterns such as "SHACL compliant", "OWL 2 DL", "no competitor", "x faster", "TCO") and failing unless each matched statement references an approved claim ID whose evidence clauses are ACCEPTED; restricted patent-candidate register (access-controlled, outside public docs) with Legal decision fields (H-12); Ontology-as-Code positioning pack generated only after CRA-022 acceptance.
- **Tests:** the four blocked-publication cases in CRA-041.A plus a passing case with a fully evidenced claim.

## 4. Cross-Cutting Engineering Conventions

- Pydantic request/response models at module level; thread-safe singleton accessors; `stats()` on engines wired to telemetry (existing conventions).
- All new I/O through the egress layer (WP-040); all new background work through the durable job system (WP-031); all heavy/untrusted work through workers (WP-002).
- Error payload shape: `{"error": {"code": "UPPER_SNAKE", "message": "...", "details": {...}, "correlation_id": "..."}}`; never include secrets or restricted content.
- Timezone-aware UTC datetimes only.
- Every new configuration key documented with default, origin tag (CRAr/AGG/OCA/RES) and the lower-only override rule where applicable.
- Every new module has a capability registration (WP-001) and a ledger entry in its WP notes.

## 5. Test Taxonomy and Directory Layout

| Directory | Contents | Counts toward VERIFIED? |
|---|---|---|
| `tests/unit/` | Pure logic with no external services | Only for clauses whose evidence category is unit-level |
| `tests/property/` | Hypothesis property/fuzz tests | Yes, for parser/chunker/term invariants |
| `tests/semantic/`, `tests/mapping/`, `tests/query/`, `tests/retrieval/`, `tests/ai/` | Feature tests with real engines | Yes, with real engines/backends |
| `tests/oracles/` | Independent expected-result builders (no production imports) | Support evidence |
| `tests/contract/` | API/SDK/route compatibility | Yes |
| `tests/integration/` | Real backends, real workers, vendor sandboxes | Yes |
| `tests/security/` | Tenancy, ACL, SSRF, injection, isolation | Yes |
| `tests/e2e/` (Playwright) | Real browser journeys | Yes |
| `tests/perf/`, `benchmarks/` | Performance/scale | Yes, with manifests |
| `tests/mock/` | Mock-only component tests | **No** |
| `tests/acceptance/` | Ledger verifier tests | Yes, for CRA-001/037 |

Fixtures that encode expected answers are authored independently of the implementation (separate author or derived from standards test suites) and carry a license note.

## 6. CI Pipeline (stages in order; a failure stops promotion)

1. Static: lint, type check, license-header check, egress-lint (no direct HTTP clients), secret scan.
2. Contracts: OpenAPI diff, schema validation, SDK generation check.
3. Unit + property/fuzz (with `--timeout`).
4. Independent semantics: differential RDF/SHACL/reasoning tests against second engines.
5. Real-backend integration (profile P0 backends in CI; P1 in staging).
6. Security/tenancy suites.
7. Browser E2E + accessibility (Playwright + axe).
8. Migration/restore drill (nightly).
9. Workload/performance with regression gate (nightly/weekly).
10. Build once: wheel, images, browser bundle, worker images; SBOM; notices; signatures.
11. Claims check (WP-041).
12. Evidence: `run_and_receipt.py` receipts collected; `verify_ledger.py --mode development` on PRs and `--mode release` on release candidates.

## 7. Agent Work Loop (repeat per clause)

```text
1. Pick the next OPEN clause in gate order whose blockers are ACCEPTED/recorded.
2. Re-read the clause, its requirement's acceptance obligation and conflict/decision notes.
3. Search for the canonical owner (rg/grep); record findings in the ledger notes.
4. Write/extend the contract and design note; set DESIGNED.
5. Write negative and positive tests first (independent oracle where semantics are involved).
6. Implement on the canonical path; no mocks in production code; set IMPLEMENTED.
7. Build the artifact; run tests via run_and_receipt.py on the real profile backend.
8. If any test fails, fix the implementation (never the expectation without an oracle); rerun.
9. Fill verified_invariants / negative_cases / evidence_categories from actual outputs; link the receipt; set VERIFIED.
10. Request independent review (different identity); reviewer re-runs or read-backs and signs -> ACCEPTED.
11. Run verify_ledger.py; update docs with actual outcomes and limitations.
12. If blocked by an external input, set BLOCKED/UNQUALIFIED with the exact missing input and move on.
```

## 8. Handoff Checklist (release candidate)

- [ ] `verify_ledger.py --mode release` passes for every clause in the declared release scope; programme-level open items listed.
- [ ] Exact commit, source inventory, artifact digests, SBOMs, notices and signatures attached.
- [ ] Supported profile/backend/source/model versions table.
- [ ] Migration, rollback and restore instructions exercised (receipts).
- [ ] Raw correctness/security/performance/browser results and manual review records.
- [ ] Operational playbooks rehearsed by a non-implementer.
- [ ] Claims register: every external statement evidenced and approved.
- [ ] Known limitations and blocked/deferred work with owners; human decisions H-01..H-14 status.

## Appendix A — Clause-by-Clause Verification Checklist

Every row must end ACCEPTED with a receipt before its requirement can be accepted. 'Primary test location' is a proposal; if an equivalent existing module is used, record the mapping in the ledger. 'Evidence categories' lists those normally applicable; any category declared not applicable needs a reviewed reason in the receipt.

| Item | Origin | Obligation (abridged — full text in requirements) | WP | Primary test location | Evidence categories |
|---|---|---|---|---|---|
| CRA-001.1 | CRAr | Inventory the actual runtime composition and all advertised features, including provider/backend/profile, license, deployment and integration status. … | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.2 | CRAr | Create decision records for profiles, semantic engines, storage authority, event durability, identity, plugin execution, retention and model policies.… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.3 | CRAr | Create one ledger entry per numbered CRA clause, with dependency, owner and required evidence categories. Preserve open historical CP/GUI requirements… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.4 | CRAr | Expose capability discovery based on configuration and runtime readiness. Unsupported, unlicensed, unavailable and unqualified are distinct states; a … | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.5 | CRAr | Adopt the selected P0/P1/P2 target profiles as versioned manifests. Record measured outcomes separately. Reject capability declarations not backed by … | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.6 | AGG | Implement a runtime `CapabilityRegistry`. Every adapter (graph backends, semantic engines, connectors, parsers, model providers) registers its declare… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.7 | RES | Capability state is exactly one of `SUPPORTED_QUALIFIED`, `SUPPORTED_UNQUALIFIED`, `DISABLED`, `UNAVAILABLE`, `UNLICENSED`, `UNSUPPORTED`. `SUPPORTED_… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.8 | AGG | A request needing a capability that is not usable returns a structured error and never an empty success: unsupported construct in a valid request -> H… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.9 | RES | Ledger location: `.audit-scratch/ledger.json`; receipts: `.audit-scratch/receipts/<clause-id>/<run-id>.json` (one directory per clause so repeated run… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.10 | RES | The ledger covers every clause `CRA-xxx.n` of CRA-001..CRA-042, every acceptance obligation `CRA-xxx.A`, end-to-end scenarios E01-E12, human decisions… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.11 | OCA | Re-measure, at the pinned baseline commit, the repository facts asserted by the source analyses and record measured value versus asserted value: Pytho… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.12 | CRA | Run the G01-G03 reproduction probe (combined requirements section 19) at baseline and store its raw output as the baseline defect receipt; later remed… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-001.A | MERGED | [CRAr] inspect an actual instance where a provider is disabled, unavailable and healthy; the UI/API must accurately distinguish all three. Corrupt a r… | WP-001 | tests/acceptance/test_verify_ledger.py, tests/integration/test_capabilities_route.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.1 | CRAr | Define versioned interfaces for connector, parser, mapper, graph store, semantic engine, search/vector index, model provider, workflow/action and UI c… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.2 | CRAr | Keep heavy parsers, JVM reasoners, native codecs, model/GPU work and untrusted extensions outside the request process. Enforce CPU/memory/time/output/… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.3 | CRAr | Require signed plugin manifests, publisher identity, digest, dependency inventory, permissions, configuration schema and migration/uninstall behavior.… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.4 | CRAr | Provide declarative configuration for ordinary customization. A configuration field must not become arbitrary import/eval/shell execution. Custom code… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.5 | CRAr | Persist plugin state through owned repositories, scope it by tenant/workspace and version schema migrations. Disable/uninstall must revoke permissions… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.6 | CRAr | Qualify replacement of one engine/plugin without altering domain APIs or corrupting canonical state. Separate licensing entitlements from authorizatio… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.7 | AGG | Default worker resource classes: `standard` <= 2 GiB RSS, <= 2 CPU, 30 s wall clock per item; `heavy` (OCR, ASR, JVM reasoners, large office conversio… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.8 | AGG | On any limit breach the orchestrator terminates the whole worker process tree within 1 s of detection, releases leases, file descriptors and temp dire… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.9 | AGG | Semantic micro-worker protocol (INV-55): JVM engines (OWL API, ELK, optional HermiT/Openllet, ROBOT, optional Jena/TopBraid SHACL) run only behind a v… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.10 | OCA | Graph backend ports: existing adapters (in-memory, HugeGraph, Neo4j, Neptune in `packages/eoip/graph/backends.py`) and a new RDF-store port (Apache Je… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.11 | OCA | Preserve existing conventions: Pydantic request models at module level (required for FastAPI OpenAPI schema resolution), thread-safe singleton accesso… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-002.A | MERGED | [CRAr] run a benign plugin then malicious timeout/memory/network/path-escape cases. Reject a modified signature and incompatible contract. Crash/resta… | WP-002 | tests/integration/test_plugin_lifecycle.py, tests/perf/health_probe.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.1 | CRAr | Implement trusted principal/session/IdP integration, memberships and tenant/workspace grants, preserving existing approved authentication contracts. D… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.2 | CRAr | Enforce deny-by-default authorization at every canonical read/write, traversal, count, search/vector candidate, semantic job, event, report/export, ra… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.3 | CRAr | Compose source ACLs and classifications on every derivative. Derived facts and evidence cannot be visible merely because their final subject is visibl… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.4 | CRAr | Bind caches, drafts, saved views, cursors and local state to authorized scope and policy epoch. Scope switching/disconnect aborts pending work and dis… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.5 | CRAr | Propagate revocation/ACL changes through every index, cache, inference, job and stream; deny unsafe stale access while projections lag. Reauthorize lo… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.6 | CRAr | Test same-backend tenants with identical external IDs, malicious tenant fields, unauthorized graph names and cross-workspace membership changes. Audit… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.7 | AGG | `TrustedScope` (fields in section 6) is derived only server-side from a validated session, JWT or mTLS identity. Tenant, workspace, roles and ACLs in … | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.8 | RES | Derived-fact visibility rule (resolves X-11): for one justification, a derived fact is visible only if the principal satisfies the ACL of every premis… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.9 | AGG | Each tenant has a monotonically increasing `policy_epoch`, incremented on any ACL, membership, classification or policy change. Caches, cursors, vecto… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.10 | AGG | Scope filters are injected into the typed query plan before execution for SPARQL, SQL, Cypher, EOQL/EQL/OSQL and vector search. User-supplied `GRAPH`/… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.11 | RES | Probing another tenant's identifier returns a response indistinguishable from a non-existent resource (HTTP 404 with the same body shape and timing cl… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.12 | OCA | TriG/N-Quads exports preserve tenant graph IRIs (`urn:eoip:tenant:{id}`) and never merge tenants; covered by a contract test. | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-003.A | MERGED | [CRAr] two real principals/tenants exercise every boundary, including hidden intermediate nodes, aggregate counts, inferred links, vector neighbors an… | WP-003 | tests/security/test_tenancy_and_derivation_acls.py | design, implementation, positive, negative, review, authorization, failure/recovery, integration |
| CRA-004.1 | CRAr | Extend the existing factory with explicit per-capability descriptors: discover, baseline, poll, webhook, CDC, ACL, deletion, attachment, lineage, writ… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.2 | CRAr | Validate configuration/secret references before instantiation. Do not swallow specialization failures and silently switch to a generic endpoint. Fallb… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.3 | CRAr | Provide generic protocol adapters for REST/OpenAPI, GraphQL, SOAP, JDBC/ODBC, SFTP/files/object storage and event/CDC sources through isolated qualifi… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.4 | CRAr | Implement conformance fixtures and a sandbox runner covering auth, pagination, rate limits, retry, rename/delete, ACL change, ordering, duplicate even… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.5 | CRAr | Store provider version/config digest and qualification receipts with each source instance. Successful connection/authentication is not baseline sync c… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.6 | CRAr | Provide authoring templates, contract validation and mock fixtures for a new custom source, followed by separate real-system qualification. Unknown bu… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.7 | AGG | `ConnectorDescriptor` fields: `provider_id`, `display_name`, `version`, `supported_product_versions`, `capabilities` (discovery, baseline_sync, pollin… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.8 | AGG | Per-source-instance token-bucket rate limiter honouring `Retry-After` and vendor rate-limit headers; HTTP 429/503 trigger exponential backoff with ful… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.9 | AGG | SDK: abstract `BaseConnector` with `discover()`, `baseline(cursor)`, `poll(cursor)`, `handle_webhook(event)`, `fetch_acl(resource)`, `fetch_attachment… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.10 | OCA | Inventory all 38 existing connector modules and `connectors/factory.py` (8 application categories) into a connector qualification table (provider, ver… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.11 | CRA | G07 closure: remove the broad exception handler that converts specialization errors into a generic REST fallback. Fallback happens only when `fallback… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.12 | OCA | Payload-to-ontology mapping for every connector is expressed in the declarative mapping language of CRA-017 (CML), not hard-coded in connector bodies;… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-004.A | MERGED | [CRAr] add a synthetic custom provider without core changes, then a real permitted vendor adapter. Demonstrate invalid credential, incompatible versio… | WP-004 | tests/integration/connectors/test_conformance_runner.py, tests/unit/test_connection_factory.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.1 | CRAr | Qualify Jira Cloud and separately selected Data Center versions for projects, issues, links, comments, custom fields and attachments. Retrieve permiss… | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.2 | CRAr | Qualify Rally workspace/project resource types and hierarchy. Preserve artifact relationships and version/cursor semantics; configuration must select … | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.3 | CRAr | Qualify qTest projects, tests, runs/results and defect associations. Distinguish test definitions from execution results and preserve updates/deletes … | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.4 | CRAr | Research the official API/version/auth/scopes and acquire licensed test access for each product. Store a compatibility manifest and vendor-response fi… | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.5 | CRAr | Demonstrate bounded baseline and incremental acquisition, pagination, rate limits, ACL-only change, deleted/renamed items, attachments and replay. A g… | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.6 | AGG | Jira: Cloud REST API v3 and a separately pinned Data Center REST version; webhooks for issue created/updated/deleted and comment events; incremental J… | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.7 | AGG | Rally: WSAPI v2.0; HierarchicalRequirement, Defect, Task, Iteration, Release, Milestone and PortfolioItem types; preserve parent/child epic hierarchie… | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.8 | CRAr | qTest: projects, test cases, test runs, executions/results and defect links; `qtest:verifiesRequirement` links to Jira issues only when the identifier… | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.9 | OCA | All three adapters express payload-to-ontology mapping in CML (CRA-017), with a parity test proving the CML output equals the previous hand-coded mapp… | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-005.A | MERGED | [CRAr] one live/sandbox end-to-end journey per product and selected edition, followed by restart/replay and access revocation. If a sandbox is unavail… | WP-005 | tests/integration/connectors/test_jira.py | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.1 | CRAr | Provide generic wiki acquisition plus Confluence-specific spaces, pages, versions, links, comments and attachments with inherited/restricted-page perm… | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.2 | CRAr | Qualify Slack through approved application scopes/events/history APIs. Preserve conversation membership, message/file edits/deletes, threads, paginati… | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.3 | CRAr | Qualify Documentum's licensed selected API for object IDs, versions/renditions, folders, relationships, ACL inheritance, checkout and retention/legal … | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.4 | CRAr | Preserve message/document part and attachment provenance through nested parsing. Redact restricted content before indexing or invoking external provid… | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.5 | CRAr | Display unsupported macros/renditions, inaccessible content and partial crawl honestly; do not fabricate plain-text equivalents or claim all wiki prod… | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.6 | AGG | Confluence and generic wiki: CQL plus REST for Space, Page, BlogPost, Comment, Attachment and Version; page tree (`wiki:childOf`), links and mentions;… | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.7 | AGG | Documentum: Documentum REST Services and CMIS at pinned licensed versions; Cabinet, Folder, sysobject, rendition and version chain; Documentum ACLs, d… | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.8 | AGG | Slack: Events API (`message.channels`, edits, deletes, `file_shared`) plus `conversations.history`/`replies`; private channels and direct messages are… | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-006.A | MERGED | [CRAr] restricted page/channel/document cannot appear through raw downloads, graph neighbors, counts or answers. Modify/delete/rename a source and cha… | WP-006 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.1 | CRAr | Qualify GitHub/GitLab selected editions for repository/project identity, commits/branches, pull/merge requests, issues, CI metadata and permitted arti… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.2 | CRAr | Support source-native app/project/repository authorization, installation scope, signed webhook verification, cursor/rate-limit behavior and rename/del… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.3 | CRAr | Qualify Artifactory repository/build/artifact metadata, checksum identity and authorized content, including promotion/deletion and repository ACLs. Ne… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.4 | CRAr | Treat API Portal as a configurable provider family until its product/API is identified. Support governed OpenAPI/schema/documentation ingestion, API/v… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.5 | CRAr | Integrate code/document/schema parsing with provenance to commit/artifact/version and explicit language/format capability. Reject unsupported binaries… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.6 | AGG | GitHub (REST plus GraphQL API v4) and GitLab (REST v4/GraphQL): Repository, Branch, Commit, Pull/Merge Request, Issue, Workflow/Pipeline run, Release;… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.7 | AGG | Cross-system issue references: extract issue keys from commit messages/PR titles with a configurable pattern (default `\b[A-Z][A-Z0-9_]+-\d+\b`) restr… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.8 | AGG | Artifactory: AQL plus storage webhooks; Repository, Artifact, Docker image/manifest, BuildInfo; `art:builtFromCommit` from build-info VCS revision; ar… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.9 | RES | API Portal: candidate provider profiles Kong, Apigee, SwaggerHub and a generic OpenAPI 3.0/3.1 crawler. The adapter remains UNQUALIFIED until the actu… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-007.A | MERGED | [CRAr] show a source change linked to an API/artifact/business entity with exact revision evidence. Revoke private-repository access and prove it disa… | WP-007 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.1 | CRAr | Qualify ServiceNow table/CMDB/incident/change/knowledge profiles with actual row/field ACLs and domain separation. Avoid broad table-service-account r… | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.2 | CRAr | Qualify Splunk searches/knowledge objects and permitted event metadata under query/time/result budgets. Sensitive log content is separately authorized… | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.3 | CRAr | Qualify Kibana saved objects/spaces separately from Elasticsearch/OpenSearch data authority. An authenticated dashboard connection does not authorize … | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.4 | CRAr | Qualify Grafana organizations/folders/dashboards and authorized data-source metadata/query results. Never retrieve or expose stored data-source secret… | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.5 | CRAr | Keep observed telemetry separate from inferred incident causality. Preserve timestamps, source sampling, staleness, missing data and uncertainty. Any … | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.6 | AGG | ServiceNow Table API profiles: `cmdb_ci*`, `cmdb_rel_ci` (Depends on::Used by, Runs on::Hosts), `incident`, `change_request`, `problem`, `kb_knowledge… | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.7 | AGG | Splunk saved searches, alerts and dashboards; Grafana `/api/search` and `/api/dashboards/uid/{uid}`; Kibana saved objects per space. Dashboard panels … | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.8 | AGG | Secret and PII redaction is applied to ingested query strings and log snippets before persistence (API keys, tokens, passwords, connection strings, em… | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.9 | RES | The CI dependency structure is stored as a directed graph; cycles present in the CMDB are detected and reported as data-quality findings, never silent… | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-008.A | MERGED | [CRAr] build an incident -> service -> deployment -> dashboard/log evidence journey. Exercise data-source denial, partial/stale telemetry, truncation … | WP-008 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.1 | CRAr | Qualify Snowflake metadata and separately authorized data/query-history access with role/warehouse scope, masking/row policies, identifiers, costs and… | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.2 | CRAr | Provide metadata-only, sampled-data and virtual-query modes with separate permissions, retention and provider readiness. Sampling/query history must b… | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.3 | CRAr | Require a real product identity, interface/schema and network/auth contract for Fortuna. Until supplied, expose the configured custom-system adapter a… | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.4 | CRAr | Integrate external catalogs such as OpenMetadata/DataHub/Atlas or commercial platforms through documented public interfaces and explicit ownership/pre… | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.5 | CRAr | Certify custom REST/GraphQL/SOAP/database/file/event providers using CRA-004 and scope-aware source fixtures. A signed plugin plus connectivity does n… | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.6 | AGG | Snowflake: `INFORMATION_SCHEMA` and, where the role allows, `ACCOUNT_USAGE`; query history feeds CRA-029 lineage parsing; live virtualization through … | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.7 | AGG | Generic protocol adapters configurable with the mapping IR: REST/OpenAPI, GraphQL, SOAP 1.2, JDBC/ODBC, SFTP/files/object storage, Kafka/RabbitMQ even… | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.8 | RES | Fortuna remains a blocked product-specific adapter until decision H-06 supplies product identity, interface and auth contract; meanwhile the generic c… | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-009.A | MERGED | [CRAr] virtual and materialized queries over the same approved source yield equivalent declared results under masking/null/join cases. Demonstrate sou… | WP-009 | see WP | design, implementation, positive, negative, review, integration (vendor sandbox), authorization, failure/recovery |
| CRA-010.1 | CRAr | Version the SourceEvent contract for upsert, delete, ACL-only change, rename/move and reconciliation. Include source instance, stable event identity, … | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-010.2 | CRAr | Preserve event order guarantees exactly as supplied; use stable deduplication and explicit conflict handling when revisions are opaque or incomparable… | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-010.3 | CRAr | Implement durable checkpoints/leases and at-least-once acquisition with idempotent published effects. Acknowledge only after the declared durable boun… | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-010.4 | CRAr | Handle source absence, partial pages, invalid cursors and expired history with visible reconciliation/backfill states. Do not treat partial baseline a… | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-010.5 | CRAr | Bind accepted assertions and projections to source/ontology/policy revisions and expose freshness/watermarks. Replay must preserve deletion and policy… | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-010.6 | AGG | Every pushed or pulled event is appended to an immutable append-only event journal; per source instance, each entry stores the SHA-256 of the previous… | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-010.7 | AGG | Bitemporal stamping: `observed_at` (platform receipt time) and `source_timestamp` (source-recorded time) are both stored; neither is inferred from the… | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-010.8 | AGG | A persistent high-watermark checkpoint per connector instance is written transactionally with (or reconciled against) the publication intent so that a… | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-010.A | MERGED | [CRAr] inject crashes before/after raw persistence, graph publication, outbox delivery and cursor acknowledgement. Replay duplicate/reordered/ACL/dele… | WP-010 | tests/integration/test_event_journal_crash.py, tests/oracles/expected_state.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.1 | CRAr | Authenticate push/webhook sources, validate signature/timestamp/body limits and prevent replay. Apply backpressure and never enqueue unbounded payload… | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.2 | CRAr | Restrict crawler schemes, hosts, ports, credentials, depth, pages, bytes, time and request concurrency. Respect authorized source policies and prefer … | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.3 | CRAr | Revalidate destination/DNS/redirect policy for every request and attachment URL, including IPv6, private/loopback/link-local/cloud metadata and proxy … | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.4 | CRAr | Disable browser scripting and arbitrary resource fetching unless an isolated, explicitly permitted adapter requires it. Keep robots/terms/authorizatio… | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.5 | CRAr | Record crawl coverage, denied/skipped/failed resources and observation times. Partial results cannot become a clean/successful full-source statement. | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.6 | AGG | Webhook signature verification: GitHub `X-Hub-Signature-256` (HMAC-SHA256), GitLab `X-Gitlab-Token`, Slack v0 signing secret with timestamp skew <= 5 … | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.7 | AGG | Crawler defaults: max depth 5, max pages 10,000, max 50 MiB per resource, concurrency 2 per host, domain allowlist mandatory, robots.txt honoured but … | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.8 | AGG | Egress block list re-evaluated per request and redirect: RFC 1918, loopback, link-local 169.254.0.0/16 including 169.254.169.254, IPv6 loopback/ULA/li… | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-011.A | MERGED | [CRAr] hostile webhook/replay, redirect/DNS rebinding, zip attachment and credential-forwarding cases are rejected under real network-policy tests. Ve… | WP-011 | tests/security/test_webhook_and_crawler.py | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.1 | CRAr | Extend the existing format engine rather than creating duplicate parsers. Support TXT/CSV/JSON/XML/HTML/RTF, DOC/DOCX, PPT/PPTX and XLS/XLSX through q… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.2 | CRAr | Preserve paragraph/table/row/column/sheet/slide locators, source encoding and parse/config versions. Distinguish spreadsheet formulas from cached/eval… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.3 | CRAr | Apply global input/expanded/member/depth/text/row/section/time budgets across nesting. Use safe XML/HTML parsing and prevent external-entity/remote-re… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.4 | CRAr | Repair and test chunking progress/termination. Validate `0 <= overlap < chunk_size`; the final chunk exits; empty, boundary, Unicode and long-unbroken… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.5 | CRAr | Model partial extraction and unsupported content explicitly. Preserve raw bytes and warnings so a parser upgrade can rebuild results. A converter exit… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.6 | RES | Core format set (from the original source requirement): TXT, JSON, CSV, XML, HTML, RTF, DOC, DOCX, PPT, PPTX, XLS, XLSX. Extended set (from AGG, requi… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.7 | AGG | Candidate libraries (each subject to CRA-035 license review and pinned versions): python-docx, python-pptx, openpyxl and/or calamine, defusedxml or lx… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.8 | AGG | Every chunk carries an `EvidenceLocator` (document ID, source system, source revision, page/slide/sheet/cell/paragraph/run index, char_start/char_end)… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.9 | AGG | Qualification target on P0 reference hardware: a 10 MB DOCX and a 50-sheet XLSX are fully extracted with locators in <= 5 s each (benchmark manifest t… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-012.A | MERGED | [CRAr] independently authored golden files for every format plus corrupted, encrypted, malformed and oversized inputs. Run the suspected long-input lo… | WP-012 | tests/fixtures/formats/ | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.1 | CRAr | Parse EML/MIME and approved mailbox protocols with stable message/thread/header/body-part identity. Support MSG only through an explicitly licensed an… | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.2 | CRAr | Preserve parent message/archive/document relationships, attachment content hashes, original names, source locators and inherited ACL/retention/legal-h… | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.3 | CRAr | Enforce combined archive/container expansion, depth, member count and path-safety limits, including duplicate names, symlinks and format confusion. Do… | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.4 | CRAr | Handle encrypted/unreadable attachments, malformed MIME, embedded messages and converter failure with per-item diagnostics and aggregate partial/faile… | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.5 | CRAr | Prevent automatic remote-image loading, active HTML/script execution and credential extraction from messages. Every attachment download rechecks sourc… | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.6 | AGG | Formats: EML/MIME and MBOX; MSG only through an explicitly licensed adapter (`extract-msg` remains disabled until its distribution terms are cleared u… | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.7 | AGG | Extract headers `From`, `To`, `Cc`, `Bcc` (only where the source exposes it and policy allows), `Subject`, `Date`, `Message-ID`, `In-Reply-To`, `Refer… | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.8 | AGG | Archives: ZIP, TAR, GZ, BZ2, 7Z with streaming decompression and combined limits: total expanded size 2 GiB, nesting depth 3, 10,000 members, per-memb… | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-013.A | MERGED | [CRAr] nested email/archive bombs, traversal, duplicate members, malformed encodings and restricted attachments fail safely. Demonstrate source email … | WP-013 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.1 | CRAr | Provide capability-specific image metadata, OCR, audio transcription, video decode/frame sampling and optional visual extraction adapters. Report exac… | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.2 | CRAr | Retain coordinates/page/frame/time spans, language, confidence, provider/model/config revisions and raw evidence references. Transcript/visual outputs… | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.3 | CRAr | Isolate codecs/OCR/ML execution, enforce duration/resolution/frame/sample/output budgets and prohibit unapproved model downloads/network calls. Requir… | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.4 | CRAr | Support cancellation/progress based on actual work and explicit partial output. Preserve unsupported or low-quality segments; never fabricate text, ti… | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.5 | CRAr | Evaluate WER/CER, entity/fact precision/recall and visual task accuracy on licensed domain/language corpora with held-out splits. Apply section 4's se… | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.6 | AGG | OCR for PNG, JPG/JPEG, TIFF, WEBP and scanned PDF using a license-reviewed engine (Tesseract or PaddleOCR candidates); each line/paragraph carries a n… | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.7 | AGG | Audio/video: audio extraction with FFmpeg (build flags determine LGPL/GPL obligations, reviewed under CRA-035) for MP4, MKV, MP3, WAV, M4A; transcript… | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.8 | AGG | All OCR/ASR/vision models run on-premises or inside the customer VPC from hash-pinned offline bundles; zero external API calls in no-egress mode. | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-014.A | MERGED | [CRAr] real permitted media files, degraded scans/noise/unsupported codecs and large/hostile inputs. Verify no external call in no-egress mode, correc… | WP-014 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.1 | CRAr | Support notation-specific structured diagrams, initially diagrams.net/Chowlk-compatible conceptual diagrams plus declared Mermaid/PlantUML subsets; re… | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.2 | CRAr | Parse components, ports, containment, directions, cardinalities, sequence/event meaning and labels only where supported. Never silently coerce every b… | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.3 | CRAr | Visual extraction from images/video creates candidates with bounding regions, uncertainty and reviewer controls. Distinguish inferred visual interpret… | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.4 | CRAr | Show a source-versus-graph diff and loss ledger. Unsupported constructs block claims of lossless conversion; the reviewer may explicitly accept a limi… | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.5 | CRAr | Round-trip supported models to editable diagrams or maintain a documented non-round-trippable status. Escape/sanitize all generated markup and labels. | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.6 | AGG | Structured formats: draw.io/diagrams.net XML (including Chowlk notation), declared PlantUML and Mermaid subsets; Visio VSDX as an extended P2 format. … | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.7 | AGG | A configurable, versioned shape/connector mapping table proposes ontology terms (for example cylinder -> `ex:Database`, rectangle -> `ex:Service`, arr… | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.8 | AGG | Unrecognized connectors are preserved as generic directed edges (`eoip:connectsTo`) with all visual attributes and an entry in the loss ledger; never … | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-015.A | MERGED | [CRAr] independently specified gold diagrams with parallel/directed edges, labels/metacharacters, nesting and intentionally unsupported constructs. Co… | WP-015 | see WP | design, implementation, positive, negative, review, integration, negative (hostile inputs), performance, failure/recovery |
| CRA-016.1 | CRAr | Use a proven standards parser for the selected RDF/JSON-LD serializations and validate exact supported syntax/profile. Do not describe the EOIP-specif… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.2 | CRAr | Preserve IRI lexical identity, case, blank-node scope, language tags, datatype and literal lexical/value distinctions, RDF lists, named graph identity… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.3 | CRAr | Restrict JSON-LD contexts and ontology imports by the approved resolver policy, hash-pin approved external resources and support disconnected resoluti… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.4 | CRAr | Distinguish syntax validity, ontology profile membership, logical consistency and instance-shape validity with separate outcomes. | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.5 | CRAr | Qualify export/import using independent parsers and canonical/isomorphic dataset comparisons plus semantic competency queries. Report bounds, truncati… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.6 | OCA | Adopt `rdflib>=7` (BSD-3, pinned) as default parser/serializer for Turtle, RDF/XML, N-Triples, N-Quads, JSON-LD 1.1 and TriG in new module `packages/e… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.7 | OCA | API: `POST /ontology/import` (`format`, `content` or `artifact_ref`) returns an import report (triple/quad counts, named graphs, losses, unsupported c… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.8 | AGG | RDF-star is an optional named profile `rdf-star` (disabled by default) with its own conformance tests; when disabled, statement-level annotations use … | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.9 | OCA | Round-trip corpus (ONT-001/ONT-019): pinned gist release, pinned schema.org release, FOAF, Dublin Core, a >= 10k-triple SKOS thesaurus and a FIBO subs… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.10 | RES | Fidelity rule (resolves X-29): 100% term/axiom fidelity on the declared supported subset; corpus-level fidelity reported with every loss enumerated (u… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-016.A | MERGED | [CRAr] case-distinct IRIs remain distinct; equivalent blank-node relabellings compare correctly; datatype/language/named graph round trips preserve me… | WP-016 | tests/fixtures/roundtrip/corpus.yaml, tests/security/test_rdf_parsing_hostile.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.1 | CRAr | Define a versioned, engine-neutral mapping representation for source schema/records to ontology terms, including stable identity, joins, nulls, dataty… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.2 | CRAr | Support qualified R2RML/RML adapters and explicit source-dialect/config compatibility. User-defined functions run through CRA-002 with approved capabi… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.3 | CRAr | Preserve multigraph/relationship assertion IDs, edge properties and evidence when projecting to/from property graphs. Record every unsupported constru… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.4 | CRAr | Separate virtual mappings from materialized ingestion, including source access policy, transaction/snapshot/freshness semantics and resource costs. Do… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.5 | CRAr | Provide mapping test cases, dry-run/sample preview, field diagnostics and source-drift analysis. Bind approval/publication to source schema and ontolo… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.6 | OCA | Connector Mapping Language (CML), YAML: `source`, `version`, `subject_map{template, class}`, `property_maps[{path, predicate, datatype, required, voca… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.7 | RES | CML compiles into the engine-neutral mapping IR; R2RML/RML (and RML-star when enabled) import translates into the same IR with an unsupported-construc… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.8 | OCA | LPG <-> RDF projection scheme: vertex IRI `eoip:entity/{Label}/{id}` (id percent-encoded) with `rdf:type eoip:class/{Label}`; vertex property `eoip:pr… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.9 | OCA | W3C PROV-O on every mined triple (ONT-018): `prov:wasDerivedFrom` source resource revision, `prov:wasGeneratedBy` mapping-run activity (mapping revisi… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.10 | OCA | AI-suggested mappings (ONT-006): sample bounded, redacted payloads and propose CML with per-field confidence; suggestions never auto-activate. Evaluat… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.11 | AGG | Benchmark targets recorded in the manifest: CML execution >= 10,000 records/s on 1M Jira issues (OCA); vectorized batch materialization (Morph-KGC-cla… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-017.A | MERGED | [CRAr] nulls, multi-value joins, language/datatype literals, blank nodes, duplicate/parallel edges and restricted fields are compared against independ… | WP-017 | tests/mapping/test_cml_language.py, tests/mapping/test_ir_equivalence.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.1 | CRAr | Persist ontology/version IRIs, imports/checksums, axioms, annotations, shapes, rules, mappings, namespace ownership, profile and license metadata in a… | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.2 | CRAr | Package immutable releases with full import closure, engine/profile/config references, provenance, validation/reasoning reports and publication signat… | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.3 | CRAr | Keep drafts, accepted releases and source/derived graph revisions separate. No mutable global singleton or browser localStorage may be the sole author… | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.4 | CRAr | Support domain packs and optional pinned upper ontologies such as gist, preserving upstream terms, namespaces, attribution and migration notes. Do not… | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.5 | CRAr | Resolve and install packages atomically with compatibility and signature checks, approved repositories and offline availability. Reject missing/tamper… | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.6 | AGG | A release bundle contains: primary ontology document(s), pinned transitive import closure with SHA-256 digests, SHACL shapes package, mapping definiti… | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.7 | OCA | Semantic versioning (SemVer 2.0) is computed from the semantic diff using the existing `compute_next_semver` (gitops.py:733) after it is verified by f… | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.8 | OCA | Domain packs (ONT-010) via existing `packs.py`, `domain_pack_manager.py` and `industry_templates.py`: gist (CC BY 4.0, attribution in NOTICE and docs)… | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-018.A | MERGED | [CRAr] clean restart and fresh-node restore retrieve the same package/release by hash; missing import, changed remote document or incompatible engine … | WP-018 | tests/semantic/test_ontology_registry.py, tests/semantic/test_semver_from_diff.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.1 | CRAr | Replace or clearly scope the custom helper; do not advertise it as complete OWL DL. Use qualified engines for RDFS, OWL 2 RL/EL/QL/DL tasks with expli… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.2 | CRAr | Preserve exact identifiers, load pinned import closure, check profile membership and distinguish consistency, unsatisfiable classes, classification an… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.3 | CRAr | Return engine/version/profile, asserted versus inferred statements, explanations/support dependencies, revision and unsupported/error/timeout/cancel s… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.4 | CRAr | Keep inferred graphs separate and implement dependency-aware invalidation/retraction after source, ontology, identity or ACL changes. Handle multiple … | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.5 | CRAr | Offer materialized/query-time modes only where supported and measured. Expose resulting plan, amplification and freshness rather than hiding expensive… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.6 | CRAr | Enforce CRA-003 on inference inputs/outputs/explanations. Prevent restricted supporting facts from leaking through an otherwise visible conclusion. | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.7 | OCA | Define `ReasonerPort` in `packages/eoip/ontology/reasoning/port.py`: `classify()`, `is_consistent()`, `unsatisfiable_classes()`, `realize()`, `entails… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.8 | OCA | Adapters: ELK (Apache-2.0, OWL 2 EL, default for classification), Openllet (license verified, OWL 2 DL alternative), HermiT (LGPL, optional separately… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.9 | OCA | Remove the hardcoded domain axioms of `OWLReasoner._bootstrap_core_axioms()` (Microservice, Engineer, RelationalDatabase; rdf.py:598-700) from all pro… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.10 | AGG | Hybrid mode (ONT-008 / AGG HTRE): a per-rule strategy table (`materialize` or `query_time`) chosen by a documented cost model (estimated amplification… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.11 | RES | Retraction uses stored justification sets (`supporting_assertion_ids`); cost is proportional to affected derivations and is measured, replacing the un… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.12 | AGG | Consistency failures abort publication with an `InconsistentOntologyException`-equivalent typed error that lists a minimal conflicting axiom set whene… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.13 | OCA | Qualification target: classify a 20k-class / 150k-axiom EL ontology in < 60 s with ELK on the P1 reference node. If JVM workers are forbidden (decisio… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-019.A | MERGED | [CRAr] independent gold entailments, non-entailments, incoherence, profile violations, chains/cycles, duplicate support and retraction. The observed c… | WP-019 | tests/fixtures/semantic/legacy_demo_axioms.ttl, tests/semantic/test_reasoning_gold.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.1 | CRAr | Use a proven validator for declared SHACL Core 2017 coverage; keep extensions/profile versions explicit. A custom Python property checker must be labe… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.2 | CRAr | Enforce min/max cardinality, datatype/node kind, class, value sets, language/length/pattern/numeric bounds, logical and property-path constraints for … | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.3 | CRAr | Produce standards-compatible reports with focus node, result path/value, source shape/constraint, severity and message, plus revision/engine/config an… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.4 | CRAr | Validate the candidate against required existing data and shape/ontology revision. Publication requires revision recheck or transactional isolation so… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.5 | CRAr | Revalidate affected data on shape changes; clearly distinguish incremental supported validation from a full check. Timeout, runtime failure, cancellat… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.6 | CRAr | Bound CPU/memory/report size and restrict remote imports/SPARQL/JS/UDF execution. Required advanced profiles receive separate qualification rather tha… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.7 | OCA | Adopt pySHACL (Apache-2.0, pinned) as default validator inside an isolated worker; TopBraid SHACL API (Apache-2.0, JVM) is the differential oracle for… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.8 | OCA | Fix `export_shacl_shapes()` (rdf.py:369-425): emit `sh:datatype`, `sh:nodeKind`, `sh:minCount`, `sh:maxCount`, `sh:pattern`, `sh:class`, `sh:in`; conv… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.9 | OCA | Keep `SHACLValidationReport` as the public type and the existing `/ontology/validate` contract unchanged (contract test); add `POST /ontology/validate… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.10 | AGG | Mutation API semantics: violation -> HTTP 422 with a W3C `sh:ValidationReport` and per-result codes (e.g. `SHACL_CARDINALITY_VIOLATION`, `SHACL_DATATY… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.11 | OCA | Throughput qualification target: >= 20,000 nodes/s on 10M nodes with 500 shapes (benchmark manifest target). | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-020.A | MERGED | [CRAr] independently authored min/max counts including zero/multivalues, invalid datatypes, paths, shape updates and concurrent conflicts. Reproduce G… | WP-020 | tests/contract/test_ontology_validate_contract.py, tests/integration/test_shacl_transactional.py | design, implementation, positive, negative, review, independent oracle, integration, performance |
| CRA-021.1 | CRAr | Support SKOS concepts/schemes, broader/narrower/related, polyhierarchy, preferred/alternative/hidden labels with language tags, mappings, deprecation/… | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-021.2 | CRAr | Provide SKOS-XL and OntoLex-Lemon through qualified optional profiles where required; reject unsupported export/import rather than flattening silently… | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-021.3 | CRAr | Support candidate terms, definitions, synonyms, crosswalk proposals, provenance, domain ownership and review. Model suggestions must not auto-create e… | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-021.4 | CRAr | Version vocabularies with classifier/embedding/index dependencies and publication receipts. Record consumer acknowledgement and stale projection state… | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-021.5 | CRAr | Provide language-aware search/editing and Unicode/RTL-safe presentation, label uniqueness policies and stable IDs independent of translated labels. | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-021.6 | OCA | Wire the existing SKOS object model (`skos.py`, 450 LOC: Concept, ConceptScheme, Collection, mappings, integrity issues, label conflicts) to the CRA-0… | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-021.7 | AGG | Labels per BCP-47 language tag; deprecation via `owl:deprecated true` plus `dct:isReplacedBy`; audited editorial notes; ISO 25964-style thesaurus impo… | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-021.8 | OCA | Existing drift detection (`drift.py`, `embedding_drift.py`) emits evolution proposals into CRA-022 review; proposals are never auto-applied (I17). | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-021.A | MERGED | [CRAr] multilingual import/edit/export, same-label distinct concepts, cyclic taxonomy policy, polyhierarchy, retired terms and concurrent edits. Chang… | WP-021 | tests/semantic/test_skos_governance.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.1 | CRAr | Implement durable draft -> validation -> review -> approval -> publication -> superseded/rollback lifecycle with explicit roles, separation of duties … | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.2 | CRAr | Diff semantic statements, imports, shapes, mappings, labels and policy implications rather than only text files. Display impacted data, queries, index… | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.3 | CRAr | Bind approval to exact candidate, base, ontology, shapes, mapping and policy revisions. Concurrent edits produce conflict/precondition errors; stale a… | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.4 | CRAr | Support scheduled/atomic publication and compatible rollback with immutable manifests, consumer acknowledgement, explicit partial failure and repair. … | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.5 | CRAr | Run competency questions, profile/consistency/shapes checks, domain review and migration dry-runs as release gates. No generated or agent-written onto… | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.6 | OCA | Preserve the existing GitOps core (`gitops.py`, 793 LOC: branches, PRs with review gates, semantic diff, impact analysis `run_ontology_impact_analysis… | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.7 | OCA | Offline ontology pitfall scanner (ONT-013, INV-49) in `packages/eoip/ontology/lint/` detecting at least 20 antipattern classes (including missing doma… | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.8 | AGG | PR gate pipeline: profile check, consistency (CRA-019), SHACL instance regression (CRA-020), pitfall lint, competency questions, semantic diff and imp… | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.9 | AGG | Semantic AST diff (added/removed classes and properties, changed cardinalities, changed subsumption) is shown visually in the UI (CRA-030), not only a… | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-022.A | MERGED | [CRAr] two editors conflict, reviewer denies, approval expires, policy changes, publication crashes and consumer fails. Prove old/new versions remain … | WP-022 | tests/integration/test_gitops_pr_gate.py, tests/semantic/test_lint_rules.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.1 | CRAr | Define scoped source identity and canonical-ID mapping with deterministic idempotency, aliases and source-instance boundaries. Same textual ID in two … | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.2 | CRAr | Generate alignment/merge candidates with lexical/structural/model evidence, uncertainty, domain rules and NIL/no-match outcomes. Never infer `owl:same… | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.3 | CRAr | Require approval for high-impact identity/schema changes and run consistency/constraint checks on proposed mappings. Preserve conflicting source claim… | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.4 | CRAr | Support reversible merge/split with relationship assertion/evidence/provenance preservation, temporal history and retraction/rebuild of dependent infe… | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.5 | CRAr | Evaluate candidate precision/recall/calibration by tenant/domain/language and adverse ambiguity, with held-out gold data. Model changes require reeval… | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.6 | AGG | Candidate generation combines deterministic keys (email, employee ID, account ID) with probabilistic features (Jaro-Winkler and normalized labels, emb… | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.7 | OCA | Schema/pack alignment uses a DeepOnto (BERTMap/BERTSubs) service in an isolated GPU/CPU worker (ONT-015); entity linking in text uses spaCy EntityLink… | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.8 | AGG | An immutable `IdentityMergeLedger` records every merge/split; a split restores the original nodes, edges, evidence and dependent inferences atomically… | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-023.A | MERGED | [CRAr] ambiguous abbreviations, same-name entities, conflicting identifiers and wrong high-confidence matches. Merge then split across restart and com… | WP-023 | tests/semantic/test_identity_resolution.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.1 | CRAr | Publish an exact grammar/capability manifest per dialect/backend: supported EQL/EOQL/OSQL subsets, qualified SPARQL and optional SQL/Cypher/Gremlin/GQ… | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.2 | CRAr | Use typed parsed plans and parameterization; reject unsupported constructs and unauthorized operations. No concatenated raw user strings enter privile… | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.3 | CRAr | Provide validate/explain/cost/profile/execute/cancel with actual execution information, bounded depth/rows/time and source budgets. Explain output mus… | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.4 | CRAr | Implement qualified OBDA/federation with source auth delegation, null/bag/set/type semantics, join pushdown, partial-source outcomes, snapshot/freshne… | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.5 | CRAr | Scope templates/history/results and caches; redact sensitive literals. Prevent unauthorized source or graph selection and export of hidden intermediat… | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.6 | CRAr | Separate warmed endpoint benchmarks from CLI startup/setup. Compare materialized and virtual results on declared semantics, not only query syntax. | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.7 | OCA | SPARQL 1.1 endpoint `GET/POST /sparql` per the SPARQL 1.1 Protocol, executed on a qualified RDF backend or translated to the LPG plan; passes the W3C … | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.8 | AGG | Optional adapters, each with an exact grammar manifest: ANSI SQL views over the ontology (DataFusion/Trino candidates), openCypher/GQL over the proper… | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.9 | AGG | Default budgets: deadline 30 s, memory 4 GiB per query, 10,000 rows per page, traversal depth 3; tenant quotas may only lower them; budgets reuse the … | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.10 | OCA | BI connectivity: Tableau and Power BI connect through the SQL or SPARQL interface (acceptance test with a recorded session). | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.11 | OCA | RDF backend port (ONT-003): Apache Jena Fuseki reference, GraphDB certified option; a customer's existing GraphDB is targetable by configuration alone… | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-024.A | MERGED | [CRAr] independent result corpus covering optional/join/null/cardinality/path/aggregate/order/limit cases, source failures and injection. Run against … | WP-024 | tests/query/test_query_semantics_oracle.py | design, implementation, positive, negative, review, integration, authorization, workflow |
| CRA-025.1 | CRAr | Version keyword/vector indexes by scope, source/ontology/policy revision, provider/model/tokenizer, dimension, normalization and distance metric. | WP-025 | tests/retrieval/test_hybrid_vector_search.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-025.2 | CRAr | Distinguish deterministic hashing fixtures from real semantic providers. Provider-disabled/unavailable or dimension mismatch cannot silently populate … | WP-025 | tests/retrieval/test_hybrid_vector_search.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-025.3 | CRAr | Enforce permission filtering at candidate generation and final delivery, with scoped caches and policy-epoch revocation. Do not retrieve unrestricted … | WP-025 | tests/retrieval/test_hybrid_vector_search.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-025.4 | CRAr | Support resumable indexing, deletion, model re-embedding, shadow index evaluation and atomic cutover/rollback. Keep watermarks and explicit stale/unav… | WP-025 | tests/retrieval/test_hybrid_vector_search.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-025.5 | CRAr | Evaluate recall@k/nDCG/latency by domain/language and ACL selectivity using a labelled corpus. Record corpus splits and model/config changes; do not u… | WP-025 | tests/retrieval/test_hybrid_vector_search.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-025.6 | AGG | Configurable dense providers (local sentence-transformers models or approved external) plus BM25 sparse retrieval; fusion by Reciprocal Rank Fusion (k… | WP-025 | tests/retrieval/test_hybrid_vector_search.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-025.7 | RES | The deterministic hashing embedder is renamed and labelled `test-hashing`; the production profile refuses it at startup. | WP-025 | tests/retrieval/test_hybrid_vector_search.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-025.A | MERGED | [CRAr] real configured provider, missing provider, vector shape errors, source delete/ACL change, re-embedding crash and rollback. Demonstrate no cros… | WP-025 | tests/retrieval/test_hybrid_vector_search.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.1 | CRAr | Keep extraction/classification/alignment/answer suggestions distinct from asserted facts and logical entailments. Record provider/model/prompt/tool/co… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.2 | CRAr | Build bounded authorized context with token budgets, evidence prioritization, freshness and conflicts. Emit clause-level evidence links to actual perm… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.3 | CRAr | Support true streaming/cancellation where configured with cleanup and accurate lifecycle. A graph event feed or simulated token timer is not answer st… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.4 | CRAr | Apply independent egress/DLP policy before provider calls. No unapproved endpoint/model downloads or external linting services in no-egress mode; reco… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.5 | CRAr | Treat retrieved documents and tool outputs as untrusted data. Prompt instructions cannot grant tools, alter trusted scope or bypass publication/action… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.6 | CRAr | Evaluate factual/evidence correctness, abstention, prompt-injection resistance, calibration, domain/language coverage and quality drift against held-o… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.7 | AGG | GraphRAG pipeline: vector entry points -> bounded multi-hop traversal (default depth 2, max 200 nodes) -> ACL pruning -> context assembly; every sente… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.8 | RES | Abstention: when evidence is insufficient or calibrated confidence is below the configured threshold the answer states that it cannot be answered from… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.9 | AGG | Air-gapped deployments route generation only to self-hosted model servers (vLLM, Ollama or TGI candidates) with zero external traffic. | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-026.A | MERGED | [CRAr] real local or approved external model traces with actual responses, malicious documents, missing evidence, contradictory sources, unavailable p… | WP-026 | tests/ai/test_graphrag_grounding.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.1 | CRAr | Define declarative action types, target source/capability, allowed argument schema, preconditions, risk class, execution scope, approval rules and com… | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.2 | CRAr | Default all sources to read-only. Write-back and source-policy provisioning require explicit configuration, separate permissions and qualified vendor … | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.3 | CRAr | Bind approval to exact intent/arguments digest, source/base/policy revisions, principal/delegation, expiry and nonce. Reauthorize immediately before e… | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.4 | CRAr | Persist intent/execution/outcome/compensation journals, enforce idempotency and expose honest partial/unknown state for uncertain remote outcomes. Rea… | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.5 | CRAr | Provide dry-run/impact preview, cancellation before commit, irreversible-action warnings and authorized operator recovery. A graph transaction cannot … | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.6 | AGG | `ActionIntent` (section 6) lifecycle: PROPOSED -> STAGED -> APPROVED -> EXECUTING -> COMPLETED \| FAILED \| COMPENSATED, plus `UNKNOWN_OUTCOME` for unce… | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.7 | OCA | Action types are declared as SHACL action shapes (`OntologyAction`, ONT-009) with SHACL preconditions, declared effects (classes/properties mutated), … | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.8 | AGG | `Idempotency-Key` header (16-128 chars) is mandatory; approvals carry a signature, nonce and default 5-minute expiry; replay or parameter change after… | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.9 | RES | Route consolidation: canonical routes `POST /api/v1/actions/execute`, `GET /api/v1/actions`, `POST /api/v1/actions/{id}/approve`; OCA aliases `POST /o… | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-027.A | MERGED | [CRAr] changed arguments, denied permission, revoked credential, stale source, duplicate request, remote timeout after commit and compensation failure… | WP-027 | tests/integration/test_action_outbox.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.1 | CRAr | Model valid time, transaction/observation time, corrections, retractions, source revision and lineage explicitly. Timestamp fields alone do not establ… | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.2 | CRAr | Support authorized as-of queries, version diffs, provenance and bounded historical snapshots. Retention/hold/deletion rules constrain what history may… | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.3 | CRAr | Separate observed relationships, deterministic graph impact, heuristic paths, stochastic estimates and domain simulation outputs in both API and GUI. | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.4 | CRAr | Simulations require versioned model/assumptions/inputs, seed, uncertainty and validation protocol. Random-walk frequency is not a calibrated failure p… | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.5 | CRAr | Preserve actual path/hop evidence and cost semantics; do not summarize a multi-hop result as a fabricated two-node explanation. Approval/execution of … | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.6 | AGG | Historical reads use an explicit `as_of` parameter on the query API (and an `eoip:asOf` service parameter for SPARQL, because standard SPARQL has no A… | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.7 | AGG | Deterministic graph algorithms (BFS, Dijkstra, PageRank, Tarjan SCC) replace heuristic random-walk summaries for impact paths (G14); existing `graph/p… | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.8 | AGG | Blast-radius output lists impacted services, teams and processes with severity scores explicitly labelled heuristic unless a validated model exists. | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-028.A | MERGED | [CRAr] late events, corrections, clock skew, merges/splits, permission changes and retention across historical reads. Repeat seeded runs, compare sens… | WP-028 | tests/semantic/test_temporal_simulation.py | design, implementation, positive, negative, review, integration, authorization, workflow, failure/recovery |
| CRA-029.1 | CRAr | Maintain technical assets, business terms, owners, classifications, quality observations and lineage as typed linked entities with source/freshness an… | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-029.2 | CRAr | Distinguish observed/base metadata, human curation and effective merged view; define field-level precedence, conflict and reset-to-source behavior. A … | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-029.3 | CRAr | Parse lineage only for supported source/query semantics. Unknown/dynamic statements yield uncertainty and diagnostics, not guessed source-target edges… | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-029.4 | CRAr | Expose data-graph versus schema/meta-graph versus provenance/security graph views with stable links and correct object types. Do not relabel the same … | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-029.5 | CRAr | Federate external catalogs through public versioned APIs with authoritative ownership rules, mappings, duplicate prevention and deletion/ACL propagati… | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-029.6 | AGG | Three metadata layers: base (crawler-observed), edit (human curation), merged (effective view by documented precedence) with reset-to-source and confl… | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-029.7 | AGG | Propagated classifications (Atlas pattern, INV-45): tagging an asset PII cascades along lineage to downstream columns/views/dashboards through an even… | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-029.8 | AGG | Metadata projections compatible with OpenMetadata, DataHub and Apache Atlas public APIs. | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-029.A | MERGED | [CRAr] source rename after human override, stale owner, conflicting glossary, denied lineage source and failed projection. Show the effective value's … | WP-029 | tests/integration/test_catalog_layers.py | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.1 | CRAr | Deliver complete task routes for source discovery/configuration/runs, ingestion review, ontology/vocabulary authoring, validation/reasoning, graph/ent… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.2 | CRAr | Use shared typed API contracts, authorization/capability-aware navigation, route boundaries, cancellable requests and explicit loading/empty/partial/s… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.3 | CRAr | Provide simple task forms plus expert model/query views over the same server state. Display exact revisions, consequences, validation and approval sta… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.4 | CRAr | Keep graph/table/tree alternatives equivalent for inspection and supported actions. Bound graph scenes; support keyboard navigation, focus/selection i… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.5 | CRAr | Target WCAG 2.2 AA across the supported product, with automated checks plus manual AT and usability qualification. Localize resources/formats, test ps… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.6 | CRAr | Version and scope theme/density/locale/white-label/plugin preferences. Safely validate brand assets and contrast, support preview/rollback and show on… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.7 | AGG | Workbenches: Source Management; Ontology Modeler (bounded graph canvas plus expert Manchester-syntax editor); Knowledge Explorer; Ask AI with side-by-… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.8 | OCA | Baseline audit of the existing 90+ React components and 146 ARIA attributes; add an i18n framework (currently zero i18n) with pseudo-locale and RTL te… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.9 | AGG | Automated checks: Playwright end-to-end and axe accessibility suites exposed as `npm run test:e2e` and `npm run test:a11y` (create the scripts if abse… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-030.A | MERGED | [CRAr] real browser against real services and built artifacts across desktop/mobile, four supported themes, reduced motion, keyboard and manual AT. Co… | WP-030 | see WP | design, implementation, positive, negative, review, workflow (real browser), accessibility, deployment |
| CRA-031.1 | CRAr | Reuse and qualify the existing job/control plane for durable queueing, scope, leases, heartbeats, deadlines, retries, cancellation and terminal status… | WP-031 | tests/integration/test_durable_jobs.py, tests/unit/test_job_queue_tenancy.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-031.2 | CRAr | Persist publication intent/mutation/outbox identity consistently. Use a real transaction where available; otherwise implement documented idempotency/r… | WP-031 | tests/integration/test_durable_jobs.py, tests/unit/test_job_queue_tenancy.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-031.3 | CRAr | Define replay/resume/retention/gap semantics for events and consumers, bounded buffers and per-principal authorization. Never put durable bearer crede… | WP-031 | tests/integration/test_durable_jobs.py, tests/unit/test_job_queue_tenancy.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-031.4 | CRAr | Enforce retry policy by operation safety; do not blindly retry mutations. Preserve poison events in a governed DLQ with reason, redaction, requeue aut… | WP-031 | tests/integration/test_durable_jobs.py, tests/unit/test_job_queue_tenancy.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-031.5 | CRAr | Fence expired leases/workers and prevent cancelled/revoked jobs from committing later. API/worker restarts and multi-instance claims must be tested on… | WP-031 | tests/integration/test_durable_jobs.py, tests/unit/test_job_queue_tenancy.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-031.6 | AGG | All jobs live in a durable database queue; workers hold leases with heartbeats every 10 s (lease TTL 30 s); an expired lease is reclaimed from the las… | WP-031 | tests/integration/test_durable_jobs.py, tests/unit/test_job_queue_tenancy.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-031.7 | AGG | Repeatedly failing payloads move to a governed DLQ with redacted diagnostics (stack trace with secrets removed), reason, attempt count and replay auth… | WP-031 | tests/integration/test_durable_jobs.py, tests/unit/test_job_queue_tenancy.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-031.A | MERGED | [CRAr] kill process/network/storage at each commit boundary; race two workers; replay a DLQ item; cancel and revoke scope mid-job. Demonstrate expecte… | WP-031 | tests/integration/test_durable_jobs.py, tests/unit/test_job_queue_tenancy.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.1 | CRAr | Integrate existing structured logging, OpenTelemetry and metrics with source event/job/semantic/publication/projection/query/action correlation and st… | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.2 | CRAr | Record latency/throughput/error/cancel/denied/unsupported/timeout, queue age, source freshness, projection/policy lag, resource usage, inference ampli… | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.3 | CRAr | Restrict metrics-label cardinality and sensitive content; protect tenant-specific diagnostics, traces and support bundles. Redact credentials/query li… | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.4 | CRAr | Provide dashboards and alerts tied to actual measured service behavior, thresholds and runbooks. Avoid initialized example metrics or always-success h… | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.5 | CRAr | Test collector absence/backpressure without corrupting critical data flows. Audit and publication durability must not depend on best-effort telemetry … | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.6 | AGG | Prometheus metrics (bounded labels): `eoip_ingestion_triples_total{source,status}`, `eoip_shacl_validation_duration_seconds{shape_id,conforms}`, `eoip… | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.7 | AGG | Every API response carries a W3C `traceparent`; security-relevant events (login, permission change, ontology merge, action execution) emit structured … | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.8 | OCA | Alerting rules (currently absent) are defined for queue age, projection/policy lag, connector failure, validator unavailability and outbox lag, each l… | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-032.A | MERGED | [CRAr] trigger a real failed connector, timeout validator, stuck lease and policy-stale index. Confirm trace correlation, correct alert/state and no s… | WP-032 | tests/integration/test_observability_truth.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-033.1 | CRAr | Inventory authoritative state: canonical graph, control database, ontology/import/release packages, raw references, identity/policy, outbox/cursors, s… | WP-033 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-033.2 | CRAr | Define consistent encrypted backups/snapshots and retention for each supported deployment/backend, with access controls, immutability where appropriat… | WP-033 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-033.3 | CRAr | Implement restore into a clean environment with revision/checksum/query/ACL consistency checks and projection rebuild. Restore secrets through the app… | WP-033 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-033.4 | CRAr | Measure P1 RPO <=15 min and RTO <=4 h for the declared tested failure model; document observed values, exceptions and exact data loss. Do not infer P2… | WP-033 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-033.5 | CRAr | Rehearse partial backup failure, corrupt snapshot, lost key, concurrent writes, API/worker restart and failed upgrade. Fence old writers and prevent e… | WP-033 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-033.6 | AGG | Online non-blocking snapshots plus transaction-journal replay provide point-in-time recovery; default PITR window 30 days, shortened automatically whe… | WP-033 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-033.7 | RES | P1 objectives RPO <= 15 min and RTO <= 4 h (CRAr). The AGG figure 'RTO <= 4 h for a 500M-triple restore' is a P2 qualification target, not a P1 claim … | WP-033 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-033.A | MERGED | [CRAr] timed independent restore with business queries, ontology revisions, source cursors and adversarial authorization checked after recovery. An ar… | WP-033 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.1 | CRAr | Implement documented export/convert/validate/compare/replay/cutover/rollback tooling using the existing CLI conventions, with dry-run and explicit sou… | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.2 | CRAr | Preserve source IDs/IRIs, blank-node semantics, literals/languages/datatypes, named graphs, edge assertions, provenance, ACL/retention and ontology hi… | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.3 | CRAr | Generate a feature/loss/unsupported ledger and source-target reconciliation counts plus independent semantic/query comparisons. Never declare migratio… | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.4 | CRAr | Stage and shadow-read from a pinned source watermark; replay deltas including ACL/delete events. Bind cutover approval to exact source, mapping, targe… | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.5 | CRAr | Support rollback of routing and compatible data/projections, with separately governed external-action compensation. Retain source until qualified rest… | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.6 | AGG | Design the `eoip-migrate` CLI (status PROPOSED until implemented): `discover --source <uri>`, `export --output <path>` (canonical Turtle/N-Quads with … | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.7 | AGG | Eight-stage protocol: discovery and pin; format extraction with hashes; mapping synthesis with loss analysis; staged loading; semantic-equivalence ver… | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.8 | OCA | R2RML/RML imports from Ontop, Morph-KGC and RMLStreamer users translate into CML/IR (ONT-017) with unsupported constructs reported. | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-034.A | MERGED | [CRAr] migrate a standards ontology and a named property-graph corpus through two qualified stores; compare independent output. Inject mapping failure… | WP-034 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.1 | CRAr | Preserve proprietary EOIP-owned licensing and upstream component rights. Do not relabel third-party files or assume all files in an owned directory ar… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.2 | CRAr | Produce exact shipped SBOMs and license/notices/source-obligation records for Python, npm/browser bundles, VSIX, OS/container packages, JVM/WASM/nativ… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.3 | CRAr | Resolve GPL/AGPL/LGPL/OEM/embedding/redistribution and data/model terms for the actual integration and both SaaS/installed profiles. Existing `extract… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.4 | CRAr | Sign/hash release artifacts and plugin packages, retain build provenance and dependency locks, and make notices available online and offline as approp… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.5 | CRAr | Qualify installation/upgrade/uninstall and air-gap operation with no unapproved runtime downloads. Entitlements must disable unavailable modules truth… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.6 | AGG | Generate CycloneDX or SPDX SBOMs for Python, npm/browser bundles, containers, JVM workers, models and datasets with tools such as syft and a license c… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.7 | OCA | Copyleft policy: GPL/AGPL code is never linked into or bundled with the distributed core; GPL/AGPL servers (Neo4j Community GPLv3, Virtuoso OSE GPLv2)… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.8 | OCA | Dependency decision table (section 13) is the authoritative allowlist input to the CI license gate; every row cites the exact artifact and license sna… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-035.A | MERGED | [CRAr] inspect actual wheel/image/browser/VSIX/air-gap artifacts and compare embedded inventories/notices with SBOM. Tamper with a plugin/artifact and… | WP-035 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.1 | CRAr | Implement a reproducible workload harness with pinned dataset/generator/license, seed, expected answers, hardware/OS/runtime, engine/config and built-… | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.2 | CRAr | Qualify P0 then P1 then P2 separately using the research profiles. Count asserted/inferred triples, raw/index/vector/history bytes, replicas and cold/… | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.3 | CRAr | Measure p50/p95/p99, successful/failed/cancelled operations, throughput, source/index lag, peak resources, amplification and cost units. Include cold/… | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.4 | CRAr | Enforce the selected profile's point-read, bounded graph and approved-query targets without suppressing errors or weakening semantics/security/durabil… | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.5 | CRAr | Run independent oracle/differential semantic checks before timing and retain at least three repeated measured trials with variability. Competitive pub… | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.6 | CRAr | Evaluate parser/OCR/linking/RAG/simulation quality with declared labelled corpora and task-specific thresholds. Use section 4's selected defaults for … | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.7 | OCA | Benchmark suites with committed generator commands, fixed seeds and expected-output hashes under `tests/benchmarks/ontology/` (ONT-020): LUBM (load >=… | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.8 | RES | Binding latency gates are the CRAr profile targets (P0/P1/P2). AGG/OCA stricter numbers (point read p95 < 20 ms at P1/P2; P2 bounded 2-hop p95 < 250 m… | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.9 | AGG | Sustained 4-hour load test (wrk and/or Locust) per profile with memory-stability checks; CI regression gate fails on > 10% p95 latency regression vers… | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-036.A | MERGED | [CRAr] raw machine-readable results and independent expected-answer checks bound to manifests. Any wrong answer, leakage, required timeout or missing … | WP-036 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.1 | CRAr | Maintain unit/property/fuzz, differential semantics, contract, real-backend/vendor integration, security/tenancy, real browser, migration/restore, cha… | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.2 | CRAr | Separate mock tests from actual integration; independently author gold fixtures/oracles so implementation and expected output do not share the same fa… | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.3 | CRAr | Build once and verify the exact promoted artifact in each supported deployment/backend/profile, with actual persistence and negative cases. Developmen… | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.4 | CRAr | Validate source stability, artifact freshness/hashes, exit codes, skip/error counts, fixtures/environment and review records. Missing/invalid/stale/co… | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.5 | CRAr | Perform manual domain, security, accessibility/AT, usability, operations and legal reviews where automated evidence is insufficient. Record reviewer/d… | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.6 | CRAr | On concurrent source changes, preserve edits and report the run as unbound; restart affected services and rerun relevant qualification on a stable rev… | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.7 | AGG | Property-based fuzzing (Hypothesis) of parsers, serializers, chunkers and query planners; mutation testing on semantic core modules. | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.8 | RES | Hygiene thresholds from AGG (line coverage >= 85% for `packages/eoip`, mutation score >= 80% on semantic core) are CI hygiene gates only; meeting them… | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.9 | AGG | Zero-skip policy: CI fails when a required test is skipped, xfailed without an open defect ID, errors or times out. | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.10 | OCA | Track and reduce test collection time (currently 60-120 s) and quarantine known pre-existing failures with tracked IDs rather than deleting them. | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-037.A | MERGED | [CRAr] deliberately tamper with a result, reuse stale artifacts, skip a required test, run against memory instead of production backend, edit source m… | WP-037 | tests/oracles/ | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.1 | CRAr | Define supported versions/deployments, lifecycle/deprecation, service ownership, incident severity, escalation and customer versus vendor responsibili… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.2 | CRAr | Implement documented incident, scaling, upgrade, backup/restore, credential compromise, poisoned data/model and projection-lag playbooks with diagnost… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.3 | CRAr | Treat 99.9% monthly availability and initial response objectives as engineering proposals until staffing, measurement, exclusions and signed contracts… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.4 | CRAr | Produce redacted support bundles with authorization, consent, retention and no secrets/customer raw data by default. Provide offline documentation for… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.5 | CRAr | Rehearse operational incidents and restore with someone other than the implementer where feasible, recording actual observations and unresolved failur… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.6 | AGG | Runbooks: ingestion backlog/consumer lag, store memory exhaustion and query kill, compromised source credentials, inconsistent ontology rollback, stuc… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.7 | AGG | Design `eoip-admin support-bundle` producing an encrypted, redacted diagnostic bundle (logs, metrics, configuration) with consent and retention metada… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.8 | RES | Severity response objectives remain proposals until signed: CRAr (P1 1 h, P2 4 business hours, P3 2 business days) and AGG (P1 < 15 min 24x7, P2 < 1 b… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-038.A | MERGED | [CRAr] real drill of a source credential compromise, stuck publication and lost store. An authorized operator follows the runbook and proves recovery/… | WP-038 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.1 | CRAr | Generate published OpenAPI/JSON schemas and Python/TypeScript SDKs from the composed real application contract. Version public APIs, errors, events an… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.2 | CRAr | Expose authorized MCP tools with typed inputs/outputs, provenance and budgets. Tools cannot change trusted identity or obtain broader rights through n… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.3 | CRAr | Provide plugin/connector templates, synthetic fixtures, conformance runner, supported-version tables and a documented qualification process. Uncertifi… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.4 | CRAr | Generate ontology/API/help documentation from exact signed release artifacts, sanitize authored content and support offline/no-egress generation. Foll… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.5 | CRAr | Define contribution, vulnerability disclosure, ownership and marketplace policies consistent with proprietary core licensing and upstream obligations.… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.6 | AGG | Generated SDKs: TypeScript (proposed package `@eoip/sdk-typescript`) and Python (proposed `eoip-python`); names verified for availability and trademar… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.7 | OCA | MCP server (ONT-011) over existing `tools_contract/` and `sdk/` exposing ontology, graph and governed actions; actions invoked through MCP pass exactl… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.8 | OCA | Offline Widoco-class HTML ontology documentation generator (ONT-014) producing cross-referenced specs with diagrams and provenance from signed release… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-039.A | MERGED | [CRAr] independently build a client and sample plugin from released schemas/templates, run a real scoped task and reject deprecated/incompatible/unaut… | WP-039 | see WP | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-040.1 | CRAr | Classify source data and derivatives, record lawful/contractual handling policy, residence, retention, consent where applicable and legal holds. Code/… | WP-040 | tests/integration/test_erasure_cascade.py, tests/integration/test_no_egress.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-040.2 | CRAr | Enforce egress policy for connectors, parsers/imports, model calls, linting, telemetry, docs and support bundles. No-egress mode must be measured at t… | WP-040 | tests/integration/test_erasure_cascade.py, tests/integration/test_no_egress.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-040.3 | CRAr | Track all copies/derivatives including graph assertions/inferences, raw objects, indexes/vectors, caches, answers, exports, jobs, traces and backups. … | WP-040 | tests/integration/test_erasure_cascade.py, tests/integration/test_no_egress.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-040.4 | CRAr | Prevent replay, restore, re-embedding or resynchronization from resurrecting deleted/revoked content. Immutable history requires documented retention/… | WP-040 | tests/integration/test_erasure_cascade.py, tests/integration/test_no_egress.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-040.5 | CRAr | Support data-subject/administrative access and deletion workflows with authorization, audit, scoped reports and explicit conflict/escalation for legal… | WP-040 | tests/integration/test_erasure_cascade.py, tests/integration/test_no_egress.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-040.6 | AGG | Erasure cascade: a deletion request for a subject locates and processes every derivative across the eight graph planes (raw, canonical, schema referen… | WP-040 | tests/integration/test_erasure_cascade.py, tests/integration/test_no_egress.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-040.7 | AGG | No-egress verification: a network socket monitor records zero external bytes during a full ingestion plus GraphRAG cycle in no-egress mode; allowed de… | WP-040 | tests/integration/test_erasure_cascade.py, tests/integration/test_no_egress.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-040.A | MERGED | [CRAr] delete and revoke a subject/source while jobs and streams are active, restore/replay older state, then inspect every derivative and network log… | WP-040 | tests/integration/test_erasure_cascade.py, tests/integration/test_no_egress.py | design, implementation, positive, negative, review, integration, failure/recovery, deployment, performance |
| CRA-041.1 | RES | Maintain a versioned Claims Register in the repository (`docs/claims/claims-register.yaml`). Every externally visible statement about EOIP capability,… | WP-041 | tests/acceptance/, tests/ai/ | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-041.2 | RES | No standards-conformance claim (RDF 1.1, JSON-LD 1.1, OWL 2 profile, SHACL Core, SPARQL 1.1, WCAG 2.2 AA) may be published until the corresponding req… | WP-041 | tests/acceptance/, tests/ai/ | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-041.3 | RES | The seven inversions labelled 'already won' in the indicative analysis (I1, I3, I6, I13, I15, I16, I17) are hypotheses until re-verified on the pinned… | WP-041 | tests/acceptance/, tests/ai/ | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-041.4 | RES | The Ontology-as-Code positioning package (ONT-012) consists of: a factual capability description of the existing GitOps layer (branch, PR, review gate… | WP-041 | tests/acceptance/, tests/ai/ | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-041.5 | RES | Competitor performance, TCO, pricing or revenue figures that originate from vendor or self-interested sources (for example negotiation-consultancy TCO… | WP-041 | tests/acceptance/, tests/ai/ | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-041.6 | RES | Patent-candidate disclosure control: the five candidates listed in OCA section 8.3 (semver from semantic diff; migration-script generation from ontolo… | WP-041 | tests/acceptance/, tests/ai/ | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-041.7 | RES | Indicative scorecards (ontology-comparison-matrix.csv, the aggregated master matrix, EOIP self-scores 2.9/3.6/4.2) are internal planning aids. Any ext… | WP-041 | tests/acceptance/, tests/ai/ | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-041.A | MERGED | [RES] Attempt to publish (a) a SHACL conformance claim while CRA-020 is not ACCEPTED, (b) an 'already won' inversion without a receipt, (c) a competit… | WP-041 | tests/acceptance/, tests/ai/ | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-042.1 | RES | Maintain one research record per tool family C01-C55 under `research/competitive/<id>.yaml`: tool family, category, reviewed baseline date, pinned pro… | WP-042 | tests/research/test_validate_research.py | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-042.2 | RES | Keep the three scoring datasets separate and labelled: evidence-qualified (competitive-research-matrix.csv, 7 scored dimensions, 15 ND), indicative (o… | WP-042 | tests/research/test_validate_research.py | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-042.3 | RES | Resolve every item in the version and investigation register (CRA section 6.1): pin exact release, artifact checksum, source/license snapshot and life… | WP-042 | tests/research/test_validate_research.py | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-042.4 | RES | Re-verify each conflict-register item marked RESEARCH (licenses for WebProtégé, LODE, TerminusDB, FIBO, schema.org, Openllet, extract-msg; gist size; … | WP-042 | tests/research/test_validate_research.py | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-042.5 | RES | Perform hands-on qualification for every third-party engine EOIP will depend on or certify (at minimum rdflib, pySHACL, OWL API, ELK, Apache Jena/Fuse… | WP-042 | tests/research/test_validate_research.py | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-042.6 | RES | Record unavailable or contradictory sources (for example the OnToology site timing out, Fabric preview limits, vendor marketing scale claims) as expli… | WP-042 | tests/research/test_validate_research.py | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-042.7 | RES | Refresh every research record at least every 6 months or on a major competitor release; each refresh produces a dated delta entry. Stale records (>6 m… | WP-042 | tests/research/test_validate_research.py | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |
| CRA-042.A | MERGED | [RES] Run the research-dataset validator: every score is an integer 1-5 with rationale or `ND` with a named gap; no record lacks a reviewed date; no t… | WP-042 | tests/research/test_validate_research.py | design, implementation, positive, negative, review, workflow, review (Legal/Marketing) |

## Appendix B — External Inputs and Human Decisions That Block Clauses

Do not guess these. Record the decision in the ledger (`kind: decision`) with the decider, date and reference; until then dependent clauses remain BLOCKED and the agent continues with independent work.

| ID | Decision | Owner | Blocks |
|---|---|---|---|
| H-01 | Confirm target scale and whether stretch latency objectives (p95 < 20 ms) become binding | CTO | CRA-036, X-05/X-06 |
| H-02 | Air-gap: may customer deployments run JVM worker sidecars (ELK, OWL API, ROBOT)? | CTO / Security | CRA-019 |
| H-03 | Is write-back (CRA-027) in v1 scope or read-only until SOC 2? | Security Officer | CRA-027 |
| H-04 | TerminusDB license verification; remove or admit | Legal | CRA-035, X-21 |
| H-05 | Accept gating all standards messaging on certification (OR6) | Marketing + Legal | CRA-041 |
| H-06 | Identify Fortuna product, API, auth and data contract | Product owner | CRA-009, X-14 |
| H-07 | Identify the API Portal product(s) in use | Product owner | CRA-007, X-13 |
| H-08 | Approve support tiers, response objectives, availability and service credits | Commercial + Counsel | CRA-038, X-08 |
| H-09 | Clear extract-msg and other open component distribution terms | Legal | CRA-013/035, X-16 |
| H-10 | Approve staffing, rates and budget inputs for the cost model | Delivery manager | CRAr section 17 |
| H-11 | Approve vendor sandbox / licensed test access per named source | Procurement | CRA-005..009 |
| H-12 | Patent provisional filing decisions before any public disclosure | Legal / IP | CRA-041 |
| H-13 | Approve legal basis for Slack private channels / DMs if ever needed | Legal / Compliance | CRA-006 |
| H-14 | Choose the durable event backbone per deployment profile (DB outbox vs Kafka/Redpanda) | Architect | CRA-010/031, INV-44 |

## Appendix C — Prompt Template for a Coding Agent Session

```text
You are implementing EOIP/KGF requirement clauses from CRAr_cpccaggcc-requirements.md using
CRAr_cpccaggcc-implementation.md. Session scope: <WP-xxx / clause IDs>.
Rules: (1) proof is execution with receipts, never file or test names; (2) verify every search lead
before use; (3) no mocks, hashing fakes, in-memory fallbacks or skips to pass; (4) never change
expected results without an independent oracle; (5) extend canonical owners, do not duplicate;
(6) GPL/AGPL never linked; (7) gitops.py/manifest.py/packs.py via ports only; (8) mark BLOCKED with
the exact missing input when an external dependency is absent and continue other work.
Deliver: code + tests + receipts via tools/acceptance/run_and_receipt.py + ledger updates +
a short report listing clause states, receipts, failures and limitations. Do not report completion
percentages derived from file counts.
```

*End of implementation guide. The standard of completion is observable, reproducible and authorized behaviour in the actual supported deployment.*
