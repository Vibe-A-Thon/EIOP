"""Shipped-artifact provenance, VCS commit extraction, and SBOM generation (T-402 / REVA-SP-001..012)."""

from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class ComponentInfo:
    name: str
    version: str
    ecosystem: str  # maven | npm | pypi | cargo | golang | oci | generic
    purl: str
    licenses: List[str] = field(default_factory=list)
    sha256: Optional[str] = None
    direct: bool = True
    dependencies: List[str] = field(default_factory=list)


@dataclass
class ProvenanceRecord:
    commit_sha: Optional[str] = None
    branch: Optional[str] = None
    build_time: Optional[str] = None
    dirty: bool = False
    builder: Optional[str] = None
    components: List[ComponentInfo] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def extract_jvm_provenance(zip_file: zipfile.ZipFile) -> ProvenanceRecord:
    """Extract provenance and component dependencies from JAR/WAR/EAR archive."""
    commit_sha = None
    branch = None
    build_time = None
    dirty = False
    components: List[ComponentInfo] = []

    # 1. Inspect git.properties if present
    for name in zip_file.namelist():
        if name.endswith("git.properties"):
            try:
                with zip_file.open(name) as f:
                    content = f.read().decode("utf-8", errors="replace")
                for line in content.splitlines():
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip()
                        if k in ("git.commit.id", "git.commit.id.full"):
                            commit_sha = v
                        elif k == "git.branch":
                            branch = v
                        elif k == "git.commit.time":
                            build_time = v
                        elif k == "git.dirty":
                            dirty = (v.lower() == "true")
            except Exception:
                pass

    # 2. Inspect pom.properties
    for name in zip_file.namelist():
        if "pom.properties" in name:
            try:
                with zip_file.open(name) as f:
                    content = f.read().decode("utf-8", errors="replace")
                props: Dict[str, str] = {}
                for line in content.splitlines():
                    if "=" in line:
                        k, v = line.split("=", 1)
                        props[k.strip()] = v.strip()
                group = props.get("groupId", "unknown")
                artifact = props.get("artifactId", "unknown")
                version = props.get("version", "unknown")
                purl = f"pkg:maven/{group}/{artifact}@{version}"
                components.append(
                    ComponentInfo(
                        name=f"{group}:{artifact}",
                        version=version,
                        ecosystem="maven",
                        purl=purl,
                    )
                )
            except Exception:
                pass

    # 3. Inspect MANIFEST.MF
    manifest_props: Dict[str, str] = {}
    if "META-INF/MANIFEST.MF" in zip_file.namelist():
        try:
            with zip_file.open("META-INF/MANIFEST.MF") as f:
                content = f.read().decode("utf-8", errors="replace")
            for line in content.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    manifest_props[k.strip()] = v.strip()
            if not commit_sha:
                commit_sha = manifest_props.get("Implementation-Build") or manifest_props.get("Git-Commit")
        except Exception:
            pass

    return ProvenanceRecord(
        commit_sha=commit_sha,
        branch=branch,
        build_time=build_time,
        dirty=dirty,
        builder=manifest_props.get("Built-By") or manifest_props.get("Created-By"),
        components=components,
        metadata={"manifest": manifest_props},
    )


def extract_npm_provenance(package_json_bytes: bytes, lockfile_bytes: Optional[bytes] = None) -> ProvenanceRecord:
    """Extract provenance and dependencies from npm package.json and lockfile."""
    try:
        pkg = json.loads(package_json_bytes.decode("utf-8"))
    except Exception:
        pkg = {}

    pkg.get("name", "unknown")
    pkg.get("version", "0.0.0")
    commit_sha = pkg.get("gitHead")

    components: List[ComponentInfo] = []
    # Add dependencies from package.json
    deps = pkg.get("dependencies", {})
    for dep_name, dep_ver in deps.items():
        components.append(
            ComponentInfo(
                name=dep_name,
                version=dep_ver.lstrip("^~"),
                ecosystem="npm",
                purl=f"pkg:npm/{dep_name}@{dep_ver.lstrip('^~')}",
            )
        )

    return ProvenanceRecord(
        commit_sha=commit_sha,
        components=components,
        metadata={"package_json": pkg},
    )


def extract_python_provenance(metadata_text: str, direct_url_json: Optional[str] = None) -> ProvenanceRecord:
    """Extract provenance from Python distribution dist-info."""
    name = "unknown"
    version = "0.0.0"
    for line in metadata_text.splitlines():
        if line.startswith("Name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("Version:"):
            version = line.split(":", 1)[1].strip()

    commit_sha = None
    if direct_url_json:
        try:
            d = json.loads(direct_url_json)
            vcs_info = d.get("vcs_info", {})
            commit_sha = vcs_info.get("commit_id")
        except Exception:
            pass

    return ProvenanceRecord(
        commit_sha=commit_sha,
        components=[
            ComponentInfo(
                name=name,
                version=version,
                ecosystem="pypi",
                purl=f"pkg:pypi/{name}@{version}",
            )
        ],
    )


def export_cyclonedx_sbom(provenance: ProvenanceRecord) -> Dict[str, Any]:
    """Generate CycloneDX 1.5 JSON SBOM representation."""
    components = []
    for c in provenance.components:
        components.append({
            "type": "library",
            "name": c.name,
            "version": c.version,
            "purl": c.purl,
        })

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "name": "artifact",
                "version": "1.0.0",
            },
            "properties": [
                {"name": "reva:commit_sha", "value": provenance.commit_sha or ""},
                {"name": "reva:dirty", "value": str(provenance.dirty)},
            ],
        },
        "components": components,
    }


def export_spdx_sbom(provenance: ProvenanceRecord, document_name: str = "REVA-SBOM") -> Dict[str, Any]:
    """Generate SPDX 2.3 JSON SBOM representation."""
    packages = []
    for idx, c in enumerate(provenance.components):
        spdx_id = f"SPDXRef-Package-{idx + 1}"
        packages.append({
            "SPDXID": spdx_id,
            "name": c.name,
            "versionInfo": c.version,
            "externalRefs": [
                {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": c.purl,
                }
            ],
        })

    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": document_name,
        "packages": packages,
    }
