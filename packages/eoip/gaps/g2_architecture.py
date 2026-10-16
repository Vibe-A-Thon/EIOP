"""Executable G2 architecture guardrails.

Implements G2-ARCH-001..015 as deterministic, machine-readable checks so the
non-negotiable architecture principles are not only prose in the gap document.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ArchitectureGuardrail:
    requirement_id: str
    title: str
    config_key: str | tuple[str, ...]
    expected: Any
    description: str


@dataclass(frozen=True)
class GuardrailResult:
    requirement_id: str
    title: str
    passed: bool
    expected: Any
    actual: Any
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "title": self.title,
            "passed": self.passed,
            "expected": self.expected,
            "actual": self.actual,
            "evidence": self.evidence,
        }


DEFAULT_G2_ARCHITECTURE_PROFILE: dict[str, Any] = {
    "source_events_required": True,
    "direct_graph_writes_for_sources": False,
    "acquisition_order": [
        "webhook",
        "incremental_api",
        "rest_api",
        "repository_protocol",
        "filesystem",
        "controlled_crawler",
        "browser_automation",
    ],
    "deterministic_precedence": True,
    "source_fidelity_retained": True,
    "semantic_truth_store": "HugeGraph",
    "raw_telemetry_in_graph": False,
    "destructive_history_overwrite": False,
    "historical_queries_supported": True,
    "canonical_identity_required": True,
    "evidence_required": True,
    "local_models_required": False,
    "incremental_after_baseline": True,
    "replay_supported": True,
    "authorized_scopes_required": True,
    "progressive_complexity_required": True,
}


G2_ARCHITECTURE_GUARDRAILS: tuple[ArchitectureGuardrail, ...] = (
    ArchitectureGuardrail("G2-ARCH-001", "One acquisition contract", ("source_events_required", "direct_graph_writes_for_sources"), {"source_events_required": True, "direct_graph_writes_for_sources": False}, "Source integrations emit SourceEvent-family envelopes and do not write HugeGraph directly."),
    ArchitectureGuardrail("G2-ARCH-002", "API/event first", "acquisition_order", DEFAULT_G2_ARCHITECTURE_PROFILE["acquisition_order"], "Acquisition preference is explicit and ordered from event/API to browser automation last."),
    ArchitectureGuardrail("G2-ARCH-003", "Deterministic first", "deterministic_precedence", True, "Deterministic metadata and relationships take precedence over AI inference."),
    ArchitectureGuardrail("G2-ARCH-004", "Preserve source fidelity", "source_fidelity_retained", True, "Raw payloads or evidence references are retained for audit/replay."),
    ArchitectureGuardrail("G2-ARCH-005", "HugeGraph is semantic operational truth", "semantic_truth_store", "HugeGraph", "Canonical enterprise knowledge is written to the semantic graph store."),
    ArchitectureGuardrail("G2-ARCH-006", "No raw telemetry lake in HugeGraph", "raw_telemetry_in_graph", False, "Telemetry is summarized into semantic objects rather than copied wholesale."),
    ArchitectureGuardrail("G2-ARCH-007", "No destructive history overwrite", "destructive_history_overwrite", False, "Changes expire/replace facts instead of silently deleting history."),
    ArchitectureGuardrail("G2-ARCH-008", "Current and historical views", "historical_queries_supported", True, "Time-varying domains expose current and historical graph views."),
    ArchitectureGuardrail("G2-ARCH-009", "One semantic identity system", "canonical_identity_required", True, "Connectors resolve records into canonical IDs independent of internal source IDs."),
    ArchitectureGuardrail("G2-ARCH-010", "Evidence is mandatory", "evidence_required", True, "External and inferred mutations carry provenance or evidence metadata."),
    ArchitectureGuardrail("G2-ARCH-011", "AI is not the source of truth", "local_models_required", False, "The platform remains useful when local model providers are disabled."),
    ArchitectureGuardrail("G2-ARCH-012", "Incremental by default after baseline", "incremental_after_baseline", True, "Normal sync processes deltas after baseline with periodic reconciliation."),
    ArchitectureGuardrail("G2-ARCH-013", "Replayability", "replay_supported", True, "Supported domains can rebuild derived graph state from captured events/mappings."),
    ArchitectureGuardrail("G2-ARCH-014", "Source permissions respected", "authorized_scopes_required", True, "Connectors/crawlers operate only against configured authorized scopes."),
    ArchitectureGuardrail("G2-ARCH-015", "Progressive complexity", "progressive_complexity_required", True, "Brokers, clusters and extra stores require workload evidence."),
)


def evaluate_g2_architecture_guardrails(profile: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate the G2 architecture profile and return structured evidence."""
    effective = {**DEFAULT_G2_ARCHITECTURE_PROFILE, **(profile or {})}
    results = [
        GuardrailResult(
            requirement_id=guardrail.requirement_id,
            title=guardrail.title,
            passed=_actual_value(effective, guardrail.config_key) == guardrail.expected,
            expected=guardrail.expected,
            actual=_actual_value(effective, guardrail.config_key),
            evidence=guardrail.description,
        )
        for guardrail in G2_ARCHITECTURE_GUARDRAILS
    ]
    passed = sum(1 for result in results if result.passed)
    return {
        "profile": effective,
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "conformant": passed == len(results),
        "results": [result.to_dict() for result in results],
    }


def assert_g2_architecture_guardrails(profile: dict[str, Any] | None = None) -> None:
    report = evaluate_g2_architecture_guardrails(profile)
    if not report["conformant"]:
        failed = [item["requirement_id"] for item in report["results"] if not item["passed"]]
        raise AssertionError(f"G2 architecture guardrails failed: {', '.join(failed)}")


def _actual_value(profile: dict[str, Any], config_key: str | tuple[str, ...]) -> Any:
    if isinstance(config_key, tuple):
        return {key: profile.get(key) for key in config_key}
    return profile.get(config_key)
