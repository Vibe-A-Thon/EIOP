#!/usr/bin/env python3
"""Map requirements to code/tests/infra via search; write traceability_matrix.csv."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "audit-output", ".venv", "venv", "__pycache__"}


def rg_or_grep(pattern: str, root: Path) -> list[str]:
    hits: list[str] = []
    if shutil.which("rg"):
        try:
            r = subprocess.run(
                [
                    "rg",
                    "-l",
                    "--hidden",
                    "-g",
                    "!/.git/",
                    "-g",
                    "!node_modules/",
                    "-g",
                    "!audit-output/",
                    pattern,
                    str(root),
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            hits = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
        except (subprocess.SubprocessError, OSError) as e:
            print(f"WARN: rg failed: {e}", file=sys.stderr)
    else:
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if any(s in p.parts for s in SKIP_DIRS):
                continue
            if p.suffix.lower() not in {
                ".py",
                ".js",
                ".ts",
                ".tsx",
                ".go",
                ".java",
                ".md",
                ".yml",
                ".yaml",
                ".sh",
                ".json",
                ".toml",
            }:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if re.search(pattern, text):
                hits.append(str(p))
    # relativize
    out = []
    for h in hits:
        try:
            out.append(str(Path(h).resolve().relative_to(root.resolve())))
        except ValueError:
            out.append(h)
    return sorted(set(out))


def classify(paths: list[str]) -> tuple[list[str], list[str], list[str]]:
    code, tests, infra = [], [], []
    for p in paths:
        pl = p.replace("\\", "/").lower()
        if any(x in pl for x in ("test", "spec", "e2e")):
            tests.append(p)
        elif any(
            x in pl
            for x in (
                "deploy/",
                "k8s/",
                "helm/",
                "terraform",
                "dockerfile",
                ".github/",
                "infra/",
            )
        ):
            infra.append(p)
        elif pl.endswith(".md"):
            continue
        else:
            code.append(p)
    return code, tests, infra


def confidence(code, tests, infra, id_hits: bool) -> float:
    score = 0.0
    if id_hits:
        score += 0.45
    if code:
        score += 0.25
    if tests:
        score += 0.2
    if infra:
        score += 0.1
    return round(min(score, 1.0), 2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", required=True, type=Path)
    ap.add_argument("--requirements", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--commit", default="")
    args = ap.parse_args()

    root = args.repo_root.resolve()
    data = json.loads(args.requirements.read_text(encoding="utf-8"))
    reqs = data.get("requirements") or data
    if isinstance(reqs, dict):
        reqs = list(reqs.values())

    rows = []
    for req in reqs:
        rid = req["id"]
        title = req.get("title") or ""
        tokens = [rid]
        # significant title words
        for w in re.findall(r"[A-Za-z]{4,}", title):
            if w.lower() not in {"with", "from", "that", "this", "have", "must"}:
                tokens.append(w)

        id_paths = rg_or_grep(re.escape(rid), root)
        title_paths = []
        if title:
            # search first 2 significant words as phrase if possible
            words = [w for w in re.findall(r"[A-Za-z]{5,}", title)][:2]
            if words:
                title_paths = rg_or_grep(r"|".join(re.escape(w) for w in words), root)

        # related_files hints
        hint_paths = []
        for rel in req.get("related_files") or []:
            candidate = root / rel
            if candidate.exists():
                if candidate.is_dir():
                    hint_paths.append(rel.rstrip("/") + "/")
                else:
                    hint_paths.append(rel)

        all_paths = sorted(set(id_paths + title_paths + hint_paths))
        code, tests, infra = classify(all_paths)
        conf = confidence(code, tests, infra, bool(id_paths))
        etype = "mixed"
        if tests and not code:
            etype = "test"
        elif code and not tests:
            etype = "code"
        elif infra:
            etype = "infra"
        rows.append(
            {
                "requirement_id": rid,
                "code_paths": ";".join(code),
                "test_paths": ";".join(tests),
                "infra_paths": ";".join(infra),
                "evidence_type": etype,
                "confidence_score": conf,
                "git_commit": args.commit or "",
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "requirement_id",
                "code_paths",
                "test_paths",
                "infra_paths",
                "evidence_type",
                "confidence_score",
                "git_commit",
            ],
        )
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
