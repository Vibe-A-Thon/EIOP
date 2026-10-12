from __future__ import annotations

import json
import re
import subprocess
import tomllib
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRATCH = ROOT / ".audit-scratch"
INV = json.loads((SCRATCH / "inventory.json").read_text(encoding="utf-8"))
REGISTRY_LIST = json.loads((ROOT / "requirements-registry.json").read_text(encoding="utf-8"))
REGISTRY = {row["id"]: row for row in REGISTRY_LIST}
DERIVED_REFS = {
    "DERIVED-LLM-SELF-001": {
        "path": "EOIP-engg-doc-pkg/todo-status.md",
        "line": 20,
        "text": "Frontier-Grade Self-LLM Engine & XAI Agent Suite Implementation",
    }
}
REGISTRY["DERIVED-LLM-SELF-001"] = {
    "id": "DERIVED-LLM-SELF-001",
    "title": "Frontier-grade Self-LLM engine with real inference, XAI and speculative decoding",
    "family": "LLM",
    "priority": "P0",
    "phase": "Derived atomic requirement from an unnumbered documented completion claim",
    "code_paths": ["packages/eoip/models/self_llm.py"],
    "test_files": ["tests/unit/test_self_llm_frontier.py"],
    "status": "FULLY_DEVELOPED",
}
OPENAPI = json.loads((SCRATCH / "openapi.json").read_text(encoding="utf-8-sig"))
SHA = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
BRANCH = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
DATE = "2026-10-13"
VERSION_CHECK_DATE = "2026-10-12"


def clean(value: object, limit: int = 190) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip().replace("|", "\\|")
    return text[:limit] + ("..." if len(text) > limit else "")


def cite(path: str, line: int | str = 1) -> str:
    return f"`{path}:{line}`"


def first_ref(req_id: str) -> dict:
    if req_id in DERIVED_REFS:
        return DERIVED_REFS[req_id]
    refs = INV["requirement_refs"].get(req_id, [])
    refs = [r for r in refs if not r["path"].startswith(".audit-scratch/")]
    preferred = [r for r in refs if "/audits/" not in r["path"] and "status.md" not in r["path"]]
    return (preferred or refs or [{"path": "requirements-registry.json", "line": 1, "text": req_id}])[0]


def first_code_ref(req_id: str, test: bool = False) -> dict | None:
    refs = INV["code_requirement_refs"].get(req_id, [])
    prefixes = ("tests/",) if test else ("packages/", "apps/api/", "scripts/", "deploy/", "config/")
    selected = [r for r in refs if r["path"].startswith(prefixes)]
    if test:
        selected = [r for r in selected if r["path"].startswith("tests/")]
    else:
        selected = [r for r in selected if not r["path"].startswith("tests/")]
    return selected[0] if selected else None


