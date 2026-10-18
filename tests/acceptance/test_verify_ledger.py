"""Unit and negative tests for verify_ledger.py.
Proves that every acceptance violation is rejected with its exact reason code.
"""
from __future__ import annotations
import json, tempfile
from pathlib import Path
import pytest
from tools.acceptance.verify_ledger import verify_ledger, sha256_file

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)

def make_valid_receipt(ev_file: Path) -> dict:
    ev_sha = sha256_file(ev_file)
    art_file = ev_file.parent / "art.whl"
    art_file.write_text("artifact-bytes", encoding="utf-8")
    art_sha = sha256_file(art_file)
    return {
        "$schema": "https://eoip.enterprise.internal/schemas/verification-receipt-v3.json",
        "receipt_id": "rcpt-00000000-0000-0000-0000-000000000001",
        "requirement_clause": "CRA-001.1",
        "state_claimed": "VERIFIED",
        "profile": "P0",
        "source_commit": "0" * 40,
        "source_tree_dirty": False,
        "source_fingerprint": "1" * 64,
        "source_unchanged_during_run": True,
        "artifact_digest": art_sha,
        "artifact_path": str(art_file).replace("\\", "/"),
        "artifact_mtime": "2026-10-18T00:00:00+00:00",
        "runtime": {
            "os": "test-os",
            "python_version": "3.11.9",
            "backend": "test-backend",
        },
        "fixture": {"id": "test-fix"},
        "execution": {
            "command": ["pytest"],
            "exit_code": 0,
            "started_at": "2026-10-18T00:00:01+00:00",
            "completed_at": "2026-10-18T00:00:02+00:00",
        },
        "results": {
            "tests_total": 5,
            "tests_passed": 5,
            "tests_failed": 0,
            "tests_skipped": 0,
            "tests_xfailed": 0,
            "tests_errors": 0,
        },
        "evidence_files": [{"path": str(ev_file).replace("\\", "/"), "sha256": ev_sha}],
        "producer": "test-producer",
        "reviewer": None,
        "review_signature": None,
    }

def test_unknown_state(temp_dir):
    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [{"id": "CRA-001.1", "kind": "clause", "state": "FOOBAR", "updated_at": "2026-10-18T00:00:00Z"}],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "UNKNOWN_STATE" in codes

def test_missing_receipt(temp_dir):
    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [{"id": "CRA-001.1", "kind": "clause", "state": "VERIFIED", "receipts": [], "updated_at": "2026-10-18T00:00:00Z"}],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "MISSING_RECEIPT" in codes

def test_receipt_hash_mismatch(temp_dir):
    ev = temp_dir / "ev.txt"
    ev.write_text("ev", encoding="utf-8")
    rcpt = make_valid_receipt(ev)
    rcpt_path = temp_dir / "rcpt.json"
    rcpt_path.write_text(json.dumps(rcpt), encoding="utf-8")
    
    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [{
            "id": "CRA-001.1",
            "kind": "clause",
            "state": "VERIFIED",
            "receipts": [{"path": str(rcpt_path).replace("\\", "/"), "sha256": "bad" * 21 + "a"}],
            "updated_at": "2026-10-18T00:00:00Z",
        }],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "RECEIPT_HASH_MISMATCH" in codes

def test_nonzero_exit_code(temp_dir):
    ev = temp_dir / "ev.txt"
    ev.write_text("ev", encoding="utf-8")
    rcpt = make_valid_receipt(ev)
    rcpt["execution"]["exit_code"] = 1
    rcpt_path = temp_dir / "rcpt.json"
    rcpt_path.write_text(json.dumps(rcpt), encoding="utf-8")
    r_sha = sha256_file(rcpt_path)

    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [{
            "id": "CRA-001.1",
            "kind": "clause",
            "state": "VERIFIED",
            "receipts": [{"path": str(rcpt_path).replace("\\", "/"), "sha256": r_sha}],
            "updated_at": "2026-10-18T00:00:00Z",
        }],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "NONZERO_EXIT" in codes

