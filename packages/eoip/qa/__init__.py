"""QA gate integrity: behavioral evidence, mutation checks, status dashboards,
code introspection inventories and lint policy gates (SR-QA-010..014, §17.3).

The prior gate implementation (``eoip.gaps.coverage``) proved that literal
string matching over comments/docstrings is gameable: any source line that
happens to mention a requirement ID counted as "evidence".  This package is
the corrective: evidence is *structured data* (explicit registry entries and
pytest markers), never text scanning.

Implements:
- SR-QA-010: requirement -> test mapping stored as data; docstring/comment
  references never count.
- SR-QA-011: mutation/negative checks prove mapped tests fail when the
  behavior is broken (sampled per release).
- SR-QA-012: dashboards report three separate numbers; no "% complete".
- SR-QA-013: inventories are generated from code introspection; hand-written
  counts fail validation.
- SR-QA-014: ruff runs at zero-error policy (report-only gate).
"""

from eoip.qa.dashboard import ExternalGateRecord, StatusDashboard
from eoip.qa.evidence import BehavioralEvidenceRegistry, EvidenceEntry
from eoip.qa.introspection import CodeIntrospector, InventorySnapshot
from eoip.qa.mutation import MutationCheck, MutationCheckStore
from eoip.qa.policy import PolicyGate, PolicyGateResult

__all__ = [
    "BehavioralEvidenceRegistry",
    "CodeIntrospector",
    "EvidenceEntry",
    "ExternalGateRecord",
    "InventorySnapshot",
    "MutationCheck",
    "MutationCheckStore",
    "PolicyGate",
    "PolicyGateResult",
    "StatusDashboard",
    "build_router",
]


def build_router(*args, **kwargs):
    """Lazy delegate to :func:`eoip.qa.router.build_router` (keeps fastapi import lazy)."""
    from eoip.qa.router import build_router as _build_router

    return _build_router(*args, **kwargs)
