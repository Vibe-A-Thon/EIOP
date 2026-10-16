"""Packager: build .eoipkg archives (GAP-MKT-002..006).

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
from typing import Any

from eoip.marketplace.manifest import CapabilityKind, PackageManifest

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


# ---------------------------------------------------------------------------
# Specialized Package Builders (GAP-MKT-002..006)
# ---------------------------------------------------------------------------

def package_connector_mapping(
    name: str,
    version: str,
    mapping_id: str,
    mapping_payload: dict[str, Any] | str,
    description: str = "",
) -> bytes:
    """Package connector mappings (GAP-MKT-002)."""
    content = (
        json.dumps(mapping_payload, indent=2).encode("utf-8")
        if isinstance(mapping_payload, dict)
        else mapping_payload.encode("utf-8")
    )
    manifest = PackageManifest(
        id=f"urn:eoip:marketplace:package:{name}",
        name=name,
        version=version,
        description=description or f"Connector mapping for {mapping_id}",
        provides={CapabilityKind.MAPPINGS: [mapping_id]},
    )
    return build_package(manifest, {f"mappings/{mapping_id}.json": content})


def package_query_template(
    name: str,
    version: str,
    template_id: str,
    query_text: str,
    description: str = "",
) -> bytes:
    """Package query templates (GAP-MKT-003)."""
    manifest = PackageManifest(
        id=f"urn:eoip:marketplace:package:{name}",
        name=name,
        version=version,
        description=description or f"Query template {template_id}",
        provides={CapabilityKind.QUERY_TEMPLATES: [template_id]},
    )
    return build_package(manifest, {f"query_templates/{template_id}.sql": query_text.encode("utf-8")})


def package_validation_rules(
    name: str,
    version: str,
    validator_id: str,
    rules: dict[str, Any] | str,
    description: str = "",
) -> bytes:
    """Package validation rules (GAP-MKT-004)."""
    content = (
        json.dumps(rules, indent=2).encode("utf-8")
        if isinstance(rules, dict)
        else rules.encode("utf-8")
    )
    manifest = PackageManifest(
        id=f"urn:eoip:marketplace:package:{name}",
        name=name,
        version=version,
        description=description or f"Validation rules for {validator_id}",
        provides={CapabilityKind.VALIDATORS: [validator_id]},
    )
    return build_package(manifest, {f"validators/{validator_id}.json": content})


def package_agent_workflow(
    name: str,
    version: str,
    workflow_id: str,
    workflow_spec: dict[str, Any] | str,
    description: str = "",
) -> bytes:
    """Package agent workflows (GAP-MKT-005)."""
    content = (
        json.dumps(workflow_spec, indent=2).encode("utf-8")
        if isinstance(workflow_spec, dict)
        else workflow_spec.encode("utf-8")
    )
    manifest = PackageManifest(
        id=f"urn:eoip:marketplace:package:{name}",
        name=name,
        version=version,
        description=description or f"Agent workflow for {workflow_id}",
        provides={CapabilityKind.AGENT_WORKFLOWS: [workflow_id]},
    )
    return build_package(manifest, {f"agent_workflows/{workflow_id}.json": content})


def package_dashboard(
    name: str,
    version: str,
    dashboard_id: str,
    dashboard_spec: dict[str, Any] | str,
    description: str = "",
) -> bytes:
    """Package dashboards (GAP-MKT-006)."""
    content = (
        json.dumps(dashboard_spec, indent=2).encode("utf-8")
        if isinstance(dashboard_spec, dict)
        else dashboard_spec.encode("utf-8")
    )
    manifest = PackageManifest(
        id=f"urn:eoip:marketplace:package:{name}",
        name=name,
        version=version,
        description=description or f"Dashboard layout for {dashboard_id}",
        provides={CapabilityKind.DASHBOARDS: [dashboard_id]},
    )
    return build_package(manifest, {f"dashboards/{dashboard_id}.json": content})


class PackageReader:
    """Read and verify a .eoipkg archive in memory (GAP-MKT-002..008)."""

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

    def get_mappings(self) -> dict[str, str]:
        """Extract connector mappings from payload (GAP-MKT-002)."""
        return {
            path: data.decode("utf-8")
            for path, data in self.payload_files().items()
            if path.startswith("mappings/")
        }

    def get_query_templates(self) -> dict[str, str]:
        """Extract query templates from payload (GAP-MKT-003)."""
        return {
            path: data.decode("utf-8")
            for path, data in self.payload_files().items()
            if path.startswith("query_templates/")
        }

    def get_validators(self) -> dict[str, str]:
        """Extract validator rules from payload (GAP-MKT-004)."""
        return {
            path: data.decode("utf-8")
            for path, data in self.payload_files().items()
            if path.startswith("validators/")
        }

    def get_agent_workflows(self) -> dict[str, str]:
        """Extract agent workflows from payload (GAP-MKT-005)."""
        return {
            path: data.decode("utf-8")
            for path, data in self.payload_files().items()
            if path.startswith("agent_workflows/")
        }

    def get_dashboards(self) -> dict[str, str]:
        """Extract dashboards from payload (GAP-MKT-006)."""
        return {
            path: data.decode("utf-8")
            for path, data in self.payload_files().items()
            if path.startswith("dashboards/")
        }
