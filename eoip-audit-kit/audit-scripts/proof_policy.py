#!/usr/bin/env python3
"""EOIP Audit Kit — Proof Policy 1.1.0 (canonical status computation)."""

from __future__ import annotations

import re
from typing import Any

PROOF_POLICY_VERSION = "1.1.0"
TIER_RANK = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}

STATUSES = (
    "Implemented",
    "Partially Implemented",
    "Not Verified",
    "Not Implemented",
    "Ambiguous",
    "Not Applicable",
)

FAIL_RE = re.compile(r"\b(fail(ed|ure|s)?|error(s)?|conclusion=failure|red)\b", re.I)
PASS_RE = re.compile(r"\b(pass(ed)?|success|ok|green|exit 0|all valid)\b", re.I)


def is_failing(item: dict[str, Any]) -> bool:
    """An L2/L3 item whose actual_result reports failure (and not a 0-failure summary)."""
    ar = item.get("actual_result") or ""
    if re.search(r"\b0 (failed|errors?)\b", ar, re.I) and not re.search(r"\b[1-9]\d* (failed|errors?)\b", ar, re.I):
        return False
    return bool(FAIL_RE.search(ar))


PLACEHOLDER_RE = re.compile(r"\bREPLACE\b|<[a-z][a-z0-9_ -]*>|<reviewer-id|<fix-commit>|<run_id>", re.I)


def is_placeholder(item: dict[str, Any]) -> bool:
    """Unfilled template items (all-zero commit, REPLACE markers, <placeholders>) are never proof."""
    if set((item.get("git_commit") or "x").lower()) == {"0"}:
        return True
    fields = [item.get("actual_result"), item.get("reviewer_id"), item.get("ci_run_id")]
    fields += [ln.get("url") for ln in item.get("links") or []]
    return any(f and PLACEHOLDER_RE.search(str(f)) for f in fields)


def tier_rank(tier: str | None) -> int:
    return TIER_RANK.get(tier or "L0", 0)


def max_tier(items: list[dict[str, Any]]) -> str:
    best = "L0"
    for it in items:
        t = it.get("proof_tier") or "L0"
        if tier_rank(t) > tier_rank(best):
            best = t
    return best


