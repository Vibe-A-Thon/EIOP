"""Compliance gate proving zero nvidia-* and cuda packages in distributed configuration (CRA-043.11, ADR-H16)."""
from __future__ import annotations
from pathlib import Path
import pytest

def scan_text_for_cuda(text: str) -> list[str]:
    violations = []
    for line in text.splitlines():
        line_clean = line.strip().lower()
        if line_clean.startswith("#") or not line_clean:
            continue
        if "nvidia-" in line_clean or "nvidia_" in line_clean:
            violations.append(line.strip())
        elif "torch-cuda" in line_clean or "cu11" in line_clean or "cu12" in line_clean:
            violations.append(line.strip())
    return violations

def test_pyproject_toml_no_cuda():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    violations = scan_text_for_cuda(pyproject)
    assert violations == [], f"Found forbidden CUDA/nvidia packages in pyproject.toml: {violations}"

def test_requirements_lock_files_no_cuda():
    lock_files = list(Path(".").glob("requirements*.lock"))
    for lf in lock_files:
        text = lf.read_text(encoding="utf-8")
        violations = scan_text_for_cuda(text)
        assert violations == [], f"Found forbidden CUDA/nvidia packages in {lf}: {violations}"

def test_fixture_with_cuda_rejected():
    fixture_text = """
    numpy==1.26.4
    torch==2.2.2+cu121
    nvidia-cuda-runtime-cu12==12.1.105
    """
    violations = scan_text_for_cuda(fixture_text)
    assert len(violations) == 2
