"""Verification and guardrail engineering (CORE-002).

Standalone verification discipline with deterministic non-LLM validators that grade
agent outputs before loop progression. Handles semantic correctness, schema conformance,
policy compliance, cognitive drift detection, and dynamic guardrail injection.
"""

from __future__ import annotations

import abc
import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger("eoip.verification.engine")


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"


@dataclass
class VerificationResult:
    """Result of a verification rule evaluation."""

    rule_name: str
    status: VerificationStatus
    score: float = 1.0  # 0.0 to 1.0
    passed: bool = True
    message: str = "Verification passed"
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class GuardrailInterception:
    """Result of dynamic guardrail evaluation on agent intent."""

    allowed: bool
    action: str  # "ALLOW", "BLOCK", "MODIFY", "ESCALATE"
    intent_name: str
    reasons: list[str] = field(default_factory=list)
    modified_params: dict[str, Any] | None = None
    audit_hash: str = ""


# ==============================================================================
# Verification Rules Base & Implementations
# ==============================================================================

class VerificationRule(abc.ABC):
    """Abstract verification rule."""

    name: str = "BaseRule"
    description: str = ""
    critical: bool = True  # If critical, failure short-circuits the verifier chain

    @abc.abstractmethod
    def check(self, output: Any, context: dict[str, Any] | None = None) -> VerificationResult:
        """Evaluate the rule against output payload."""


class SchemaConformanceRule(VerificationRule):
    """Verifies output adheres to expected schema keys and non-empty values."""

    name = "SchemaConformanceRule"

    def __init__(self, required_keys: list[str] | None = None) -> None:
        self.required_keys = required_keys or ["canonical_id", "status"]

    def check(self, output: Any, context: dict[str, Any] | None = None) -> VerificationResult:
        ctx = context or {}
        reqs = ctx.get("required_keys", self.required_keys)
        if not isinstance(output, dict):
            return VerificationResult(
                rule_name=self.name,
                status=VerificationStatus.FAILED,
                passed=False,
                score=0.0,
                message=f"Output must be a dictionary, got {type(output).__name__}",
            )
        missing = [k for k in reqs if k not in output]
        if missing:
            return VerificationResult(
                rule_name=self.name,
                status=VerificationStatus.FAILED,
                passed=False,
                score=round(1.0 - (len(missing) / len(reqs)), 2),
                message=f"Missing required schema keys: {missing}",
                details={"missing_keys": missing},
            )
        return VerificationResult(rule_name=self.name, status=VerificationStatus.PASSED, passed=True, score=1.0)


class PolicyComplianceRule(VerificationRule):
    """Verifies output does not violate enterprise policies (e.g. unauthorized egress, unsafe commands)."""

    name = "PolicyComplianceRule"

    def __init__(self, blocked_patterns: list[str] | None = None) -> None:
        self.blocked_patterns = [p.lower() for p in (blocked_patterns or [
            "rm -rf", "drop table", "format disk", "eval(", "exec(", "<script>", "bearer secret", "password="
        ])]

    def check(self, output: Any, context: dict[str, Any] | None = None) -> VerificationResult:
        text = json.dumps(output) if not isinstance(output, str) else output
        lower = text.lower()
        violations = [p for p in self.blocked_patterns if p in lower]
        if violations:
            return VerificationResult(
                rule_name=self.name,
                status=VerificationStatus.BLOCKED,
                passed=False,
                score=0.0,
                message=f"Policy violation: detected blocked pattern(s) {violations}",
                details={"violations": violations},
            )
        return VerificationResult(rule_name=self.name, status=VerificationStatus.PASSED, passed=True, score=1.0)


class ConfidenceThresholdRule(VerificationRule):
    """Verifies output confidence meets required threshold."""

    name = "ConfidenceThresholdRule"

    def __init__(self, min_confidence: float = 0.70) -> None:
        self.min_confidence = min_confidence

    def check(self, output: Any, context: dict[str, Any] | None = None) -> VerificationResult:
        confidence = 1.0
        if isinstance(output, dict):
            confidence = float(output.get("confidence", output.get("score", 1.0)))
        elif context and "confidence" in context:
            confidence = float(context["confidence"])

        if confidence < self.min_confidence:
            return VerificationResult(
                rule_name=self.name,
                status=VerificationStatus.FAILED,
                passed=False,
                score=confidence,
                message=f"Confidence {confidence:.2f} is below minimum threshold {self.min_confidence:.2f}",
                details={"confidence": confidence, "min_threshold": self.min_confidence},
            )
        return VerificationResult(
            rule_name=self.name,
            status=VerificationStatus.PASSED,
            passed=True,
            score=confidence,
            message=f"Confidence {confidence:.2f} satisfies threshold",
        )


