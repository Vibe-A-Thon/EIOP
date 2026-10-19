"""Unit tests for REVA identifiers (T-102 / OBL-REVA-WK-002-01)."""

import pytest
from reva.core.ids import (
    warrant_id,
    artifact_id,
    blob_id,
    gap_id,
    contradiction_id,
    ledger_id,
    normalize_set,
    normalize_question,
    parse_id,
    is_valid_id,
)

pytestmark = pytest.mark.reva_depth("unit")


@pytest.mark.reva_obligation("OBL-REVA-WK-002-01")
@pytest.mark.reva_case("positive")
def test_id_generation_and_prefix():
    wid = warrant_id({"tenant_id": "t1", "op": "test"})
    assert wid.startswith("wr1_")
    assert is_valid_id(wid, "wr")

    aid = artifact_id("a" * 64)
    assert aid.startswith("art1_")
    assert is_valid_id(aid, "art")

    bid = blob_id("b" * 64)
    assert bid.startswith("blb1_")
    assert is_valid_id(bid, "blb")


@pytest.mark.reva_obligation("OBL-REVA-WK-002-01")
@pytest.mark.reva_case("positive")
def test_parse_id():
    prefix, ver, hex_digest = parse_id("wr1_" + "c" * 64)
    assert prefix == "wr"
    assert ver == "1"
    assert hex_digest == "c" * 64


@pytest.mark.reva_obligation("OBL-REVA-WK-002-01")
@pytest.mark.reva_case("negative")
def test_parse_id_invalid():
    with pytest.raises(ValueError, match="Malformed REVA identifier"):
        parse_id("invalid-id")


@pytest.mark.reva_obligation("OBL-REVA-WK-002-01")
@pytest.mark.reva_case("positive")
def test_normalize_question():
    q1 = "   What   is   the IMPACT of service?  "
    q2 = "what is the impact of service?"
    assert normalize_question(q1) == normalize_question(q2)
    assert gap_id("t1", "d", q1, {}) == gap_id("t1", "d", q2, {})


@pytest.mark.reva_obligation("OBL-REVA-WK-002-01")
@pytest.mark.reva_case("positive")
def test_normalize_set():
    s1 = [{"b": 2}, {"a": 1}, {"b": 2}]
    s2 = [{"a": 1}, {"b": 2}]
    assert normalize_set(s1) == normalize_set(s2)
    assert len(normalize_set(s1)) == 2
