"""Audit OpenAPI response-schema quality without claiming endpoint behavior."""

from __future__ import annotations

import argparse
import json
from collections import Counter

from qa.bench import ROOT, check, exit_code, offline_document, write_evidence

PIN = ROOT / "qa" / "contracts" / "schema-quality.json"
METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}


def analyze(document: dict) -> dict:
    findings = []
    operation_ids = []
    operation_count = 0
    for path, path_item in sorted(document.get("paths", {}).items()):
        for method, operation in sorted(path_item.items()):
            if method not in METHODS:
                continue
            operation_count += 1
            identifier = operation.get("operationId")
            if identifier:
                operation_ids.append(identifier)
            responses = operation.get("responses", {})
            success = [(code, response) for code, response in responses.items() if code.isdigit() and 200 <= int(code) < 300]
            if not success:
                findings.append({"method": method.upper(), "path": path, "status": "none", "reason": "no_success_response"})
                continue
            for code, response in success:
                if code == "204":
                    continue
                content = response.get("content", {})
                if not content:
                    findings.append({"method": method.upper(), "path": path, "status": code, "reason": "no_response_content"})
                    continue
                for media, definition in content.items():
                    if not definition.get("schema"):
                        findings.append({"method": method.upper(), "path": path, "status": code, "media": media, "reason": "empty_response_schema"})
    duplicate_ids = sorted(identifier for identifier, count in Counter(operation_ids).items() if count > 1)
    return {
        "schema_version": 1,
        "interpretation": "Static OpenAPI documentation audit; passing drift check is not runtime schema validation",
        "operation_count": operation_count,
        "finding_count": len(findings),
        "counts_by_reason": dict(sorted(Counter(item["reason"] for item in findings).items())),
        "duplicate_operation_ids": duplicate_ids,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Explicitly update the review-required findings pin")
    args = parser.parse_args(argv)
    current = analyze(offline_document())
    if args.write:
        PIN.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {PIN.relative_to(ROOT)}; review all {current['finding_count']} findings and the diff")
        return 0
    if not PIN.exists():
        checks = [check("Schema-quality baseline", None, "Run --write and review the initial pin")]
    else:
        pinned = json.loads(PIN.read_text(encoding="utf-8"))
        current_set = {json.dumps(item, sort_keys=True) for item in current["findings"]}
        pinned_set = {json.dumps(item, sort_keys=True) for item in pinned["findings"]}
        new = [json.loads(item) for item in sorted(current_set - pinned_set)]
        checks = [
            check("New undocumented success responses", not new, f"new={new[:10]}; known={current['finding_count']}"),
            check("Duplicate operation IDs", not current["duplicate_operation_ids"], f"{len(current['duplicate_operation_ids'])} duplicates"),
        ]
    path = write_evidence("schema-quality", checks, {"operations": current["operation_count"], "known_findings": current["counts_by_reason"]})
    for item in checks:
        print(f"{item['status'].upper():7} {item['name']}: {item['detail']}")
    print(f"Evidence: {path.relative_to(ROOT)}")
    return exit_code(checks)


if __name__ == "__main__":
    raise SystemExit(main())
