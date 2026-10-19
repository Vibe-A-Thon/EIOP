#!/usr/bin/env python3
"""Redact common secrets/PII patterns from a file or stdin."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", re.S)),
    ("aws_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{36,}")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}")),
    ("assignment_secret", re.compile(
        r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    )),
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("email", re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")),
]


def redact(text: str) -> tuple[str, list[dict]]:
    log: list[dict] = []
    out = text
    for name, cre in PATTERNS:
        def _sub(m, _name=name):
            log.append({"pattern": _name, "span": [m.start(), m.end()], "replacement": f"[REDACTED_{_name.upper()}]"})
            return f"[REDACTED_{_name.upper()}]"
        out, n = cre.subn(_sub, out)
        # count already in log
    return out, log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="infile", default="-")
    ap.add_argument("--out", dest="outfile", required=True)
    ap.add_argument("--log", dest="logfile", required=True)
    args = ap.parse_args()

    if args.infile == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.infile).read_text(encoding="utf-8", errors="replace")

    redacted, log = redact(text)
    Path(args.outfile).parent.mkdir(parents=True, exist_ok=True)
    Path(args.logfile).parent.mkdir(parents=True, exist_ok=True)
    Path(args.outfile).write_text(redacted, encoding="utf-8")
    import json
    Path(args.logfile).write_text(
        json.dumps({"count": len(log), "hits": log}, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Redacted {len(log)} hit(s) → {args.outfile}; log → {args.logfile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