def test_no_tests_and_test_failure_and_skipped(temp_dir):
    ev = temp_dir / "ev.txt"
    ev.write_text("ev", encoding="utf-8")
    rcpt = make_valid_receipt(ev)
    rcpt["results"]["tests_total"] = 0
    rcpt["results"]["tests_skipped"] = 1
    rcpt["results"]["tests_failed"] = 1
    rcpt_path = temp_dir / "rcpt.json"
    rcpt_path.write_text(json.dumps(rcpt), encoding="utf-8")
    r_sha = sha256_file(rcpt_path)

    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [{
            "id": "CRA-001.1",
            "kind": "clause",
            "state": "VERIFIED",
            "receipts": [{"path": str(rcpt_path).replace("\\", "/"), "sha256": r_sha}],
            "updated_at": "2026-10-18T00:00:00Z",
        }],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "NO_TESTS" in codes
    assert "TEST_FAILURE" in codes
    assert "SKIPPED_REQUIRED" in codes

def test_source_changed_and_stale_artifact(temp_dir):
    ev = temp_dir / "ev.txt"
    ev.write_text("ev", encoding="utf-8")
    rcpt = make_valid_receipt(ev)
    rcpt["source_unchanged_during_run"] = False
    rcpt["artifact_mtime"] = "2026-10-18T05:00:00+00:00"
    rcpt["execution"]["completed_at"] = "2026-10-18T04:00:00+00:00"
    rcpt_path = temp_dir / "rcpt.json"
    rcpt_path.write_text(json.dumps(rcpt), encoding="utf-8")
    r_sha = sha256_file(rcpt_path)

    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [{
            "id": "CRA-001.1",
            "kind": "clause",
            "state": "VERIFIED",
            "receipts": [{"path": str(rcpt_path).replace("\\", "/"), "sha256": r_sha}],
            "updated_at": "2026-10-18T00:00:00Z",
        }],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "SOURCE_CHANGED" in codes
    assert "STALE_ARTIFACT" in codes

def test_unreviewed_and_self_review(temp_dir):
    ev = temp_dir / "ev.txt"
    ev.write_text("ev", encoding="utf-8")
    rcpt = make_valid_receipt(ev)
    rcpt["state_claimed"] = "ACCEPTED"
    rcpt["producer"] = "alice"
    rcpt["reviewer"] = "alice"
    rcpt["review_signature"] = "sig-alice"
    rcpt_path = temp_dir / "rcpt.json"
    rcpt_path.write_text(json.dumps(rcpt), encoding="utf-8")
    r_sha = sha256_file(rcpt_path)

    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [{
            "id": "CRA-001.1",
            "kind": "clause",
            "state": "ACCEPTED",
            "receipts": [{"path": str(rcpt_path).replace("\\", "/"), "sha256": r_sha}],
            "updated_at": "2026-10-18T00:00:00Z",
        }],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "SELF_REVIEW" in codes

def test_child_open(temp_dir):
    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [
            {"id": "CRA-001.1", "parent": "CRA-001", "kind": "clause", "state": "OPEN", "updated_at": "2026-10-18T00:00:00Z"},
            {"id": "CRA-001.A", "parent": "CRA-001", "kind": "acceptance", "state": "ACCEPTED", "receipts": [], "updated_at": "2026-10-18T00:00:00Z"},
        ],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "CHILD_OPEN" in codes

def test_blocked_item(temp_dir):
    led = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [
            {"id": "H-17", "kind": "decision", "state": "BLOCKED", "updated_at": "2026-10-18T00:00:00Z"},
            {"id": "CRA-044.1", "parent": "CRA-044", "kind": "clause", "state": "VERIFIED", "blocked_by": ["H-17"], "receipts": [], "updated_at": "2026-10-18T00:00:00Z"},
        ],
    }
    led_path = temp_dir / "ledger.json"
    led_path.write_text(json.dumps(led), encoding="utf-8")
    violations = verify_ledger(led_path)
    codes = [v["code"] for v in violations]
    assert "BLOCKED" in codes
