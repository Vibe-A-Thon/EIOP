"""FT-F01: ASG loading fails closed (no default file, hashed entries, denylist)."""

from __future__ import annotations

import hashlib
import os
import secrets

import pytest

from apps.api import asg as asg_mod
from apps.api.asg import ASGConfigurationError, default_keys_path, load_asg, token_digest


def _tok() -> str:
    return "eoip_test_" + secrets.token_urlsafe(32)


def _write(tmp_path, text: str, mode: int = 0o400):
    p = tmp_path / "asg"
    if p.exists():
        os.chmod(p, 0o600)  # Windows refuses to unlink read-only files
        p.unlink()
    p.write_text(text, encoding="utf-8")
    os.chmod(p, mode)
    return p


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    for key in ("EOIP_ASG_FILE", "EOIP_REVOKED_TOKEN_SHA256_FILE", "EOIP_ENV",
                "EOIP_ASG_ALLOW_PLAINTEXT", "EOIP_BOOTSTRAP_SUPERADMIN"):
        monkeypatch.delenv(key, raising=False)


def test_no_repository_default_path():
    assert default_keys_path() is None


def test_no_file_and_no_token_refuses_to_start():
    with pytest.raises(ASGConfigurationError, match="no principals"):
        load_asg(None, None)


def test_missing_configured_file_is_fatal(tmp_path):
    with pytest.raises(ASGConfigurationError, match="missing"):
        load_asg(str(tmp_path / "nope"), _tok())


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits")
def test_group_or_world_accessible_file_is_fatal(tmp_path):
    p = _write(tmp_path, f"sha256:{token_digest(_tok())} | viewer | default | v\n", mode=0o644)
    with pytest.raises(ASGConfigurationError, match="group/world"):
        load_asg(str(p), _tok())


def test_plaintext_entry_rejected_outside_dev(tmp_path, monkeypatch):
    p = _write(tmp_path, f"{_tok()} | admin | default | a\n")
    with pytest.raises(ASGConfigurationError, match="plaintext"):
        load_asg(str(p), _tok())
    monkeypatch.setenv("EOIP_ASG_ALLOW_PLAINTEXT", "true")  # not enough without EOIP_ENV=dev
    with pytest.raises(ASGConfigurationError, match="plaintext"):
        load_asg(str(p), _tok())


def test_plaintext_entry_allowed_only_in_explicit_dev_profile(tmp_path, monkeypatch):
    token = _tok()
    p = _write(tmp_path, f"plain:{token} | analyst | default | dev-analyst\n")
    monkeypatch.setenv("EOIP_ENV", "dev")
    monkeypatch.setenv("EOIP_ASG_ALLOW_PLAINTEXT", "true")
    registry = load_asg(str(p), None)
    assert registry.authenticate(token).username == "dev-analyst"


def test_malformed_line_is_fatal(tmp_path):
    p = _write(tmp_path, "sha256:nothex | admin | default | a\n")
    with pytest.raises(ASGConfigurationError, match="malformed"):
        load_asg(str(p), _tok())
    p = _write(tmp_path, f"sha256:{token_digest(_tok())} | root | default | a\n")
    with pytest.raises(ASGConfigurationError, match="unknown role"):
        load_asg(str(p), _tok())


def test_revoked_entry_and_revoked_bootstrap_are_fatal(tmp_path):
    bad = _tok()
    p = _write(tmp_path, f"sha256:{token_digest(bad)} | viewer | default | v\n")
    with pytest.raises(ASGConfigurationError, match="revoked"):
        load_asg(str(p), _tok(), revoked={token_digest(bad)})
    with pytest.raises(ASGConfigurationError, match="revoked"):
        load_asg(None, bad, revoked={token_digest(bad)})


def test_revoked_file_from_env(tmp_path, monkeypatch):
    bad = _tok()
    rev = tmp_path / "revoked"
    rev.write_text(f"# old tokens\n{token_digest(bad)}\n", encoding="utf-8")
    monkeypatch.setenv("EOIP_REVOKED_TOKEN_SHA256_FILE", str(rev))
    with pytest.raises(ASGConfigurationError, match="revoked"):
        load_asg(None, bad)


def test_runtime_rejects_short_or_revoked_bootstrap_token(tmp_path, monkeypatch):
    from eoip import runtime

    monkeypatch.setenv("EOIP_API_TOKEN", "x" * 31)
    with pytest.raises(RuntimeError, match="32"):
        runtime.api_token()
    good = _tok()
    monkeypatch.setenv("EOIP_API_TOKEN", good)
    assert runtime.api_token() == good
    rev = tmp_path / "revoked"
    rev.write_text(token_digest(good) + "\n", encoding="utf-8")
    monkeypatch.setenv("EOIP_REVOKED_TOKEN_SHA256_FILE", str(rev))
    with pytest.raises(RuntimeError, match="revoked"):
        runtime.api_token()
    monkeypatch.delenv("EOIP_API_TOKEN")
    with pytest.raises(RuntimeError):
        runtime.api_token()


def test_hashed_entries_authenticate_and_others_are_rejected(tmp_path):
    viewer, admin, boot = _tok(), _tok(), _tok()
    p = _write(tmp_path, "\n".join([
        "# comment",
        f"sha256:{token_digest(viewer)} | viewer | default | v",
        f"SHA256:{token_digest(admin).upper()} | admin | acme | a",
    ]) + "\n")
    registry = load_asg(str(p), boot)
    assert registry.authenticate(viewer).roles == ("viewer",)
    assert registry.authenticate(admin).tenant_id == "acme"
    assert set(registry.authenticate(boot).roles) == {"superadmin", "admin", "system"}
    assert registry.authenticate(_tok()) is None
    assert registry.authenticate("") is None
    assert registry.authenticate(token_digest(viewer)) is None  # the digest is not a credential


def test_summary_and_repr_never_expose_digests(tmp_path):
    t = _tok()
    p = _write(tmp_path, f"sha256:{token_digest(t)} | viewer | default | v\n")
    registry = load_asg(str(p), _tok())
    text = repr(registry.entries) + repr(registry.summary())
    assert token_digest(t) not in text and t not in text


def test_bootstrap_superadmin_can_be_disabled(monkeypatch):
    boot = _tok()
    monkeypatch.setenv("EOIP_BOOTSTRAP_SUPERADMIN", "false")
    registry = load_asg(None, boot)
    assert registry.authenticate(boot).roles == ("admin", "system")


def test_entries_store_digests_not_tokens(tmp_path):
    t = _tok()
    p = _write(tmp_path, f"sha256:{hashlib.sha256(t.encode()).hexdigest()} | viewer | default | v\n")
    entry = load_asg(str(p), None).entries[0]
    assert not hasattr(entry, "token")
    assert entry.token_sha256 == token_digest(t)
    assert asg_mod.MIN_TOKEN_LENGTH == 32
