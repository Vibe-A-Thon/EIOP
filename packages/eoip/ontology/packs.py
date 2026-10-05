"""Domain pack loading and validation (GAP-DP-001..005, requirements section 37).

A domain pack is a standalone, ontology-shaped YAML definition that EXTENDS the
core ontology manifest (``packages/eoip/ontology/manifest.py``) with additional
classes (vertex labels with properties), relationships (edge labels with
endpoint constraints) and validators. Packs never replace core terms: a pack
class or property that collides with a core term is a conflict unless it is
explicitly declared as an extension of that core term.

Pack directory layout (see ``config/domain-packs/``)::

    config/domain-packs/<pack-name>/
        pack.yaml      # metadata: name, version, extends, description
        ontology.yaml  # ontology-shaped definition (core schema format)

The ontology file reuses the core ontology schema: ``ontology_version``,
``schema_version``, ``domains`` plus ``classes`` (label -> properties /
relationships) and ``validators`` (declarative validation rules).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from . import manifest

# Requirements section 37 / GAP-DP-005: prebuilt packs ship in the repo.
DEFAULT_PACKS_DIR = Path(__file__).resolve().parents[3] / "config" / "domain-packs"

VALID_PROPERTY_TYPES = {"TEXT", "INT", "LONG", "DOUBLE", "BOOLEAN", "DATE"}

METADATA_FILENAME = "pack.yaml"
ONTOLOGY_FILENAME = "ontology.yaml"


class PackMetadata(BaseModel):
    """pack.yaml descriptor for a domain pack (GAP-DP-001)."""

    name: str
    version: str
    extends: str = "core"
    description: str = ""


class PackClass(BaseModel):
    """A vertex-label extension declared by a pack (GAP-DP-002).

    ``extends_core``: when true, ``label`` must name an existing core vertex
    label and the declared properties/relationships are additive extensions.
    When false, ``label`` must be a new, pack-owned class; a name that matches
    a core label is a collision.
    """

    label: str
    description: str = ""
    extends_core: bool = False
    properties: dict[str, str] = Field(default_factory=dict)
    relationships: dict[str, "PackRelationship"] = Field(default_factory=dict)


class PackRelationship(BaseModel):
    """An edge-label extension declared by a pack (GAP-DP-003)."""

    out: list[str] = Field(default_factory=list)
    in_: list[str] = Field(default_factory=list, alias="in")
    extends_core: bool = False

    model_config = {"populate_by_name": True}


class PackValidator(BaseModel):
    """A declarative validation rule shipped with a pack (GAP-DP-004)."""

    id: str
    description: str = ""
    applies_to: list[str] = Field(default_factory=list)
    severity: str = "WARNING"


class DomainPack(BaseModel):
    """A loaded domain pack: metadata + ontology-shaped definition."""

    metadata: PackMetadata
    ontology_version: str
    schema_version: str
    domains: list[str] = Field(default_factory=list)
    classes: dict[str, PackClass] = Field(default_factory=dict)
    validators: list[PackValidator] = Field(default_factory=list)


class PackConflict(BaseModel):
    """A single collision between a pack and the core ontology."""

    kind: str  # "class" | "property" | "relationship" | "format"
    name: str
    detail: str


class PackValidationResult(BaseModel):
    """Outcome of validating one pack against the core ontology."""

    pack: str
    valid: bool
    conflicts: list[PackConflict] = Field(default_factory=list)
    extensions: list[str] = Field(default_factory=list)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping at the document root")
    return data


def load_metadata(pack_dir: Path) -> PackMetadata:
    """Read and validate ``pack.yaml`` inside a pack directory."""
    path = Path(pack_dir) / METADATA_FILENAME
    if not path.is_file():
        raise FileNotFoundError(f"missing pack metadata file: {path}")
    return PackMetadata.model_validate(_load_yaml(path))


def load_ontology(pack_dir: Path, metadata: PackMetadata) -> DomainPack:
    """Read and validate the ontology-shaped definition inside a pack directory."""
    path = Path(pack_dir) / ONTOLOGY_FILENAME
    if not path.is_file():
        raise FileNotFoundError(f"missing pack ontology file: {path}")
    data = _load_yaml(path)
    classes = {
        label: PackClass(label=label, **spec)
        for label, spec in (data.get("classes") or {}).items()
    }
    validators = [PackValidator.model_validate(v) for v in data.get("validators") or []]
    return DomainPack(
        metadata=metadata,
        ontology_version=str(data.get("ontology_version", "")),
        schema_version=str(data.get("schema_version", "")),
        domains=list(data.get("domains") or []),
        classes=classes,
        validators=validators,
    )


def validate_pack(pack: DomainPack, core: Any = manifest) -> PackValidationResult:
    """Validate a pack against the core ontology manifest (GAP-DP-002..004).

    Rules:
    - format: ``ontology_version``/``schema_version`` must match the core
      manifest versions; declared property types must be valid HugeGraph types.
    - class collision: a pack class whose label matches a core vertex label
      without ``extends_core: true`` conflicts.
    - property collision: a property key already defined in core with a
      different type conflicts; pack-owned classes must not redeclare core
      required properties of the class they extend with different types.
    - relationship collision: an edge label matching a core edge label without
      ``extends_core: true`` conflicts; new edge labels with empty endpoints
      are format errors.
    """
    conflicts: list[PackConflict] = []
    extensions: list[str] = []

    if pack.ontology_version != core.ONTOLOGY_VERSION:
        conflicts.append(PackConflict(
            kind="format", name="ontology_version",
            detail=f"pack declares {pack.ontology_version!r}, core is {core.ONTOLOGY_VERSION!r}",
        ))
    if pack.schema_version != core.SCHEMA_VERSION:
        conflicts.append(PackConflict(
            kind="format", name="schema_version",
            detail=f"pack declares {pack.schema_version!r}, core is {core.SCHEMA_VERSION!r}",
        ))
    if pack.metadata.extends != "core":
        conflicts.append(PackConflict(
            kind="format", name="extends",
            detail=f"pack extends {pack.metadata.extends!r}, only 'core' is supported",
        ))
    for domain in pack.domains:
        if domain not in core.DOMAINS:
            conflicts.append(PackConflict(
                kind="format", name=domain, detail="unknown graph domain",
            ))

    for label, cls in pack.classes.items():
        if label in core.VERTEX_LABELS:
            if not cls.extends_core:
                conflicts.append(PackConflict(
                    kind="class", name=label,
                    detail="label collides with a core vertex label; set extends_core: true "
                           "to declare an additive extension",
                ))
            else:
                extensions.append(f"class:{label}")
        for prop, ptype in cls.properties.items():
            if ptype not in VALID_PROPERTY_TYPES:
                conflicts.append(PackConflict(
                    kind="property", name=f"{label}.{prop}",
                    detail=f"invalid property type {ptype!r}",
                ))
                continue
            core_type = core.PROPERTY_KEYS.get(prop)
            if core_type is not None and core_type != ptype:
                conflicts.append(PackConflict(
                    kind="property", name=f"{label}.{prop}",
                    detail=f"property key collides with core type {core_type!r}, "
                           f"pack declares {ptype!r}",
                ))
            elif core_type == ptype and cls.extends_core:
                extensions.append(f"property:{label}.{prop}")
        for edge, rel in cls.relationships.items():
            spec = core.EDGE_LABELS.get(edge)
            if spec is not None:
                if not rel.extends_core:
                    conflicts.append(PackConflict(
                        kind="relationship", name=edge,
                        detail="edge label collides with a core edge label; set "
                               "extends_core: true to declare an additive extension",
                    ))
                else:
                    extensions.append(f"relationship:{edge}")
            elif not rel.out or not rel.in_:
                conflicts.append(PackConflict(
                    kind="relationship", name=edge,
                    detail="new edge labels must declare non-empty out/in endpoint labels",
                ))
            for endpoint in (*rel.out, *rel.in_):
                known = (
                    endpoint in core.VERTEX_LABELS
                    or endpoint in pack.classes
                    or endpoint == "*"
                )
                if not known:
                    conflicts.append(PackConflict(
                        kind="relationship", name=edge,
                        detail=f"unknown endpoint vertex label {endpoint!r}",
                    ))

    return PackValidationResult(
        pack=pack.metadata.name,
        valid=not conflicts,
        conflicts=conflicts,
        extensions=extensions,
    )


def load_pack(pack_dir: str | Path) -> tuple[DomainPack, PackValidationResult]:
    """Load one pack directory and validate it against the core ontology.

    Raises ``ValueError`` when the pack is invalid; returns the pack and its
    validation result otherwise.
    """
    metadata = load_metadata(pack_dir)
    pack = load_ontology(pack_dir, metadata)
    result = validate_pack(pack)
    if not result.valid:
        details = "; ".join(f"{c.kind}:{c.name} ({c.detail})" for c in result.conflicts)
        raise ValueError(f"domain pack {metadata.name!r} failed validation: {details}")
    return pack, result


def list_installed_packs(packs_dir: str | Path = DEFAULT_PACKS_DIR) -> list[PackMetadata]:
    """List metadata for every installed pack (a subdirectory with pack.yaml)."""
    root = Path(packs_dir)
    if not root.is_dir():
        return []
    metas: list[PackMetadata] = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / METADATA_FILENAME).is_file():
            metas.append(load_metadata(child))
    return metas


def load_all_packs(packs_dir: str | Path = DEFAULT_PACKS_DIR) -> list[DomainPack]:
    """Load and validate every installed pack (GAP-DP-005).

    Invalid packs raise ``ValueError`` so a broken pack can never be silently
    merged into the ontology.
    """
    root = Path(packs_dir)
    packs: list[DomainPack] = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / METADATA_FILENAME).is_file():
            pack, _ = load_pack(child)
            packs.append(pack)
    return packs


__all__ = [
    "DEFAULT_PACKS_DIR",
    "METADATA_FILENAME",
    "ONTOLOGY_FILENAME",
    "VALID_PROPERTY_TYPES",
    "DomainPack",
    "PackClass",
    "PackConflict",
    "PackMetadata",
    "PackRelationship",
    "PackValidationResult",
    "PackValidator",
    "list_installed_packs",
    "load_all_packs",
    "load_metadata",
    "load_ontology",
    "load_pack",
    "validate_pack",
]
