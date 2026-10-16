"""Upgrade planner (requirements §47 / GAP-OPS-002).

Given a current and target version, produces a structured upgrade plan
document: pre-checks, migration steps classified via the ontology semantic
diff machinery (``eoip.ontology.gitops``), and a rollback note. Deterministic —
no network or LLM involvement.
"""

from __future__ import annotations

import re
from typing import Any

_VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

_BREAKING_CHANGE_TYPES = {"label_removed", "property_removed", "edge_removed"}


def _parse_version(version: str) -> tuple[int, int, int] | None:
    match = _VERSION_RE.match(version.strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def _classify_changes(diff: dict[str, Any]) -> list[dict[str, Any]]:
    """Map ontology semantic-diff output onto migration-step severities."""
    steps = []
    for change in diff.get("changes", []):
        ctype = change.get("change_type", "")
        severity = "breaking" if ctype in _BREAKING_CHANGE_TYPES else "safe"
        steps.append(
            {
                "id": f"urn:eoip:ops:migration-step:{change.get('subject', 'unknown')}:{ctype}",
                "change_type": ctype,
                "subject": change.get("subject", ""),
                "detail": change.get("detail", ""),
                "severity": severity,
            }
        )
    return steps


def plan_upgrade(
    current_version: str,
    target_version: str,
    *,
    current_manifest: dict[str, Any] | None = None,
    target_manifest: dict[str, Any] | None = None,
    graph_store: Any = None,
) -> dict[str, Any]:
    """Produce an upgrade plan document (§47).

    When ontology manifests are supplied, migration steps are classified by
    reusing ``eoip.ontology.gitops.diff_manifests``. ``graph_store`` may be
    any object with ``health()`` / ``ping()`` for the reachability pre-check.
    """
    current_parsed = _parse_version(current_version)
    target_parsed = _parse_version(target_version)

    prechecks: list[dict[str, Any]] = []

    if current_parsed is None:
        prechecks.append({"name": "current_version", "status": "fail", "detail": f"unparseable version {current_version!r}"})
    if target_parsed is None:
        prechecks.append({"name": "target_version", "status": "fail", "detail": f"unparseable version {target_version!r}"})

    if current_parsed and target_parsed:
        if target_parsed <= current_parsed:
            prechecks.append(
                {
                    "name": "version_order",
                    "status": "fail",
                    "detail": f"target {target_version} is not newer than current {current_version}",
                }
            )
        else:
            prechecks.append(
                {
                    "name": "version_order",
                    "status": "pass",
                    "detail": f"{current_version} -> {target_version} is a forward upgrade",
                }
            )

    if graph_store is not None:
        try:
            healthy = graph_store.health() if hasattr(graph_store, "health") else bool(graph_store.ping())
            prechecks.append(
                {
                    "name": "graph_store",
                    "status": "pass" if healthy else "fail",
                    "detail": "graph store reachable" if healthy else "graph store unhealthy",
                }
            )
        except Exception as exc:  # noqa: BLE001
            prechecks.append({"name": "graph_store", "status": "fail", "detail": f"unreachable: {exc}"})
    else:
        prechecks.append({"name": "graph_store", "status": "warn", "detail": "reachability not verified"})

    diff_summary: dict[str, Any] = {}
    steps: list[dict[str, Any]] = []
    if current_manifest is not None and target_manifest is not None:
        from eoip.ontology.gitops import diff_manifests

        diff = diff_manifests(current_manifest, target_manifest).to_dict()
        diff_summary = {
            "safe": diff.get("safe", True),
            "breaking_count": diff.get("breaking_count", 0),
            "total_changes": len(diff.get("changes", [])),
        }
        steps = _classify_changes(diff)
    else:
        prechecks.append(
            {
                "name": "ontology_diff",
                "status": "warn",
                "detail": "manifests not provided; migration steps limited to version bump",
            }
        )

    blocking = any(p["status"] == "fail" for p in prechecks)
    rollback_note = (
        f"Rollback: redeploy version {current_version} and restore the pre-upgrade "
        "graph snapshot taken immediately before cutover; ontology changes with "
        "severity 'breaking' require snapshot restore to undo."
    )

    return {
        "id": f"urn:eoip:ops:upgrade-plan:{current_version}-to-{target_version}",
        "current_version": current_version,
        "target_version": target_version,
        "prechecks": prechecks,
        "prechecks_ok": not blocking,
        "ontology_diff": diff_summary,
        "migration_steps": steps,
        "rollback_note": rollback_note,
    }
