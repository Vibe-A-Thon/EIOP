"""Unit tests for the wave-2 non-IT domain packs (SR-COM-020/021, §19).

Healthcare and manufacturing packs ship at GA (SR-COM-021 "two non-IT
packs"); these tests extend tests/unit/test_domain_packs.py coverage without
modifying it beyond the EXPECTED_PACKS set.
"""

from eoip.ontology import packs
from eoip.ontology.packs import load_pack, validate_pack

PACKS_DIR = packs.DEFAULT_PACKS_DIR

EXPECTED_CLASSES = {
    "healthcare": {"Encounter", "Order", "Drug", "Lot", "Device",
                   "Protocol", "Site"},
    "manufacturing": {"Part", "BOM", "Supplier", "Plant", "WorkOrder",
                      "QualityEvent"},
}


def test_healthcare_pack_loads_and_validates():
    pack, result = load_pack(PACKS_DIR / "healthcare")
    assert result.valid, result.conflicts
    assert {label for label in pack.classes} == EXPECTED_CLASSES["healthcare"]
    assert pack.metadata.name == "healthcare"
    assert pack.metadata.extends == "core"
    assert pack.ontology_version == packs.load_ontology(
        PACKS_DIR / "healthcare", pack.metadata
    ).ontology_version


def test_manufacturing_pack_loads_and_validates():
    pack, result = load_pack(PACKS_DIR / "manufacturing")
    assert result.valid, result.conflicts
    assert {label for label in pack.classes} == EXPECTED_CLASSES["manufacturing"]
    assert pack.metadata.name == "manufacturing"


def test_both_packs_validate_cleanly_via_validate_pack():
    for name in ("healthcare", "manufacturing"):
        pack, _ = load_pack(PACKS_DIR / name)
        result = validate_pack(pack)
        assert result.valid, result.conflicts
        assert result.conflicts == []


def test_healthcare_pack_declares_lot_recall_tracing_relationship():
    pack, _ = load_pack(PACKS_DIR / "healthcare")
    lot = pack.classes["Lot"]
    recall = lot.relationships["RECALL_AFFECTS"]
    assert "Site" in recall.in_
    assert "Protocol" in recall.in_
    assert "Order" in recall.in_
    # Order PRESCRIBES targets Drug and Device (polymorphic target set).
    order = pack.classes["Order"]
    assert {"Drug", "Device"} <= set(order.relationships["PRESCRIBES"].in_)


def test_manufacturing_pack_declares_nonconformance_impact_path():
    pack, _ = load_pack(PACKS_DIR / "manufacturing")
    qe = pack.classes["QualityEvent"]
    assert "Part" in qe.relationships["NONCONFORMING_PART"].in_
    part = pack.classes["Part"]
    assert "BOM" in part.relationships["USED_IN"].in_
    assert "Supplier" in part.relationships["SUPPLIED_BY"].in_
    wo = pack.classes["WorkOrder"]
    assert "BOM" in wo.relationships["EXECUTES"].in_


def test_wave2_packs_have_validators_and_valid_property_types():
    for name in ("healthcare", "manufacturing"):
        pack, _ = load_pack(PACKS_DIR / name)
        assert pack.validators, f"{name} declares no validators"
        for label, cls in pack.classes.items():
            for prop, ptype in cls.properties.items():
                assert ptype in packs.VALID_PROPERTY_TYPES, (label, prop)


def test_wave2_pack_relationship_endpoints_are_known_labels():
    pack, _ = load_pack(PACKS_DIR / "healthcare")
    known = set(pack.classes)
    for cls in pack.classes.values():
        for edge, rel in cls.relationships.items():
            for endpoint in (*rel.out, *rel.in_):
                assert endpoint in known or endpoint == "*", (edge, endpoint)


def test_wave2_packs_extend_core_without_collisions():
    from eoip.ontology import manifest
    for name in ("healthcare", "manufacturing"):
        pack, result = load_pack(PACKS_DIR / name)
        for label in pack.classes:
            assert label not in manifest.VERTEX_LABELS or \
                pack.classes[label].extends_core
