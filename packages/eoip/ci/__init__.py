"""KG CI/CD pipeline (requirements §30, GAP-KGCI-001..004, release gates §16).

Unified, deterministic pipeline for ontology/knowledge-graph releases:
lint → schema validation → contract checks → graph invariant tests →
quality gates → compatibility check → security checks → migration
simulation → publish. Every stage reports pass/fail/skipped with findings;
the aggregate :class:`KGCIReport` carries the overall verdict and exit code.

Runnable as ``python -m packages.eoip.ci`` or used as a library via
:class:`KGCIPipeline` / :func:`run_pipeline`.
"""

from eoip.ci.pipeline import (
    FAIL_ON_ANY,
    FAIL_ON_BREAKING,
    FAIL_ON_NEVER,
    Finding,
    KGCIPipeline,
    KGCIReport,
    StageResult,
    StageStatus,
    run_pipeline,
)

__all__ = [
    "FAIL_ON_ANY",
    "FAIL_ON_BREAKING",
    "FAIL_ON_NEVER",
    "Finding",
    "KGCIPipeline",
    "KGCIReport",
    "StageResult",
    "StageStatus",
    "run_pipeline",
]
