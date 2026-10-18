"""Verification of baseline facts, defect probe, and profile manifests (CRA-001.5, CRA-001.11-001.13)."""
from __future__ import annotations
import json
from pathlib import Path
import yaml
import pytest

def test_baseline_facts_file():
    facts_path = Path(".audit-scratch/baseline/facts.json")
    assert facts_path.exists(), "facts.json must exist in .audit-scratch/baseline/"
    data = json.loads(facts_path.read_text(encoding="utf-8"))
    assert "measured_at_commit" in data
    assert "facts" in data
    facts_by_id = {f["id"]: f for f in data["facts"]}
    assert "python_version" in facts_by_id
    assert "packages_py_files" in facts_by_id
    assert "tests_files_count" in facts_by_id
    assert "connectors_py_files" in facts_by_id
    assert "ontology_py_files" in facts_by_id
    assert "fileparse_py_files" in facts_by_id

def test_baseline_defect_probe():
    probe_path = Path(".audit-scratch/baseline/g01-g03-probe.txt")
    assert probe_path.exists(), "g01-g03-probe.txt must exist in .audit-scratch/baseline/"
    content = probe_path.read_text(encoding="utf-8")
    assert "conforms" in content
    assert "True" in content

def test_profile_manifests():
    for p in ("P0", "P1", "P2"):
        p_path = Path(f"benchmarks/profiles/{p}.yaml")
        assert p_path.exists(), f"Profile manifest {p_path} must exist"
        data = yaml.safe_load(p_path.read_text(encoding="utf-8"))
        assert data["profile"] == p
        assert "binding" in data
        assert "asserted_triples" in data["binding"]
        assert "reference_compute" in data["binding"]
        assert "accelerator" in data["binding"]

def test_decision_records():
    decisions_dir = Path("docs/decisions")
    assert (decisions_dir / "ADR-H15-numerical-stack-tiers.md").exists()
    assert (decisions_dir / "ADR-H16-no-cuda-redistribution.md").exists()
    assert (decisions_dir / "ADR-H17-gpu-availability.md").exists()
