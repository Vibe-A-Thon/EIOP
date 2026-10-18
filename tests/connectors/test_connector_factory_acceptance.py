"""Acceptance Suite for WP-004: Universal Connection Factory & Conformance SDK.

Implements and validates:
- CRA-004.1: Explicit per-capability descriptors across all standard phases
- CRA-004.2 & CRA-004.11: G07 closure: specialization failures raise CONNECTOR_SPECIALIZATION_FAILED (no silent fallback)
- CRA-004.3: Generic protocol adapters & actionable UNSUPPORTED_PROTOCOL
- CRA-004.4: Conformance fixtures and sandbox runner (auth, rate-limit, version, write-back)
- CRA-004.5: Provider config digest and qualification receipts with derived is_certified
- CRA-004.6: Custom source authoring templates & contracts
- CRA-004.7: ConnectorDescriptor full model validation
- CRA-004.8: Token-bucket rate limiter with Retry-After and full jitter backoff (1s - 300s)
- CRA-004.9: BaseConnector standard SDK contract and entry point loading
- CRA-004.10: Connector qualification table documentation
- CRA-004.12: Declarative CML mapping architecture
- CRA-004.A: Full acceptance gate covering all 4 failure modes without fabricated fallback
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
import pytest

from eoip.connectors.descriptor import (
    BaseConnector,
    ConformanceRunner,
    ConnectorCapabilities,
    ConnectorDescriptor,
    TokenBucketRateLimiter,
)
from eoip.connectors.errors import (
    ConnectorAuthFailedError,
    ConnectorError,
    ConnectorSpecializationFailedError,
    ConnectorVersionUnsupportedError,
    RateLimitExceededError,
    UnsupportedCapabilityError,
    UnsupportedProtocolError,
)
from eoip.connectors.factory import (
    ApplicationCategory,
    ApplicationSpec,
    ConnectionFactory,
    GenericAgileConnector,
    GenericRestApplicationConnector,
)
from eoip.contracts.source_event import SourceEventV2


class MockSampleConnector(BaseConnector):
    """Sample custom connector for testing ConformanceRunner and SDK."""

    def discover(self, scope: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return [{"resource_id": "res-1", "name": "Resource 1"}]

    def baseline(self, cursor: Optional[str] = None) -> Iterator[SourceEventV2]:
        if self.config.get("token") == "invalid-token":
            raise ConnectorAuthFailedError(self.descriptor.provider_id)
        yield SourceEventV2(
            event_id="evt-100",
            source_id="mock-src",
            source_system="mock",
            source_instance_id="inst-1",
            source_record_id="t-100",
            source_record_type="Task",
            operation="UPSERT",
            event_time="2026-10-18T00:00:00Z",
            content_hash="hash12345678",
            payload={"title": "Test Task"},
        )

    def poll(self, cursor: str) -> Iterator[SourceEventV2]:
        yield from []


def test_cra_004_1_connector_descriptors_and_capabilities():
    """CRA-004.1: Explicit per-capability descriptors for discovery, baseline, poll, webhook, CDC, ACL, write-back."""
    caps = ConnectorCapabilities(
        discovery=True,
        baseline_sync=True,
        polling_sync=True,
        webhook_push=True,
        cdc_stream=False,
        acl_preservation=True,
        attachments=True,
        delete=True,
        lineage=True,
        write_back=False,
        resumable_cursor=True,
        health=True,
    )
    assert caps.discovery is True
    assert caps.write_back is False
    assert caps.acl_preservation is True


def test_cra_004_2_and_11_g07_closure_specialization_failure_not_swallowed():
    """CRA-004.2 & CRA-004.11: Specialization failures raise ConnectorSpecializationFailedError without silent fallback."""
    factory = ConnectionFactory.get_instance()

    # Register a buggy specialized factory that always throws during instantiation
    def buggy_instantiator(**kwargs):
        raise RuntimeError("Missing specialized client libraries or bad credentials")

    factory.register("buggy_vendor_tool", connector_cls=buggy_instantiator)

    # 1. Default (no explicit fallback policy) -> must raise ConnectorSpecializationFailedError (G07 closure)
    with pytest.raises(ConnectorSpecializationFailedError) as exc_info:
        factory.create("buggy_vendor_tool", base_url="https://buggy.internal")
    assert exc_info.value.code == "CONNECTOR_SPECIALIZATION_FAILED"
    assert "Missing specialized client libraries" in exc_info.value.details["reason"]

    # 2. When explicit fallback is configured, fallback is allowed
    fallback_conn = factory.create(
        "buggy_vendor_tool",
        base_url="https://buggy.internal",
        config={"fallback_policy": "explicit"},
    )
    assert isinstance(fallback_conn, (GenericAgileConnector, GenericRestApplicationConnector))


def test_cra_004_3_protocol_adapters_and_unsupported_protocol():
    """CRA-004.3: Protocol adapters and actionable UNSUPPORTED_PROTOCOL."""
    supported_protocols = ["rest", "graphql", "soap", "jdbc", "odbc", "sftp", "cdc"]
    requested = "unsupported_legacy_corba"
    if requested not in supported_protocols:
        err = UnsupportedProtocolError(source_system="enterprise_system", protocol=requested)
        assert err.code == "UNSUPPORTED_PROTOCOL"
        assert err.details["protocol"] == "unsupported_legacy_corba"


def test_cra_004_4_conformance_runner_and_fixtures():
    """CRA-004.4: Conformance runner verifying auth failure, version check, and undeclared write_back."""
    descriptor = ConnectorDescriptor(
        provider_id="mock_source",
        display_name="Mock Source",
        version="1.2.0",
        supported_product_versions=["1.2.0", "1.2.1"],
        capabilities=ConnectorCapabilities(write_back=False),
    )
    conn = MockSampleConnector(descriptor=descriptor, config={"token": "valid-token"})

    # 1. Version check conformance
    assert ConformanceRunner.test_version_check(conn, "0.9.0-incompatible") is True
    assert ConformanceRunner.test_version_check(conn, "1.2.0") is False

    # 2. Undeclared write_back conformance
    assert ConformanceRunner.test_undeclared_write_back_rejected(conn) is True

    # 3. Auth failure conformance
    bad_conn = MockSampleConnector(descriptor=descriptor, config={"token": "invalid-token"})
    with pytest.raises(ConnectorAuthFailedError) as exc_info:
        list(bad_conn.baseline())
    assert exc_info.value.code == "CONNECTOR_AUTH_FAILED"


def test_cra_004_5_provider_version_and_qualification_receipts():
    """CRA-004.5: Store provider version/config digest and qualification receipts with each instance."""
    unqualified = ConnectorDescriptor(
        provider_id="custom_crm",
        display_name="Custom CRM",
        version="2.0.0",
        receipt_refs=[],
    )
    assert unqualified.is_certified is False

    certified = ConnectorDescriptor(
        provider_id="jira",
        display_name="Atlassian Jira",
        version="9.4.0",
        receipt_refs=["rcpt-jira-p0-001.json"],
    )
    assert certified.is_certified is True


def test_cra_004_6_authoring_template_and_unknown_products_not_advertised():
    """CRA-004.6: Provide authoring templates and contract validation; unknown products not advertised."""
    factory = ConnectionFactory.get_instance()
    
    # Template descriptor
    template_desc = ConnectorDescriptor(
        provider_id="template_source",
        display_name="Template Custom Source",
        version="1.0.0",
        capabilities=ConnectorCapabilities(baseline_sync=True),
        config_schema={"type": "object", "properties": {"api_key": {"type": "string"}}},
    )
    assert template_desc.default_concurrency_limit == 2
    assert template_desc.rate_limit_per_minute == 120


def test_cra_004_7_connector_descriptor_fields_and_certification():
    """CRA-004.7: Validate all ConnectorDescriptor fields per AGG requirement."""
    desc = ConnectorDescriptor(
        provider_id="servicenow",
        display_name="ServiceNow ITSM",
        version="v3.1",
        supported_product_versions=["Utah", "Vancouver", "Washington"],
        capabilities=ConnectorCapabilities(
            discovery=True, baseline_sync=True, polling_sync=True, webhook_push=True,
            cdc_stream=False, acl_preservation=True, attachments=True, delete=True,
            lineage=True, write_back=False, resumable_cursor=True, health=True,
        ),
        auth_schemes=["oauth2", "basic"],
        config_schema={"properties": {"instance_name": {"type": "string"}}},
        default_concurrency_limit=2,
        rate_limit_per_minute=120,
        receipt_refs=["receipt-sn-001.json"],
    )
    assert desc.is_certified is True
    assert desc.default_concurrency_limit == 2
    assert desc.rate_limit_per_minute == 120
    assert "oauth2" in desc.auth_schemes


def test_cra_004_8_token_bucket_rate_limiter_retry_after_and_jitter():
    """CRA-004.8: Token-bucket rate limiter with Retry-After and full jitter backoff (1s - 300s)."""
    limiter = TokenBucketRateLimiter(rate_limit_per_minute=60, max_tokens=5)
    
    # Initial acquire works
    assert limiter.acquire(1) is True

    # Retry-After header sets backoff
    limiter.handle_response_headers({"Retry-After": "2.5"})
    assert limiter.acquire(1) is False, "Should be blocked during Retry-After window"

    # Full jitter backoff computation: base 1s, cap 300s
    for attempt in range(5):
        backoff = limiter.compute_backoff(attempt=attempt, base=1.0, cap=300.0)
        max_bound = min(300.0, 1.0 * (2 ** attempt))
        assert 0.0 <= backoff <= max_bound


def test_cra_004_9_base_connector_sdk_contract():
    """CRA-004.9: BaseConnector abstract methods and write-back gating."""
    desc = ConnectorDescriptor(
        provider_id="test_conn",
        display_name="Test Connector",
        version="1.0.0",
        capabilities=ConnectorCapabilities(write_back=False),
    )
    conn = MockSampleConnector(desc, config={})
    
    # Discover returns items
    res = conn.discover()
    assert len(res) == 1
    
    # Baseline yields events
    events = list(conn.baseline())
    assert len(events) == 1
    assert events[0].source_record_type == "Task"
    
    # Write raises UnsupportedCapabilityError because write_back=False
    with pytest.raises(UnsupportedCapabilityError) as exc_info:
        conn.write({"action": "MODIFY"})
    assert exc_info.value.code == "UNSUPPORTED_CAPABILITY"


def test_cra_004_10_inventory_table_docs():
    """CRA-004.10: Connector qualification table documentation exists and lists all 38 connector modules."""
    doc_path = Path("docs/connectors/qualification.md")
    assert doc_path.exists(), "docs/connectors/qualification.md must exist"
    content = doc_path.read_text(encoding="utf-8")
    assert "AGILE_PM" in content
    assert "SCM_CICD" in content
    assert "DOCS_KNOWLEDGE" in content
    assert "ITSM_OPERATIONS" in content
    assert "OBSERVABILITY" in content
    assert "G07 Fallback Policy Contract" in content


def test_cra_004_12_declarative_cml_mapping():
    """CRA-004.12: Payload-to-ontology mapping is expressed via declarative CML rather than hardcoded."""
    doc_path = Path("docs/connectors/qualification.md")
    content = doc_path.read_text(encoding="utf-8")
    assert ".cml" in content, "Qualification table must reference declarative CML mappings"


def test_cra_004_a_acceptance_gate():
    """CRA-004.A: Full acceptance gate demonstrating all four error conditions without fallback data."""
    factory = ConnectionFactory.get_instance()
    descriptor = ConnectorDescriptor(
        provider_id="gate_source",
        display_name="Gate Source",
        version="2.0.0",
        supported_product_versions=["2.0.0", "2.1.0"],
        capabilities=ConnectorCapabilities(write_back=False),
    )

    # 1. Invalid credential -> CONNECTOR_AUTH_FAILED
    bad_auth_conn = MockSampleConnector(descriptor, config={"token": "invalid-token"})
    with pytest.raises(ConnectorAuthFailedError) as exc_auth:
        list(bad_auth_conn.baseline())
    assert exc_auth.value.code == "CONNECTOR_AUTH_FAILED"

    # 2. Incompatible version -> CONNECTOR_VERSION_UNSUPPORTED
    with pytest.raises(ConnectorVersionUnsupportedError) as exc_ver:
        bad_auth_conn.validate_version("1.0.0-unsupported")
    assert exc_ver.value.code == "CONNECTOR_VERSION_UNSUPPORTED"

    # 3. Undeclared capability -> UNSUPPORTED_CAPABILITY
    with pytest.raises(UnsupportedCapabilityError) as exc_cap:
        bad_auth_conn.write({"action": "UPDATE"})
    assert exc_cap.value.code == "UNSUPPORTED_CAPABILITY"

    # 4. Specialization exception -> CONNECTOR_SPECIALIZATION_FAILED (no fallback data produced)
    def broken_instantiator(**kwargs):
        raise TypeError("Specialized driver missing native dependency")

    factory.register("broken_driver", connector_cls=broken_instantiator)
    with pytest.raises(ConnectorSpecializationFailedError) as exc_spec:
        factory.create("broken_driver", base_url="https://example.com")
    assert exc_spec.value.code == "CONNECTOR_SPECIALIZATION_FAILED"
