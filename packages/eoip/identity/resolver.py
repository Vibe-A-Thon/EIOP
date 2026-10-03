"""Identity resolution (FR-INGEST-002).

Deterministic person identity resolution using email, source ID, and
display name normalization. No LLM inference for identity matching.
"""

from __future__ import annotations

from dataclasses import dataclass


def person_identity(
    email: str | None, source_system: str, identity: object
) -> tuple[str, str]:
    """Resolve one canonical person identity namespace for ingestion (FR-ID-001).

    Returns (canonical_id, source_alias). When an email is present the person
    keys to the shared ``urn:eoip:identity:person:email`` namespace so the same
    human ingested from different sources becomes ONE Person vertex. Without an
    email the person stays in a deterministic, source-scoped alias namespace —
    no cross-source merge is invented without evidence. The source alias
    (``{source_system}:{casefolded identity}``) is stored on the vertex so the
    contributing source identities remain visible.
    """
    if email:
        key = email.strip().casefold()
        return f"urn:eoip:identity:person:email:{key}", f"{source_system}:{key}"
    key = str(identity).strip().casefold()
    return f"urn:eoip:identity:person:alias:{source_system}:{key}", f"{source_system}:{key}"


def merge_source_aliases(existing: str | None, alias: str) -> str:
    """Comma-merge a new source alias into an existing source_aliases value."""
    merged = {part for part in (existing or "").split(",") if part}
    merged.add(alias)
    return ",".join(sorted(merged))


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
        return person_identity(
            identity.email, identity.source_system, identity.source_id or identity.canonical_key
        )[0]

    def is_same_person(self, a: ResolvedIdentity, b: ResolvedIdentity) -> bool:
        if a.email and b.email:
            return a.email.strip().casefold() == b.email.strip().casefold()
        return a.canonical_key == b.canonical_key
