"""Unit tests for Phase P2 Proof-of-Done and Verifier Sandbox modules."""

import sys
import ast
import tempfile
from pathlib import Path
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

pytestmark = pytest.mark.reva_depth("unit")

from reva.core.errors import RevaValidationError
from reva.kernel.authority import Depth
from reva.kernel.keys import generate_keypair
from reva.kernel.store import RevaStore
from reva.pd.antigaming import (
    check_ag05_meaningful_assertion,
    check_ag06_no_self_mock,
    check_ag13_positive_test_count,
    check_ag14_fixtures_integrity,
)
from reva.pd.bindings import (
    Binding,
    FixtureRef,
    OwnerRef,
    VerifierSpec,
    load_bindings,
    sync_bindings,
    validate_bindings,
)
from reva.pd.closure import ClosureContext, evaluate_closure
from reva.pd.export_html import render_ledger_html
from reva.pd.gates import GateDefinition, GateStage, evaluate_gate
from reva.pd.ledger import build_ledger
from reva.pd.obligations import (
    Obligation,
    load_obligations,
    sync_obligations,
    validate_obligations_dag,
)
from reva.pd.owner_digest import compute_owner_digest, normalize_source_bytes
from reva.pd.runs import RunRecord
from reva.pd.waivers import create_waiver, get_active_waivers
from reva.sandbox.attest import (
    create_dsse_attestation,
    create_in_toto_statement,
    verify_dsse_attestation,
)
from reva.sandbox.collectors import (
    OwnerSpan,
    ParsedTest,
    parse_coverage_contexts,
    parse_junit_xml,
    parse_playwright_json,
)
from reva.sandbox.limits import SandboxLimits
from reva.sandbox.runner import ProcessSandbox, RunSpec


@pytest.fixture
def temp_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        store = RevaStore(str(db_path))
        try:
            yield store
        finally:
            store.conn.close()


def test_obligations_dag_and_sync(temp_store):
    yaml_text = """
    obligations:
      - key: OBL-A
        version: 1
        requirement_id: REQ-A
        title: Task A
        case_kinds: ["positive"]
        dependencies: []
      - key: OBL-B
        version: 1
        requirement_id: REQ-B
        title: Task B
        case_kinds: ["positive", "negative"]
        dependencies: ["OBL-A"]
    """
    obs = load_obligations(yaml_text)
    assert len(obs) == 2
    validate_obligations_dag(obs)

    count = sync_obligations(temp_store, "tenant_test", obs)
    assert count == 2

    # Cycle test
    cyclic_obs = [
        Obligation(key="OBL-1", requirement_id="R1", title="1", dependencies=["OBL-2"]),
        Obligation(key="OBL-2", requirement_id="R2", title="2", dependencies=["OBL-1"]),
    ]
    with pytest.raises(RevaValidationError, match="Cyclic obligation dependency"):
        validate_obligations_dag(cyclic_obs)


def test_bindings_validation_and_sync(temp_store):
    binding = Binding(
        obligation_key="OBL-A",
        obligation_version=1,
        owners=[OwnerRef(repo_id="repo1", path="src/foo.py", symbol="foo")],
        verifier=VerifierSpec(verifier_id="v1", argv=["pytest"]),
    )
    validate_bindings([binding])
    count = sync_bindings(temp_store, "tenant_test", [binding])
    assert count == 1


def test_owner_digest_python_and_file():
    code = """
def sample_func(x):
    # comment
    return x + 1
"""
    res = compute_owner_digest(code, symbol="sample_func", language="python")
    assert res.status == "found"
    assert res.digest is not None
    assert len(res.digest) == 64

    # File mode
    res_file = compute_owner_digest(code, symbol="*file*")
    assert res_file.status == "found"
    assert res_file.start_line == 1


def test_sandbox_runner_process():
    spec = RunSpec(
        # FT-D13: absolute interpreter path; CI images often ship only python3.
        argv=[sys.executable, "-c", "import sys; sys.stdout.write('hello stdout'); sys.stderr.write('hello stderr')"],
        timeout_s=10,
    )
    outcome = ProcessSandbox.run(spec)
    assert outcome.exit_code == 0
    assert b"hello stdout" in outcome.stdout
    assert b"hello stderr" in outcome.stderr
    assert outcome.duration_ms >= 0


def test_collectors_junit_and_coverage():
    junit_xml = """<?xml version="1.0" encoding="utf-8"?>
    <testsuites>
      <testsuite name="pytest" tests="2">
        <testcase classname="test_mod" name="test_one" time="0.05">
          <properties>
            <property name="reva_nodeid" value="tests/test_mod.py::test_one" />
            <property name="reva_obligation" value="OBL-A" />
            <property name="reva_case" value="positive" />
          </properties>
        </testcase>
        <testcase classname="test_mod" name="test_two" time="0.08">
          <failure message="assertion error">Traceback...</failure>
        </testcase>
      </testsuite>
    </testsuites>
    """
    tests = parse_junit_xml(junit_xml)
    assert len(tests) == 2
    assert tests[0].outcome == "passed"
    assert tests[0].obligation_keys == ["OBL-A"]
    assert tests[1].outcome == "failed"

    # Coverage mapping
    cov_data = {
        "files": {
            "src/mod.py": {
                "contexts": {
                    "tests/test_mod.py::test_one|run": [10, 11, 12],
                }
            }
        }
    }
    owner_span = OwnerSpan(owner_digest="dig1", path="src/mod.py", start_line=5, end_line=15)
    line_hits = parse_coverage_contexts(cov_data, [owner_span])
    assert line_hits["tests/test_mod.py::test_one"]["dig1"] == 3


