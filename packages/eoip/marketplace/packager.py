"""Packager: build .eoipkg archives (GAP-MKT-003, GAP-MKT-005).

A ``.eoipkg`` is a zip archive containing:

- ``manifest.json`` — the :class:`PackageManifest`.
- ``payload/...`` — the package's payload files (ontologies, mappings, etc.).
- ``checksums.json`` — SHA-256 checksum of every archive member.

The archive bytes can then be signed with the shared install key via
:mod:`eoip.marketplace.signing`.
"""

from __future__ import annotations

import hashlib
import io
import json
import zipfile

from eoip.marketplace.manifest import PackageManifest

MANIFEST_FILENAME = "manifest.json"
CHECKSUMS_FILENAME = "checksums.json"
PAYLOAD_PREFIX = "payload/"
ARCHIVE_SUFFIX = ".eoipkg"


class PackageBuildError(ValueError):
    """Raised when a package cannot be built or is malformed."""


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_package(
    manifest: PackageManifest,
    payload_files: dict[str, bytes],
) -> bytes:
    """Build a .eoipkg archive as bytes.

    ``payload_files`` maps archive-relative paths (under ``payload/``) to
    their bytes. Raises :class:`PackageBuildError` on path collisions or
    reserved names.
    """

    if not payload_files:
        raise PackageBuildError("package must contain at least one payload file")

    members: dict[str, bytes] = {}
    members[MANIFEST_FILENAME] = manifest.model_dump_json(indent=2).encode("utf-8")

    for rel_path, content in sorted(payload_files.items()):
        normalized = rel_path.replace("\\", "/").lstrip("/")
        if not normalized or ".." in normalized.split("/"):
            raise PackageBuildError(f"invalid payload path: {rel_path!r}")
        if normalized in (MANIFEST_FILENAME, CHECKSUMS_FILENAME):
            raise PackageBuildError(f"payload path collides with reserved name: {normalized}")
        archive_path = f"{PAYLOAD_PREFIX}{normalized}"
        if archive_path in members:
            raise PackageBuildError(f"duplicate payload path: {archive_path}")
        members[archive_path] = content

    members[CHECKSUMS_FILENAME] = json.dumps(
        {name: sha256_hex(data) for name, data in sorted(members.items())},
        indent=2,
        sort_keys=True,
    ).encode("utf-8")

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in sorted(members.items()):
            zf.writestr(name, data)
    return buffer.getvalue()


class PackageReader:
    """Read and verify a .eoipkg archive in memory (GAP-MKT-005)."""

    def __init__(self, archive: bytes) -> None:
        try:
            self._zip = zipfile.ZipFile(io.BytesIO(archive))
            self._zip.getinfo(MANIFEST_FILENAME)
        except (zipfile.BadZipFile, KeyError) as exc:
            raise PackageBuildError("not a valid .eoipkg archive") from exc
        self._archive = archive

    def _read(self, name: str) -> bytes:
        try:
            return self._zip.read(name)
        except KeyError as exc:
            raise PackageBuildError(f"archive missing {name}") from exc

    def manifest(self) -> PackageManifest:
        return PackageManifest.model_validate_json(self._read(MANIFEST_FILENAME))

    def payload_files(self) -> dict[str, bytes]:
        return {
            info.filename[len(PAYLOAD_PREFIX):]: self._zip.read(info.filename)
            for info in self._zip.infolist()
            if info.filename.startswith(PAYLOAD_PREFIX) and not info.is_dir()
        }

    def verify_checksums(self) -> list[str]:
        """Verify every member against ``checksums.json``.

        Returns a list of mismatch descriptions (empty when intact).
        """

        try:
            recorded = json.loads(self._read(CHECKSUMS_FILENAME).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            return [f"unreadable {CHECKSUMS_FILENAME}: {exc}"]
        problems: list[str] = []
        for name, expected in recorded.items():
            try:
                actual = sha256_hex(self._zip.read(name))
            except KeyError:
                problems.append(f"missing member: {name}")
                continue
            if actual != expected:
                problems.append(f"checksum mismatch: {name}")
        return problems
