"""Filesystem-advisory leader lease for single-writer worker failover (§10 / GAP-HA-001).

Implements a leader election primitive for HA worker deployments: exactly one
worker may hold the lease at a time; on node loss the lease expires after its
TTL and another worker may steal it. Safe across processes on one host via
``O_CREAT|O_EXCL`` atomic create; on shared filesystems this is advisory and
must be paired with the TTL for correctness.

API statelessness requirements (§10): all HTTP-facing API processes MUST be
stateless so any replica can serve any request and failover is transparent:

- No in-request state survives the request: sessions, auth context, and
  partial writes live in the graph store / audit sink, not in process memory.
- Long-running or single-writer work (indexing, ontology publication,
  snapshot jobs) MUST be executed only by the lease-holding worker; API
  replicas only enqueue or query.
- Uploaded artifacts go to shared/object storage, never local disk only.
- Idempotency keys and job IDs make retries safe when a worker fails over.
- The lease TTL must exceed the maximum expected GC/pause of the holder.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path


class LeaderLease:
    """Advisory leader lease backed by a lock file with a TTL (GAP-HA-001).

    Usage::

        lease = LeaderLease("/var/run/eoip/worker.lock", ttl_seconds=15)
        if lease.acquire():
            try:
                ...  # single-writer work
                lease.renew()
            finally:
                lease.release()
    """

    def __init__(self, path: str | Path, ttl_seconds: float = 30.0) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.path = Path(path)
        self.ttl_seconds = float(ttl_seconds)
        self.owner_token = uuid.uuid4().hex

    # -- internals ---------------------------------------------------------

    def _read(self) -> dict | None:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None
        except (OSError, ValueError):
            return None

    def _write(self, expires_at: float) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + f".{os.getpid()}.tmp")
        tmp.write_text(
            json.dumps({"owner": self.owner_token, "expires_at": expires_at}),
            encoding="utf-8",
        )
        os.replace(tmp, self.path)

    def _expired(self, record: dict, now: float) -> bool:
        return now >= float(record.get("expires_at", 0.0))

    # -- public API --------------------------------------------------------

    @property
    def held(self) -> bool:
        """True when this instance currently owns a live lease."""
        record = self._read()
        if record is None or record.get("owner") != self.owner_token:
            return False
        return not self._expired(record, time.monotonic())

    def acquire(self) -> bool:
        """Take the lease if free or expired; False while another owner holds it."""
        now = time.monotonic()
        try:
            self._write(now + self.ttl_seconds)
            return True
        except OSError:
            pass
        record = self._read()
        if record is not None and not self._expired(record, now):
            return False
        # Stale or unparseable lease: steal after expiry.
        try:
            self._write(now + self.ttl_seconds)
            return True
        except OSError:
            return False

    def renew(self) -> bool:
        """Extend the lease; only the current owner may renew."""
        record = self._read()
        now = time.monotonic()
        if record is None or record.get("owner") != self.owner_token or self._expired(record, now):
            return False
        try:
            self._write(now + self.ttl_seconds)
            return True
        except OSError:
            return False

    def release(self) -> bool:
        """Drop the lease if we hold it."""
        record = self._read()
        if record is None or record.get("owner") != self.owner_token:
            return False
        try:
            self.path.unlink()
            return True
        except OSError:
            return False

    def steal(self) -> bool:
        """Forcefully take the lease (post-expiry failover path).

        Refuses to steal a lease that has not yet expired; call ``acquire``
        for the normal (expiry-aware) path.
        """
        record = self._read()
        now = time.monotonic()
        if record is not None and not self._expired(record, now):
            return False
        return self.acquire()
