"""Unit tests for time, error catalog and redaction (T-103 / OBL-REVA-CORE-ERR-01)."""

import pytest
from datetime import datetime, timezone
from reva.core.time import format_ts, parse_ts, utc_now_ms
from reva.core.errors import RevaError, ValidationError, NotFoundError
from reva.core.redact import redact_headers, redact_url, redact_data

pytestmark = pytest.mark.reva_depth("unit")


@pytest.mark.reva_obligation("OBL-REVA-CORE-ERR-01")
@pytest.mark.reva_case("positive")
def test_time_round_trip():
    now = utc_now_ms()
    s = format_ts(now)
    assert s.endswith("Z")
    parsed = parse_ts(s)
    assert parsed == now


@pytest.mark.reva_obligation("OBL-REVA-CORE-ERR-01")
@pytest.mark.reva_case("negative")
def test_time_invalid_format():
    with pytest.raises(ValueError, match="Invalid timestamp"):
        parse_ts("2026-10-18 10:00:00")  # missing T and Z


@pytest.mark.reva_obligation("OBL-REVA-CORE-ERR-01")
@pytest.mark.reva_case("positive")
def test_error_payload_shape():
    err = ValidationError("Bad input field", details={"issues": [{"pointer": "/foo", "reason": "required"}]})
    payload = err.to_dict(correlation_id="corr-123")
    assert payload["error"]["code"] == "REVA_E_VALIDATION"
    assert payload["error"]["category"] == "invalid_input"
    assert payload["error"]["correlation_id"] == "corr-123"
    assert len(payload["error"]["details"]["issues"]) == 1


@pytest.mark.reva_obligation("OBL-REVA-CORE-ERR-01")
@pytest.mark.reva_case("positive")
def test_redaction():
    headers = {"Authorization": "Bearer secret123", "Content-Type": "application/json"}
    redacted = redact_headers(headers)
    assert redacted["Authorization"] == "[REDACTED]"
    assert redacted["Content-Type"] == "application/json"

    url = "https://user:password@example.com/api?token=secret456&page=1"
    r_url = redact_url(url)
    assert "password" not in r_url
    assert "secret456" not in r_url
    assert "page=1" in r_url

    data = {"user": "alice", "password": "mypassword", "nested": {"api_key": "xyz"}}
    r_data = redact_data(data)
    assert r_data["password"] == "[REDACTED]"
    assert r_data["nested"]["api_key"] == "[REDACTED]"
    assert r_data["user"] == "alice"
