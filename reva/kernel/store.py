"""Relational SQLite store and tenant repository for REVA (T-108 / REVA-SEC-001 / D-03)."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from reva.core.time import format_ts, utc_now_ms


class RevaStore:
    """Tenant-scoped transactional repository supporting SQLite (WAL mode) and in-memory databases."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA synchronous=NORMAL;")
        cur.execute("PRAGMA foreign_keys=ON;")

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS reva_producers (
            producer_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            producer_type TEXT NOT NULL,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            build_digest TEXT,
            owner TEXT,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS reva_keys (
            key_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            owner_kind TEXT NOT NULL,
            owner_id TEXT NOT NULL,
            public_key BLOB NOT NULL,
            private_key_enc BLOB,
            status TEXT NOT NULL,
            activated_at TEXT NOT NULL,
            revoked_at TEXT
        );

        CREATE TABLE IF NOT EXISTS reva_blobs (
            tenant_id TEXT NOT NULL,
            blob_id TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            media_type TEXT NOT NULL,
            classification TEXT NOT NULL DEFAULT 'internal',
            created_at TEXT NOT NULL,
            PRIMARY KEY (tenant_id, blob_id)
        );

        CREATE TABLE IF NOT EXISTS reva_warrants (
            tenant_id TEXT NOT NULL,
            warrant_id TEXT NOT NULL,
            body TEXT NOT NULL,
            envelope TEXT NOT NULL,
            subject_key TEXT NOT NULL,
            predicate TEXT NOT NULL,
            producer_id TEXT NOT NULL,
            authority TEXT NOT NULL,
            epistemic TEXT NOT NULL,
            confidence_bp INTEGER NOT NULL,
            observed_at TEXT NOT NULL,
            valid_from TEXT NOT NULL,
            valid_to TEXT,
            recorded_at TEXT NOT NULL,
            status TEXT NOT NULL,
            log_index INTEGER NOT NULL,
            acl_tokens TEXT NOT NULL,
            classification TEXT NOT NULL,
            PRIMARY KEY (tenant_id, warrant_id)
        );
        CREATE INDEX IF NOT EXISTS idx_warrants_subj ON reva_warrants(tenant_id, subject_key);
        CREATE INDEX IF NOT EXISTS idx_warrants_pred ON reva_warrants(tenant_id, predicate);
        CREATE INDEX IF NOT EXISTS idx_warrants_rec ON reva_warrants(tenant_id, recorded_at);

        CREATE TABLE IF NOT EXISTS reva_warrant_links (
            tenant_id TEXT NOT NULL,
            from_id TEXT NOT NULL,
            rel TEXT NOT NULL,
            to_id TEXT NOT NULL,
            PRIMARY KEY (tenant_id, from_id, rel, to_id)
        );
        CREATE INDEX IF NOT EXISTS idx_links_to ON reva_warrant_links(tenant_id, to_id, rel);

        CREATE TABLE IF NOT EXISTS reva_log_leaves (
            log_id TEXT NOT NULL,
            leaf_index INTEGER NOT NULL,
            leaf_data TEXT NOT NULL,
            leaf_hash BLOB NOT NULL,
            appended_at TEXT NOT NULL,
            PRIMARY KEY (log_id, leaf_index)
        );

        CREATE TABLE IF NOT EXISTS reva_sths (
            log_id TEXT NOT NULL,
            tree_size INTEGER NOT NULL,
            root_hash BLOB NOT NULL,
            issued_at TEXT NOT NULL,
            key_id TEXT NOT NULL,
            signature BLOB NOT NULL,
            sth_id TEXT NOT NULL,
            PRIMARY KEY (log_id, tree_size)
        );

        CREATE TABLE IF NOT EXISTS reva_gap_heads (
            tenant_id TEXT NOT NULL,
            gap_id TEXT NOT NULL,
            revision INTEGER NOT NULL,
            status TEXT NOT NULL,
            severity TEXT NOT NULL,
            impact_score_bp INTEGER NOT NULL,
            owner TEXT,
            due_at TEXT,
            domain TEXT NOT NULL,
            record TEXT NOT NULL,
            PRIMARY KEY (tenant_id, gap_id)
        );

        CREATE TABLE IF NOT EXISTS reva_contradictions (
            tenant_id TEXT NOT NULL,
            contradiction_id TEXT NOT NULL,
            record TEXT NOT NULL,
            status TEXT NOT NULL,
            conflict_kind TEXT NOT NULL,
            subject_key TEXT NOT NULL,
            predicate TEXT NOT NULL,
            opened_at TEXT NOT NULL,
            PRIMARY KEY (tenant_id, contradiction_id)
        );

        CREATE TABLE IF NOT EXISTS reva_obligations (
            tenant_id TEXT NOT NULL,
            key TEXT NOT NULL,
            version INTEGER NOT NULL,
            digest TEXT NOT NULL,
            definition TEXT NOT NULL,
            reviewed_warrant_id TEXT,
            disposition TEXT NOT NULL,
            PRIMARY KEY (tenant_id, key, version)
        );

        CREATE TABLE IF NOT EXISTS reva_bindings (
            tenant_id TEXT NOT NULL,
            obligation_key TEXT NOT NULL,
            obligation_version INTEGER NOT NULL,
            binding_digest TEXT NOT NULL,
            binding TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (tenant_id, obligation_key)
        );

        CREATE TABLE IF NOT EXISTS reva_runs (
            tenant_id TEXT NOT NULL,
            run_id TEXT NOT NULL,
            verifier_id TEXT NOT NULL,
            binding_digest TEXT NOT NULL,
            commit_sha TEXT NOT NULL,
            status TEXT NOT NULL,
            record TEXT NOT NULL,
            attestation_id TEXT,
            started_at TEXT,
            finished_at TEXT,
            PRIMARY KEY (tenant_id, run_id)
        );

        CREATE TABLE IF NOT EXISTS reva_run_tests (
            tenant_id TEXT NOT NULL,
            run_id TEXT NOT NULL,
            test_id TEXT NOT NULL,
            outcome TEXT NOT NULL,
            obligation_keys TEXT NOT NULL,
            case_kinds TEXT NOT NULL,
            owner_lines_hit TEXT NOT NULL,
            rerun_outcomes TEXT NOT NULL,
            PRIMARY KEY (tenant_id, run_id, test_id)
        );

        CREATE TABLE IF NOT EXISTS reva_attestations (
            tenant_id TEXT NOT NULL,
            attestation_id TEXT NOT NULL,
            envelope TEXT NOT NULL,
            log_index INTEGER NOT NULL,
            PRIMARY KEY (tenant_id, attestation_id)
        );

        CREATE TABLE IF NOT EXISTS reva_waivers (
            tenant_id TEXT NOT NULL,
            waiver_id TEXT NOT NULL,
            target TEXT NOT NULL,
            kind TEXT NOT NULL,
            rationale TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            warrant_id TEXT NOT NULL,
            PRIMARY KEY (tenant_id, waiver_id)
        );

        CREATE TABLE IF NOT EXISTS reva_closures (
            tenant_id TEXT NOT NULL,
            closure_id TEXT NOT NULL,
            obligation_key TEXT NOT NULL,
            obligation_version INTEGER NOT NULL,
            commit_sha TEXT NOT NULL,
            outcome TEXT NOT NULL,
            reasons TEXT NOT NULL,
            record TEXT NOT NULL,
            evaluated_at TEXT NOT NULL,
            PRIMARY KEY (tenant_id, closure_id)
        );

        CREATE TABLE IF NOT EXISTS reva_ledgers (
            tenant_id TEXT NOT NULL,
            ledger_id TEXT NOT NULL,
            scope TEXT NOT NULL,
            commit_sha TEXT NOT NULL,
            complete INTEGER NOT NULL,
            record TEXT NOT NULL,
            warrant_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (tenant_id, ledger_id)
        );

        CREATE TABLE IF NOT EXISTS reva_jobs (
            job_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            kind TEXT NOT NULL,
            payload TEXT NOT NULL,
            priority INTEGER NOT NULL,
            status TEXT NOT NULL,
            lease_owner TEXT,
            lease_expires_at TEXT,
            attempts INTEGER NOT NULL DEFAULT 0,
            progress TEXT,
            result_ref TEXT,
            error TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS reva_outbox (
            event_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            type TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL,
            delivered_at TEXT
        );

        CREATE TABLE IF NOT EXISTS reva_quarantine (
            tenant_id TEXT NOT NULL,
            object_kind TEXT NOT NULL,
            object_id TEXT NOT NULL,
            reason TEXT NOT NULL,
            detected_at TEXT NOT NULL,
            details TEXT,
            PRIMARY KEY (tenant_id, object_kind, object_id)
        );

        CREATE TABLE IF NOT EXISTS reva_entities (
            tenant_id TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            logical_key TEXT NOT NULL,
            current_version_id TEXT,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            PRIMARY KEY (tenant_id, entity_id),
            UNIQUE (tenant_id, entity_type, logical_key)
        );

        CREATE TABLE IF NOT EXISTS reva_entity_versions (
            tenant_id TEXT NOT NULL,
            version_id TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            version_basis TEXT NOT NULL,
            version_digest TEXT NOT NULL,
            repo_id TEXT,
            commit_sha TEXT,
            valid_from TEXT NOT NULL,
            valid_to TEXT,
            warrant_id TEXT NOT NULL,
            PRIMARY KEY (tenant_id, version_id)
        );
        """)
        self.conn.commit()



    # --- Warrants ---
    def save_warrant(
        self,
        tenant_id: str,
        warrant_id: str,
        body: Dict[str, Any],
        envelope: Dict[str, Any],
        subject_key: str,
        predicate: str,
        producer_id: str,
        authority: str,
        epistemic: str,
        confidence_bp: int,
        observed_at: str,
        valid_from: str,
        valid_to: Optional[str],
        recorded_at: str,
        status: str,
        log_index: int,
        acl_tokens: List[str],
        classification: str,
        links: List[Dict[str, str]],
    ) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO reva_warrants (
                tenant_id, warrant_id, body, envelope, subject_key, predicate, producer_id,
                authority, epistemic, confidence_bp, observed_at, valid_from, valid_to,
                recorded_at, status, log_index, acl_tokens, classification
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                warrant_id,
                json.dumps(body),
                json.dumps(envelope),
                subject_key,
                predicate,
                producer_id,
                authority,
                epistemic,
                confidence_bp,
                observed_at,
                valid_from,
                valid_to,
                recorded_at,
                status,
                log_index,
                json.dumps(acl_tokens),
                classification,
            ),
        )
        for link in links:
            cur.execute(
                """
                INSERT OR IGNORE INTO reva_warrant_links (tenant_id, from_id, rel, to_id)
                VALUES (?, ?, ?, ?)
                """,
                (tenant_id, warrant_id, link["rel"], link["warrant_id"]),
            )
        self.conn.commit()

    def get_warrant(self, tenant_id: str, warrant_id: str) -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
        cur = self.conn.cursor()
        row = cur.execute(
            "SELECT body, envelope FROM reva_warrants WHERE tenant_id = ? AND warrant_id = ?",
            (tenant_id, warrant_id),
        ).fetchone()
        if not row:
            return None
        return json.loads(row["body"]), json.loads(row["envelope"])

    def update_warrant_envelope(self, tenant_id: str, warrant_id: str, envelope: Dict[str, Any], status: str) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE reva_warrants SET envelope = ?, status = ? WHERE tenant_id = ? AND warrant_id = ?",
            (json.dumps(envelope), status, tenant_id, warrant_id),
        )
        self.conn.commit()

    # --- Keys ---
    def save_key(
        self,
        key_id: str,
        tenant_id: str,
        owner_kind: str,
        owner_id: str,
        public_key: bytes,
        private_key_enc: bytes,
        status: str,
        activated_at: str,
    ) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO reva_keys (
                key_id, tenant_id, owner_kind, owner_id, public_key, private_key_enc, status, activated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (key_id, tenant_id, owner_kind, owner_id, public_key, private_key_enc, status, activated_at),
        )
        self.conn.commit()

    def get_key(self, key_id: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        row = cur.execute("SELECT * FROM reva_keys WHERE key_id = ?", (key_id,)).fetchone()
        if not row:
            return None
        return dict(row)

    # --- Outbox ---
    def save_outbox_event(self, event_id: str, tenant_id: str, event_type: str, payload: Dict[str, Any]) -> None:
        cur = self.conn.cursor()
        now = format_ts(utc_now_ms())
        cur.execute(
            "INSERT INTO reva_outbox (event_id, tenant_id, type, payload, created_at) VALUES (?, ?, ?, ?, ?)",
            (event_id, tenant_id, event_type, json.dumps(payload), now),
        )
        self.conn.commit()

    # --- Quarantine ---
    def quarantine_object(
        self,
        tenant_id: str,
        object_kind: str,
        object_id: str,
        reason: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        cur = self.conn.cursor()
        now = format_ts(utc_now_ms())
        cur.execute(
            """
            INSERT OR REPLACE INTO reva_quarantine (
                tenant_id, object_kind, object_id, reason, detected_at, details
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tenant_id, object_kind, object_id, reason, now, json.dumps(details or {})),
        )
        self.conn.commit()

    def is_quarantined(self, tenant_id: str, object_kind: str, object_id: str) -> bool:
        cur = self.conn.cursor()
        row = cur.execute(
            "SELECT 1 FROM reva_quarantine WHERE tenant_id = ? AND object_kind = ? AND object_id = ?",
            (tenant_id, object_kind, object_id),
        ).fetchone()
        return row is not None

    def list_quarantined(self, tenant_id: str) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        rows = cur.execute(
            "SELECT * FROM reva_quarantine WHERE tenant_id = ? ORDER BY detected_at DESC",
            (tenant_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    # --- Query & Bitemporal Filters ---
    def get_superseded_warrant_ids(self, tenant_id: str, recorded_before: Optional[str] = None) -> Set[str]:
        """Find IDs of warrants that were superseded, optionally before a recorded_at timestamp."""
        cur = self.conn.cursor()
        if recorded_before is not None:
            query = """
            SELECT DISTINCT l.to_id FROM reva_warrant_links l
            JOIN reva_warrants w ON l.tenant_id = w.tenant_id AND l.from_id = w.warrant_id
            WHERE l.tenant_id = ? AND l.rel = 'supersedes' AND w.recorded_at <= ?
            """
            rows = cur.execute(query, (tenant_id, recorded_before)).fetchall()
        else:
            query = "SELECT DISTINCT to_id FROM reva_warrant_links WHERE tenant_id = ? AND rel = 'supersedes'"
            rows = cur.execute(query, (tenant_id,)).fetchall()
        return {r[0] for r in rows}

    def search_warrants(
        self,
        tenant_id: str,
        subject_key: Optional[str] = None,
        predicate: Optional[str] = None,
        producer_id: Optional[str] = None,
        authority: Optional[str] = None,
        epistemic: Optional[str] = None,
        status: Optional[str] = None,
        min_confidence_bp: Optional[int] = None,
        classification: Optional[str] = None,
        as_of_valid: Optional[str] = None,
        as_of_recorded: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
        """Bitemporal search for warrants with multi-dimensional filtering."""
        clauses = ["tenant_id = ?"]
        params: List[Any] = [tenant_id]

        if subject_key is not None:
            clauses.append("subject_key = ?")
            params.append(subject_key)
        if predicate is not None:
            clauses.append("predicate = ?")
            params.append(predicate)
        if producer_id is not None:
            clauses.append("producer_id = ?")
            params.append(producer_id)
        if authority is not None:
            clauses.append("authority = ?")
            params.append(authority)
        if epistemic is not None:
            clauses.append("epistemic = ?")
            params.append(epistemic)
        if status is not None:
            clauses.append("status = ?")
            params.append(status)
        if min_confidence_bp is not None:
            clauses.append("confidence_bp >= ?")
            params.append(min_confidence_bp)
        if classification is not None:
            clauses.append("classification = ?")
            params.append(classification)

        # As-of valid: valid_from <= V and (valid_to is null or V < valid_to)
        if as_of_valid is not None:
            clauses.append("valid_from <= ? AND (valid_to IS NULL OR valid_to > ?)")
            params.extend([as_of_valid, as_of_valid])

        # As-of recorded: recorded_at <= T
        if as_of_recorded is not None:
            clauses.append("recorded_at <= ?")
            params.append(as_of_recorded)

        sql = f"SELECT body, envelope FROM reva_warrants WHERE {' AND '.join(clauses)} ORDER BY recorded_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cur = self.conn.cursor()
        rows = cur.execute(sql, params).fetchall()

        results = []
        superseded_ids = self.get_superseded_warrant_ids(tenant_id, as_of_recorded) if as_of_recorded else set()

        for r in rows:
            body = json.loads(r["body"])
            env = json.loads(r["envelope"])
            wid = env.get("warrant_id") or body.get("warrant_id")
            # If as_of_recorded is active, exclude warrants that were superseded before T
            if as_of_recorded and wid in superseded_ids:
                continue
            results.append((body, env))
        return results

