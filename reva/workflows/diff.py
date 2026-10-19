"""Graph version difference and semantic changelog calculation (T-702 / GD-001..005)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from reva.core.ids import diff_id as compute_diff_id


@dataclass
class ElementDiff:
    entity_id: str
    change_type: str  # added | removed | modified | unchanged
    label: str
    old_properties: Dict[str, Any] = field(default_factory=dict)
    new_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VersionDiffResult:
    diff_id: str
    tenant_id: str
    from_commit: str
    to_commit: str
    added_count: int
    removed_count: int
    modified_count: int
    element_diffs: List[ElementDiff] = field(default_factory=list)


def compute_version_diff(
    tenant_id: str,
    from_commit: str,
    to_commit: str,
    elements_v1: Dict[str, Dict[str, Any]],  # entity_id -> {label, properties}
    elements_v2: Dict[str, Dict[str, Any]],
) -> VersionDiffResult:
    """Compare graph elements across commits and categorize semantic mutations."""
    diffs: List[ElementDiff] = []
    added = 0
    removed = 0
    modified = 0

    all_keys = set(elements_v1.keys()).union(set(elements_v2.keys()))

    for eid in sorted(list(all_keys)):
        if eid not in elements_v1:
            added += 1
            diffs.append(
                ElementDiff(
                    entity_id=eid,
                    change_type="added",
                    label=elements_v2[eid].get("label", "unknown"),
                    new_properties=elements_v2[eid].get("properties", {}),
                )
            )
        elif eid not in elements_v2:
            removed += 1
            diffs.append(
                ElementDiff(
                    entity_id=eid,
                    change_type="removed",
                    label=elements_v1[eid].get("label", "unknown"),
                    old_properties=elements_v1[eid].get("properties", {}),
                )
            )
        else:
            p1 = elements_v1[eid].get("properties", {})
            p2 = elements_v2[eid].get("properties", {})
            if p1 != p2:
                modified += 1
                diffs.append(
                    ElementDiff(
                        entity_id=eid,
                        change_type="modified",
                        label=elements_v2[eid].get("label", "unknown"),
                        old_properties=p1,
                        new_properties=p2,
                    )
                )

    d_id = compute_diff_id({
        "added": added,
        "from_commit": from_commit,
        "modified": modified,
        "removed": removed,
        "tenant_id": tenant_id,
        "to_commit": to_commit,
    })

    return VersionDiffResult(
        diff_id=d_id,
        tenant_id=tenant_id,
        from_commit=from_commit,
        to_commit=to_commit,
        added_count=added,
        removed_count=removed,
        modified_count=modified,
        element_diffs=diffs,
    )
