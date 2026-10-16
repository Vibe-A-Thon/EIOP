"""SBOM/SCA vulnerability and dependency connector (G2-SRC-SBOM-001..004).

Parses SPDX and CycloneDX JSON files into SourceEventV2 envelopes for graph
ingestion. Extracts package/component metadata and known vulnerabilities from
standard SBOM formats.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from eoip.connectors.base import ConnectorHealth, DiscoveredResource, DiscoveryResult, DiscoveryScope
from eoip.contracts.source_event import SourceEventV2, utc_now_iso

logger = logging.getLogger(__name__)


class SBOMConnector:
    """SBOM/SCA vulnerability and dependency connector (G2-SRC-SBOM-001..004).

    Parses SPDX and CycloneDX JSON SBOM files into SourceEventV2 envelopes.
    Provides ``discover``, ``extract_spdx``, ``extract_cyclonedx``,
    ``checkpoint`` and ``health`` methods.
    """

    source_system = "sbom"
    mapper_version = "sbom-json/1.0"

    def __init__(
        self,
        *,
        source_id: str = "sbom-default",
    ) -> None:
        self.source_id = source_id
        self._checkpoint: str | None = None

    def _make_event(
        self,
        record_kind: str,
        record_id: str,
        payload: dict[str, Any],
        version: str | None = None,
    ) -> SourceEventV2:
        captured_at = utc_now_iso()
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        content_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        event_id = hashlib.sha256(
            f"{self.source_system}:{record_kind}:{record_id}:{content_hash}".encode()
        ).hexdigest()
        return SourceEventV2(
            event_id=event_id,
            source_system=self.source_system,
            source_instance_id=self.source_id,
            source_record_id=record_id,
            operation="UPSERT",
            source_version=version or content_hash[:16],
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=content_hash,
            payload=payload,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": record_kind,
            },
        )

    def discover(self, scope: DiscoveryScope | None = None) -> DiscoveryResult:
        """Discover supported SBOM format types."""
        resources = [
            DiscoveredResource(
                resource_id="spdx",
                resource_type="sbom_format",
                name="SPDX JSON",
                metadata={"format_version": "2.3"},
            ),
            DiscoveredResource(
                resource_id="cyclonedx",
                resource_type="sbom_format",
                name="CycloneDX JSON",
                metadata={"format_version": "1.5"},
            ),
        ]
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def extract_spdx(self, path: str | Path) -> list[SourceEventV2]:
        """Parse an SPDX JSON file and return SourceEventV2 envelopes.

        Parameters
        ----------
        path:
            Path to an SPDX JSON SBOM file.

        Returns
        -------
        list[SourceEventV2]
            One event per package declared in the SBOM.
        """
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"SPDX file not found: {path}")

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        events: list[SourceEventV2] = []
        doc_name = data.get("name", file_path.stem)

        packages = data.get("packages", [])
        for pkg in packages:
            if not isinstance(pkg, dict):
                continue
            spdx_id = pkg.get("SPDXID", "")
            pkg_name = pkg.get("name", "unknown")
            pkg_version = pkg.get("versionInfo", "")
            record_id = f"{self.source_id}:spdx:{doc_name}:{spdx_id}"
            payload = {
                "sbom_format": "spdx",
                "document_name": doc_name,
                "spdx_id": spdx_id,
                "package_name": pkg_name,
                "package_version": pkg_version,
                "supplier": pkg.get("supplier"),
                "download_location": pkg.get("downloadLocation"),
                "license_concluded": pkg.get("licenseConcluded"),
                "license_declared": pkg.get("licenseDeclared"),
                "external_refs": pkg.get("externalRefs", []),
            }
            events.append(self._make_event("spdx_package", record_id, payload, pkg_version))

        return events

    def extract_cyclonedx(self, path: str | Path) -> list[SourceEventV2]:
        """Parse a CycloneDX JSON file and return SourceEventV2 envelopes.

        Parameters
        ----------
        path:
            Path to a CycloneDX JSON SBOM file.

        Returns
        -------
        list[SourceEventV2]
            One event per component declared in the SBOM.
        """
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"CycloneDX file not found: {path}")

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        events: list[SourceEventV2] = []
        serial = data.get("serialNumber", file_path.stem)

        components = data.get("components", [])
        for comp in components:
            if not isinstance(comp, dict):
                continue
            comp_type = comp.get("type", "library")
            comp_name = comp.get("name", "unknown")
            comp_version = comp.get("version", "")
            bom_ref = comp.get("bom-ref", f"{comp_name}-{comp_version}")
            record_id = f"{self.source_id}:cyclonedx:{serial}:{bom_ref}"
            payload = {
                "sbom_format": "cyclonedx",
                "serial_number": serial,
                "bom_ref": bom_ref,
                "component_type": comp_type,
                "component_name": comp_name,
                "component_version": comp_version,
                "purl": comp.get("purl"),
                "group": comp.get("group"),
                "publisher": comp.get("publisher"),
                "licenses": comp.get("licenses", []),
                "hashes": comp.get("hashes", []),
            }
            events.append(self._make_event("cyclonedx_component", record_id, payload, comp_version))

        # Extract vulnerabilities if present
        vulnerabilities = data.get("vulnerabilities", [])
        for vuln in vulnerabilities:
            if not isinstance(vuln, dict):
                continue
            vuln_id = vuln.get("id", "unknown")
            record_id = f"{self.source_id}:cyclonedx:{serial}:vuln:{vuln_id}"
            payload = {
                "sbom_format": "cyclonedx",
                "serial_number": serial,
                "vulnerability_id": vuln_id,
                "source": vuln.get("source", {}),
                "ratings": vuln.get("ratings", []),
                "description": vuln.get("description"),
                "recommendation": vuln.get("recommendation"),
                "affects": vuln.get("affects", []),
            }
            events.append(self._make_event("cyclonedx_vulnerability", record_id, payload))

        return events

    def checkpoint(self) -> str | None:
        """Return the current extraction checkpoint."""
        return self._checkpoint

    def health(self) -> ConnectorHealth:
        """Check connector health. Always HEALTHY since no external deps needed."""
        return ConnectorHealth(
            status="HEALTHY",
            checked_at=utc_now_iso(),
            detail="SBOM connector ready (JSON parsing only, no external deps)",
        )