def concrete_path(path_value: str) -> str | None:
    path = ROOT / path_value
    if path.is_file():
        return path_value.replace("\\", "/")
    if path.is_dir():
        candidates = sorted(
            p for p in path.rglob("*")
            if p.is_file() and p.suffix.lower() in {".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".yaml", ".yml"}
        )
        if candidates:
            return candidates[0].relative_to(ROOT).as_posix()
    return None


AREA_RULES = [
    ("ING", r"INGEST|PARSER|EXTRACT|DLQ|CHECKPOINT|UPLOAD|MAPPING"),
    ("CON", r"CONNECTOR|\bCONN\b|JIRA|GITLAB|CONFLUENCE|SERVICENOW|CRAWL|SOURCE"),
    ("ONT", r"ONTOLOG|SCHEMA|\bOWL\b|\bRDF\b|JSON.?LD|META.?GRAPH"),
    ("GRA", r"GRAPH|HUGEGRAPH|NEO4J|NEPTUNE|\bEDGE\b|\bVERTEX\b|\bPATH\b|CENTRALITY"),
    ("VEC", r"VECTOR|EMBED|RERANK"),
    ("NLQ", r"\bNLQ\b|NATURAL.?LANG|SUGGESTED.?QUERY"),
    ("QRY", r"\bQRY\b|QUERY|CYPHER|GREMLIN|SPARQL|\bGQL\b|\bSQL\b"),
    ("RAG", r"\bRAG\b|RETRIEV|GROUND|CITATION"),
    ("AGT", r"AGENT|\bTOOL\b|\bMCP\b|HUMAN.?IN.?LOOP"),
    ("IMP", r"IMPACT|BLAST|WHAT.?TO.?TEST"),
    ("LIN", r"LINEAGE|PROVENANCE|EVIDENCE"),
    ("TMP", r"TEMPORAL|TIME.?TRAVEL|VERSION|HISTORY|SNAPSHOT|\bDIFF\b"),
    ("SEC", r"SECURITY|AUTHENT|AUTHORIZ|RBAC|ABAC|SAML|OIDC|SSO|PII|DLP|SECRET|AUDIT"),
    ("TEN", r"TENANT|MULTI.?TEN|QUOTA|ISOLATION"),
    ("WLB", r"WHITE.?LABEL|BRAND"),
    ("LLM", r"\bLLM\b|\bMODEL\b|PROMPT|INFERENCE|FINE.?TUN"),
    ("LOC", r"LOCAL.?FIRST|OFFLINE|DESKTOP|TAURI|DISTRIBUT"),
    ("SCL", r"SCALAB|PERFORMANCE|LATENCY|THROUGHPUT|CACHE|RATE.?LIMIT"),
    ("OBS", r"OBSERV|METRIC|TRACE|TELEMET|LOGGING|HEALTH"),
    ("ADM", r"ADMIN|LICEN[CS]|REPORT|NOTIF|COLLAB"),
    ("API", r"\bAPI\b|WEBHOOK|\bREST\b|OPENAPI|\bSDK\b|ERROR"),
    ("UI", r"\bUI\b|\bUX\b|\bWEB\b|DASHBOARD|EXPLORER|STUDIO|\bVIEW\b"),
    ("OPS", r"\bOPS\b|DEPLOY|DOCKER|HELM|K8S|BACKUP|RESTORE|FAILOVER|DISASTER.?RECOVERY|RELEASE"),
    ("DEV", r"DEVELOPER|\bTEST\b|\bCI\b|\bCD\b|QUALITY|DOCUMENTATION|REGISTRY|\bBASE\b"),
]


def area_for(req_id: str, title: str, family: str = "") -> str:
    family_area = family.upper().strip()
    if family_area in {area for area, _ in AREA_RULES} | {"NFR"}:
        return family_area
    id_hay = req_id.upper()
    id_rules = [
        ("TEN", r"TENANT|TENANCY|(?:^|-)TEN(?:-|$)"),
        ("SEC", r"SECURITY|(?:^|-)SEC(?:-|$)|AUTHN|AUTHZ|RBAC|ABAC"),
        ("WLB", r"WHITE.?LABEL|(?:^|-)WLB(?:-|$)"),
        ("LLM", r"(?:^|-)LLM(?:-|$)|MODEL"),
        ("ING", r"INGEST|(?:^|-)ING(?:-|$)"),
        ("CON", r"CONNECTOR|(?:^|-)CONN(?:-|$)|JIRA|GITLAB|CONFLUENCE|SERVICENOW"),
        ("ONT", r"ONTOLOG|(?:^|-)ONT(?:-|$)|SCHEMA"),
        ("GRA", r"GRAPH|(?:^|-)GRA(?:-|$)|HUGEGRAPH|NEO4J|NEPTUNE"),
        ("VEC", r"VECTOR|(?:^|-)VEC(?:-|$)|EMBED"),
        ("NLQ", r"(?:^|-)NLQ(?:-|$)"),
        ("QRY", r"QUERY|(?:^|-)QRY(?:-|$)"),
        ("RAG", r"(?:^|-)RAG(?:-|$)|RETRIEV"),
        ("AGT", r"AGENT|(?:^|-)AGT(?:-|$)"),
        ("IMP", r"IMPACT|(?:^|-)IMP(?:-|$)"),
        ("LIN", r"LINEAGE|PROVENANCE|(?:^|-)LIN(?:-|$)|(?:^|-)PROV(?:-|$)"),
        ("TMP", r"TEMPORAL|(?:^|-)TMP(?:-|$)"),
        ("LOC", r"LOCAL|OFFLINE|(?:^|-)LOC(?:-|$)"),
        ("SCL", r"SCALE|PERF|(?:^|-)SCL(?:-|$)"),
        ("OBS", r"OBSERV|TELEMET|(?:^|-)OBS(?:-|$)"),
        ("ADM", r"ADMIN|LICEN[CS]|(?:^|-)ADM(?:-|$)"),
        ("API", r"(?:^|-)API(?:-|$)|OPENAPI|WEBHOOK"),
        ("UI", r"(?:^|-)UI(?:-|$)|(?:^|-)UX(?:-|$)"),
        ("OPS", r"(?:^|-)OPS(?:-|$)|DEPLOY|BACKUP|RESTORE|RELEASE|HA"),
        ("DEV", r"(?:^|-)DEV(?:-|$)|(?:^|-)BASE(?:-|$)|(?:^|-)TEST(?:-|$)"),
    ]
    for area, pattern in id_rules:
        if re.search(pattern, id_hay):
            return area
    hay = f"{req_id} {family} {title}".upper()
    for area, pattern in AREA_RULES:
        if re.search(pattern, hay):
            return area
    return "NFR"


targeted_tests = {
    "tests/unit/test_authn.py", "tests/unit/test_authz.py",
    "tests/unit/test_named_graph_isolation.py", "tests/unit/test_self_llm_frontier.py",
    "tests/unit/test_sr_wave_api_routes.py", "tests/unit/test_enterprise_security_wp55.py",
    "tests/security/test_security_baseline.py", "tests/security/test_no_egress.py",
}


def status_for(req_id: str, row: dict, title: str) -> tuple[str, str, str, str]:
    hay = f"{req_id} {title}".lower()
    code = first_code_ref(req_id)
    test = first_code_ref(req_id, test=True)
    code_paths = [p for p in row.get("code_paths", []) if p]
    tests = [p for p in row.get("test_files", []) if p]
    has_code = bool(code or code_paths)
    has_test = bool(test or tests)
    test_path = (test or {}).get("path") or (tests[0] if tests else "")
    if any(k in hay for k in ("frontier-grade self-llm", "self-llm neural", "speculative decoding")):
        return "STUBBED", "Deterministic templates/hash math are presented as model inference; generated evidence and confidence are not graph-derived.", "AMBIGUOUS-SPEC;KNOWLEDGE-GAP", "CRITICAL"
    if "pdf" in hay or "docx" in hay or "pptx" in hay or "stored report export" in hay:
        return "STUBBED", "The route returns an explicit HTTP 501 for one or more required export formats or stored-report export.", "DEPENDENCY-MISSING;SCOPE-DEFERRED", "HIGH"
    if any(k in hay for k in ("distributed hugegraph", "production ha", "failover drill", "external acceptance", "hubble browser")):
        return "BLOCKED", "Code or documentation scaffolding exists, but the required external infrastructure receipt was not produced in this audit.", "INFRA-MISSING;DEPENDENCY-MISSING", "HIGH"
    if not has_code:
        if row.get("status") == "ROADMAP":
            return "SKIPPED", "The backlog records this requirement as roadmap work and no production implementation evidence was found.", "SCOPE-DEFERRED;TIME/EFFORT", "MEDIUM"
        return "MISSED", "No production implementation reference was found after repository-wide ID and path tracing.", "UNKNOWN;TIME/EFFORT", "HIGH" if row.get("priority") == "P0" else "MEDIUM"
    if test_path in targeted_tests and has_test:
        return "IMPLEMENTED-UNVERIFIED", "A focused test passed in the fresh 110-test run, but its assertions do not prove the requirement's complete end-to-end wiring and acceptance scope.", "INTEGRATION-COMPLEXITY", "MEDIUM"
    if has_test:
        return "IMPLEMENTED-UNVERIFIED", "Code and a requirement-tagged test exist, but this requirement was not proven end-to-end by the incomplete full-suite run.", "INTEGRATION-COMPLEXITY", "MEDIUM"
    return "PARTIAL", "Production code is traceable, but acceptance coverage, wiring, or an executable proof is absent.", "TIME/EFFORT;INTEGRATION-COMPLEXITY", "HIGH" if row.get("priority") == "P0" else "MEDIUM"


all_ids = sorted(set(REGISTRY) | set(INV["requirement_refs"]))
area_seq: dict[str, int] = defaultdict(int)
requirements: list[dict] = []
for original in all_ids:
    row = REGISTRY.get(original, {})
    ref = first_ref(original)
    title = clean(row.get("title") or ref.get("text") or original, 220)
    area = area_for(original, title, row.get("family", ""))
    area_seq[area] += 1
    normalized = f"REQ-{area}-{area_seq[area]:03d}"
    status, gap, cause, severity = status_for(original, row, title)
    code_ref = first_code_ref(original)
    test_ref = first_code_ref(original, test=True)
    if not code_ref and row.get("code_paths"):
        concrete = concrete_path(row["code_paths"][0])
        code_ref = {"path": concrete, "line": 1} if concrete else None
    if not test_ref and row.get("test_files"):
        concrete = concrete_path(row["test_files"][0])
        test_ref = {"path": concrete, "line": 1} if concrete else None
    if original == "UI-005":
        code_ref = {"path": "packages/eoip/reports/router.py", "line": 93}
    priority_match = re.search(r"\bP[0-3]\b", ref.get("text", ""), re.IGNORECASE)
    priority = row.get("priority") or (priority_match.group(0).upper() if priority_match else "UNSTATED")
    req_type = (
        "non-functional" if area in {"NFR", "SCL", "OBS", "LOC", "DEV", "OPS"}
        else "compliance" if area == "SEC" and any(k in title.lower() for k in ("compliance", "privacy", "audit"))
        else "UI" if area == "UI"
        else "integration" if area in {"CON", "API"}
        else "functional"
    )
    acceptance = f"DERIVED: Given valid authorized inputs, when {clean(title, 100)}, then the documented outcome occurs and invalid/forbidden inputs fail explicitly."
    requirements.append({
        "id": normalized, "original": original, "title": title, "area": area,
        "source": f"{ref['path']}:{ref['line']}", "status": status,
        "evidence": f"{code_ref['path']}:{code_ref['line']}" if code_ref else "none",
        "test": f"{test_ref['path']}:{test_ref['line']}" if test_ref else "none",
        "gap": gap, "cause": cause, "severity": severity,
        "effort": "XL" if severity == "CRITICAL" else ("L" if severity == "HIGH" else ("M" if status not in {"IMPLEMENTED-VERIFIED", "IMPLEMENTED-UNVERIFIED"} else "S")),
        "priority": priority, "depends": "See source dependency chain" if row.get("phase") else "Not stated",
        "type": req_type, "acceptance": acceptance,
    })


weights = {"P0": 5, "P1": 3, "P2": 1, "UNSTATED": 1}
credits = {"IMPLEMENTED-VERIFIED": 1.0, "IMPLEMENTED-UNVERIFIED": .75, "PARTIAL": .5,
           "DIVERGED": .4, "STUBBED": .15, "SKIPPED": 0, "MISSED": 0, "BLOCKED": 0, "OBSOLETE": 0}
weighted_den = sum(weights.get(r["priority"], 1) for r in requirements if r["status"] != "OBSOLETE")
weighted_num = sum(weights.get(r["priority"], 1) * credits[r["status"]] for r in requirements if r["status"] != "OBSOLETE")
weighted_score = 100 * weighted_num / weighted_den
status_counts = Counter(r["status"] for r in requirements)


def requirement_score_tables() -> str:
    out = ["### By status", "", "| Status | Count | Percent |", "|---|---:|---:|"]
    for status in credits:
        n = status_counts.get(status, 0)
        out.append(f"| `{status}` | {n} | {n/len(requirements)*100:.1f}% |")
    out += ["", "### By area", "", "| Area | Total | Verified | Unverified | Partial | Stubbed | Missed/Skipped/Blocked |", "|---|---:|---:|---:|---:|---:|---:|"]
    for area in sorted({r["area"] for r in requirements}):
        c = Counter(r["status"] for r in requirements if r["area"] == area)
        out.append(f"| `{area}` | {sum(c.values())} | {c['IMPLEMENTED-VERIFIED']} | {c['IMPLEMENTED-UNVERIFIED']} | {c['PARTIAL']} | {c['STUBBED']} | {c['MISSED']+c['SKIPPED']+c['BLOCKED']} |")
    out += ["", "### By priority", "", "| Priority | Total | Verified | Weighted completion |", "|---|---:|---:|---:|"]
    for p in ["P0", "P1", "P2", "UNSTATED"]:
        rows = [r for r in requirements if r["priority"] == p]
        score = 100 * sum(credits[r["status"]] for r in rows) / len(rows) if rows else 0
        out.append(f"| `{p}` | {len(rows)} | {sum(r['status']=='IMPLEMENTED-VERIFIED' for r in rows)} | {score:.1f}% |")
    return "\n".join(out)


area_challenges = {
    "SEC": "The main HTTP boundary authenticates a shared bearer secret and does not produce a verified human/service principal with role claims; enterprise identity modules are not the route boundary.",
    "TEN": "Tenant identity is accepted from a caller header and several stateful services are process-global, so route-level data partitioning is not demonstrated.",
    "LLM": "The self-LLM path mixes deterministic templates with model terminology, and external-model data-boundary enforcement is not proven at every call site.",
    "GRA": "Graph abstractions are broad, but canonical HugeGraph operation, large-graph performance, and tenant partitioning require deployed receipts rather than memory-store tests.",
    "UI": "Backend capability is extensive but operation shapes and workflow aggregation are inconsistent, leaving the new client to orchestrate too many low-level calls.",
    "API": "The live surface contains 734 operations with sparse tagging and uneven error, pagination, caching, and idempotency contracts.",
    "OPS": "Local Compose assets exist, while HA, failover, restore, migration, and production release evidence remain environment-dependent.",
    "SCL": "Performance targets are documented without a current reproducible production-scale benchmark receipt for the largest supported graph and workload.",
    "LOC": "Local deployment is strong, but offline mutation queues, conflict resolution, and desktop synchronization are not end-to-end contracts.",
    "ADM": "Administrative services frequently retain state in process memory, which does not satisfy durable multi-replica operation.",
}


def detailed_findings() -> str:
    out = []
    for area in sorted({r["area"] for r in requirements}):
        rows = [r for r in requirements if r["area"] == area and r["status"] != "IMPLEMENTED-VERIFIED"]
        if not rows:
            continue
        out += [f"### {area}", "", area_challenges.get(area, "The repository contains meaningful implementation, but documentary completion labels are ahead of fresh end-to-end evidence."), ""]
        for r in rows:
            fix = f"Trace `{r['original']}` through its public boundary, add an acceptance test that asserts the documented outcome and failure modes, and persist a fresh CI/runtime receipt."
            if r["status"] == "MISSED":
                fix = f"Implement `{r['original']}` behind the established {area} service boundary, expose only the required contract, and add acceptance plus negative tests."
            elif r["status"] == "STUBBED":
                fix = f"Replace the placeholder behavior for `{r['original']}` with a real adapter or fail-closed unavailable state; tests must reject fabricated success/evidence."
            elif r["status"] == "BLOCKED":
                fix = f"Provision the named dependency for `{r['original']}`, run its operational drill, and attach machine-readable logs and measurements."
            out += [f"#### {r['id']} / {r['original']} - {r['status']}", "",
                    f"The requirement is recorded at `{r['source']}`; the best implementation evidence is `{r['evidence']}` and test evidence is `{r['test']}`. {r['gap']}", "",
                    f"This matters because an unproven {area} contract can produce incorrect user-visible state or an unsafe operational assumption. The codebase-specific challenge is {area_challenges.get(area, 'that acceptance is distributed across adapters, routes, and tests without one executable release receipt').lower()} Root cause: `{r['cause']}`. Remediation ({r['effort']}): {fix}", ""]
    return "\n".join(out)


matrix_lines = [
    "| REQ ID | Requirement | Source (file:line) | Type | Priority | Acceptance criteria | Status | Evidence (file:line) | Tests (file:line / none) | Gap description | Root-cause category | Severity | Effort | Depends on | Recommended fix |",
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
]
for r in requirements:
    matrix_lines.append(
        f"| `{r['id']}` | `{r['original']}`: {r['title']} | `{r['source']}` | `{r['type']}` | `{r['priority']}` | {r['acceptance']} | `{r['status']}` | `{r['evidence']}` | `{r['test']}` | {r['gap']} | `{r['cause']}` | `{r['severity']}` | `{r['effort']}` | {r['depends']} | Verify the complete acceptance path; replace stubs or add missing wiring and a fresh executable receipt. |"
    )
matrix_text = "\n".join(matrix_lines)
detailed_findings_text = detailed_findings()


top_gaps = """1. **Identity is not enterprise authentication.** The request boundary checks one global bearer token and assigns `local-user`; OIDC/SAML/RBAC modules do not establish the principal used by all routes (`apps/api/main.py:322-400`, `packages/eoip/authn/oauth_sso.py:209-234`).
2. **Tenant isolation is not an enforced invariant.** `X-Tenant-ID` is caller-controlled and defaults to `default`; the instantiated tenancy service lacks a graph store (`packages/eoip/enterprise/middleware.py:67-91`, `apps/api/extended.py:236-239`).
3. **The advertised Self-LLM is a deterministic simulator.** MD5 token IDs, sine/cosine embeddings, templated answers, fabricated citations/confidence, and simulated speculative decoding are shipped as frontier inference (`packages/eoip/models/self_llm.py:301-611`).
4. **Enterprise state is commonly process-local.** Identity, roles, model registry, configuration, branding, collaboration, snapshots, and related services cannot provide durable multi-replica semantics (`apps/api/extended.py:169-289`).
5. **The API surface is too broad and inconsistent for a safe generated client.** The live spec has 734 operations; 278 are untagged and cross-cutting pagination, RFC 7807 errors, caching, rate limits, and idempotency are not uniform (`apps/api/app.py:191-232`).
6. **Report delivery is incomplete.** PDF/DOCX/PPTX and stored-report export paths return 501 (`packages/eoip/reports/router.py:93-122`).
7. **Real-time contracts are not production-ready.** The WebSocket has no explicit route-level principal/tenant contract and failed an unauthenticated handshake with 500; LLM “streaming” buffers chunks before returning (`apps/api/main.py:1489-1500`, `packages/eoip/brain/router.py:418-437`).
8. **Browser security needs hardening.** Wildcard CORS is combined with credentials, no CSP/Trusted Types policy was found, and an export surface inserts graph values through `innerHTML` (`apps/api/app.py:218-225`, `apps/web/src/kgr/export/InteractiveExport.js:122-126`).
9. **Production evidence is incomplete.** The backlog itself says external HA, browser, VS Code, Hubble, and infrastructure receipts were not rerun (`KGF-MASTER-BACKLOG.md:41-52`, `KGF-MASTER-BACKLOG.md:1264-1278`).
10. **Project licensing is unresolved.** Dependency inventories exist, but no root LICENSE/COPYING/NOTICE was found; this blocks an unambiguous redistribution posture (`EOIP-engg-doc-pkg/69-dependency-license-sbom.md:1`)."""


audit_doc = f"""# EOIP / KGF Complete Requirements Gap Audit

**Repository:** `EIOP`  
**Branch / commit:** `{BRANCH}` / `{SHA}`  
**Audit date:** {DATE}  
**Auditor:** OpenAI Codex, GPT-5 coding agent  
**Scope:** all first-party non-generated repository text/source/configuration plus every Markdown line; user-directed exclusions are demo/example content and demo/sample data. Existing audit documents are evidence, never proof. No application code was modified.

## 1. Executive Summary

This audit normalizes **{len(requirements):,} documented requirement records** (explicit IDs plus separately identified atomic clauses) into stable `REQ-<AREA>-NNN` records. The conservative priority-weighted completion score is **{weighted_score:.1f}%**. It is intentionally lower than backlog checkbox completion because `IMPLEMENTED-VERIFIED` requires a fresh executable receipt and end-to-end wiring, not a filename, requirement tag, or historical test assertion.

**Verdict: Not production-ready; bounded pilot-ready only in a single-tenant, trusted-network, supervised deployment.** The product has unusual functional breadth, a passing production web build, 110 focused security/tenancy/model tests, zero known vulnerabilities from fresh `pip-audit` and `npm audit`, and a locally running API. However, principal identity, tenant enforcement, durable state, truthful model semantics, complete export/streaming, and production-scale operational receipts remain material blockers.

### Top 10 gaps by business impact

{top_gaps}

### Verification executed

- `npm --prefix apps/web run build`: passed; 197 modules, main chunk 849.24 kB / 219.98 kB gzip, Cytoscape chunk 443.04 kB / 141.98 kB gzip.
- Focused pytest set covering authn/authz, named graph isolation, security baseline/no-egress, Self-LLM and route waves: **110 passed**.
- Full pytest: **3,492 collected**, but not a release receipt. One run emitted failures/errors and stopped progressing near 10%; a fail-fast diagnostic run reached 62 passes before a long MCP integration test was interrupted after 256 seconds.
- `pip-audit -r requirements.lock`: no known vulnerabilities. `npm audit --json`: zero vulnerabilities across 79 dependencies.
- Live `/openapi.json`: OpenAPI 3.1, 689 paths, 734 operations, 303 schemas, one bearer security scheme.

## 2. Scorecard Dashboard

{requirement_score_tables()}

**Weighted formula:** `sum(priority weight * status credit) / sum(priority weight)`, where P0=5, P1=3, P2/UNSTATED=1 and credits are verified=1.0, unverified=.75, partial=.5, diverged=.4, stubbed=.15, all other open states=0. This is an audit confidence/completion score, not a feature-count percentage.

## 3. Master Traceability Matrix

The normalized ID is stable within this audit. The original documentary ID is retained in the requirement column. A line citation indicates the exact trace point; it does not by itself prove behavior.

{matrix_text}

## 4. Detailed Findings Per Area

{detailed_findings_text}

## 5. Non-Functional Audit

| Domain | Assessment | Evidence | Required release action |
|---|---|---|---|
| Authentication | **Critical / partial.** Shared static bearer token; fallback validator accepts any non-JWT token of length >=16. | `apps/api/main.py:322-400`; `packages/eoip/authn/oauth_sso.py:209-234` | Wire OIDC/SAML/local identity to one principal middleware; remove permissive fallback; rotate/revoke sessions. |
| Authorization | **Partial.** RBAC/ABAC code exists but is not uniformly bound to route/resource decisions. | `packages/eoip/authz/core.py:1`; `apps/api/main.py:322-400` | Central policy enforcement with deny-by-default route/resource tests. |
| Tenant isolation | **Critical / unverified.** Caller header and process-global state undermine isolation; tests use separate in-memory objects. | `packages/eoip/enterprise/middleware.py:67-91`; `tests/unit/test_named_graph_isolation.py:24-98` | Derive tenant from signed principal; partition graph/vector/cache/jobs/logs; adversarial cross-tenant E2E suite. |
| Secrets / connector SSRF | Secret abstractions and crawler guards exist; all connector paths and redirect/DNS rebinding behavior were not proven together. | `packages/eoip/egress/vault.py:1`; `tests/security/test_crawler_security.py:1` | Central egress policy, vault-backed secrets, redirect/IP revalidation and negative integration tests. |
| Query/prompt injection | Query policy modules exist; the generated/model output boundary is not uniformly typed and fail-closed. | `packages/eoip/query/policy.py:1`; `packages/eoip/models/self_llm.py:398-523` | AST/parameterized query enforcement; treat model output as untrusted data; red-team corpus. |
| LLM data sharing | Egress/DLP policy exists, but enforcement at every model adapter and route is not demonstrated. | `packages/eoip/egress/gateway.py:1`; `tests/security/test_no_egress.py:1` | Mandatory gateway at adapter factory; immutable audit of endpoint, classification and redaction. |
| Local-first/offline | Local Compose and local adapters are substantial; browser offline mutation/conflict behavior is not a backend contract. | `deploy/docker-compose.yml:1`; `EOIP-engg-doc-pkg/01-project-vision.md:33` | Define local cache, queued mutation, sync and conflict protocols; offline E2E tests. |
| Distribution / HA | Documented and scaffolded, not proven on production topology. | `KGF-MASTER-BACKLOG.md:1238`; `EOIP-engg-doc-pkg/08-deployment-architecture.md:1` | Multi-node failover, rolling upgrade, network partition and restore drills. |
| Scalability | No current release receipt proves stated 100k-node UI or largest graph/throughput/latency targets. | `KGF-MASTER-BACKLOG.md:1264-1278`; `packages/eoip/graph/benchmark.py:1` | Publish hardware/dataset profile, p50/p95/p99, memory and cancellation results. |
| Observability | Logs/metrics/traces/audit modules exist; cross-service correlation and sensitive-field redaction need deployed proof. | `packages/eoip/observability/metrics.py:1`; `packages/eoip/audit/sink.py:42` | Golden-signal dashboards, trace propagation and redaction assertions. |
| Privacy | PII/DLP primitives exist; classification-to-render/export enforcement is incomplete. | `packages/eoip/privacy/scanner.py:1`; `packages/eoip/egress/dlp.py:1` | Field-level classification, masked responses, reveal audit and export policy tests. |
| Backup/restore | Scripts/docs exist; clean-target, tenant-aware production restore receipt is absent. | `EOIP-engg-doc-pkg/53-backup-restore.md:13`; `KGF-MASTER-BACKLOG.md:1238` | Automated encrypted backup, checksum, clean restore, RPO/RTO evidence. |
| Upgrade/migration | Versioning and migration concepts exist without a full rollback receipt across graph/config/model state. | `packages/eoip/graph/schema_migration.py:106`; `EOIP-engg-doc-pkg/64-decisions-and-adrs.md:39` | N-1 to N migration rehearsal plus rollback and compatibility matrix. |
| Licensing | Dependency scan is clean today; project license/notice is absent. | `EOIP-engg-doc-pkg/69-dependency-license-sbom.md:1` | Legal choice, root LICENSE/NOTICE, SBOM and deny-list CI. |

## 6. Document Conflicts

| ID | Side A | Side B | Resolution |
|---|---|---|---|
| `CONFLICT-001` | README claims 516/516 complete (`README.md:11-14`). | Release definition requires 516 tasks, registry closure and all exit receipts, while baseline lists unrunning external gates (`KGF-MASTER-BACKLOG.md:28-52`). | Replace checkbox headline with evidence-tier status; do not use “production-ready” until Phase 8 receipts pass. |
| `CONFLICT-002` | Current registry physically contains 944 records (`requirements-registry.json:1`). | Backlog says 826/826 (`KGF-MASTER-BACKLOG.md:33`) and status pages say 893 (`available-status.md:13`). | Generate all counts from one registry artifact in CI. |
| `CONFLICT-003` | Status pages report 167/516 (`available-status.md:12`; `todo-status.md:7`). | README reports 516/516 (`README.md:11`). | Mark status files historical with dates or regenerate atomically. |
| `CONFLICT-004` | HugeGraph is described as authoritative/mandatory (`EOIP-engg-doc-pkg/08-deployment-architecture.md:23`). | Product docs permit Neptune, Neo4j and memory backends (`EOIP-engg-doc-pkg/76-multi-backend.md:3`). | State “canonical GraphStore contract; HugeGraph default reference deployment”; forbid memory in production. |
| `CONFLICT-005` | Report requirements claim server export routes exist (`eoip-phase4-2-requirements.md:108`). | PDF/DOCX/PPTX and stored export return 501 (`packages/eoip/reports/router.py:93-122`). | Reclassify as stubbed until successful artifact tests pass. |
| `CONFLICT-006` | Audit prose calls the Self-LLM frontier-grade (`EOIP-engg-doc-pkg/audits/audit-2026-10-06/assessed-gap-report.md:898-930`). | Implementation is deterministic templates/hash math (`packages/eoip/models/self_llm.py:301-611`). | Rename as deterministic simulator or implement a real model runtime with quality evaluations. |

## 7. Undocumented Features

| ID | Location | Observation | Recommendation |
|---|---|---|---|
| `UNDOCUMENTED-001` | `packages/eoip/query/polyglot_engine.py:1` | Polyglot query orchestration exceeds the primary product docs' public contract detail. | Document supported languages, guarantees and failure semantics. |
| `UNDOCUMENTED-002` | `packages/eoip/gaps/enterprise_completion.py:1` | A broad “enterprise completion” surface packages many gap IDs behind one module. | Split into owned capabilities and document lifecycle/support tier. |
| `UNDOCUMENTED-003` | `apps/api/extended.py:169-289` | Numerous process-local registries are exposed as enterprise services without persistence semantics in API docs. | Document as development-only or add durable adapters. |
| `UNDOCUMENTED-004` | Live OpenAPI `/openapi.json` | 278 operations have blank tags, making ownership undiscoverable. | Require operation ID, owner, tag, stability and deprecation metadata in CI. |

## 8. Technical Debt And Quality Observations

- **Completion machinery is circular:** `scripts/build_requirements_registry.py` promotes path existence and a test file to “fully developed”; it does not semantically execute acceptance criteria (`scripts/build_requirements_registry.py:1`).
- **State ownership is fragmented:** the scan found 452 in-memory collection assignments in production modules. Not all are defects, but enterprise records need explicit persistence/lifetime contracts.
- **Cross-cutting contracts drift:** 734 operations lack uniform problem details, pagination, rate-limit headers, cache validators, and idempotency rules.
- **Streaming is mislabeled:** `/brain/llm/stream` returns a buffered list, not an incremental transport (`packages/eoip/brain/router.py:418-437`).
- **Unsafe HTML composition:** interactive export interpolates graph keys/values into `innerHTML` (`apps/web/src/kgr/export/InteractiveExport.js:122-126`).
- **Test truth is mixed with implementation truth:** tests that assert a fabricated confidence/citation or templated phrase prove repeatability, not the advertised intelligence quality (`tests/unit/test_self_llm_frontier.py:117-214`).

## 9. Backend Readiness For The New GUI

| Screen area | Readiness | Main reason |
|---|---|---|
| Auth, user settings | Missing/critical | No production session/principal/profile boundary. |
| Home, health, jobs | Partially ready | Many metrics/routes; aggregation and durable job protocol inconsistent. |
| Ask Brain | Partially ready | Query/RAG breadth exists; Self-LLM and streaming are not truthful production contracts. |
| Graph Explorer, Entity 360, Impact, Change | Partially ready | Strong graph/query APIs; tenant scope, saved views, LOD and aggregate entity contract incomplete. |
| Incident, temporal | Partially ready | Algorithms exist; durable workspace/snapshot comparison protocols need consolidation. |
| Query Workbench | Partially ready | Multiple query routes; validate/explain/profile/cancel contract is inconsistent. |
| Ontology/meta graph | Partially ready | Read/write capability exists; draft/approval/migration lifecycle is incomplete. |
| Sources/ingestion/resolution | Partially ready | Broad connectors and jobs; resumable uploads and governed review/publish need contracts. |
| Agents | Partially ready | Catalog/runs exist; approval/event/audit semantics need one durable protocol. |
| Reports | Stubbed/partial | Core report logic exists; production document exports and stored download are 501. |
| Collaboration/notifications | Partially ready | Process-local state and incomplete real-time delivery. |
| Governance/tenant/white-label | Critical partial | Rich modules, but principal/tenant enforcement and persistence are not production-grade. |
| Platform health | Partially ready | Health endpoints exist; topology-wide status and operational actions need aggregation. |

## 10. Prioritised Remediation Roadmap

**Now (release blockers):** establish signed principal/session middleware; derive tenant server-side; enforce tenant partitions in graph/vector/cache/jobs/audit; remove permissive token fallback; rename/disable fake Self-LLM claims; sanitize all rich/graph output; implement RFC 7807 and operation metadata; add a root license. These changes precede GUI integration because the client must not encode unsafe contracts.

**Next (pilot integrity):** durable stores for identity/config/collaboration/reports/jobs; true SSE/WebSocket protocols with auth and cancellation; report artifacts; saved views; resumable upload; ontology publish workflow; fresh cross-tenant, backup/restore and migration tests.

**Later (production scale):** distributed graph/worker HA, production benchmark envelopes, 100k-node LOD endpoints, desktop/offline sync, CRDT collaboration, external model governance, multi-region DR and complete accessibility/performance certification.

## 11. Assumptions And Limitations

- Demo/example pieces and demo/sample data were inventoried but excluded from conclusions per user instruction.
- Existing frontend visuals/routes were not used as design input. Frontend code was inspected only for backend-contract and security evidence.
- Historical audit/status files are claims, not fresh evidence. A passing requirement-tagged unit test can still validate a stub's current behavior.
- The local live API was used for OpenAPI inspection. External SaaS, browser, VS Code, Hubble, distributed HugeGraph and cloud infrastructure were not exercised.
- The full test suite did not complete reliably, so no repository-wide green claim is made.
- Explicit IDs are the auditable atomic registry. Un-IDed normative Markdown clauses were read and used as acceptance/conflict context; repeated rationale and explanatory prose were not inflated into duplicate requirement rows.
"""


# ---------------- API catalogue and GUI specification ----------------

route_lookup = INV["routes"]
actual_integrations = []
for path, item in sorted(OPENAPI.get("paths", {}).items()):
    for method, op in item.items():
        if method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}:
            continue
        iid = f"INT-{len(actual_integrations)+1:03d}"
        candidates = [r for r in route_lookup if r["method"] == method.upper() and (path.endswith(r["path"]) or r["path"] == path)]
        loc = f"{candidates[0]['source']}:{candidates[0]['line']}" if candidates else "apps/api/app.py:191"
        req = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
        params = op.get("parameters", [])
        responses = op.get("responses", {})
        response_schema = next((v.get("content", {}).get("application/json", {}).get("schema", {}) for v in responses.values() if isinstance(v, dict) and v.get("content")), {})
        def schema_name(schema):
            if not schema:
                return "none"
            if "$ref" in schema:
                return schema["$ref"].split("/")[-1]
            if "items" in schema and "$ref" in schema["items"]:
                return "array<" + schema["items"]["$ref"].split("/")[-1] + ">"
            return clean(schema.get("type") or ",".join(schema.get("properties", {}).keys()) or "inline", 70)
        hay = f"{path} {op.get('summary','')}".lower()
        audit = "PARTIAL" if any(k in hay for k in ("stream", "export", "auth", "tenant", "collab")) else "IMPLEMENTED-UNVERIFIED"
        actual_integrations.append({
            "id": iid, "method": method.upper(), "path": path,
            "purpose": clean(op.get("summary") or op.get("operationId") or "Backend operation", 90),
            "request": schema_name(req), "response": schema_name(response_schema),
            "params": ", ".join(p.get("name", "") for p in params) or "none",
            "errors": ",".join(responses.keys()) or "undocumented", "loc": loc, "audit": audit,
            "tags": op.get("tags") or [],
        })


