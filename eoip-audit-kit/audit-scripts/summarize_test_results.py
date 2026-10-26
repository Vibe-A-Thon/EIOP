"""Collect finished JUnit runs and retain redacted failure details for handoff."""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from redact_sensitive import redact


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    combined = ET.Element("testsuites")
    failures = []
    runs = []
    for path in sorted((out / "evidence").glob("*/tests.xml")):
        # Redact XML text/attributes through the structured tree, never by
        # replacing serialized XML (which can invalidate entities/markup).
        tree = ET.parse(path)
        hits = 0
        for element in tree.iter():
            if element.text:
                element.text, log = redact(element.text)
                hits += len(log)
            for key, value in list(element.attrib.items()):
                element.attrib[key], log = redact(value)
                hits += len(log)
        tree.write(path, encoding="utf-8", xml_declaration=True)
        (path.with_name("xml-redaction.json")).write_text(json.dumps({"redaction_hits": hits}), encoding="utf-8")
        suites = list(tree.getroot()) if tree.getroot().tag == "testsuites" else [tree.getroot()]
        for suite in suites:
            combined.append(suite)
        tests = list(tree.iter("testcase"))
        run = {"artifact": path.relative_to(out).as_posix(), "cases": len(tests), "failures": 0, "errors": 0, "skipped": 0}
        for case in tests:
            for tag, field in (("failure", "failures"), ("error", "errors"), ("skipped", "skipped")):
                problem = case.find(tag)
                if problem is None:
                    continue
                run[field] += 1
                if tag != "skipped":
                    failures.append({"case": case.get("classname", "") + "::" + case.get("name", ""),
                                     "type": tag, "artifact": run["artifact"],
                                     "detail": (problem.text or problem.get("message", "")).strip()})
        run["passed"] = run["cases"] - run["failures"] - run["errors"] - run["skipped"]
        runs.append(run)
    ET.ElementTree(combined).write(out / "evidence/tests.xml", encoding="utf-8", xml_declaration=True)
    (out / "evidence/test_results/junit-summary.json").write_text(json.dumps({"runs": runs, "failures": failures}, indent=2), encoding="utf-8")
    lines = ["# Executed Test Failures", "", "These are retained local observations, not inferred failures from source names.",
             "Repeated runs can contain the same case; do not add totals across overlapping runs as unique coverage.", ""]
    for failure in failures:
        lines += ["## " + failure["case"], "", f"Type: {failure['type']}; artifact: `{failure['artifact']}`.",
                  "", "```text", "\n".join(failure["detail"].splitlines()[-30:]), "```", "",
                  "Remediation: reproduce this exact case with isolated data, identify the assertion/fixture/contract mismatch, fix the responsible boundary, and rerun adjacent regression and integration tests. Do not weaken the assertion merely to obtain green output.", ""]
    (out / "test_failures.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"runs": runs, "retained_failures": len(failures)}))


if __name__ == "__main__":
    main()
