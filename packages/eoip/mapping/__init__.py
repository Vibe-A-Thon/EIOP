"""Mapping package — Connector Mapping Language (CML), Mapping IR, and LPG/RDF projection engine."""

from eoip.mapping.ir import (
    MappingIR,
    SubjectMapIR,
    PropertyMapIR,
    RelationMapIR,
    ProvenanceConfigIR,
)
from eoip.mapping.cml import (
    CMLParseError,
    parse_and_compile_cml,
    safe_apply_template,
)
from eoip.mapping.executor import (
    execute_mapping,
)
from eoip.mapping.r2rml import (
    R2RMLAdapter,
    LossReport,
    UnsupportedConstruct,
)
from eoip.mapping.virtualization import (
    FreshnessModel,
    MappingExecutionMode,
    VirtualContext,
    MaterializedContext,
    OBDAPushdownEngine,
)
from eoip.mapping.diagnostics import (
    FieldDiagnostic,
    DryRunResult,
    SchemaDriftReport,
    SuggestedProperty,
    MappingProposal,
    run_dry_run_preview,
    detect_schema_drift,
    propose_cml_mapping,
)

__all__ = [
    "MappingIR",
    "SubjectMapIR",
    "PropertyMapIR",
    "RelationMapIR",
    "ProvenanceConfigIR",
    "CMLParseError",
    "parse_and_compile_cml",
    "safe_apply_template",
    "execute_mapping",
    "R2RMLAdapter",
    "LossReport",
    "UnsupportedConstruct",
    "FreshnessModel",
    "MappingExecutionMode",
    "VirtualContext",
    "MaterializedContext",
    "OBDAPushdownEngine",
    "FieldDiagnostic",
    "DryRunResult",
    "SchemaDriftReport",
    "SuggestedProperty",
    "MappingProposal",
    "run_dry_run_preview",
    "detect_schema_drift",
    "propose_cml_mapping",
]