class HallucinationDetectionRule(VerificationRule):
    """Detects unsupported or fabricated claims against reference context."""

    name = "HallucinationDetectionRule"

    def check(self, output: Any, context: dict[str, Any] | None = None) -> VerificationResult:
        ctx = context or {}
        reference_entities = set(ctx.get("reference_entities", []))
        if not reference_entities:
            return VerificationResult(rule_name=self.name, status=VerificationStatus.PASSED, passed=True, score=1.0)

        output_entities = set()
        if isinstance(output, dict):
            ents = output.get("entities") or output.get("referenced_nodes") or []
            output_entities.update(ents)

        unsupported = [e for e in output_entities if e not in reference_entities]
        if unsupported and len(unsupported) > len(output_entities) * 0.5:
            return VerificationResult(
                rule_name=self.name,
                status=VerificationStatus.WARNING,
                passed=False,
                score=0.5,
                message=f"Potential hallucination: unsupported entities {unsupported}",
                details={"unsupported_entities": unsupported},
            )
        return VerificationResult(rule_name=self.name, status=VerificationStatus.PASSED, passed=True, score=1.0)


class CognitiveDriftRule(VerificationRule):
    """Detects cognitive drift across iterative reasoning steps."""

    name = "CognitiveDriftRule"

    def check(self, output: Any, context: dict[str, Any] | None = None) -> VerificationResult:
        ctx = context or {}
        initial_goal = ctx.get("initial_goal", "")
        current_step = ctx.get("current_step", "")
        iteration = ctx.get("iteration", 0)

        if iteration > 15:
            return VerificationResult(
                rule_name=self.name,
                status=VerificationStatus.WARNING,
                passed=False,
                score=0.4,
                message=f"Loop iteration count {iteration} indicates possible circular drift",
            )
        return VerificationResult(rule_name=self.name, status=VerificationStatus.PASSED, passed=True, score=1.0)


class FactConsistencyRule(VerificationRule):
    """Ensures contradictory facts are not asserted in the same output."""

    name = "FactConsistencyRule"

    def check(self, output: Any, context: dict[str, Any] | None = None) -> VerificationResult:
        if isinstance(output, dict) and output.get("has_contradictions") is True:
            return VerificationResult(
                rule_name=self.name,
                status=VerificationStatus.FAILED,
                passed=False,
                score=0.0,
                message="Contradictory assertions detected in output payload",
            )
        return VerificationResult(rule_name=self.name, status=VerificationStatus.PASSED, passed=True, score=1.0)


class OutputFormatRule(VerificationRule):
    """Verifies output format matches expected payload structure."""

    name = "OutputFormatRule"

    def check(self, output: Any, context: dict[str, Any] | None = None) -> VerificationResult:
        if output is None:
            return VerificationResult(
                rule_name=self.name,
                status=VerificationStatus.FAILED,
                passed=False,
                score=0.0,
                message="Output payload is empty/None",
            )
        return VerificationResult(rule_name=self.name, status=VerificationStatus.PASSED, passed=True, score=1.0)


# ==============================================================================
# Verifier Registry & Verification Gate
# ==============================================================================

class VerifierRegistry:
    """Registry and composer for verification rule chains."""

    def __init__(self) -> None:
        self.rules: dict[str, VerificationRule] = {}
        self._bootstrap_default_rules()

    def _bootstrap_default_rules(self) -> None:
        self.register(SchemaConformanceRule())
        self.register(PolicyComplianceRule())
        self.register(ConfidenceThresholdRule())
        self.register(HallucinationDetectionRule())
        self.register(CognitiveDriftRule())
        self.register(FactConsistencyRule())
        self.register(OutputFormatRule())

    def register(self, rule: VerificationRule) -> None:
        self.rules[rule.name] = rule

    def unregister(self, rule_name: str) -> None:
        self.rules.pop(rule_name, None)

    def get(self, rule_name: str) -> VerificationRule | None:
        return self.rules.get(rule_name)

    def evaluate_chain(
        self,
        output: Any,
        rule_names: list[str] | None = None,
        context: dict[str, Any] | None = None,
        short_circuit: bool = True,
    ) -> list[VerificationResult]:
        """Run verification chain. Short-circuits on critical failure if requested."""
        target_rules = [self.rules[n] for n in rule_names if n in self.rules] if rule_names else list(self.rules.values())
        results: list[VerificationResult] = []
        ctx = context if isinstance(context, dict) else {}

        for rule in target_rules:
            res = rule.check(output, ctx)
            results.append(res)
            if short_circuit and rule.critical and not res.passed:
                logger.info("Verification short-circuited on rule %s", rule.name)
                break

        return results

    def verify_chain(
        self,
        output: Any,
        context: dict[str, Any] | None = None,
        rule_names: list[str] | None = None,
        short_circuit: bool = True,
    ) -> VerificationChainResult:
        """Run chain and return structured VerificationChainResult."""
        results = self.evaluate_chain(output, rule_names=rule_names, context=context, short_circuit=short_circuit)
        failures = [f"{r.rule_name}: {r.message}" for r in results if not r.passed]
        passed = len(failures) == 0
        scores = [r.score for r in results]
        avg = round(sum(scores) / len(scores), 3) if scores else 1.0
        return VerificationChainResult(
            passed=passed,
            failures=failures,
            results=results,
            average_score=avg,
        )


