"""Inventory dedicated QA API probes against the pinned OpenAPI operation surface."""

from __future__ import annotations

import argparse
import json

from qa.bench import BASELINE, ROOT, check, exit_code, write_evidence
from qa.postman.build_collection import collection as read_collection
from qa.postman.build_workflow import collection as workflow_collection

PIN = ROOT / "qa" / "contracts" / "probe-coverage.json"


def _items(collection: dict) -> list[dict]:
    pending = list(collection["item"])
    found = []
    while pending:
        item = pending.pop()
        if "request" in item:
            found.append(item)
        else:
            pending.extend(item.get("item", []))
    return found


def probe_operations() -> set[tuple[str, str]]:
    result = set()
    for collection in (read_collection(), workflow_collection()):
        for item in _items(collection):
            request = item["request"]
            path = request["url"]["raw"].removeprefix("{{baseUrl}}")
            path = path.replace("{{qaSourceId}}", "{source_id}")
            result.add((request["method"], path))
    return result


def analyze(surface: dict, probes: set[tuple[str, str]]) -> dict:
    operations = {(item["method"], item["path"]) for item in surface["operations"]}
    covered = sorted(operations & probes)
    unprobed = sorted(operations - probes)
    negative = sorted(probes - operations)
    return {
        "schema_version": 1,
        "interpretation": "Dedicated bench request breadth only; not functional correctness or app-wide test coverage",
        "openapi_operations": len(operations),
        "qa_probed_operations": len(covered),
        "unprobed_operations": len(unprobed),
        "negative_or_undocumented_probes": [{"method": method, "path": path} for method, path in negative],
        "probed": [{"method": method, "path": path} for method, path in covered],
        "unprobed": [{"method": method, "path": path} for method, path in unprobed],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Explicitly update the review-required route-probe inventory")
    args = parser.parse_args(argv)
    if not BASELINE.exists():
        print("OpenAPI operation baseline missing; run python -m qa.bench baseline --write")
        return 2
    current = analyze(json.loads(BASELINE.read_text(encoding="utf-8")), probe_operations())
    if args.write:
        PIN.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {PIN.relative_to(ROOT)}: {current['qa_probed_operations']}/{current['openapi_operations']} operations have dedicated QA probes")
        return 0
    if not PIN.exists():
        checks = [check("Probe inventory", None, "Run --write and review the initial inventory")]
    else:
        pinned = json.loads(PIN.read_text(encoding="utf-8"))
        checks = [
            check("Probe inventory drift", pinned == current, f"{current['qa_probed_operations']}/{current['openapi_operations']} operations probed; {current['unprobed_operations']} unprobed"),
            check("Known non-schema probes", all(item["path"] in {"/api/v1/qa-nonexistent-route", "/openapi.json"} for item in current["negative_or_undocumented_probes"]), f"{len(current['negative_or_undocumented_probes'])} intentional framework/negative probes"),
        ]
    output = write_evidence("probe-coverage", checks, {"qa_probed_operations": current["qa_probed_operations"], "unprobed_operations": current["unprobed_operations"]})
    for item in checks:
        print(f"{item['status'].upper():7} {item['name']}: {item['detail']}")
    print(f"Evidence: {output.relative_to(ROOT)}")
    return exit_code(checks)


if __name__ == "__main__":
    raise SystemExit(main())
