"""Unit tests for RFC 8785 Canonical JSON (T-101 / OBL-REVA-WK-001-01)."""

import pytest
from reva.core.jcs import canonicalize, canonical_digest, CanonicalizationError

pytestmark = pytest.mark.reva_depth("unit")


@pytest.mark.reva_obligation("OBL-REVA-WK-001-01")
@pytest.mark.reva_case("positive")
def test_jcs_basic_types():
    assert canonicalize(None) == b"null"
    assert canonicalize(True) == b"true"
    assert canonicalize(False) == b"false"
    assert canonicalize(42) == b"42"
    assert canonicalize(-100) == b"-100"
    assert canonicalize("hello world") == b'"hello world"'


@pytest.mark.reva_obligation("OBL-REVA-WK-001-01")
@pytest.mark.reva_case("positive")
def test_jcs_key_sorting():
    # RFC 8785 UTF-16 code unit sorting order test
    data = {
        "\u20ac": "Euro",
        "\r": "CR",
        "\u05f3": "Hebrew Yod",
        "1": "one",
        "\U0001f600": "Grinning face",
        "\u0080": "Padding",
        "\u00f6": "o-umlaut",
    }
    res = canonicalize(data).decode("utf-8")
    # Verify exact key ordering in serialized output
    import json
    keys_order = list(json.loads(res).keys())
    assert keys_order == ["\r", "1", "\u0080", "\u00f6", "\u05f3", "\u20ac", "\U0001f600"]


@pytest.mark.reva_obligation("OBL-REVA-WK-001-01")
@pytest.mark.reva_case("positive")
def test_jcs_escaping():
    assert canonicalize('quote: " and backslash: \\ and newline: \n') == b'"quote: \\" and backslash: \\\\ and newline: \\n"'
    assert canonicalize("\x00\x1f") == b'"\\u0000\\u001f"'


@pytest.mark.reva_obligation("OBL-REVA-WK-001-01")
@pytest.mark.reva_case("boundary")
def test_jcs_float_handling():
    # When allow_float is True
    assert canonicalize(0.0, allow_float=True) == b"0"
    assert canonicalize(123.456, allow_float=True) == b"123.456"

    # Default rejects floats
    with pytest.raises(CanonicalizationError, match="Floats are forbidden"):
        canonicalize(12.34)


@pytest.mark.reva_obligation("OBL-REVA-WK-001-01")
@pytest.mark.reva_case("negative")
def test_jcs_negative_and_malformed():
    with pytest.raises(CanonicalizationError, match="outside IEEE-754"):
        canonicalize(2**60)

    with pytest.raises(CanonicalizationError, match="Dict key must be str"):
        canonicalize({123: "number key"})

    # Cycle detection
    cycle_list = []
    cycle_list.append(cycle_list)
    with pytest.raises(CanonicalizationError, match="Circular reference"):
        canonicalize(cycle_list)

    cycle_dict = {}
    cycle_dict["self"] = cycle_dict
    with pytest.raises(CanonicalizationError, match="Circular reference"):
        canonicalize(cycle_dict)


@pytest.mark.reva_obligation("OBL-REVA-WK-001-01")
@pytest.mark.reva_case("positive")
def test_canonical_digest():
    d1 = canonical_digest({"b": 2, "a": 1})
    d2 = canonical_digest({"a": 1, "b": 2})
    assert d1 == d2
    assert len(d1) == 64