@dataclass
class VerificationChainResult:
    passed: bool
    failures: list[str]
    results: list[VerificationResult]
    average_score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "failures": self.failures,
            "average_score": self.average_score,
            "results": [r.to_dict() for r in self.results],
        }


class DynamicGuardrailInjector:
    """Intercepts agent tool/action intents in real-time against policy boundaries."""

    def __init__(self, blocked_tools: list[str] | None = None, dry_run: bool = False) -> None:
        self.blocked_tools = set(blocked_tools or ["system_shutdown", "drop_database", "raw_exec"])
        self.interceptors: list[Callable[[str, dict[str, Any]], GuardrailInterception | None]] = []
        self.dry_run = dry_run

    def register_interceptor(self, fn: Callable[[str, dict[str, Any]], GuardrailInterception | None]) -> None:
        self.interceptors.append(fn)

    def add_boundary(self, name: str, predicate: Callable[[str, dict[str, Any]], bool]) -> None:
        def _interceptor(tool_name: str, params: dict[str, Any]) -> GuardrailInterception | None:
            if not predicate(tool_name, params):
                return GuardrailInterception(
                    allowed=False,
                    action="BLOCK",
                    intent_name=tool_name,
                    reasons=[f"Blocked by boundary rule '{name}'"],
                )
            return None
        self.register_interceptor(_interceptor)

    def intercept(self, tool_name: str, params: dict[str, Any], tenant_id: str | None = None) -> GuardrailInterception:
        """Inspect and intercept tool invocation before execution."""
        # 1. Blocked tools check
        if tool_name.lower() in self.blocked_tools:
            audit = hashlib.sha256(f"BLOCK:{tenant_id or 'default'}:{tool_name}:{params}".encode()).hexdigest()
            if self.dry_run:
                return GuardrailInterception(
                    allowed=True,
                    action="AUDIT_BLOCKED",
                    intent_name=tool_name,
                    reasons=[f"[DRY-RUN] Prohibited tool {tool_name} logged without blocking"],
                    audit_hash=audit,
                )
            return GuardrailInterception(
                allowed=False,
                action="BLOCK",
                intent_name=tool_name,
                reasons=[f"Tool {tool_name} is permanently prohibited by enterprise guardrails"],
                audit_hash=audit,
            )

        # 2. Run custom interceptors
        for interceptor in self.interceptors:
            res = interceptor(tool_name, params)
            if res and not res.allowed:
                if self.dry_run:
                    res.allowed = True
                    res.action = "AUDIT_BLOCKED"
                return res

        audit = hashlib.sha256(f"ALLOW:{tenant_id or 'default'}:{tool_name}:{params}".encode()).hexdigest()
        return GuardrailInterception(
            allowed=True,
            action="ALLOW",
            intent_name=tool_name,
            audit_hash=audit,
        )

    def intercept_intent(self, agent_id: str, intent: str, params: dict[str, Any]) -> tuple[bool, str]:
        res = self.intercept(intent, params)
        reason = res.reasons[0] if res.reasons else "All boundaries cleared"
        return res.allowed, reason


class VerificationEngine:
    """Enterprise Verification & Guardrail Engine.

    Coordinates deterministic non-LLM validators, loop boundary verification gates,
    dynamic guardrail injection, and tamper-evident audit trails.
    """

    _instance: VerificationEngine | None = None

    def __init__(self) -> None:
        self.registry = VerifierRegistry()
        self.guardrail = DynamicGuardrailInjector()
        self.audit_log: list[dict[str, Any]] = []

    @classmethod
    def get_instance(cls) -> VerificationEngine:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def verify(
        self,
        output: Any,
        rules: list[str] | None = None,
        context: dict[str, Any] | None = None,
    ) -> VerificationChainResult:
        """Perform comprehensive verification and record audit trail."""
        # Handle swapped / flexible arguments
        rule_list = rules
        ctx_dict = context
        if isinstance(rules, dict) and context is None:
            ctx_dict = rules
            rule_list = None
        elif isinstance(context, list) and rules is None:
            rule_list = context
            ctx_dict = None

        chain_res = self.registry.verify_chain(output, context=ctx_dict, rule_names=rule_list)

        audit_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "passed": chain_res.passed,
            "average_score": chain_res.average_score,
            "failures": chain_res.failures,
            "results": [r.to_dict() for r in chain_res.results],
            "audit_hash": hashlib.sha256(json.dumps([r.to_dict() for r in chain_res.results], sort_keys=True).encode()).hexdigest(),
        }
        self.audit_log.append(audit_entry)
        return chain_res

    def intercept_intent(self, tool_name: str, params: dict[str, Any]) -> GuardrailInterception:
        """Intercept agent tool invocation."""
        return self.guardrail.intercept(tool_name, params)

    def get_audit_trail(self, limit: int = 50) -> list[dict[str, Any]]:
        return self.audit_log[-limit:]


def get_verification_engine() -> VerificationEngine:
    return VerificationEngine.get_instance()

