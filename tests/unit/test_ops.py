"""Tests for eoip.ops: preflight, upgrade planner, support bundle (§47)."""

from _principals import provision_api_token
import pytest

pytestmark = pytest.mark.req("§47")


@pytest.fixture
def ontology_file(tmp_path):
    path = tmp_path / "ontology.yaml"
    path.write_text("classes:\n  Person:\n    label: person\n", encoding="utf-8")
    return path


class _HealthyStore:
    def health(self):
        return True

    def ping(self):
        return {"status": "up"}


class _DeadStore:
    def health(self):
        raise ConnectionError("refused")


class _FakeSink:
    def __init__(self, events):
        self._events = events

    def read(self, *, limit=100):
        return self._events[:limit]


# -- preflight ---------------------------------------------------------------


def test_preflight_all_pass(tmp_path, monkeypatch, ontology_file):
    from eoip.ops import run_preflight

    monkeypatch.setenv("EOIP_GRAPH_URL", "http://graph:8080")
    monkeypatch.setenv("EOIP_API_TOKEN", "secret-token")
    provision_api_token(monkeypatch, "secret-token")
    report = run_preflight(
        required_env=["EOIP_GRAPH_URL"],
        ontology_paths=[ontology_file],
        graph_store=_HealthyStore(),
        disk_path=tmp_path,
    )
    assert report.ok
    assert {c.name for c in report.checks} == {"env", "token", "ontology", "graph_store", "disk_space"}


def test_preflight_missing_env_fails(monkeypatch, ontology_file, tmp_path):
    from eoip.ops import run_preflight

    monkeypatch.delenv("EOIP_MISSING_VAR", raising=False)
    report = run_preflight(
        required_env=["EOIP_MISSING_VAR"],
        ontology_paths=[ontology_file],
        disk_path=tmp_path,
    )
    assert not report.ok
    assert report.failures[0].name == "env"


def test_preflight_unparseable_ontology_fails(tmp_path, monkeypatch):
    from eoip.ops import run_preflight

    bad = tmp_path / "bad.yaml"
    bad.write_text("a: [1, 2\n  b: }", encoding="utf-8")
    monkeypatch.setenv("EOIP_GRAPH_URL", "x")
    report = run_preflight(required_env=[], ontology_paths=[bad], disk_path=tmp_path)
    assert not report.ok
    assert any(c.name == "ontology" and c.status == "fail" for c in report.checks)


def test_preflight_dead_graph_store_fails(tmp_path, monkeypatch, ontology_file):
    from eoip.ops import run_preflight

    monkeypatch.setenv("EOIP_GRAPH_URL", "x")
    report = run_preflight(
        required_env=[], ontology_paths=[ontology_file], graph_store=_DeadStore(), disk_path=tmp_path
    )
    assert not report.ok
    assert any(c.name == "graph_store" and c.status == "fail" for c in report.checks)


def test_preflight_missing_token_warns_not_fails(tmp_path, monkeypatch, ontology_file):
    from eoip.ops import run_preflight

    monkeypatch.setenv("EOIP_GRAPH_URL", "x")
    monkeypatch.delenv("EOIP_API_TOKEN", raising=False)
    report = run_preflight(required_env=[], ontology_paths=[ontology_file], disk_path=tmp_path)
    assert report.ok  # warn must not fail the report
    assert any(c.name == "token" and c.status == "warn" for c in report.checks)


def test_preflight_low_disk_warns(tmp_path, monkeypatch, ontology_file):
    from eoip.ops import run_preflight

    monkeypatch.setenv("EOIP_GRAPH_URL", "x")
    report = run_preflight(
        required_env=[], ontology_paths=[ontology_file], disk_path=tmp_path,
        min_free_bytes=10**15,
    )
    assert any(c.name == "disk_space" and c.status == "warn" for c in report.checks)


def test_preflight_port_unavailable_fails(tmp_path, monkeypatch, ontology_file):
    import socket

    from eoip.ops import run_preflight

    monkeypatch.setenv("EOIP_GRAPH_URL", "x")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        port = sock.getsockname()[1]
        report = run_preflight(
            required_env=[], ontology_paths=[ontology_file], disk_path=tmp_path,
            port=port, host="127.0.0.1",
        )
    assert any(c.name == "port" and c.status == "fail" for c in report.checks)


