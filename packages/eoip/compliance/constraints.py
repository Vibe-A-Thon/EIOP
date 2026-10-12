"""Compliance-as-Code Graph Constraints Engine (COMPLY-001).

Encodes regulatory rules (GDPR, SOX, HIPAA, SOC2) as continuous graph pattern constraints:
- ComplianceRule: Formal graph constraint pattern definition
- ContinuousMonitor: Evaluates graph store changes against compliance rules
- ViolationReport: Structured findings with severity, blast radius, and actionable remediation
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.compliance.constraints")


class ComplianceSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class ComplianceFramework(str, Enum):
    GDPR = "GDPR"
    SOX = "SOX"
    HIPAA = "HIPAA"
    SOC2 = "SOC2"


@dataclass
class ComplianceViolation:
    rule_id: str
    framework: ComplianceFramework
    severity: ComplianceSeverity
    entity_id: str
    entity_label: str
    message: str
    remediation: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "framework": self.framework.value,
            "severity": self.severity.value,
            "entity_id": self.entity_id,
            "entity_label": self.entity_label,
            "message": self.message,
            "remediation": self.remediation,
            "timestamp": self.timestamp,
        }


@dataclass
class ViolationReport:
    conforms: bool
    total_violations: int
    critical_count: int
    warning_count: int
    violations: list[ComplianceViolation] = field(default_factory=list)
    evaluated_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conforms": self.conforms,
            "total_violations": self.total_violations,
            "critical_count": self.critical_count,
            "warning_count": self.warning_count,
            "violations": [v.to_dict() for v in self.violations],
            "evaluated_at": self.evaluated_at,
        }


class ComplianceRule:
    """Base graph pattern constraint rule."""

    def __init__(
        self,
        rule_id: str,
        framework: ComplianceFramework,
        severity: ComplianceSeverity,
        description: str,
    ) -> None:
        self.rule_id = rule_id
        self.framework = framework
        self.severity = severity
        self.description = description

    def evaluate(self, store: MemoryGraphStore) -> list[ComplianceViolation]:
        raise NotImplementedError


class GDPRRightToErasureRule(ComplianceRule):
    """GDPR Art. 17: Soft-deleted vertices must not have active incoming edges."""

    def __init__(self) -> None:
        super().__init__(
            rule_id="GDPR-001",
            framework=ComplianceFramework.GDPR,
            severity=ComplianceSeverity.CRITICAL,
            description="Entities marked deleted_at must not have active dependent relations",
        )

    def evaluate(self, store: MemoryGraphStore) -> list[ComplianceViolation]:
        violations = []
        for v in store.find_vertices(include_deleted=True):
            props = v.get("properties", {})
            if props.get("deleted_at"):
                cid = props.get("canonical_id", v.get("canonical_id"))
                incoming = store.edges_to(v.get("vid"))
                if incoming:
                    violations.append(
                        ComplianceViolation(
                            rule_id=self.rule_id,
                            framework=self.framework,
                            severity=self.severity,
                            entity_id=cid,
                            entity_label=v["label"],
                            message=f"Entity '{cid}' has deleted_at but still has {len(incoming)} active incoming relations",
                            remediation="Sever or cascade deletion to incoming edges",
                        )
                    )
        return violations


class SOXSegregationOfDutiesRule(ComplianceRule):
    """SOX Section 404: Service and Release changes require separation of author and deployer."""

    def __init__(self) -> None:
        super().__init__(
            rule_id="SOX-001",
            framework=ComplianceFramework.SOX,
            severity=ComplianceSeverity.CRITICAL,
            description="Author of code change must not be the sole approver/deployer",
        )

    def evaluate(self, store: MemoryGraphStore) -> list[ComplianceViolation]:
        violations = []
        for v in store.find_vertices(label="Deployment"):
            props = v.get("properties", {})
            author = props.get("author_name") or props.get("author_id")
            deployer = props.get("actor") or props.get("deployer_id")
            if author and deployer and author == deployer:
                cid = props.get("canonical_id", v.get("canonical_id"))
                violations.append(
                    ComplianceViolation(
                        rule_id=self.rule_id,
                        framework=self.framework,
                        severity=self.severity,
                        entity_id=cid,
                        entity_label="Deployment",
                        message=f"Author '{author}' self-deployed deployment '{cid}' violating segregation of duties",
                        remediation="Require peer review and separate deployment approval",
                    )
                )
        return violations


class HIPAAMinimumNecessaryRule(ComplianceRule):
    """HIPAA Security Rule 45 CFR: Health/PII data stores must declare encryption and access controls."""

    def __init__(self) -> None:
        super().__init__(
            rule_id="HIPAA-001",
            framework=ComplianceFramework.HIPAA,
            severity=ComplianceSeverity.CRITICAL,
            description="Healthcare data stores must explicitly specify encryption at rest",
        )

    def evaluate(self, store: MemoryGraphStore) -> list[ComplianceViolation]:
        violations = []
        for v in store.find_vertices(label="Database"):
            props = v.get("properties", {})
            cid = props.get("canonical_id", v.get("canonical_id"))
            name = str(props.get("name", "")).lower()
            desc = str(props.get("description", "")).lower()
            status = str(props.get("status", "")).lower()
            is_health_data = "health" in name or "phi" in desc or props.get("data_class") == "PHI"
            is_unencrypted = "unencrypted" in desc or status == "unencrypted" or not props.get("encrypted_at_rest", True)
            if is_health_data and is_unencrypted:
                violations.append(
                    ComplianceViolation(
                        rule_id=self.rule_id,
                        framework=self.framework,
                        severity=self.severity,
                        entity_id=cid,
                        entity_label="Database",
                        message=f"Database '{cid}' handles PHI but does not have encrypted_at_rest=True",
                        remediation="Enable KMS/AES-256 encryption at rest",
                    )
                )
        return violations


class SOC2AccessControlRule(ComplianceRule):
    """SOC 2 CC6.1: Production services must declare an active resilience tier."""

    def __init__(self) -> None:
        super().__init__(
            rule_id="SOC2-001",
            framework=ComplianceFramework.SOC2,
            severity=ComplianceSeverity.WARNING,
            description="Critical production services must declare resilience tier",
        )

    def evaluate(self, store: MemoryGraphStore) -> list[ComplianceViolation]:
        violations = []
        for v in store.find_vertices(label="Service"):
            props = v.get("properties", {})
            cid = props.get("canonical_id", v.get("canonical_id"))
            if props.get("criticality") == "CRITICAL" and not props.get("resilience"):
                violations.append(
                    ComplianceViolation(
                        rule_id=self.rule_id,
                        framework=self.framework,
                        severity=self.severity,
                        entity_id=cid,
                        entity_label="Service",
                        message=f"CRITICAL Service '{cid}' missing resilience configuration",
                        remediation="Specify resilience tier (e.g. MULTI_AZ, ACTIVE_ACTIVE)",
                    )
                )
        return violations


class ContinuousMonitor:
    """Continuous Compliance Monitor evaluating graph mutations."""

    def __init__(self) -> None:
        self.rules: list[ComplianceRule] = [
            GDPRRightToErasureRule(),
            SOXSegregationOfDutiesRule(),
            HIPAAMinimumNecessaryRule(),
            SOC2AccessControlRule(),
        ]
        self._lock = threading.Lock()

    def register_rule(self, rule: ComplianceRule) -> None:
        with self._lock:
            self.rules.append(rule)

    def evaluate_compliance(self, store: MemoryGraphStore) -> ViolationReport:
        with self._lock:
            rules_to_run = list(self.rules)

        all_violations: list[ComplianceViolation] = []
        for r in rules_to_run:
            all_violations.extend(r.evaluate(store))

        crit_count = sum(1 for v in all_violations if v.severity == ComplianceSeverity.CRITICAL)
        warn_count = sum(1 for v in all_violations if v.severity == ComplianceSeverity.WARNING)

        return ViolationReport(
            conforms=len(all_violations) == 0,
            total_violations=len(all_violations),
            critical_count=crit_count,
            warning_count=warn_count,
            violations=all_violations,
        )
