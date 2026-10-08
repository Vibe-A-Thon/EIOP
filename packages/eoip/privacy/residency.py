"""Data-residency pinning config validation (SR-PRV-006, partial).

A residency policy pins which regions storage, processing, and model
endpoints may run in for a tenant, and which regions data may be
transferred to. ``ResidencyValidator`` checks proposed placements against
the policy; cross-border transfer controls (DPAs, SCCs, transfer impact
assessments) are External gate — legal review workflow outside the
runtime. Runtime *enforcement* (routing decisions in the infra layer)
is ADR-gated; this module is the config + validation layer.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_REGION_RE = __import__("re").compile(r"^[a-z]{2}(?:-[a-z0-9-]+)?$")


class ResidencyAspect(str, Enum):
    STORAGE = "storage"
    PROCESSING = "processing"
    MODEL_ENDPOINTS = "model_endpoints"


def _check_region(value: str) -> str:
    if not _REGION_RE.match(value):
        raise ValueError(f"invalid region code {value!r} (e.g. 'eu-west-1', 'eu')")
    return value


class RegionSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed: list[str] = Field(min_length=1)

    @field_validator("allowed")
    @classmethod
    def _regions(cls, value: list[str]) -> list[str]:
        for region in value:
            _check_region(region)
        return sorted(set(value))


class ResidencyPolicy(BaseModel):
    """Region constraints per tenant (SR-PRV-006)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:privacy:residency:<slug>")
    tenant_id: str = Field(min_length=1)
    storage: RegionSet
    processing: RegionSet
    model_endpoints: RegionSet
    transfer_regions: list[str] = Field(
        default_factory=list,
        description="Regions data may be transferred to (cross-border transfer control is External gate)",
    )
    deny_regions: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:privacy:residency:"):
            raise ValueError("residency policy id must be urn:eoip:privacy:residency:<slug>")
        return value

    @field_validator("transfer_regions", "deny_regions")
    @classmethod
    def _transfer(cls, value: list[str]) -> list[str]:
        for region in value:
            _check_region(region)
        return sorted(set(value))

    @model_validator(mode="after")
    def _no_overlap(self) -> ResidencyPolicy:
        overlap = set(self.deny_regions) & (set(self.storage.allowed) | set(self.processing.allowed) | set(self.model_endpoints.allowed))
        if overlap:
            raise ValueError(f"deny_regions overlap with allowed regions: {sorted(overlap)}")
        return self

    def allows(self, aspect: ResidencyAspect, region: str) -> bool:
        _check_region(region)
        if region in self.deny_regions:
            return False
        aspect_set = {
            ResidencyAspect.STORAGE: self.storage,
            ResidencyAspect.PROCESSING: self.processing,
            ResidencyAspect.MODEL_ENDPOINTS: self.model_endpoints,
        }[aspect]
        return any(region == allowed or region.startswith(allowed + "-") for allowed in aspect_set.allowed)


class ResidencyViolation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aspect: ResidencyAspect
    region: str
    reason: str


class ResidencyValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str
    valid: bool
    violations: list[ResidencyViolation] = Field(default_factory=list)


class ResidencyValidator:
    """Validates proposed placements against tenant residency policies (SR-PRV-006)."""

    def __init__(self) -> None:
        self._policies: dict[str, ResidencyPolicy] = {}

    def register(self, policy: ResidencyPolicy) -> None:
        self._policies[policy.tenant_id] = policy

    def get(self, tenant_id: str) -> ResidencyPolicy | None:
        return self._policies.get(tenant_id)

    def validate(self, tenant_id: str, placements: dict[ResidencyAspect, str]) -> ResidencyValidation:
        """Check each aspect's proposed region; empty placements = nothing to check."""
        policy = self._policies.get(tenant_id)
        violations: list[ResidencyViolation] = []
        if policy is None:
            if placements:
                violations.append(
                    ResidencyViolation(
                        aspect=next(iter(placements)),
                        region=next(iter(placements.values())),
                        reason="no residency policy registered for tenant",
                    )
                )
            return ResidencyValidation(tenant_id=tenant_id, valid=not violations, violations=violations)
        for aspect, region in placements.items():
            if not policy.allows(aspect, region):
                violations.append(
                    ResidencyViolation(
                        aspect=aspect,
                        region=region,
                        reason=f"region {region!r} not permitted for {aspect.value}",
                    )
                )
        return ResidencyValidation(tenant_id=tenant_id, valid=not violations, violations=violations)
