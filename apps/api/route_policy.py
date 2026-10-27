"""Central role policy for mutating HTTP routes (D-roles, deny by default).

Decision D-roles (recorded per area as D-*-04 in the audit kit): read verbs viewer+; write verbs
steward/admin; tenant/system-wide or security-sensitive mutations admin. Every POST/PUT/PATCH/DELETE
route is classified here:

* ``ADMIN``  - security-sensitive or system-wide (config, migrations, recovery, marketplace,
  kill switches, QA evidence, tool registration, learning state ...): admin | system | superadmin.
* ``READ``   - POST used for a read/compute that persists nothing (queries, analytics, search,
  previews, validation, explanation): viewer+.
* ``ANALYST``- personal/sandbox writes (simulations, what-if, suggestion pins, agent queries):
  analyst+.
* anything else: ``WRITE`` - steward+. A new route is therefore steward-only until classified.

Unknown roles rank below viewer and get no mutating access.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from eoip.authz.core import role_rank

ADMIN_ROLES = frozenset({"admin", "system", "superadmin"})
MUTATING = frozenset({"POST", "PUT", "PATCH", "DELETE"})

# Paths always reachable (login / webhook signature-authenticated / logout of own session).
OPEN = (r"/api/v1/auth/login", r"/api/v1/auth/logout", r"/api/v1/auth/sso/.*",
        r"/api/v1/sources/[^/]+/webhooks")

ADMIN = (
    r"/api/v1/admin/.*", r"/api/v1/sources(/.*)?", r"/api/v1/authz/.*", r"/api/v1/security/.*",
    r"/api/v1/tenancy/.*", r"/api/v1/identity/.*", r"/api/v1/graph/merge", r".*/merge",
    r"/api/v1/ontology/gitops/(rollback|package-release|migration).*", r"/api/v1/ontology/import",
    r"/api/v1/marketplace/.*", r"/api/v1/enterprise/snapshots.*",
    r"/api/v1/egress/(endpoints|plugins|policy|kill).*",
    # added by the 2026-10-20 authz sweep
    r"/api/v1/config/(set|import|rollback|bounds|flags|reload-subscribe)",
    r"/api/v1/enterprise/(migrations|chaos|cache|lifecycle|resilience|dlq|webhooks)(/.*)?",
    r"/api/v1/enterprise/feature-flags(/override)?",
    r"/api/v1/governance/(kill-switch|models|templates)(/.*)?",
    r"/api/v1/privacy/dsar/.*", r"/api/v1/privacy/consents",
    r"/api/v1/platform/(recovery|edge|security|tools/register|tools/mcp)(/.*)?",
    r"/api/v1/platform/state/(restore|snapshot)",
    r"/api/v1/(brain|platform)/learning/(load|save|train)", r"/brain/learning/(load|save|train)",
    r"/api/v1/licensing/(verify|meter/record)", r"/api/v1/domain-packs/.*",
    r"/api/v1/qa/(evidence/register|dashboard/test-runs|dashboard/external-gates|mutation-checks)",
    r"/api/v1/systems(/.*)?", r"/api/v1/catalog/products/import",
    r"/api/v1/ingestion/.*", r"/api/processing/v1/.*",
    r"/api/v1/platform/integrations/[^/]+/sync", r"/api/v1/platform/imports/csv",
    r"/api/v1/platform/aiml/tokens/budget", r"/api/v1/platform/token-budget/allocate",
    r"/api/v1/loops/(run|approvals)/.*", r"/api/v1/enterprise/nlconfig/execute",
    r"/api/v1/xai/certify-decision",
)

READ = (
    r"/api/v1/query(/(cost|eql|explain|language|multi-paradigm|nl|what-changed|what-if|why|why-not))?",
    r"/api/v1/query/templates/[^/]+/bind",
    r"/api/v1/graph/(anomalies|bitemporal/.*|blast-radius|centrality/full|cluster|components|convert|"
    r"degree-distribution|diff|k-core|link-prediction|metrics|reverse-impact|shortest-paths|similarity|"
    r"surprises|what-if)",
    r"/api/v1/(impact|lineage|path|neighborhood|traceability|lens/[^/]+)",
    r"/api/v1/(rag|rag/query)", r"/api/v1/retrieval/search", r"/api/v1/search/faceted",
    r"/api/v1/federation/query", r"/api/v1/sparql", r"/api/v1/suggest/?", r"/api/v1/suggest/interpret",
    r"/(api/v1/)?brain/(ask|query|intelligent-query|narrate|llm/(explain|tokenize|embed|generate|stream))",
    r"/api/v1/causal/.*", r"/api/v1/playback/(evidence|stream)", r"/api/v1/process/deviations",
    r"/api/v1/(ontology/diff|ontology/validate/shacl|ontology/gitops/(diff|impact|validate))",
    r"/ontology/validate/shacl", r"/api/v1/conformance/check", r"/api/v1/knowledge/(firewall/inspect|slo)",
    r"/api/v1/privacy/(classify|residency/validate|retention/evaluate)",
    r"/api/v1/reports/render", r"/api/v1/compliance/packs/[^/]+/gap-analysis",
    r"/api/v1/config/(diff|export)", r"/api/v1/enterprise/feature-flags/evaluate",
    r"/api/v1/enterprise/nlconfig/suggest", r"/api/v1/enterprise/correlation/analyze/.*",
    r"/api/v1/enterprise/health/check-all", r"/api/v1/governance/evaluate",
    r"/api/v1/licensing/check-module", r"/api/v1/egress/call",
    r"/api/v1/ingest/profile(/(drift|keys|relationships))?", r"/api/v1/branding/terminology/canonicalize",
    r"/api/v1/engineering/[^/]+", r"/api/v1/evidence/manifest", r"/api/v1/gaps/g2/.*",
    r"/api/v1/ops/(helm-summary|shard-plan|upgrade-plan)", r"/api/v1/qa/inventory/validate",
    r"/api/v1/xai/verify-certificate", r"/api/v1/truth/resolve", r"/api/v1/twin/test-intelligence/select",
    r"/api/v1/platform/(search/query|semantic/search|semantic/hybrid|memory/recall|gateway/query|"
    r"graph-graph/(cross-layer-query|diff)|xai/explain|verification/check|tools/validate-call|"
    r"tools/verify-attestation|prompts/render|routing/classify-and-route|intelligence/analyze|"
    r"aiml/hallucination/check|token-formats/(serialize|deserialize|benchmark)|context/slice-graph|"
    r"embeddings/drift|integrations/[^/]+/health|search/user-context|graph-loop/plan|intelligence/plan)",
    r"/api/v1/agents/(analytics|trace-impact)", r"/api/v1/moonshot/(bitemporal/time-warp|causal/simulate|transpile)",
    r"/api/v1/whatif/plan",
    # REVA (mounted at /api/reva/v1 when REVA_ENABLED): warrant query and closure evaluation are reads;
    # issuing/superseding/retracting warrants, gap edits, contradiction resolution and PD sync are writes.
    r"/api/reva/v1/warrants/query", r"/api/reva/v1/pd/closure/evaluate",
)

ANALYST = (
    r"/api/v1/suggest/pin", r"/api/v1/simulation(s)?(/.*)?", r"/api/v1/whatif/execute",
    r"/api/v1/agents/query", r"/api/v1/agents/[^/]+/runs", r"/api/v1/capsules",
    r"/api/v1/platform/copilot/message", r"/api/v1/platform/notifications/[^/]+/read",
    r"/api/v1/enterprise/learning/feedback", r"/api/v1/platform/aiml/rlhf/preference",
)

_C = {name: re.compile("^(?:" + "|".join(pats) + ")$")
      for name, pats in (("open", OPEN), ("admin", ADMIN), ("read", READ), ("analyst", ANALYST))}


def classify(method: str, path: str) -> str:
    """Return the minimum tier for a request: open | read | analyst | write | admin."""
    if method.upper() not in MUTATING:
        return "read"
    for tier in ("open", "admin", "read", "analyst"):
        if _C[tier].match(path):
            return tier
    return "write"


def allowed(method: str, path: str, roles: Iterable[str]) -> bool:
    roles = set(roles or ())
    tier = classify(method, path)
    if tier == "open":
        return True
    if roles & ADMIN_ROLES:
        return True
    if tier == "admin":
        return False
    rank = max((role_rank(r) for r in roles), default=-1)
    need = {"read": 0, "analyst": 1, "write": 2}[tier]  # viewer=0, analyst=1, steward=2
    return rank >= need
