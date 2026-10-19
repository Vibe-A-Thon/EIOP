#!/usr/bin/env python3
"""Parse .md files under --root into requirements_index.json (+ optional CSV)."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REQ_ID_RE = re.compile(r"\b(REQ-[A-Z]+-\d{4})\b")
BLOCK_ID_RE = re.compile(r"^ID:\s*(REQ-[A-Z]+-\d{4})\s*$", re.I | re.M)
HEADING_RE = re.compile(
    r"^#{1,3}\s+(REQ-[A-Z]+-\d{4})\s*[—\-:]\s*(.+)$", re.M
)
FIELD_RE = re.compile(
    r"^\*\*?(Type|Priority|Owner|Severity_Hint|Estimated Effort)\*\*?:\s*(.+)$",
    re.I | re.M,
)


def iter_md(root: Path):
    for p in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in p.parts):
            continue
        if "audit-output" in p.parts or "node_modules" in p.parts:
            continue
        yield p


def extract_from_text(text: str, path: Path) -> list[dict]:
    found: dict[str, dict] = {}

    for m in HEADING_RE.finditer(text):
        rid, title = m.group(1), m.group(2).strip()
        start = m.start()
        # slice until next heading or EOF
        nxt = re.search(r"^#{1,3}\s+", text[m.end() :], re.M)
        end = m.end() + nxt.start() if nxt else len(text)
        body = text[start:end]
        line_start = text.count("\n", 0, start) + 1
        line_end = text.count("\n", 0, end) + 1
        rec = {
            "id": rid,
            "title": title,
            "type": _field(body, "Type") or _guess_type(rid),
            "priority": _field(body, "Priority") or "UNKNOWN",
            "owner": _field(body, "Owner") or "UNKNOWN",
            "acceptance_criteria": _ac(body),
            "related_files": _related(body),
            "line_range": [line_start, line_end],
            "source_file": str(path),
            "raw_text": body.strip()[:4000],
        }
        found[rid] = rec

    for m in BLOCK_ID_RE.finditer(text):
        rid = m.group(1).upper().replace("REQ-FUNC-", "REQ-FUNC-")  # normalize later
        rid = re.match(r"REQ-[A-Z]+-\d{4}", m.group(1), re.I).group(0).upper()
        # Fix type segment casing: REQ-SEC-0002
        parts = rid.split("-")
        rid = f"{parts[0]}-{parts[1]}-{parts[2]}"
        if rid in found:
            continue
        start = m.start()
        nxt = BLOCK_ID_RE.search(text, m.end())
        end = nxt.start() if nxt else min(len(text), start + 2500)
        # also stop at ---
        dash = text.find("\n---", start + 1)
        if dash != -1 and dash < end:
            end = dash
        body = text[start:end]
        title_m = re.search(r"^Title:\s*(.+)$", body, re.M | re.I)
        line_start = text.count("\n", 0, start) + 1
        line_end = text.count("\n", 0, end) + 1
        found[rid] = {
            "id": rid,
            "title": title_m.group(1).strip() if title_m else rid,
            "type": _field(body, "Type") or _guess_type(rid),
            "priority": _field(body, "Priority") or "UNKNOWN",
            "owner": _field(body, "Owner") or "UNKNOWN",
            "acceptance_criteria": _ac(body),
            "related_files": _related(body),
            "line_range": [line_start, line_end],
            "source_file": str(path),
            "raw_text": body.strip()[:4000],
        }

    # Heading without dash: ## REQ-AI-0003 LLM egress...
    for m in re.finditer(r"^#{1,3}\s+(REQ-[A-Z]+-\d{4})\s+(.+)$", text, re.M):
        rid = m.group(1)
        if rid in found:
            continue
        if re.match(r"^[—\-:]", m.group(2)):
            continue
        title = m.group(2).strip()
        start = m.start()
        nxt = re.search(r"^#{1,3}\s+", text[m.end() :], re.M)
        end = m.end() + nxt.start() if nxt else len(text)
        body = text[start:end]
        line_start = text.count("\n", 0, start) + 1
        line_end = text.count("\n", 0, end) + 1
        found[rid] = {
            "id": rid,
            "title": title,
            "type": _field(body, "Type") or _guess_type(rid),
            "priority": _field(body, "Priority") or "UNKNOWN",
            "owner": _field(body, "Owner") or "UNKNOWN",
            "acceptance_criteria": _ac(body),
            "related_files": _related(body),
            "line_range": [line_start, line_end],
            "source_file": str(path),
            "raw_text": body.strip()[:4000],
        }

    return list(found.values())


def _field(body: str, name: str) -> str | None:
    m = re.search(
        rf"^(?:\*\*)?{name}(?:\*\*)?:\s*(.+)$", body, re.M | re.I
    )
    return m.group(1).strip() if m else None


def _guess_type(rid: str) -> str:
    seg = rid.split("-")[1]
    return {
        "FUNC": "Functional",
        "NFR": "Non-Functional",
        "SEC": "Security",
        "COMP": "Compliance",
        "AI": "AI",
        "INFRA": "Infra",
    }.get(seg, "Functional")


def _ac(body: str) -> list[str]:
    lines = []
    in_ac = False
    for line in body.splitlines():
        if re.search(r"acceptance criteria", line, re.I):
            in_ac = True
            rest = re.split(r"acceptance criteria\s*:?\s*", line, flags=re.I)
            if len(rest) > 1 and rest[1].strip():
                lines.append(rest[1].strip())
            continue
        if in_ac:
            if re.match(r"^#{1,3}\s+", line) or re.match(
                r"^(ID|Title|Type|Priority|Security|Estimated):", line, re.I
            ):
                break
            if re.match(r"^---", line):
                break
            s = line.strip().lstrip("-*").strip()
            s = re.sub(r"^\d+\.\s*", "", s)
            if s:
                lines.append(s)
    return lines


def _related(body: str) -> list[str]:
    files = []
    in_rel = False
    for line in body.splitlines():
        if re.search(r"related files", line, re.I):
            in_rel = True
            continue
        if in_rel:
            if not line.strip() or line.strip().startswith("#"):
                if files:
                    break
                continue
            s = line.strip().lstrip("-*").strip()
            if s:
                files.append(s)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--commit", default="")
    ap.add_argument("--csv", dest="csv_out", default="", help="Optional CSV path")
    args = ap.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: --root not a directory: {root}", file=sys.stderr)
        return 2

    requirements = []
    for md in iter_md(root):
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"WARN: skip {md}: {e}", file=sys.stderr)
            continue
        for rec in extract_from_text(text, md.relative_to(root)):
            requirements.append(rec)

    # de-dupe by id (first wins)
    by_id = {}
    for r in requirements:
        by_id.setdefault(r["id"], r)
    requirements = sorted(by_id.values(), key=lambda r: r["id"])

    out = {
        "schema_hint": "requirements_index",
        "commit": args.commit or None,
        "root": str(root),
        "count": len(requirements),
        "requirements": requirements,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(requirements)} requirements → {args.out}")

    if args.csv_out:
        csv_path = Path(args.csv_out)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(
                f,
                fieldnames=[
                    "id",
                    "title",
                    "type",
                    "priority",
                    "owner",
                    "source_file",
                    "line_range",
                ],
            )
            w.writeheader()
            for r in requirements:
                w.writerow(
                    {
                        "id": r["id"],
                        "title": r["title"],
                        "type": r["type"],
                        "priority": r["priority"],
                        "owner": r["owner"],
                        "source_file": r["source_file"],
                        "line_range": f"{r['line_range'][0]}-{r['line_range'][1]}",
                    }
                )
        print(f"Wrote CSV → {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
