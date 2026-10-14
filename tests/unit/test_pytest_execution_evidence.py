"""Run isolated pytest processes to verify real outcome and source binding."""

import json
import os
import subprocess
import sys

import pytest
from eoip.verification.test_receipts import seal_receipt, validate_receipt

pytestmark = pytest.mark.req("BASE-02", "BASE-03")


def _run(tmp_path, source, *args):
    tests = tmp_path / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "test_case.py").write_text(source, encoding="utf-8")
    (tmp_path / "pytest.ini").write_text("[pytest]\nmarkers =\n    req(id): requirement\n", encoding="utf-8")
    receipt = tmp_path / "receipt.json"
    mapping = tmp_path / "map.json"
    env = {**os.environ, "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}
    command = [sys.executable, "-m", "pytest", "-p", "eoip.verification.pytest_evidence",
               "--run-evidence", str(receipt), "--requirements-map", str(mapping), "-q", *args]
    result = subprocess.run(command, cwd=tmp_path, env=env, capture_output=True, text=True, timeout=40, check=False)
    assert receipt.exists(), result.stdout + result.stderr
    return result, json.loads(receipt.read_text()), mapping


def test_pass_receipt_is_bound_to_source_and_replaces_stale_map(tmp_path):
    (tmp_path / "map.json").write_text('{"STALE": ["deleted.py::old"]}')
    result, receipt, mapping = _run(tmp_path, 'import pytest\n@pytest.mark.req("REQ-ONE")\ndef test_ok():\n    assert 2 + 2 == 4\n')
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(mapping.read_text()) == {"REQ-ONE": ["tests/test_case.py::test_ok"]}
    validate_receipt(tmp_path, receipt)
    (tmp_path / "tests/test_case.py").write_text("def test_ok():\n    assert False\n")
    with pytest.raises(ValueError, match="source has changed"):
        validate_receipt(tmp_path, receipt)


@pytest.mark.parametrize("source,outcome", [
    ('def test_bad():\n    assert False\n', "FAILED"),
    ('import pytest\n@pytest.mark.skip(reason="no infrastructure")\ndef test_skip():\n    pass\n', "SKIPPED"),
    ('import pytest\n@pytest.mark.xfail\ndef test_xfail():\n    assert False\n', "XFAIL"),
    ('import pytest\n@pytest.fixture\ndef broken():\n    yield\n    assert False\ndef test_teardown(broken):\n    pass\n', "FAILED"),
])
def test_fail_skip_xfail_and_teardown_failures_never_count_as_pass(tmp_path, source, outcome):
    _, receipt, _ = _run(tmp_path, source)
    assert receipt["tests"][0]["outcome"] == outcome
    with pytest.raises(ValueError):
        validate_receipt(tmp_path, receipt)


def test_collect_only_is_not_execution_and_selection_is_explicit(tmp_path):
    _, receipt, _ = _run(tmp_path, "def test_a():\n    pass\ndef test_b():\n    pass\n", "--collect-only", "-k", "test_b")
    assert receipt["selected_node_ids"] == ["tests/test_case.py::test_b"]
    assert receipt["tests"][0]["outcome"] == "NOT_EXECUTED"
    with pytest.raises(ValueError, match="did not execute"):
        validate_receipt(tmp_path, receipt)


def test_receipt_tampering_and_missing_cases_are_rejected(tmp_path):
    _, receipt, _ = _run(tmp_path, "def test_ok():\n    pass\n")
    receipt["counts"]["passed"] = 99
    with pytest.raises(ValueError, match="digest mismatch"):
        validate_receipt(tmp_path, receipt)
    with pytest.raises(ValueError, match="counts"):
        validate_receipt(tmp_path, seal_receipt(receipt))
    receipt["tests"] = []
    with pytest.raises(ValueError, match="incomplete"):
        validate_receipt(tmp_path, seal_receipt(receipt))


def test_deleted_test_is_removed_by_next_collection(tmp_path):
    _run(tmp_path, 'import pytest\n@pytest.mark.req("OLD")\ndef test_old():\n    pass\n')
    _, _, mapping = _run(tmp_path, "def test_new():\n    pass\n")
    assert json.loads(mapping.read_text()) == {}


def test_collection_error_preserves_inventory_but_records_failed_run(tmp_path):
    mapping = tmp_path / "map.json"
    mapping.write_text('{"KEEP": ["tests/test_old.py::test_ok"]}')
    result, receipt, mapping = _run(tmp_path, "this is not valid python (\n")
    assert result.returncode != 0
    assert receipt["collection_errors"]
    assert "KEEP" in json.loads(mapping.read_text())
    with pytest.raises(ValueError, match="did not execute"):
        validate_receipt(tmp_path, receipt)
