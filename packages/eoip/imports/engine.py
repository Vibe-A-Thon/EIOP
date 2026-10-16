"""Data Import Engine — CSV/JSON import with validation, column mapping, and dry-run.

Validates records against schema rules before committing, supports
dry-run mode, and tracks import history.
"""

from __future__ import annotations

import csv
import enum
import io
import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


class ImportStatus(str, enum.Enum):
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    DRY_RUN = "DRY_RUN"
    IMPORTING = "IMPORTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


class ValidationType(str, enum.Enum):
    REQUIRED = "REQUIRED"
    TYPE_CHECK = "TYPE_CHECK"
    RANGE = "RANGE"
    PATTERN = "PATTERN"
    UNIQUENESS = "UNIQUENESS"
    REFERENCE = "REFERENCE"


@dataclass
class ColumnMapping:
    source_column: str
    target_field: str
    transform: str | None = None
    default_value: Any = None
    required: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_column": self.source_column,
            "target_field": self.target_field,
            "transform": self.transform,
            "default_value": self.default_value,
            "required": self.required,
        }


@dataclass
class ValidationIssue:
    row: int
    column: str
    issue_type: ValidationType
    message: str
    severity: str = "ERROR"
    value: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "row": self.row,
            "column": self.column,
            "issue_type": self.issue_type.value,
            "message": self.message,
            "severity": self.severity,
            "value": str(self.value) if self.value is not None else None,
        }


@dataclass
class ImportResult:
    job_id: str
    status: ImportStatus
    total_rows: int
    valid_rows: int
    invalid_rows: int
    imported_rows: int
    skipped_rows: int
    validation_issues: list[ValidationIssue]
    duration_ms: float
    dry_run: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "total_rows": self.total_rows,
            "valid_rows": self.valid_rows,
            "invalid_rows": self.invalid_rows,
            "imported_rows": self.imported_rows,
            "skipped_rows": self.skipped_rows,
            "issues": [i.to_dict() for i in self.validation_issues[:100]],
            "total_issues": len(self.validation_issues),
            "duration_ms": round(self.duration_ms, 2),
            "dry_run": self.dry_run,
        }


@dataclass
class ImportJob:
    job_id: str
    source_format: str
    target_entity_type: str
    status: ImportStatus
    mappings: list[ColumnMapping]
    total_rows: int = 0
    imported_rows: int = 0
    failed_rows: int = 0
    dry_run: bool = False
    author: str = ""
    tenant_id: str | None = None
    result: ImportResult | None = None
    created_at: float = field(default_factory=time.time)
    completed_at: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "source_format": self.source_format,
            "target_entity_type": self.target_entity_type,
            "status": self.status.value,
            "mappings": [m.to_dict() for m in self.mappings],
            "total_rows": self.total_rows,
            "imported_rows": self.imported_rows,
            "failed_rows": self.failed_rows,
            "dry_run": self.dry_run,
            "author": self.author,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class SchemaValidator:
    """Validates import records against type and constraint rules."""

    def __init__(self) -> None:
        self._type_checkers: dict[str, type] = {
            "string": str, "int": int, "float": float, "bool": bool,
        }
        self._field_rules: dict[str, dict[str, Any]] = {}

    def add_field_rule(self, field_name: str, field_type: str = "string",
                       required: bool = False, min_val: float | None = None,
                       max_val: float | None = None) -> None:
        self._field_rules[field_name] = {
            "type": field_type, "required": required,
            "min": min_val, "max": max_val,
        }

    def validate_record(self, record: dict[str, Any],
                        row_num: int) -> list[ValidationIssue]:
        issues = []
        for field_name, rules in self._field_rules.items():
            value = record.get(field_name)
            if rules["required"] and (value is None or value == ""):
                issues.append(ValidationIssue(
                    row=row_num, column=field_name,
                    issue_type=ValidationType.REQUIRED,
                    message=f"Required field '{field_name}' is missing",
                ))
                continue
            if value is None or value == "":
                continue

            expected_type = rules["type"]
            if expected_type in self._type_checkers:
                try:
                    if expected_type == "int":
                        coerced = int(value)
                    elif expected_type == "float":
                        coerced = float(value)
                    elif expected_type == "bool":
                        coerced = str(value).lower() in ("true", "1", "yes")
                    else:
                        coerced = str(value)

                    if rules["min"] is not None and isinstance(coerced, (int, float)):
                        if coerced < rules["min"]:
                            issues.append(ValidationIssue(
                                row=row_num, column=field_name,
                                issue_type=ValidationType.RANGE,
                                message=f"Value {coerced} below minimum {rules['min']}",
                                value=value,
                            ))
                    if rules["max"] is not None and isinstance(coerced, (int, float)):
                        if coerced > rules["max"]:
                            issues.append(ValidationIssue(
                                row=row_num, column=field_name,
                                issue_type=ValidationType.RANGE,
                                message=f"Value {coerced} above maximum {rules['max']}",
                                value=value,
                            ))
                except (ValueError, TypeError):
                    issues.append(ValidationIssue(
                        row=row_num, column=field_name,
                        issue_type=ValidationType.TYPE_CHECK,
                        message=f"Cannot convert '{value}' to {expected_type}",
                        value=value,
                    ))
        return issues