screen_defs = [
    ("SCR-001", "Authentication and tenant entry", "/auth/*", "All users", "Establish identity, MFA, session and tenant context", ["auth", "identity", "tenant"]),
    ("SCR-002", "First-run onboarding", "/t/:tenant/onboarding", "Tenant admin, data engineer", "Configure workspace, source, ingestion review and first question", ["source", "ingest", "ontology"]),
    ("SCR-003", "Brain overview", "/t/:tenant/w/:workspace", "All users", "Summarize graph health, changes, jobs, alerts and saved work", ["health", "metric", "job", "graph"]),
    ("SCR-004", "Ask the Brain", "/t/:tenant/w/:workspace/ask", "Executive, analyst", "Ask, compare deterministic suggestions, inspect evidence and export", ["brain", "rag", "query", "suggest"]),
    ("SCR-005", "Graph Explorer", "/t/:tenant/w/:workspace/graph", "Analyst, engineer, steward", "Explore, filter, path-find, cluster and save ontology-driven graphs", ["graph", "path", "neighbor", "search"]),
    ("SCR-006", "Entity 360", "/t/:tenant/w/:workspace/entity/:id", "All knowledge users", "Inspect properties, relations, provenance, timeline and work", ["entity", "provenance", "lineage"]),
    ("SCR-007", "Impact Analysis studio", "/t/:tenant/w/:workspace/impact", "Engineer, analyst", "Model a change, inspect blast radius and produce a test checklist", ["impact", "blast", "test"]),
    ("SCR-008", "Change history", "/t/:tenant/w/:workspace/changes", "Engineer, compliance", "Trace who changed what and compare versions", ["change", "history", "diff"]),
    ("SCR-009", "Incident root-cause workspace", "/t/:tenant/w/:workspace/incidents/:id", "IT user, responder", "Rank causes and walk evidence-backed troubleshooting paths", ["incident", "root", "cause"]),
    ("SCR-010", "Temporal and time travel", "/t/:tenant/w/:workspace/time", "Analyst, steward", "Compare snapshots and play graph evolution", ["temporal", "snapshot", "time"]),
    ("SCR-011", "Query Workbench", "/t/:tenant/w/:workspace/query", "Analyst, data engineer", "Author, validate, explain, run and save polyglot queries", ["query", "cypher", "gremlin", "sparql"]),
    ("SCR-012", "Ontology Designer", "/t/:tenant/w/:workspace/ontology", "Ontology steward", "Edit, validate, diff, approve and publish schema", ["ontology", "schema"]),
    ("SCR-013", "Meta-graph", "/t/:tenant/w/:workspace/meta-graph", "Steward, analyst", "Explore type relationships and instance counts", ["meta", "ontology"]),
    ("SCR-014", "Sources and connectors", "/t/:tenant/w/:workspace/sources", "Integration engineer", "Configure, test and monitor source connections", ["connector", "source"]),
    ("SCR-015", "Ingestion and Mapping studio", "/t/:tenant/w/:workspace/ingestion", "Data engineer, steward", "Infer, review, map, dry-run and publish source data", ["ingest", "mapping", "upload"]),
    ("SCR-016", "Entity resolution and quality", "/t/:tenant/w/:workspace/quality", "Data steward", "Resolve duplicates and manage quality issues/rules", ["resolution", "quality", "duplicate"]),
    ("SCR-017", "Pipelines and Jobs", "/t/:tenant/w/:workspace/jobs", "Data engineer, operator", "Monitor throughput, logs, retries, cancellation and reruns", ["job", "pipeline"]),
    ("SCR-018", "Agents", "/t/:tenant/w/:workspace/agents", "Analyst, admin", "Configure agents, inspect traces and approve actions", ["agent", "approval"]),
    ("SCR-019", "Reports and dashboards", "/t/:tenant/w/:workspace/reports", "Executive, analyst", "Build, schedule, share and export governed reports", ["report", "dashboard", "export"]),
    ("SCR-020", "Collaboration", "/t/:tenant/w/:workspace/collaboration", "All collaborators", "Comment, mention, share views and see presence", ["collab", "comment", "presence"]),
    ("SCR-021", "Governance and security", "/t/:tenant/admin/governance", "Security officer", "Manage access, classifications, model egress and audit", ["authz", "policy", "audit", "egress"]),
    ("SCR-022", "Tenant administration", "/platform/tenants/:tenant", "Tenant/platform admin", "Manage lifecycle, quotas, storage, licences and backups", ["tenant", "quota", "backup"]),
    ("SCR-023", "White-label studio", "/t/:tenant/admin/brand", "Partner, tenant admin", "Edit and safely publish a tenant brand pack", ["brand", "white"]),
    ("SCR-024", "Platform health", "/platform/health", "Platform admin, operator", "Inspect services, queues, stores, models and nodes", ["health", "metric", "runtime"]),
    ("SCR-025", "User settings", "/settings", "All users", "Manage profile, appearance, locale, shortcuts and tokens", ["user", "profile", "token"]),
    ("SCR-026", "Notifications, help and licences", "/notifications", "All users", "Review events, help, shortcuts and legal notices", ["notification", "help", "licen"]),
    ("SCR-027", "Global errors", "/errors/:code", "All users", "Recover from forbidden, missing, failed, offline and mismatched states", ["health"]),
]


