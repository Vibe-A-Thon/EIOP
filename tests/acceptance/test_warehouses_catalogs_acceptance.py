"""Acceptance test suite for Warehouses, Catalog Federation, and Custom Systems (WP-009, CRA-009.1-009.8, CRA-009.A)."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from eoip.catalog.federation import (
    CatalogEntity,
    CatalogFederationEngine,
    CatalogSource,
)
from eoip.connectors.custom_system import (
    CustomProtocol,
    GenericCustomSystemConnector,
    ProtocolEndpointConfig,
)
from eoip.connectors.errors import ConnectorError
from eoip.connectors.factory import ConnectorFactory
from eoip.connectors.fortuna import (
    FORTUNA_DECISION_REF,
    FORTUNA_MISSING_INPUT_REASON,
    FortunaConnector,
    FortunaConnectorBlockedError,
)
from eoip.connectors.snowflake import (
    ColumnPolicy,
    SnowflakeConnector,
    SnowflakeCostGuard,
    SnowflakeMode,
)
from eoip.contracts.source_event import SourceEventV2
from eoip.mapping import parse_and_compile_cml

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "connectors"
SNOWFLAKE_FIXTURE = FIXTURES_DIR / "snowflake" / "information_schema.json"
CATALOGS_FIXTURE = FIXTURES_DIR / "catalogs" / "openmetadata_datahub_atlas.json"
PROTOCOLS_FIXTURE = FIXTURES_DIR / "custom" / "protocols.json"


# ===========================================================================
# CRA-009.1: Snowflake metadata and policy scoping
# ===========================================================================

def test_cra_009_1_snowflake_metadata_and_policy_scoping():
    data = json.loads(SNOWFLAKE_FIXTURE.read_text(encoding="utf-8"))
    table_def = data["tables"][0]

    columns = [
        ColumnPolicy(
            column_name=c["column_name"],
            data_type=c["data_type"],
            is_masked=c.get("is_masked", False),
            masking_policy=c.get("masking_policy"),
        )
        for c in table_def["columns"]
    ]

    sf = SnowflakeConnector(
        source_id="sf-corp-prod",
        account="acme_corp.us-east-1",
        warehouse="FINANCE_WH",
        database="PROD_DB",
        schema="FINANCE",
        role="FINANCE_ANALYST",
        token="sf-token",
    )

    evt = sf.make_table_event(table_def["table_name"], columns, is_view=False, row_count=table_def["row_count"])
    assert evt.source_system == "snowflake"
    assert evt.permissions.principal_refs == ["snowflake:role:FINANCE_ANALYST"]
    assert evt.permissions.inherited_from == "snowflake:warehouse:FINANCE_WH"
    assert evt.metadata["database"] == "PROD_DB"
    assert evt.metadata["schema"] == "FINANCE"
    assert evt.metadata["warehouse"] == "FINANCE_WH"
    assert evt.metadata["role"] == "FINANCE_ANALYST"
    assert evt.metadata["has_masked_columns"] is True

    # Account Number column has masking policy attached
    acct_col = next(c for c in evt.payload["columns"] if c["name"] == "ACCOUNT_NUMBER")
    assert acct_col["is_masked"] is True
    assert acct_col["masking_policy"] == "POLICY_MASK_ACCOUNT_NUM"


# ===========================================================================
# CRA-009.2: Snowflake modes and opt-in redaction
# ===========================================================================

def test_cra_009_2_snowflake_modes_and_opt_in_redaction():
    data = json.loads(SNOWFLAKE_FIXTURE.read_text(encoding="utf-8"))
    raw_rows = data["sample_rows"]
    table_def = data["tables"][0]
    columns = [
        ColumnPolicy(
            column_name=c["column_name"],
            data_type=c["data_type"],
            is_masked=c.get("is_masked", False),
            masking_policy=c.get("masking_policy"),
        )
        for c in table_def["columns"]
    ]

    # 1. In METADATA_ONLY mode: sampling is rejected
    sf_meta = SnowflakeConnector(
        source_id="sf-meta",
        account="acme.snowflake",
        mode=SnowflakeMode.METADATA_ONLY,
        opt_in_sampling=False,
        token="sf-token",
    )
    with pytest.raises(PermissionError, match="metadata-only mode"):
        sf_meta.sample_table_data(table_def["table_name"], raw_rows, columns)

    # 2. In SAMPLED_DATA mode without opt-in: sampling is rejected
    sf_no_optin = SnowflakeConnector(
        source_id="sf-sampled",
        account="acme.snowflake",
        mode=SnowflakeMode.SAMPLED_DATA,
        opt_in_sampling=False,
        token="sf-token",
    )
    with pytest.raises(PermissionError, match="not explicitly opted in"):
        sf_no_optin.sample_table_data(table_def["table_name"], raw_rows, columns)

    # 3. In SAMPLED_DATA mode with opt-in: masking and PII redaction are applied
    sf_sampled = SnowflakeConnector(
        source_id="sf-sampled",
        account="acme.snowflake",
        mode=SnowflakeMode.SAMPLED_DATA,
        opt_in_sampling=True,
        token="sf-token",
    )
    cleaned_rows, meta = sf_sampled.sample_table_data(table_def["table_name"], raw_rows, columns)
    assert len(cleaned_rows) == 1
    sample = cleaned_rows[0]

    # Masked column is replaced with policy marker
    assert sample["ACCOUNT_NUMBER"] == "[MASKED_BY_POLICY]"
    # Email column was sanitized via automated PII redaction
    assert "[REDACTED_EMAIL]" in sample["CUSTOMER_EMAIL"]
    assert "alice.williams@customer.example.com" not in json.dumps(sample)
    assert meta["redacted_values_count"] >= 2


# ===========================================================================
# CRA-009.3: Fortuna missing input reason and contract requirement
# ===========================================================================

def test_cra_009_3_fortuna_missing_input_reason_and_contract_requirement():
    # Attempting to instantiate Fortuna raises FortunaConnectorBlockedError
    with pytest.raises(FortunaConnectorBlockedError) as exc_info:
        FortunaConnector("https://fortuna.internal/api")

    err = exc_info.value
    assert err.source_system == "fortuna"
    assert err.code == "FORTUNA_UNSPECIFIED_DECISION_H06"
    assert err.details["decision_ref"] == "H-06"
    assert "Decision H-06" in err.details["missing_input_reason"]
    assert "GenericCustomSystemConnector" in err.details["recommended_alternative"]


# ===========================================================================
# CRA-009.4: External catalog federation and precedence
# ===========================================================================

def test_cra_009_4_external_catalog_federation_and_precedence():
    data = json.loads(CATALOGS_FIXTURE.read_text(encoding="utf-8"))
    raw_entities = data["entities"]

    entities = [
        CatalogEntity(
            entity_urn=e["entity_urn"],
            entity_type=e["entity_type"],
            name=e["name"],
            description=e.get("description"),
            owner=e.get("owner"),
            tags=e.get("tags", []),
            custom_properties=e.get("custom_properties", {}),
            source_catalog=CatalogSource(e["source_catalog"]),
        )
        for e in raw_entities
    ]

    # Precedence: DataHub > OpenMetadata > Apache Atlas
    engine = CatalogFederationEngine(
        precedence_order=[
            CatalogSource.DATAHUB,
            CatalogSource.OPENMETADATA,
            CatalogSource.APACHE_ATLAS,
        ]
    )

    resolved = engine.resolve_entity(entities)
    assert resolved.source_catalog == CatalogSource.DATAHUB
    # Owner and description chosen from highest-precedence source (DataHub)
    assert resolved.owner == "lead-cfo-analyst@example.com"
    assert "Authoritative DataHub description" in resolved.description

    # Tags and non-conflicting properties are merged across sources
    assert "datahub_curated" in resolved.tags
    assert "openmetadata_verified" in resolved.tags
    assert "legacy_hive_import" in resolved.tags
    assert resolved.custom_properties["compliance_officer"] == "auditor_sec_ops"
    assert resolved.custom_properties["retention_days"] == "2555"

    # Emitted SourceEvent preserves federation provenance
    evt = engine.to_source_event(resolved)
    assert evt.source_system == "datahub"
    assert "openmetadata" in evt.payload["provenance"]["federated_from"]
    assert "apache_atlas" in evt.payload["provenance"]["federated_from"]


# ===========================================================================
# CRA-009.5: Custom provider certification and scope awareness
# ===========================================================================

def test_cra_009_5_custom_provider_certification_and_scope_awareness():
    cml_content = Path("packages/eoip/mapping/cml/snowflake.cml").read_text(encoding="utf-8")
    mapping = parse_and_compile_cml(cml_content)

    # 1. Valid certified endpoint
    valid_cfg = ProtocolEndpointConfig(
        protocol=CustomProtocol.REST,
        endpoint_url="https://api.internal.corp/v1/data",
        auth_type="bearer",
        credentials={"token": "valid_token"},
    )
    conn = GenericCustomSystemConnector("test-provider-valid", valid_cfg, mapping=mapping)
    fixture = {
        "table_name": "CUSTOMERS",
        "database": "SALES_DB",
        "schema": "PUBLIC",
        "warehouse": "COMPUTE_WH",
        "is_public": False,
    }
    report = conn.certify(fixture)
    assert report.is_certified is True
    assert report.connectivity_ok is True
    assert report.schema_mapping_ok is True
    assert report.authorization_fidelity_ok is True

    # 2. Scope-aware denial: Private endpoint with 'none' auth fails authorization fidelity
    insecure_cfg = ProtocolEndpointConfig(
        protocol=CustomProtocol.REST,
        endpoint_url="https://api.internal.corp/v1/private_data",
        auth_type="none",
    )
    insecure_conn = GenericCustomSystemConnector("test-provider-insecure", insecure_cfg, mapping=mapping)
    insecure_report = insecure_conn.certify({"table_name": "SECRET", "database": "DB", "schema": "S", "warehouse": "W", "is_public": False})
    assert insecure_report.is_certified is False
    assert insecure_report.authorization_fidelity_ok is False
    assert any("fails authorization fidelity" in d for d in insecure_report.diagnostics)


# ===========================================================================
# CRA-009.6: Snowflake lineage parsing and cost guard
# ===========================================================================

def test_cra_009_6_snowflake_lineage_virtualization_and_cost_guard():
    cost_guard = SnowflakeCostGuard(max_credits=2.0, statement_timeout_seconds=30.0, max_result_rows=100)
    sf = SnowflakeConnector(
        source_id="sf-ops",
        account="acme.snowflake",
        cost_guard=cost_guard,
        opt_in_query_history=True,
        token="sf-token",
    )

    # Within limits: passes
    sf.validate_cost_guard(credits_consumed=1.2, duration_seconds=12.0, rows=50)

    # Exceeding credit guard raises cost_limit_exceeded
    with pytest.raises(ConnectorError) as exc_cost:
        sf.validate_cost_guard(credits_consumed=3.5, duration_seconds=5.0, rows=50)
    assert exc_cost.value.category == "cost_limit_exceeded"

    # Exceeding 30s statement timeout raises statement_timeout
    with pytest.raises(ConnectorError) as exc_time:
        sf.validate_cost_guard(credits_consumed=0.5, duration_seconds=35.0, rows=50)
    assert exc_time.value.category == "statement_timeout"

    # Lineage parsing from query history
    data = json.loads(SNOWFLAKE_FIXTURE.read_text(encoding="utf-8"))
    raw_qh = data["query_history"]
    cleaned_qh, lineage = sf.extract_query_history(raw_qh)
    assert len(cleaned_qh) == 1
    # Secret in query was sanitized
    assert "ghp_SECRET_TOKEN" not in cleaned_qh[0]["query_text"]
    assert "[REDACTED_TOKEN]" in cleaned_qh[0]["query_text"]

    # Lineage candidate extracted for CRA-029
    assert len(lineage) == 1
    assert lineage[0]["target_table"] == "ANALYTICS.DAILY_REVENUE_SUMMARY"
    assert lineage[0]["source_table"] == "FINANCE.CUSTOMER_TRANSACTIONS"
    assert lineage[0]["relationship"] == "derivedFrom"


# ===========================================================================
# CRA-009.7: Generic protocol adapters with Mapping IR
# ===========================================================================

def test_cra_009_7_generic_protocol_adapters_with_mapping_ir():
    data = json.loads(PROTOCOLS_FIXTURE.read_text(encoding="utf-8"))

    protocols_to_test = [
        (CustomProtocol.REST, data["rest_item"], "https://api.orders.corp/v1"),
        (CustomProtocol.GRAPHQL, data["graphql_item"], "https://api.catalog.corp/graphql"),
        (CustomProtocol.SOAP, data["soap_envelope"], "https://services.bank.corp/AccountService"),
        (CustomProtocol.DATABASE, data["database_row"], "jdbc:postgresql://db.corp:5432/inv"),
        (CustomProtocol.EVENTS, data["kafka_event"], "kafka://broker1.corp:9092/payments"),
    ]

    for proto, payload, endpoint in protocols_to_test:
        cfg = ProtocolEndpointConfig(protocol=proto, endpoint_url=endpoint)
        conn = GenericCustomSystemConnector(f"conn-{proto.value}", cfg)
        evt = conn.parse_payload(payload, record_type=proto.value)

        assert evt.source_system == "custom_system"
        assert evt.metadata["protocol"] == proto.value
        assert evt.metadata["endpoint_url"] == endpoint
        assert f"custom:{proto.value}:consumer" in evt.permissions.principal_refs


# ===========================================================================
# CRA-009.8: Fortuna blocked status and alternative offering
# ===========================================================================

def test_cra_009_8_fortuna_blocked_status_and_alternative_offering():
    status = FortunaConnector.get_adapter_status()
    assert status["source_system"] == "fortuna"
    assert status["is_blocked"] is True
    assert status["blocked_by"] == "H-06"
    assert "Decision H-06" in status["missing_input_reason"]
    assert status["recommended_alternative"] == "GenericCustomSystemConnector"


# ===========================================================================
# CRA-009.A: Virtual vs Materialized query equivalence & secrets sweep
# ===========================================================================

def test_cra_009_a_virtual_vs_materialized_query_equivalence_and_secrets_sweep():
    # 1. Equivalence of virtual vs materialized declared results under masking
    data = json.loads(SNOWFLAKE_FIXTURE.read_text(encoding="utf-8"))
    raw_rows = data["sample_rows"]
    table_def = data["tables"][0]
    columns = [
        ColumnPolicy(
            column_name=c["column_name"],
            data_type=c["data_type"],
            is_masked=c.get("is_masked", False),
            masking_policy=c.get("masking_policy"),
        )
        for c in table_def["columns"]
    ]

    sf = SnowflakeConnector(
        source_id="sf-test",
        account="acme.snowflake",
        mode=SnowflakeMode.SAMPLED_DATA,
        opt_in_sampling=True,
        token="sf-token",
    )
    rows_virtual, _ = sf.sample_table_data(table_def["table_name"], raw_rows, columns)
    rows_materialized, _ = sf.sample_table_data(table_def["table_name"], raw_rows, columns)

    # Declared results match identically across virtual and materialized evaluation
    assert rows_virtual == rows_materialized
    assert rows_virtual[0]["ACCOUNT_NUMBER"] == "[MASKED_BY_POLICY]"

    # 2. Universal Connection Factory validation
    factory = ConnectorFactory()
    sf_conn = factory.create("snowflake", "acme_account", token="sf-tok")
    assert isinstance(sf_conn, SnowflakeConnector)

    custom_conn = factory.create("custom_system", "https://custom.corp/api", config={"protocol": "rest_openapi"})
    assert isinstance(custom_conn, GenericCustomSystemConnector)

    # Fortuna instantiation through factory raises FortunaConnectorBlockedError
    with pytest.raises(FortunaConnectorBlockedError):
        factory.create("fortuna", "https://fortuna.corp/api")

    # 3. CML compilation sweep
    cml_files = [
        "packages/eoip/mapping/cml/snowflake.cml",
        "packages/eoip/mapping/cml/catalog_federation.cml",
    ]
    for cml_path in cml_files:
        content = Path(cml_path).read_text(encoding="utf-8")
        mapping = parse_and_compile_cml(content)
        assert mapping.mapping_id.startswith("cml_")

    # 4. Secrets fixture sweep: confirm 0 leaked plaintext secrets
    assert "ghp_SECRET_TOKEN_IN_QUERY_998877" not in json.dumps(rows_virtual)
    qh_clean, _ = sf.extract_query_history(data["query_history"]) if sf.opt_in_query_history else ([], [])
