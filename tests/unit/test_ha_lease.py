"""Tests for eoip.ha.LeaderLease (§10 / GAP-HA-001)."""

import time

import pytest

pytestmark = pytest.mark.req("GAP-HA-001")


@pytest.fixture
def lock_path(tmp_path):
    return tmp_path / "worker.lock"


def _lease(path, **kwargs):
    from eoip.ha import LeaderLease

    return LeaderLease(path, **kwargs)


def test_acquire_and_hold(lock_path):
    lease = _lease(lock_path, ttl_seconds=30)
    assert lease.acquire()
    assert lease.held


def test_second_acquire_rejected(lock_path):
    first = _lease(lock_path, ttl_seconds=30)
    second = _lease(lock_path, ttl_seconds=30)
    assert first.acquire()
    assert not second.acquire()
    assert first.held
    assert not second.held


def test_release_allows_takeover(lock_path):
    first = _lease(lock_path, ttl_seconds=30)
    second = _lease(lock_path, ttl_seconds=30)
    first.acquire()
    assert first.release()
    assert not first.held
    assert second.acquire()


def test_release_by_non_owner_fails(lock_path):
    first = _lease(lock_path, ttl_seconds=30)
    second = _lease(lock_path, ttl_seconds=30)
    first.acquire()
    assert not second.release()
    assert first.held


def test_renew_extends_lease(lock_path):
    lease = _lease(lock_path, ttl_seconds=0.5)
    lease.acquire()
    for _ in range(3):
        time.sleep(0.1)
        assert lease.renew()
    assert lease.held
    lease.release()


def test_renew_by_non_owner_fails(lock_path):
    first = _lease(lock_path, ttl_seconds=30)
    second = _lease(lock_path, ttl_seconds=30)
    first.acquire()
    assert not second.renew()


def test_steal_after_expiry(lock_path):
    first = _lease(lock_path, ttl_seconds=0.1)
    second = _lease(lock_path, ttl_seconds=30)
    first.acquire()
    time.sleep(0.15)
    assert second.steal()
    assert second.held
    assert not first.held


def test_steal_refused_before_expiry(lock_path):
    first = _lease(lock_path, ttl_seconds=30)
    second = _lease(lock_path, ttl_seconds=30)
    first.acquire()
    assert not second.steal()
    assert first.held


def test_acquire_takes_expired_lease(lock_path):
    first = _lease(lock_path, ttl_seconds=0.1)
    second = _lease(lock_path, ttl_seconds=30)
    first.acquire()
    time.sleep(0.15)
    assert second.acquire()  # expired lease is fair game
    assert second.held


def test_positive_ttl_required(lock_path):
    with pytest.raises(ValueError):
        _lease(lock_path, ttl_seconds=0)


def test_module_docstring_documents_statelessness():
    import eoip.ha

    assert "stateless" in eoip.ha.__doc__.lower()
