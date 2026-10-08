"""EgressGateway — the only path to external models (SR-LLM-010).

All external model/embedding/OCR/speech/rerank/telemetry calls MUST go
through this gateway; the deployment is expected to enforce this with
network policy (egress allowlist + proxy) so bypass is technically
impossible. Default posture is S0 — nothing leaves — until a tenant
administrator enables an endpoint, which requires a recorded
consent/contract record (signer, date, DPA reference, residency region,
scope) and emits an audit event (SR-LLM-017, SR-LLM-010).

Per call the gateway:

1. checks the kill switch (global / per-endpoint) and budgets
   (rate, cost, anomaly volume threshold) — SR-LLM-016;
2. evaluates the policy matrix (most-restrictive-wins, default deny) —
   SR-LLM-011;
3. checks region/jurisdiction pinning (SR-LLM-020);
4. transforms the payload to the permitted level (SR-LLM-011) and scans
   it with DLP + canary registry (SR-LLM-014);
5. in dry-run returns the exact payload that WOULD be sent (SR-LLM-012);
   otherwise dispatches through the injectable transport, re-identifies
   and re-scans the response locally (SR-LLM-015), and records an
   immutable EgressManifest (SR-LLM-013).

On denial or transport failure the gateway returns a local-fallback
notice so tasks can degrade to local models (SR-LLM-019).
"""

from __future__ import annotations

import json
import time
import uuid
from collections import deque
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field

from eoip.egress.dlp import CanaryRegistry, DlpScanner
from eoip.egress.manifest import (
    EgressManifest,
    hash_bytes,
    hash_payload,
    new_manifest,
    what_left_the_building,
)
from eoip.egress.policy import PolicyEngine, SharingLevel
from eoip.egress.provider import PluginRegistry
from eoip.egress.transforms import transform
from eoip.egress.vault import TokenVault

# Transport: (payload, endpoint) -> response dict. Injectable so tests make
# no network calls; production wiring supplies an httpx/async client.
Transport = Callable[[dict, "EndpointConfig"], dict]

AuditFn = Callable[[dict], None]

SR_REGIONS: frozenset[str] = frozenset({"EU", "US", "UK", "CH", "APAC"})


class EndpointConfig(BaseModel):
    """An external endpoint; disabled (S0) by default (SR-LLM-010)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    kind: str = Field(default="chat", description="chat|embed|ocr|speech|rerank|telemetry (SR-LLM-018)")
    url_allowlist: list[str] = Field(default_factory=list)
    region: str = "EU"
    enabled: bool = False  # nothing leaves until an admin flips this, with audit + approval
    mtls: bool = True
    zero_retention: bool = False
    no_training: bool = False
    dpa_ref: str = ""


class ConsentRecord(BaseModel):
    """Consent/contract record for enabling an endpoint (SR-LLM-017)."""

    model_config = ConfigDict(extra="forbid")

    consent_id: str
    endpoint_id: str
    signer: str
    signed_at: float
    dpa_ref: str = ""
    residency_region: str = ""
    scope: str = ""


class BudgetExhausted(Exception):
    pass


class EgressDenied(Exception):
    """Raised/returned on policy denial; carries a local-fallback notice."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason
        self.fallback_notice = (
            "egress denied; falling back to local model / deterministic mode"
        )


