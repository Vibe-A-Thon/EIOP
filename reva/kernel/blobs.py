"""Content-addressed filesystem and object blob store for REVA (T-109 / §4.3 / D-04 / REVA-WK-007)."""

from __future__ import annotations

import hashlib
import io
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import BinaryIO, List, Optional, Set, Union

from pydantic import BaseModel, Field

from reva.config import get_settings
from reva.core.digest import sha256_hex
from reva.core.errors import RevaIntegrityError, RevaNotFoundError
from reva.core.ids import blob_id as make_blob_id
from reva.core.time import format_ts, utc_now_ms


class BlobRef(BaseModel):
    """Metadata reference to an immutable stored blob."""

    blob_id: str
    sha256: str
    size_bytes: int
    media_type: str = "application/octet-stream"
    classification: str = "internal"
    created_at: str = Field(default_factory=lambda: format_ts(utc_now_ms()))
    storage_path: Optional[str] = None


class HashingReader(io.RawIOBase):
    """Reader stream that verifies SHA-256 at EOF."""

    def __init__(self, raw_stream: BinaryIO, expected_sha256: str, blob_id: str) -> None:
        self._raw = raw_stream
        self._expected_sha256 = expected_sha256.lower()
        self._blob_id = blob_id
        self._hasher = hashlib.sha256()
        self._closed = False

    def readable(self) -> bool:
        return True

    def readinto(self, b: bytearray) -> int:
        n = self._raw.readinto(b)
        if n > 0:
            self._hasher.update(b[:n])
        elif n == 0 or n is None:
            # EOF reached: verify digest
            computed = self._hasher.hexdigest().lower()
            if computed != self._expected_sha256:
                raise RevaIntegrityError(
                    f"Blob {self._blob_id} integrity mismatch: expected {self._expected_sha256}, got {computed}",
                    details={"blob_id": self._blob_id, "expected": self._expected_sha256, "actual": computed},
                )
        return n if n is not None else 0

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self._raw.close()
        super().close()


class BlobStore:
    """Content-addressed filesystem blob store partitioned by tenant."""

    def __init__(self, root_dir: Optional[str] = None) -> None:
        settings = get_settings()
        self.root = Path(root_dir) if root_dir else Path(settings.blob_root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _tenant_ns(self, tenant_id: str) -> str:
        return hashlib.sha256(tenant_id.encode("utf-8")).hexdigest()[:16]

    def _blob_path(self, tenant_id: str, sha256_val: str) -> Path:
        ns = self._tenant_ns(tenant_id)
        hex_clean = sha256_val.lower().removeprefix("sha256:")
        ab = hex_clean[:2]
        cd = hex_clean[2:4]
        return self.root / ns / "sha256" / ab / cd / hex_clean

    def _tmp_dir(self, tenant_id: str) -> Path:
        ns = self._tenant_ns(tenant_id)
        tmp = self.root / ns / "tmp"
        tmp.mkdir(parents=True, exist_ok=True)
        return tmp

    def put(
        self,
        tenant_id: str,
        data: Union[BinaryIO, bytes],
        media_type: str = "application/octet-stream",
        classification: str = "internal",
    ) -> BlobRef:
        """Store content idempotently by content hash, streaming to temporary file first."""
        tmp_dir = self._tmp_dir(tenant_id)
        hasher = hashlib.sha256()
        size_bytes = 0

        # Create temporary file in same filesystem for atomic rename
        with tempfile.NamedTemporaryFile(dir=tmp_dir, delete=False) as tmp_file:
            temp_path = Path(tmp_file.name)
            try:
                if isinstance(data, bytes):
                    hasher.update(data)
                    tmp_file.write(data)
                    size_bytes = len(data)
                else:
                    while chunk := data.read(1024 * 1024):
                        hasher.update(chunk)
                        tmp_file.write(chunk)
                        size_bytes += len(chunk)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            except Exception:
                if temp_path.exists():
                    temp_path.unlink()
                raise

        digest = hasher.hexdigest().lower()
        final_path = self._blob_path(tenant_id, digest)
        final_path.parent.mkdir(parents=True, exist_ok=True)

        if final_path.exists():
            # Already exists: delete temp file (idempotent write)
            temp_path.unlink(missing_ok=True)
        else:
            # Atomic rename into CAS location
            temp_path.replace(final_path)
            try:
                # Fsync directory entry on POSIX if available
                dir_fd = os.open(str(final_path.parent), os.O_RDONLY)
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)
            except (OSError, AttributeError):
                pass

        bid = make_blob_id(digest)
        return BlobRef(
            blob_id=bid,
            sha256=digest,
            size_bytes=size_bytes,
            media_type=media_type,
            classification=classification,
            storage_path=str(final_path),
        )

    def get(self, tenant_id: str, blob_id_or_hash: str) -> BinaryIO:
        """Stream a blob and verify SHA-256 integrity on read."""
        clean_hash = blob_id_or_hash.lower().removeprefix("blb1_").removeprefix("sha256:")
        path = self._blob_path(tenant_id, clean_hash)
        if not path.is_file():
            raise RevaNotFoundError(
                f"Blob not found: {blob_id_or_hash}",
                details={"tenant_id": tenant_id, "blob_id": blob_id_or_hash},
            )

        raw = open(path, "rb")
        return HashingReader(raw, clean_hash, blob_id_or_hash)

    def get_bytes(self, tenant_id: str, blob_id_or_hash: str, max_bytes: Optional[int] = None) -> bytes:
        """Read all or up to max_bytes from the blob, validating digest integrity."""
        reader = self.get(tenant_id, blob_id_or_hash)
        with reader:
            if max_bytes is not None:
                data = reader.read(max_bytes)
                reader.read()
                return data
            return reader.read()


    def exists(self, tenant_id: str, blob_id_or_hash: str) -> bool:
        clean_hash = blob_id_or_hash.lower().removeprefix("blb1_").removeprefix("sha256:")
        return self._blob_path(tenant_id, clean_hash).is_file()

    def gc_dry_run(
        self,
        tenant_id: str,
        referenced_blob_ids: Set[str],
        older_than_s: int = 86400,
    ) -> List[str]:
        """List orphaned blobs unreferenced by any entity older than threshold."""
        ns = self._tenant_ns(tenant_id)
        tenant_root = self.root / ns / "sha256"
        if not tenant_root.exists():
            return []

        now = time.time()
        orphans: List[str] = []
        normalized_refs = {b.lower().removeprefix("blb1_") for b in referenced_blob_ids}

        for path in tenant_root.rglob("*"):
            if path.is_file():
                digest = path.name.lower()
                bid = make_blob_id(digest)
                if digest not in normalized_refs and bid not in referenced_blob_ids:
                    stat = path.stat()
                    if (now - stat.st_mtime) >= older_than_s:
                        orphans.append(bid)
        return orphans

    def gc(
        self,
        tenant_id: str,
        referenced_blob_ids: Set[str],
        older_than_s: int = 86400,
    ) -> List[str]:
        """Delete orphaned blobs unreferenced by any entity older than threshold."""
        orphans = self.gc_dry_run(tenant_id, referenced_blob_ids, older_than_s)
        for bid in orphans:
            digest = bid.removeprefix("blb1_")
            p = self._blob_path(tenant_id, digest)
            if p.is_file():
                p.unlink(missing_ok=True)
        return orphans