def test_preflight_report_to_dict(tmp_path, monkeypatch):
    from eoip.ops import run_preflight

    monkeypatch.setenv("EOIP_GRAPH_URL", "x")
    report = run_preflight(required_env=[], disk_path=tmp_path)
    data = report.to_dict()
    assert data["id"].startswith("urn:eoip:ops:preflight-report:")
    assert isinstance(data["ok"], bool)
    assert len(data["checks"]) == len(report.checks)


# -- upgrade planner ---------------------------------------------------------


def _manifest(vertex_labels):
    return {
        "vertex_labels": vertex_labels,
        "edge_labels": {},
        "property_keys": {},
    }


def test_upgrade_plan_basic():
    from eoip.ops import plan_upgrade

    plan = plan_upgrade("0.1.0", "0.2.0")
    assert plan["prechecks_ok"]
    assert plan["current_version"] == "0.1.0"
    assert plan["target_version"] == "0.2.0"
    assert plan["id"] == "urn:eoip:ops:upgrade-plan:0.1.0-to-0.2.0"
    assert "rollback_note" in plan


def test_upgrade_plan_rejects_downgrade():
    from eoip.ops import plan_upgrade

    plan = plan_upgrade("0.2.0", "0.1.0")
    assert not plan["prechecks_ok"]
    assert any(p["name"] == "version_order" and p["status"] == "fail" for p in plan["prechecks"])


def test_upgrade_plan_rejects_unparseable_version():
    from eoip.ops import plan_upgrade

    assert not plan_upgrade("x", "0.2.0")["prechecks_ok"]
    assert not plan_upgrade("0.1.0", "latest")["prechecks_ok"]


def test_upgrade_plan_classifies_breaking_changes():
    from eoip.ops import plan_upgrade

    old = _manifest({"person": {"required": ["name"], "domain": "identity"}})
    new = _manifest({
        "person": {"required": ["name"], "domain": "identity"},
        "org": {"required": ["title"], "domain": "identity"},
    })
    plan = plan_upgrade("0.1.0", "0.2.0", current_manifest=old, target_manifest=new)
    assert plan["prechecks_ok"]
    assert plan["ontology_diff"]["total_changes"] >= 1
    assert any(s["severity"] == "safe" for s in plan["migration_steps"])
    assert all(s["id"].startswith("urn:eoip:ops:migration-step:") for s in plan["migration_steps"])


def test_upgrade_plan_with_graph_store_precheck():
    from eoip.ops import plan_upgrade

    plan = plan_upgrade("0.1.0", "0.2.0", graph_store=_HealthyStore())
    assert any(p["name"] == "graph_store" and p["status"] == "pass" for p in plan["prechecks"])
    plan = plan_upgrade("0.1.0", "0.2.0", graph_store=_DeadStore())
    assert not plan["prechecks_ok"]


# -- support bundle ----------------------------------------------------------


def test_support_bundle_structure(monkeypatch, tmp_path):
    from eoip.ops import collect_support_bundle

    monkeypatch.setenv("EOIP_GRAPH_URL", "http://graph:8080")
    monkeypatch.setenv("EOIP_API_TOKEN", "super-secret-token")
    provision_api_token(monkeypatch, "super-secret-token")
    bundle = collect_support_bundle(
        audit_sink=_FakeSink([{"event": "login", "actor": "alice"}]),
        graph_store=_HealthyStore(),
        env_vars=["EOIP_GRAPH_URL", "EOIP_API_TOKEN", "EOIP_UNDEFINED"],
    )
    assert bundle["schema"] == "urn:eoip:ops:support-bundle:v1"
    assert bundle["config"]["EOIP_GRAPH_URL"] == "http://graph:8080"
    assert bundle["config"]["EOIP_API_TOKEN"] == "***REDACTED***"
    assert bundle["config"]["EOIP_UNDEFINED"] is None
    assert bundle["audit_events"] == [{"event": "login", "actor": "alice"}]
    assert bundle["graph_stats"]["available"] is True
    assert "python" in bundle["versions"]


def test_support_bundle_redacts_extra(monkeypatch):
    from eoip.ops import collect_support_bundle

    bundle = collect_support_bundle(env_vars=(), extra={"api_key": "abc123"})
    assert bundle["extra"]["api_key"] == "***REDACTED***"


def test_support_bundle_without_sources(monkeypatch):
    from eoip.ops import collect_support_bundle

    bundle = collect_support_bundle(env_vars=())
    assert bundle["audit_events"] == []
    assert bundle["graph_stats"]["available"] is False
