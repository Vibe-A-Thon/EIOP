"""Unit tests for REVA configuration (T-003 / OBL-REVA-CFG-01)."""

import pytest
from reva.config import RevaSettings, get_settings
from tests.reva.support.settings import override_settings

pytestmark = pytest.mark.reva_depth("unit")


@pytest.mark.reva_obligation("OBL-REVA-CFG-01")
@pytest.mark.reva_case("positive")
def test_config_defaults():
    s = get_settings()
    assert s.enabled is False
    assert s.store_url.startswith("sqlite")
    assert s.mutation_min == 0.70
    assert s.gap_weights["high"] == 4
    assert len(s.service_account_patterns) >= 2


@pytest.mark.reva_obligation("OBL-REVA-CFG-01")
@pytest.mark.reva_case("positive")
def test_config_override():
    with override_settings(enabled=True, max_runs=5):
        s = get_settings()
        assert s.enabled is True
        assert s.max_runs == 5


@pytest.mark.reva_obligation("OBL-REVA-CFG-01")
@pytest.mark.reva_case("negative")
def test_invalid_kek():
    with pytest.raises(ValueError, match="must decode to exactly 32 bytes"):
        RevaSettings(kek="c2hvcnQ=")  # "short" is only 5 bytes


@pytest.mark.reva_obligation("OBL-REVA-CFG-01")
@pytest.mark.reva_case("boundary")
def test_json_parsed_fields():
    s = RevaSettings(service_url_map='{"billing": "http://billing:8080"}')
    assert s.service_url_map == {"billing": "http://billing:8080"}
