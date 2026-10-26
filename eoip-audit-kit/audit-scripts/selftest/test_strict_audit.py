import importlib.util
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


policy = load("strict_audit_policy")
parser = load("parse_md_requirements")
COMMIT = "a" * 40


def item(tier="L2", **kwargs):
    return {"proof_tier": tier, "git_commit": COMMIT, "type": "test_run",
            "actual_result": "1 passed, 0 failed", "repro_command": "pytest exact.py::test_x",
            "links": [{"kind": "artifact", "url": "tests.xml"}], **kwargs}


def status(items, gaps=None, **kwargs):
    args = dict(commit=COMMIT, bundle_commit=COMMIT, severity="High",
                gaps=gaps if gaps is not None else ["AC scope not independently reviewed"],
                producer="auditor")
    args.update(kwargs)
    return policy.assess(items, **args)


def test_unknown_and_fail_only_never_prove_completion():
    for result in ("", "not executed", "1 failed", "0 failed, 1 error"):
        assert status([item(actual_result=result)])["status"] == "Not Verified"


def test_l1_only_and_bare_l2_are_not_partial():
    assert status([item("L1")])["status"] == "Not Verified"
    assert status([item(links=[])])["status"] == "Not Verified"
    assert status([item(repro_command="")])["status"] == "Not Verified"


def test_bundle_mismatch_is_stale_even_when_item_matches():
    result = status([item()], bundle_commit="b" * 40)
    assert result["status"] == "Not Verified"
    assert result["stale_count"] == 1


def test_no_residual_gaps_no_ci_is_not_complete():
    assert status([item()], gaps=[])["status"] == "Not Verified"
    assert status([item()])["status"] == "Partially Implemented"


def test_ci_needs_job_and_run_and_no_gaps():
    assert status([item(), item("L3")], gaps=[])["status"] == "Not Verified"
    ci = item("L3", ci_run_id="123", ci_job="test", type="ci_run")
    assert status([item(), ci], gaps=[])["status"] == "Implemented"
    assert status([item(), ci])["status"] == "Partially Implemented"


def test_runtime_requires_nonproduction():
    for environment in (None, "production"):
        assert status([item(), item("L4", environment=environment)], gaps=[])["status"] == "Not Verified"
    assert status([item(), item("L4", environment="test")], gaps=[])["status"] == "Implemented"


def test_critical_requires_independent_review_and_ci():
    ci = item("L3", ci_run_id="123", ci_job="tests")
    assert status([item(), ci], gaps=[], severity="Critical")["status"] == "Not Verified"
    assert status([item(), ci, item("L5", reviewer_id="auditor")],
                  gaps=[], severity="Critical")["status"] == "Not Verified"
    assert status([item(), ci, item("L5", reviewer_id="reviewer")],
                  gaps=[], severity="Critical")["status"] == "Implemented"


def test_mixed_results_conflict():
    assert status([item(), item(actual_result="1 failed")])["status"] == "Ambiguous"


def test_parser_preserves_full_requirement_and_table_line():
    text = "## REQ-FUNC-0001: Complete body\n" + ("must retain every line\n" * 400)
    record = parser.extract(text, "requirements.md")[0]
    assert record["raw_text"] == text.rstrip("\n")
    row = "| REQ-FUNC-0002 | Title | MUST retain pipes |"
    assert parser.extract(row, "requirements.md")[0]["raw_text"] == row


def test_independently_tracked_clauses_keep_their_full_id():
    records = parser.extract("- **CRA-021.7** `[AGG]` Preserve language labels.\n"
                             "- `PRE-002.2` Tests carry explicit markers.", "requirements.md")
    assert [record["id"] for record in records] == ["CRA-021.7", "PRE-002.2"]