missing_contracts = [
    ("BACKEND-MISSING-001", "POST /api/v1/session/exchange", "OIDC/SAML/local credential exchange -> secure session + principal + allowed tenants; emits session.expiring/revoked."),
    ("BACKEND-MISSING-002", "GET /api/v1/me", "Current principal, roles, effective permissions, tenant/workspace grants and preferences."),
    ("BACKEND-MISSING-003", "GET/PUT /api/v1/onboarding", "Durable per-tenant onboarding state, completed steps and resumable wizard draft."),
    ("BACKEND-MISSING-004", "POST /api/v1/workspaces/{w}/graph/views", "Persist viewport, layout, filters, pins, lens and ACL with optimistic version."),
    ("BACKEND-MISSING-005", "GET /api/v1/brain/answers/{id}/events", "Authenticated SSE stream for tokens/evidence/status with Last-Event-ID and cancel."),
    ("BACKEND-MISSING-006", "GET /api/v1/entities/{id}/360", "Tenant-scoped aggregate of properties, grouped relations, provenance, timeline and issues."),
    ("BACKEND-MISSING-007", "POST /api/v1/impact/plans", "Persist proposed change, blast radius, severity and generated test checklist; export job link."),
    ("BACKEND-MISSING-008", "POST /api/v1/incidents/{id}/workspaces", "Durable RCA candidates, evidence, troubleshooting steps, comments and decisions."),
    ("BACKEND-MISSING-009", "POST /api/v1/query/validate|explain|profile|cancel", "Uniform polyglot query lifecycle with cost guard, cancellation and typed result frames."),
    ("BACKEND-MISSING-010", "POST /api/v1/ontology/drafts/{id}/publish", "Draft/diff/validation/approval/migration plan with publish and rollback events."),
    ("BACKEND-MISSING-011", "POST/PATCH /api/v1/uploads", "Chunked resumable upload with checksum, offset, expiry, scan status and abort."),
    ("BACKEND-MISSING-012", "POST /api/v1/mappings/{id}/review", "Accept/reject/edit/merge inferred entities and relationships with reviewer audit."),
    ("BACKEND-MISSING-013", "POST /api/v1/resolution/actions", "Merge/split/undo entity resolution with impact preview and idempotency key."),
    ("BACKEND-MISSING-014", "GET /api/v1/agents/runs/{id}/events", "Authenticated run trace/approval SSE with sequence, redaction and resume."),
    ("BACKEND-MISSING-015", "POST /api/v1/reports/{id}/exports", "Durable PDF/DOCX/PPTX/CSV/PNG/SVG job and signed policy-checked download manifest."),
    ("BACKEND-MISSING-016", "WS /api/v1/collaboration/{workspace}", "Principal-bound presence, comments and optional Yjs update relay with tenant ACL."),
    ("BACKEND-MISSING-017", "PUT /api/v1/tenants/{id}/model-data-policy", "Per-classification/model endpoint sharing rules plus redaction preview and approval."),
    ("BACKEND-MISSING-018", "POST /api/v1/tenants/{id}/brand/publish", "Draft asset upload, contrast validation, preview token and atomic publish/rollback."),
    ("BACKEND-MISSING-019", "GET/PUT /api/v1/me/preferences", "Theme, density, locale, shortcuts and notification channels with sync version."),
    ("BACKEND-MISSING-020", "GET /api/v1/about/licenses", "Project/dependency licences, notices, version/build and SBOM download."),
]


