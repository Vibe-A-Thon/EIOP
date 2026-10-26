#!/usr/bin/env python3
"""Convert pytest-reportlog JSONL files into one JUnit XML (survives killed/hung runs).

Usage: reportlog_to_junit.py --out tests.xml a.jsonl b.jsonl ...  (later files override earlier results for the same nodeid)
Phases: a setup failure is an <error>, a call failure is a <failure>, and a skip is <skipped>.
Collection failures become <error> testcases named '<collection>'. Long reprs are truncated; no env or secrets are captured.
"""
import argparse, json, sys
from pathlib import Path
from xml.sax.saxutils import quoteattr, escape


def split(nodeid):
    path, _, rest = nodeid.partition("::")
    mod = path[:-3].replace("/", ".") if path.endswith(".py") else path.replace("/", ".")
    parts = rest.split("::") if rest else ["<module>"]
    cls = ".".join([mod] + parts[:-1])
    return cls, parts[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("files", nargs="+", type=Path)
    a = ap.parse_args()
    cases, order = {}, []
    for f in a.files:
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            t = r.get("$report_type")
            if t == "CollectReport" and r.get("outcome") == "failed":
                nid = r.get("nodeid") or str(f)
                cases[nid + "::<collection>"] = {"state": "error", "msg": "collection error", "dur": 0.0}
                order.append(nid + "::<collection>")
            if t != "TestReport":
                continue
            nid, when, out = r["nodeid"], r.get("when"), r.get("outcome")
            c = cases.get(nid)
            if c is not None and when == "setup" and c.get("file") != str(f):
                c = None  # a later file re-ran this test: later result wins
                if nid in order:
                    order.remove(nid)
            if c is None:
                c = cases[nid] = {"state": "passed", "msg": "", "dur": 0.0, "file": str(f)}
                order.append(nid)
            c["dur"] += float(r.get("duration") or 0)
            if out == "failed":
                c["state"] = "error" if when != "call" else "failed"
                lr = r.get("longrepr")
                msg = lr.get("reprcrash", {}).get("message") if isinstance(lr, dict) and isinstance(lr.get("reprcrash"), dict) else str(lr)[:300]
                c["msg"] = (msg or "")[:500]
            elif out == "skipped" and c["state"] == "passed":
                c["state"] = "skipped"
    counts = {"passed": 0, "failed": 0, "error": 0, "skipped": 0}
    body = []
    for nid in order:
        c = cases[nid]; counts[c["state"]] += 1
        cls, name = split(nid)
        inner = ""
        if c["state"] == "failed":
            inner = f"<failure message={quoteattr(c['msg'])}>{escape(c['msg'])}</failure>"
        elif c["state"] == "error":
            inner = f"<error message={quoteattr(c['msg'])}>{escape(c['msg'])}</error>"
        elif c["state"] == "skipped":
            inner = "<skipped/>"
        body.append(f'<testcase classname={quoteattr(cls)} name={quoteattr(name)} time="{c["dur"]:.3f}">{inner}</testcase>')
    n = len(order)
    xml = (f'<?xml version="1.0" encoding="utf-8"?>\n<testsuites><testsuite name="pytest-reportlog" tests="{n}" '
           f'failures="{counts["failed"]}" errors="{counts["error"]}" skipped="{counts["skipped"]}">\n' + "\n".join(body) + "\n</testsuite></testsuites>\n")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(xml, encoding="utf-8")
    print(json.dumps({"tests": n, **counts}))


if __name__ == "__main__":
    main()
