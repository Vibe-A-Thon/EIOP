"""FT-D08: clause -> test mapping used to regenerate real ledger receipts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "acceptance"))
from clause_tests import clause_test_map  # noqa: E402


def test_maps_by_function_name_and_docstring(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_x.py").write_text(
        'def test_cra_007_3_thing():\n    pass\n\n'
        'def test_other():\n    """CRA-012.A: acceptance."""\n\n'
        'class TestK:\n    def test_cra_002_11_k(self):\n        pass\n\n'
        'def test_unrelated():\n    """Mentions nothing."""\n'
    )
    mapping = clause_test_map(tmp_path)
    assert mapping == {
        "CRA-007.3": ["tests/test_x.py::test_cra_007_3_thing"],
        "CRA-012.A": ["tests/test_x.py::test_other"],
        "CRA-002.11": ["tests/test_x.py::TestK::test_cra_002_11_k"],
    }


def test_repository_clause_tests_cover_the_ledger_clauses():
    mapping = clause_test_map(Path(__file__).resolve().parents[2])
    assert "CRA-001.9" in mapping
    assert all(ids for ids in mapping.values())


def test_file_fallback_uses_exact_citations_only(tmp_path):
    from clause_tests import clause_file_map

    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_m.py").write_text('"""Covers (CRA-018.4, CRA-018.8) and CRA-031.1 - CRA-031.7."""\n')
    assert clause_file_map(tmp_path) == {
        "CRA-018.4": ["tests/test_m.py"],
        "CRA-018.8": ["tests/test_m.py"],
        "CRA-031.1": ["tests/test_m.py"],
        "CRA-031.7": ["tests/test_m.py"],
    }
