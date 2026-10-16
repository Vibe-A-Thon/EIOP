"""Conservative import and validation of the CP audit execution registry."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AUDIT_FILE = "gaps-audit-cp.md"
PLAN_FILE = "gaps-audit-cp-implementation-plan.md"
AUDIT_SHA256 = "affc9247d2383b02a4e9257e9bb85b9d20e81593f28c3e4d40d29323f17ed602"
AUDIT_COUNT = 2603
REGISTRY_BASELINE_FILE = "config/verification/cp-registry-baseline.json"
REGISTRY_BASELINE_SHA256 = "55917afdef287ee9c167c4f164b90b7ff74217423e89ef378f6783c5bb58df94"
MAX_DOCUMENT_BYTES = 16 * 1024 * 1024
STATES = Literal["UNTRIAGED", "READY", "IN_PROGRESS", "IMPLEMENTED", "INTEGRATION_VERIFIED", "VERIFIED", "BLOCKED"]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_file(root: Path, relative: str) -> Path:
    path = root / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Reference must remain inside the project: {relative}")
    if not path.is_file():
        raise ValueError(f"Missing referenced file: {relative}")
    return path


def read_document(path: Path) -> bytes:
    if path.stat().st_size > MAX_DOCUMENT_BYTES:
        raise ValueError(f"Document exceeds size limit: {path.name}")
    return path.read_bytes()


def matrix_rows(text: str):
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.startswith("| `REQ-"):
            # The audit embeds escaped table rows within its requirement cells.
            cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
            yield line_number, cells


class AcceptanceClause(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1)
    outcome: str = Field(min_length=1)
    test_node_ids: list[str] = Field(default_factory=list)


class ReceiptReference(BaseModel):
    model_config = ConfigDict(extra="forbid")
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class Implementation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[1] = 1
    state: STATES = "UNTRIAGED"
    classification: Literal["UNRESOLVED", "ENGINEERING", "ALIAS", "METADATA_ONLY", "EXTERNAL_OWNER", "SUPERSEDED"] = "UNRESOLVED"
    primary_package: str = Field(pattern=r"^CP-(?:[0-2][0-9]|3[0-7])$")
    secondary_packages: list[str] = Field(default_factory=list)
    source_reviewed: bool = False
    canonical_id: str | None = None
    disposition_reason: str = ""
    public_entrypoints: list[str] = Field(default_factory=list)
    acceptance_clauses: list[AcceptanceClause] = Field(default_factory=list)
    receipts: list[ReceiptReference] = Field(default_factory=list)
    blocker: str | None = None


def load_audit(root: Path, *, expected_sha256: str | None = AUDIT_SHA256,
               expected_count: int | None = AUDIT_COUNT) -> list[dict]:
    raw = read_document(local_file(root, AUDIT_FILE))
    audit_hash = digest(raw.replace(b"\r\n", b"\n"))
    if expected_sha256 and audit_hash != expected_sha256:
        raise ValueError("Audit digest changed; explicitly reconcile the baseline before importing")
    source_cache: dict[str, tuple[str, list[str]]] = {}
    records, seen, originals = [], set(), set()
    for line_number, cells in matrix_rows(raw.decode("utf-8-sig")):
        if len(cells) != 15:
            raise ValueError(f"Audit line {line_number}: expected 15 columns")
        audit_id = cells[0].strip("`")
        match = re.fullmatch(r"`([^`]+)`: (.+)", cells[1])
        if not re.fullmatch(r"REQ-[A-Z]+-\d{3}", audit_id) or not match:
            raise ValueError(f"Malformed audit requirement at line {line_number}")
        original_id, title = match.groups()
        if audit_id in seen or original_id in originals:
            raise ValueError(f"Duplicate audit/original ID: {audit_id} / {original_id}")
        seen.add(audit_id)
        originals.add(original_id)
        source = re.fullmatch(r"`(.+):(\d+)`", cells[2])
        if not source:
            raise ValueError(f"Invalid source reference for {audit_id}")
        source_path, source_line = source.group(1), int(source.group(2))
        if source_path not in source_cache:
            if source_path == "requirements-registry.json":
                # The audit cites the pre-migration registry; never read our own output as input.
                source_raw = read_document(local_file(root, REGISTRY_BASELINE_FILE))
                if digest(source_raw.replace(b"\r\n", b"\n")) != REGISTRY_BASELINE_SHA256:
                    raise ValueError("Historical registry baseline digest changed")
            else:
                source_raw = read_document(local_file(root, source_path))
            source_cache[source_path] = (digest(source_raw.replace(b"\r\n", b"\n")),
                                         source_raw.decode("utf-8-sig").splitlines())
        source_hash, source_lines = source_cache[source_path]
        if not 1 <= source_line <= len(source_lines):
            raise ValueError(f"Source line outside document for {audit_id}")
        baseline = dict(zip(
            ["audit_id", "requirement", "source", "type", "priority", "acceptance", "status",
             "evidence", "tests", "gap", "root_cause", "severity", "effort", "depends_on", "recommended_fix"],
            cells, strict=True,
        ))
        baseline.update(audit_id=audit_id, original_id=original_id, audit_line=line_number,
                        audit_sha256=audit_hash, source_path=source_path, source_line=source_line,
                        source_sha256=source_hash, source_line_text=source_lines[source_line - 1],
                        text_hash_normalization="utf8-lf")
        records.append({"id": original_id, "title": title, "audit_baseline": baseline})
    if not records or (expected_count is not None and len(records) != expected_count):
        raise ValueError(f"Unexpected audit requirement count: {len(records)}")
    return records


def load_routing(root: Path, audit: list[dict]) -> dict[str, str]:
    text = read_document(local_file(root, PLAN_FILE)).decode("utf-8-sig")
    routes = {}
    for line_number, cells in matrix_rows(text):
        if len(cells) != 8:
            raise ValueError(f"Plan line {line_number}: expected 8 columns")
        audit_id = cells[0].strip("`")
        package = re.fullmatch(r"\[(CP-\d{2})\]\(#(cp-\d{2})\)", cells[5])
        if audit_id in routes or package is None or package.group(1).lower() != package.group(2):
            raise ValueError(f"Duplicate or invalid plan route for {audit_id}")
        routes[audit_id] = package.group(1)
    expected = {record["audit_baseline"]["audit_id"] for record in audit}
    if set(routes) != expected:
        raise ValueError("Plan coverage does not match the exact audit ID set")
    return routes


def load_registry(path: Path) -> list[dict]:
    data = json.loads(read_document(path))
    if not isinstance(data, list) or any(not isinstance(row, dict)
            or not isinstance(row.get("id"), str) or not row["id"].strip() for row in data):
        raise ValueError("Registry must be a list of records with IDs")
    if len({row["id"] for row in data}) != len(data):
        raise ValueError("Registry contains duplicate IDs")
    return data


def migrate_registry(existing: list[dict], audit: list[dict], routing: dict[str, str]) -> list[dict]:
    """Keep legacy IDs and fields, but never promote references into verified status."""
    records = {}
    for original in existing:
        if original["id"] in records:
            raise ValueError(f"Duplicate registry ID: {original['id']}")
        record = dict(original)
        if "legacy_claims" not in record:
            record["legacy_claims"] = {key: record[key] for key in ("status", "evidence_receipt") if key in record}
        record.pop("evidence_receipt", None)
        record["status"] = record.get("implementation", {}).get("state", "UNVERIFIED")
        records[record["id"]] = record
    for imported in audit:
        original_id = imported["id"]
        baseline = imported["audit_baseline"]
        record = records.setdefault(original_id, {"id": original_id, "title": imported["title"]})
        if "audit_baseline" in record and record["audit_baseline"] != baseline:
            raise ValueError(f"Immutable audit/source baseline changed for {original_id}")
        record["audit_baseline"] = baseline
        if "implementation" not in record:
            record["implementation"] = Implementation(primary_package=routing[baseline["audit_id"]]).model_dump()
        execution = Implementation.model_validate(record["implementation"])
        record["status"] = execution.state
    return [records[key] for key in sorted(records)]


def validate_registry(root: Path, records: list[dict], audit: list[dict]) -> dict:
    from eoip.verification.test_receipts import validate_receipt

    expected = {row["id"]: row["audit_baseline"] for row in audit}
    by_id = {row["id"]: row for row in records}
    errors, states = [], Counter()
    if len(by_id) != len(records):
        errors.append("Duplicate registry IDs")
    for original_id, baseline in expected.items():
        record = by_id.get(original_id)
        if record is None:
            errors.append(f"Missing audit requirement {original_id}")
            continue
        if record.get("audit_baseline") != baseline:
            errors.append(f"Audit/source baseline mismatch: {original_id}")
        try:
            execution = Implementation.model_validate(record.get("implementation"))
            states[execution.state] += 1
            if record.get("status") != execution.state:
                raise ValueError("status must match implementation.state")
            if execution.state == "BLOCKED" and not execution.blocker:
                raise ValueError("blocked requirements need a blocker")
            if (execution.state not in {"UNTRIAGED", "BLOCKED"}
                    and (not execution.source_reviewed or execution.classification == "UNRESOLVED")):
                raise ValueError("source review and classification are required before work starts")
            if execution.classification in {"ALIAS", "SUPERSEDED"}:
                if not execution.disposition_reason or execution.canonical_id not in by_id:
                    raise ValueError("alias/supersession requires a valid canonical ID and reason")
                visited = {original_id}
                target = execution.canonical_id
                while target:
                    if target in visited:
                        raise ValueError("cyclic canonical reference")
                    visited.add(target)
                    target = by_id.get(target, {}).get("implementation", {}).get("canonical_id")
            clause_ids = [clause.id for clause in execution.acceptance_clauses]
            if len(clause_ids) != len(set(clause_ids)):
                raise ValueError("duplicate acceptance clause IDs")
            if execution.state in {"INTEGRATION_VERIFIED", "VERIFIED"}:
                if execution.classification != "ENGINEERING":
                    raise ValueError("non-engineering dispositions cannot claim engineering verification")
                if not execution.acceptance_clauses or not execution.public_entrypoints or not execution.receipts:
                    raise ValueError("verification requires acceptance clauses, public entrypoints and execution receipts")
                passed = set()
                for reference in execution.receipts:
                    path = local_file(root, reference.path)
                    raw = read_document(path)
                    if digest(raw) != reference.sha256:
                        raise ValueError("receipt hash mismatch")
                    receipt = json.loads(raw)
                    validate_receipt(root, receipt)
                    for case in receipt["tests"]:
                        if original_id in case["requirements"] or baseline["audit_id"] in case["requirements"]:
                            passed.add(case["nodeid"])
                for clause in execution.acceptance_clauses:
                    if not clause.test_node_ids or not set(clause.test_node_ids) <= passed:
                        raise ValueError(f"missing passing tagged evidence for clause {clause.id}")
                # Test receipts establish execution only; integration/sign-off requires its own verifier.
                raise ValueError("full integration/acceptance evidence verifier is not yet implemented; retain IMPLEMENTED")
        except (ValueError, KeyError, TypeError, OSError) as exc:
            errors.append(f"{original_id}: {exc}")
    extras = [row["id"] for row in records if "audit_baseline" in row and row["id"] not in expected]
    if extras:
        errors.append(f"Unrecognized audit records: {extras}")
    return {"schema_version": 1, "valid": not errors, "audit_records": len(expected),
            "registry_records": len(records), "legacy_only_records": len(set(by_id) - set(expected)),
            "states": dict(sorted(states.items())), "errors": errors,
            "implementation_completion_percent": None}
