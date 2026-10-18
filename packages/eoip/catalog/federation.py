"""External Catalog Federation with ownership and precedence mapping (CRA-009.4).

Integrates external metadata catalogs (OpenMetadata, DataHub, Apache Atlas) through
documented public REST interfaces without blind model duplication, using deterministic
precedence resolution.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso


class CatalogSource(str, Enum):
    EOIP_ONTOLOGY = "eoip_ontology"
    DATAHUB = "datahub"
    OPENMETADATA = "openmetadata"
    APACHE_ATLAS = "apache_atlas"


DEFAULT_CATALOG_PRECEDENCE = [
    CatalogSource.EOIP_ONTOLOGY,
    CatalogSource.DATAHUB,
    CatalogSource.OPENMETADATA,
    CatalogSource.APACHE_ATLAS,
]


@dataclass
class CatalogEntity:
    entity_urn: str
    entity_type: str  # dataset, table, dashboard, pipeline, glossary_term
    name: str
    description: str | None = None
    owner: str | None = None
    tags: list[str] = field(default_factory=list)
    custom_properties: dict[str, Any] = field(default_factory=dict)
    source_catalog: CatalogSource = CatalogSource.OPENMETADATA
    raw_payload: dict[str, Any] = field(default_factory=dict)


class CatalogFederationEngine:
    """Federates and resolves entities across heterogeneous enterprise catalogs with precedence."""

    def __init__(
        self,
        precedence_order: list[CatalogSource] | None = None,
    ) -> None:
        self.precedence = precedence_order or list(DEFAULT_CATALOG_PRECEDENCE)

    def resolve_entity(self, candidates: list[CatalogEntity]) -> CatalogEntity:
        """Resolve conflicting catalog entities using configured precedence order (CRA-009.4)."""
        if not candidates:
            raise ValueError("Candidates list cannot be empty")

        # Sort candidates according to precedence rank (lower index = higher priority)
        def _rank(c: CatalogEntity) -> int:
            try:
                return self.precedence.index(c.source_catalog)
            except ValueError:
                return 999

        sorted_candidates = sorted(candidates, key=_rank)
        primary = sorted_candidates[0]

        # Merge descriptions, tags, and properties across sources when primary is sparse
        merged_tags = set(primary.tags)
        merged_props = dict(primary.custom_properties)
        owner = primary.owner
        description = primary.description

        for secondary in sorted_candidates[1:]:
            merged_tags.update(secondary.tags)
            for k, v in secondary.custom_properties.items():
                if k not in merged_props:
                    merged_props[k] = v
            if not owner and secondary.owner:
                owner = secondary.owner
            if not description and secondary.description:
                description = secondary.description

        return CatalogEntity(
            entity_urn=primary.entity_urn,
            entity_type=primary.entity_type,
            name=primary.name,
            description=description,
            owner=owner,
            tags=sorted(list(merged_tags)),
            custom_properties=merged_props,
            source_catalog=primary.source_catalog,
            raw_payload={
                "federated_from": [c.source_catalog.value for c in sorted_candidates],
                "primary_source": primary.source_catalog.value,
            },
        )

    def to_source_event(self, entity: CatalogEntity) -> SourceEventV2:
        """Convert a federated catalog entity to an EOIP SourceEventV2."""
        payload = {
            "urn": entity.entity_urn,
            "type": entity.entity_type,
            "name": entity.name,
            "description": entity.description,
            "owner": entity.owner,
            "tags": entity.tags,
            "properties": entity.custom_properties,
            "source_catalog": entity.source_catalog.value,
            "provenance": entity.raw_payload,
        }
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()
        event_id = hashlib.sha256(f"catalog:{entity.source_catalog.value}:{entity.entity_urn}:{payload_hash}".encode()).hexdigest()
        captured_at = utc_now_iso()

        permissions = PermissionMetadata(
            visibility="INTERNAL",
            principal_refs=[f"catalog:{entity.source_catalog.value}:reader"],
            inherited_from=f"catalog:{entity.source_catalog.value}",
        )

        return SourceEventV2(
            event_id=event_id,
            source_system=entity.source_catalog.value,
            source_instance_id=f"cat-{entity.source_catalog.value}",
            source_record_id=entity.entity_urn,
            operation="UPSERT",
            source_version=payload_hash,
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=payload_hash,
            permissions=permissions,
            payload=payload,
            metadata={
                "mapper_version": "catalog-federation/1.0",
                "entity_type": entity.entity_type,
                "primary_catalog": entity.source_catalog.value,
            },
        )