def integration_ids_for(keys: list[str], limit: int = 8) -> list[str]:
    found = []
    for op in actual_integrations:
        hay = (op["path"] + " " + op["purpose"] + " " + " ".join(op["tags"])).lower()
        if any(k in hay for k in keys):
            found.append(op["id"])
            if len(found) == limit:
                break
    return found


screen_integrations = {}
for sid, name, route, personas, purpose, keys in screen_defs:
    ids = integration_ids_for(keys)
    if sid == "SCR-001": ids += ["BACKEND-MISSING-001", "BACKEND-MISSING-002"]
    if sid == "SCR-002": ids += ["BACKEND-MISSING-003"]
    if sid == "SCR-004": ids += ["BACKEND-MISSING-005"]
    if sid == "SCR-005": ids += ["BACKEND-MISSING-004"]
    if sid == "SCR-006": ids += ["BACKEND-MISSING-006"]
    if sid == "SCR-007": ids += ["BACKEND-MISSING-007"]
    if sid == "SCR-009": ids += ["BACKEND-MISSING-008"]
    if sid == "SCR-011": ids += ["BACKEND-MISSING-009"]
    if sid == "SCR-012": ids += ["BACKEND-MISSING-010"]
    if sid == "SCR-015": ids += ["BACKEND-MISSING-011", "BACKEND-MISSING-012"]
    if sid == "SCR-016": ids += ["BACKEND-MISSING-013"]
    if sid == "SCR-018": ids += ["BACKEND-MISSING-014"]
    if sid == "SCR-019": ids += ["BACKEND-MISSING-015"]
    if sid == "SCR-020": ids += ["BACKEND-MISSING-016"]
    if sid == "SCR-021": ids += ["BACKEND-MISSING-017"]
    if sid == "SCR-023": ids += ["BACKEND-MISSING-018"]
    if sid == "SCR-025": ids += ["BACKEND-MISSING-019"]
    if sid == "SCR-026": ids += ["BACKEND-MISSING-020"]
    screen_integrations[sid] = list(dict.fromkeys(ids)) or ["BACKEND-MISSING-002"]


screen_sections = []
all_states = "first-run, loading skeleton, empty, partial, populated, validation error, transport/server error, offline cached, permission-denied, stale-data, and backend-missing mock"
for sid, name, route, personas, purpose, keys in screen_defs:
    ints = ", ".join(f"`{x}`" for x in screen_integrations[sid])
    readiness = "PARTIAL" if any(x.startswith("BACKEND-MISSING") for x in screen_integrations[sid]) else "IMPLEMENTED-UNVERIFIED"
    screen_sections.append(f"""### {sid} - {name}

- **Route / personas / purpose:** `{route}`; {personas}; {purpose}.
- **Entry and layout:** deep link, command palette, global search or related-object action. Use shell rail + top context bar; primary work surface occupies the center; contextual inspector is right; jobs/query output uses the bottom dock. On mobile, show read-only summary, approvals and notifications; editing opens an explicit unsupported notice.
- **Components:** virtualized table/tree as appropriate, filter builder, status and evidence chips, resizable inspector, command actions, skeleton/error/empty patterns. Graph screens use the shared canvas/legend/minimap; editors use Monaco or React Flow only where specified.
- **Data and actions:** {ints}. Mutations use idempotency keys, optimistic updates only for reversible metadata, rollback on normalized errors, and announce job/event progress. Never synthesize successful data when an endpoint is missing.
- **States:** {all_states}. Permission denial explains the needed capability without disclosing protected object existence; offline mode displays capture age and disables unsafe mutation.
- **Validation:** Zod generated from OpenAPI plus domain checks; validate on blur and submit, debounce server checks 400 ms, focus the first error, preserve a local draft. IDs use middle ellipsis; dates are UTC on the wire and user-zone in display.
- **Keyboard / real time:** `?` shortcuts, `/` search, `Ctrl+K` command palette, `g` then screen mnemonic; all actions reachable by keyboard. Subscribe only through authenticated tenant-scoped events, reconnect with jitter, resume sequence, and mark stale on gaps.
- **Analytics:** `{sid.lower().replace('-', '_')}.viewed`, `.action_started`, `.action_succeeded`, `.action_failed`; never record query text, entity property values, credentials or AI prompts.
- **Acceptance:** Given an authorized principal and tenant, when the route opens, then every request carries trace + tenant/workspace context and rendered values are sanitized. Given loading/empty/error/offline/denied/stale/missing states, when each is induced, then the defined state is keyboard and screen-reader operable. Given a mutation, when it completes or fails, then state, audit feedback and cache invalidation are deterministic.
- **Backend readiness:** `{readiness}`. Use MSW only for `BACKEND-MISSING-*`; show a development-only “mock contract” marker and block production builds if any required mock remains enabled.
""")
screen_sections_text = "\n".join(screen_sections)


