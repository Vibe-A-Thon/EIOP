"""Governance roles registry (SR-GOV-004).

Extends the platform RBAC roles (``eoip.authz.core``) with governance role
metadata: data owners, stewards, custodians, ontology curators, security
admins and auditors. The auditor role carries a read-only, tamper-evident
view flag — auditors can read (including audit trails and compliance
reports) but never mutate; their views are served from the append-only audit
and revision records so what they see cannot be rewritten after the fact.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class GovernanceRole(str, Enum):
    DATA_OWNER = "data_owner"
    STEWARD = "steward"
    CUSTODIAN = "custodian"
    ONTOLOGY_CURATOR = "ontology_curator"
    SECURITY_ADMIN = "security_admin"
    AUDITOR = "auditor"


class RoleDefinition(BaseModel):
    """A governance role definition (SR-GOV-004)."""

    model_config = ConfigDict(extra="forbid")

    role: GovernanceRole
    description: str
    permissions: list[str] = Field(default_factory=list)
    read_only: bool = False
    tamper_evident_view: bool = False


BUILTIN_ROLES: list[RoleDefinition] = [
    RoleDefinition(
        role=GovernanceRole.DATA_OWNER,
        description="Accountable for a data domain's quality, access and lifecycle.",
        permissions=["domain:read", "domain:grant-access", "domain:classify"],
    ),
    RoleDefinition(
        role=GovernanceRole.STEWARD,
        description="Curates and remediates data in a domain under owner policy.",
        permissions=["domain:read", "domain:remediate", "propose:change"],
    ),
    RoleDefinition(
        role=GovernanceRole.CUSTODIAN,
        description="Operates storage, backup and retention for a domain.",
        permissions=["domain:read", "backup:run", "retention:apply"],
    ),
    RoleDefinition(
        role=GovernanceRole.ONTOLOGY_CURATOR,
        description="Reviews and approves ontology/mapping changes (SR-GOV-003).",
        permissions=["ontology:read", "propose:change", "review:change"],
    ),
    RoleDefinition(
        role=GovernanceRole.SECURITY_ADMIN,
        description="Configures authz policies, keys and kill switch.",
        permissions=["authz:manage", "policy:manage", "kill-switch:activate"],
    ),
    RoleDefinition(
        role=GovernanceRole.AUDITOR,
        description="Read-only, tamper-evident view across audit, compliance and graph history (SR-GOV-004).",
        permissions=["audit:read", "compliance:read", "graph:read", "reports:read"],
        read_only=True,
        tamper_evident_view=True,
    ),
]


class RolesRegistry:
    """Lookup for governance role definitions (SR-GOV-004)."""

    def __init__(self, definitions: list[RoleDefinition] | None = None) -> None:
        self._roles: dict[str, RoleDefinition] = {
            d.role.value: d for d in (definitions or BUILTIN_ROLES)
        }

    def get(self, role: str | GovernanceRole) -> RoleDefinition | None:
        key = role.value if isinstance(role, GovernanceRole) else role
        return self._roles.get(key)

    def list(self) -> list[RoleDefinition]:
        return list(self._roles.values())

    def auditor_view(self) -> dict:
        """Describe the auditor's read-only, tamper-evident view (SR-GOV-004)."""
        auditor = self._roles[GovernanceRole.AUDITOR.value]
        return {
            "role": auditor.role.value,
            "read_only": auditor.read_only,
            "tamper_evident": auditor.tamper_evident_view,
            "permissions": auditor.permissions,
            "note": (
                "Auditor views are served from append-only audit/revision "
                "records; no mutation endpoints are exposed to this role."
            ),
        }