def _active_items(
    items: list[dict[str, Any]],
    audited_commit: str | None,
    bundle_commit: str | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Split evidence into active vs stale. Stale = item/bundle commit ≠ audited."""
    warnings: list[str] = []
    active: list[dict[str, Any]] = []
    stale: list[dict[str, Any]] = []
    ph = [it for it in items if is_placeholder(it)]
    for it in ph:
        warnings.append(f"{it.get('evidence_id', '?')}: TEMPLATE placeholder, ignored as proof")
    items = [it for it in items if not is_placeholder(it)]
    if not audited_commit:
        return list(items), ph, warnings
    audited = audited_commit.lower()
    stale.extend(ph)
    for it in items:
        item_commit = (it.get("git_commit") or bundle_commit or "").lower()
        if item_commit and item_commit != audited:
            stale.append(it)
            warnings.append(
                f"{it.get('evidence_id', '?')}: STALE "
                f"(evidence commit {item_commit[:12]} ≠ audited {audited[:12]})"
            )
        else:
            active.append(it)
    return active, stale, warnings


def _has_tier(items: list[dict[str, Any]], tier: str) -> bool:
    return any(it.get("proof_tier") == tier for it in items)


def _l3_on_commit(
    items: list[dict[str, Any]], audited_commit: str | None, bundle_commit: str | None
) -> bool:
    """L3 CI evidence must be on the audited commit (item or bundle)."""
    for it in items:
        if it.get("proof_tier") != "L3":
            continue
        c = (it.get("git_commit") or bundle_commit or "").lower()
        if audited_commit and c and c != audited_commit.lower():
            continue
        if it.get("type") in ("ci_run", "ci_log", None) or it.get("ci_run_id"):
            return True
        if it.get("type") == "ci_run" or it.get("ci_job"):
            return True
        # Accept L3 typed items even without ci_run_id if explicitly L3
        return True
    return False


def _l5_dual_control(
    items: list[dict[str, Any]], producer_agent_id: str | None
) -> bool:
    """L5 requires independent_review with reviewer_id distinct from producer."""
    for it in items:
        if it.get("proof_tier") != "L5":
            continue
        if it.get("type") not in ("independent_review", "artifact", None) and it.get(
            "type"
        ) != "independent_review":
            # still allow if reviewer_id present
            pass
        reviewer = (it.get("reviewer_id") or "").strip()
        if not reviewer:
            continue
        if producer_agent_id and reviewer == producer_agent_id:
            continue
        return True
    return False


def _has_conflict(items: list[dict[str, Any]]) -> bool:
    """Conflicting signals on same commit → Ambiguous."""
    has_neg = any(it.get("type") == "negative_proof" for it in items)
    has_positive = any(
        it.get("proof_tier") in ("L2", "L3", "L4", "L5")
        and it.get("type") != "negative_proof"
        for it in items
    )
    if has_neg and has_positive:
        return True
    # Pass vs fail among L2/L3
    l23 = [it for it in items if it.get("proof_tier") in ("L2", "L3") and it.get("actual_result")]
    if any(is_failing(it) for it in l23) and any(not is_failing(it) for it in l23):
        return True
    return False


def _ni_supported(items: list[dict[str, Any]]) -> bool:
    """Not Implemented needs negative_proof OR absence search with repro_command."""
    for it in items:
        if it.get("type") == "negative_proof":
            return True
        if it.get("repro_command") and any(
            k in (it.get("summary") or "").lower()
            for k in ("absence", "not found", "no ", "missing", "0 matches")
        ):
            return True
        if it.get("type") == "negative_proof" or (
            it.get("repro_command") and it.get("type") in ("scan_report", "artifact", "other")
        ):
            # presence of repro + negative framing
            ar = (it.get("actual_result") or "").lower()
            if "0 match" in ar or "not found" in ar or ar.strip() == "0 matches":
                return True
    return any(it.get("type") == "negative_proof" for it in items)


def compute_status(
    *,
    severity: str,
    evidence_items: list[dict[str, Any]],
    residual_gaps: list[str] | None = None,
    audited_commit: str | None = None,
    bundle_commit: str | None = None,
    producer_agent_id: str | None = None,
    manual_override: dict[str, Any] | None = None,
    current_status: str | None = None,
) -> dict[str, Any]:
    """
    Proof policy 1.1.0:
    - L1 never contributes to Implemented or Partial alone.
    - Partial requires ≥ L2 AND explicit residual_gaps.
    - Implemented requires L2 AND (L3 on same commit OR L4).
    - Critical Implemented additionally requires L5 dual-control (distinct reviewer).
    - Conflicting evidence → Ambiguous.
    - Stale items (commit ≠ audited) excluded from closure; flagged.
    - NI needs negative_proof or absence search with repro_command.
    """
    warnings: list[str] = []
    gaps = list(residual_gaps or [])

    if manual_override and manual_override.get("status"):
        active, stale, w = _active_items(evidence_items, audited_commit, bundle_commit)
        warnings.extend(w)
        return {
            "status": manual_override["status"],
            "proof_tier": max_tier(active) if active else max_tier(evidence_items),
            "warnings": warnings
            + [f"Manual override: {manual_override.get('reason', '')}"],
            "stale_count": len(stale),
            "active_count": len(active),
            "proof_policy_version": PROOF_POLICY_VERSION,
        }

    active, stale, w = _active_items(evidence_items, audited_commit, bundle_commit)
    warnings.extend(w)

    def out(status: str, extra_w: list[str] | None = None, **kw: Any) -> dict[str, Any]:
        r = {
            "status": status,
            "proof_tier": max_tier(passing) if passing else max_tier([i for i in active if i.get("proof_tier") == "L1"]),
            "warnings": warnings + (extra_w or []),
            "stale_count": len(stale),
            "active_count": len(active),
            "proof_policy_version": PROOF_POLICY_VERSION,
        }
        r.update(kw)
        return r

    failing = [i for i in active if i.get("proof_tier") in ("L2", "L3") and is_failing(i)]
    passing = [i for i in active if i not in failing]
    if failing:
        warnings.append(f"{len(failing)} failing L2/L3 item(s) do not count as proof")

    if not active:
        status = current_status if current_status in STATUSES else "Not Verified"
        if status in ("Implemented", "Partially Implemented"):
            warnings.append(f"No active (non-stale) evidence — demoted from {status}")
            status = "Not Verified"
        return {
            "status": status,
            "proof_tier": "L0",
            "warnings": warnings
            + (["All evidence stale"] if stale else ["No evidence items"]),
            "stale_count": len(stale),
            "active_count": 0,
            "proof_policy_version": PROOF_POLICY_VERSION,
        }

    if failing and any(i.get("proof_tier") in ("L2", "L3") for i in passing):
        return out("Ambiguous", ["Passing and failing L2/L3 evidence on the audited commit"])

    if _has_conflict(passing):
        return {
            "status": "Ambiguous",
            "proof_tier": max_tier(active),
            "warnings": warnings + ["Conflicting evidence on audited commit"],
            "stale_count": len(stale),
            "active_count": len(active),
            "proof_policy_version": PROOF_POLICY_VERSION,
        }

    has_l2 = _has_tier(passing, "L2")
    has_l3 = _l3_on_commit(passing, audited_commit, bundle_commit)
    has_l4 = _has_tier(passing, "L4")
    has_l5 = _l5_dual_control(passing, producer_agent_id)
    has_neg = any(it.get("type") == "negative_proof" for it in passing)
    higher = has_l2 or has_l3 or has_l4 or has_l5
    only_l1 = (not higher) and _has_tier(passing, "L1")

    # L1 alone → never Partial or Implemented. Without negative proof it is Not Verified.
    if only_l1 or (not higher and not has_neg):
        if has_neg or _ni_supported(passing):
            return out("Not Implemented",
                       ["L1 does not count toward Partial/Implemented"] if only_l1 else [])
        return out("Not Verified",
                   ["L1-only / insufficient evidence: not verified (no L2, no negative proof)"])

    # Negative-only (no positive L2+) → NI if supported
    if has_neg and not has_l2 and not has_l3 and not has_l4 and not has_l5:
        if not _ni_supported(active):
            warnings.append(
                "Not Implemented claim lacks negative_proof or absence repro_command"
            )
        return {
            "status": "Not Implemented",
            "proof_tier": max_tier(active),
            "warnings": warnings,
            "stale_count": len(stale),
            "active_count": len(active),
            "proof_policy_version": PROOF_POLICY_VERSION,
        }

    can_implement = bool(has_l2 and (has_l3 or has_l4))
    if has_l2 and has_l4 and not has_l3:
        warnings.append("Implemented via L2+L4 (CI L3 absent — document why)")

    is_critical = (severity or "") == "Critical"

    if can_implement:
        if is_critical:
            if has_l3 and has_l5:
                return {
                    "status": "Implemented",
                    "proof_tier": max_tier(active),
                    "warnings": warnings,
                    "stale_count": len(stale),
                    "active_count": len(active),
                    "proof_policy_version": PROOF_POLICY_VERSION,
                }
            warnings.append(
                "Critical: needs L3 on audited commit + L5 dual-control "
                "(reviewer_id ≠ producer); holding at Partial"
            )
            if not gaps:
                gaps.append("Critical dual-control (L5) and/or L3 on commit incomplete")
                warnings.append("Auto residual_gaps added for Critical Partial")
            return {
                "status": "Partially Implemented",
                "proof_tier": max_tier(active),
                "warnings": warnings,
                "residual_gaps": gaps,
                "stale_count": len(stale),
                "active_count": len(active),
                "proof_policy_version": PROOF_POLICY_VERSION,
            }
        return {
            "status": "Implemented",
            "proof_tier": max_tier(active),
            "warnings": warnings,
            "stale_count": len(stale),
            "active_count": len(active),
            "proof_policy_version": PROOF_POLICY_VERSION,
        }

    # Partial path: need ≥ L2 and explicit residual_gaps
    if has_l2:
        if not gaps:
            warnings.append(
                "Partial requires explicit residual_gaps — status held at Not Verified "
                "until gaps are listed"
            )
            return {
                "status": "Not Verified",
                "proof_tier": max_tier(active),
                "warnings": warnings,
                "stale_count": len(stale),
                "active_count": len(active),
                "proof_policy_version": PROOF_POLICY_VERSION,
            }
        return {
            "status": "Partially Implemented",
            "proof_tier": max_tier(active),
            "warnings": warnings,
            "residual_gaps": gaps,
            "stale_count": len(stale),
            "active_count": len(active),
            "proof_policy_version": PROOF_POLICY_VERSION,
        }

    # L3/L4/L5 without L2 cannot Implement; without L2 cannot Partial either under 1.1
    warnings.append("L2 automated test evidence required for Partial or Implemented")
    return {
        "status": "Not Verified",
        "proof_tier": max_tier(active),
        "warnings": warnings,
        "stale_count": len(stale),
        "active_count": len(active),
        "proof_policy_version": PROOF_POLICY_VERSION,
    }


def enforce_bundle_rules(bundle: dict[str, Any]) -> list[str]:
    """Return list of violation messages (empty = ok for soft checks)."""
    errs: list[str] = []
    ppv = bundle.get("proof_policy_version")
    if ppv != PROOF_POLICY_VERSION:
        errs.append(
            f"proof_policy_version must be {PROOF_POLICY_VERSION}, got {ppv!r}"
        )
    for it in bundle.get("evidence_items") or []:
        if it.get("proof_tier") == "L0":
            errs.append(f"{it.get('evidence_id')}: L0 not allowed in evidence.json")
        if it.get("proof_tier") == "L5":
            if not it.get("reviewer_id"):
                errs.append(
                    f"{it.get('evidence_id')}: L5 requires reviewer_id (dual-control)"
                )
            producer = (bundle.get("generated_by") or {}).get("agent_id")
            if producer and it.get("reviewer_id") == producer:
                errs.append(
                    f"{it.get('evidence_id')}: L5 reviewer_id must differ from generated_by.agent_id"
                )
    return errs