class ImportEngine:
    """Data import engine with validation, mapping, dry-run, and history."""

    def __init__(self) -> None:
        self._jobs: dict[str, ImportJob] = {}
        self._validators: dict[str, SchemaValidator] = {}
        self._imported_records: dict[str, list[dict[str, Any]]] = {}
        self._lock = threading.Lock()

    def register_validator(self, entity_type: str) -> SchemaValidator:
        validator = SchemaValidator()
        with self._lock:
            self._validators[entity_type] = validator
        return validator

    def get_validator(self, entity_type: str) -> SchemaValidator | None:
        with self._lock:
            return self._validators.get(entity_type)

    def import_csv(self, csv_data: str, entity_type: str,
                   mappings: list[ColumnMapping],
                   author: str = "",
                   dry_run: bool = False,
                   tenant_id: str | None = None) -> ImportResult:
        reader = csv.DictReader(io.StringIO(csv_data))
        records = list(reader)
        return self._run_import(records, "csv", entity_type, mappings,
                                author, dry_run, tenant_id)

    def import_json(self, json_data: str, entity_type: str,
                    mappings: list[ColumnMapping],
                    author: str = "",
                    dry_run: bool = False,
                    tenant_id: str | None = None) -> ImportResult:
        parsed = json.loads(json_data)
        records = parsed if isinstance(parsed, list) else [parsed]
        return self._run_import(records, "json", entity_type, mappings,
                                author, dry_run, tenant_id)

    def _run_import(self, records: list[dict[str, Any]],
                    source_format: str, entity_type: str,
                    mappings: list[ColumnMapping],
                    author: str, dry_run: bool,
                    tenant_id: str | None) -> ImportResult:
        start = time.time()
        job = ImportJob(
            job_id=uuid.uuid4().hex[:12],
            source_format=source_format,
            target_entity_type=entity_type,
            status=ImportStatus.VALIDATING,
            mappings=mappings,
            total_rows=len(records),
            dry_run=dry_run,
            author=author,
            tenant_id=tenant_id,
        )

        all_issues: list[ValidationIssue] = []
        valid_records: list[dict[str, Any]] = []
        validator = self._validators.get(entity_type)

        for row_num, raw_record in enumerate(records, start=1):
            mapped = self._apply_mappings(raw_record, mappings)

            if validator:
                issues = validator.validate_record(mapped, row_num)
                if issues:
                    all_issues.extend(issues)
                    has_errors = any(i.severity == "ERROR" for i in issues)
                    if has_errors:
                        continue

            valid_records.append(mapped)

        imported_count = 0
        if not dry_run and valid_records:
            job.status = ImportStatus.IMPORTING
            with self._lock:
                store = self._imported_records.setdefault(entity_type, [])
                for rec in valid_records:
                    rec["_import_job"] = job.job_id
                    rec["_imported_at"] = time.time()
                    store.append(rec)
                    imported_count += 1

        end = time.time()
        invalid_count = len(records) - len(valid_records)
        status = ImportStatus.DRY_RUN if dry_run else (
            ImportStatus.COMPLETED if invalid_count == 0 else
            ImportStatus.PARTIAL if imported_count > 0 else
            ImportStatus.FAILED
        )

        result = ImportResult(
            job_id=job.job_id,
            status=status,
            total_rows=len(records),
            valid_rows=len(valid_records),
            invalid_rows=invalid_count,
            imported_rows=imported_count,
            skipped_rows=invalid_count,
            validation_issues=all_issues,
            duration_ms=(end - start) * 1000,
            dry_run=dry_run,
        )

        job.status = status
        job.imported_rows = imported_count
        job.failed_rows = invalid_count
        job.result = result
        job.completed_at = end

        with self._lock:
            self._jobs[job.job_id] = job

        return result

    def _apply_mappings(self, record: dict[str, Any],
                        mappings: list[ColumnMapping]) -> dict[str, Any]:
        if not mappings:
            return dict(record)

        mapped: dict[str, Any] = {}
        for m in mappings:
            value = record.get(m.source_column, m.default_value)
            if value is None and m.default_value is not None:
                value = m.default_value
            if value is not None and m.transform:
                value = self._apply_transform(value, m.transform)
            mapped[m.target_field] = value
        return mapped

    def _apply_transform(self, value: Any, transform: str) -> Any:
        if transform == "lowercase":
            return str(value).lower()
        elif transform == "uppercase":
            return str(value).upper()
        elif transform == "strip":
            return str(value).strip()
        elif transform == "to_int":
            try:
                return int(value)
            except (ValueError, TypeError):
                return value
        elif transform == "to_float":
            try:
                return float(value)
            except (ValueError, TypeError):
                return value
        return value

    def get_job(self, job_id: str) -> ImportJob | None:
        with self._lock:
            return self._jobs.get(job_id)

    def get_imported_records(self, entity_type: str,
                             limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            records = self._imported_records.get(entity_type, [])
            return records[-limit:]

    def list_jobs(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            jobs = sorted(self._jobs.values(),
                          key=lambda j: j.created_at, reverse=True)
            return [j.to_dict() for j in jobs[:limit]]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total_imported = sum(len(r) for r in self._imported_records.values())
            by_format: dict[str, int] = {}
            for j in self._jobs.values():
                by_format[j.source_format] = by_format.get(j.source_format, 0) + 1
            return {
                "total_jobs": len(self._jobs),
                "total_imported_records": total_imported,
                "entity_types": list(self._imported_records.keys()),
                "validators_registered": len(self._validators),
                "by_format": by_format,
            }


_INSTANCE: ImportEngine | None = None
_LOCK = threading.Lock()


def get_import_engine() -> ImportEngine:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = ImportEngine()
    return _INSTANCE
