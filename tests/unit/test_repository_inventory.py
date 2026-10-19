"""Inventory safety and honest static-analysis boundaries."""

import json
from pathlib import Path

import pytest

from scripts.repository_inventory import exclusion, inspect_file, python_summary


@pytest.mark.parametrize("name", [
    ".env", "deploy/.env.example", "Logins_credentials.keys", "secrets/key.txt",
    "node_modules/pkg/index.js", ".audit-scratch/ledger.json", "../outside.py",
    "C:/outside.py", "..\\outside.py", "docs/generated/repository-inventory.json",
    "memory/test_credentials.md",
])
def test_excluded_inputs_are_not_opened(tmp_path, name):
    assert exclusion(name)
    assert inspect_file(tmp_path, name)["status"] == "excluded"


def test_python_summary_is_discovery_not_execution(tmp_path):
    path = tmp_path / "app.py"
    path.write_text('import os\nraise RuntimeError("never execute")\n'
                    '@router.get("/items")\ndef items():\n    return "SECRET-CANARY"\n', encoding="utf-8")
    result = inspect_file(tmp_path, "app.py")
    assert result["semantic_review"] == "not_asserted"
    assert result["status"] == "text_read"
    assert result["python"]["route_candidates"] == [{"method": "GET", "path": "/items", "line": 4}]
    assert "SECRET-CANARY" not in json.dumps(result)
    assert len(result["sha256"]) == 64


def test_syntax_error_and_binary_are_reported_without_success_claims(tmp_path):
    assert python_summary("def invalid(")["parse_status"] == "syntax_error"
    (tmp_path / "asset.bin").write_bytes(b"\x00\xff")
    assert inspect_file(tmp_path, "asset.bin")["status"] == "binary_hashed"
    assert inspect_file(tmp_path, "missing.py")["status"] == "unread"


def test_manifest_emits_names_not_command_or_secret_values(tmp_path):
    (tmp_path / "package.json").write_text(json.dumps({
        "name": "fixture", "version": "1.0.0", "scripts": {"test": "SECRET-CANARY"},
        "dependencies": {"example": "1.0"},
    }), encoding="utf-8")
    result = inspect_file(tmp_path, "package.json")
    assert result["package"]["script_names"] == ["test"]
    assert "SECRET-CANARY" not in json.dumps(result)


def test_symlink_is_not_followed(tmp_path, monkeypatch):
    original = Path.is_symlink
    monkeypatch.setattr(Path, "is_symlink", lambda self: self.name == "linked.py" or original(self))
    assert inspect_file(tmp_path, "linked.py")["reason"] == "symlink"
