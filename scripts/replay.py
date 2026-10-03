"""Replay captured raw SourceEvents through the durable job queue (FR-CONN-006).

Usage:
    python -m scripts.replay --source jira [--event-id HEX ...] [--dry-run]
    python -m scripts.replay --source gitlab

Submits a RAW_REPLAY job to the local worker queue and prints the submitted
job id. The replay is idempotent: capture deduplicates by event id + payload
hash and graph upserts are keyed by canonical identity.
"""

from __future__ import annotations

import argparse
import json
import sys
from uuid import uuid4

from eoip.jobs import JobQueue
from eoip.runtime import data_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, choices=sorted({"jira", "gitlab", "git"}))
    parser.add_argument("--event-id", action="append", dest="event_ids", default=None)
    parser.add_argument("--repository-id", default="demo")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    queue = JobQueue(data_root())
    job = queue.submit(
        "REPLAY",
        {
            "source_system": args.source,
            "event_ids": args.event_ids,
            "repository_id": args.repository_id,
            "dry_run": args.dry_run,
        },
        correlation_id=str(uuid4()),
    )
    print(json.dumps(job, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
