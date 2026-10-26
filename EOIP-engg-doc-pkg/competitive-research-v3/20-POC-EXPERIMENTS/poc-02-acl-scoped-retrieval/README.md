# POC-02: ACL-Scoped Retrieval (zero cross-user / cross-tenant leakage)

| Field | Value |
|---|---|
| Status | **SPECIFICATION ONLY — NOT EXECUTED.** Per `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md` §16 item 21, POC experiments in this package "run only if authorized and possible"; none is authorized in this research run. This README and `run_poc.py` describe a reproducible experiment design, not a result. No pass/fail outcome is reported here because none was produced. |
| Why this POC, not another | Of the P0 gaps in `07-GAP-REGISTER.md`, GAP-02 (source-ACL not enforced on deployed retrieval/answer/export/MCP paths) and GAP-03 (tenant isolation not enforced in graph adapters) are the two forced-P0, Critical-severity items with the clearest falsifiable benchmark already specified: `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-01 and INV-SELF-02 each name "two synthetic users/tenants with disjoint permissions; zero leaked facts is the pass condition" as their own benchmark. This POC is the smallest Docker-first reproduction of that benchmark, proving BM-04/BM-05 (`15-VALIDATION-BENCHMARK-PLAN.md`) are measurable at all before any larger investment in fixing the gap. |
| Validates | BM-04 (ACL/tenant leakage — retrieval) and BM-05 (ACL/tenant leakage — cross-tenant adversarial), as specified in `15-VALIDATION-BENCHMARK-PLAN.md`. |
| Gaps under test | GAP-02, GAP-03, and by extension GAP-34 (agent memory lacks ACL/tenant fields) for the memory-read case. |

## 1. Objective

Prove, with the smallest possible reproducible setup, that EOIP's retrieval path can be measured for cross-user and cross-tenant leakage — and, run against the code at HEAD 896e06d, is *expected* (per `01a-BASELINE-DELTA-HEAD.md` BL-18/BL-20/U-04) to **fail** the zero-leakage bar on the deployed API routes today, because:

- `retrieve()`'s source-ACL filter (`authz/pdp.py:107`, `authz/derivation_acl.py:167`) is reached only when a `scope` argument is passed, and no deployed route (`apps/api/extended.py:906-913`, `apps/api/main.py:1770` `/api/v1/rag`, `agents/governed.py:250`) passes it (GAP-02).
- Keyword, vector, and hybrid retrieval candidate stages filter by tenant ownership only (`owned_by`, `retrieval/tenant_index.py:30`), never by source ACL or classification.
- No graph adapter (`graph/hugegraph.py`, `graph/neo4j.py`, `graph/neptune.py`, `graph/memory.py`) contains any `tenant` reference (GAP-03).

This POC does not fix either gap. It specifies the fixture and the test that would **prove the gap exists** (today) and would later **prove it is closed** (once the INV-SELF-01/02 selected options are implemented), using the same fixture and the same script in both cases.

## 2. Experiment design

### 2.1 Fixture: two synthetic tenants, two synthetic users, one disjoint fact set

- **Tenant A**, **Tenant B** — two tenant contexts (`tenancy/context.py:36`).
- **User A1** (member of Tenant A, source-ACL clearance: `source:jira`, `source:confluence`), **User A2** (member of Tenant A, source-ACL clearance: `source:confluence` only — deliberately *not* `source:jira`).
- **User B1** (member of Tenant B, source-ACL clearance: `source:jira`, `source:confluence` — same clearance labels as User A1, but a different tenant, to isolate the tenant-leakage case from the source-ACL-leakage case).
- A small fact set (10-20 facts) ingested with `PermissionMetadata`/`acl_hash` (`contracts/source_event.py:42,50,74`) such that:
  - Half the facts are tagged `source:jira`, owned by Tenant A.
  - Half the facts are tagged `source:confluence`, owned by Tenant A.
  - A disjoint, structurally similar fact set is owned by Tenant B (same shape, different content, so a leak is unambiguous to detect — never the same literal string in both tenants' fact sets).
  - At least one fact is engineered to be reachable only via a derived/inferred edge (to exercise `authz/pdp.py:200-215`'s derived-fact ACL-inheritance path, not just direct-fact ACLs).

### 2.2 Retrieval call

One identical question, asked as:
1. User A1 (should see both `source:jira` and `source:confluence` facts, Tenant A only).
2. User A2 (should see `source:confluence` facts only, Tenant A only — the source-ACL leakage probe).
3. User B1 (should see Tenant B facts only, despite holding the same source-ACL clearance labels as User A1 — the tenant-isolation leakage probe).

Each call is made through every retrieval mode this POC can reach without a live model: keyword (BM25), vector (hashing embedder), hybrid (RRF), and graph-traversal (`retrieve()` with and without `scope` passed, to show the before/after of GAP-02's fix). The call is also made through the MCP tool surface (`apps/mcp/main.py`) if reachable in the test environment, to confirm the same leakage (or non-leakage) pattern holds there (GAP-09's shared-bearer-token caveat applies: MCP calls in this POC act as whatever principal the bootstrap token resolves to until GAP-09 is fixed, so the MCP leg of this POC is explicitly scoped as "MCP inherits the REST result" rather than an independent test, until T-04 in `16-SECURITY-PRIVACY-THREAT-MODEL.md` is closed).

### 2.3 Pass/fail script outline

A pass/fail script (`run_poc.py`) that, for each (user, retrieval mode) pair:
1. Issues the retrieval call.
2. Collects every fact, citation, cached entry, and (if reachable) agent-memory record surfaced in the response.
3. Diffs the surfaced set against the *expected-visible* set for that user (computed independently from the fixture's own ACL/tenant labels, not from the system under test).
4. Reports any surfaced item **not** in the expected-visible set as a **leak**, tagged with which user, which mode, and which fact leaked.
5. Exits non-zero if any leak is found, prints a per-mode leak-count table otherwise, and exits zero only when every mode shows exactly zero leaks for every user.

### 2.4 Docker-first reproduction (target shape, not yet built)

```
docker compose -f deploy/docker-compose.acceptance.yml up -d   # or a dedicated poc-02 compose overlay (TODO)
python 20-POC-EXPERIMENTS/poc-02-acl-scoped-retrieval/run_poc.py --seed-fixture
python 20-POC-EXPERIMENTS/poc-02-acl-scoped-retrieval/run_poc.py --run --mode all --report json
```

No compose overlay for this POC exists yet; `--seed-fixture` and `--run` are both unimplemented stubs in `run_poc.py` (see TODOs in that file). This section records the *intended* invocation shape for whoever implements it.

## 3. Expected outcome (a prediction, not a result)

Based on the static-code evidence already in `01a-BASELINE-DELTA-HEAD.md` (BL-18, BL-20, U-04, U-05), this POC is expected to show:
- User A2 receives `source:jira`-tagged facts it should not see, via the keyword/vector/hybrid candidate stages (which filter by tenant ownership only).
- User B1 receives no Tenant A facts (tenant ownership filtering is applied in those same stages), so the tenant-leakage probe is expected to pass *today* for the lexical/vector/hybrid modes, while the source-ACL probe is expected to fail.
- The graph-traversal mode without `scope` passed is expected to leak on both axes; with `scope` passed (manually, bypassing the production call sites), it is expected to correctly filter, because the underlying `authz/pdp.py`/`authz/derivation_acl.py` code is real and already unit-tested — it is simply not wired into any deployed caller.

This prediction is exactly the gap GAP-02/GAP-03 already document from code reading; this POC's purpose is to turn that code-reading finding into an executable, repeatable test, not to discover something new.

## 4. Out of scope for this POC

- Fixing GAP-02/GAP-03 (tracked in `16-SECURITY-PRIVACY-THREAT-MODEL.md` T-01/T-02 and `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-01/02).
- Load/scale testing (that is BM-05's Tier 2 "noisy neighbor" extension, not this minimal POC).
- MCP per-user authorization (GAP-09/T-04) — noted above as an explicit limitation, not solved here.
- Any live external backend (HugeGraph/Neo4j/Neptune) — this POC targets `MemoryGraphStore` first, per INV-SELF-01's own "(1) quick integration" sequencing, so the fixture is cheap to run before any infrastructure is needed.

## 5. How to run

```bash
python run_poc.py --help
```

`run_poc.py` is a stub: argument parsing and TODOs only, as required for this package (Master Prompt §16 item 21 — "run only if authorized and possible"; not authorized here). It prints `NOT EXECUTED` for every action and performs no network or filesystem mutation. No output of this script should be read as a benchmark result.
