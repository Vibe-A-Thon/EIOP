"""Validator for competitive research records per CRA-042 and CRA-042.A."""
from __future__ import annotations
import argparse, csv, sys
from datetime import date, datetime, timedelta
from pathlib import Path
import yaml

DEPENDENCY_TOOLS = {
    "rdflib", "pyshacl", "owl api", "elk", "jena", "fuseki",
    "ontop", "morph-kgc", "deeponto", "spacy", "tesseract"
}

def validate_record(data: dict, ref_date: date | None = None) -> list[str]:
    errors = []
    today = ref_date or date.today()
    
    cid = data.get("id")
    if not cid:
        return ["Missing research record 'id'"]

    # 1. reviewed_at present
    reviewed_at_str = data.get("reviewed_at")
    if not reviewed_at_str:
        errors.append(f"[{cid}] missing required 'reviewed_at' date")
    else:
        try:
            rev_date = date.fromisoformat(str(reviewed_at_str)[:10])
            if (today - rev_date) > timedelta(days=183):
                errors.append(f"[{cid}] STALE: reviewed_at ({rev_date}) is older than 183 days")
        except Exception:
            errors.append(f"[{cid}] invalid date format for reviewed_at: {reviewed_at_str}")

    # 2. Dependency tool must have pinned_artifact
    tool_name = str(data.get("tool_family", "")).lower()
    pinned = data.get("pinned_artifact")
    is_dep = any(dep in tool_name for dep in DEPENDENCY_TOOLS)
    if is_dep and (not pinned or pinned == "unpinned" or pinned == "ND"):
        errors.append(f"[{cid}] dependency tool '{data.get('tool_family')}' lacks pinned_artifact")

    # 3. Dimensions D01..D22 scoring
    scores = data.get("scores", {})
    if not scores:
        errors.append(f"[{cid}] missing scores dictionary for dimensions")
    else:
        for dim, sinfo in scores.items():
            if isinstance(sinfo, dict):
                score_val = sinfo.get("score")
                rationale = sinfo.get("rationale")
            else:
                score_val = sinfo
                rationale = data.get("rationale_reference", "")

            if score_val is None or str(score_val).strip() == "":
                errors.append(f"[{cid}] blank score for dimension {dim}")
            elif str(score_val).upper() == "ND":
                pass
            else:
                try:
                    # must be an integer 1..5, not a float (e.g. 3.5 rejected)
                    if isinstance(score_val, float) and not score_val.is_integer():
                        errors.append(f"[{cid}] dimension {dim} score must be integer 1..5 or ND, got float {score_val}")
                    else:
                        int_val = int(str(score_val))
                        if not (1 <= int_val <= 5):
                            errors.append(f"[{cid}] dimension {dim} score {int_val} outside 1..5 range")
                except ValueError:
                    errors.append(f"[{cid}] dimension {dim} invalid score format: {score_val}")

    return errors

def validate_all(dir_path: Path, ref_date: date | None = None) -> list[str]:
    all_errors = []
    files = sorted(dir_path.glob("C*.yaml"))
    if not files:
        return [f"No competitive research records found in {dir_path}"]
    for f in files:
        try:
            content = yaml.safe_load(f.read_text(encoding="utf-8"))
            errs = validate_record(content, ref_date=ref_date)
            all_errors.extend(errs)
        except Exception as e:
            all_errors.append(f"Error parsing {f}: {e}")
    return all_errors

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="research/competitive")
    ap.add_argument("--ref-date", default="2026-10-18")
    a = ap.parse_args()

    ref_date = date.fromisoformat(a.ref_date) if a.ref_date else None
    errors = validate_all(Path(a.dir), ref_date=ref_date)
    if errors:
        print(f"FAILED: {len(errors)} validation errors:")
        for e in errors:
            print("  -", e)
        return 1
    else:
        print(f"PASSED: All competitive research records in {a.dir} valid")
        return 0

if __name__ == "__main__":
    sys.exit(main())
