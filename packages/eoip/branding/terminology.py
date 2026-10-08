"""Tenant terminology rename maps (SR-WL-003, SR-ONT-007).

A tenant may rename canonical ontology concepts for display purposes —
"Service" → "Application", "Incident" → "Case", etc. — WITHOUT changing
the underlying canonical type. Canonical type identifiers stored in the
graph never change; the rename map only affects presentation, query
suggestions, and label rendering.

Both directions are supported:

* ``rename(canonical) -> tenant-facing label`` (rendering)
* ``canonicalize(label) -> canonical type`` (parsing user input)
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TerminologyMap(BaseModel):
    """Rename map for one tenant (SR-ONT-007).

    Keys are canonical ontology type names; values are the tenant-facing
    labels. A tenant may also restyle the AI assistant persona via the
    theme package (SR-WL-003) — that lives in ``branding.theme`` and is
    presentation-only.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:branding:terminology:<tenant>")
    tenant_id: str = Field(min_length=1)
    renames: dict[str, str] = Field(default_factory=dict)

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:branding:terminology:"):
            raise ValueError("terminology id must be urn:eoip:branding:terminology:<slug>")
        return value

    @model_validator(mode="after")
    def _renames_nonempty_and_distinct(self) -> TerminologyMap:
        labels = [v.strip().lower() for v in self.renames.values()]
        if any(not v for v in labels):
            raise ValueError("rename labels must be non-empty")
        if len(set(labels)) != len(labels):
            raise ValueError("rename labels must be distinct per tenant (canonicalize would be ambiguous)")
        return self

    def rename(self, canonical_type: str) -> str:
        """Tenant-facing label for a canonical type (default: unchanged)."""
        return self.renames.get(canonical_type, canonical_type)

    def canonicalize(self, label: str) -> str:
        """Canonical type for a tenant-facing label (default: unchanged)."""
        stripped = label.strip()
        for canonical, tenant_label in self.renames.items():
            if tenant_label.lower() == stripped.lower():
                return canonical
        return label

    def apply(self, canonical_types: list[str]) -> dict[str, str]:
        """Rename a batch of canonical types, preserving canonical keys."""
        return {c: self.rename(c) for c in canonical_types}


class TerminologyRegistry:
    """Per-tenant terminology resolution (SR-WL-003)."""

    def __init__(self) -> None:
        self._maps: dict[str, TerminologyMap] = {}

    def register(self, term_map: TerminologyMap) -> None:
        self._maps[term_map.tenant_id] = term_map

    def get(self, tenant_id: str) -> TerminologyMap:
        return self._maps.get(tenant_id) or TerminologyMap(
            id=f"urn:eoip:branding:terminology:{tenant_id or 'default'}",
            tenant_id=tenant_id or "default",
        )

    def rename(self, tenant_id: str | None, canonical_type: str) -> str:
        return self.get(tenant_id or "").rename(canonical_type)

    def canonicalize(self, tenant_id: str | None, label: str) -> str:
        return self.get(tenant_id or "").canonicalize(label)
