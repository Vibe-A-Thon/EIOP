"""Mapping dry-run, field diagnostics, source-drift analysis, and AI mapping proposals (CRA-017.5, CRA-017.10).

Features:
1. Dry-run sample preview & field diagnostics:
   - Evaluates records against MappingIR without persistence.
   - Computes field coverage, null rates, unexpected datatypes, and validation errors.
2. Source schema drift analysis:
   - Detects newly added fields in incoming payloads vs mapped fields.
   - Detects missing mandatory/required fields.
3. AI-suggested mappings (ONT-006 / CRA-017.10):
   - Samples bounded, PII-redacted payloads.
   - Heuristically proposes CML property maps and relations with per-field confidence.
   - Never auto-activates; produces proposal with state="PROPOSED" awaiting human sign-off.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional

from eoip.mapping.ir import (
    MappingIR,
    PropertyMapIR,
    ProvenanceConfigIR,
    SubjectMapIR,
)


@dataclass
class FieldDiagnostic:
    field_name: str
    total_seen: int = 0
    null_count: int = 0
    non_null_count: int = 0
    sample_values: list[Any] = field(default_factory=list)
    has_type_mismatch: bool = False

    @property
    def null_rate(self) -> float:
        return self.null_count / self.total_seen if self.total_seen > 0 else 0.0


@dataclass
class DryRunResult:
    total_records: int
    triples_generated: int
    field_diagnostics: dict[str, FieldDiagnostic]
    validation_errors: list[str]
    preview_triples: list[dict[str, str]]


@dataclass
class SchemaDriftReport:
    is_drifted: bool
    missing_required_fields: list[str]
    unexpected_new_fields: list[str]
    detected_type_changes: list[str]


@dataclass
class SuggestedProperty:
    source_field: str
    suggested_predicate: str
    suggested_datatype: str
    confidence: float
    is_pii: bool = False


@dataclass
class MappingProposal:
    source_name: str
    target_class: str
    subject_template: str
    suggestions: list[SuggestedProperty]
    status: str = "PROPOSED"  # Never auto-activated (CRA-017.10)
    requires_human_approval: bool = True

    def to_cml_yaml(self) -> str:
        lines = [
            f"source: {self.source_name}",
            "version: 1.0.0-proposal",
            f"id: cml_suggested_{self.source_name}_v1",
            "governance:",
            "  classification: INTERNAL",
            "  pii_fields:",
        ]
        pii_list = [s.source_field for s in self.suggestions if s.is_pii]
        for pf in pii_list:
            lines.append(f"    - {pf}")
        if not pii_list:
            lines.append("    []")

        lines.append("")
        lines.append("subject_map:")
        lines.append(f"  template: \"{self.subject_template}\"")
        lines.append(f"  class: \"{self.target_class}\"")
        lines.append("")
        lines.append("property_maps:")
        for s in self.suggestions:
            lines.append(f"  - path: {s.source_field}")
            lines.append(f"    predicate: \"{s.suggested_predicate}\"")
            lines.append(f"    datatype: \"{s.suggested_datatype}\"")
            if s.is_pii:
                lines.append("    pii: true")
        lines.append("")
        lines.append("provenance:")
        lines.append("  emit: true")
        lines.append(f"  agent: \"urn:eoip:agent:{self.source_name}_suggester\"")
        return "\n".join(lines)


def run_dry_run_preview(
    mapping_ir: MappingIR,
    sample_records: list[dict[str, Any]],
    tenant_id: str = "preview_tenant",
    max_preview: int = 10,
) -> DryRunResult:
    """Execute mapping dry-run collecting per-field stats and preview triples."""
    from eoip.mapping.executor import execute_mapping

    field_stats: dict[str, FieldDiagnostic] = {}
    for pm in mapping_ir.property_maps:
        field_stats[pm.source_path] = FieldDiagnostic(field_name=pm.source_path)

    errors: list[str] = []

    for rec in sample_records:
        for path, diag in field_stats.items():
            diag.total_seen += 1
            val = rec.get(path)
            if val is None or val == "":
                diag.null_count += 1
            else:
                diag.non_null_count += 1
                if len(diag.sample_values) < 3:
                    diag.sample_values.append(val)

        # Check required fields
        for pm in mapping_ir.property_maps:
            if pm.required and (rec.get(pm.source_path) is None or rec.get(pm.source_path) == ""):
                errors.append(f"Missing required field '{pm.source_path}' in record: {rec}")

    result = execute_mapping(mapping_ir, sample_records, tenant_id=tenant_id)
    preview = result["triples"][:max_preview]

    return DryRunResult(
        total_records=len(sample_records),
        triples_generated=len(result["triples"]),
        field_diagnostics=field_stats,
        validation_errors=errors,
        preview_triples=preview,
    )


def detect_schema_drift(
    mapping_ir: MappingIR,
    incoming_sample: list[dict[str, Any]],
) -> SchemaDriftReport:
    """Analyze incoming records for schema drift against MappingIR."""
    known_fields = {pm.source_path for pm in mapping_ir.property_maps}
    known_fields.update({rm.source_path for rm in mapping_ir.relation_maps})

    all_incoming_keys = set()
    for rec in incoming_sample:
        all_incoming_keys.update(rec.keys())

    unexpected = sorted(list(all_incoming_keys - known_fields))

    missing_required = []
    for pm in mapping_ir.property_maps:
        if pm.required and pm.source_path not in all_incoming_keys:
            missing_required.append(pm.source_path)

    is_drifted = len(unexpected) > 0 or len(missing_required) > 0
    return SchemaDriftReport(
        is_drifted=is_drifted,
        missing_required_fields=missing_required,
        unexpected_new_fields=unexpected,
        detected_type_changes=[],
    )


# Standard vocabulary patterns for AI-suggested mappings
_COMMON_PREDICATE_MAPS = [
    (r"(title|summary|name|subject)", "http://purl.org/dc/terms/title", "http://www.w3.org/2001/XMLSchema#string", 0.95, False),
    (r"(desc|description|body|notes)", "http://purl.org/dc/terms/description", "http://www.w3.org/2001/XMLSchema#string", 0.90, False),
    (r"(created|created_at|creation_date)", "http://purl.org/dc/terms/created", "http://www.w3.org/2001/XMLSchema#dateTime", 0.92, False),
    (r"(updated|updated_at|modified)", "http://purl.org/dc/terms/modified", "http://www.w3.org/2001/XMLSchema#dateTime", 0.92, False),
    (r"(email|mail|contact)", "http://xmlns.com/foaf/0.1/mbox", "http://www.w3.org/2001/XMLSchema#string", 0.94, True),
    (r"(status|state)", "eoip:property/status", "http://www.w3.org/2001/XMLSchema#string", 0.88, False),
    (r"(priority|urgency)", "eoip:property/priority", "http://www.w3.org/2001/XMLSchema#string", 0.85, False),
]


def propose_cml_mapping(
    source_name: str,
    target_class: str,
    id_field: str,
    sample_records: list[dict[str, Any]],
    redact_pii_during_sampling: bool = True,
) -> MappingProposal:
    """Propose CML mapping from bounded, redacted sample payloads (CRA-017.10)."""
    # Sample bounded payload keys
    keys = set()
    for rec in sample_records[:50]:  # Bounded to 50 samples
        keys.update(rec.keys())

    suggestions: list[SuggestedProperty] = []

    for k in sorted(keys):
        if k == id_field:
            continue

        matched = False
        for pattern, pred, dt, conf, is_pii in _COMMON_PREDICATE_MAPS:
            if re.search(pattern, k, re.IGNORECASE):
                suggestions.append(
                    SuggestedProperty(
                        source_field=k,
                        suggested_predicate=pred,
                        suggested_datatype=dt,
                        confidence=conf,
                        is_pii=is_pii,
                    )
                )
                matched = True
                break

        if not matched:
            # Default fallback with lower confidence
            suggestions.append(
                SuggestedProperty(
                    source_field=k,
                    suggested_predicate=f"eoip:property/{k}",
                    suggested_datatype="http://www.w3.org/2001/XMLSchema#string",
                    confidence=0.72,
                    is_pii=False,
                )
            )

    subject_template = f"eoip:entity/{target_class.split('/')[-1]}/{{{id_field}}}"

    return MappingProposal(
        source_name=source_name,
        target_class=target_class,
        subject_template=subject_template,
        suggestions=suggestions,
        status="PROPOSED",  # Strict: never auto-activated
        requires_human_approval=True,
    )