def test_attestation_signing_and_verification():
    priv, pub, kid = generate_keypair()
    statement = create_in_toto_statement(
        repo_id="kgf",
        commit="abc1234",
        owner_files=[{"path": "reva/core/ids.py", "sha256": "0" * 64}],
        run_record={"run_id": "vr1_123"},
        binding_digest="bnd1_456",
        obligation_keys=["OBL-TEST"],
    )
    envelope = create_dsse_attestation(statement, priv, kid)
    assert envelope["attestation_id"].startswith("att1_")

    verified_stmt = verify_dsse_attestation(envelope, pub)
    assert verified_stmt["predicateType"] == "https://reva.kgf/verification/v1"
    assert verified_stmt["predicate"]["binding_digest"] == "bnd1_456"


def test_antigaming_rules():
    # AG-05
    good_code = "def test_ok(): assert 1 + 1 == 2"
    bad_code = "def test_trivial(): assert True"
    assert check_ag05_meaningful_assertion(ast.parse(good_code)) is True
    assert check_ag05_meaningful_assertion(ast.parse(bad_code)) is False

    # AG-06
    assert check_ag06_no_self_mock(["reva.core.jcs.canonicalize"], ["reva.core.jcs.canonicalize"]) is False
    assert check_ag06_no_self_mock(["other_collaborator"], ["reva.core.jcs.canonicalize"]) is True

    # AG-13
    assert check_ag13_positive_test_count(5) is True
    assert check_ag13_positive_test_count(0) is False


def test_closure_evaluation_and_precedence():
    ob = Obligation(
        key="OBL-CLOSE-TEST",
        version=1,
        requirement_id="REQ-TEST",
        title="Test Close",
        case_kinds=["positive"],
        reviewed_warrant_id="wr1_review",
    )
    b = Binding(
        obligation_key="OBL-CLOSE-TEST",
        obligation_version=1,
        owners=[OwnerRef(repo_id="kgf", path="src/test.py", symbol="test_sym", owner_digest="dig1")],
        verifier=VerifierSpec(verifier_id="v1", argv=["pytest"]),
    )
    test_item = ParsedTest(
        test_id="test_suite::test_a",
        outcome="passed",
        duration_ms=10,
        obligation_keys=["OBL-CLOSE-TEST"],
        case_kinds=["positive"],
        owner_lines_hit={"dig1": 2},
    )
    run_rec = RunRecord(
        run_id="vr1_test",
        verifier_id="v1",
        binding_digest=b.digest(),
        repo_id="kgf",
        commit="commit1",
        tree_digest="0" * 64,
        clean=True,
        environment={},
        profile="unit",
        depth=Depth.UNIT,
        network="none",
        argv=["pytest"],
        started_at="2026-10-18T00:00:00.000Z",
        finished_at="2026-10-18T00:00:01.000Z",
        exit_code=0,
        timed_out=False,
        lineage={},
        artifacts=[],
        tests=[test_item],
        reruns=1,
    )

    ctx = ClosureContext(
        obligation=ob,
        binding=b,
        commit="commit1",
        current_owner_digests={"src/test.py::test_sym": "dig1"},
        runs=[run_rec],
    )
    dec = evaluate_closure(ctx)
    assert dec.outcome == "closed"
    assert dec.closure_id.startswith("cls1_")
    assert not dec.reasons


def test_ledger_construction_and_export():
    ob = Obligation(
        key="OBL-1",
        version=1,
        requirement_id="REQ-1",
        title="1",
        reviewed_warrant_id="wr1_ok",
    )
    b = Binding(
        obligation_key="OBL-1",
        obligation_version=1,
        owners=[OwnerRef(repo_id="kgf", path="src/1.py", symbol="sym", owner_digest="d1")],
        verifier=VerifierSpec(verifier_id="v1", argv=["pytest"]),
    )
    run = RunRecord(
        run_id="vr1_1",
        verifier_id="v1",
        binding_digest=b.digest(),
        repo_id="kgf",
        commit="sha1",
        tree_digest="0" * 64,
        clean=True,
        environment={},
        profile="unit",
        depth=Depth.UNIT,
        network="none",
        argv=["pytest"],
        started_at="2026-10-18T00:00:00.000Z",
        finished_at="2026-10-18T00:00:01.000Z",
        exit_code=0,
        timed_out=False,
        lineage={},
        artifacts=[],
        tests=[ParsedTest("t1", "passed", 1, ["OBL-1"], ["positive"], {"d1": 1})],
        reruns=1,
    )
    ctx = ClosureContext(
        obligation=ob,
        binding=b,
        commit="sha1",
        current_owner_digests={"src/1.py::sym": "d1"},
        runs=[run],
    )
    dec = evaluate_closure(ctx)
    ledger = build_ledger("tenant_t", "all", "sha1", [dec])
    assert ledger.ledger_id.startswith("ldg1_")
    assert ledger.complete is True

    # HTML export
    html = render_ledger_html(ledger)
    assert "REVA Proof-of-Done Ledger" in html
    assert ledger.ledger_id in html


def test_waivers_and_gates(temp_store):
    waiver = create_waiver(
        temp_store,
        "tenant_test",
        target="OBL-WAIVE",
        kind="defer",
        rationale="Approved deferral",
        expires_at="2099-01-01T00:00:00.000Z",
        warrant_id_ref="wr1_mock",
    )
    active = get_active_waivers(temp_store, "tenant_test")
    assert len(active) == 1
    assert active[0].target == "OBL-WAIVE"

    # Gate test
    gate = GateDefinition(
        gate_id="G1",
        stages=[GateStage(stage_id="s1", obligations=["OBL-*"])],
    )
    # With a complete ledger
    ledger = build_ledger("tenant_test", "all", "sha1", [])
    outcome = evaluate_gate(gate, ledger)
    # Obligation missing from empty ledger
    assert outcome.passed is False
