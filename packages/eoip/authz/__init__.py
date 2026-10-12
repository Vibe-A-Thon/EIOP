"""RBAC/ABAC authorization framework (GAP-SEC-001..012, §27, §48).

Framework-agnostic policy-as-code authorization: permission catalog, role
hierarchy, YAML policies with ABAC conditions, an auditable default-deny
enforce function, CRUD+export role/user stores, and stdlib HMAC-SHA256
signed tokens. No FastAPI imports — wire as middleware/dependencies later.
"""

from eoip.authz.core import (
    ADMIN_WILDCARD,
    CLASSIFICATION_ORDER,
    KNOWN_PERMISSIONS,
    ROLE_ADMIN,
    ROLE_ANALYST,
    ROLE_HIERARCHY,
    ROLE_STEWARD,
    ROLE_VIEWER,
    Condition,
    Decision,
    PolicyEnforcer,
    PolicyStatement,
    RoleRegistry,
    User,
    UserStore,
    load_policy_yaml,
    permission_known,
    role_inherited_roles,
    role_rank,
)
from eoip.authz.tokens import (
    TokenError,
    TokenRevocationStore,
    TokenSigner,
    global_revocation_store,
    has_scope,
)

__all__ = [
    "ADMIN_WILDCARD",
    "CLASSIFICATION_ORDER",
    "KNOWN_PERMISSIONS",
    "ROLE_ADMIN",
    "ROLE_ANALYST",
    "ROLE_HIERARCHY",
    "ROLE_STEWARD",
    "ROLE_VIEWER",
    "Condition",
    "Decision",
    "PolicyEnforcer",
    "PolicyStatement",
    "RoleRegistry",
    "TokenError",
    "TokenRevocationStore",
    "TokenSigner",
    "User",
    "UserStore",
    "global_revocation_store",
    "has_scope",
    "load_policy_yaml",
    "permission_known",
    "role_inherited_roles",
    "role_rank",
]
