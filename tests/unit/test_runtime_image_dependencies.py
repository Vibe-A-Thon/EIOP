"""FT-X03 / FT-F06 / FT-D14: runtime image and documented install carry the imported dependencies."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _pins(path: Path) -> dict[str, str]:
    pins = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Za-z0-9_.\-]+)==([^\s;\\]+)", line)
        if m:
            pins[m.group(1).lower().replace("_", "-")] = m.group(2)
    return pins


def test_runtime_images_install_hash_pinned_numerics_lock():
    for name in ("Dockerfile", "Containerfile"):
        text = (REPO_ROOT / "deploy" / name).read_text(encoding="utf-8")
        runtime = text.split(" AS test")[0]
        assert "requirements-numerics.lock" in runtime, name
        assert re.search(r"--require-hashes[^\n]*requirements-numerics\.lock", runtime), name


def test_numerics_lock_is_hashed_and_matches_neural_lock():
    numerics = REPO_ROOT / "requirements-numerics.lock"
    pins = _pins(numerics)
    assert {"numpy", "scipy", "scikit-learn", "joblib", "threadpoolctl", "cloudpickle"} <= set(pins)
    blocks = re.split(r"\n(?=[A-Za-z])", numerics.read_text(encoding="utf-8"))
    assert all("--hash=sha256:" in b for b in blocks if re.match(r"[A-Za-z]", b))
    neural = _pins(REPO_ROOT / "requirements-neural.lock")
    assert all(neural[k] == v for k, v in pins.items())


def test_processing_module_imports_numpy_at_module_level():
    # Guard that the image fix is still needed / still sufficient.
    text = (REPO_ROOT / "packages" / "eoip" / "processing" / "service.py").read_text(encoding="utf-8")
    if re.search(r"^import numpy", text, re.M):
        assert "numpy" in _pins(REPO_ROOT / "requirements-numerics.lock")


def test_test_extra_covers_default_suite_dependencies():
    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    extras = project["optional-dependencies"]
    assert any("pyshacl" in dep for dep in extras["semantic"])  # FT-D14
    composite = extras["test"][0]
    for extra in ("dev", "numerics", "fileparse", "codeparse", "reports", "semantic"):
        assert extra in composite
    for doc in ("README.md", "docs/getting-started.md"):
        assert 'pip install -c requirements.lock -e ".[test]"' in (REPO_ROOT / doc).read_text(encoding="utf-8")
