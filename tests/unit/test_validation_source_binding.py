import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.validate_with_evidence import capture_source, validate_command


@pytest.fixture
def repository(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text("test-results/\nsecrets/\n", encoding="utf-8")
    (tmp_path / "source.py").write_text("VALUE = 1\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", ".gitignore", "source.py"], check=True)
    subprocess.run([
        "git", "-C", str(tmp_path), "-c", "user.name=Evidence Test",
        "-c", "user.email=evidence@example.invalid", "commit", "-qm", "fixture",
    ], check=True)
    return tmp_path


def run(repository, code, *, artifacts=(), timeout=None):
    return validate_command(
        repository, [sys.executable, "-c", code],
        output=repository / "test-results" / "receipt.json",
        artifacts=artifacts, timeout=timeout,
    )


@pytest.mark.req("MVP-FR-027")
def test_executes_command_and_persists_source_bound_fresh_artifact(repository):
    artifact = repository / "test-results" / "results.xml"
    receipt = run(
        repository,
        "from pathlib import Path; p=Path('test-results/results.xml'); "
        "p.parent.mkdir(); p.write_text('<testsuites/>')",
        artifacts=[artifact],
    )
    assert receipt["status"] == "PASS"
    assert receipt["source_unchanged"] is True
    assert receipt["source_content_bound"] is True
    assert receipt["source_revision_bound"] is True
    assert receipt["artifacts_fresh"] is True
    assert receipt["artifacts"][str(artifact)]["sha256"]
    assert json.loads((repository / "test-results" / "receipt.json").read_text()) == receipt


def test_dirty_source_can_be_content_bound_but_not_revision_bound(repository):
    (repository / "source.py").write_text("VALUE = 2\n", encoding="utf-8")
    receipt = run(repository, "pass")
    assert receipt["status"] == "PASS"
    assert receipt["source_content_bound"] is True
    assert receipt["source_revision_bound"] is False


@pytest.mark.parametrize("code", [
    "from pathlib import Path; Path('source.py').write_text('changed')",
    "from pathlib import Path; Path('added.py').write_text('added')",
    "from pathlib import Path; Path('source.py').unlink()",
])
def test_changed_added_or_removed_source_refuses_pass(repository, code):
    receipt = run(repository, code)
    assert receipt["command_exit_code"] == 0
    assert receipt["status"] == "FAIL"
    assert receipt["source_unchanged"] is False


def test_command_failure_is_persisted(repository):
    receipt = run(repository, "raise SystemExit(7)")
    assert receipt["status"] == "FAIL"
    assert receipt["command_exit_code"] == 7


def test_launch_failure_is_persisted(repository):
    receipt = validate_command(
        repository, [str(repository / "missing-program")],
        output=repository / "test-results" / "receipt.json",
    )
    assert receipt["status"] == "FAIL"
    assert receipt["execution_error"]
    assert receipt["command_exit_code"] is None


def test_timeout_is_a_failed_receipt(repository):
    receipt = run(repository, "import time; time.sleep(5)", timeout=0.05)
    assert receipt["status"] == "FAIL"
    assert receipt["execution_error"] == "TimeoutExpired"


@pytest.mark.parametrize("existing", [False, True])
def test_missing_or_unchanged_artifact_is_not_fresh(repository, existing):
    artifact = repository / "test-results" / "results.xml"
    if existing:
        artifact.parent.mkdir()
        artifact.write_text("old", encoding="utf-8")
    receipt = run(repository, "pass", artifacts=[artifact])
    assert receipt["status"] == "FAIL"
    assert receipt["artifacts_fresh"] is False


def test_rewritten_identical_content_is_fresh(repository):
    artifact = repository / "test-results" / "results.xml"
    artifact.parent.mkdir()
    artifact.write_text("same", encoding="utf-8")
    receipt = run(
        repository, "from pathlib import Path; Path('test-results/results.xml').write_text('same')",
        artifacts=[artifact],
    )
    assert receipt["status"] == "PASS"


def test_scope_exclusions_and_secrets_are_not_read(repository, monkeypatch):
    for name in [
        "EOIP-engg-doc-pkg/KGR-requirements.md",
        "EOIP-engg-doc-pkg/KGR-implementation-plan.md",
        "secrets/token.txt", "secrets.example/api-token.txt",
        "deploy/.env", "node_modules/example.txt", ".data/private.txt",
    ]:
        path = repository / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("DO_NOT_READ", encoding="utf-8")
        subprocess.run(["git", "-C", str(repository), "add", "-f", name], check=True)
    original_open = Path.open

    def guarded_open(path, *args, **kwargs):
        if path.name in {"KGR-requirements.md", "KGR-implementation-plan.md", "token.txt", "api-token.txt", ".env"}:
            raise AssertionError("protected content must not be opened")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    snapshot = capture_source(repository)
    assert set(snapshot["files"]) == {".gitignore", "source.py"}
    receipt = run(
        repository,
        "from pathlib import Path; Path('EOIP-engg-doc-pkg/KGR-requirements.md').write_text('updated')",
    )
    assert receipt["status"] == "PASS"
    assert receipt["source_revision_bound"] is False


