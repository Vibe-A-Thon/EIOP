"""RBAC/ABAC authorization core (GAP-SEC-001..006, §27, §48).

Framework-agnostic policy-as-code authorization:

- Permission catalog: action x resource strings (e.g. ``graph:read``,
  ``ontology:publish``) with wildcard admin grants (GAP-SEC-001).
- Role hierarchy: viewer < analyst < steward < admin (GAP-SEC-002).
- YAML-loadable policies binding roles to permissions with optional ABAC
  conditions evaluated against target-resource attributes
  (GAP-SEC-003, §27 policy-as-code).
- ``enforce()`` decision function: default-deny, fail-closed, returns an
  auditable decision record with allow/deny and reasons (GAP-SEC-004,
  §48 auditability).
- ``RoleRegistry`` / ``UserStore`` with CRUD and JSON export round-trip
  (GAP-SEC-005, GAP-SEC-006).
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field

import yaml

from eoip.audit.redaction import redact_secrets

# ---------------------------------------------------------------------------
# Permission catalog (GAP-SEC-001)
# ---------------------------------------------------------------------------

ADMIN_WILDCARD = "admin:*"

KNOWN_PERMISSIONS: frozenset[str] = frozenset({
    "graph:read",
    "graph:mutate",
    "ontology:publish",
    "agents:approve",
    ADMIN_WILDCARD,
    "audit:read",
    "policy:manage",
    "user:manage",
})


def permission_known(permission: str) -> bool:
    """Whether a permission string is in the catalog (GAP-SEC-001)."""
    return permission in KNOWN_PERMISSIONS


# ---------------------------------------------------------------------------
# Roles & hierarchy (GAP-SEC-002)
# ---------------------------------------------------------------------------

ROLE_VIEWER = "viewer"
ROLE_ANALYST = "analyst"
ROLE_STEWARD = "steward"
ROLE_ADMIN = "admin"

# Ordered weakest -> strongest; a role inherits all permissions of weaker roles.
ROLE_HIERARCHY: tuple[str, ...] = (ROLE_VIEWER, ROLE_ANALYST, ROLE_STEWARD, ROLE_ADMIN)

CLASSIFICATION_ORDER = ("public", "internal", "confidential", "restricted")


def role_rank(role: str) -> int:
    """Hierarchy rank; higher inherits more. Unknown roles rank below viewer."""
    try:
        return ROLE_HIERARCHY.index(role)
    except ValueError:
        return -1


def role_inherited_roles(role: str) -> list[str]:
    """Roles this role inherits from (weaker-or-equal roles), GAP-SEC-002."""
    rank = role_rank(role)
    if rank < 0:
        return []
    return list(ROLE_HIERARCHY[: rank + 1])


# ---------------------------------------------------------------------------
# Conditions & policies (GAP-SEC-003, §27)
# ---------------------------------------------------------------------------

_SUPPORTED_ATTRS = ("domain", "classification", "source_system")


@dataclass(frozen=True)
class Condition:
    """ABAC condition on a target-resource attribute (GAP-SEC-003).

    ``op`` is ``eq`` or ``in``. An empty value set means the condition
    always matches (i.e. it degenerates to a pure RBAC grant).
    """

    attribute: str
    op: str = "eq"
    value: object = None

    def matches(self, resource_attrs: dict) -> bool:
        if self.attribute not in _SUPPORTED_ATTRS:
            return False
        actual = resource_attrs.get(self.attribute)
        if self.op == "eq":
            return actual == self.value
        if self.op == "in":
            return actual in (self.value or [])
        return False

    def to_dict(self) -> dict:
        return {"attribute": self.attribute, "op": self.op, "value": self.value}

    @classmethod
    def from_dict(cls, data: dict) -> "Condition":
        return cls(attribute=data["attribute"], op=data.get("op", "eq"), value=data.get("value"))


@dataclass(frozen=True)
class PolicyStatement:
    """One policy-as-code statement: role -> permission + ABAC conditions."""

    policy_id: str
    role: str
    permission: str
    conditions: tuple[Condition, ...] = ()
    description: str = ""

    def __post_init__(self) -> None:
        coerced = tuple(
            c if isinstance(c, Condition) else Condition.from_dict(c)
            for c in self.conditions
        )
        object.__setattr__(self, "conditions", coerced)

    def matches(self, role: str, action: str, resource_attrs: dict) -> bool:
        if self.permission != action and self.permission != ADMIN_WILDCARD:
            return False
        if role_rank(role) < role_rank(self.role):
            return False
        return all(c.matches(resource_attrs) for c in self.conditions)

    def to_dict(self) -> dict:
        return {
            "policy_id": self.policy_id,
            "role": self.role,
            "permission": self.permission,
            "conditions": [c.to_dict() for c in self.conditions],
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PolicyStatement":
        return cls(
            policy_id=data["policy_id"],
            role=data["role"],
            permission=data["permission"],
            conditions=tuple(Condition.from_dict(c) for c in data.get("conditions", [])),
            description=data.get("description", ""),
        )


def load_policy_yaml(text: str) -> list[PolicyStatement]:
    """Parse YAML policy-as-code into statements (GAP-SEC-003, §27).

    Expected shape::

        policies:
          - id: steward-publish-internal
            role: steward
            permission: ontology:publish
            conditions:
              - {attribute: classification, op: in, value: [internal, public]}
    """
    data = yaml.safe_load(text) or {}
    raw = data.get("policies", data if isinstance(data, list) else [])
    statements = []
    for entry in raw:
        statements.append(PolicyStatement.from_dict({
            "policy_id": entry.get("id", entry.get("policy_id", "")),
            "role": entry["role"],
            "permission": entry["permission"],
            "conditions": entry.get("conditions", []),
            "description": entry.get("description", ""),
        }))
    return statements


# ---------------------------------------------------------------------------
# Decision (GAP-SEC-004, §48)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Decision:
    """An auditable authorization decision: allow/deny + reasons."""

    allow: bool
    reasons: tuple[str, ...]
    user_id: str
    action: str
    roles: tuple[str, ...]
    policy_id: str | None = None
    decision_id: str = field(default_factory=lambda: f"urn:eoip:authz:decision:{uuid.uuid4()}")
    timestamp: float = field(default_factory=time.time)

    def to_audit_record(self) -> dict:
        """Redacted, JSON-serializable audit record of this decision (§48)."""
        return redact_secrets({
            "event": "authz.decision",
            "decision_id": self.decision_id,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "action": self.action,
            "roles": list(self.roles),
            "allow": self.allow,
            "policy_id": self.policy_id,
            "reasons": list(self.reasons),
        })


# ---------------------------------------------------------------------------
# Enforcer: default-deny, fail-closed (GAP-SEC-004)
# ---------------------------------------------------------------------------


class PolicyEnforcer:
    """Evaluates roles + policies against (action, resource attributes).

    Fail-closed: any evaluation error, unknown action, or unmatched
    statement yields DENY with a reason (GAP-SEC-004).
    """

    def __init__(self, statements: list[PolicyStatement] | None = None) -> None:
        self._statements: list[PolicyStatement] = list(statements or [])

    def add_policy(self, statement: PolicyStatement) -> None:
        self._statements.append(statement)

    def load_yaml(self, text: str) -> int:
        statements = load_policy_yaml(text)
        self._statements.extend(statements)
        return len(statements)

    @property
    def statements(self) -> tuple[PolicyStatement, ...]:
        return tuple(self._statements)

    def enforce(self, user: "User", action: str, resource_attrs: dict | None = None) -> Decision:
        attrs = dict(resource_attrs or {})
        try:
            if not action or ":" not in action:
                return Decision(False, ("deny: malformed action",), user.user_id, action, tuple(user.roles))
            matched = None
            for stmt in self._statements:
                for role in user.roles:
                    if stmt.matches(role, action, attrs):
                        # Most specific (highest-role) statement wins on ties.
                        if matched is None or role_rank(stmt.role) > role_rank(matched.role):
                            matched = stmt
                        break
            if matched is not None:
                return Decision(
                    True,
                    (f"allow: policy {matched.policy_id} grants {matched.permission} to role {matched.role}",),
                    user.user_id, action, tuple(user.roles), policy_id=matched.policy_id,
                )
            return Decision(
                False,
                (f"deny: no policy grants {action} for roles {sorted(user.roles)} with attributes {sorted(attrs)}",),
                user.user_id, action, tuple(user.roles),
            )
        except Exception as exc:  # fail-closed (GAP-SEC-004)
            return Decision(
                False,
                (f"deny: evaluation error (fail-closed): {type(exc).__name__}",),
                user.user_id, action, tuple(user.roles),
            )


# ---------------------------------------------------------------------------
# Users & roles storage with JSON export (GAP-SEC-005, GAP-SEC-006)
# ---------------------------------------------------------------------------


@dataclass
class User:
    user_id: str
    roles: list[str]
    attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"user_id": self.user_id, "roles": list(self.roles), "attributes": dict(self.attributes)}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(user_id=data["user_id"], roles=list(data.get("roles", [])), attributes=dict(data.get("attributes", {})))


def _stable_id(area: str, type_: str, id_: str) -> str:
    return f"urn:eoip:{area}:{type_}:{id_}"


class RoleRegistry:
    """CRUD for role definitions + JSON export round-trip (GAP-SEC-005)."""

    def __init__(self) -> None:
        self._roles: dict[str, dict] = {}
        for role in ROLE_HIERARCHY:
            self.create_role(role, description=f"Built-in {role} role")

    def create_role(self, name: str, *, description: str = "", permissions: list[str] | None = None) -> dict:
        if name in self._roles:
            raise ValueError(f"role already exists: {name}")
        for perm in permissions or []:
            if not permission_known(perm):
                raise ValueError(f"unknown permission: {perm}")
        role = {
            "role_id": _stable_id("authz", "role", name),
            "name": name,
            "description": description,
            "permissions": list(permissions or []),
            "inherits": role_inherited_roles(name)[-1] if role_inherited_roles(name)[:-1] else None,
        }
        self._roles[name] = role
        return dict(role)

    def get_role(self, name: str) -> dict | None:
        role = self._roles.get(name)
        return dict(role) if role else None

    def update_role(self, name: str, *, description: str | None = None, permissions: list[str] | None = None) -> dict:
        if name not in self._roles:
            raise KeyError(name)
        if permissions is not None:
            for perm in permissions:
                if not permission_known(perm):
                    raise ValueError(f"unknown permission: {perm}")
            self._roles[name]["permissions"] = list(permissions)
        if description is not None:
            self._roles[name]["description"] = description
        return dict(self._roles[name])

    def delete_role(self, name: str) -> None:
        if name in ROLE_HIERARCHY:
            raise ValueError(f"cannot delete built-in role: {name}")
        del self._roles[name]

    def list_roles(self) -> list[dict]:
        return [dict(r) for r in self._roles.values()]

    def export_json(self) -> str:
        return json.dumps({"roles": self.list_roles()}, sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "RoleRegistry":
        data = json.loads(text)
        reg = cls()
        for role in data.get("roles", []):
            name = role["name"]
            if name in reg._roles:
                reg._roles[name].update({k: v for k, v in role.items() if k != "role_id"})
            else:
                reg._roles[name] = dict(role)
        return reg


class UserStore:
    """CRUD for users + JSON export round-trip (GAP-SEC-006)."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def create_user(self, user_id: str, roles: list[str], attributes: dict | None = None) -> User:
        if user_id in self._users:
            raise ValueError(f"user already exists: {user_id}")
        user = User(user_id=user_id, roles=list(roles), attributes=dict(attributes or {}))
        self._users[user_id] = user
        return user

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def update_user(self, user_id: str, *, roles: list[str] | None = None, attributes: dict | None = None) -> User:
        user = self._users.get(user_id)
        if user is None:
            raise KeyError(user_id)
        if roles is not None:
            user.roles = list(roles)
        if attributes is not None:
            user.attributes = dict(attributes)
        return user

    def delete_user(self, user_id: str) -> None:
        if user_id not in self._users:
            raise KeyError(user_id)
        del self._users[user_id]

    def list_users(self) -> list[User]:
        return list(self._users.values())

    def export_json(self) -> str:
        return json.dumps({"users": [u.to_dict() for u in self._users.values()]}, sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "UserStore":
        store = cls()
        for entry in json.loads(text).get("users", []):
            store._users[entry["user_id"]] = User.from_dict(entry)
        return store
