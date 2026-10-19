"""Readiness gates evaluator and release policy enforcement (T-214 / REVA-PD-009 / §14.3)."""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
import yaml

from reva.core.errors import RevaValidationError
from reva.pd.ledger import LedgerRecord

REMEDIATION_MAP = {
    "OBLIGATION_OPEN": "Execute bound verifiers for open obligation",
    "OBLIGATION_FAILED": "Investigate failing test assertions and fix defects",
    "OBLIGATION_BLOCKED": "Resolve linked blocking knowledge gaps or contradictions",
    "OBLIGATION_STALE": "Re-run verifiers against updated owner code digest",
    "CHECK_FAILED": "Review automated gate check failure details and remediate",
}


@dataclass
class GateStage:
    stage_id: str
    obligations: List[str] = field(default_factory=list)  # Globs supported
    checks: List[str] = field(default_factory=list)  # Named check functions


@dataclass
class GateDefinition:
    gate_id: str
    stages: List[GateStage] = field(default_factory=list)


@dataclass
class GateFinding:
    stage_id: str
    reason_code: str
    obligation_key: Optional[str]
    next_action: str
    details: Optional[str] = None


@dataclass
class GateOutcome:
    gate_id: str
    passed: bool
    findings: List[GateFinding] = field(default_factory=list)


def load_gate_definition(yaml_source: Union[str, Path]) -> GateDefinition:
    """Load and validate gate definition from YAML source."""
    if isinstance(yaml_source, Path) or (
        isinstance(yaml_source, str) and "\n" not in yaml_source and Path(yaml_source).is_file()
    ):
        content = Path(yaml_source).read_text(encoding="utf-8")
    else:
        content = str(yaml_source)

    data = yaml.safe_load(content)
    if not isinstance(data, dict) or "gate_id" not in data:
        raise RevaValidationError("Gate definition must be a dictionary with 'gate_id' and 'stages'")

    stages: List[GateStage] = []
    for s in data.get("stages", []):
        stages.append(
            GateStage(
                stage_id=s.get("stage_id", "stage"),
                obligations=s.get("obligations", []),
                checks=s.get("checks", []),
            )
        )

    return GateDefinition(gate_id=data["gate_id"], stages=stages)


def evaluate_gate(
    gate: GateDefinition,
    ledger: LedgerRecord,
    custom_checks: Optional[Dict[str, Callable[[], bool]]] = None,
) -> GateOutcome:
    """Evaluate readiness gate against ledger using fail-closed aggregation."""
    findings: List[GateFinding] = []
    custom_checks = custom_checks or {}
    closure_map = {c.obligation_key: c for c in ledger.closures}

    for stage in gate.stages:
        # 1. Match obligations against globs
        for pattern in stage.obligations:
            matched_keys = [k for k in closure_map.keys() if fnmatch.fnmatch(k, pattern)]
            if not matched_keys:
                findings.append(
                    GateFinding(
                        stage_id=stage.stage_id,
                        reason_code="OBLIGATION_MISSING",
                        obligation_key=pattern,
                        next_action="Define and bind required obligation",
                        details=f"Pattern '{pattern}' matched no obligations in ledger",
                    )
                )
            for k in matched_keys:
                dec = closure_map[k]
                if dec.outcome != "closed":
                    reason = f"OBLIGATION_{dec.outcome.upper()}"
                    findings.append(
                        GateFinding(
                            stage_id=stage.stage_id,
                            reason_code=reason,
                            obligation_key=k,
                            next_action=REMEDIATION_MAP.get(reason, "Investigate non-closed outcome"),
                            details=f"Outcome is {dec.outcome}, reasons: {dec.reasons}",
                        )
                    )

        # 2. Execute custom stage checks
        for check_name in stage.checks:
            handler = custom_checks.get(check_name)
            if handler is not None:
                try:
                    passed = handler()
                    if not passed:
                        findings.append(
                            GateFinding(
                                stage_id=stage.stage_id,
                                reason_code="CHECK_FAILED",
                                obligation_key=None,
                                next_action=REMEDIATION_MAP["CHECK_FAILED"],
                                details=f"Check '{check_name}' returned False",
                            )
                        )
                except Exception as e:
                    findings.append(
                        GateFinding(
                            stage_id=stage.stage_id,
                            reason_code="CHECK_ERROR",
                            obligation_key=None,
                            next_action="Fix error in check execution",
                            details=str(e),
                        )
                    )

    passed = len(findings) == 0
    return GateOutcome(gate_id=gate.gate_id, passed=passed, findings=findings)
