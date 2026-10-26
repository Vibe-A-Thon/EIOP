"""Produce small, structured scanner summaries without copying sensitive snippets."""

import argparse
import json
from collections import Counter
from pathlib import Path


def payload(path):
    text = path.read_text(encoding="utf-8")
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "[{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
            if isinstance(value, (dict, list)):
                return value
        except json.JSONDecodeError:
            pass
    raise ValueError(f"No JSON payload in {path.name}; review redacted output")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    out = args.out
    results = {}
    for name in ("security-sast", "lint", "dependency-advisories", "web-advisories", "ci-public-query"):
        path = out / "evidence" / name / "output.txt"
        try:
            data = payload(path)
            if name == "security-sast":
                findings = data.get("results", [])
                results[name] = {"severity_counts": dict(Counter(f["issue_severity"] for f in findings)),
                                 "findings": [{k: f.get(k) for k in ("filename", "line_number", "test_id", "issue_severity", "issue_confidence", "issue_text")}
                                              for f in findings], "scanner_errors": data.get("errors", [])}
            elif name == "lint":
                results[name] = {"count": len(data), "codes": dict(Counter(f["code"] for f in data)),
                                 "files": len({f["filename"] for f in data})}
            elif name == "dependency-advisories":
                dependencies = data.get("dependencies", [])
                affected = [d for d in dependencies if d.get("vulns")]
                results[name] = {"scope": "Installed audit Python environment, not release lock or deployed image",
                                 "affected_packages": len(affected), "advisories": sum(len(d["vulns"]) for d in affected),
                                 "packages": [{"name": d["name"], "version": d["version"],
                                               "advisories": [{k: v.get(k) for k in ("id", "aliases", "fix_versions")} for v in d["vulns"]]}
                                              for d in affected]}
            elif name == "web-advisories":
                results[name] = {"scope": "apps/web package-lock.json including development dependencies",
                                 "metadata": data.get("metadata"), "vulnerabilities": data.get("vulnerabilities", {}),
                                 "error": data.get("error")}
            else:
                results[name] = data
        except (OSError, ValueError, TypeError, KeyError) as exc:
            results[name] = {"status": "unparsed", "reason": str(exc)}
    (out / "vuln_report.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: {field: value for field, value in v.items() if field not in {"findings", "packages", "vulnerabilities", "runs"}}
                      for k, v in results.items()}, indent=2))


if __name__ == "__main__":
    main()
