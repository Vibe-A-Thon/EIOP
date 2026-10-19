"""Archive and container format detection, safe extraction, and inventory (T-401 / REVA-AI-001..007)."""

from __future__ import annotations

import bz2
import gzip
import hashlib
import io
import lzma
import os
import tarfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from reva.core.errors import RevaResourceLimitError, RevaValidationError

MAX_UNCOMPRESSED_BYTES = 8 * 1024 * 1024 * 1024  # 8 GiB
MAX_MEMBER_COUNT = 500_000
MAX_SINGLE_MEMBER_BYTES = 2 * 1024 * 1024 * 1024  # 2 GiB
MAX_PATH_LENGTH = 4096


@dataclass
class MemberRecord:
    member_path: str
    size_bytes: int
    sha256: str
    media_type: str = "application/octet-stream"
    format: str = "binary"
    mode: Optional[int] = None
    mtime: Optional[float] = None


@dataclass
class InventoryResult:
    container_format: str
    total_members: int
    total_uncompressed_bytes: int
    members: List[MemberRecord] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)


def detect_format(header_bytes: bytes, filename: Optional[str] = None) -> str:
    """Detect container format using magic bytes first, extension second."""
    if header_bytes.startswith(b"PK\x03\x04") or header_bytes.startswith(b"PK\x05\x06"):
        return "zip"
    if header_bytes.startswith(b"\x1f\x8b"):
        return "tar.gz"
    if header_bytes.startswith(b"BZh"):
        return "tar.bz2"
    if header_bytes.startswith(b"\xfd7zXZ\x00"):
        return "tar.xz"
    if len(header_bytes) >= 262 and header_bytes[257:262] == b"ustar":
        return "tar"

    if filename:
        fn_lower = filename.lower()
        if fn_lower.endswith(".zip") or fn_lower.endswith(".jar") or fn_lower.endswith(".war") or fn_lower.endswith(".whl"):
            return "zip"
        if fn_lower.endswith(".tar.gz") or fn_lower.endswith(".tgz"):
            return "tar.gz"
        if fn_lower.endswith(".tar.bz2"):
            return "tar.bz2"
        if fn_lower.endswith(".tar.xz"):
            return "tar.xz"
        if fn_lower.endswith(".tar"):
            return "tar"

    return "binary"


def validate_member_path(path_str: str) -> str:
    """Validate and normalize member path, preventing directory traversal and absolute paths."""
    norm = path_str.replace("\\", "/").strip()
    if norm.startswith("/") or ":" in norm:
        raise RevaValidationError(f"Invalid member path (absolute or drive letter): {path_str}")
    parts = norm.split("/")
    if ".." in parts:
        raise RevaValidationError(f"Directory traversal detected in member path: {path_str}")
    if len(norm) > MAX_PATH_LENGTH:
        raise RevaValidationError(f"Member path exceeds maximum length of {MAX_PATH_LENGTH}: {path_str}")
    return norm


