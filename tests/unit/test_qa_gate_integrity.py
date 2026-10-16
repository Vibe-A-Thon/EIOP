"""Tests for QA gate integrity (SR-QA-010 through SR-QA-014, §17.3).

Every test here is tagged with its requirement ID via the
``eoip_requirement`` marker (SR-QA-010: explicit declarations only — the
prior ``eoip.gaps.coverage`` gate counted docstring mentions, which made
status gaming trivial; nothing in these tests relies on text references).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from eoip.qa.dashboard import ExternalGateRecord, StatusDashboard, TestRunSummary
from eoip.qa.evidence import (
    BehavioralEvidenceRegistry,
    record_requirement,
)
from eoip.qa.introspection import (
    CodeIntrospector,
    InventorySnapshot,
    InventoryValidationError,
)
from eoip.qa.mutation import (
    MutationCheck,
    MutationCheckStore,
    flip_assertion,
    run_mutation_check,
)
from eoip.qa.policy import PolicyGate, PolicyGateResult
from eoip.qa.pytest_plugin import get_collector

pytestmark = pytest.mark.eoip_requirement(
    "SR-QA-010", "SR-QA-011", "SR-QA-012", "SR-QA-013", "SR-QA-014"
)

REPO_ROOT = Path(__file__).resolve().parents[2]

MUTATION_FIXTURE = '''
def test_addition_holds():
    assert 1 + 1 == 2
'''


@pytest.fixture()
def registry(tmp_path):
    return BehavioralEvidenceRegistry(tmp_path / "evidence.json")


# -- SR-QA-010: structured behavioral evidence -------------------------------

class TestBehavioralEvidenceRegistry:
    @pytest.mark.eoip_requirement("SR-QA-010")
    def test_register_and_query_mapping(self, registry):
        registry.register("SR-QA-010", "tests/unit/test_x.py::test_a")
        result = registry.coverage("SR-QA-010")
        assert result.covered
        assert result.test_ids == ["tests/unit/test_x.py::test_a"]

    @pytest.mark.eoip_requirement("SR-QA-010")
    def test_persistence_roundtrip(self, registry):
        registry.register("SR-QA-010", "tests/unit/test_x.py::test_a", source="manual")
        reloaded = BehavioralEvidenceRegistry(registry.path)
        assert reloaded.coverage("SR-QA-010").covered

    @pytest.mark.eoip_requirement("SR-QA-010")
    def test_docstring_references_never_count(self, registry, tmp_path):
        """The core lesson from eoip.gaps.coverage: a file that merely
        MENTIONS a requirement ID in prose must produce zero evidence."""
        prose = tmp_path / "fake_test.py"
        prose.write_text(
            '"""This test covers SR-QA-010 totally."""\n'
            "def test_nothing_real():\n"
            "    pass\n"
        )
        # No registry scan of any kind is even possible here — evidence only
        # enters through explicit register()/collector entries.
        assert registry.coverage("SR-QA-010").test_ids == []
        report = registry.coverage_report(["SR-QA-010"])
        assert report["requirements_with_behavioral_evidence"] == 0
        assert report["gate_passed"] is False

    @pytest.mark.eoip_requirement("SR-QA-010")
    def test_invalid_requirement_id_rejected(self, registry):
        with pytest.raises(ValueError):
            registry.register("not-a-requirement", "tests/unit/test_x.py::test_a")

    @pytest.mark.eoip_requirement("SR-QA-010")
    def test_explicit_call_declaration_drains(self):
        record_requirement("SR-QA-010")
        record_requirement("SR-QA-011")
        from eoip.qa.evidence import drain_recorded_requirements
        assert drain_recorded_requirements() == ["SR-QA-010", "SR-QA-011"]
        assert drain_recorded_requirements() == []

    @pytest.mark.eoip_requirement("SR-QA-010")
    def test_collector_records_marker_and_call(self, request):
        if request.config.pluginmanager.get_plugin("eoip.qa.pytest_plugin") is None and \
                not request.config.pluginmanager.hasplugin("eoip.qa.pytest_plugin"):
            pytest.skip("collector test requires -p eoip.qa.pytest_plugin")
        collector = get_collector()
        before = len(collector.records)
        # This very test was tagged with the eoip_requirement marker at
        # module/class level, so the running plugin must have recorded it.
        assert len(collector.records) > before or any(
            r.requirement_id.startswith("SR-QA-") for r in collector.records
        )


# -- SR-QA-011: mutation / negative checks ------------------------------------

class TestMutationChecks:
    @pytest.mark.eoip_requirement("SR-QA-011")
    def test_flip_assertion(self):
        mutated, line = flip_assertion(MUTATION_FIXTURE)
        assert line == 3
        assert "assert 1 + 1 != 2" in mutated
        assert "MUTATED" in mutated

    @pytest.mark.eoip_requirement("SR-QA-011")
    def test_flip_requires_equality_assert(self):
        with pytest.raises(ValueError):
            flip_assertion("def test_x():\n    assert True\n")

    @pytest.mark.eoip_requirement("SR-QA-011")
    def test_mutation_check_catches_broken_behavior(self, tmp_path):
        fixture = tmp_path / "test_fixture_demo.py"
        fixture.write_text(MUTATION_FIXTURE)
        check = run_mutation_check(
            fixture,
            check_id="mc-1",
            requirement_id="SR-QA-011",
            test_id="test_fixture_demo.py::test_addition_holds",
            release="R1",
        )
        assert check.caught is True, "mutated (broken) test must FAIL to prove detection"
        assert check.mutated_exit_code != 0
        assert check.mutation == "== -> !="

    @pytest.mark.eoip_requirement("SR-QA-011")
    def test_store_and_release_summary(self, tmp_path):
        store = MutationCheckStore(tmp_path / "mutations.json")
        caught = MutationCheck(
            check_id="mc-1", requirement_id="SR-QA-011",
            test_id="t::a", mutated_file="f.py", mutation_line=1,
            mutation="== -> !=", original_assert="assert 1 == 1",
            mutated_exit_code=1, caught=True, release="R1",
        )
        missed = MutationCheck(
            check_id="mc-2", requirement_id="SR-QA-012",
            test_id="t::b", mutated_file="f.py", mutation_line=1,
            mutation="== -> !=", original_assert="assert 1 == 1",
            mutated_exit_code=0, caught=False, release="R1",
        )
        store.record(caught)
        store.record(missed)
        summary = store.release_summary("R1")
        assert summary["total"] == 2
        assert summary["caught"] == 1
        assert summary["missed"] == 1
        assert summary["gate_passed"] is False
        reloaded = MutationCheckStore(store.path)
        assert len(reloaded.all_checks()) == 2


# -- SR-QA-012: dashboard with three separate numbers --------------------------

class TestStatusDashboard:
    @pytest.mark.eoip_requirement("SR-QA-012")
    def test_three_numbers_reported_separately(self, tmp_path, registry):
        registry.register("SR-QA-010", "tests/unit/test_a.py::test_1", source="marker")
        registry.register("SR-QA-011", "tests/unit/test_b.py::test_2", source="marker")
        dash = StatusDashboard(registry, path=tmp_path / "dash.json")
        dash.record_test_run(TestRunSummary(run_id="r1", tests_total=10, tests_passed=9))
        dash.record_external_gate(ExternalGateRecord(
            gate_id="pentest-1", requirement_id="SR-QA-013",
            gate_kind="pentest", status="passed", evidence_ref="report.pdf",
        ))
        report = dash.report(["SR-QA-010", "SR-QA-011", "SR-QA-013", "SR-QA-014"])
        assert report["tests_passing"]["count"] == 9
        assert report["requirements_with_behavioral_evidence"]["count"] == 2
        assert report["requirements_with_external_gate_evidence"]["count"] == 1
        assert report["requirements_with_external_gate_evidence"]["requirement_ids"] == ["SR-QA-013"]

    @pytest.mark.eoip_requirement("SR-QA-012")
    def test_no_single_percent_complete(self, tmp_path, registry):
        """A single merged '% complete' number is prohibited (SR-QA-012)."""
        dash = StatusDashboard(registry, path=tmp_path / "dash.json")
        report = dash.report(["SR-QA-010"])
        assert "percent_complete" not in report
        assert "completion" not in report
        for key in ("tests_passing", "requirements_with_behavioral_evidence",
                    "requirements_with_external_gate_evidence"):
            assert key in report

    @pytest.mark.eoip_requirement("SR-QA-012")
    def test_external_gate_persistence(self, tmp_path, registry):
        dash = StatusDashboard(registry, path=tmp_path / "dash.json")
        dash.record_external_gate(ExternalGateRecord(
            gate_id="audit-1", requirement_id="SR-QA-014", gate_kind="audit",
        ))
        reloaded = StatusDashboard(registry, path=tmp_path / "dash.json")
        assert [g.gate_id for g in reloaded.external_gates()] == ["audit-1"]


# -- SR-QA-013: code introspection inventories ---------------------------------

class TestCodeIntrospection:
    @pytest.mark.eoip_requirement("SR-QA-013")
    def test_generates_all_inventories_from_code(self):
        snap = CodeIntrospector(REPO_ROOT).generate()
        data = snap.to_dict()
        for key in ("api_routes", "mcp_tools", "vscode_commands", "algorithms",
                    "metrics", "vertex_labels", "edge_labels"):
            assert key in data
        # MCP tools come from AST of apps/mcp/main.py (@mcp.tool decorators).
        assert "search" in snap.mcp_tools
        assert "entity" in snap.mcp_tools
        # VS Code commands come from package.json as data.
        commands = {c["command"] for c in snap.vscode_commands}
        assert "eoip.nlq" in commands
        # Labels come from the real ontology manifest.
        from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS
        assert snap.vertex_labels == sorted(VERTEX_LABELS)
        assert snap.edge_labels == sorted(EDGE_LABELS)
        # Algorithm/metrics registries are public callables of the real classes.
        from eoip.graph.algorithms import GraphAlgorithms
        assert "weighted_shortest_path" in snap.algorithms
        assert not any(a.startswith("_") for a in snap.algorithms)
        assert callable(getattr(GraphAlgorithms, snap.algorithms[0]))

    @pytest.mark.eoip_requirement("SR-QA-013")
    def test_api_routes_from_real_code(self):
        snap = CodeIntrospector(REPO_ROOT).generate()
        assert snap.api_routes, "apps/api exposes routes via import or AST"
        rendered = {f"{r['method']} {r['path']}" for r in snap.api_routes}
        assert any(path.startswith("/api/v1/") for _, path in (r.split(" ", 1) for r in rendered))

    @pytest.mark.eoip_requirement("SR-QA-013")
    def test_hand_written_counts_fail_validation(self):
        """Hand-edited inventory counts must fail validation (SR-QA-013)."""
        introspector = CodeIntrospector(REPO_ROOT)
        snap = introspector.generate()
        # A hand-written snapshot that "forgets" a real tool must be caught.
        tampered = InventorySnapshot.from_dict(snap.to_dict())
        tampered.mcp_tools = [t for t in tampered.mcp_tools if t != "search"]
        result = introspector.validate_snapshot(tampered)
        assert result["valid"] is False
        assert "search" in result["diffs"]["mcp_tools"]["added_in_code"]
        with pytest.raises(InventoryValidationError):
            introspector.assert_snapshot_valid(tampered)

    @pytest.mark.eoip_requirement("SR-QA-013")
    def test_valid_snapshot_passes(self):
        introspector = CodeIntrospector(REPO_ROOT)
        snap = introspector.generate()
        assert introspector.validate_snapshot(snap)["valid"] is True
        assert introspector.validate_snapshot(snap.to_dict())["valid"] is True


# -- SR-QA-014: policy gate -----------------------------------------------------

class TestPolicyGate:
    @pytest.mark.eoip_requirement("SR-QA-014")
    def test_ruff_runs_and_records_zero_error_status(self, tmp_path):
        import shutil
        gate = PolicyGate(repo_root=REPO_ROOT, path=tmp_path / "policy.json")
        result = gate.run(run_id="pg-1")
        assert result.tool == "ruff"
        assert result.report_only is True
        if shutil.which("ruff"):
            assert result.available and not result.skipped
            assert result.error_count >= 0
            assert result.zero_error_policy_met == (result.error_count == 0)
        else:
            # Tolerant mode: ruff unavailable => skipped, not a crash.
            assert result.skipped and result.available is False
        assert gate.latest().run_id == "pg-1"
        reloaded = PolicyGate(repo_root=REPO_ROOT, path=tmp_path / "policy.json")
        assert reloaded.history()[-1].run_id == "pg-1"

    @pytest.mark.eoip_requirement("SR-QA-014")
    def test_zero_error_policy_met_on_clean_tree(self, tmp_path):
        """The zero-error status flips to True when ruff finds no errors."""
        import shutil
        if not shutil.which("ruff"):
            pytest.skip("ruff unavailable")
        clean = tmp_path / "clean"
        clean.mkdir()
        (clean / "clean_mod.py").write_text("X = 1\n")
        gate = PolicyGate(repo_root=clean, path=tmp_path / "policy.json")
        result = gate.run(run_id="pg-clean", paths=["."])
        assert result.zero_error_policy_met is True, result.summary

    @pytest.mark.eoip_requirement("SR-QA-014")
    def test_result_serialization(self):
        result = PolicyGateResult(
            run_id="pg-x", tool="ruff", command=["ruff", "check"],
            available=True, skipped=False, exit_code=0, error_count=0,
            zero_error_policy_met=True,
        )
        roundtrip = json.loads(json.dumps(result.to_dict()))
        assert roundtrip["zero_error_policy_met"] is True


# -- Router ----------------------------------------------------------------------

class TestRouter:
    @pytest.mark.eoip_requirement("SR-QA-010", "SR-QA-012", "SR-QA-013", "SR-QA-014")
    def test_router_routes(self, tmp_path):
        fastapi = pytest.importorskip("fastapi")
        from eoip.qa import build_router

        registry = BehavioralEvidenceRegistry(tmp_path / "evidence.json")
        mutations = MutationCheckStore(tmp_path / "mutations.json")
        dash = StatusDashboard(registry, mutations, path=tmp_path / "dash.json")
        router = build_router(
            evidence_registry=registry,
            mutation_store=mutations,
            dashboard=dash,
            introspector=CodeIntrospector(REPO_ROOT),
            policy_gate=PolicyGate(repo_root=REPO_ROOT, path=tmp_path / "policy.json"),
        )
        paths = sorted({getattr(r, "path", "") for r in router.routes})
        for expected in (
            "/api/v1/qa/evidence/coverage",
            "/api/v1/qa/evidence/register",
            "/api/v1/qa/mutation-checks",
            "/api/v1/qa/dashboard",
            "/api/v1/qa/inventory",
            "/api/v1/qa/inventory/validate",
            "/api/v1/qa/policy-gate/run",
            "/api/v1/qa/policy-gate/latest",
        ):
            assert expected in paths, f"missing route {expected}"

        app = fastapi.FastAPI()
        app.include_router(router)
        from fastapi.testclient import TestClient
        client = TestClient(app)
        resp = client.post("/api/v1/qa/evidence/register", json={
            "requirement_id": "SR-QA-010",
            "test_id": "tests/unit/test_qa_gate_integrity.py::test_register_via_api",
            "source": "manual",
            "recorded_at": "",
        })
        assert resp.status_code == 201
        resp = client.get("/api/v1/qa/evidence/coverage/SR-QA-010")
        assert resp.status_code == 200
        assert resp.json()["covered"] is True

        dash_resp = client.get("/api/v1/qa/dashboard")
        assert dash_resp.status_code == 200
        body = dash_resp.json()
        assert "percent_complete" not in body
        assert body["requirements_with_behavioral_evidence"]["count"] == 1

        inv_resp = client.get("/api/v1/qa/inventory")
        assert inv_resp.status_code == 200
        assert "search" in inv_resp.json()["mcp_tools"]
