"""Independent offline verification engine for ASPEII evidence bundles (plan §7, §8)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class VerifierResult:
    schema_version: str
    run_id: str
    verified_clauses: int
    total_clauses: int
    verdict: str  # PASS or FAIL
    verified_at: str
    failures: List[Dict[str, Any]]
    profile: str
    cases_executed: int


class ASPEIIVerifier:
    """Verifies evidence bundles independently of the runtime system."""

    def __init__(self, expected_total_clauses: int = 216) -> None:
        self.expected_total_clauses = expected_total_clauses

    def verify_bundle(self, bundle_dir: Path | str) -> VerifierResult:
        p = Path(bundle_dir)
        if not p.exists() or not p.is_dir():
            raise FileNotFoundError(f"Bundle directory does not exist: {p}")

        manifest_file = p / "manifest.json"
        cases_file = p / "cases.jsonl"

        if not manifest_file.exists():
            raise FileNotFoundError(f"manifest.json missing in bundle: {p}")
        if not cases_file.exists():
            raise FileNotFoundError(f"cases.jsonl missing in bundle: {p}")

        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        run_id = manifest.get("run_id", p.name)
        profile = manifest.get("profile", "local-sqlite-windows")

        verified_clauses_set: Set[str] = set()
        failures: List[Dict[str, Any]] = []
        cases_count = 0

        with cases_file.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                cases_count += 1
                try:
                    case = json.loads(line)
                except Exception as exc:
                    failures.append({"line": idx, "error": f"JSON parse error: {exc}"})
                    continue

                case_id = case.get("case_id", f"case-{idx}")
                status = case.get("status", "UNKNOWN")
                clause_ids = case.get("clause_ids", [])

                if status != "PASSED":
                    failures.append({
                        "case_id": case_id,
                        "status": status,
                        "reason": case.get("error") or f"Case ended with status {status} (must be PASSED)",
                    })
                else:
                    for cid in clause_ids:
                        verified_clauses_set.add(cid)

        # Verdict evaluation
        verdict = "PASS" if len(failures) == 0 and len(verified_clauses_set) >= self.expected_total_clauses else "FAIL"

        result = VerifierResult(
            schema_version="aspeii-verifier-result/1",
            run_id=run_id,
            verified_clauses=len(verified_clauses_set),
            total_clauses=self.expected_total_clauses,
            verdict=verdict,
            verified_at=datetime.now(timezone.utc).isoformat(),
            failures=failures,
            profile=profile,
            cases_executed=cases_count,
        )

        # Write verifier-result.json to bundle
        out_file = p / "verifier-result.json"
        out_file.write_text(
            json.dumps(
                {
                    "schema_version": result.schema_version,
                    "run_id": result.run_id,
                    "verified_clauses": result.verified_clauses,
                    "total_clauses": result.total_clauses,
                    "verdict": result.verdict,
                    "verified_at": result.verified_at,
                    "failures": result.failures,
                    "profile": result.profile,
                    "cases_executed": result.cases_executed,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        return result
