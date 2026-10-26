"""Validate generated snapshot schemas, status policy, source text and artifact links."""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import jsonschema

from redact_sensitive import redact
from strict_audit_policy import assess


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out, root = args.out.resolve(), args.root.resolve()
    kit = Path(__file__).resolve().parents[1]
    evidence = read(out / "evidence/evidence.json")
    memory = read(out / "audit-memory.json")
    index = read(out / "requirements_index.json")
    errors = []
    for name, data in (("evidence", evidence), ("audit-memory", memory)):
        validator = jsonschema.Draft7Validator(read(kit / "schemas" / f"{name}.schema.json"),
                                              format_checker=jsonschema.FormatChecker())
        errors.extend(f"{name}: {error.message}" for error in validator.iter_errors(data))
        _, hits = redact(json.dumps(data))
        if hits:
            errors.append(f"{name}: {len(hits)} secret/PII heuristic matches; local review required")
    by_req = defaultdict(list)
    ids = set()
    for item in evidence["evidence_items"]:
        if item["evidence_id"] in ids:
            errors.append("Duplicate evidence ID: " + item["evidence_id"])
        ids.add(item["evidence_id"])
        by_req[item["requirement_id"]].append(item)
        for link in item.get("links", []):
            if link["kind"] == "artifact" and not (out / link["url"]).is_file():
                errors.append("Missing artifact: " + link["url"])
    if set(memory["requirements"]) != {r["id"] for r in index["requirements"]}:
        errors.append("Requirement index and memory IDs differ")
    source_cache = {}
    for req in index["requirements"]:
        source = req["source_file"]
        if source not in source_cache:
            source_cache[source] = (root / source).read_text(encoding="utf-8-sig").splitlines()
        start, end = req["line_range"]
        original = "\n".join(source_cache[source][start - 1:end])
        if original != req["raw_text"]:
            errors.append("Source text mismatch: " + req["id"])
        current = memory["requirements"][req["id"]]
        assessment = assess(by_req[req["id"]], commit=memory["audited_commit"],
                            bundle_commit=evidence["git_commit"], severity=current["severity"],
                            gaps=current["residual_gaps"], producer=evidence["generated_by"]["agent_id"])
        if current["status"] != assessment["status"] or current["proof_tier_achieved"] != assessment["proof_tier"]:
            errors.append("Status mismatch: " + req["id"])
    result = {"status": "passed" if not errors else "failed", "errors": errors,
              "requirements_checked": len(index["requirements"]), "evidence_items_checked": len(ids),
              "checks": ["JSON schemas with formats", "secret/PII heuristics", "unique evidence IDs",
                         "local artifact existence", "all source text verbatim", "strict status and tier parity"]}
    destination = out / "evidence/bundle-validation.json"
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
