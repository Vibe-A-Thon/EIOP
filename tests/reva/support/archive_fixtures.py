"""Deterministic archive fixtures for REVA extractor tests (REVA-AI-001..003, NFR-012).

Every fixture is generated from code (no binary blobs are committed) with fixed timestamps,
owners and member order, so two builds produce byte-identical files. ``build_fixtures``
writes them plus ``manifest.json`` (name -> sha256, expectations) into ``out_dir``.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import tarfile
import zipfile
from pathlib import Path

FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)
FIXED_MTIME = 1577836800  # 2020-01-01T00:00:00Z
BOMB_MEMBER_BYTES = 32 * 1024 * 1024  # 32 MiB of zeros, deflates to ~32 KiB (ratio ~1000:1)

FILES = {
    "src/app.py": b"print('hello')\n",
    "src/util/strings.py": b"def upper(value):\n    return value.upper()\n",
    "README.txt": b"fixture archive\n",
}


def default_cache_dir() -> Path:
    return Path(os.environ.get("REVA_FIXTURE_CACHE", ".reva-fixtures"))


def _zip(members: list[tuple[str, bytes]]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in members:
            info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)
    return buf.getvalue()


def _tar(entries: list[tarfile.TarInfo | tuple[str, bytes]]) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as tf:
        for entry in entries:
            if isinstance(entry, tarfile.TarInfo):
                entry.mtime, entry.uid, entry.gid, entry.uname, entry.gname = FIXED_MTIME, 0, 0, "", ""
                tf.addfile(entry)
                continue
            name, data = entry
            info = tarfile.TarInfo(name)
            info.size, info.mtime, info.mode = len(data), FIXED_MTIME, 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tf.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def _gzip(data: bytes) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0, filename="") as gz:
        gz.write(data)
    return buf.getvalue()


def _symlink(name: str, target: str) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type, info.linkname, info.mode = tarfile.SYMTYPE, target, 0o777
    return info


def fixture_specs() -> dict[str, dict]:
    """name -> {bytes, expect}; ``expect`` is what a correct inventory must report."""
    plain = sorted(FILES.items())
    expected_members = {name: hashlib.sha256(data).hexdigest() for name, data in plain}
    return {
        "plain.zip": {"bytes": _zip(plain), "expect": {"format": "zip", "members": expected_members}},
        "plain.tar.gz": {"bytes": _gzip(_tar(plain)), "expect": {"format": "tar.gz", "members": expected_members}},
        "tar-named-as.zip": {
            "bytes": _tar(plain),
            "expect": {"format": "tar", "members": expected_members, "limitation_prefix": "FORMAT_EXTENSION_MISMATCH"},
        },
        "traversal.zip": {
            "bytes": _zip([("ok.txt", b"fine\n"), ("../escape.txt", b"outside\n")]),
            "expect": {"format": "zip", "members": {"ok.txt": hashlib.sha256(b"fine\n").hexdigest()},
                       "limitation_prefix": "PATH_REJECTED", "coverage": "partial"},
        },
        "absolute.tar": {
            "bytes": _tar([("ok.txt", b"fine\n"), ("/etc/evil.conf", b"x\n")]),
            "expect": {"format": "tar", "members": {"ok.txt": hashlib.sha256(b"fine\n").hexdigest()},
                       "limitation_prefix": "PATH_REJECTED", "coverage": "partial"},
        },
        "symlink-escape.tar": {
            "bytes": _tar([("ok.txt", b"fine\n"), _symlink("link-out", "../../etc/passwd")]),
            "expect": {"format": "tar", "members": {"ok.txt": hashlib.sha256(b"fine\n").hexdigest()},
                       "links": {"link-out": "../../etc/passwd"}},
        },
        "zip-bomb.zip": {
            "bytes": _zip([("ok.txt", b"fine\n"), ("zeros.bin", b"\0" * BOMB_MEMBER_BYTES)]),
            "expect": {"format": "zip", "members": {"ok.txt": hashlib.sha256(b"fine\n").hexdigest()},
                       "limitation_prefix": "COMPRESSION_RATIO_EXCEEDED", "coverage": "partial"},
        },
    }


def build_fixtures(out_dir: Path | str) -> dict:
    """Write every fixture and manifest.json into out_dir; return the manifest."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, spec in sorted(fixture_specs().items()):
        (out / name).write_bytes(spec["bytes"])
        manifest[name] = {"sha256": hashlib.sha256(spec["bytes"]).hexdigest(), "expect": spec["expect"]}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest
