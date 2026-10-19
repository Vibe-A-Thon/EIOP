"""Canonical Proof-of-Done ledger construction, verification, and export (T-212 / REVA-PD-006 / REVA-PD-011)."""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from reva.core.ids import ledger_id as compute_ledger_id
from reva.core.jcs import canonicalize
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.store import RevaStore
from reva.pd.closure import ClosureDecision


@dataclass
class LedgerRecord:
    """Canonical signed ledger of all Proof-of-Done closure decisions."""

    ledger_id: str
    tenant_id: str
    scope: str
    commit: str
    complete: bool
    summary: Dict[str, int]
    closures: List[ClosureDecision]
    created_at: str
    signature: Optional[str] = None
    key_id: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "closures": [c.canonical_dict() for c in sorted(self.closures, key=lambda x: x.obligation_key)],
            "commit": self.commit,
            "complete": self.complete,
            "created_at": self.created_at,
            "ledger_id": self.ledger_id,
            "scope": self.scope,
            "summary": self.summary,
            "tenant_id": self.tenant_id,
        }

    def to_markdown(self) -> str:
        """Render human-readable Markdown summary report."""
        lines = [
            f"# REVA Proof-of-Done Ledger",
            f"",
            f"| Field | Value |",
            f"|---|---|",
            f"| **Ledger ID** | `{self.ledger_id}` |",
            f"| **Commit** | `{self.commit}` |",
            f"| **Scope** | `{self.scope}` |",
            f"| **Complete** | `{'Yes (100%)' if self.complete else 'No'}` |",
            f"| **Evaluated At** | `{self.created_at}` |",
            f"",
            f"## Outcome Summary",
            f"",
            f"| Outcome | Count |",
            f"|---|---|",
        ]
        for k, v in self.summary.items():
            lines.append(f"| **{k.capitalize()}** | {v} |")

        lines.extend([
            f"",
            f"## Closure Decisions ({len(self.closures)})",
            f"",
            f"| Obligation Key | Outcome | Reasons |",
            f"|---|---|---|",
        ])

        for c in sorted(self.closures, key=lambda x: x.obligation_key):
            reasons_str = ", ".join(c.reasons) if c.reasons else "—"
            lines.append(f"| `{c.obligation_key}` | **{c.outcome.upper()}** | {reasons_str} |")

        return "\n".join(lines)


def build_ledger(
    tenant_id: str,
    scope: str,
    commit: str,
    decisions: List[ClosureDecision],
    store: Optional[RevaStore] = None,
    private_key: Optional[Ed25519PrivateKey] = None,
    key_id: Optional[str] = None,
) -> LedgerRecord:
    """Construct deterministic signed ledger from closure decisions."""
    sorted_closure_ids = sorted([d.closure_id for d in decisions])
    lid = compute_ledger_id(scope, sorted_closure_ids)
    created_at = format_ts(utc_now_ms())

    # Calculate summary counts
    summary: Dict[str, int] = {
        "closed": 0,
        "open": 0,
        "failed": 0,
        "blocked": 0,
        "stale": 0,
        "flaky": 0,
        "unknown": 0,
    }
    for d in decisions:
        summary[d.outcome] = summary.get(d.outcome, 0) + 1

    total = len(decisions)
    complete = (summary["closed"] == total) and total > 0

    record = LedgerRecord(
        ledger_id=lid,
        tenant_id=tenant_id,
        scope=scope,
        commit=commit,
        complete=complete,
        summary=summary,
        closures=decisions,
        created_at=created_at,
    )

    if private_key is not None and key_id is not None:
        payload_bytes = b"REVA-LEDGER-V1\n" + canonicalize(record.canonical_dict())
        sig_raw = private_key.sign(payload_bytes)
        record.signature = base64.urlsafe_b64encode(sig_raw).decode("ascii").rstrip("=")
        record.key_id = key_id

    # Persist in store
    if store is not None:
        cur = store.conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO reva_ledgers (
                tenant_id, ledger_id, scope, commit_sha, complete, record, warrant_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                lid,
                scope,
                commit,
                1 if complete else 0,
                json.dumps(record.canonical_dict()),
                "",
                created_at,
            ),
        )
        store.conn.commit()

    return record
