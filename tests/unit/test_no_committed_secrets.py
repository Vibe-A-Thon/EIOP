"""FT-F01 / FT-F02 guard: no bearer tokens or ASG credential files in the tracked tree.

The leaked tokens are identified only by SHA-256 digest (plus length) so this test
never contains a secret. Rotation of the real tokens is an operator action; this
test only proves the values are gone from the current tree and stay gone.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# sha256(token) -> token length, for every token found committed at 3ed3acd/76f8e8b
# (Logins_credentials.keys principals, SignIn.tsx DEV_TOKEN, backend/server.py default).
LEAKED_TOKEN_SHA256 = {
    "af79cda6fdaede258752a3faebe215d683e92b0ff7d4954db85b10a4f6a15a1b": 37,
    "83187f542f122432a28fe738e687e9fcffa152b7a2edebeb2b4dbf027dca4cbc": 35,
    "3190765f8a257315aac2a7557b871cb40a2f5afa992c5825260e30daf4f89d06": 37,
    "98faf3400ec23811cc6ca2aeeba8dc405c490e085150205c616ce6f29d9d0d57": 32,
    "5eadd530a5c1e19e2b8bdcded57421c4b72ce13b60c328e0ab1f0d3830b44f0f": 37,
    "f295232eec204f5f5e0d280306f0cbd19cc31e61caf91e709560d9de1a9f78ba": 36,
}
_LENGTHS = sorted(set(LEAKED_TOKEN_SHA256.values()))
_RUN = re.compile(rb"[A-Za-z0-9_\-]{%d,}" % min(_LENGTHS))
# A plaintext ASG principal line: "<long token> | role | tenant | user".
_ASG_PLAINTEXT_LINE = re.compile(
    rb"^\s*(?:plain:)?(?!sha256:)[A-Za-z0-9_\-]{24,}\s*\|\s*(?:superadmin|admin|system|steward|analyst|viewer)\b",
    re.MULTILINE,
)
_NEW_STYLE_TOKEN = re.compile(rb"eoip_pat_[A-Za-z0-9_\-]{20,}")
FORBIDDEN_PATHS = ("Logins_credentials.keys", "memory/test_credentials.md")
MAX_BYTES = 20 * 1024 * 1024


def _tracked_files() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"], cwd=REPO_ROOT, capture_output=True, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    return [p for p in out.decode("utf-8", "surrogateescape").split("\0") if p]


def _contains_leaked_token(data: bytes) -> bool:
    for match in _RUN.finditer(data):
        run = match.group(0)
        for length in _LENGTHS:
            for start in range(0, len(run) - length + 1):
                digest = hashlib.sha256(run[start:start + length]).hexdigest()
                if LEAKED_TOKEN_SHA256.get(digest) == length:
                    return True
    return False


def test_credential_files_are_not_tracked():
    tracked = set(_tracked_files())
    assert not [p for p in FORBIDDEN_PATHS if p in tracked]
    assert not [p for p in tracked if p.endswith(".keys")], "*.keys files must stay out of git"


def test_no_leaked_token_plaintext_or_asg_lines_in_tracked_files():
    offenders: list[str] = []
    for rel in _tracked_files():
        path = REPO_ROOT / rel
        try:
            if not path.is_file() or path.stat().st_size > MAX_BYTES:
                continue
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:4096]:
            continue  # binary
        if _contains_leaked_token(data):
            offenders.append(f"{rel}: contains a revoked F-01/F-02 token")
        if _ASG_PLAINTEXT_LINE.search(data):
            offenders.append(f"{rel}: plaintext ASG principal line")
        if _NEW_STYLE_TOKEN.search(data):
            offenders.append(f"{rel}: eoip_pat_ token")
    assert not offenders, "\n".join(offenders)


def test_detector_recognises_a_leaked_digest_without_the_value():
    # Self-check of the scanner using a synthetic value registered at runtime.
    synthetic = b"synthetic-not-a-secret-value-000000000"
    digest = hashlib.sha256(synthetic).hexdigest()
    LEAKED_TOKEN_SHA256[digest] = len(synthetic)
    _LENGTHS.append(len(synthetic))
    try:
        assert _contains_leaked_token(b"Authorization: Bearer " + synthetic + b"\n")
        assert not _contains_leaked_token(b"Authorization: Bearer " + synthetic[:-1] + b"X\n")
    finally:
        del LEAKED_TOKEN_SHA256[digest]
        _LENGTHS.remove(len(synthetic))
    assert _ASG_PLAINTEXT_LINE.search(b"abcdefghijklmnopqrstuvwxyz0123 | admin | default | x")
    assert not _ASG_PLAINTEXT_LINE.search(b"sha256:" + b"a" * 64 + b" | admin | default | x")
