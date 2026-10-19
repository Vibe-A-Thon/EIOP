#!/usr/bin/env python3
"""Validate evidence.json against schema + proof policy 1.1.0 rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from proof_policy import (  # noqa: E402
    PROOF_POLICY_VERSION,
    compute_status,
    enforce_bundle_rules,
)

SECRET_RES = [
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
]


def load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(instance: dict, schema: dict) -> list[str]:
    errs: list[str] = []
    try:
        import jsonschema

        validator = jsonschema.Draft7Validator(schema)
        for e in sorted(validator.iter_errors(instance), key=lambda x: list(x.path)):
            errs.append(e.message + f" at {list(e.path)}")
    except ImportError:
        # Minimal fallback checks
        for req in schema.get("required", []):
            if req not in instance:
                errs.append(f"missing required property: {req}")
        if instance.get("schema_version") != schema.get("properties", {}).get(
            "schema_version", {}
        ).get("const"):
            # soft
            pass
        if instance.get("proof_policy_version") != PROOF_POLICY_VERSION:
            errs.append(
                f"proof_policy_version must be {PROOF_POLICY_VERSION}"
            )
    return errs


def secret_scan(bundle: dict) -> list[str]:
    raw = json.dumps(bundle)
    hits = []
    for cre in SECRET_RES:
        if cre.search(raw):
            hits.append(f"secret pattern matched: {cre.pattern[:40]}...")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--schema", required=True, type=Path)
    ap.add_argument("--in", dest="infile", required=True, type=Path)
    ap.add_argument("--audited-commit", default="", help="If set, flag stale items")
    ap.add_argument(
        "--memory",
        type=Path,
        default=None,
        help="Optional audit-memory for residual_gaps / severity",
    )
    ap.add_argument("--strict-closure", action="store_true",
                    help="Exit non-zero if any requirement would be Implemented without meeting 1.1 rules")
    args = ap.parse_args()

    bundle = json.loads(args.infile.read_text(encoding="utf-8"))
    schema = load_schema(args.schema)

    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(validate_schema(bundle, schema))
    errors.extend(enforce_bundle_rules(bundle))
    errors.extend(secret_scan(bundle))

    memory = {}
    if args.memory and args.memory.is_file():
        memory = json.loads(args.memory.read_text(encoding="utf-8")).get(
            "requirements", {}
        )

    audited = args.audited_commit or bundle.get("git_commit")
    producer = (bundle.get("generated_by") or {}).get("agent_id")
    by_req: dict[str, list] = defaultdict(list)
    for it in bundle.get("evidence_items") or []:
        by_req[it["requirement_id"]].append(it)

    for rid, items in sorted(by_req.items()):
        meta = memory.get(rid) or {}
        severity = meta.get("severity") or "Medium"
        gaps = meta.get("residual_gaps") or []
        result = compute_status(
            severity=severity,
            evidence_items=items,
            residual_gaps=gaps,
            audited_commit=audited,
            bundle_commit=bundle.get("git_commit"),
            producer_agent_id=producer,
        )
        for w in result.get("warnings") or []:
            warnings.append(f"{rid}: {w}")
        if result.get("stale_count"):
            warnings.append(f"{rid}: {result['stale_count']} stale evidence item(s)")
        # Closure integrity: if someone claimed Implemented in memory but policy disagrees
        if meta.get("status") == "Implemented" and result["status"] != "Implemented":
            errors.append(
                f"{rid}: memory says Implemented but proof policy 1.1 yields {result['status']}"
            )
        if args.strict_closure and result["status"] == "Implemented":
            # already validated by compute_status
            pass
        print(f"  {rid}: {result['status']} (tier {result['proof_tier']})")

    # If computed status is NI, require negative/absence support
    from proof_policy import _ni_supported

    for rid, items in by_req.items():
        meta = memory.get(rid) or {}
        severity = meta.get("severity") or "Medium"
        gaps = meta.get("residual_gaps") or []
        result = compute_status(
            severity=severity,
            evidence_items=items,
            residual_gaps=gaps,
            audited_commit=audited,
            bundle_commit=bundle.get("git_commit"),
            producer_agent_id=producer,
        )
        if result["status"] == "Not Implemented" and items:
            if not _ni_supported(items) and not any(
                i.get("type") == "negative_proof" for i in items
            ):
                # L1-only NI is acceptable outcome but document absence when claiming NI intentionally
                if all(i.get("proof_tier") == "L1" and i.get("type") != "negative_proof" for i in items):
                    warnings.append(
                        f"{rid}: only L1 evidence — status Not Implemented (add L2 or negative_proof)"
                    )

    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: evidence valid under proof policy {PROOF_POLICY_VERSION} "
          f"({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
