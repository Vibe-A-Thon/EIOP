#!/usr/bin/env python3
"""Generate audit-output/requirements.md (requirements catalogue) and audit-output/implementation.md
(implementation status against requirements), deterministically, from the kit's outputs.

Inputs (all read-only): requirements_index.json, traceability_detail.json, evidence/evidence.json (merged),
audit-memory.json, test_results_merged/ (or test_results/), remediation/requirement_tasks.json,
remediation/findings_tasks.json, remediation/duplicate_id_tasks.json, remediation/orphan_test_ids.json,
audit-config.json, and the read-only clone (verbatim text is read from the source lines at the audited commit).

No network, no LLM, no secrets: requirement text comes from the repo's requirement docs only.
Same inputs -> byte-identical output (dates come from --generated-at, default: audit-memory last_audit_date).

  python3 generate_requirements_and_implementation_md.py --kit /workspace/eoip-audit-kit --repo-root /workspace/repos/EIOP
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
STATUS_ORDER = ["Implemented", "Partially Implemented", "Ambiguous", "Not Verified", "Not Implemented"]
MAX_VERBATIM = 20000
PARAM_RE = re.compile(r"\[.*\]$")
ID_TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+[A-Za-z]?(?:\.\d+)?\b")
DEP_LABEL_RE = re.compile(r"^\s*[-*]?\s*\**(depends on|dependencies|dependency|prerequisites?|requires)\**\s*:\**\s*(.+)$", re.I)


def load(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


# ---------------------------------------------------------------- markdown helpers
def cell(s) -> str:
    """Safe table-cell text: escape pipes, angle brackets; collapse newlines."""
    s = "" if s is None else str(s)
    s = s.replace("\\", "\\\\").replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\s*\n\s*", "<br>", s.strip())


def inline(s) -> str:
    """Safe inline text for headings/list items."""
    s = "" if s is None else str(s)
    s = s.replace("\\", "\\\\").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"([*_\[\]`#|])", r"\\\1", s)
    return re.sub(r"\s+", " ", s).strip()


def code(s) -> str:
    s = str(s).replace("|", "\\|")
    return f"`` {s} ``" if "`" in s else f"`{s}`"


def fence(text: str, info: str = "text") -> str:
    runs = [len(m) for m in re.findall(r"`+", text)] or [0]
    f = "`" * max(3, max(runs) + 1)
    return f"{f}{info}\n{text.rstrip()}\n{f}"


def anchor(rid: str) -> str:
    return "req-" + re.sub(r"[^A-Za-z0-9_-]", "_", rid)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ---------------------------------------------------------------- repo helpers
class Repo:
    def __init__(self, root: Path | None, commit: str):
        self.root, self.commit, self._files, self._exists = root, commit, {}, {}
        self.at_commit = False
        if root and (root / ".git").exists():
            try:
                head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True,
                                      check=True).stdout.strip()
                self.at_commit = head == commit
            except (OSError, subprocess.CalledProcessError):
                pass

    def lines(self, path: str) -> list[str] | None:
        if not self.at_commit:
            return None
        if path not in self._files:
            p = self.root / path
            self._files[path] = p.read_text(encoding="utf-8", errors="replace").splitlines() if p.is_file() else None
        return self._files[path]

    def exists(self, path: str) -> bool:
        if path not in self._exists:
            self._exists[path] = bool(self.root and (self.root / path).is_file())
        return self._exists[path]

    def ls(self, prefix: str) -> list[str]:
        if not self.at_commit:
            return []
        out = subprocess.run(["git", "-C", str(self.root), "ls-files", prefix], capture_output=True, text=True).stdout
        return [x for x in out.splitlines() if x]


def table_context(lines: list[str], lineno: int) -> tuple[list[str], list[str]] | None:
    """For a markdown table row at 1-based lineno: (header cells, row cells)."""
    i = lineno - 1
    if not (0 <= i < len(lines)) or not lines[i].lstrip().startswith("|"):
        return None
    j = i
    while j > 0 and lines[j - 1].lstrip().startswith("|"):
        j -= 1
    split = lambda ln: [c.strip() for c in ln.strip().strip("|").split("|")]
    return split(lines[j]), split(lines[i])


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kit", type=Path, default=SCRIPT_DIR.parent)
    ap.add_argument("--repo-root", type=Path, default=None, help="read-only clone at the audited commit")
    ap.add_argument("--generated-at", default=None)
    ap.add_argument("--split-threshold-mb", type=float, default=15.0,
                    help="also write per-source-doc files when a single file exceeds this size")
    ap.add_argument("--force-split", action="store_true")
    a = ap.parse_args()
    K = a.kit
    O, REM = K / "audit-output", K / "remediation"
    cfg = load(K / "audit-config.json", {}) or {}
    idx = load(O / "requirements_index.json", {})
    trace = load(O / "traceability_detail.json", {}) or {}
    mem = load(O / "audit-memory.json", {}) or {}
    ev = load(O / "evidence" / "evidence.json", {}) or {}
    TR = O / "test_results_merged" if (O / "test_results_merged" / "summary.json").is_file() else O / "test_results"
    tsum = (load(TR / "summary.json", {}) or {}).get("counts") or {}
    perreq = load(TR / "per_requirement.json", {}) or {}
    rtasks = {t["requirement_id"]: t for t in (load(REM / "requirement_tasks.json", {}) or {}).get("tasks", [])}
    ftj = load(REM / "findings_tasks.json", {}) or {}
    ftasks = ftj.get("tasks", [])
    dups = {t["requirement_id"]: t for t in (load(REM / "duplicate_id_tasks.json", {}) or {}).get("tasks", [])}
    orphans = load(REM / "orphan_test_ids.json", {}) or {}
    commit = mem.get("audited_commit") or idx.get("commit") or ev.get("git_commit") or "UNKNOWN"
    gen_at = a.generated_at or (mem.get("last_audit_date") or "")[:10] or "UNKNOWN"
    repo_cfg = cfg.get("repo") or {}
    repo_url, branch = repo_cfg.get("url", ""), repo_cfg.get("branch", "")
    line_tpl = (cfg.get("links") or {}).get("code_line_template", "")
    file_tpl = (cfg.get("links") or {}).get("code_file_template", "")
    policy = mem.get("proof_policy_version") or cfg.get("proof_policy_version") or "1.1.0"
    repo = Repo(a.repo_root or Path(repo_cfg.get("local_clone_path", "")), commit)

    def gh(path: str, start=None, end=None) -> str:
        if start and line_tpl:
            return line_tpl.format(commit=commit, path=path, start=start, end=end or start)
        return file_tpl.format(commit=commit, path=path) if file_tpl else ""

    def site_link(site: str) -> str:
        m = re.match(r"^(.*?):(\d+)(?:-(\d+))?$", site)
        if not m:
            return code(site)
        return f"[{code(site)}]({gh(m.group(1), m.group(2), m.group(3) or m.group(2))})"

    reqs = sorted(idx.get("requirements") or [], key=lambda r: r["id"])
    by_id = {r["id"]: r for r in reqs}
    known_ids = set(by_id)
    doc_order = [f["file"] for f in idx.get("files") or []]
    by_doc = collections.defaultdict(list)
    for r in reqs:
        by_doc[r["source_file"]].append(r)
    for d in by_doc:
        by_doc[d].sort(key=lambda r: (r["line_range"][0], r["id"]))
    docs = [d for d in doc_order if d in by_doc] + sorted(d for d in by_doc if d not in doc_order)

    # per-case test status from merged junit
    case_status: dict[str, str] = {}
    xml = TR / "tests.xml"
    if xml.is_file():
        for tc in ET.parse(xml).getroot().iter("testcase"):
            k = f"{tc.get('classname')}::{PARAM_RE.sub('', tc.get('name') or '')}"
            st = "passed"
            for ch in tc:
                if ch.tag in ("failure", "error"):
                    st = "failed"
                elif ch.tag == "skipped" and st != "failed":
                    st = "skipped"
            prev = case_status.get(k)
            case_status[k] = "failed" if "failed" in (prev, st) else ("passed" if "passed" in (prev, st) else st)

    file_of_case: dict[str, str] = {}

    def case_file(key: str) -> str | None:
        cls = key.split("::")[0]
        if cls not in file_of_case:
            parts, found = cls.split("."), None
            for i in range(len(parts), 0, -1):
                cand = "/".join(parts[:i]) + ".py"
                if repo.exists(cand):
                    found = cand
                    break
            file_of_case[cls] = found
        return file_of_case[cls]

    # FT task -> affected requirement ids (via RT depends_on)
    ft_reqs = collections.defaultdict(set)
    for rid, t in rtasks.items():
        for dep in t.get("depends_on") or []:
            if dep != "FT-F04" and dep != "FT-F09":
                ft_reqs[dep].add(rid)

    # ------------------------------------------------ per-requirement derived data
    def verbatim(r) -> tuple[str, str]:
        lines = repo.lines(r["source_file"])
        a_, b_ = r["line_range"]
        if lines is not None and 1 <= a_ <= len(lines):
            txt = "\n".join(lines[a_ - 1:b_])
            note = f"source lines {a_}-{b_} at {commit[:7]}"
        else:
            txt, note = r.get("raw_text") or "", "parser raw_text (clone not at audited commit)"
        if len(txt) > MAX_VERBATIM:
            txt, note = txt[:MAX_VERBATIM], note + f"; truncated at {MAX_VERBATIM} chars, see the source link"
        return txt, note

    def table_ctx(r):
        if r.get("definition_site") != "table_row":
            return None
        lines = repo.lines(r["source_file"])
        return table_context(lines, r["line_range"][0]) if lines else None

    def dependencies(r, text: str, ctx) -> list[str]:
        out = []
        if ctx:
            hdr, row = ctx
            for i, h in enumerate(hdr):
                if re.search(r"depend|prereq", h, re.I) and i < len(row) and row[i] and row[i] not in ("—", "-", ""):
                    out.append(f"{h}: {row[i]}")
        for ln in text.splitlines():
            m = DEP_LABEL_RE.match(ln)
            if m:
                out.append(f"{m.group(1).strip().title()}: {m.group(2).strip()}"[:300])
            if ln.lstrip().startswith("|") and re.search(r"(?i)\|\s*depends on\s*\|", ln):
                hdr = [c.strip() for c in ln.strip().strip("|").split("|")]
                nxt = text.splitlines()
                k = nxt.index(ln)
                for row in nxt[k + 1:k + 3]:
                    cells = [c.strip() for c in row.strip().strip("|").split("|")]
                    if set("".join(cells)) <= set("-: "):
                        continue
                    for i, h in enumerate(hdr):
                        if h.lower().startswith("depends") and i < len(cells):
                            out.append(f"{h}: {cells[i]}")
                    break
        seen, res = set(), []
        for x in out:
            if x.lower() not in seen:
                seen.add(x.lower())
                res.append(x)
        return res

    def referenced_ids(rid: str, text: str) -> list[str]:
        ids = {m for m in ID_TOKEN_RE.findall(text) if m in known_ids and m != rid and not m.startswith(rid + ".")}
        return sorted(ids)

    def verbatim_acs(r, text: str) -> list[str]:
        norm_text = re.sub(r"\s+", " ", text)
        out = []
        for ac in r.get("acceptance_criteria") or []:
            s = re.sub(r"\s+", " ", ac).strip()
            if (len(s.split()) < 4 or s.count("|") >= 2 or s.lower().startswith("aggregated title")
                    or s.startswith(r["id"] + ".") and False):
                continue
            if s in norm_text and s not in out:
                out.append(s)
        return out

    # ------------------------------------------------ components (from repo reading)
    COMPONENTS = [
        ("api", "API service (FastAPI)", ("apps/api/",),
         "`apps/api/main.py:create_app` is the uvicorn factory (deploy/Dockerfile CMD `uvicorn apps.api.main:create_app --factory`). "
         "It builds the graph store (`create_store`), JobQueue, SourceRegistry, AcquisitionScheduler, WebhookGateway, ChangeJournal, "
         "GraphEvolutionEngine, AuditSink, ValidationEngine and AgentRuntime, wraps `apps/api/app.py:query_app` (core query/graph routes) "
         "behind bearer auth (`SafeHTTPBearer`), adds `apps/api/extended.py:ensure_extended` (extended routers incl. processing units "
         "and advanced capabilities), loads role/token keys via `apps/api/asg.py`, and mounts the REVA router at `/api/reva/v1` when enabled. "
         "Compose service `eoip-api`, 127.0.0.1:8000, health `/health/ready`."),
        ("worker", "Job worker", ("apps/worker/",),
         "`apps/worker/main.py:main` runs a polling loop over the durable JobQueue; `execute_job` dispatches configured source syncs, "
         "file, GitHub, GitLab and Jira ingestion operations and the default graph consumers. Compose service `eoip-worker`."),
        ("mcp", "MCP server", ("apps/mcp/",),
         "`apps/mcp/main.py:create_app` builds a FastMCP server whose tools (search, entity, path, impact, lineage, trace_impact, "
         "list_agents, run_agent, agent_explanation, blast_radius, graph_surprises, validate_ontology, neighbors, document, code_symbol) "
         "proxy the API with the bearer token from `eoip.runtime.api_token`. Compose service `eoip-mcp`, 127.0.0.1:8001."),
        ("graph", "Graph layer + HugeGraph", ("packages/eoip/graph/",),
         "`packages/eoip/graph/backends.py` selects the store (HugeGraph via `EOIP_HUGEGRAPH_URL`, RDF backend, in-memory); "
         "`database_adapters.py` holds adapter variants (finding F-08: f-string SQL). Runtime: compose `hugegraph-server` 1.7.0 + "
         "`schema-init`, Hubble UI (`hubble`, `hubble-init`, 127.0.0.1:8088)."),
        ("core", "Core library (packages/eoip, excl. graph)", ("packages/eoip/",),
         "Python package `eoip` (pyproject). Top-level modules include `platform_router.py` (platform routes: token formats, intent "
         "routing, ...), `runtime.py` (`data_root`, `api_token`), `jobs.py`, `cli.py` (`eoip` console script), `demo.py`. "
         "Largest subpackages are listed below."),
        ("reva", "REVA subsystem", ("reva/",),
         "`reva/api/__init__.py:reva_router` (warrants, logs, gaps, ... routers) mounted by the API; plus `reva/worker.py`, "
         "`sandbox/` (process runner), `kernel/`, `mcp/`, `pd/`, `graph/`. Own compose file `docker-compose.reva.yml`."),
        ("web", "Web UI (React + Vite)", ("apps/web/",),
         "`apps/web/src/main.jsx` -> `App.jsx`; feature areas `admin/`, `kgr/`, `studio/`, `dashboards/`, `cognitive/`, `design-system/`. "
         "Scripts: `vite build`, `tsc --noEmit`, node `test:unit` (needs node 22), Playwright e2e/a11y. Compose `eoip-web` (nginx), 127.0.0.1:8080."),
        ("vscode", "VS Code extension", ("apps/vscode-extension/",),
         "`apps/vscode-extension/extension.js` (package.json `main`) with `mcp-client.js`; node tests in `test/`; built by compose "
         "`extension-build`."),
        ("preview", "Preview shim (frontend/ + backend/)", ("frontend/", "backend/"),
         "`backend/server.py` sets env defaults and launches the API (F-02: hard-coded bootstrap token default); `frontend/` is a "
         "separate React sign-in preview (`src/screens/SignIn.tsx`, F-01/F-02)."),
        ("deploy", "Deploy, scripts, CI", ("deploy/", "scripts/", ".github/", "docker-compose", "config/"),
         "`deploy/Dockerfile` (runtime + test stages), `deploy/docker-compose*.yml` (stack, DLQ acceptance, HA, observability), "
         "`scripts/container.ps1` (up / hubble-local-admin / demo-data actions), `.github/workflows/` (CI, see F-04)."),
    ]

    def components_of(paths: list[str]) -> set[str]:
        out = set()
        for p in paths:
            p = p.split(":")[0]
            for key, _, prefixes, _ in COMPONENTS:
                if any(p.startswith(x) for x in prefixes):
                    out.add(key)
                    break
            else:
                if p.startswith("tests/"):
                    continue
                out.add("other")
        return out

    # ------------------------------------------------ build entries
    entries = {}
    for r in reqs:
        rid = r["id"]
        text, vnote = verbatim(r)
        ctx = table_ctx(r)
        vacs = verbatim_acs(r, text)
        rt = rtasks.get(rid) or {}
        tr = trace.get(rid) or {}
        m = (mem.get("requirements") or {}).get(rid) or {}
        entries[rid] = dict(
            r=r, text=text, vnote=vnote, ctx=ctx, deps=dependencies(r, text, ctx), refs=referenced_ids(rid, text),
            vacs=vacs, dacs=[] if vacs else list(rt.get("acceptance_criteria") or []), rt=rt, tr=tr, m=m,
            comps=components_of((tr.get("code") or []) + (tr.get("infra") or [])),
        )

    status_c = collections.Counter(e["m"].get("status", "Not Verified") for e in entries.values())
    tier_c = collections.Counter(e["m"].get("proof_tier_achieved", "L0") for e in entries.values())
    type_c = collections.Counter(r.get("type") for r in reqs)
    prio_c = collections.Counter(r.get("priority") or "UNKNOWN" for r in reqs)
    rprio_c = collections.Counter((rtasks.get(r["id"]) or {}).get("priority", "?") for r in reqs)
    site_c = collections.Counter(r.get("definition_site") for r in reqs)

    def header(title: str, kind: str) -> list[str]:
        return [f"# {title}", "",
                f"- **Repository:** [{repo_url}]({repo_url}) (branch `{branch}`)",
                f"- **Audited commit:** [`{commit}`]({repo_url}/tree/{commit})",
                f"- **Generated:** {gen_at} by `audit-scripts/generate_requirements_and_implementation_md.py` (deterministic, no LLM)",
                f"- **Proof policy:** {policy}",
                f"- **Scope:** {len(reqs)} requirement IDs parsed from {len(docs)} requirement documents ({kind})", ""]

    def write_both(single_path: Path, parts_dir: Path, head: list[str], intro: list[str], doc_sections: dict, tail: list[str],
                   other_name: str) -> dict:
        body = head + intro
        for d in docs:
            body += doc_sections[d](f"{other_name}.md")
        body += tail
        content = "\n".join(body) + "\n"
        single_path.write_text(content, encoding="utf-8")
        size_mb = len(content.encode("utf-8")) / 1e6
        split = a.force_split or size_mb > a.split_threshold_mb
        info = {"file": str(single_path.relative_to(K)), "bytes": len(content.encode("utf-8")), "split": split}
        if split:
            parts_dir.mkdir(exist_ok=True)
            ix = head + [f"Per-source-document files ({len(docs)}). Single-file version: [`../{single_path.name}`](../{single_path.name}).", "",
                         "| Source document | Requirements | File |", "|---|---|---|"]
            for d in docs:
                fn = slug(d) + ".md"
                (parts_dir / fn).write_text("\n".join(head + doc_sections[d](f"../{other_name}/{fn}")) + "\n", encoding="utf-8")
                ix.append(f"| {code(d)} | {len(by_doc[d])} | [{fn}]({fn}) |")
            ix += [""] + tail
            (parts_dir / "index.md").write_text("\n".join(ix) + "\n", encoding="utf-8")
            info["parts"] = len(docs) + 1
        return info

    # ================================================= requirements.md
    def req_doc_section(d):
        def render(impl_href: str) -> list[str]:
            L = [f'<a id="doc-{slug(d)}"></a>', "", f"## {inline(d)}", "",
                 f"{len(by_doc[d])} requirements. Source: [{code(d)}]({gh(d)}).", ""]
            for r in by_doc[d]:
                e = entries[r["id"]]
                rid, rt = r["id"], e["rt"]
                a_, b_ = r["line_range"]
                L += [f'<a id="{anchor(rid)}"></a>', "", f"### {inline(rid)}: {inline(r.get('title') or rid)}", "",
                      "| Field | Value |", "|---|---|",
                      f"| Source | [{code(f'{d}:{a_}-{b_}')}]({gh(d, a_, b_)}) ({cell(r.get('definition_site'))}) |",
                      f"| Type | {cell(r.get('type'))} |",
                      f"| Priority (document) | {cell(r.get('priority') or 'UNKNOWN')} |",
                      f"| Remediation priority (derived) | {cell(rt.get('priority', '?'))}: {cell(rt.get('priority_reason', ''))} |",
                      f"| Owner (document) | {cell(r.get('owner') or 'UNKNOWN')} |",
                      "| Dependencies (from source) | " + ("<br>".join(cell(x) for x in e["deps"]) or "none stated") + " |",
                      "| Other requirement IDs referenced in the text | " + (", ".join(f"[{x}](#{anchor(x)})" for x in e["refs"][:40])
                                                                          + (f" … +{len(e['refs']) - 40}" if len(e["refs"]) > 40 else "") or "none") + " |"]
                dup = dups.get(rid)
                if dup:
                    sites = dup.get("sites") or []
                    L.append(f"| Other definition sites ({len(sites)}, task DUP-{cell(rid)}) | "
                             + "<br>".join(f"{site_link(s['site'])} ({cell(s['kind'])})" for s in sites[:15])
                             + (f"<br>… +{len(sites) - 15} more (see `remediation/duplicate_id_tasks.json`)" if len(sites) > 15 else "") + " |")
                elif r.get("also_defined_at"):
                    L.append(f"| Sub-clause / reference sites ({len(r['also_defined_at'])}, not duplicates) | "
                             + ", ".join(site_link(s) for s in r["also_defined_at"][:10])
                             + (f" … +{len(r['also_defined_at']) - 10}" if len(r["also_defined_at"]) > 10 else "") + " |")
                st = e["m"].get("status", "Not Verified")
                L.append(f"| Implementation status | [{cell(st)} ({cell(e['m'].get('proof_tier_achieved', 'L0'))})]({impl_href}#{anchor(rid)}) |")
                L += ["", f"**Requirement text (verbatim, {e['vnote']}):**", ""]
                if e["ctx"]:
                    L += ["Table header (context): " + " \\| ".join(inline(h) for h in e["ctx"][0]), ""]
                L += [fence(e["text"] or "(empty)"), ""]
                if e["vacs"]:
                    L += ["**Acceptance criteria (verbatim from the source):**", ""]
                    L += [f"{i}. {inline(x)}" for i, x in enumerate(e["vacs"], 1)]
                else:
                    L += ["**Acceptance criteria (DERIVED by `generate_fix_tasks.py`; the source states none explicitly):**", ""]
                    L += [f"{i}. {inline(x)}" for i, x in enumerate(e["dacs"] or ["UNKNOWN: refine with the requirement owner"], 1)]
                L.append("")
            return L
        return render

    toc = ["## Contents", "", "- [Summary](#summary)"]
    for d in docs:
        toc.append(f"- [{inline(d)}](#doc-{slug(d)}) ({len(by_doc[d])})")
    toc += ["- [Orphan test-only IDs](#orphan-ids)", ""]
    for d in docs:
        toc.append(f"<details><summary>{cell(d)}: {len(by_doc[d])} IDs</summary>\n")
        toc.append(", ".join(f"[{r['id']}](#{anchor(r['id'])})" for r in by_doc[d]))
        toc.append("\n</details>\n")
    tbl = lambda c, h: [f"| {h[0]} | {h[1]} |", "|---|---|"] + [f"| {cell(k)} | {v} |" for k, v in c] + [""]
    n_sub = sum(1 for r in reqs if r.get("also_defined_at") and r["id"] not in dups)
    summ = ['<a id="summary"></a>', "", "## Summary", "",
            f"**{len(reqs)}** unique requirement IDs. Each appears once here, at its primary definition site.", ""]
    summ += ["### By type", ""] + tbl(type_c.most_common(), ("Type", "Count"))
    summ += ["### By document priority", "", "Most source docs state no priority (UNKNOWN). The derived remediation "
             "priority (`requirement_tasks.json`) is shown per entry and below.", ""] + tbl(sorted(prio_c.items()), ("Priority (document)", "Count"))
    summ += tbl(sorted(rprio_c.items()), ("Remediation priority (derived)", "Count"))
    summ += ["### By definition form", ""] + tbl(site_c.most_common(), ("Defined as", "Count"))
    summ += ["### By source document", "", "| Source document | Requirements | Functional | Security | Non-Functional | Other |", "|---|---|---|---|---|---|"]
    for d in docs:
        c = collections.Counter(r.get("type") for r in by_doc[d])
        L_other = sum(v for k, v in c.items() if k not in ("Functional", "Security", "Non-Functional"))
        summ.append(f"| [{cell(d)}](#doc-{slug(d)}) | {len(by_doc[d])} | {c.get('Functional', 0)} | {c.get('Security', 0)} | {c.get('Non-Functional', 0)} | {L_other} |")
    summ += ["", "### Duplicate IDs", "",
             f"- **{len(dups)}** IDs are genuinely defined more than once (same-doc or cross-doc redefinition). Each has a DUP-<ID> task "
             "(`remediation/duplicate_id_tasks.json`, parent FT-F09) and its other sites are listed in its entry.",
             f"- A further **{n_sub}** IDs only have sub-clause references (e.g. `CRA-001.1`) or mentions elsewhere. Those are listed but are not duplicates.",
             f"- **{orphans.get('count', len(orphans.get('ids') or []))}** IDs are used by tests but defined in no requirement doc ([orphans](#orphan-ids)).", ""]
    orph = ['<a id="orphan-ids"></a>', "", "## Orphan test-only IDs", "",
            cell(orphans.get("note", "")), "",
            "| ID | Mapped tests passed | Mapped tests failed |", "|---|---|---|"]
    orph += [f"| {code(o['id'])} | {o.get('passed', 0)} | {o.get('failed', 0)} |" for o in orphans.get("ids") or []]
    orph.append("")
    req_info = write_both(O / "requirements.md", O / "requirements",
                          header("EOIP requirements catalogue", "consolidated catalogue"),
                          ["Companion: [implementation.md](implementation.md) (status per requirement), "
                           "[audit_gaps_requirements.md](audit_gaps_requirements.md) (audit report).", ""] + toc + summ,
                          {d: req_doc_section(d) for d in docs}, orph, "implementation")

    # ================================================= implementation.md
    def tests_block(rid):
        pr = perreq.get(rid) or {}
        rank = {"failed": 0, "not run": 1, "skipped": 2, "passed": 3}
        cases = sorted(set(pr.get("tests") or []), key=lambda k: (rank.get(case_status.get(k, "not run"), 1), k))
        rows = []
        for k in cases[:30]:
            st = case_status.get(k, "not run")
            f = case_file(k)
            name = k.split("::", 1)[-1]
            ref = f"[{code(f + '::' + name)}]({gh(f)})" if f else code(k)
            rows.append(f"{'✅' if st == 'passed' else '❌' if st == 'failed' else '⏭'} {st}: {ref}")
        more = f"<br>… +{len(cases) - 30} more" if len(cases) > 30 else ""
        return pr, rows, more

    def impl_doc_section(d):
        def render(req_href: str) -> list[str]:
            L = [f'<a id="doc-{slug(d)}"></a>', "", f"## {inline(d)}", ""]
            c = collections.Counter(entries[r["id"]]["m"].get("status", "Not Verified") for r in by_doc[d])
            L += ["Status: " + ", ".join(f"{s} {c[s]}" for s in STATUS_ORDER if c.get(s)), ""]
            for r in by_doc[d]:
                rid = r["id"]
                e = entries[rid]
                m, rt, tr = e["m"], e["rt"], e["tr"]
                pr, trows, more = tests_block(rid)
                codes = list(dict.fromkeys((tr.get("code") or [])))
                code_cells = []
                for c_ in codes[:25]:
                    p, _, ln = c_.rpartition(":")
                    code_cells.append(f"[{code(c_)}]({gh(p, ln, ln) if ln.isdigit() else gh(c_)})")
                infra = [f"[{code(x)}]({gh(x.rpartition(':')[0] or x, x.rpartition(':')[2] if x.rpartition(':')[2].isdigit() else None)})"
                         for x in (tr.get("infra") or [])[:10]]
                test_files = sorted(set((tr.get("tests") or []) + (tr.get("test_map_nodeids") or [])))
                ft_links = [x for x in rt.get("depends_on") or []]
                tasks = [f"RT-{rid}"] + ([f"DUP-{rid}"] if rid in dups else []) + ft_links
                missing = list((rt.get("proof_plan") or {}).get("missing") or [])
                if "L2" in missing and pr.get("failed"):
                    missing[missing.index("L2")] = f"clean L2 (all mapped tests passing; {pr.get('failed')} failing now)"
                elif "L2" in missing:
                    missing[missing.index("L2")] = "L2 (a passing mapped test on this commit)"
                la, lb = r["line_range"]
                src_ref = f"{d}:{la}"
                L += [f'<a id="{anchor(rid)}"></a>', "", f"### {inline(rid)}: {inline(r.get('title') or rid)}", "",
                      "| Field | Value |", "|---|---|",
                      f"| Status | **{cell(m.get('status', 'Not Verified'))}** (proof tier {cell(m.get('proof_tier_achieved', 'L0'))}) |",
                      f"| Requirement | [{cell(rid)} in requirements.md]({req_href}#{anchor(rid)}) · [{code(src_ref)}]({gh(d, la, lb)}) |",
                      f"| Components | {cell(', '.join(sorted(e['comps'])) or 'none (no code trace)')} |",
                      "| Code (L1 references) | " + ("<br>".join(code_cells) + (f"<br>… +{len(codes) - 25} more" if len(codes) > 25 else "") or "none found") + " |",
                      "| Infra references | " + ("<br>".join(infra) or "none") + " |",
                      f"| Mapped tests (merged run) | {pr.get('passed', 0)} passed, {pr.get('failed', 0)} failed, {pr.get('skipped', 0)} skipped"
                      + ("<br>" + "<br>".join(trows) + more if trows else "") + " |",
                      "| Test files referencing the ID | " + (", ".join(code(x) for x in test_files[:15]) + (f" … +{len(test_files) - 15}" if len(test_files) > 15 else "") or "none") + " |",
                      "| Evidence IDs | " + (", ".join(code(x) for x in (m.get("evidence_ids") or [])[:10]) or "none") + " |",
                      "| Residual gaps | " + ("<br>".join(cell(g) for g in (m.get("residual_gaps") or rt.get("gaps") or [])[:8]) or "none recorded") + " |",
                      f"| Gap category | {cell(rt.get('gap_category', '?'))} |",
                      "| Fix tasks | " + ", ".join(code(t) for t in tasks) + " |",
                      "| Needed for Implemented (policy " + policy + ") | " + (cell("; ".join(missing)) or "none") +
                      ("; L5 independent review (Critical)" if rt.get("derived_severity") == "Critical" and not any("L5" in x for x in missing) else "") + " |",
                      ""]
            return L
        return render

    ex_comp = []
    for key, name, prefixes, desc in COMPONENTS:
        files = [f for p in prefixes for f in repo.ls(p)] if not prefixes[0].startswith("docker-compose") else []
        if key == "core":
            files = [f for f in repo.ls("packages/eoip/") if not f.startswith("packages/eoip/graph/")]
        py = sum(f.endswith(".py") for f in files)
        js = sum(f.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs")) for f in files)
        ex_comp.append((key, name, len(files), py, js, desc))
    core_sub = collections.Counter(f.split("/")[2] for f in repo.ls("packages/eoip/") if f.count("/") >= 3 and f.endswith(".py"))
    services = []
    dc = repo.lines("deploy/docker-compose.yml") or []
    in_services = False
    for ln in dc:
        if re.match(r"^\S", ln):
            in_services = ln.startswith("services:")
            continue
        mm = re.match(r"^  ([a-z0-9-]+):\s*$", ln)
        if in_services and mm:
            services.append(mm.group(1))
    if "volumes:" in [x.strip() for x in dc]:
        pass
    arch = ["## Architecture and stack (what is actually built)", "",
            "From reading the repo at the audited commit (entry points and wiring), not from the docs' claims. File counts come from "
            f"`git ls-files` at `{commit[:7]}`.", "",
            "| Component | Files | .py | JS/TS | Key modules and entry points |", "|---|---|---|---|---|"]
    arch += [f"| {cell(n)} | {f} | {p} | {j} | {d_.replace('|', '/')} |" for _, n, f, p, j, d_ in ex_comp]
    arch += ["", "Largest `packages/eoip` subpackages by Python files: " +
             ", ".join(f"`{k}` ({v})" for k, v in core_sub.most_common(25)) + ".", "",
             "Compose (`deploy/docker-compose.yml`) declares: " + ", ".join(f"`{s}`" for s in services) + ". "
             "Extended run: the stack only came up with workarounds (X-03 numpy missing from the runtime image, X-04 Hubble password "
             "length), see [Known defects](#known-defects).", ""]
    comp_names = {k: n for k, n, *_ in COMPONENTS} | {"other": "Other paths", "none": "No code trace"}
    cov = collections.defaultdict(collections.Counter)
    for e in entries.values():
        for c in (e["comps"] or {"none"}):
            cov[c][e["m"].get("status", "Not Verified")] += 1
    covt = ["## Implementation coverage per component", "",
            "A requirement counts for every component its L1 code/infra references touch, so rows overlap. Status is the audit status, "
            "not the component's own claim.", "",
            "| Component | Requirements | " + " | ".join(STATUS_ORDER[:4]) + " |", "|---|---|" + "---|" * 4]
    for k in [c[0] for c in COMPONENTS] + ["other", "none"]:
        if cov.get(k):
            covt.append(f"| {cell(comp_names[k])} | {sum(cov[k].values())} | " + " | ".join(str(cov[k].get(s, 0)) for s in STATUS_ORDER[:4]) + " |")
    covt.append("")
    execs = ["## Executive summary", "",
             "| Status | Count |", "|---|---|"] + [f"| {s} | {status_c.get(s, 0)} |" for s in STATUS_ORDER if s != "Not Implemented" or status_c.get(s)]
    execs += ["", "| Highest proof tier | Count |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(tier_c.items())]
    execs += ["", f"Tests (`{TR.name}/`: main run, with extended-run results overriding the same test case): **{tsum.get('cases', '?')}** cases, "
              f"**{tsum.get('passed', '?')}** passed, **{tsum.get('failed', '?')}** failed, **{tsum.get('skipped', '?')}** skipped.", "",
              "**Implemented: 0.** No L3-eligible CI run is green on this commit and no L4/L5 evidence exists, so under policy "
              f"{policy} nothing can reach Implemented. *Partially Implemented* means at least one mapped test passed locally (L2) "
              "and residual gaps remain. The requirement→test mapping is the repo's own and has not been independently reviewed. "
              "*Ambiguous* means mapped tests both pass and fail. *Not Verified* means an L1 code reference only, or nothing.", ""]
    toc2 = ["## Contents", "", "- [Executive summary](#executive-summary)", "- [Architecture and stack](#architecture-and-stack-what-is-actually-built)",
            "- [Coverage per component](#implementation-coverage-per-component)", "- [Known defects](#known-defects)"]
    toc2 += [f"- [{inline(d)}](#doc-{slug(d)}) ({len(by_doc[d])})" for d in docs] + [""]
    # known defects
    kd = ['<a id="known-defects"></a>', "", "## Known defects affecting implementation (FT / X tasks)", "",
          "Hand-written tasks from `remediation/findings_tasks.json` (findings F-*, defects D-*, extended-run X-*, harness H-*). "
          "Affected requirements are those whose RT task depends on the FT task (via failing mapped tests).", "",
          "| Task | Priority | Status | Defect / finding | Title | Failing tests | Affected requirements |", "|---|---|---|---|---|---|---|"]
    for t in ftasks:
        aff = sorted(ft_reqs.get(t["id"], set()))
        xs = (t.get("extended_run") or {}).get("defect") or ""
        kd.append(f"| {code(t['id'])} | {t['priority']} | {cell(t.get('status', 'Open'))} | {cell(', '.join(x for x in (t.get('finding'), xs) if x))} | "
                  f"{cell(t['title'])} | {len(t.get('tests_covered') or [])} | "
                  + ({"FT-F04": f"all {len(rtasks)} RT tasks (no L3 possible until CI is real)",
                      "FT-F09": f"{len(dups)} duplicate IDs (DUP-* tasks)"}.get(t["id"])
                     or ", ".join(f"[{x}](#{anchor(x)})" for x in aff[:20]) + (f" … +{len(aff) - 20}" if len(aff) > 20 else "")
                     or "none via failing tests") + " |")
    kd += ["", "Full task detail: `remediation/findings_tasks.md`.", ""]
    impl_info = write_both(O / "implementation.md", O / "implementation",
                           header("EOIP implementation status against requirements", "implementation status"),
                           ["Companion: [requirements.md](requirements.md) (verbatim requirements), "
                            "[audit_gaps_requirements.md](audit_gaps_requirements.md) (audit report).", ""] + toc2 + execs + arch + covt + kd,
                           {d: impl_doc_section(d) for d in docs}, [], "requirements")
    print(json.dumps({"requirements": req_info, "implementation": impl_info, "verbatim_from_repo": repo.at_commit,
                      "status": dict(status_c), "entries": len(entries)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
