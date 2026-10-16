"""Moonshot 4: Self-Healing Active Graph Fabric & Autonomous Remediation Agents.

Provides:
- Continuous graph drift and architecture violation detection.
- Closed-loop autonomous remediation generation (Git PR diffs, Terraform HCL fixes, Jira tickets).
- Strict human-in-the-loop approval workflows with R0-R4 risk tiering.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DriftViolation:
    violation_id: str
    rule_id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    title: str
    details: str
    entities_involved: list[str]
    detected_at: float = field(default_factory=time.time)


@dataclass
class RemediationAction:
    action_id: str
    violation_id: str
    action_type: str  # GIT_PR, TERRAFORM_FIX, JIRA_TICKET
    risk_level: str  # R0 (read-only), R1 (safe change), R2 (moderate), R3 (high), R4 (critical)
    title: str
    payload: dict[str, Any]
    status: str = "PENDING_APPROVAL"  # PENDING_APPROVAL, APPROVED, DISPATCHED, REJECTED
    approved_by: str | None = None
    dispatched_at: float | None = None


class GraphDriftDetector:
    """Scans enterprise graph entities and edges for topology and architecture drift."""

    def __init__(self) -> None:
        self.rules: list[dict[str, Any]] = [
            {
                "rule_id": "DRIFT-ARCH-001",
                "severity": "HIGH",
                "title": "Direct Database Call from Frontend Service",
            },
            {
                "rule_id": "DRIFT-SEC-002",
                "severity": "CRITICAL",
                "title": "Unrotated Service Account Credential Exceeds 90 Days",
            },
            {
                "rule_id": "DRIFT-OPS-003",
                "severity": "MEDIUM",
                "title": "Orphan Service Lacks Designated Owner Team",
            },
        ]

    def scan_graph(self, entities: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[DriftViolation]:
        violations: list[DriftViolation] = []

        # Check 1: Orphan services without OWNER edge
        owned_services = {e["from"] for e in edges if e.get("type") in ("OWNED_BY", "MAINTAINED_BY")}
        for ent in entities:
            if ent.get("type") == "Service" and ent["id"] not in owned_services:
                violations.append(
                    DriftViolation(
                        violation_id=f"viol_{uuid.uuid4().hex[:8]}",
                        rule_id="DRIFT-OPS-003",
                        severity="MEDIUM",
                        title="Orphan Service Lacks Designated Owner Team",
                        details=f"Service '{ent['id']}' has no active OWNED_BY edge.",
                        entities_involved=[ent["id"]],
                    )
                )

        # Check 2: Service account credentials age
        now = time.time()
        for ent in entities:
            if ent.get("type") == "ServiceAccount":
                created_at = ent.get("created_at", now)
                days_old = (now - created_at) / (24 * 3600)
                if days_old > 90:
                    violations.append(
                        DriftViolation(
                            violation_id=f"viol_{uuid.uuid4().hex[:8]}",
                            rule_id="DRIFT-SEC-002",
                            severity="CRITICAL",
                            title="Unrotated Service Account Credential Exceeds 90 Days",
                            details=f"Account '{ent['id']}' was created {int(days_old)} days ago without credential rotation.",
                            entities_involved=[ent["id"]],
                        )
                    )

        # Check 3: Direct database edge from UI
        for e in edges:
            if e.get("from_type") == "Frontend" and e.get("to_type") == "Database":
                violations.append(
                    DriftViolation(
                        violation_id=f"viol_{uuid.uuid4().hex[:8]}",
                        rule_id="DRIFT-ARCH-001",
                        severity="HIGH",
                        title="Direct Database Call from Frontend Service",
                        details=f"Frontend '{e['from']}' bypasses API gateway to call Database '{e['to']}'.",
                        entities_involved=[e["from"], e["to"]],
                    )
                )

        return violations


class AutonomousRemediationEngine:
    """Synthesizes verified pull requests, Terraform fixes, and Jira tickets with approval gates."""

    def __init__(self) -> None:
        self.remediations: dict[str, RemediationAction] = {}

    def generate_remediation(self, violation: DriftViolation) -> RemediationAction:
        action_id = f"act_{uuid.uuid4().hex[:8]}"

        if violation.rule_id == "DRIFT-SEC-002":
            # Generate Terraform key rotation fix
            hcl_snippet = f"""
resource "vault_generic_secret" "{violation.entities_involved[0]}_rotation" {{
  path = "secret/{violation.entities_involved[0]}"
  data_json = jsonencode({{
    rotate_policy = "90d"
    auto_rotate   = true
  }})
}}
""".strip()
            action = RemediationAction(
                action_id=action_id,
                violation_id=violation.violation_id,
                action_type="TERRAFORM_FIX",
                risk_level="R2",
                title=f"Automated Credential Rotation for {violation.entities_involved[0]}",
                payload={"target_file": "infra/vault/rotations.tf", "hcl": hcl_snippet},
            )
        elif violation.rule_id == "DRIFT-ARCH-001":
            # Generate Git Pull Request patch
            diff_patch = f"""
--- a/src/api/client.ts
+++ b/src/api/client.ts
@@ -10,3 +10,4 @@
- const dbUrl = "postgres://direct-db:5432/main";
+ const apiUrl = "/api/v1/proxy/entities";
""".strip()
            action = RemediationAction(
                action_id=action_id,
                violation_id=violation.violation_id,
                action_type="GIT_PR",
                risk_level="R3",
                title=f"Route frontend calls through API Gateway for {violation.entities_involved[0]}",
                payload={"branch": "fix/route-through-gateway", "patch": diff_patch},
            )
        else:
            # Generate Jira ticket
            action = RemediationAction(
                action_id=action_id,
                violation_id=violation.violation_id,
                action_type="JIRA_TICKET",
                risk_level="R1",
                title=f"Assign Owner Team to {violation.entities_involved[0]}",
                payload={
                    "issue_type": "Task",
                    "priority": violation.severity,
                    "description": violation.details,
                    "labels": ["governance", "architecture-drift"],
                },
            )

        self.remediations[action_id] = action
        return action

    def approve_action(self, action_id: str, approver: str, approver_role: str) -> RemediationAction:
        if action_id not in self.remediations:
            raise KeyError(f"Remediation action '{action_id}' not found")
        action = self.remediations[action_id]

        # Approval policy based on risk level
        if action.risk_level in ("R3", "R4") and "admin" not in approver_role.lower() and "lead" not in approver_role.lower():
            raise PermissionError(f"High risk action {action.risk_level} requires Admin/Lead approval")

        action.status = "APPROVED"
        action.approved_by = approver
        return action

    def dispatch_action(self, action_id: str) -> dict[str, Any]:
        action = self.remediations.get(action_id)
        if not action:
            raise KeyError(f"Remediation action '{action_id}' not found")
        if action.status != "APPROVED":
            raise RuntimeError(f"Action '{action_id}' cannot be dispatched in status '{action.status}'")

        action.status = "DISPATCHED"
        action.dispatched_at = time.time()
        return {
            "dispatched": True,
            "action_id": action.action_id,
            "action_type": action.action_type,
            "target": action.title,
            "payload": action.payload,
        }
