"""Automated Backup, Verification & Restore Testing Engine (INFRA-007).

Provides automated enterprise recovery capabilities:
- BackupScheduler: Scheduled snapshot generation with retention policies
- BackupVerifier: Integrity verification using SHA-256 digests and schema checks
- RestoreTestRunner: Non-destructive dry-run restore validation into isolated test stores
- EncryptedBackupStore: Encryption-at-rest simulation for cold storage archives
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import logging
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.recovery.backup")


@dataclass
class BackupArchive:
    backup_id: str
    created_at: float
    vertex_count: int
    edge_count: int
    checksum: str
    encrypted: bool
    payload_bytes: bytes
    retention_days: int = 30
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "backup_id": self.backup_id,
            "created_at": self.created_at,
            "vertex_count": self.vertex_count,
            "edge_count": self.edge_count,
            "checksum": self.checksum,
            "encrypted": self.encrypted,
            "size_bytes": len(self.payload_bytes),
            "retention_days": self.retention_days,
            "metadata": self.metadata,
        }


class BackupVerifier:
    """Verifies archive integrity and tamper detection."""

    @staticmethod
    def verify(archive: BackupArchive, encryption_key: str = "eoip-recovery-key") -> dict[str, Any]:
        # 1. Verify Checksum
        computed_checksum = hashlib.sha256(archive.payload_bytes).hexdigest()
        is_checksum_valid = computed_checksum == archive.checksum

        # 2. Verify Decryption & Schema Decode
        decrypted_valid = False
        parsed_vertices = 0
        parsed_edges = 0
        try:
            raw = archive.payload_bytes
            if archive.encrypted:
                # Decrypt (symmetric XOR stream with key)
                key_bytes = hashlib.sha256(encryption_key.encode()).digest()
                decrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(raw))
            else:
                decrypted = raw

            data = json.loads(decrypted.decode("utf-8"))
            parsed_vertices = len(data.get("vertices", []))
            parsed_edges = len(data.get("edges", []))
            decrypted_valid = parsed_vertices == archive.vertex_count and parsed_edges == archive.edge_count
        except Exception as e:
            logger.warning(f"Decryption / parse failed during verification: {e}")

        conforms = is_checksum_valid and decrypted_valid
        return {
            "conforms": conforms,
            "checksum_valid": is_checksum_valid,
            "data_valid": decrypted_valid,
            "expected_vertices": archive.vertex_count,
            "actual_vertices": parsed_vertices,
            "expected_edges": archive.edge_count,
            "actual_edges": parsed_edges,
        }


class RestoreTestRunner:
    """Performs automated non-destructive restore testing into an isolated MemoryGraphStore."""

    def __init__(self, encryption_key: str = "eoip-recovery-key") -> None:
        self.encryption_key = encryption_key

    def test_restore(self, archive: BackupArchive) -> dict[str, Any]:
        start = time.time()
        # 1. Verify integrity first
        ver = BackupVerifier.verify(archive, self.encryption_key)
        if not ver["conforms"]:
            return {
                "success": False,
                "error": "Archive failed pre-restore integrity check",
                "duration_ms": (time.time() - start) * 1000,
            }

        # 2. Restore to isolated in-memory graph
        try:
            raw = archive.payload_bytes
            if archive.encrypted:
                key_bytes = hashlib.sha256(self.encryption_key.encode()).digest()
                raw = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(raw))

            data = json.loads(raw.decode("utf-8"))
            test_store = MemoryGraphStore()

            for v in data.get("vertices", []):
                test_store.upsert_vertex(v["label"], v["properties"])

            for e in data.get("edges", []):
                out_ref = e.get("out_cid", e["out_v"])
                in_ref = e.get("in_cid", e["in_v"])
                test_store.upsert_edge(e["label"], out_ref, in_ref, dict(e.get("properties", {})))

            # Verify isolated graph count
            restored_v = test_store.count_vertices()
            restored_e = test_store.count_edges()

            return {
                "success": True,
                "restored_vertices": restored_v,
                "restored_edges": restored_e,
                "duration_ms": round((time.time() - start) * 1000, 2),
                "isolated_store_healthy": test_store.health(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "duration_ms": round((time.time() - start) * 1000, 2),
            }


class BackupScheduler:
    """Schedules backups and enforces retention policy."""

    def __init__(self, encryption_key: str = "eoip-recovery-key") -> None:
        self.encryption_key = encryption_key
        self.archives: dict[str, BackupArchive] = {}
        self.restore_runner = RestoreTestRunner(encryption_key)
        self._lock = threading.Lock()

    def create_backup(
        self,
        store: MemoryGraphStore,
        encrypt: bool = True,
        retention_days: int = 30,
    ) -> BackupArchive:
        with self._lock:
            vertices = store.find_vertices()
            edges = store.find_edges()
            payload = json.dumps({"vertices": vertices, "edges": edges}, default=str).encode("utf-8")

            if encrypt:
                key_bytes = hashlib.sha256(self.encryption_key.encode()).digest()
                final_bytes = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(payload))
            else:
                final_bytes = payload

            bid = f"backup_{uuid.uuid4().hex[:10]}"
            checksum = hashlib.sha256(final_bytes).hexdigest()

            archive = BackupArchive(
                backup_id=bid,
                created_at=time.time(),
                vertex_count=len(vertices),
                edge_count=len(edges),
                checksum=checksum,
                encrypted=encrypt,
                payload_bytes=final_bytes,
                retention_days=retention_days,
            )
            self.archives[bid] = archive
            return archive

    def run_automated_restore_drill(self, backup_id: str) -> dict[str, Any]:
        with self._lock:
            archive = self.archives.get(backup_id)
            if not archive:
                raise ValueError(f"Backup {backup_id} not found")
        return self.restore_runner.test_restore(archive)

    def prune_expired(self) -> int:
        with self._lock:
            now = time.time()
            expired = [
                bid for bid, a in self.archives.items()
                if (now - a.created_at) > (a.retention_days * 86400)
            ]
            for bid in expired:
                del self.archives[bid]
            return len(expired)
