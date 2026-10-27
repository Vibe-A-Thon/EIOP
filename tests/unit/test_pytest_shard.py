"""CI test sharding (eoip.verification.pytest_shard) and its partition proof."""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
from eoip.verification.pytest_shard import assign_files, parse_shard

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "ci" / "check_test_shards.py"


def test_parse_shard_accepts_and_rejects():
    assert parse_shard("2/4") == (2, 4)
    assert parse_shard(" 1 / 1 ") == (1, 1)
    for bad in ("0/4", "5/4", "1/0", "a/b", "2", "-1/3", ""):
        with pytest.raises(pytest.UsageError):
            parse_shard(bad)


def test_assignment_is_complete_disjoint_and_order_independent():
    files = [f"tests/t{i}.py" for i in range(23)]
    weights = {f: float(i % 7) for i, f in enumerate(files[:15])}  # 8 files unknown -> median
    first = assign_files(files, 4, weights)
    assert sorted(first) == sorted(files)
    assert set(first.values()) == {1, 2, 3, 4}
    assert assign_files(list(reversed(files)), 4, weights) == first
    assert assign_files(files + files[:3], 4, weights) == first  # duplicates collapse


def test_more_shards_than_files_leaves_empty_shards():
    assert sorted(assign_files(["a.py", "b.py"], 5, {}).values()) == [1, 2]


def test_heavy_file_is_balanced_against_many_light_files():
    weights = {"heavy.py": 100.0, **{f"l{i}.py": 10.0 for i in range(10)}}
    loads = {1: 0.0, 2: 0.0}
    for name, slot in assign_files(list(weights), 2, weights).items():
        loads[slot] += weights[name]
    assert loads == {1: 100.0, 2: 100.0}


def _project(tmp_path: Path) -> Path:
    (tmp_path / "conftest.py").write_text('pytest_plugins = ["eoip.verification.pytest_shard"]\n')
    for i in range(7):
        body = "".join(f"def test_{i}_{j}():\n    pass\n" for j in range(i % 3 + 1))
        (tmp_path / f"test_mod{i}.py").write_text(body)
    (tmp_path / "test_param.py").write_text(textwrap.dedent("""
        import pytest
        @pytest.mark.parametrize("v", [1, 2, 3])
        def test_p(v):
            pass
    """))
    return tmp_path


def _run(project: Path, env_extra: dict[str, str]) -> subprocess.CompletedProcess:
    import os
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(REPO_ROOT / "packages"), str(REPO_ROOT)])}
    for key in ("EOIP_TEST_SHARD", "EOIP_TEST_SHARD_MANIFEST", "EOIP_TEST_SHARD_WEIGHTS", "EOIP_TEST_QUARANTINE_FILE"):
        env.pop(key, None)
    env.update(env_extra)
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=",
                           str(project)], cwd=project, env=env, capture_output=True, text=True, timeout=120, check=False)


def test_real_pytest_runs_partition_the_suite(tmp_path):
    project = _project(tmp_path)
    manifests = []
    for shard in (1, 2, 3):
        out = tmp_path / f"m{shard}.json"
        res = _run(project, {"EOIP_TEST_SHARD": f"{shard}/3", "EOIP_TEST_SHARD_MANIFEST": str(out)})
        assert res.returncode == 0, res.stdout + res.stderr
        manifests.append(out)
    data = [json.loads(p.read_text()) for p in manifests]
    assert len(data[0]["collected"]) == 16
    assert sum(len(d["assigned"]) for d in data) == 16
    assert all(d["assigned"] for d in data)
    # parametrized cases of one file stay together
    owners = {d["shard"] for d in data for n in d["assigned"] if n.startswith("test_param.py")}
    assert len(owners) == 1
    ok = subprocess.run([sys.executable, str(CHECKER), *map(str, manifests)], capture_output=True, text=True, check=False)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    missing = subprocess.run([sys.executable, str(CHECKER), *map(str, manifests[:2])], capture_output=True, text=True, check=False)
    assert missing.returncode == 1 and "exactly once" in missing.stderr


def test_empty_shard_exits_zero_and_unsharded_run_is_untouched(tmp_path):
    project = _project(tmp_path)
    res = _run(project, {"EOIP_TEST_SHARD": "12/12"})  # 8 files, 12 shards -> shard 12 empty
    assert res.returncode == 0, res.stdout + res.stderr
    assert "deselected" in res.stdout
    plain = _run(project, {})
    assert plain.returncode == 0 and "16 passed" in plain.stdout


def test_malformed_shard_fails_loudly(tmp_path):
    res = _run(_project(tmp_path), {"EOIP_TEST_SHARD": "4/3"})
    assert res.returncode != 0
    assert "EOIP_TEST_SHARD" in res.stdout + res.stderr


def test_checker_detects_overlap_and_divergent_collection(tmp_path):
    def write(name, shard, collected, assigned):
        path = tmp_path / name
        path.write_text(json.dumps({"shard": shard, "total": 2, "collected": collected, "assigned": assigned}))
        return str(path)

    overlap = [write("a.json", 1, ["x", "y"], ["x", "y"]), write("b.json", 2, ["x", "y"], ["y"])]
    res = subprocess.run([sys.executable, str(CHECKER), *overlap], capture_output=True, text=True, check=False)
    assert res.returncode == 1 and "assigned to shards 1 and 2" in res.stderr
    diverge = [write("c.json", 1, ["x"], ["x"]), write("d.json", 2, ["x", "z"], ["z"])]
    res = subprocess.run([sys.executable, str(CHECKER), *diverge], capture_output=True, text=True, check=False)
    assert res.returncode == 1 and "different suite" in res.stderr


def test_shard_settings_are_not_inherited_by_child_processes(tmp_path):
    (tmp_path / "conftest.py").write_text('pytest_plugins = ["eoip.verification.pytest_shard"]\n')
    (tmp_path / "test_env.py").write_text(
        "import os\n"
        "def test_child_sees_no_shard():\n"
        "    assert 'EOIP_TEST_SHARD' not in os.environ\n"
        "    assert 'EOIP_TEST_SHARD_MANIFEST' not in os.environ\n"
    )
    res = _run(tmp_path, {"EOIP_TEST_SHARD": "1/1", "EOIP_TEST_SHARD_MANIFEST": str(tmp_path / "m.json")})
    assert res.returncode == 0, res.stdout + res.stderr
    assert json.loads((tmp_path / "m.json").read_text())["assigned"] == ["test_env.py::test_child_sees_no_shard"]


def test_checker_warns_but_passes_on_unstable_node_ids(tmp_path):
    def write(name, shard, collected, assigned):
        path = tmp_path / name
        path.write_text(json.dumps({"shard": shard, "total": 2, "collected": collected, "assigned": assigned}))
        return str(path)

    files = [write("a.json", 1, ["t.py::x[1.0]", "u.py::y"], ["t.py::x[1.0]"]),
             write("b.json", 2, ["t.py::x[2.0]", "u.py::y"], ["u.py::y"])]
    res = subprocess.run([sys.executable, str(CHECKER), *files], capture_output=True, text=True, check=False)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "non-deterministic" in res.stdout and "t.py" in res.stdout