def test_head_change_refuses_pass_even_when_contents_unchanged(repository):
    receipt = run(
        repository,
        "import subprocess; subprocess.run(['git','-c','user.name=Test',"
        "'-c','user.email=test@example.invalid','commit','--allow-empty','-qm','advance'],check=True)",
    )
    assert receipt["status"] == "FAIL"
    assert receipt["source_unchanged"] is False


@pytest.mark.parametrize("target", [
    "source.py", "SOURCE.py", "../outside.json", "EOIP-engg-doc-pkg/KGR-requirements.md", "secrets/result.json",
])
def test_refuses_artifact_paths_that_hide_tracked_or_excluded_source(repository, target):
    with pytest.raises(ValueError):
        validate_command(
            repository, [sys.executable, "-c", "pass"],
            output=repository / "test-results" / "receipt.json", artifacts=[repository / target],
        )


def test_refuses_empty_command(repository):
    with pytest.raises(ValueError, match="command"):
        validate_command(repository, [], output=repository / "test-results" / "receipt.json")


def test_old_timestamp_on_changed_artifact_does_not_prove_freshness(repository):
    artifact = repository / "test-results" / "results.xml"
    artifact.parent.mkdir()
    artifact.write_text("old", encoding="utf-8")
    receipt = run(
        repository, "from pathlib import Path; import os; p=Path('test-results/results.xml'); "
        "p.write_text('changed'); os.utime(p, ns=(1, 1))", artifacts=[artifact],
    )
    assert receipt["status"] == "FAIL"
    assert receipt["artifacts_fresh"] is False


def test_refuses_identical_receipt_and_artifact_paths(repository):
    output = repository / "test-results" / "receipt.json"
    with pytest.raises(ValueError, match="distinct"):
        validate_command(repository, [sys.executable, "-c", "pass"], output=output, artifacts=[output])


def test_source_symlink_is_hashed_without_opening_its_target(repository, monkeypatch):
    source = repository / "source.py"
    original_is_symlink = Path.is_symlink
    original_open = Path.open

    def is_symlink(path):
        return path == source or original_is_symlink(path)

    def guarded_open(path, *args, **kwargs):
        if path == source:
            raise AssertionError("source symlink must not be dereferenced")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "is_symlink", is_symlink)
    monkeypatch.setattr(Path, "readlink", lambda path: Path("../outside/private.txt"))
    monkeypatch.setattr(Path, "open", guarded_open)
    snapshot = capture_source(repository)
    assert snapshot["files"]["source.py"]["kind"] == "symlink"


def test_post_execution_capture_error_is_not_success(repository, monkeypatch):
    from scripts import validate_with_evidence as wrapper

    original_capture = wrapper.capture_source
    calls = 0

    def capture(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("cannot inspect source")
        return original_capture(*args, **kwargs)

    monkeypatch.setattr(wrapper, "capture_source", capture)
    receipt = run(repository, "pass")
    assert receipt["status"] == "FAIL"
    assert receipt["source_after"] is None
    assert "post-command source capture failed: OSError" in receipt["errors"]


def test_child_staging_artifact_cannot_produce_pass(repository):
    artifact = repository / "test-results" / "results.xml"
    receipt = run(
        repository,
        "from pathlib import Path; import subprocess; "
        "p=Path('test-results/results.xml'); p.parent.mkdir(); p.write_text('fresh'); "
        "subprocess.run(['git', 'add', '-f', str(p)], check=True)",
        artifacts=[artifact],
    )
    assert receipt["status"] == "FAIL"
    assert receipt["artifacts_fresh"] is False
    assert any("artifact inspection failed" in error for error in receipt["errors"])


def test_child_staging_receipt_is_not_overwritten(repository):
    with pytest.raises(ValueError, match="Git-tracked"):
        run(
            repository,
            "from pathlib import Path; import subprocess; "
            "p=Path('test-results/receipt.json'); p.parent.mkdir(); p.write_text('child source'); "
            "subprocess.run(['git', 'add', '-f', str(p)], check=True)",
        )
    assert (repository / "test-results" / "receipt.json").read_text() == "child source"


@pytest.mark.parametrize("name", [".git/HEAD", ".git/config"])
def test_receipt_cannot_overwrite_git_metadata(repository, name):
    path = repository / name
    before = path.read_bytes()
    with pytest.raises(ValueError, match="protected"):
        validate_command(repository, [sys.executable, "-c", "pass"], output=path)
    assert path.read_bytes() == before


def test_cli_executes_and_returns_failure_for_child_failure(repository):
    result = subprocess.run([
        sys.executable, "-m", "scripts.validate_with_evidence",
        "--project-root", str(repository),
        "--output", str(repository / "test-results" / "receipt.json"),
        "--", sys.executable, "-c", "raise SystemExit(9)",
    ], cwd=Path(__file__).resolve().parents[2], check=False)
    assert result.returncode == 9
    assert json.loads((repository / "test-results" / "receipt.json").read_text())["status"] == "FAIL"


def test_cli_without_command_does_not_silently_succeed(repository):
    result = subprocess.run([
        sys.executable, "-m", "scripts.validate_with_evidence",
        "--project-root", str(repository),
        "--output", str(repository / "test-results" / "receipt.json"),
    ], cwd=Path(__file__).resolve().parents[2], check=False)
    assert result.returncode != 0
    assert not (repository / "test-results" / "receipt.json").exists()