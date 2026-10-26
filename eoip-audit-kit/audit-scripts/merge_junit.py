#!/usr/bin/env python3
"""Merge junit files case by case: a later file's result replaces the same classname::name case.

Used to fold an extended/re-run pass into the main run without double-counting re-run tests
(proof policy 1.1: one result per test case per commit; the later, correct-environment run wins).

  python3 merge_junit.py --base test_results/tests.xml --override test_results_extended/tests.xml \
      --out test_results_merged/tests.xml
"""
from __future__ import annotations

import argparse
import copy
import xml.etree.ElementTree as ET
from pathlib import Path


def cases(path: Path) -> dict:
    return {(tc.get("classname"), tc.get("name")): tc for tc in ET.parse(path).getroot().iter("testcase")}


def state(tc) -> str:
    for ch in tc:
        if ch.tag in ("failure", "error"):
            return "failed"
        if ch.tag == "skipped":
            return "skipped"
    return "passed"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--override", type=Path, action="append", required=True, help="repeatable; later wins")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    merged = cases(a.base)
    stats = {}
    for ov in a.override:
        oc = cases(ov)
        stats[str(ov)] = {"overridden": len(set(oc) & set(merged)), "appended": len(set(oc) - set(merged))}
        merged.update(oc)
    root = ET.Element("testsuites")
    suite = ET.SubElement(root, "testsuite", name="merged")
    for tc in merged.values():
        suite.append(copy.deepcopy(tc))
    st = [state(tc) for tc in merged.values()]
    suite.set("tests", str(len(st)))
    suite.set("failures", str(st.count("failed")))
    suite.set("errors", "0")
    suite.set("skipped", str(st.count("skipped")))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(a.out, encoding="utf-8", xml_declaration=True)
    print({"cases": len(st), "passed": st.count("passed"), "failed": st.count("failed"), "skipped": st.count("skipped"), "inputs": stats})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
