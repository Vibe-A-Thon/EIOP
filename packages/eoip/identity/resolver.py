"""Identity resolution (FR-INGEST-002).

Deterministic person identity resolution using email, source ID, and
display name normalization. No LLM inference for identity matching.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResolvedIdentity:
    canonical_key: str
    display_name: str
    email: str | None
    source_system: str
    source_id: str | None
    resolution_method: str


class IdentityResolver:
    def resolve_person(
        self,
        *,
        display_name: str,
        email: str | None = None,
        source_id: str | None = None,
        source_system: str = "unknown",
        record_id: str | None = None,
    ) -> ResolvedIdentity:
        if email:
            key = email.strip().casefold()
            method = "email"
        elif source_id:
            key = str(source_id).strip().casefold()
            method = "source_id"
        else:
            fallback = f"{record_id}:{display_name}" if record_id else display_name
            key = fallback.strip().casefold()
            method = "display_name_fallback"

        return ResolvedIdentity(
            canonical_key=key,
            display_name=display_name,
            email=email,
            source_system=source_system,
            source_id=source_id,
            resolution_method=method,
        )

    def person_canonical_id(self, identity: ResolvedIdentity) -> str:
        return f"urn:eoip:identity:person:{identity.source_system}:{identity.canonical_key}"

    def is_same_person(self, a: ResolvedIdentity, b: ResolvedIdentity) -> bool:
        if a.email and b.email:
            return a.email.strip().casefold() == b.email.strip().casefold()
        return a.canonical_key == b.canonical_key
