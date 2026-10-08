"""Unit tests for domain packs (requirements section 37, GAP-DP-001..005)."""

from pathlib import Path

import pytest

from eoip.ontology import packs
from eoip.ontology.packs import (
    DomainPack,
    PackMetadata,
    list_installed_packs,
    load_all_packs,
    load_ontology,
    load_pack,
    validate_pack,
)

PACKS_DIR = packs.DEFAULT_PACKS_DIR
EXPECTED_PACKS = {
    "software-engineering",
    "itsm",
    "bfsi",
    "data-governance",
    "compliance",
    "cybersecurity",
    "healthcare",
    "manufacturing",
}


def test_default_packs_dir_points_at_repo_config():
    assert PACKS_DIR.is_dir()
    assert PACKS_DIR.name == "domain-packs"
    assert (PACKS_DIR.parent / "ontology" / "ontology-v0.2.0.yaml").is_file()


def test_all_eight_packs_are_installed():
    metas = list_installed_packs()
    assert {m.name for m in metas} == EXPECTED_PACKS
    for meta in metas:
        assert meta.extends == "core"
        assert meta.version
        assert meta.description


def test_all_packs_load_and_validate_cleanly():
    loaded = load_all_packs()
    assert {p.metadata.name for p in loaded} == EXPECTED_PACKS
    for pack in loaded:
        result = validate_pack(pack)
        assert result.valid, result.conflicts
        assert result.conflicts == []


def test_loaded_packs_are_pydantic_models_with_classes_and_validators():
    for pack in load_all_packs():
        assert isinstance(pack, DomainPack)
        assert isinstance(pack.metadata, PackMetadata)
        assert pack.ontology_version == "0.4.0"
        assert pack.schema_version == "1.2"
        assert pack.classes, f"{pack.metadata.name} declares no classes"
        assert pack.validators, f"{pack.metadata.name} declares no validators"
        for label, cls in pack.classes.items():
            assert cls.label == label
            for prop, ptype in cls.properties.items():
                assert ptype in packs.VALID_PROPERTY_TYPES


def test_load_pack_returns_extensions_for_core_extensions():
    pack, result = load_pack(PACKS_DIR / "software-engineering")
    assert "class:WorkItem" in result.extensions
    assert "property:WorkItem.story_points" not in result.extensions  # new key


def test_list_installed_packs_missing_dir_returns_empty(tmp_path):
    assert list_installed_packs(tmp_path / "nope") == []


def _write_pack(root: Path, name: str, ontology: str) -> Path:
    pack_dir = root / name
    pack_dir.mkdir(parents=True)
    (pack_dir / packs.METADATA_FILENAME).write_text(
        f'name: {name}\nversion: "1.0.0"\nextends: core\ndescription: bad fixture\n',
        encoding="utf-8",
    )
    (pack_dir / packs.ONTOLOGY_FILENAME).write_text(ontology, encoding="utf-8")
    return pack_dir


BAD_COLLIDING_CLASS = """\
ontology_version: "0.4.0"
schema_version: "1.2"
domains: [WORK]
classes:
  WorkItem:
    description: Re-defines a core class without extends_core.
    properties:
      story_points: INT
validators: []
"""

BAD_PROPERTY_TYPE = """\
ontology_version: "0.4.0"
schema_version: "1.2"
domains: [WORK]
classes:
  MyThing:
    properties:
      name: INT
validators: []
"""

BAD_CORE_EXTENSION = """\
ontology_version: "0.4.0"
schema_version: "1.2"
domains: [WORK]
classes:
  WorkItem:
    extends_core: true
    properties:
      status: INT
validators: []
"""


def test_class_collision_detected(tmp_path):
    pack_dir = _write_pack(tmp_path, "bad-class", BAD_COLLIDING_CLASS)
    pack = load_ontology(pack_dir, packs.load_metadata(pack_dir))
    result = validate_pack(pack)
    assert not result.valid
    assert any(c.kind == "class" and c.name == "WorkItem" for c in result.conflicts)
    with pytest.raises(ValueError, match="failed validation"):
        load_pack(pack_dir)


def test_property_type_collision_with_core_detected(tmp_path):
    pack_dir = _write_pack(tmp_path, "bad-prop", BAD_PROPERTY_TYPE)
    pack = load_ontology(pack_dir, packs.load_metadata(pack_dir))
    result = validate_pack(pack)
    assert not result.valid
    assert any(
        c.kind == "property" and c.name == "MyThing.name" for c in result.conflicts
    )


def test_core_extension_with_conflicting_property_type_detected(tmp_path):
    pack_dir = _write_pack(tmp_path, "bad-ext", BAD_CORE_EXTENSION)
    pack = load_ontology(pack_dir, packs.load_metadata(pack_dir))
    result = validate_pack(pack)
    assert not result.valid
    assert any(
        c.kind == "property" and c.name == "WorkItem.status" for c in result.conflicts
    )


def test_good_fixture_pack_passes(tmp_path):
    pack_dir = _write_pack(
        tmp_path,
        "good-fixture",
        """\
ontology_version: "0.4.0"
schema_version: "1.2"
domains: [WORK]
classes:
  WorkItem:
    extends_core: true
    properties:
      story_points: INT
  Widget:
    properties:
      widget_id: TEXT
    relationships:
      LINKS_TO:
        out: [Widget]
        in: [WorkItem]
validators:
  - id: GAP-DP-T-001
    applies_to: [Widget]
    severity: WARNING
""",
    )
    pack, result = load_pack(pack_dir)
    assert result.valid
    assert "class:WorkItem" in result.extensions
    assert pack.classes["Widget"].relationships["LINKS_TO"].in_ == ["WorkItem"]
