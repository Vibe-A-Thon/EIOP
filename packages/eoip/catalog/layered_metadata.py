"""Layered Metadata Architecture with Human Override and Source Conflict Governance (CRA-029.2, CRA-029.6, CRA-029.A).

Three metadata layers:
- Base Layer: Crawler-observed technical truth from source systems.
- Edit Layer: Human curation (business glossary, descriptions, owners, classifications).
- Merged Layer: Effective view computed by documented field-level precedence.

Key Invariants:
- Human curation survives later crawler runs.
- Human overrides CANNOT silently hide changed source truth: when source changes,
  a conflict indicator and drift notification are recorded.
- Reset-to-source restores crawler-observed value atomically.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Optional


@dataclass
class BaseMetadataEntry:
    """Crawler-observed technical metadata from source system."""
    observed_at: str
    source_revision: str
    source_system: str
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class HumanEditEntry:
    """Human curation override."""
    author: str
    edited_at: str
    reason: str
    field_name: str
    curated_value: Any


@dataclass
class FieldConflict:
    """Conflict record when source truth drifts after a human edit."""
    field_name: str
    human_value: Any
    observed_base_value: Any
    drift_observed_at: str
    human_edit_at: str
    human_author: str


@dataclass
class LayeredAssetMetadata:
    """Asset metadata container tracking base, edit, and effective merged layers."""
    asset_id: str
    entity_type: str
    base_layer: Optional[BaseMetadataEntry] = None
    edit_layer: dict[str, HumanEditEntry] = field(default_factory=dict)  # field_name -> edit
    conflicts: dict[str, FieldConflict] = field(default_factory=dict)

    def record_crawl(
        self,
        properties: dict[str, Any],
        source_system: str,
        source_revision: str,
        observed_at: Optional[str] = None,
    ) -> dict[str, Any]:
        """Record crawler-observed base metadata and detect source drift (CRA-029.2, CRA-029.6, CRA-029.A)."""
        ts = observed_at or datetime.now(UTC).isoformat()
        old_base_props = self.base_layer.properties if self.base_layer else {}

        self.base_layer = BaseMetadataEntry(
            observed_at=ts,
            source_revision=source_revision,
            source_system=source_system,
            properties=dict(properties),
        )

        # Detect source drift for fields where a human edit exists (CRA-029.6, CRA-029.A)
        for f_name, edit in self.edit_layer.items():
            new_base_val = properties.get(f_name)
            old_base_val = old_base_props.get(f_name)

            if new_base_val is not None and old_base_val is not None and new_base_val != old_base_val:
                # Source truth has changed since the human edit!
                # Record conflict so human edit does not silently hide changed source truth
                self.conflicts[f_name] = FieldConflict(
                    field_name=f_name,
                    human_value=edit.curated_value,
                    observed_base_value=new_base_val,
                    drift_observed_at=ts,
                    human_edit_at=edit.edited_at,
                    human_author=edit.author,
                )

        return self.effective_view()

    def apply_human_edit(
        self,
        field_name: str,
        curated_value: Any,
        author: str,
        reason: str,
        edited_at: Optional[str] = None,
    ) -> dict[str, Any]:
        """Apply human curation override in EditLayer (CRA-029.2, CRA-029.6)."""
        ts = edited_at or datetime.now(UTC).isoformat()
        self.edit_layer[field_name] = HumanEditEntry(
            author=author,
            edited_at=ts,
            reason=reason,
            field_name=field_name,
            curated_value=curated_value,
        )
        # Clear any prior conflict for this field since human has actively curated it
        self.conflicts.pop(field_name, None)
        return self.effective_view()

    def reset_to_source(self, field_name: str) -> dict[str, Any]:
        """Remove human curation and reset field to crawler-observed base value (CRA-029.2)."""
        self.edit_layer.pop(field_name, None)
        self.conflicts.pop(field_name, None)
        return self.effective_view()

    def effective_view(self) -> dict[str, Any]:
        """Compute merged effective view by precedence: EditLayer overrides BaseLayer (CRA-029.2)."""
        merged_props: dict[str, Any] = {}
        provenance_by_field: dict[str, str] = {}

        # 1. Base layer values
        if self.base_layer:
            for k, v in self.base_layer.properties.items():
                merged_props[k] = v
                provenance_by_field[k] = f"base:{self.base_layer.source_system}:{self.base_layer.source_revision}"

        # 2. Human curation overrides
        for k, edit in self.edit_layer.items():
            merged_props[k] = edit.curated_value
            provenance_by_field[k] = f"edit:{edit.author}:{edit.edited_at}"

        return {
            "asset_id": self.asset_id,
            "entity_type": self.entity_type,
            "effective_properties": merged_props,
            "field_provenance": provenance_by_field,
            "has_conflicts": bool(self.conflicts),
            "conflicts": {
                k: {
                    "human_value": c.human_value,
                    "observed_base_value": c.observed_base_value,
                    "drift_observed_at": c.drift_observed_at,
                    "human_author": c.human_author,
                }
                for k, c in self.conflicts.items()
            },
        }