def inventory_archive(
    source: Union[str, Path, bytes],
    filename: Optional[str] = None,
) -> InventoryResult:
    """Safely inventory all members of an archive or container."""
    if isinstance(source, bytes):
        raw_bytes = source
        stream = io.BytesIO(raw_bytes)
        fn = filename or "archive"
    else:
        path = Path(source).resolve()
        fn = filename or path.name
        with open(path, "rb") as f:
            header = f.read(512)
        stream = open(path, "rb")

    stream.seek(0)
    header = stream.read(512)
    stream.seek(0)

    fmt = detect_format(header, fn)
    members: List[MemberRecord] = []
    limitations: List[str] = []
    total_bytes = 0

    if fmt == "zip":
        with zipfile.ZipFile(stream, "r") as zf:
            infolist = zf.infolist()
            if len(infolist) > MAX_MEMBER_COUNT:
                raise RevaResourceLimitError(f"Zip member count ({len(infolist)}) exceeds limit {MAX_MEMBER_COUNT}")

            for info in infolist:
                if info.is_dir():
                    continue
                norm_path = validate_member_path(info.filename)
                if info.file_size > MAX_SINGLE_MEMBER_BYTES:
                    limitations.append(f"MEMBER_EXCEEDED_SIZE:{norm_path}")
                    continue

                total_bytes += info.file_size
                if total_bytes > MAX_UNCOMPRESSED_BYTES:
                    raise RevaResourceLimitError(f"Total uncompressed bytes exceed limit {MAX_UNCOMPRESSED_BYTES}")

                with zf.open(info) as mf:
                    content = mf.read()
                    digest = hashlib.sha256(content).hexdigest()

                members.append(
                    MemberRecord(
                        member_path=norm_path,
                        size_bytes=info.file_size,
                        sha256=digest,
                        mtime=float(info.date_time[0]) if info.date_time else None,
                    )
                )

    elif fmt in ("tar", "tar.gz", "tar.bz2", "tar.xz"):
        mode = "r:*"
        if fmt == "tar.gz":
            mode = "r:gz"
        elif fmt == "tar.bz2":
            mode = "r:bz2"
        elif fmt == "tar.xz":
            mode = "r:xz"

        with tarfile.open(fileobj=stream, mode=mode) as tf:
            count = 0
            for ti in tf:
                if not ti.isfile():
                    continue
                count += 1
                if count > MAX_MEMBER_COUNT:
                    raise RevaResourceLimitError(f"Tar member count exceeds limit {MAX_MEMBER_COUNT}")

                norm_path = validate_member_path(ti.name)
                if ti.size > MAX_SINGLE_MEMBER_BYTES:
                    limitations.append(f"MEMBER_EXCEEDED_SIZE:{norm_path}")
                    continue

                total_bytes += ti.size
                if total_bytes > MAX_UNCOMPRESSED_BYTES:
                    raise RevaResourceLimitError(f"Total uncompressed bytes exceed limit {MAX_UNCOMPRESSED_BYTES}")

                ef = tf.extractfile(ti)
                content = ef.read() if ef else b""
                digest = hashlib.sha256(content).hexdigest()

                members.append(
                    MemberRecord(
                        member_path=norm_path,
                        size_bytes=ti.size,
                        sha256=digest,
                        mode=ti.mode,
                        mtime=ti.mtime,
                    )
                )
    else:
        # Single binary file
        stream.seek(0)
        content = stream.read()
        digest = hashlib.sha256(content).hexdigest()
        members.append(
            MemberRecord(
                member_path=fn,
                size_bytes=len(content),
                sha256=digest,
            )
        )
        total_bytes = len(content)

    return InventoryResult(
        container_format=fmt,
        total_members=len(members),
        total_uncompressed_bytes=total_bytes,
        members=members,
        limitations=limitations,
    )


def extract_members(
    archive_path: Union[str, Path],
    member_paths: List[str],
    dest_dir: Union[str, Path],
) -> List[str]:
    """Safely extract specified members from archive to destination directory."""
    dest = Path(dest_dir).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    extracted: List[str] = []
    target_set = {validate_member_path(p) for p in member_paths}

    inv = inventory_archive(archive_path)
    if inv.container_format == "zip":
        with zipfile.ZipFile(archive_path, "r") as zf:
            for info in zf.infolist():
                norm = validate_member_path(info.filename)
                if norm in target_set:
                    out_path = dest / norm
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(info) as src, open(out_path, "wb") as dst:
                        dst.write(src.read())
                    extracted.append(norm)

    elif inv.container_format.startswith("tar"):
        with tarfile.open(archive_path, "r:*") as tf:
            for ti in tf:
                norm = validate_member_path(ti.name)
                if norm in target_set:
                    out_path = dest / norm
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    ef = tf.extractfile(ti)
                    if ef:
                        with open(out_path, "wb") as dst:
                            dst.write(ef.read())
                        extracted.append(norm)

    return extracted
