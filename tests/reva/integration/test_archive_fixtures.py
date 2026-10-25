"""Archive inventory against the deterministic REVA fixtures (REVA-AI-001..003, NFR-012).

Run by the reva-fixtures lane (which pre-builds the fixtures into REVA_FIXTURE_CACHE) and by
reva-integration (which builds them into a temp dir).
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from pathlib import Path

import pytest

from reva.extract.artifacts.inventory import extract_members, inventory_archive
from tests.reva.support.archive_fixtures import build_fixtures, fixture_specs

pytestmark = [pytest.mark.reva_depth("integration"), pytest.mark.reva_fixtures]

SPECS = fixture_specs()
NAMES = sorted(SPECS)


@pytest.fixture(scope="module")
def fixture_dir(tmp_path_factory) -> Path:
    cache = os.environ.get("REVA_FIXTURE_CACHE")
    if cache and (Path(cache) / "manifest.json").exists():
        return Path(cache)
    out = tmp_path_factory.mktemp("reva-fixtures")
    build_fixtures(out)
    return out


@pytest.fixture(scope="module")
def manifest(fixture_dir) -> dict:
    return json.loads((fixture_dir / "manifest.json").read_text(encoding="utf-8"))


@pytest.mark.reva_case("positive")
def test_fixture_files_match_their_declared_digests(fixture_dir, manifest):
    """AG-14: each fixture's declared sha256 matches the file used by this run and the generator."""
    assert sorted(manifest) == NAMES
    for name, entry in manifest.items():
        on_disk = hashlib.sha256((fixture_dir / name).read_bytes()).hexdigest()
        assert on_disk == entry["sha256"] == hashlib.sha256(SPECS[name]["bytes"]).hexdigest(), name
        assert entry["expect"] == SPECS[name]["expect"], f"stale fixture cache for {name}"


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.reva_case("boundary")
def test_inventory_matches_fixture_expectation(fixture_dir, name):
    expect = SPECS[name]["expect"]
    result = inventory_archive(fixture_dir / name)
    assert result.container_format == expect["format"]
    assert {m.member_path: m.sha256 for m in result.members} == expect["members"]
    prefix = expect.get("limitation_prefix")
    if prefix:
        assert any(lim.startswith(prefix) for lim in result.limitations), result.limitations
    else:
        assert result.limitations == []
    assert result.coverage == expect.get("coverage", "complete")
    assert {link.member_path: link.target for link in result.links} == expect.get("links", {})


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.reva_case("positive")
def test_inventory_is_deterministic(fixture_dir, name):
    first = asdict(inventory_archive(fixture_dir / name))
    second = asdict(inventory_archive(fixture_dir / name))
    assert first == second


@pytest.mark.parametrize("name", ["traversal.zip", "absolute.tar", "symlink-escape.tar"])
@pytest.mark.reva_case("negative")
def test_extraction_never_writes_outside_the_root(fixture_dir, tmp_path, name):
    root = tmp_path / "root"
    extracted = extract_members(fixture_dir / name, ["ok.txt"], root)
    assert extracted == ["ok.txt"]
    written = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*") if p.is_file() or p.is_symlink())
    assert written == ["root/ok.txt"]
