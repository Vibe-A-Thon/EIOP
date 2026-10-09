"""Reproducible documentation inventory and conservative evidence triage.

Reading every byte is not semantic review. Identifier occurrences are discovery
leads, not passing acceptance evidence, and never promote a requirement to Done.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree

from eoip.jobs import write_json

ID_RE = re.compile(r"\b(?:MVP-FR|FR|NFR|GAP|G2|REQ)(?:-[A-Z0-9]+)*-\d{3}\b")
NORMATIVE_RE = re.compile(r"\b(?:must|shall|required|acceptance criteria)\b", re.IGNORECASE)
GENERATED_ROOT = Path("EOIP-engg-doc-pkg/audits/generated")
EXCLUDED_PARTS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
    ".ruff_cache", "test-results", "dist", "build", "state", "raw", "dlq",
    "volumes", ".cache", "model-cache", "secrets", "secrets.example",
}
EVIDENCE_ROOTS = {"packages", "apps", "scripts", "tests", "deploy", ".github"}
EVIDENCE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".yml", ".yaml", ".toml", ".ps1"}
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024


def recorded_runtime_progress(root: Path) -> dict:
    """Report recorded outcomes without promoting requirements or certifying CI."""
    receipts = []
    for name in (
        "enterprise-stable-final-junit.xml",
        "enterprise-search-focused-junit.xml",
        "enterprise-final-source-junit.xml",
        "enterprise-whatif-fix-junit.xml",
        "enterprise-whatif-source-junit.xml",
        "enterprise-code-ingestion-focused-junit.xml",
        "enterprise-code-ingestion-final-junit.xml",
    ):
        path = root / "test-results" / name
        if not path.is_file():
            receipts.append({"path": path.relative_to(root).as_posix(), "status": "UNVERIFIED"})
            continue
        content = path.read_bytes()
        cases = list(ElementTree.fromstring(content).iter("testcase"))
        failed = sum(case.find("failure") is not None for case in cases)
        errors = sum(case.find("error") is not None for case in cases)
        skipped = sum(case.find("skipped") is not None for case in cases)
        receipts.append({
            "path": path.relative_to(root).as_posix(),
            "status": "RECORDED_FAILURE" if failed or errors else "RECORDED_PASS",
            "sha256": hashlib.sha256(content).hexdigest(),
            "passed": len(cases) - failed - errors - skipped,
            "failed": failed, "errors": errors, "skipped": skipped,
        })
    pack_path = root / "demo" / "demodata" / "enterprise" / "scenario-pack.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8")) if pack_path.is_file() else None
    return {
        "scope": "Recorded local JUnit outcomes and canonical seed inventory, not live graph totals.",
        "limitations": [
            "JUnit alone does not record the process exit code or certify remote CI.",
            "Absent receipts are UNVERIFIED; no running test is treated as passing.",
            "Seed inventory is not a product-requirement completion percentage.",
        ],
        "seed": {
            "version": pack["version"], "scenarios": len(pack["scenarios"]),
            "entities": len(pack["vertices"]), "relationships": len(pack["edges"]),
        } if pack else {"status": "UNVERIFIED"},
        "receipts": receipts,
    }


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, encoding="utf-8",
    ).stdout


def _names(root: Path) -> list[str]:
    if Path(_git(root, "rev-parse", "--show-toplevel").strip()).resolve() != root:
        raise ValueError("project root must be the Git repository root")
    return sorted(set(_git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split("\0")) - {""})


def _exclusion(path: Path) -> str | None:
    if any(part.casefold() in EXCLUDED_PARTS for part in path.parts):
        return "secret, Git internal, dependency or generated runtime directory"
    if path.is_relative_to(GENERATED_ROOT) and path.name in {
        "current-gap-report.md", "test-report.md", "completion-checklist.md",
    }:
        return "current generated audit output; excluded to avoid self-referential receipts"
    if any(part.casefold().startswith(".env") for part in path.parts):
        return "environment/secret configuration"
    return None


def _read(root: Path, name: str) -> bytes:
    relative = Path(name)
    path = root / relative
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("inventory path must stay inside the repository")
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root):
        raise ValueError(f"refusing symlink input: {name}")
    if not path.resolve().is_relative_to(root) or not path.is_file():
        raise ValueError(f"input is missing, nonregular or outside the repository: {name}")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(f"input exceeds file budget: {name}")
    raw = path.read_bytes()
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError(f"input exceeds file budget: {name}")
    return raw


def _reference(path: str, line: int, text: str, kind: str) -> dict:
    return {"path": path, "line": line, "text": text, "kind": kind}


def build_audit(root: Path) -> dict:
    root = root.resolve()
    names = _names(root)
    inventory, excluded, by_id = [], [], {}
    total_bytes = 0
    for name in names:
        relative = Path(name)
        if relative.suffix.casefold() not in {".md", ".txt"}:
            continue
        reason = _exclusion(relative)
        if reason:
            excluded.append({"path": name, "reason": reason, "content_read": False})
            continue
        raw = _read(root, name)
        total_bytes += len(raw)
        if total_bytes > MAX_TOTAL_BYTES:
            raise ValueError("documentation exceeds total byte budget")
        lines = raw.decode("utf-8-sig").splitlines()
        inventory.append({
            "path": name, "bytes": len(raw), "lines": len(lines),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "mechanical_read": "complete", "semantic_review": "pending",
            "role": (
                "historical_audit_evidence"
                if relative.is_relative_to(GENERATED_ROOT) and relative.name != "phase-1-spec.md"
                else "requirement_source"
            ),
        })
        if inventory[-1]["role"] == "historical_audit_evidence":
            continue
        for number, text in enumerate(lines, 1):
            ids = sorted(set(ID_RE.findall(text)))
            if not ids and NORMATIVE_RE.search(text):
                # Stable location identity; candidate obligations still require
                # human reconciliation into atomic, testable requirements.
                location = f"{name}:{number}"
                ids = ["AUD-DOC-" + hashlib.sha256(location.encode()).hexdigest()[:16]]
            for identifier in ids:
                row = by_id.setdefault(identifier, {
                    "requirement_id": identifier,
                    "record_type": "unnumbered_obligation_candidate" if identifier.startswith("AUD-DOC-") else "explicit_id",
                    "documentation_refs": [], "implementation_leads": [], "test_leads": [],
                })
                row["documentation_refs"].append(_reference(name, number, text, "documentation"))
    # Scan only first-party source. Identifier occurrences are evidence leads
    # only; they never become acceptance or completion by themselves.
    for name in names:
        relative = Path(name)
        if (
            not relative.parts or relative.parts[0] not in EVIDENCE_ROOTS
            or relative.suffix not in EVIDENCE_SUFFIXES or _exclusion(relative)
        ):
            continue
        raw = _read(root, name)
        total_bytes += len(raw)
        if total_bytes > MAX_TOTAL_BYTES:
            raise ValueError("audit inputs exceed total byte budget")
        for number, text in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
            for identifier in set(ID_RE.findall(text)):
                if identifier in by_id:
                    is_test = relative.parts[0] == "tests" or any(
                        part in {"tests", "__tests__"} for part in relative.parts
                    )
                    key = "test_leads" if is_test else "implementation_leads"
                    by_id[identifier][key].append(_reference(name, number, text, "identifier_occurrence"))
    requirements = []
    for identifier, row in sorted(by_id.items()):
        has_leads = bool(row["implementation_leads"] or row["test_leads"])
        requirements.append({
            **row, "implementation_status": "Partial" if has_leads else "Missing",
            "status_basis": "Evidence triage only; absence of literal IDs does not prove absent behavior.",
            "acceptance_verified": False, "semantic_review": "pending",
            "severity": "unassessed", "priority": "P1" if identifier.startswith(("MVP-FR-", "NFR-")) else "P2",
            "priority_basis": "Provisional audit queue priority, not approved product delivery priority.",
            "recommended_change": (
                "Inspect cited code/tests and derive atomic acceptance checks; bind fresh results before completion."
                if has_leads else
                "Trace behavior semantically before implementing; establish acceptance criteria and phase dependencies."
            ),
        })
    return {
        "schema_version": "1.0", "generated_at": datetime.now(UTC).isoformat(),
        "branch": _git(root, "branch", "--show-current").strip(),
        "head": _git(root, "rev-parse", "HEAD").strip(),
        "working_tree_dirty": bool(_git(root, "status", "--porcelain", "-z")),
        "scope": (
            "All Git-listed first-party nonignored Markdown/text, including both KGR catalogs. "
            "Historical audit Markdown is read as evidence, not indexed as new product obligations. "
            "Current generated outputs are excluded from their own read receipts."
        ),
        "status_policy": {
            "Done": "Full acceptance verified by fresh source-bound automated/manual evidence and review.",
            "Partial": "Implementation/test discovery leads exist; acceptance has not been established.",
            "Missing": "Evidence mapping missing; implementation absence is not yet established.",
        },
        "limitations": [
            "This is a complete mechanical content scan, not a complete line-by-line semantic audit.",
            "Explicit IDs can denote references, tasks or examples; unnumbered candidates are not yet atomic requirements.",
            "Range/wildcard shorthand requires semantic expansion; counts are not a complete requirement total.",
            "No product requirement is promoted to Done by this tool; historical reports and CI are not fresh verification.",
            "Uncommitted user-owned API/readiness changes are visible leads but excluded from the phase commit.",
        ],
        "counts": {
            "documents": len(inventory), "document_lines": sum(item["lines"] for item in inventory),
            "records": len(requirements),
            "by_status": dict(Counter(item["implementation_status"] for item in requirements)),
        },
        "runtime_progress": recorded_runtime_progress(root),
        "documents": inventory, "excluded": excluded, "requirements": requirements,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Current documentation audit - phase 1 evidence foundation", "",
        f"Generated: `{report['generated_at']}`; source HEAD: `{report['head']}`.",
        "", f"Scope: {report['scope']}", "",
        (f"Mechanically read {report['counts']['documents']} documents / "
         f"{report['counts']['document_lines']} lines. Indexed {report['counts']['records']} candidate records."),
        "", "**No global completion or remote CI pass is asserted.**",
        "Severity is unassessed; priorities are provisional audit ordering.", "",
        "## Limitations", *[f"- {item}" for item in report["limitations"]], "",
        "## Requirement/evidence triage", "",
        "| ID | Status | Severity / priority | Documentation | Code / test leads | Next action |",
        "|---|---|---|---|---|---|",
    ]
    progress = report.get("runtime_progress")
    if progress:
        seed = progress["seed"]
        insert_at = lines.index("## Requirement/evidence triage")
        lines[insert_at:insert_at] = [
            "## Recorded enterprise remediation progress", "",
            progress["scope"], "", f"Canonical seed inventory: `{json.dumps(seed, sort_keys=True)}`.", "",
            "| Local receipt | Outcome | Passed / failed / errors / skipped |",
            "|---|---|---|",
            *[
                f"| {receipt['path']} | {receipt['status']} | "
                + (
                    f"{receipt['passed']} / {receipt['failed']} / {receipt['errors']} / {receipt['skipped']} |"
                    if "passed" in receipt else "Not recorded |"
                )
                for receipt in progress["receipts"]
            ],
            "", *[f"- {item}" for item in progress["limitations"]], "",
        ]
    for row in report["requirements"]:
        source = row["documentation_refs"][0]
        leads = row["implementation_leads"] + row["test_leads"]
        evidence = "; ".join(f"{item['path']}:{item['line']}" for item in leads[:3]) or "No literal-ID lead"
        lines.append(
            f"| {row['requirement_id']} | {row['implementation_status']} | "
            f"{row['severity']} / {row['priority']} | {source['path']}:{source['line']} | "
            f"{evidence} | {row['recommended_change']} |"
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-directory", type=Path, default=GENERATED_ROOT)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    output = args.output_directory if args.output_directory.is_absolute() else root / args.output_directory
    if (
        output.is_symlink()
        or any(parent.is_symlink() for parent in output.parents if parent != root)
        or not output.resolve().is_relative_to(root)
    ):
        parser.error("output directory must stay inside the repository")
    # Only the designated report folder is writable; prevent source-document overwrite.
    if output.resolve() != (root / GENERATED_ROOT).resolve():
        parser.error("output directory must be EOIP-engg-doc-pkg/audits/generated")
    for filename in ("current-gap-report.json", "documentation-inventory.json", "current-gap-report.md"):
        destination = output / filename
        if destination.is_symlink() or (destination.exists() and not destination.is_file()):
            parser.error(f"output must be a regular file: {filename}")
    report = build_audit(root)
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "current-gap-report.json", report)
    write_json(output / "documentation-inventory.json", {
        "schema_version": "1.0", "generated_at": report["generated_at"],
        "head": report["head"], "scope": report["scope"], "counts": report["counts"],
        "documents": report["documents"], "excluded": report["excluded"],
        "semantic_review_complete": False,
    })
    (output / "current-gap-report.md").write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
