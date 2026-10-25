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
MAX_MEMBER_COMPRESSION_RATIO = 200  # REVA-AI-002: per member
MAX_OVERALL_COMPRESSION_RATIO = 100  # REVA-AI-002: whole container
RATIO_CHECK_FLOOR_BYTES = 1024 * 1024  # tiny members/archives are never ratio-limited
_CHUNK = 1024 * 1024


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
class LinkRecord:
    """A symlink/hardlink member: recorded, never followed or materialized (REVA-AI-003)."""

    member_path: str
    target: str
    link_type: str = "symlink"


@dataclass
class InventoryResult:
    container_format: str
    total_members: int
    total_uncompressed_bytes: int
    members: List[MemberRecord] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    links: List[LinkRecord] = field(default_factory=list)
    coverage: str = "complete"  # "partial" when any limit or rejection stopped part of the expansion


def _format_from_extension(filename: Optional[str]) -> Optional[str]:
    if not filename:
        return None
    fn_lower = filename.lower()
    if fn_lower.endswith((".zip", ".jar", ".war", ".whl")):
        return "zip"
    if fn_lower.endswith((".tar.gz", ".tgz")):
        return "tar.gz"
    if fn_lower.endswith(".tar.bz2"):
        return "tar.bz2"
    if fn_lower.endswith(".tar.xz"):
        return "tar.xz"
    if fn_lower.endswith(".tar"):
        return "tar"
    return None


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


def _hash_stream(fileobj, limit: int) -> tuple[str, int, bool]:
    """sha256 a member stream in chunks; stop (truncated=True) once more than ``limit`` bytes are read."""
    digest = hashlib.sha256()
    read = 0
    while True:
        chunk = fileobj.read(_CHUNK)
        if not chunk:
            return digest.hexdigest(), read, False
        read += len(chunk)
        if read > limit:
            return digest.hexdigest(), read, True
        digest.update(chunk)


def inventory_archive(
    source: Union[str, Path, bytes],
    filename: Optional[str] = None,
) -> InventoryResult:
    """Safely inventory all members of an archive or container.

    Limits never abort the whole inventory: a breached limit or a rejected path is recorded in
    ``limitations`` (``CODE:detail``), the offending member is skipped, and ``coverage`` becomes
    ``partial`` (REVA-AI-002/003). Links are recorded in ``links`` and never followed.
    """
    if isinstance(source, bytes):
        stream = io.BytesIO(source)
        fn = filename or "archive"
        archive_size = len(source)
    else:
        path = Path(source).resolve()
        fn = filename or path.name
        archive_size = path.stat().st_size
        stream = open(path, "rb")

    try:
        return _inventory_stream(stream, fn, archive_size)
    finally:
        stream.close()


