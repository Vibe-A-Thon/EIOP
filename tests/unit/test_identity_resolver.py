import pytest
from eoip.identity.resolver import IdentityResolver


@pytest.mark.req("FR-INGEST-002")
def test_email_resolution():
    resolver = IdentityResolver()
    identity = resolver.resolve_person(display_name="Alice", email="Alice@Example.com", source_system="jira")
    assert identity.canonical_key == "alice@example.com"
    assert identity.resolution_method == "email"
    assert resolver.person_canonical_id(identity) == "urn:eoip:identity:person:email:alice@example.com"


def test_source_id_fallback():
    resolver = IdentityResolver()
    identity = resolver.resolve_person(display_name="Bob", source_id="user-123", source_system="gitlab")
    assert identity.canonical_key == "user-123"
    assert identity.resolution_method == "source_id"


def test_display_name_fallback():
    resolver = IdentityResolver()
    identity = resolver.resolve_person(display_name="Charlie", source_system="jira", record_id="rec-1")
    assert identity.canonical_key == "rec-1:charlie"
    assert identity.resolution_method == "display_name_fallback"


@pytest.mark.req("G2-EKAF-026")
def test_same_person_by_email():
    resolver = IdentityResolver()
    a = resolver.resolve_person(display_name="Alice", email="alice@example.com", source_system="jira")
    b = resolver.resolve_person(display_name="alice_dev", email="ALICE@EXAMPLE.COM", source_system="gitlab")
    assert resolver.is_same_person(a, b)
    assert resolver.person_canonical_id(a) == resolver.person_canonical_id(b)