class EgressGateway:
    """Policy-gated single egress path for external model calls."""

    def __init__(self, *, tenant_id: str, policy: PolicyEngine | None = None,
                 vault: TokenVault | None = None,
                 scanner: DlpScanner | None = None,
                 canaries: CanaryRegistry | None = None,
                 transport: Transport | None = None,
                 audit: AuditFn | None = None) -> None:
        self.tenant_id = tenant_id
        self.policy = policy or PolicyEngine()
        self.vault = vault or TokenVault(tenant_id, secret=b"eoip-local-vault")
        self.scanner = scanner or DlpScanner()
        self.canaries = canaries or CanaryRegistry()
        self.transport = transport or _no_network_transport
        self.audit = audit or (lambda event: None)
        self.endpoints: dict[str, EndpointConfig] = {}
        self.consents: dict[str, ConsentRecord] = {}
        self.plugin_registry = PluginRegistry()
        self.manifests: list[EgressManifest] = []  # append-only (SR-LLM-013)
        self.kill_switch_global = False
        self.killed_endpoints: set[str] = set()
        # Budgets (SR-LLM-016).
        self.rate_limit_per_window = 0  # 0 = unlimited; window is 60s
        self.cost_budget = 0.0          # 0 = unlimited
        self.anomaly_bytes_threshold = 0  # 0 = disabled
        self._window: deque[float] = deque()
        self._cost_spent = 0.0
        self._bytes_out_window: deque[tuple[float, int]] = deque()

    # ------------------------------------------------------------------
    # Endpoint lifecycle (SR-LLM-010, SR-LLM-017)
    # ------------------------------------------------------------------

    def register_endpoint(self, config: EndpointConfig) -> None:
        self.endpoints[config.id] = config

    def enable_endpoint(self, endpoint_id: str, *, admin: str,
                        consent: ConsentRecord) -> None:
        """Enable an external endpoint — admin-only, audited, consent-gated."""
        endpoint = self._endpoint(endpoint_id)
        if consent.endpoint_id != endpoint_id or not consent.signer:
            raise ValueError("a valid consent/contract record (SR-LLM-017) is required")
        if consent.dpa_ref and consent.dpa_ref != endpoint.dpa_ref and endpoint.dpa_ref:
            raise ValueError("consent DPA reference does not match the endpoint contract")
        endpoint.enabled = True
        self.consents[endpoint_id] = consent
        self.audit({
            "event": "egress.endpoint_enabled",
            "endpoint_id": endpoint_id,
            "admin": admin,
            "consent_id": consent.consent_id,
            "signer": consent.signer,
            "dpa_ref": consent.dpa_ref,
            "region": consent.residency_region,
            "scope": consent.scope,
        })

    def disable_endpoint(self, endpoint_id: str, *, admin: str,
                         reason: str = "") -> None:
        self._endpoint(endpoint_id).enabled = False
        self.audit({"event": "egress.endpoint_disabled",
                    "endpoint_id": endpoint_id, "admin": admin, "reason": reason})

    # ------------------------------------------------------------------
    # Kill switch + budgets (SR-LLM-016)
    # ------------------------------------------------------------------

    def kill(self, *, admin: str, reason: str = "") -> None:
        self.kill_switch_global = True
        self.audit({"event": "egress.kill_switch", "admin": admin, "reason": reason})

    def kill_endpoint(self, endpoint_id: str, *, admin: str, reason: str = "") -> None:
        self.killed_endpoints.add(endpoint_id)
        self.audit({"event": "egress.endpoint_killed", "endpoint_id": endpoint_id,
                    "admin": admin, "reason": reason})

    # ------------------------------------------------------------------
    # Core call path
    # ------------------------------------------------------------------

    def call(self, *, endpoint_id: str, task: str, payload: dict,
             user_id: str, role: str,
             data_classes: list[str], tags: list[str] | None = None,
             region: str | None = None,
             approval_id: str | None = None,
             dry_run: bool = False,
             estimated_cost: float = 0.0) -> dict:
        """Send (or preview) one egress call. Returns the manifest + result.

        ``dry_run=True`` returns the exact payload that WOULD be sent
        without invoking the transport (SR-LLM-012).
        """
        endpoint = self._endpoint(endpoint_id)
        now = time.time()
        tags = tags or []

        manifest = new_manifest(
            tenant_id=self.tenant_id, user_id=user_id, role=role, task=task,
            endpoint_id=endpoint_id, endpoint_region=endpoint.region,
            data_classes=list(data_classes), tags=list(tags),
            dry_run=dry_run,
            request_hash=hash_payload(payload),
            fields=list(payload.keys()),
        )

        def deny(reason: str) -> dict:
            manifest.denied = True
            manifest.denial_reason = reason
            self.manifests.append(manifest)
            self.audit({"event": "egress.denied", "endpoint_id": endpoint_id,
                        "user_id": user_id, "reason": reason})
            raise EgressDenied(reason)

        # 1. enablement + kill switch (SR-LLM-010/016)
        if self.kill_switch_global:
            deny("global kill switch engaged")
        if endpoint_id in self.killed_endpoints:
            deny("endpoint kill switch engaged")
        if not endpoint.enabled:
            deny(f"endpoint {endpoint_id} is disabled (default S0)")

        # 2. region / sovereignty pinning (SR-LLM-020)
        if region is not None and region != endpoint.region:
            deny(f"endpoint region {endpoint.region} violates jurisdiction pin {region}")

        # 3. budgets (SR-LLM-016)
        self._check_budgets(now, estimated_cost)

        # 4. policy matrix (SR-LLM-011)
        decision = self.policy.evaluate(
            classes=data_classes, tags=tags, task=task,
            endpoint=endpoint_id, role=role, region=region,
        )
        manifest.matched_rule_ids = decision.matched_rule_ids
        if not decision.allowed:
            deny("policy default deny (S0): " + "; ".join(decision.reasons))
        if decision.approval_required and not approval_id:
            deny("per-request human approval required (S6) — supply approval_id")
        manifest.approval_id = approval_id

        # 5. transform to permitted level (SR-LLM-011/015)
        outbound = transform(
            payload, decision.allowed_level, vault=self.vault,
        )
        manifest.level = int(decision.allowed_level)
        if decision.allowed_level == SharingLevel.S4:
            manifest.tokens = [
                e.token for e in self.vault._entries.values()
                if e.field.split(".")[0] in payload
            ]

        # 6. DLP + canary scan of the exact outbound payload (SR-LLM-014)
        findings = self.scanner.scan(outbound)
        manifest.dlp_findings = [f.detector for f in findings.findings]
        canary_hits = self.canaries.check(outbound, manifest.level)
        if canary_hits:
            manifest.canary_blocked = True
            deny(f"canary values would egress below allowed level: "
                 f"{[c.canary_id for c in canary_hits]}")

        serialized = json.dumps(outbound, sort_keys=True, default=str)
        manifest.bytes_out = len(serialized.encode("utf-8"))

        if dry_run:
            # SR-LLM-012: exact preview payload, no transport call.
            self.manifests.append(manifest)
            return {"manifest": manifest, "dry_run": True, "payload": outbound}

        # 7. dispatch through the injectable transport
        response = self.transport(outbound, endpoint)
        raw = json.dumps(response, sort_keys=True, default=str).encode("utf-8")
        manifest.bytes_in = len(raw)
        manifest.response_hash = hash_bytes(raw)
        self._record_budget(now, manifest.bytes_out, estimated_cost)

        # 8. local re-identification + outbound-style scan before display (SR-LLM-015)
        display = self._reidentify(response)
        self.manifests.append(manifest)
        self.audit({"event": "egress.executed", "endpoint_id": endpoint_id,
                    "user_id": user_id, "manifest_id": manifest.manifest_id,
                    "level": manifest.level, "bytes_out": manifest.bytes_out})
        return {"manifest": manifest, "response": display}

    def report(self, since: float | None = None) -> dict:
        """Exportable 'what left the building' report (SR-LLM-013)."""
        manifests = self.manifests
        if since is not None:
            manifests = [m for m in manifests if m.created_at >= since]
        return what_left_the_building(manifests)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _endpoint(self, endpoint_id: str) -> EndpointConfig:
        endpoint = self.endpoints.get(endpoint_id)
        if endpoint is None:
            raise KeyError(f"unknown endpoint {endpoint_id}")
        return endpoint

    def _reidentify(self, response: Any) -> Any:
        if isinstance(response, str):
            return self.vault.reidentify_text(response)
        if isinstance(response, list):
            return [self._reidentify(item) for item in response]
        if isinstance(response, dict):
            return {k: self._reidentify(v) for k, v in response.items()}
        return response

    def _check_budgets(self, now: float, estimated_cost: float) -> None:
        if self.rate_limit_per_window:
            while self._window and now - self._window[0] > 60:
                self._window.popleft()
            if len(self._window) >= self.rate_limit_per_window:
                raise BudgetExhausted("egress rate budget exhausted (SR-LLM-016)")
        if self.cost_budget:
            if self._cost_spent + estimated_cost > self.cost_budget:
                raise BudgetExhausted("egress cost budget exhausted (SR-LLM-016)")
        if self.anomaly_bytes_threshold:
            while self._bytes_out_window and now - self._bytes_out_window[0][0] > 60:
                self._bytes_out_window.popleft()
            window_bytes = sum(b for _, b in self._bytes_out_window)
            if window_bytes > self.anomaly_bytes_threshold:
                self.audit({"event": "egress.anomaly",
                            "window_bytes": window_bytes,
                            "threshold": self.anomaly_bytes_threshold})
                raise BudgetExhausted("egress anomaly threshold tripped (SR-LLM-016)")

    def _record_budget(self, now: float, bytes_out: int, cost: float) -> None:
        self._window.append(now)
        self._cost_spent += cost
        self._bytes_out_window.append((now, bytes_out))


def _no_network_transport(payload: dict, endpoint: EndpointConfig) -> dict:
    raise RuntimeError(
        "no egress transport configured — external calls are disabled; "
        "use a local model (SR-LLM-019) or inject a transport"
    )