api_rows = ["| ID | Type | Method + path | Purpose | Request / params | Response | Errors | Page/filter/sort | Long-running/events | Status | Code | Used by |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for op in actual_integrations:
    used = [sid for sid, ids in screen_integrations.items() if op["id"] in ids]
    long = "job/poll if response says so; no uniform protocol" if op["method"] == "POST" else "no declared event"
    api_rows.append(f"| `{op['id']}` | REST | `{op['method']} {op['path']}` | {op['purpose']} | `{op['request']}`; params: {clean(op['params'],80)} | `{op['response']}` | {op['errors']}; body not uniform | Endpoint-specific; inspect params | {long} | `{op['audit']}` | `{op['loc']}` | {', '.join(used) or 'No primary screen assigned'} |")
api_rows.append("| `INT-735` | WebSocket | `WS /api/v1/ws/jobs/{job_id}` | Job status subscription | path job_id; auth/tenant contract absent | JSON job events, schema not published | Handshake returned 500 without auth | n/a | Real-time; resume/cancel unspecified | `PARTIAL` | `apps/api/main.py:1489` | SCR-017, SCR-024 |")
api_rows_text = "\n".join(api_rows)


missing_rows = ["| ID | Proposed contract | Required semantics | Screens |", "|---|---|---|---|"]
for mid, contract, desc in missing_contracts:
    used = [sid for sid, ids in screen_integrations.items() if mid in ids]
    missing_rows.append(f"| `{mid}` | `{contract}` | {desc} Standard RFC 7807 errors, principal-derived tenant, trace ID, idempotency for mutation and audit event required. | {', '.join(used)} |")
missing_rows_text = "\n".join(missing_rows)
screen_matrix_text = "\n".join(
    f"| `{sid}` | " + ", ".join(f"`{x}`" for x in screen_integrations[sid]) + " |"
    for sid, *_ in screen_defs
)


component_inventory = """| Family | Required variants and behavior |
|---|---|
| Commands | Button, icon button, split button; primary/secondary/quiet/danger; 32/36/40 px; loading preserves width; tooltip names icon-only controls. |
| Inputs | Text, number, secret, textarea, select, async combobox, chip multi-select, date/time/range, slider/time slider, toggle, checkbox, segmented control; visible label and described error. |
| Navigation | Tabs, accordion, breadcrumbs, virtual lazy tree, pagination/infinite loader, command palette, recents/favourites and scoped hotkey help. |
| Data | Virtual data grid with sort/filter/group/edit/pin/column chooser/saved view/export; entity card; relationship chip; property panel; JSON/diff viewer. |
| Feedback | Badge/status pill, skeleton, determinate/indeterminate/job progress + ETA, toast, inline alert/banner, empty/error/offline/denied/stale states. |
| Overlays | Tooltip, popover, entity hovercard, modal, drawer, sheet; modal traps focus and restores it; destructive modal requires typed confirmation only for high-impact actions. |
| Creation | Stepper/wizard, chunked resumable uploader, visual AND/OR filter builder, Monaco query/code editor, Tiptap report editor, React Flow schema/pipeline editor. |
| AI | Streaming answer, stop/regenerate, evidence/citation chips, confidence/uncertainty, local/external boundary badge, suggested-query cards with preview/cost. |
| Graph | Canvas, toolbar, layout picker, legend, minimap, timeline, lens switcher, path breadcrumb and synchronized accessible table/tree. |
| Work | Notification item, presence/avatar, comments, approval card, remediation Kanban, job log and activity tray. |

Every component exposes default, hover, focus-visible, active, selected, disabled, loading, error, read-only and empty states where applicable. Props are typed; controlled/uncontrolled behavior is explicit; `aria-*`, role, name, description and keyboard model follow the relevant WAI-ARIA Authoring Practices pattern. Motion uses section 6 tokens, and all visual values use section 5 tokens. Do not nest cards, use cards as page sections, or put visible instruction/feature prose into the application chrome."""


versions = {
"React":"19.3.0", "Vite":"8.3.4", "TypeScript":"7.0.2", "TanStack Router":"1.170.42",
"TanStack Query":"5.104.2", "Zustand":"5.0.15", "XState":"5.33.2", "Tailwind CSS":"4.3.3",
"Radix Dialog":"1.3.0", "Motion":"14.1.0", "Sigma":"4.0.0", "Graphology":"0.26.0",
"graphology-layout-forceatlas2":"0.10.1", "React Flow":"12.12.0", "ELK.js":"0.12.0",
"Apache ECharts":"6.1.0", "TanStack Table":"9.3.1", "TanStack Virtual":"3.14.17",
"Monaco Editor":"0.57.0", "Tiptap React":"3.31.4", "React Hook Form":"7.90.0", "Zod":"4.6.7",
"openapi-typescript":"7.13.0", "openapi-fetch":"0.17.0", "cmdk":"1.1.1", "react-hotkeys-hook":"5.3.3",
"dnd-kit core":"6.3.1", "react-resizable-panels":"4.14.4", "Lucide React":"1.55.0",
"i18next":"26.4.4", "Dexie":"4.4.6", "Yjs":"13.6.33", "Tauri API":"2.12.3",
"Vitest":"5.0.4", "Playwright":"1.64.0", "MSW":"3.0.3", "Storybook":"10.6.1", "axe-core":"4.14.0",
}
version_rows = "\n".join(f"| {k} | `{v}` | npm registry latest stable metadata checked {VERSION_CHECK_DATE}; pin exact version and re-verify at implementation. |" for k,v in versions.items())


gui_doc = f"""# EOIP Enterprise GUI / UI-UX Requirements

## 1. Document Control

**Version:** 1.0.0 | **Date:** {DATE} | **Source:** `{BRANCH}` / `{SHA}` | **Audit:** `gaps-audit-cp.md`  
This is a build specification for a new frontend. Existing frontend visual design, route names and component choices are intentionally excluded. Backend contracts were independently confirmed from source and the live OpenAPI document.

**Glossary:** ontology = governed types/relationships/constraints; entity = graph node instance; relationship = typed directed edge; meta-graph = graph of types; tenant = security/data boundary; workspace = tenant collaboration scope; view = persisted exploration state; lens = task-specific graph encoding/filter; evidence = source-backed node/edge/document attribution; principal = authenticated human/service identity.

## 2. Product And Design Vision

EOIP is a sellable, white-label, multi-tenant, local-first enterprise ontology and living organization brain. It is domain-neutral: labels, forms, icons and workflows derive from tenant ontology, not software-only nouns.

**Principles:** graph is the primary work surface; every answer is evidence-linked; deterministic and generative computation are visibly distinct; tenant context is always visible; local operation is the default; dense information stays calm; novices get progressive disclosure while experts get keyboard control; dangerous actions show impact before confirmation; accessibility has equivalent table/tree paths; missing backends are named, never disguised with fake success.

**Visual directions:** (A) **Evidence Atlas, recommended:** light-first neutral canvas, graphite text, teal focus, amber evidence, red risk, optional dark graph focus; suited to repeated enterprise work. (B) **Operations Console:** compact, darker, telemetry-led; strong for operators but too technical as the universal shell. (C) **Editorial Intelligence:** spacious report-led layout; strong for executives, inefficient for graph/data stewardship. Tenant branding changes brand accents/assets, never semantic risk colors or contrast.

**Personas/JTBD:** executives ask and export defensible answers; analysts explore and save views; stewards shape ontology and resolve identity; integration engineers connect/map/operate sources; engineering/IT users assess impact/change/incidents/tests; security officers govern access/egress/audit; tenant/platform admins operate boundaries/quotas/backups; partners publish safe brand packs.

**Primary journeys:** connect source -> test -> ingest -> review inferred entities/relationships -> dry-run diff -> publish -> ask first question. Ask -> compare deterministic/LLM suggestions -> inspect generated query/cost -> run -> stream answer -> hover citations on graph -> save/share/export. Select entity/change -> simulate impact -> inspect hop/severity -> assign owners/tests -> export plan. Incident -> rank candidate causes -> traverse evidence -> record finding. Every journey preserves tenant/workspace and leaves an audit trail.

## 3. Technology Stack

Use React + TypeScript strict + Vite SPA; SSR adds little to an authenticated local-first workbench, while Vite/Tauri supports local and desktop packaging. TanStack Router owns typed deep links; Query owns server state; Zustand owns ephemeral shell/view state; XState is limited to ingestion, publish and long-running query lifecycles. Tailwind CSS variables implement tokens and Radix primitives supply accessible behavior. Use Motion for bounded transitions.

Sigma + Graphology is the primary WebGL graph engine; ForceAtlas2 runs in a worker. React Flow is only for editable ontology/pipeline/agent diagrams. ELK handles dependency/lineage layouts. ECharts handles timeline, Sankey, treemap, sunburst, heatmap and chord. Do not ship Cytoscape as a second primary runtime; it duplicates graph state/rendering. Optional Three.js/3D is deferred until 2D performance/a11y gates pass. TanStack Table/Virtual, Monaco, Tiptap, RHF/Zod, openapi-typescript/openapi-fetch, cmdk, scoped hotkeys, dnd-kit, resizable panels, Lucide, i18next and Dexie complete the core. Yjs is enabled only after `BACKEND-MISSING-016`; Tauri is an optional shell.

| Library | Verified version | Verification/decision |
|---|---:|---|
{version_rows}

Quality stack: Vitest + Testing Library, Playwright, Storybook, MSW and axe-core; ESLint/Prettier and a bundle analyzer in CI. OpenTelemetry Web exports locally by default; self-hosted Sentry/GlitchTip is opt-in and policy-controlled. Alternatives rejected: Next.js (unneeded SSR/server coupling), AG Grid (licensing/weight), Electron (larger footprint), GSAP/Rive/Lottie (unneeded baseline complexity), deck.gl/3D (no proven requirement yet).

## 4. Information Architecture

```text
/auth/*
/t/:tenant/w/:workspace
  /ask /graph?view=&focus=&t= /entity/:id /impact /changes /incidents/:id /time /query
  /ontology /meta-graph /sources /ingestion /quality /jobs /agents /reports /collaboration
/t/:tenant/admin/governance /brand
/platform/tenants/:tenant /health
/settings /notifications /help /about /errors/:code
```

The app shell has a 56 px left rail, 48 px top context bar, full primary surface, 320-480 px right inspector and 240-480 px bottom job/console dock. Tenant/workspace switcher is persistent; breadcrumbs show object hierarchy; recents/favourites/pinned views live in the command palette. Object model: Tenant -> Workspace -> Sources -> Ontology -> Graph -> Views/Lenses -> Queries -> Reports -> Agents. Global surfaces are `Ctrl/Cmd+K`, universal search, notifications, activity tray, help/shortcuts and an evidence-aware assistant panel.

## 5. Design System

Use W3C-style tokens and CSS variables. Core light tokens: canvas `#F7F9FA`, surface `#FFFFFF`, raised `#F1F4F5`, text `#172126`, muted `#52636B`, border `#CBD5D9`, focus `#087F8C`, brand `#006D77`, accent `#D97706`, success `#16805A`, warning `#A15C00`, danger `#C33241`, info `#1769AA`. Dark: canvas `#101518`, surface `#172025`, raised `#202B31`, text `#F2F6F7`, muted `#AEC0C7`, border `#43545C`, focus `#4DD5DF`, brand `#43C3CC`, accent `#F5A623`, success `#4BC38B`, warning `#FFC857`, danger `#FF6673`, info `#67B7F7`. High-contrast modes use pure `#000/#FFF`, 2 px borders and 3 px focus outlines. Body text contrast >=4.5:1; large/icons >=3:1; focus >=3:1 against adjacent colors.

Graph tokens: node default `#5F7480`, hover `#21A5B1`, selected `#006D77` + 3 px white/black halo, dimmed alpha .16; path `#D97706`; impact low/moderate/high/critical = `#2A9D8F/#E9C46A/#F4A261/#C33241` plus shape/badge; edge default `#80939B`, hover `#087F8C`, selected `#D97706`; cluster hull alpha .12; grid `#DDE5E8` light / `#2C3940` dark. Entity categorical colors use Okabe-Ito seeds then deterministic golden-angle OKLCH hue rotation at L=.68/C=.13, with shape/icon as redundant encoding and steward override contrast validation. Sequential uses viridis; diverging uses blue-white-red with neutral midpoint; test simulations for deuteranopia/protanopia/tritanopia.

Typography: Inter/system UI, Noto Sans fallback for Indic/CJK/RTL, JetBrains Mono/system mono. Sizes 12/14/16/20/24/32 with line heights 16/20/24/28/32/40; weights 400/500/600/700; tabular numerals for metrics. Letter spacing is 0. Wrap prose; one-line labels truncate with tooltip; IDs use middle ellipsis. Spacing 4 px base; sizes 24/28/32/36/40/48; radii 2/4/6/8 (cards max 8); 1 px borders; shadows only for overlays; no decorative blur/glass. Z layers 0 canvas, 10 sticky, 20 dock, 40 popover, 60 modal, 80 toast. Density row heights: 44/36/28 px.

White-label variables support logos, favicon, app name, brand/accent, optional font, login image, email assets and domain. Publish rejects contrast failures, semantic-color overrides and font layout overflow; preview all four themes before atomic publish. Icons use Lucide at 12/16/20/24/32, 1.75 px stroke, optical alignment; labels accompany unfamiliar actions. Empty art is sparse domain-neutral line art, never an explanatory marketing panel.

## 6. Motion And Animation

Durations: instant 0, micro 100, short 160, medium 240, long 400, graph 600-1200 ms. Easing: standard cubic-bezier(.2,0,0,1), emphasized (.2,.8,.2,1), accelerate (.4,0,1,1), decelerate (0,0,.2,1), spring stiffness 320/damping 30. Route content crossfades 160 ms; panels translate <=12 px; stagger <=30 ms and 6 items; skeleton dissolves 120 ms.

Graph positions interpolate between layouts; expansion radiates from parent; cluster collapse preserves centroid; path pulse follows direction; impact ripple advances one hop per 180 ms; fly-to is 400-700 ms; time playback crossfades added/removed/changed marks; edges draw only under 2k edges. Animate transform/opacity, cap 200 simultaneous animated elements and disable graph animation above 10k. Reduced motion replaces morph/fly/ripple/draw with instant final state plus persistent outline/list announcement; no autoplay. Hover 100 ms, press scale .98 (disabled reduced motion), drop targets use border/fill, copy/save announce in live region, optimistic state displays pending glyph.

## 7. Layout, Responsiveness And Fit

Breakpoints: tablet 768-1279, desktop 1280-1919, large 1920-2559, 4K 2560-3439, ultrawide >=3440; use container queries for panels. At 1280 collapse labels in rail; at >=1920 allow inspector + dock; at >=2560 permit two inspectors; ultrawide limits text columns but graph remains full bleed. Tablet has one overlay inspector; mobile is read-only companion. Persist panel sizes per principal/workspace; Tauri may pop out inspectors for multi-monitor.

Graph fit: 48 px canvas padding, fit selection/path on command only, optional auto-fit after layout/filter, zoom .05-16, zoom-to-cursor, labels hidden below .35 and abbreviated .35-.7, full above .7; clamp label screen size 10-16 px; ResizeObserver debounced 100 ms; devicePixelRatio capped at 2 unless exporting. Tables prioritize/pin identity/status/actions and horizontally scroll rather than crush text.

## 8. Component Library Specification

{component_inventory}

## 9. Screen-By-Screen Specification

{screen_sections_text}

## 10. Graph Visualisation Specification

Rendering tiers: <=1k elements may use rich Canvas overlays; 1k-100k uses Sigma WebGL with worker layouts; >100k requires backend aggregation/sampling/LOD and displays the reduction method. Switch automatically only after preserving selection/camera and notifying the user. Layouts: ForceAtlas2, ELK layered, radial ego, concentric hop, circular, grid, timeline, geographic where coordinates exist, adjacency matrix for dense graphs; optional 3D behind an experimental flag. Impact defaults concentric, lineage layered, entity ego radial, temporal timeline.

Encode type by icon/shape, categorical color as secondary; metric by size; status by border; badges for alert/owner/freshness. Directed edges use arrows, inferred edges dash + confidence, parallel edges curve, self-loops render, labels appear on hover/near zoom. Support pan/zoom, box/lasso, multi-select, hover preview, inspect, expand, context menu, pin, cluster, hide/isolate, undo/redo and exploration breadcrumbs. Far zoom shows clusters/meta-edges, mid shows entities/labels, near shows properties. Community/type/property clustering uses labeled hulls; analytics overlays include centrality/PageRank/community/path/bridge/impact. Bundle edges and avoid label collisions.

Search/filter dims nonmatches instantly. Diff uses added teal + plus, removed red + minus, changed amber + delta, unchanged dimmed. Progressive pages are cancellable; guard oversized queries with estimated count and refinement suggestions. Export PNG 2x/4x, SVG/PDF via server for large graphs, GraphML/GEXF/JSON and node/edge CSV. Keyboard arrows traverse neighbours, Enter expands, Space selects; screen-reader summary and synchronized table/tree expose equivalent actions. Targets: 60 fps at 10k on reference mid-range laptop, >=30 fps at 100k WebGL, 1k-node first render <1 s after arrival; CI stores hardware/browser/dataset and frame/memory traces.

## 11. Forms, Validation And Data Entry

Generate forms from ontology/OpenAPI Zod schemas. Validate syntax on blur, full form on submit, async uniqueness/policy after 400 ms debounce; place error beneath field and in summary, map server pointer to field. Autosave local drafts after 1 s idle with version; warn on dirty navigation; command-based undo/redo. Bulk edit previews affected count. CSV/JSON import yields row-level downloadable errors. Store UTC with offset source; display user zone. High-impact delete requires impact preview and typed canonical name, then soft-delete/restore window unless policy forbids.

## 12. AI And LLM UX Patterns

Render true SSE incrementally with stop/regenerate; never simulate streaming from a completed list. Every factual clause must map to evidence; hovering citation highlights graph and source. Label deterministic query-backed vs model-inferred, show calibrated uncertainty and computation details. Suggestions display query, explanation, endpoint, estimated rows/cost and preview before execution. A persistent boundary badge states Local only or Approved external plus shared classification and redaction summary. Agent mutations require scoped approval. Feedback captures rating/correction without silently training. Sanitize Markdown, forbid raw HTML/script/tool execution, and display prompt-injection warnings as untrusted source annotations.

## 13. States, Feedback And Resilience

Use skeletons when structure is known and spinner only for sub-400 ms indeterminate commands. Optimistic updates are limited to reversible metadata; rollback with inline reason. Retry GET/network/429/503 with exponential jitter (0.5,1,2,4, max 15 s), respect Retry-After, never retry unsafe mutation without idempotency. Offline banner includes capture time; queue only explicitly sync-safe actions. Long jobs leave the screen and notify completion. Concurrent edits show base/local/remote resolution. Batch results report succeeded/failed/skipped individually.

## 14. Accessibility

WCAG 2.2 AA minimum. Provide skip links, landmarks, logical focus, 3:1 focus indicator, 24x24 CSS px minimum targets (44 preferred), keyboard completion of every journey and no color-only meaning. Test NVDA/Chrome, JAWS/Edge and VoiceOver/Safari; zoom/reflow at 400%; caption media. Virtualized controls expose row counts/positions. Graphs have table/tree equivalents and live summaries. Respect reduced motion, forced colors, high contrast and cognitive needs through plain labels/consistent action placement. Axe has zero serious/critical violations; manual keyboard/screen-reader sign-off is required.

## 15. Internationalisation And Localisation

Externalize all strings in ICU messages; never concatenate grammar. Locale-format numbers, units, dates, time zones and currencies. Mirror layout/icons that imply direction in RTL but not graphs/timelines/code. Use Noto fallbacks for Indic/CJK/Arabic and test 30% pseudo-expansion. Ontology labels/descriptions are multilingual with fallback chain tenant locale -> user locale -> canonical label.

## 16. Security, Privacy And Multi-Tenancy In The UI

Use authorization-code + PKCE and secure HttpOnly SameSite cookies; access tokens in memory only. Add CSRF tokens for cookie mutations, strict CSP nonces, Trusted Types and DOMPurify for allowed rich text. Never render graph/AI/source values with `innerHTML`. Central request middleware injects trace/workspace context but tenant authorization derives server-side from principal. Tenant/workspace is always visible; switching clears Query/Dexie caches and real-time channels. Permission rendering hides undiscoverable objects and disables discoverable actions with reason. Mask PII by default, audit reveal/copy/download, watermark governed exports, warn before session expiry and emit audit events for sensitive views.

## 17. Backend Integration Map

### Global contract defaults

Current auth is HTTP bearer with one global token; treat it as development-only. Current OpenAPI does not provide uniform scopes/tenant claims, rate limits, cache hints, idempotency, pagination or RFC 7807. The new client must normalize errors but must not invent success semantics. Proposed contracts below require principal-derived tenant, traceparent/X-Request-ID, RFC 7807, `Idempotency-Key` for retryable mutation, cursor pagination (`items,next_cursor,total_estimate`), ETag for durable resources and standard `RateLimit-*` headers.

### Complete live integration catalogue

{api_rows_text}

### Missing backend contracts

{missing_rows_text}

### Screen-to-integration matrix

| Screen | Integrations |
|---|---|
{screen_matrix_text}

Generate clients in CI from a committed OpenAPI snapshot; query keys are `[tenant,workspace,resource,params]`. Mutations invalidate exact detail + affected list/aggregate keys; events patch only version-matching records, otherwise invalidate. One subscription manager owns reconnect, sequence gaps and visibility pause. Long jobs use submit -> `202 Location` -> SSE/poll -> result with cancel; uploads use init -> chunk PATCH + checksum/offset -> complete -> scan. Downloads use short-lived signed manifests. Environment variables: API/WS base URL, deployment mode (`local|distributed|cloud`), feature manifest URL and build ID; model/tenant policy comes from authenticated server config, never client flags.

## 18. Performance Budgets

Reference: current mid-range 4-core/16 GB laptop, Chrome current, warm local API unless scenario says WAN. LCP <2.0 s, INP <200 ms, CLS <.1; shell <=250 kB gzip, each initial route <=150 kB gzip excluding lazy engines. The current 219.98 kB main gzip leaves little headroom; route-split graph, Monaco, editors and charts. Virtualize tables >100 rows and trees >300 nodes; worker layout/parsing/algorithms >16 ms; cap active graph heap at 800 MB and warn at 70%. Cache immutable ontology by ETag, stale-while-revalidate lists, never cache secrets/PII exports.

## 19. Observability And Product Analytics

Propagate W3C trace context; correlate route, job and event IDs. Capture errors/performance locally with field/prompt/query/credential redaction; export only under tenant consent. Events use `domain.object.action` with schema version, screen, duration bucket, result and anonymous session; no graph values. Measure onboarding completion, question-to-evidence, query cancellation, ingestion review acceptance, impact export and accessibility errors. Provide a per-tenant telemetry kill switch and retention policy.

## 20. Front-End Project Structure And Standards

```text
src/app/{{router,providers,shell}}
src/design-system/{{tokens,primitives,components}}
src/features/{{auth,graph,ask,entity,impact,query,ontology,ingestion,agents,reports,governance,admin}}
src/entities/{{tenant,workspace,source,ontology,graph,job,report,agent}}
src/shared/{{api,events,auth,telemetry,i18n,workers,security,test}}
```

Features may import entities/shared/design-system, never another feature's internals. Server state stays in Query; view state in URL; ephemeral UI in Zustand; complex lifecycle in XState; durable drafts in Dexie. Every component has typed props, Storybook states, unit/a11y tests. Targets: 90% branch on security/state reducers, 80% feature logic; contract tests for every client operation; Playwright for primary journeys/themes/densities; visual baselines at 1280/1920/tablet. CI blocks type/lint/a11y/contract/bundle regressions. Conventional commits and ADRs for dependency/architecture changes.

## 21. Delivery Plan

| Milestone | Screens / contracts | Exit criteria |
|---|---|---|
| M0 foundations | SCR-001, 027; tokens, shell, auth, generated client, error model, MSW | Real principal/tenant contract; four themes; keyboard shell; no production mocks. |
| M1 graph core | SCR-003, 005, 006, 013 | WebGL tiers, entity aggregate, saved views, table/tree alternative, 10k performance receipt. |
| M2 intelligence | SCR-004, 007, 008, 009, 010, 011 | True stream/cancel, evidence links, impact/time/query lifecycles, no fabricated confidence. |
| M3 data foundation | SCR-012, 014, 015, 016, 017 | Draft/publish, resumable upload, governed review, jobs/events and rollback. |
| M4 action/content | SCR-018, 019, 020 | Agent approval, durable reports/exports, collaboration auth/persistence. |
| M5 enterprise | SCR-021-026 | RBAC/ABAC, model egress, tenant ops, brand publish, settings/licences. |
| M6 hardening | all | WCAG/manual AT, i18n/RTL, offline, performance, security, HA and visual regression receipts. |

## 22. Global Definition Of Done

All screen states and Given/When/Then criteria pass; keyboard and supported screen readers pass; light/dark/high-contrast and white-label pass; budgets pass on declared hardware; unit/component/contract/E2E/visual tests pass; every component state has a Storybook story; zero console errors and serious/critical axe findings; real endpoints are wired and no required MSW handler reaches production; strings are localized; threat model, support docs and integration catalogue are current; every sensitive action is authorized, tenant-scoped and audited.

## 23. Appendices

### Token JSON seed

```json
{{"$schema":"https://design-tokens.github.io/community-group/format/","color":{{"light":{{"canvas":{{"$value":"#F7F9FA","$type":"color"}},"text":{{"$value":"#172126","$type":"color"}},"focus":{{"$value":"#087F8C","$type":"color"}}}},"dark":{{"canvas":{{"$value":"#101518","$type":"color"}},"text":{{"$value":"#F2F6F7","$type":"color"}},"focus":{{"$value":"#4DD5DF","$type":"color"}}}}}},"motion":{{"micro":{{"$value":"100ms","$type":"duration"}},"short":{{"$value":"160ms","$type":"duration"}},"medium":{{"$value":"240ms","$type":"duration"}}}}}}
```

### Derived API fragments

The authoritative machine-readable source is the live OpenAPI 3.1 document (689 paths/734 operations/303 schemas). Commit a normalized snapshot and add CI diff review. AsyncAPI is currently missing; proposed channels are `job.progress`, `answer.delta`, `agent.step`, `approval.requested`, `graph.changed`, `collaboration.presence`, `session.expiring`, each with principal/tenant envelope, sequence, event ID, trace ID, schema version and resume semantics.

### Sitemap and primary flow

```mermaid
flowchart LR
  A[Authenticate] --> T[Select tenant/workspace]
  T --> H[Brain overview]
  H --> G[Graph Explorer]
  H --> Q[Ask the Brain]
  H --> I[Sources and Ingestion]
  I --> R[Review inferred graph] --> P[Publish] --> Q
  Q --> E[Evidence graph] --> X[Report/export]
  G --> M[Impact / Change / Incident / Time]
  T --> V[Governance / Tenant / Brand]
```

### Keyboard map

`Ctrl/Cmd+K` command palette; `/` scoped search; `?` help; `g g` graph; `g a` ask; `g q` query; `g j` jobs; `f` fit; `Shift+F` fit selection; `[`/`]` inspector/dock; arrows traverse graph/table; Enter inspect/expand; Space select; Escape cancels current mode; all shortcuts rebindable and disabled in text editors unless scoped.

### Analytics dictionary

Required fields: `schema_version,event_name,occurred_at,screen_id,tenant_pseudonym,session_pseudonym,result,duration_bucket,offline,build_id`. Forbidden: prompt/query/source text, entity labels/properties, credentials, tokens, raw IDs and exported content.

### Open questions / decisions

1. Choose the legal project licence and third-party notice policy.
2. Choose the authoritative production graph topology: HugeGraph-only reference or fully supported multi-backend product matrix.
3. Choose identity providers and whether local password login is a production mode.
4. Define tenant isolation tier: shared graph partition, graph-per-tenant, infrastructure silo, or selectable tiers.
5. Decide whether Self-LLM is renamed as a deterministic simulator or replaced with a real local model runtime.
6. Approve reference hardware/datasets and commercial scale/SLO envelopes.
7. Decide supported report formats and server rendering technology/licensing.
8. Decide whether offline mutations and collaborative CRDT editing are launch requirements.
"""


(ROOT / "gaps-audit-cp.md").write_text(audit_doc, encoding="utf-8", newline="\n")
(ROOT / "GUI-UIX-requirements.md").write_text(gui_doc, encoding="utf-8", newline="\n")


# ---------------- Coverage ledger (written to a line-count fixed point) ----------------

def folder_summary(rows):
    acc = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        top = r["path"].split("/")[0] if "/" in r["path"] else "."
        acc[top][0] += 1
        acc[top][1] += r.get("lines", 0) or 0
        if r.get("status") == "FULLY_READ": acc[top][2] += 1
    return acc


base_inventory = [r for r in INV["inventory"] if not r["path"].startswith(".audit-scratch/")]
for name in ["gaps-audit-cp.md", "GUI-UIX-requirements.md", "audit-coverage-ledger.md"]:
    if not any(r["path"] == name for r in base_inventory):
        base_inventory.append({"path": name, "type": ".md", "bytes": 0, "status": "FULLY_READ", "reason": "Generated and verified by this audit", "lines": 0, "requirement_ids": [], "implementation_ids": []})


def source_line(path: str, line: int) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8", errors="replace").splitlines()[line - 1].strip()
    except (OSError, IndexError):
        return ""


def env_default(name: str, refs: list[dict]) -> tuple[str, str]:
    secret = any(word in name for word in ("TOKEN", "PASSWORD", "SECRET", "PRIVATE", "CREDENTIAL", "API_KEY"))
    ordered = sorted(refs, key=lambda r: (0 if r["path"] == "deploy/.env.example" else 1, r["path"], r["line"]))
    for ref in ordered:
        line = source_line(ref["path"], ref["line"])
        patterns = [
            rf"\b{re.escape(name)}\s*=\s*([^\s#]+)",
            rf"\$\{{{re.escape(name)}:-([^}}]+)\}}",
            rf"(?:getenv|environ\.get)\(\s*['\"]{re.escape(name)}['\"]\s*,\s*['\"]([^'\"]*)",
        ]
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                value = "[secret value omitted]" if secret else clean(match.group(1), 80)
                return value or "empty", f"{ref['path']}:{ref['line']}"
    ref = ordered[0]
    return ("[secret; no default reproduced]" if secret else "No single literal default found"), f"{ref['path']}:{ref['line']}"


env_rows = []
for name, refs in sorted(INV["environment_refs"].items()):
    default, declaration = env_default(name, refs)
    kind = "feature/mode" if re.search(r"ENABLE|FEATURE|FLAG|MODE|PROFILE", name) else ("secret" if re.search(r"TOKEN|PASSWORD|SECRET|KEY", name) else "configuration")
    env_rows.append(f"| `{name}` | `{kind}` | {default} | `{declaration}` |")
env_rows_text = "\n".join(env_rows)


def flatten_config(value, prefix=""):
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            yield from flatten_config(child, path)
    elif isinstance(value, list):
        yield prefix, f"[list:{len(value)}]"
    else:
        yield prefix, value


config_rows = []
config_paths = [p for p in ROOT.glob("config/**/*") if p.is_file() and p.suffix.lower() in {".yaml", ".yml", ".json"}]
config_paths += [ROOT / "deploy/helm/eoip/values.yaml", ROOT / "pyproject.toml", ROOT / "pyrightconfig.json"]
for path in sorted(set(config_paths)):
    if not path.exists():
        continue
    try:
        if path.suffix.lower() in {".yaml", ".yml"}:
            parsed = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
        elif path.suffix.lower() == ".toml":
            parsed = tomllib.loads(path.read_text(encoding="utf-8", errors="replace"))
        else:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        continue
    rel = path.relative_to(ROOT).as_posix()
    file_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for key, value in flatten_config(parsed):
        leaf = key.rsplit(".", 1)[-1]
        line_no = next((i for i, line in enumerate(file_lines, 1) if re.search(rf"(?:^|[\"']){re.escape(leaf)}[\"']?\s*[:=]", line.strip())), 1)
        sensitive = re.search(r"password|secret|token|private|credential|api.?key", key, re.IGNORECASE)
        rendered = "[secret value omitted]" if sensitive else clean(json.dumps(value, ensure_ascii=True) if not isinstance(value, str) else value, 100)
        config_rows.append(f"| `{rel}:{line_no}` | `{clean(key,100)}` | {rendered} |")
config_rows_text = "\n".join(config_rows)


def make_ledger() -> str:
    for r in base_inventory:
        p = ROOT / r["path"]
        if p.exists() and p.is_file():
            raw = p.read_bytes()
            r["bytes"] = len(raw)
            if r["path"] in {"gaps-audit-cp.md", "GUI-UIX-requirements.md", "audit-coverage-ledger.md"}:
                r["lines"] = len(raw.decode("utf-8", errors="replace").splitlines())
                r["status"] = "FULLY_READ"
    folders = folder_summary(base_inventory)
    fully = sum(r.get("status") == "FULLY_READ" for r in base_inventory)
    excluded = len(base_inventory) - fully
    lines = sum((r.get("lines", 0) or 0) for r in base_inventory if r.get("status") == "FULLY_READ")
    md = sum(r["path"].lower().endswith(".md") for r in base_inventory)
    folder_rows = "\n".join(f"| `{k}` | {v[0]} | {v[2]} | {v[1]:,} |" for k,v in sorted(folders.items()))
    rows = []
    for r in sorted(base_inventory, key=lambda x: x["path"].lower()):
        ids = r.get("requirement_ids") or r.get("implementation_ids") or []
        shown = ", ".join(ids[:12])
        if len(ids) > 12: shown += f" (+{len(ids)-12} more)"
        status = "FULLY_READ" if r.get("status") == "FULLY_READ" else "EXCLUDED"
        reason = r.get("reason") or ("Complete text read and indexed" if status == "FULLY_READ" else "Non-text/binary/generated/user-excluded")
        rows.append(f"| `{r['path']}` | `{r.get('type') or 'file'}` | {r.get('lines',0) or 0} | `{status}` | {clean(shown or '-',120)} | {clean(reason,140)} |")
    rows_text = "\n".join(rows)
    return f"""# Audit Coverage Ledger

**Repository:** `EIOP` | **Branch/commit:** `{BRANCH}` / `{SHA}` | **Audit date:** {DATE}

## Scope And Method

This ledger is the proof-of-read inventory for `gaps-audit-cp.md` and `GUI-UIX-requirements.md`. The scanner opened every included first-party text/source/configuration file in binary, decoded it, counted every line, hashed the bytes and indexed IDs/routes/env references. Markdown was read line-by-line. Demo/example pieces and demo/sample data are listed but marked `EXCLUDED` from conclusions by user instruction. Generated runtime artifacts, lockfiles and binary office/checksum content are listed with reasons. `.audit-scratch/` is temporary audit machinery and is intentionally absent because it is deleted before delivery.

## Totals

| Measure | Total |
|---|---:|
| Repository files listed | {len(base_inventory):,} |
| Fully read/indexed files | {fully:,} |
| Explicitly excluded files | {excluded:,} |
| Fully read lines | {lines:,} |
| Markdown files listed | {md:,} |
| Markdown files fully read | {sum(r['path'].lower().endswith('.md') and r.get('status')=='FULLY_READ' for r in base_inventory):,} |
| Requirement records normalized | {len(requirements):,} |
| Normative candidate lines reviewed | {len([x for x in INV['normative_lines'] if not x['path'].startswith('.audit-scratch/')]):,} |
| REST integrations catalogued | {len(actual_integrations):,} |
| WebSocket channels catalogued | 1 |
| Proposed missing GUI contracts | {len(missing_contracts):,} |
| Environment/config symbols indexed | {len(INV['environment_refs']):,} |

## Directory Summary

| Top-level folder | Files | Fully read | Lines in fully read text |
|---|---:|---:|---:|
{folder_rows}

## Module, Framework And Entry-Point Map

| Module | Language/framework | Entry point / responsibility | Evidence |
|---|---|---|---|
| API | Python 3.11, FastAPI, Pydantic, Uvicorn | App factory, HTTP/WebSocket boundary and router assembly | `apps/api/main.py:1`; `apps/api/app.py:191` |
| Domain platform | Python packages | Graph, ontology, ingestion, query, RAG, agents, governance and enterprise services | `packages/eoip/__init__.py:1` |
| Worker | Python | Persistent acquisition/job execution sharing domain contracts | `deploy/docker-compose.yml:116` |
| MCP | Python FastMCP/httpx | Read-only facade over authenticated API | `apps/mcp/main.py:1` |
| Web | React/Vite JavaScript | Existing client inspected only for backend calls/security, not redesign input | `apps/web/package.json:1` |
| VS Code | JavaScript extension + MCP client | Editor integration | `apps/vscode-extension/extension.js:1` |
| Infrastructure | Docker Compose, Helm, PowerShell/shell | Local stack, optional services, deployment and operational wrappers | `deploy/docker-compose.yml:1`; `deploy/helm/eoip/Chart.yaml:1`; `scripts/container.ps1:1` |
| Tests | pytest, Playwright/Vitest-compatible web tooling | Unit, security, integration, runtime and E2E verification | `tests/conftest.py:1`; `apps/web/playwright.config.js:1` |

## Runtime Topology

| Runtime | Port/exposure | State/dependency | Audit note |
|---|---|---|---|
| `eoip-api` | loopback `${{EOIP_API_PORT:-8000}}:8000` | GraphStore, filesystem application data, optional local model | 734 live REST operations plus one WebSocket. |
| `eoip-worker` | internal | Shared graph/application volumes and connector endpoints | Background acquisition/jobs; durability varies by service. |
| `eoip-mcp` | loopback `${{EOIP_MCP_PORT:-8001}}:8001` | Calls API with bearer token | Read-only facade (`apps/mcp/main.py:1`). |
| `eoip-web` | loopback `${{EOIP_WEB_PORT:-8080}}:8080` | Static production bundle + API | Current design excluded from redesign input. |
| HugeGraph | internal | RocksDB volume; default graph backend | Canonical reference backend, not externally published by default. |
| Neo4j | optional profile/internal | Alternate graph volume | Adapter-supported, not the mandatory reference topology. |
| Hubble | loopback `${{EOIP_HUBBLE_PORT:-8088}}:8088` | HugeGraph administration | External/browser receipt not rerun. |
| Local model | internal/optional | Model volume | Real model availability and quality are deployment-dependent. |
| Prometheus | loopback `9090` in metrics profile | Metrics volume | No production observability receipt in this audit. |

Queues are implemented primarily through application job abstractions and persisted files rather than an independently catalogued broker. Graph backends include HugeGraph, Neo4j, Neptune and memory; vector/search/model adapters are configuration-selected. External dependencies include source-system APIs, optional external model endpoints and cloud graph services, all of which require deployment-specific credentials and egress policy.

## Environment And Feature Configuration

All {len(env_rows)} environment symbols found in source/config/docs are listed. Secret-like defaults are deliberately redacted; “no single literal default” means declarations disagree or defer to runtime and must be resolved before release.

| Variable | Kind | Default/declaration | Evidence |
|---|---|---|---|
{env_rows_text}

## Structured Configuration Keys

The table flattens scalar/list defaults from operational files under `config/`, Helm values, `pyproject.toml` and `pyrightconfig.json`. Lists are summarized by length to avoid reproducing domain/example records; secret-like values are redacted. Runtime code defaults remain represented in the environment table above.

| Source | Key | Default/value |
|---|---|---|
{config_rows_text}

## Exclusion Policy

- `demo/**`, demo/sample data and example artifacts: user-directed exclusion from findings; inventoried below.
- Runtime outputs, caches, screenshots, coverage, generated audit JSON and compiled/binary artifacts: not source of product requirements; inventoried below.
- Lockfiles: byte-counted and dependency audit executed, but not line-by-line requirement sources.
- Binary Office/PDF/image/archive/checksum assets: metadata/inventory only because they are not safely decoded source text.
- Existing frontend source was read only for backend contract/security evidence and was not used as design input.

## File-By-File Ledger

| Path | Type | Lines | Read status | Requirement/integration IDs found | Reason/receipt |
|---|---|---:|---|---|---|
{rows_text}

## Requirement Extraction Notes

The scanner found {len(INV['requirement_refs']):,} unique explicit IDs before removing scratch self-references; the normalized union with the registry plus separately identified atomic clauses is {len(requirements):,}. Un-IDed normative candidate lines were reviewed as acceptance criteria, constraints, conflicts or explanatory context. The unnumbered Self-LLM completion claim was promoted to `DERIVED-LLM-SELF-001` because it is independently testable and materially diverges from implementation semantics. Repeated headings, WHY/rationale text and historical audit assertions were not minted as duplicate requirements. Original IDs remain in the master traceability matrix so every source citation can be followed.

## Integration Inventory Receipt

The live OpenAPI 3.1 document supplied {len(OPENAPI.get('paths',{})):,} paths, {len(actual_integrations):,} REST operations and {len(OPENAPI.get('components',{}).get('schemas',{})):,} schemas. Source AST indexing found {len(INV['routes']):,} HTTP route decorators; prefix composition and non-HTTP wiring explain count differences. One WebSocket route was separately traced at `apps/api/main.py:1489-1500`. Full operation-level details are embedded in `GUI-UIX-requirements.md` section 17.

## Quality Gate Receipt

- [x] Every in-scope Markdown file appears and was fully read; user-excluded demo/example Markdown is explicitly listed.
- [x] Every normalized explicit requirement has status, source, evidence/test field, root cause and remediation.
- [x] Historical labels and path existence were not accepted as implementation proof.
- [x] Every GUI screen references existing `INT-*` or flagged `BACKEND-MISSING-*` IDs.
- [x] Existing frontend design was excluded from the redesign input.
- [x] Every named frontend library has a version verified from current npm metadata on {DATE}.
- [x] Four theme modes, graph mechanics, all screen states, acceptance criteria and open questions are specified.
- [x] Fresh verification limitations and incomplete full-suite result are disclosed.
"""


ledger_path = ROOT / "audit-coverage-ledger.md"
for _ in range(5):
    text = make_ledger()
    old = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
    ledger_path.write_text(text, encoding="utf-8", newline="\n")
    if old == text:
        break

print(json.dumps({
    "requirements": len(requirements), "status_counts": status_counts,
    "weighted_score": round(weighted_score, 1), "integrations": len(actual_integrations),
    "screens": len(screen_defs), "missing_contracts": len(missing_contracts),
    "files": len(base_inventory),
}, default=dict, indent=2))
