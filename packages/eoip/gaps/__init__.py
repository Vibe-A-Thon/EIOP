"""Competitive GAP requirement registry and coverage reporting."""

from eoip.gaps.coverage import (
    GapCoverageReport,
    GapRequirement,
    build_gap_coverage_report,
    load_gap_requirements,
)

__all__ = [
    "GapCoverageReport",
    "GapRequirement",
    "build_gap_coverage_report",
    "load_gap_requirements",
]
