import json
from pathlib import Path
from uuid import uuid4

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from pydantic import ValidationError

from eoip.contracts.warrant import Warrant
from eoip.provenance.warrant_order import (
    DEFAULT_WARRANT_STATUS_ORDER,
    minimum_warrant_status,
    validate_warrant_status_order,
    warrant_status_rank,
)


def _warrant_payload():
    return {
        "warrant_id": str(uuid4()),
        "tenant_id": "tenant-a",
        "schema_version": "1.0",
        "subject": {"kind": "assertion", "ref": "assertion-1", "text": "service uses db"},
        "grounds": [{"kind": "source_record", "id": "source-1", "version": "rev-1"}],
        "status": "OBSERVED",
        "confidence": 1.0,
        "validity": {"valid_from": "2026-10-18T00:00:00Z", "valid_to": None, "lease_ids": []},
        "authority": {"principal_id": "principal-a", "scopes": [], "delegation_chain": []},
        "consequence": {"kappa": 0, "impact_run_id": None, "action_class": "READ_ONLY"},
        "operator": {"operator_id": "connector-a", "class": "OBSERVER", "version": "1"},
        "parents": [],
        "created_at": "2026-10-18T00:00:00Z",
        "signature": None,
    }


def test_typed_warrant_serializes_against_canonical_schema():
    schema_path = Path("schemas/warrant.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    warrant = Warrant.model_validate(_warrant_payload())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(warrant.to_schema_dict())


@pytest.mark.parametrize("field", ["tenant_id", "subject", "grounds", "status", "validity", "authority", "consequence", "operator", "parents", "created_at", "schema_version"])
def test_typed_warrant_requires_canonical_fields(field):
    payload = _warrant_payload()
    del payload[field]
    with pytest.raises(ValidationError):
        Warrant.model_validate(payload)


def test_warrant_preserves_status_and_operator_class_values():
    warrant = Warrant.model_validate(_warrant_payload())

    assert warrant.status.value == "OBSERVED"
    assert warrant.operator.class_.value == "OBSERVER"
    assert warrant.model_dump(mode="json", by_alias=True)["operator"]["class"] == "OBSERVER"


def test_warrant_rejects_naive_timestamps():
    payload = _warrant_payload()
    payload["created_at"] = "2026-10-18T00:00:00"
    with pytest.raises(ValidationError, match="timezone"):
        Warrant.model_validate(payload)


def test_warrant_status_order_accepts_default_and_only_allowed_swap():
    default = [status.value for status in DEFAULT_WARRANT_STATUS_ORDER]
    swapped = ["ATTESTED", "OBSERVED", *default[2:]]

    assert validate_warrant_status_order(default) == DEFAULT_WARRANT_STATUS_ORDER
    assert validate_warrant_status_order(swapped)[0].value == "ATTESTED"
    assert warrant_status_rank("OBSERVED", order=swapped) == 1
    assert minimum_warrant_status(["OBSERVED", "PREDICTED"], order=swapped).value == "PREDICTED"
    assert minimum_warrant_status([]).value == "UNKNOWN"


@pytest.mark.parametrize("invalid_order", [
    ["OBSERVED", "PREDICTED", "ATTESTED", "GENERATED", "HEARSAY", "UNKNOWN"],
    ["OBSERVED", "OBSERVED", "PREDICTED", "GENERATED", "HEARSAY", "UNKNOWN"],
    ["OBSERVED", "ATTESTED", "PREDICTED", "GENERATED", "HEARSAY"],
])
def test_warrant_status_order_rejects_every_other_order(invalid_order):
    with pytest.raises(ValueError, match="WAR_INVALID_ORDER"):
        validate_warrant_status_order(invalid_order)