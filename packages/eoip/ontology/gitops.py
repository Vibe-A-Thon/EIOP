"""Ontology GitOps: semantic diff and CI validation (GAP-GITOPS-001..008).

Compares two ontology manifest snapshots and classifies every change as:

- ``additive`` — new optional vocabulary; existing facts remain valid.
- ``potentially_breaking`` — changed constraints or required properties; review.
- ``breaking`` — removed vocabulary or tightened required properties; existing
  graph facts may violate the new manifest and require a migration plan.

The diff is structural (manifest AST comparison), not a text diff. A manifest
snapshot is a dict of the shape produced by :func:`snapshot_manifest`.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any

ADDITIVE = "additive"
POTENTIALLY_BREAKING = "potentially_breaking"
BREAKING = "breaking"


@dataclass
class SemanticChange:
    change_type: str  # label_added | label_removed | property_added | ...
    subject: str
    detail: str
    classification: str


@dataclass
class SemanticDiff:
    changes: list[SemanticChange] = field(default_factory=list)

    @property
    def breaking(self) -> list[SemanticChange]:
        return [c for c in self.changes if c.classification == BREAKING]

    @property
    def safe(self) -> bool:
        return not self.breaking

    def to_dict(self) -> dict[str, Any]:
        return {
            "safe": self.safe,
            "counts": {
                "total": len(self.changes),
                BREAKING: len(self.breaking),
                POTENTIALLY_BREAKING: len(
                    [c for c in self.changes if c.classification == POTENTIALLY_BREAKING]
                ),
                ADDITIVE: len([c for c in self.changes if c.classification == ADDITIVE]),
            },
            "changes": [asdict(change) for change in self.changes],
        }


def snapshot_manifest(
    vertex_labels: dict[str, tuple[str, list[str], list[str]]],
    edge_labels: dict[str, tuple[list[str], list[str], list[str]]],
    property_keys: dict[str, str],
) -> dict[str, Any]:
    """Capture a manifest in a JSON-serializable snapshot form."""
    return {
        "vertex_labels": {
            name: {"domain": spec[0], "required": sorted(spec[1]), "optional": sorted(spec[2])}
            for name, spec in vertex_labels.items()
        },
        "edge_labels": {
            name: {"out": sorted(spec[0]), "in": sorted(spec[1])}
            for name, spec in edge_labels.items()
        },
        "property_keys": dict(sorted(property_keys.items())),
    }


def current_manifest_snapshot() -> dict[str, Any]:
    from eoip.ontology.manifest import EDGE_LABELS, PROPERTY_KEYS, VERTEX_LABELS

    return snapshot_manifest(VERTEX_LABELS, EDGE_LABELS, PROPERTY_KEYS)


def diff_manifests(old: dict[str, Any], new: dict[str, Any]) -> SemanticDiff:
    """Structural semantic diff between two manifest snapshots."""
    diff = SemanticDiff()

    old_v = old.get("vertex_labels", {})
    new_v = new.get("vertex_labels", {})
    for name in sorted(set(new_v) - set(old_v)):
        diff.changes.append(SemanticChange("vertex_label_added", name, "new vertex label", ADDITIVE))
    for name in sorted(set(old_v) - set(new_v)):
        diff.changes.append(
            SemanticChange("vertex_label_removed", name, "existing graph facts may use it", BREAKING)
        )
    for name in sorted(set(old_v) & set(new_v)):
        o, n = old_v[name], new_v[name]
        for prop in sorted(set(n.get("required", [])) - set(o.get("required", []))):
            diff.changes.append(
                SemanticChange(
                    "required_property_added", f"{name}.{prop}",
                    "existing facts may lack the now-required property",
                    POTENTIALLY_BREAKING,
                )
            )
        for prop in sorted(set(o.get("required", [])) - set(n.get("required", []))):
            diff.changes.append(
                SemanticChange("required_property_removed", f"{name}.{prop}", "relaxed", ADDITIVE)
            )
        if o.get("domain") != n.get("domain"):
            diff.changes.append(
                SemanticChange(
                    "domain_changed", name, f"{o.get('domain')} -> {n.get('domain')}",
                    POTENTIALLY_BREAKING,
                )
            )

    old_e = old.get("edge_labels", {})
    new_e = new.get("edge_labels", {})
    for name in sorted(set(new_e) - set(old_e)):
        diff.changes.append(SemanticChange("edge_label_added", name, "new edge label", ADDITIVE))
    for name in sorted(set(old_e) - set(new_e)):
        diff.changes.append(
            SemanticChange("edge_label_removed", name, "existing edges may use it", BREAKING)
        )
    for name in sorted(set(old_e) & set(new_e)):
        o, n = old_e[name], new_e[name]
        removed_out = sorted(set(o.get("out", [])) - set(n.get("out", [])))
        removed_in = sorted(set(o.get("in", [])) - set(n.get("in", [])))
        if removed_out or removed_in:
            diff.changes.append(
                SemanticChange(
                    "edge_endpoints_narrowed", name,
                    f"removed out={removed_out} in={removed_in}",
                    POTENTIALLY_BREAKING,
                )
            )
        added_out = sorted(set(n.get("out", [])) - set(o.get("out", [])))
        added_in = sorted(set(n.get("in", [])) - set(o.get("in", [])))
        if added_out or added_in:
            diff.changes.append(
                SemanticChange(
                    "edge_endpoints_widened", name, f"added out={added_out} in={added_in}", ADDITIVE
                )
            )

    old_p = old.get("property_keys", {})
    new_p = new.get("property_keys", {})
    for key in sorted(set(new_p) - set(old_p)):
        diff.changes.append(SemanticChange("property_key_added", key, "new property", ADDITIVE))
    for key in sorted(set(old_p) - set(new_p)):
        diff.changes.append(
            SemanticChange("property_key_removed", key, "existing facts may set it", BREAKING)
        )
    for key in sorted(set(old_p) & set(new_p)):
        if old_p[key] != new_p[key]:
            diff.changes.append(
                SemanticChange(
                    "property_type_changed", key, f"{old_p[key]} -> {new_p[key]}",
                    POTENTIALLY_BREAKING,
                )
            )

    return diff


def validate_ontology_change(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """CI gate (GAP-GITOPS-004): pass only when no breaking changes are present."""
    result = diff_manifests(old, new).to_dict()
    result["publishable"] = result["safe"]
    result["verdict"] = "PUBLISH_OK" if result["safe"] else "BREAKING_CHANGE_REFUSED"
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", help="Path to the old manifest snapshot JSON ('-' for current)")
    parser.add_argument("new", help="Path to the new manifest snapshot JSON ('-' for current)")
    args = parser.parse_args(argv)

    def load(path: str) -> dict[str, Any]:
        if path == "-":
            return current_manifest_snapshot()
        return json.loads(open(path, encoding="utf-8").read())

    result = validate_ontology_change(load(args.old), load(args.new))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["publishable"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
