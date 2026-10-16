"""Property-Based and Fuzz Testing Suite (TEST-003).

Uses Hypothesis to verify mathematical invariants, round-trip fidelity,
and security boundaries under pseudo-random adversarial inputs:
- Token Format Serialization Round-Trip Invariants
- Dynamic Guardrail and Boundary Rule Invariants
- PII Masking and Anonymization Invariants
- Graph Ingestion Validation Invariants
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from eoip.privacy.scanner import Anonymizer, PIIScanner, PIIType, Pseudonymizer
from eoip.token_formats.engine import (
    ASONStrategy,
    LEANStrategy,
    TokenFormatEngine,
    TOONStrategy,
    TRONStrategy,
    TSONStrategy,
    ZONStrategy,
    ZOONStrategy,
)
from eoip.validation.gate import MutationBlocked, check_vertex


# Primitive and nested JSON-compatible strategy
json_primitives = st.one_of(
    st.text(min_size=1, max_size=40),
    st.integers(min_value=-100000, max_value=100000),
    st.floats(min_value=-10000.0, max_value=10000.0, allow_nan=False, allow_infinity=False),
    st.booleans(),
)

json_objects = st.recursive(
    json_primitives,
    lambda children: st.one_of(
        st.lists(children, max_size=5),
        st.dictionaries(st.text(min_size=1, max_size=15), children, max_size=5),
    ),
    max_leaves=10,
)


@pytest.mark.req("TEST-003")
class TestPropertyTokenFormatSerialization:
    """Hypothesis tests for Token Format round-trip fidelity & token sizing."""

    @settings(max_examples=25)
    @given(payload=st.dictionaries(st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789_", min_size=1, max_size=10), st.integers(), min_size=1, max_size=5))
    def test_toon_serialization_round_trip(self, payload: dict):
        engine = TokenFormatEngine()
        serialized = engine.serialize(payload, "TOON")
        assert isinstance(serialized, str)
        assert len(serialized) > 0
        recovered = engine.deserialize(serialized, "TOON")
        assert recovered == payload

    @settings(max_examples=25)
    @given(payload=st.dictionaries(st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789_", min_size=1, max_size=10), st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789_ ", min_size=1, max_size=20), min_size=1, max_size=5))
    def test_tron_serialization_round_trip(self, payload: dict):
        engine = TokenFormatEngine()
        serialized = engine.serialize(payload, "TRON")
        assert isinstance(serialized, str)
        recovered = engine.deserialize(serialized, "TRON")
        assert recovered == payload

    @settings(max_examples=25)
    @given(payload=st.dictionaries(st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789_", min_size=1, max_size=10), st.booleans(), min_size=1, max_size=5))
    def test_lean_serialization_round_trip(self, payload: dict):
        engine = TokenFormatEngine()
        serialized = engine.serialize(payload, "LEAN")
        recovered = engine.deserialize(serialized, "LEAN")
        assert recovered == payload

    @settings(max_examples=25)
    @given(payload=st.dictionaries(st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789_", min_size=1, max_size=10), st.integers(), min_size=1, max_size=5))
    def test_all_formats_token_compression_ratio(self, payload: dict):
        engine = TokenFormatEngine()
        for fmt in ["TOON", "TRON", "LEAN", "ASON", "ZON", "ZOON", "TSON"]:
            ratio = engine.get_strategy(fmt).compression_ratio(payload)
            assert ratio is not None


class TestPropertyPrivacyAnonymization:
    """Hypothesis tests for PII masking invariants."""

    @settings(max_examples=25)
    @given(email_user=st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789", min_size=2, max_size=15),
           domain=st.sampled_from(["example.com", "test.org", "enterprise.net"]))
    def test_email_masking_never_leaks_full_address(self, email_user: str, domain: str):
        full_email = f"{email_user}@{domain}"
        scanner = PIIScanner()
        anonymizer = Anonymizer()

        findings = scanner.scan_properties("usr_prop", {"email": full_email})
        assert len(findings) == 1
        assert findings[0].pii_type == PIIType.EMAIL

        masked = anonymizer.mask(full_email, PIIType.EMAIL)
        assert full_email != masked
        assert masked.startswith(email_user[0])
        assert f"@{domain}" in masked

    @settings(max_examples=20)
    @given(ssn_digits=st.integers(min_value=100000000, max_value=999999999))
    def test_ssn_masking_always_preserves_last_four_only(self, ssn_digits: int):
        s = str(ssn_digits)
        ssn_str = f"{s[:3]}-{s[3:5]}-{s[5:]}"
        anonymizer = Anonymizer()
        masked = anonymizer.mask(ssn_str, PIIType.SSN)
        assert masked == f"***-**-{s[5:]}"


class TestPropertyOntologyGate:
    """Hypothesis tests for ontology mutation validation."""

    @settings(max_examples=25)
    @given(random_label=st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=5, max_size=15))
    def test_random_unregistered_label_always_blocked(self, random_label: str):
        with pytest.raises(MutationBlocked):
            check_vertex(random_label, {"canonical_id": "cid_123"})
