#!/usr/bin/env python3
"""Map requirements to code / tests / infra with a single-pass id index.

For every source file (code, tests, infra; docs excluded) the script records which requirement ids
appear and on which lines. Optional inputs add the repo's own requirement->test map and its
claimed code paths (registry). Output: traceability_matrix.csv (+ optional JSON with line anchors).

Confidence (0-1) is about *traceability*, not completion: an id in code is L1 at best.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{1,5}[a-z]?\b")
SKIP_DIRS = {".git", "node_modules", "audit-output", ".venv", "venv", "__pycache__", ".tmp",
             ".audit-scratch", ".eoip-data", "dist", "build", ".mypy_cache", ".pytest_cache"}
CODE_EXT = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".go", ".java", ".rs", ".cs", ".sh", ".ps1", ".sql"}
INFRA_EXT = {".yml", ".yaml", ".toml", ".tf", ".hcl", ".dockerfile"}
MAX_BYTES = 2_000_000


def classify(rel: str) -> str | None:
    low = rel.lower()
    name = os.path.basename(low)
    ext = os.path.splitext(name)[1]
    if name.startswith(("dockerfile", "containerfile")):
        return "infra"
    parts = low.split("/")
    if ext in CODE_EXT:
        if "tests" in parts or "test" in parts or name.startswith("test_") or ".test." in name or ".spec." in name:
            return "test"
        return "code"
    if ext in INFRA_EXT and any(p in parts for p in (".github", "deploy", "helm", "k8s", "infra", "terraform", "config")):
        return "infra"
    return None


def build_index(root: Path, wanted: set[str]) -> dict[str, dict[str, list[tuple[str, int]]]]:
    idx: dict[str, dict[str, list[tuple[str, int]]]] = defaultdict(lambda: defaultdict(list))
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            full = Path(dirpath) / fn
            rel = str(full.relative_to(root)).replace("\\", "/")
            kind = classify(rel)
            if not kind:
                continue
            try:
                if full.stat().st_size > MAX_BYTES:
                    continue
                text = full.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for ln, line in enumerate(text.splitlines(), 1):
                for rid in set(ID_RE.findall(line)):
                    if rid in wanted and len(idx[rid][kind]) < 200:
                        idx[rid][kind].append((rel, ln))
    return idx


def files_of(refs: list[tuple[str, int]]) -> list[str]:
    seen: dict[str, None] = {}
    for f, _ in refs:
        seen.setdefault(f, None)
    return list(seen)


def anchors(refs: list[tuple[str, int]], n: int = 3) -> list[str]:
    out, seen = [], set()
    for f, ln in refs:
        if f in seen:
            continue
        seen.add(f)
        out.append(f"{f}:{ln}")
        if len(out) >= n:
            break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-root", required=True, type=Path)
    ap.add_argument("--requirements", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--json-out", type=Path, default=None, help="Also write per-requirement refs with line anchors")
    ap.add_argument("--commit", default="")
    ap.add_argument("--test-map", type=Path, default=None, help="Repo JSON {req_id: [pytest nodeids]}")
    ap.add_argument("--claims", type=Path, default=None,
                    help="Repo registry JSON list with id/code_paths/test_files (claims, low weight)")
    args = ap.parse_args()

    root = args.repo_root.resolve()
    data = json.loads(args.requirements.read_text(encoding="utf-8"))
    reqs = data.get("requirements") or data
    if isinstance(reqs, dict):
        reqs = list(reqs.values())
    wanted = {r["id"] for r in reqs}

    idx = build_index(root, wanted)
    test_map = json.loads(args.test_map.read_text(encoding="utf-8")) if args.test_map and args.test_map.is_file() else {}
    claims: dict[str, dict] = {}
    if args.claims and args.claims.is_file():
        raw = json.loads(args.claims.read_text(encoding="utf-8"))
        for c in raw if isinstance(raw, list) else raw.values():
            if isinstance(c, dict) and c.get("id") in wanted:
                claims[c["id"]] = c

    rows, detail = [], {}
    for req in reqs:
        rid = req["id"]
        refs = idx.get(rid, {})
        code, tests, infra = refs.get("code", []), refs.get("test", []), refs.get("infra", [])
        mapped_tests = sorted({n.split("::")[0] for n in test_map.get(rid, []) or []})
        claim = claims.get(rid, {})
        claimed_code = [p for p in (claim.get("code_paths") or []) if isinstance(p, str)]
        claimed_tests = [p for p in (claim.get("test_files") or []) if isinstance(p, str)]
        claimed_existing = [p for p in claimed_code + claimed_tests if (root / p.split("::")[0].split("#")[0]).exists()]
        conf = 0.0
        conf += 0.4 if code else 0.0
        conf += 0.25 if tests else 0.0
        conf += 0.15 if mapped_tests else 0.0
        conf += 0.1 if infra else 0.0
        conf += 0.1 if claimed_existing and not code else 0.0
        etype = "+".join(k for k, v in (("code", code), ("test", tests or mapped_tests), ("infra", infra)) if v) or (
            "claimed_only" if claimed_existing else "none")
        rows.append({
            "requirement_id": rid,
            "source": f"{req.get('source_file')}:{req.get('line_range', [0])[0]}",
            "code_paths": ";".join(files_of(code)[:15]),
            "test_paths": ";".join(sorted(set(files_of(tests)[:15]) | set(mapped_tests[:15]))),
            "infra_paths": ";".join(files_of(infra)[:10]),
            "code_anchors": ";".join(anchors(code)),
            "claimed_paths": ";".join(claimed_existing[:10]),
            "evidence_type": etype,
            "confidence_score": round(min(conf, 1.0), 2),
            "git_commit": args.commit,
        })
        detail[rid] = {"code": anchors(code, 10), "tests": anchors(tests, 10), "infra": anchors(infra, 5),
                       "test_map_nodeids": (test_map.get(rid) or [])[:25], "claimed_existing": claimed_existing[:10]}

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["requirement_id"])
        w.writeheader()
        w.writerows(rows)
    if args.json_out:
        args.json_out.write_text(json.dumps(detail, indent=1) + "\n", encoding="utf-8")
    by_type: dict[str, int] = defaultdict(int)
    for r in rows:
        by_type[r["evidence_type"]] += 1
    print(f"Wrote {len(rows)} rows -> {args.out}; evidence_type counts: {dict(by_type)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