def _inventory_stream(stream, fn: str, archive_size: int) -> InventoryResult:
    stream.seek(0)
    header = stream.read(512)
    stream.seek(0)

    fmt = detect_format(header, fn)
    members: List[MemberRecord] = []
    links: List[LinkRecord] = []
    limitations: List[str] = []
    total_bytes = 0
    partial = False
    by_extension = _format_from_extension(fn)
    if by_extension and fmt != "binary" and by_extension != fmt:
        limitations.append(f"FORMAT_EXTENSION_MISMATCH:magic={fmt},extension={by_extension}")

    def overall_budget() -> int:
        ratio_cap = max(archive_size, 1) * MAX_OVERALL_COMPRESSION_RATIO
        return min(MAX_UNCOMPRESSED_BYTES, max(ratio_cap, RATIO_CHECK_FLOOR_BYTES))

    if fmt == "zip":
        with zipfile.ZipFile(stream, "r") as zf:
            infolist = zf.infolist()
            if len(infolist) > MAX_MEMBER_COUNT:
                limitations.append(f"MEMBER_COUNT_EXCEEDED:{len(infolist)}>{MAX_MEMBER_COUNT}")
                infolist = infolist[:MAX_MEMBER_COUNT]
                partial = True
            for info in infolist:
                if info.is_dir():
                    continue
                try:
                    norm_path = validate_member_path(info.filename)
                except RevaValidationError as exc:
                    limitations.append(f"PATH_REJECTED:{info.filename}:{exc}")
                    partial = True
                    continue
                if info.file_size > MAX_SINGLE_MEMBER_BYTES:
                    limitations.append(f"MEMBER_EXCEEDED_SIZE:{norm_path}")
                    partial = True
                    continue
                if info.file_size > RATIO_CHECK_FLOOR_BYTES and \
                        info.file_size > max(info.compress_size, 1) * MAX_MEMBER_COMPRESSION_RATIO:
                    ratio = info.file_size // max(info.compress_size, 1)
                    limitations.append(f"COMPRESSION_RATIO_EXCEEDED:{norm_path}:{ratio}:1")
                    partial = True
                    continue
                if total_bytes + info.file_size > overall_budget():
                    limitations.append(f"TOTAL_UNCOMPRESSED_EXCEEDED:{norm_path}")
                    partial = True
                    break
                with zf.open(info) as mf:
                    digest, size, truncated = _hash_stream(mf, info.file_size)
                if truncated:  # declared size lied: never trust the header over the bytes
                    limitations.append(f"MEMBER_SIZE_MISMATCH:{norm_path}")
                    partial = True
                    continue
                total_bytes += size
                members.append(
                    MemberRecord(
                        member_path=norm_path,
                        size_bytes=size,
                        sha256=digest,
                        mtime=float(info.date_time[0]) if info.date_time else None,
                    )
                )

    elif fmt in ("tar", "tar.gz", "tar.bz2", "tar.xz"):
        mode = {"tar.gz": "r:gz", "tar.bz2": "r:bz2", "tar.xz": "r:xz"}.get(fmt, "r:*")
        with tarfile.open(fileobj=stream, mode=mode) as tf:
            count = 0
            for ti in tf:
                if ti.isdir():
                    continue
                count += 1
                if count > MAX_MEMBER_COUNT:
                    limitations.append(f"MEMBER_COUNT_EXCEEDED:>{MAX_MEMBER_COUNT}")
                    partial = True
                    break
                try:
                    norm_path = validate_member_path(ti.name)
                except RevaValidationError as exc:
                    limitations.append(f"PATH_REJECTED:{ti.name}:{exc}")
                    partial = True
                    continue
                if ti.issym() or ti.islnk():
                    links.append(LinkRecord(norm_path, ti.linkname, "symlink" if ti.issym() else "hardlink"))
                    continue
                if not ti.isfile():
                    limitations.append(f"SPECIAL_MEMBER_SKIPPED:{norm_path}")
                    continue
                if ti.size > MAX_SINGLE_MEMBER_BYTES:
                    limitations.append(f"MEMBER_EXCEEDED_SIZE:{norm_path}")
                    partial = True
                    continue
                if total_bytes + ti.size > overall_budget():
                    limitations.append(f"TOTAL_UNCOMPRESSED_EXCEEDED:{norm_path}")
                    partial = True
                    break
                ef = tf.extractfile(ti)
                digest, size, _ = _hash_stream(ef, ti.size) if ef else (hashlib.sha256(b"").hexdigest(), 0, False)
                total_bytes += size
                members.append(
                    MemberRecord(
                        member_path=norm_path,
                        size_bytes=size,
                        sha256=digest,
                        mode=ti.mode,
                        mtime=ti.mtime,
                    )
                )
    else:
        # Single binary file
        stream.seek(0)
        digest, size, _ = _hash_stream(stream, MAX_SINGLE_MEMBER_BYTES)
        members.append(MemberRecord(member_path=fn, size_bytes=size, sha256=digest))
        total_bytes = size

    return InventoryResult(
        container_format=fmt,
        total_members=len(members),
        total_uncompressed_bytes=total_bytes,
        members=members,
        limitations=limitations,
        links=links,
        coverage="partial" if partial else "complete",
    )


def extract_members(
    archive_path: Union[str, Path],
    member_paths: List[str],
    dest_dir: Union[str, Path],
) -> List[str]:
    """Safely extract specified members from archive to destination directory.

    Only regular members that the inventory accepted are written; rejected paths and links are
    never materialized, and every output path is checked to stay inside ``dest_dir``.
    """
    dest = Path(dest_dir).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    extracted: List[str] = []
    target_set = {validate_member_path(p) for p in member_paths}

    inv = inventory_archive(archive_path)
    allowed = {m.member_path for m in inv.members} & target_set

    def out_for(norm: str) -> Path:
        out_path = (dest / norm).resolve()
        if dest not in out_path.parents:
            raise RevaValidationError(f"Member {norm} resolves outside the extraction root")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        return out_path

    if inv.container_format == "zip":
        with zipfile.ZipFile(archive_path, "r") as zf:
            for info in zf.infolist():
                norm = info.filename.replace("\\", "/").strip()
                if norm in allowed and norm not in extracted:
                    with zf.open(info) as src, open(out_for(norm), "wb") as dst:
                        dst.write(src.read())
                    extracted.append(norm)

    elif inv.container_format.startswith("tar"):
        with tarfile.open(archive_path, "r:*") as tf:
            for ti in tf:
                norm = ti.name.replace("\\", "/").strip()
                if norm in allowed and ti.isfile() and norm not in extracted:
                    ef = tf.extractfile(ti)
                    if ef:
                        with open(out_for(norm), "wb") as dst:
                            dst.write(ef.read())
                        extracted.append(norm)

    return extracted
