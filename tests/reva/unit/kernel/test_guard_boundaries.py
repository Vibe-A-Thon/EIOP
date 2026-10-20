"""Boundary tests for kernel guards (valid-time split, inclusion verification, member paths, gap patch)."""

from __future__ import annotations

import pytest

from reva.core.errors import RevaValidationError
from reva.extract.artifacts.inventory import MAX_PATH_LENGTH, validate_member_path
from reva.kernel.contradictions import _valid_times_overlap
from reva.kernel.gaps import open_gap, update_gap
from reva.kernel.store import RevaStore
from reva.kernel.translog import leaf_hash, node_hash, verify_inclusion

pytestmark = pytest.mark.reva_depth("unit")
A, B, C = "2026-01-01T00:00:00.000Z", "2026-02-01T00:00:00.000Z", "2026-03-01T00:00:00.000Z"


@pytest.mark.parametrize("a,b,overlap", [
    ({"from": A, "to": B}, {"from": B, "to": C}, False),  # touching half-open intervals
    ({"from": B, "to": C}, {"from": A, "to": B}, False),
    ({"from": A, "to": C}, {"from": B, "to": None}, True),
    ({"from": A}, {"from": B}, True),
    ({"from": A, "to": B}, {"from": C}, False),
    ({"from": C}, {"from": A, "to": B}, False),
    (None, {"from": A}, True),
    ({"from": A}, None, True),
    ({"from": ""}, {"from": A, "to": B}, True),
    ({"from": A, "to": B}, {"from": ""}, True),
])
def test_valid_time_overlap(a, b, overlap):
    assert _valid_times_overlap(a, b) is overlap


def test_inclusion_verification_rejects_bad_inputs():
    l0, l1 = leaf_hash(b"a"), leaf_hash(b"b")
    root2 = node_hash(l0, l1)
    assert verify_inclusion(l0, 0, 2, [l1], root2)
    assert verify_inclusion(l1, 1, 2, [l0], root2)
    assert not verify_inclusion(l0, 0, 0, [], root2)
    assert not verify_inclusion(l0, -1, 2, [l1], root2)
    assert not verify_inclusion(l0, 2, 2, [l1], root2)
    assert not verify_inclusion(l0, 0, 2, [], root2)
    assert not verify_inclusion(l0, 0, 2, [l1, l1], root2)
    assert not verify_inclusion(l0, 0, 2, [l0], root2)
    assert verify_inclusion(l0, 0, 1, [], l0)
    assert not verify_inclusion(l0, 0, 1, [], l1)
    assert not verify_inclusion(l0, 0, 1, [l1], l0)


def test_member_path_length_limit_is_inclusive():
    assert validate_member_path("a" * MAX_PATH_LENGTH) == "a" * MAX_PATH_LENGTH
    with pytest.raises(RevaValidationError):
        validate_member_path("a" * (MAX_PATH_LENGTH + 1))


def test_gap_patch_without_status_only_changes_fields():
    store = RevaStore(":memory:")
    gap = open_gap(store, "t1", "d", "q", "s")
    updated = update_gap(store, "t1", gap.gap_id, 1, {"owner": "team-a"})
    assert updated["status"] == "open" and updated["owner"] == "team-a" and updated["revision"] == 2
    again = update_gap(store, "t1", gap.gap_id, 2, {"status": None, "severity": "high"})
    assert again["status"] == "open" and again["severity"] == "high"
