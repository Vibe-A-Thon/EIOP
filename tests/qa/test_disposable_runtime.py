from pathlib import Path
from unittest.mock import Mock

from qa.runtime import environment


def test_environment_replaces_shared_state_and_credentials_without_mutation(tmp_path):
    inherited = {"EOIP_DATA_DIR": "shared", "EOIP_API_TOKEN": "not-for-tests",
                 "EOIP_ASG_FILE": "shared.keys", "PATH": "keep-path"}
    result = environment(tmp_path, inherited)
    assert inherited["EOIP_DATA_DIR"] == "shared"
    assert result["EOIP_DATA_DIR"] == str(tmp_path / "data")
    assert result["EOIP_ASG_FILE"] == str(tmp_path / "no-shared-credentials.keys")
    assert result["EOIP_GRAPH_BACKEND"] == "memory"
    assert len(result["EOIP_API_TOKEN"]) >= 24
    assert result["EOIP_API_TOKEN"] != inherited["EOIP_API_TOKEN"]
    assert result["PATH"] == "keep-path"
    assert result["QA_REPORTS_DIR"] == str(tmp_path / "reports")


def test_each_runtime_gets_a_distinct_credential(tmp_path):
    assert environment(tmp_path, {})["EOIP_API_TOKEN"] != environment(tmp_path, {})["EOIP_API_TOKEN"]


def test_learning_default_uses_runtime_root(monkeypatch, tmp_path):
    import eoip.brain.router as router

    engine = Mock()
    engine.load_state.return_value = True
    monkeypatch.setattr(router._kernel, "learning_engine", engine)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    target = str((tmp_path / "learning" / "default").resolve())
    assert router.save_learning_state() == {"status": "SAVED", "slot": "default"}
    engine.save_state.assert_called_once_with(target)
    assert router.load_learning_state() == {"status": "LOADED", "slot": "default"}
    engine.load_state.assert_called_once_with(target)
    assert not Path(target).exists()


def test_learning_explicit_path_is_rejected(monkeypatch, tmp_path):
    import pytest
    from fastapi import HTTPException

    import eoip.brain.router as router

    engine = Mock()
    monkeypatch.setattr(router._kernel, "learning_engine", engine)
    target = str(tmp_path / "explicit")
    for call in (router.save_learning_state, router.load_learning_state):
        with pytest.raises(HTTPException) as exc:
            call(directory=target)
        assert exc.value.status_code == 400
    engine.save_state.assert_not_called()
    engine.load_state.assert_not_called()
