"""Generate a merged CycloneDX 1.5 SBOM for EOIP (CC3-017, 69-dependency-license-sbom).

Sources, all offline:
* Python distributions of the interpreter running this script (importlib.metadata,
  i.e. ``pip freeze`` equivalent for the active venv);
* npm packages from ``apps/web/package-lock.json`` (lockfileVersion 3);
* container images referenced by ``deploy/docker-compose*.yml`` and
  ``deploy/Containerfile``/``Dockerfile`` ``FROM`` lines.

License classification merges, in priority order: the ``licenses/`` evidence
directory (package-pinned license texts, matched by name), then metadata
declared by the package itself (``License-Expression``, ``License``, or
``License :: OSI Approved`` classifiers). Undetermined licenses are recorded
as ``NOASSERTION``.

Usage:
    python scripts/generate_sbom.py --output sbom.cyclonedx.json --validate

``--validate`` performs structural validation of the generated document
(required CycloneDX fields, unique bom-refs, well-formed purls) and exits
non-zero on failure. Schema validation against the official CycloneDX JSON
schema requires the schema file; see docs/sbom.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import UTC, datetime
from importlib import metadata as importlib_metadata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC_VERSION = "1.5"

_SPDX_HINTS: list[tuple[str, str]] = [
    ("apache license, version 2.0", "Apache-2.0"),
    ("apache license", "Apache-2.0"),
    ("mit license", "MIT"),
    ("permission is hereby granted, free of charge", "MIT"),
    ("bsd 3-clause", "BSD-3-Clause"),
    ("bsd 2-clause", "BSD-2-Clause"),
    ("bsd license", "BSD-3-Clause"),
    ("redistribution and use in source and binary forms", "BSD-3-Clause"),
    ("gnu lesser general public license", "LGPL-3.0-or-later"),
    ("gnu general public license", "GPL-3.0-or-later"),
    ("mozilla public license", "MPL-2.0"),
    ("python software foundation license", "PSF-2.0"),
    ("the unlicense", "Unlicense"),
]

_CLASSIFIER_SPDX = {
    "MIT License": "MIT",
    "Apache Software License": "Apache-2.0",
    "BSD License": "BSD-3-Clause",
    "Python Software Foundation License": "PSF-2.0",
    "GNU General Public License v3 (GPLv3)": "GPL-3.0-only",
    "GNU Lesser General Public License v3 (LGPLv3)": "LGPL-3.0-only",
    "Mozilla Public License 2.0 (MPL 2.0)": "MPL-2.0",
    "The Unlicense (Unlicense)": "Unlicense",
}


def _spdx_from_text(text: str) -> str | None:
    lowered = text.lower()
    for hint, spdx in _SPDX_HINTS:
        if hint in lowered:
            return spdx
    return None


def _normalise_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def load_license_evidence(licenses_dir: Path) -> dict[str, dict]:
    """Map normalised package name -> {spdx, evidence} from the licenses/ dir."""
    evidence: dict[str, dict] = {}
    if not licenses_dir.is_dir():
        return evidence
    pattern = re.compile(r"^(?P<name>.+?)-(?P<version>\d[\d.]*)(?:-(?:LICENSE|COPYING))?\.(?:txt|md)$")
    for path in sorted(licenses_dir.iterdir()):
        if not path.is_file() or path.suffix not in {".txt", ".md"}:
            continue
        match = pattern.match(path.name)
        if not match:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")[:8192]
        entry = {
            "spdx": _spdx_from_text(text) or "NOASSERTION",
            "evidence": f"licenses/{path.name}",
            "evidence_version": match.group("version"),
        }
        evidence.setdefault(_normalise_name(match.group("name")), entry)
    return evidence


def _python_declared_license(meta: importlib_metadata.PackageMetadata) -> str | None:
    expression = (meta.get("License-Expression") or "").strip()
    if expression:
        return expression
    for classifier in meta.get_all("Classifier") or []:
        prefix = "License :: OSI Approved :: "
        if classifier.startswith(prefix):
            tail = classifier[len(prefix):]
            return _CLASSIFIER_SPDX.get(tail, tail)
    declared = (meta.get("License") or "").strip().splitlines()
    if declared:
        return _spdx_from_text(declared[0]) or (declared[0][:64] if len(declared[0]) < 64 else None)
    return None


def collect_python_components(evidence: dict[str, dict]) -> list[dict]:
    components = []
    for dist in importlib_metadata.distributions():
        meta = dist.metadata
        name = meta.get("Name")
        version = dist.version
        if not name or not version:
            continue
        normalised = _normalise_name(name)
        match = evidence.get(normalised)
        spdx = (match or {}).get("spdx") or _python_declared_license(meta) or "NOASSERTION"
        component = {
            "type": "library",
            "bom-ref": f"pkg:pypi/{normalised}@{version}",
            "name": name,
            "version": version,
            "purl": f"pkg:pypi/{normalised}@{version}",
            "licenses": [{"license": {"id": spdx}}] if spdx != "NOASSERTION" else [{"license": {"name": "NOASSERTION"}}],
            "properties": [{"name": "eoip:ecosystem", "value": "pypi"}],
        }
        if match:
            component["properties"].append({"name": "eoip:license_evidence", "value": match["evidence"]})
        components.append(component)
    deduped = {component["bom-ref"]: component for component in components}
    return sorted(deduped.values(), key=lambda c: c["bom-ref"])


def collect_npm_components(lock_path: Path, evidence: dict[str, dict]) -> list[dict]:
    if not lock_path.is_file():
        return []
    document = json.loads(lock_path.read_text(encoding="utf-8"))
    packages = document.get("packages")
    if not isinstance(packages, dict):
        raise TypeError(f"{lock_path} is not a lockfileVersion>=2 lockfile (no 'packages' map)")
    components = []
    for key, entry in sorted(packages.items()):
        if not key:
            continue  # root project entry
        name = key.split("node_modules/")[-1]
        version = entry.get("version")
        if not version:
            continue
        match = evidence.get(_normalise_name(name))
        spdx = (match or {}).get("spdx") or _spdx_from_text(str(entry.get("license", ""))) or "NOASSERTION"
        purl = f"pkg:npm/{name}@{version}"
        component = {
            "type": "library",
            "bom-ref": purl,
            "name": name,
            "version": version,
            "purl": purl,
            "licenses": [{"license": {"id": spdx}}] if spdx != "NOASSERTION" else [{"license": {"name": "NOASSERTION"}}],
            "properties": [
                {"name": "eoip:ecosystem", "value": "npm"},
                {"name": "eoip:dev_dependency", "value": "true" if entry.get("dev") else "false"},
            ],
        }
        if match:
            component["properties"].append({"name": "eoip:license_evidence", "value": match["evidence"]})
        components.append(component)
    return components


def collect_container_components(deploy_dir: Path) -> list[dict]:
    images: dict[str, set[str]] = {}
    image_re = re.compile(r"^\s*image:\s*(?P<image>[^\s#]+)")
    from_re = re.compile(r"^\s*FROM\s+(?P<image>[^\s:@]+(?::[^\s@]+)?(?:@[^\s]+)?)")
    for path in sorted(deploy_dir.glob("docker-compose*.yml")):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = image_re.match(line)
            if match:
                images.setdefault(match.group("image"), set()).add(path.name)
    for path in sorted(deploy_dir.glob("*file")) + sorted(deploy_dir.glob("Dockerfile*")):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = from_re.match(line)
            if match and match.group("image").lower() != "scratch":
                images.setdefault(match.group("image"), set()).add(path.name)
    components = []
    for image in sorted(images):
        name, _, tag = image.partition(":")
        tag = tag or "latest"
        purl = f"pkg:docker/{name}@{tag}"
        components.append({
            "type": "container",
            "bom-ref": purl,
            "name": image,
            "version": tag,
            "purl": purl,
            "properties": [
                {"name": "eoip:ecosystem", "value": "container"},
                {"name": "eoip:referenced_by", "value": ",".join(sorted(images[image]))},
                {"name": "eoip:digest_pinned", "value": "true" if "@sha256:" in image else "false"},
            ],
        })
    return components


def build_sbom(root: Path = PROJECT_ROOT) -> dict:
    evidence = load_license_evidence(root / "licenses")
    components = (
        collect_python_components(evidence)
        + collect_npm_components(root / "apps" / "web" / "package-lock.json", evidence)
        + collect_container_components(root / "deploy")
    )
    return {
        "bomFormat": "CycloneDX",
        "specVersion": SPEC_VERSION,
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(UTC).isoformat(),
            "tools": [{"vendor": "EOIP", "name": "scripts/generate_sbom.py", "version": "1.0.0"}],
            "component": {
                "type": "application",
                "bom-ref": "pkg:generic/eoip@1.0.0rc1",
                "name": "eoip",
                "version": "1.0.0rc1",
                "description": "Enterprise Ontology & Intelligence Platform",
            },
        },
        "components": components,
    }


_PURL_RE = re.compile(r"^pkg:(pypi|npm|docker|oci)/\S+@\S+$")


def validate_sbom(document: dict) -> list[str]:
    """Structural validation; returns a list of problems (empty == valid)."""
    problems: list[str] = []
    if document.get("bomFormat") != "CycloneDX":
        problems.append("bomFormat must be 'CycloneDX'")
    if document.get("specVersion") != SPEC_VERSION:
        problems.append(f"specVersion must be {SPEC_VERSION}")
    if not str(document.get("serialNumber", "")).startswith("urn:uuid:"):
        problems.append("serialNumber must be a urn:uuid")
    metadata = document.get("metadata") or {}
    if "timestamp" not in metadata:
        problems.append("metadata.timestamp missing")
    if not (metadata.get("component") or {}).get("name"):
        problems.append("metadata.component missing")
    components = document.get("components")
    if not isinstance(components, list) or not components:
        problems.append("components must be a non-empty list")
        return problems
    seen: set[str] = set()
    for index, component in enumerate(components):
        for field in ("type", "bom-ref", "name", "version", "purl"):
            if not component.get(field):
                problems.append(f"components[{index}] missing {field}")
        ref = component.get("bom-ref", "")
        if ref in seen:
            problems.append(f"duplicate bom-ref: {ref}")
        seen.add(ref)
        if component.get("purl") and not _PURL_RE.match(component["purl"]):
            problems.append(f"malformed purl: {component['purl']}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="sbom.cyclonedx.json")
    parser.add_argument("--validate", action="store_true", help="structurally validate the generated SBOM")
    args = parser.parse_args(argv)

    document = build_sbom()
    rendered = json.dumps(document, indent=2) + "\n"
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(rendered, encoding="utf-8")

    ecosystems: dict[str, int] = {}
    for component in document["components"]:
        for prop in component["properties"]:
            if prop["name"] == "eoip:ecosystem":
                ecosystems[prop["value"]] = ecosystems.get(prop["value"], 0) + 1
    print(f"SBOM written to {destination} ({len(rendered)} bytes)")
    print("components: " + ", ".join(f"{kind}={count}" for kind, count in sorted(ecosystems.items())))

    if args.validate:
        problems = validate_sbom(document)
        if problems:
            for problem in problems:
                print(f"INVALID: {problem}", file=sys.stderr)
            return 1
        print("structural validation: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
