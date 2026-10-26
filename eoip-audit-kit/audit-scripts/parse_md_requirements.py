#!/usr/bin/env python3
"""Parse requirement .md files into requirements_index.json (+ optional CSV).

Recognised *definition sites* (an ID merely mentioned in prose is NOT a definition):
  1. Heading:      ## CRA-001. Title   |  ### `PUR-SEC-01` — Title  |  ## REQ-FUNC-0001: Title
  2. Table row:    | PUR-SEC-01 | Title | ... (first cell is the ID; header row gives columns)
  3. List item:    - **WG-CAP-03** — text   |   * `GN-12`: text
  4. Block field:  ID: REQ-SEC-0002   (with Title:, Type:, Priority:, Acceptance Criteria:)
Fallback for included files that define no IDs: H2/H3 sections whose body contains
normative MUST/SHALL become records with synthetic ids DOC-<ABBR>-NNNN (flagged synthetic).

IDs are generic: PREFIX(-SEGMENT)*-NUMBER, e.g. CRA-001, PUR-SEC-01, REQ-FUNC-0001.
Standards identifiers (SHA-256, ISO-27001, CVE-, RFC-, WCAG-2 ...) are excluded.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import re
import sys
from pathlib import Path

ID_CORE = r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{1,5}[a-z]?(?:\.(?:\d+|[A-Z]))*"
ID_RE = re.compile(rf"\b({ID_CORE})\b")
NOT_REQ_PREFIXES = {
    "SHA", "ISO", "IEC", "IEEE", "UTF", "CVE", "CWE", "RFC", "NIST", "SP", "WCAG", "HTTP", "TLS",
    "AES", "PEP", "GPL", "LGPL", "AGPL", "MIT", "BSD", "CC", "SPDX", "OWASP", "ASVS", "PCI", "SOC",
    "GDPR", "ES", "ECMA", "X", "P", "L", "V", "H", "COVID", "GPT", "BERT", "MD", "RSA", "ED",
    "E", "S", "T", "Q", "W", "PHASE", "STEP", "SECTION", "FIG", "TABLE", "APPENDIX", "PR", "ISSUE",
}
DEFAULT_SKIP_DIRS = {".git", "node_modules", "audit-output", ".venv", "venv", "__pycache__",
                     ".tmp", ".audit-scratch", ".eoip-data"}
DEFAULT_EXCLUDE = ["*implementation*", "*/audits/*", "*/tickets/*", "*traceability*", "*tracker*"]
# Families that are decisions / risks / work packages / comparison notes, not requirements.
DEFAULT_EXCLUDE_PREFIXES = ["D", "DEC", "DEC-*", "ADR", "RK", "RISK", "WP", "XP", "ASM", "OQ", "Q"]
DEFAULT_INCLUDE = ["*requirement*.md", "*reqirement*.md", "*-requirements*.md", "REQUIREMENTS*.md"]

HEADING_RE = re.compile(rf"^(#{{1,6}})\s+[`*_]*({ID_CORE})[`*_]*\s*[.:\-—–)]*\s*(.*)$")
TABLE_ROW_RE = re.compile(rf"^\|\s*[`*_\[]*({ID_CORE})[`*_\]]*\s*\|(.*)$")
LIST_RE = re.compile(rf"^\s*[-*+]\s+(?:\[[ xX]\]\s+)?[`*_]*({ID_CORE})[`*_]*(?:\s*[:.\-—–)]+\s*|\s+)(.+)$")
BLOCK_RE = re.compile(rf"^(?:\*\*)?ID(?:\*\*)?\s*:\s*[`*]*({ID_CORE})[`*]*\s*$", re.I)
NORMATIVE_RE = re.compile(r"\b(MUST|SHALL|REQUIRED)\b")

TYPE_HINTS = [
    ("Security", ("SEC", "AUTH", "AUTHZ", "PRIV", "THREAT", "SR-SEC", "IAM", "CRYPTO")),
    ("Compliance", ("COMP", "LIC", "LEGAL", "GOV", "AUDIT", "IP", "CIP")),
    ("AI", ("AI", "LLM", "AGT", "AGENT", "RAG", "NEU", "GN", "ML", "MODEL", "AIDLC", "NS")),
    ("Infra", ("INFRA", "DEP", "DEPLOY", "K8S", "OPS", "CI", "CD", "DOCKER", "RUN")),
    ("Non-Functional", ("NFR", "PERF", "REL", "SCAL", "OBS", "DR", "BAK", "A11Y", "UX", "VER")),
]


def strip_md(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"[`*_]+", "", s)
    s = s.replace("\\|", "|")
    return re.sub(r"\s+", " ", s).strip(" |—–-:.")


EXCLUDED_PREFIXES: list[str] = list(DEFAULT_EXCLUDE_PREFIXES)


def is_req_id(rid: str) -> bool:
    prefix = rid.split("-")[0]
    family = rid.rsplit("-", 1)[0]
    if any(fnmatch.fnmatch(family, g) for g in EXCLUDED_PREFIXES):
        return False
    if prefix in NOT_REQ_PREFIXES:
        return False
    if len(prefix) < 2 and prefix not in {"D", "C", "G", "R"}:
        return False
    return True


def guess_type(rid: str, text: str = "") -> str:
    segs = set(rid.split("-")[:-1])
    for tname, keys in TYPE_HINTS:
        if segs & set(keys) or any(rid.startswith(k + "-") for k in keys if "-" in k):
            return tname
    low = text.lower()
    if any(w in low for w in ("authenticat", "authoriz", "secret", "encrypt", "rbac", "tenant isolation")):
        return "Security"
    if any(w in low for w in ("latency", "throughput", "p95", "availability", "backup", "restore")):
        return "Non-Functional"
    return "Functional"


def priority_from(text: str) -> str:
    m = re.search(r"\b(P[0-3])\b", text)
    if m:
        return m.group(1)
    m = re.search(r"\b(MUST|SHOULD|MAY)\b", text)
    return {"MUST": "P1", "SHOULD": "P2", "MAY": "P3"}[m.group(1)] if m else "UNKNOWN"


def field(body: str, name: str) -> str | None:
    m = re.search(rf"^\s*[-*]?\s*(?:\*\*)?{name}(?:\*\*)?\s*:\s*(.+)$", body, re.M | re.I)
    return strip_md(m.group(1)) if m else None


def acceptance(body: str) -> list[str]:
    out, on = [], False
    for line in body.splitlines():
        if re.search(r"acceptance(\s+criteria)?|verification|definition of done", line, re.I) and (
            line.lstrip().startswith(("#", "*", "-", "|")) or ":" in line
        ):
            on = True
            rest = re.split(r"(?i)acceptance criteria\s*:?|acceptance\s*:?", line, maxsplit=1)
            tail = strip_md(rest[1]) if len(rest) > 1 else ""
            if tail and len(tail) > 3:
                out.append(tail)
            continue
        if on:
            if re.match(r"^#{1,6}\s", line) or re.match(r"^\s*(\*\*)?[A-Z][A-Za-z ]{2,30}(\*\*)?:\s", line):
                break
            s = strip_md(re.sub(r"^\s*(?:[-*+]|\d+[.)])\s*", "", line))
            if s:
                out.append(s)
    return out


def parse_table_header(cells: list[str]) -> dict[str, int]:
    idx = {}
    for i, c in enumerate(cells):
        lc = c.lower()
        if "accept" in lc or "verif" in lc or "evidence" in lc:
            idx.setdefault("ac", i)
        elif "prior" in lc or lc in ("p", "moscow"):
            idx.setdefault("priority", i)
        elif "type" in lc or "category" in lc:
            idx.setdefault("type", i)
        elif "owner" in lc:
            idx.setdefault("owner", i)
        elif any(w in lc for w in ("requirement", "title", "description", "statement", "capability", "name")):
            idx.setdefault("title", i)
    return idx


def split_row(line: str) -> list[str]:
    body = line.strip()
    body = body[1:] if body.startswith("|") else body
    body = body[:-1] if body.endswith("|") else body
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def section_end(lines: list[str], start: int, level: int) -> int:
    for j in range(start + 1, len(lines)):
        m = re.match(r"^(#{1,6})\s", lines[j])
        if m and len(m.group(1)) <= level:
            return j
    return len(lines)


def extract(text: str, rel: str) -> list[dict]:
    lines = text.splitlines()
    recs: list[dict] = []
    header: dict[str, int] | None = None
    prev_cells: list[str] | None = None
    in_code = False

    def rec(rid, title, start, end, body, site, extra=None):
        r = {
            "id": rid,
            "title": strip_md(title)[:300] or rid,
            "type": guess_type(rid, body),
            "priority": priority_from(body),
            "owner": "UNKNOWN",
            "acceptance_criteria": acceptance(body),
            "related_files": sorted(set(re.findall(r"`((?:apps|packages|reva|tests|scripts|deploy|config|schemas|frontend|backend)/[\w./-]+)`", body))),
            "line_range": [start + 1, max(start + 1, end)],
            "source_file": rel,
            "definition_site": site,
            "normative": bool(NORMATIVE_RE.search(body)),
            "synthetic_id": False,
            "raw_text": body,
        }
        if extra:
            r.update({k: v for k, v in extra.items() if v})
        recs.append(r)

    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        if line.lstrip().startswith("|"):
            cells = split_row(line)
            if all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells if c.strip()) and prev_cells:
                header = parse_table_header(prev_cells)
                prev_cells = cells
                continue
            m = TABLE_ROW_RE.match(line)
            if m and is_req_id(m.group(1)):
                rid = m.group(1)
                hdr = header or {}
                ti = hdr.get("title", 1)
                title = cells[ti] if ti < len(cells) else (cells[1] if len(cells) > 1 else rid)
                if len(strip_md(title).split()) <= 2:
                    # short tag-like cell ("extend", "merge"): add the most descriptive other cell
                    others = [c for j, c in enumerate(cells) if j not in (0, ti) and len(strip_md(c).split()) >= 4]
                    if others:
                        best = max(others, key=lambda c: len(c))
                        title = (strip_md(title) + ": " if strip_md(title) else "") + strip_md(best)[:200]
                body = line
                extra = {}
                if "ac" in hdr and hdr["ac"] < len(cells):
                    extra["acceptance_criteria"] = [strip_md(cells[hdr["ac"]])] if strip_md(cells[hdr["ac"]]) else None
                if "priority" in hdr and hdr["priority"] < len(cells):
                    extra["priority"] = strip_md(cells[hdr["priority"]]) or None
                if "owner" in hdr and hdr["owner"] < len(cells):
                    extra["owner"] = strip_md(cells[hdr["owner"]]) or None
                rec(rid, title, i, i + 1, body, "table_row", extra)
            prev_cells = cells
            continue
        header, prev_cells = None, None

        m = HEADING_RE.match(line)
        if m and is_req_id(m.group(2)):
            level = len(m.group(1))
            end = section_end(lines, i, level)
            body = "\n".join(lines[i:end])
            rec(m.group(2), m.group(3) or m.group(2), i, end, body, "heading",
                {"type": field(body, "Type"), "owner": field(body, "Owner")})
            continue

        m = BLOCK_RE.match(line)
        if m and is_req_id(m.group(1)):
            end = len(lines)
            for j in range(i + 1, len(lines)):
                if BLOCK_RE.match(lines[j]) or lines[j].startswith("---") or re.match(r"^#{1,6}\s", lines[j]):
                    end = j
                    break
            body = "\n".join(lines[i:end])
            rec(m.group(1), field(body, "Title") or m.group(1), i, end, body, "id_block",
                {"type": field(body, "Type"), "owner": field(body, "Owner")})
            continue

        m = LIST_RE.match(line)
        if m and is_req_id(m.group(1)):
            end = i + 1
            while end < len(lines) and lines[end].startswith(("  ", "\t")) and lines[end].strip():
                end += 1
            body = "\n".join(lines[i:end])
            rec(m.group(1), m.group(2), i, end, body, "list_item")
    return recs


def fallback_headings(text: str, rel: str, abbr: str) -> list[dict]:
    lines = text.splitlines()
    out, n = [], 0
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if not m:
            continue
        end = section_end(lines, i, len(m.group(1)))
        body = "\n".join(lines[i:end])
        if not NORMATIVE_RE.search(body):
            continue
        n += 1
        rid = f"DOC-{abbr}-{n:04d}"
        out.append({
            "id": rid, "title": strip_md(m.group(2))[:300], "type": guess_type(rid, body),
            "priority": priority_from(body), "owner": "UNKNOWN", "acceptance_criteria": acceptance(body),
            "related_files": [], "line_range": [i + 1, end], "source_file": rel,
            "definition_site": "heading_fallback", "normative": True, "synthetic_id": True,
            "raw_text": body,
        })
    return out


def abbr_for(path: Path) -> str:
    words = re.findall(r"[A-Za-z0-9]+", path.stem)
    a = "".join(w[0] for w in words).upper()
    return (a or "X")[:8]


def iter_md(root: Path, include: list[str], exclude: list[str], all_md: bool):
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if any(part in DEFAULT_SKIP_DIRS for part in rel.parts):
            continue
        rs = str(rel).replace("\\", "/")
        if any(fnmatch.fnmatch(rs, g) or fnmatch.fnmatch(p.name, g) for g in exclude):
            continue
        if all_md or any(fnmatch.fnmatch(p.name, g) or fnmatch.fnmatch(rs, g) for g in include):
            yield p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--commit", default="")
    ap.add_argument("--csv", dest="csv_out", default="")
    ap.add_argument("--include", default=",".join(DEFAULT_INCLUDE),
                    help="Comma-separated filename/path globs of requirement docs")
    ap.add_argument("--exclude", default=",".join(DEFAULT_EXCLUDE), help="Comma-separated globs to skip")
    ap.add_argument("--exclude-prefixes", default=",".join(DEFAULT_EXCLUDE_PREFIXES),
                    help="ID families (globs, number stripped) that are not requirements")
    ap.add_argument("--all-md", action="store_true", help="Parse every .md (noisy: audits/plans reference ids)")
    ap.add_argument("--no-fallback", action="store_true", help="Disable DOC-* heading fallback")
    args = ap.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: --root not a directory: {root}", file=sys.stderr)
        return 2
    include = [g.strip() for g in args.include.split(",") if g.strip()]
    exclude = [g.strip() for g in args.exclude.split(",") if g.strip()]
    EXCLUDED_PREFIXES[:] = [g.strip() for g in args.exclude_prefixes.split(",") if g.strip()]

    by_id: dict[str, dict] = {}
    dup_sites: dict[str, list[str]] = {}
    files_report = []
    used_abbr: dict[str, int] = {}
    for md in iter_md(root, include, exclude, args.all_md):
        rel = str(md.relative_to(root)).replace("\\", "/")
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"WARN: skip {rel}: {e}", file=sys.stderr)
            continue
        recs = extract(text, rel)
        site = "ids"
        if not recs and not args.no_fallback:
            ab = abbr_for(md)
            used_abbr[ab] = used_abbr.get(ab, 0) + 1
            if used_abbr[ab] > 1:
                ab = f"{ab}{used_abbr[ab]}"
            recs = fallback_headings(text, rel, ab)
            site = "fallback"
        new = 0
        for r in recs:
            if r["id"] in by_id:
                dup_sites.setdefault(r["id"], []).append(f"{rel}:{r['line_range'][0]}")
                continue
            by_id[r["id"]] = r
            new += 1
        files_report.append({"file": rel, "records": len(recs), "new_ids": new, "mode": site})

    for rid, sites in dup_sites.items():
        by_id[rid]["also_defined_at"] = sites
        by_id[rid]["duplicate_definitions"] = len(sites)

    requirements = sorted(by_id.values(), key=lambda r: (r["source_file"], r["line_range"][0]))
    prefixes: dict[str, int] = {}
    for r in requirements:
        p = r["id"].rsplit("-", 1)[0]
        prefixes[p] = prefixes.get(p, 0) + 1
    out = {
        "schema_hint": "requirements_index/1.1",
        "commit": args.commit or None,
        "root": str(root),
        "include": include,
        "exclude": exclude,
        "exclude_prefixes": EXCLUDED_PREFIXES,
        "count": len(requirements),
        "synthetic_count": sum(r["synthetic_id"] for r in requirements),
        "files": files_report,
        "id_prefixes": dict(sorted(prefixes.items(), key=lambda kv: -kv[1])),
        "requirements": requirements,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(requirements)} requirements from {len(files_report)} files "
          f"({out['synthetic_count']} synthetic) -> {args.out}")

    if args.csv_out:
        cp = Path(args.csv_out)
        cp.parent.mkdir(parents=True, exist_ok=True)
        with cp.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "title", "type", "priority", "source_file", "line_start", "line_end",
                        "definition_site", "normative", "synthetic_id"])
            for r in requirements:
                w.writerow([r["id"], r["title"], r["type"], r["priority"], r["source_file"],
                            r["line_range"][0], r["line_range"][1], r["definition_site"],
                            r["normative"], r["synthetic_id"]])
        print(f"Wrote CSV -> {cp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
