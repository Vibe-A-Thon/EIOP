"""Replay captured Jira/GitLab SourceEvents and optionally verify a golden graph.

Examples:
    python -m scripts.replay jira --event-id <sha256>
    python -m scripts.replay gitlab --repository-id platform --write-golden replay-golden.json
    python -m scripts.replay jira --golden replay-golden.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eoip.ingestion.replay import (
    logical_graph_output,
    logical_output_diff,
    replay_captured_events,
)
from eoip.runtime import create_store, data_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_system", choices=["jira", "gitlab", "git"])
    parser.add_argument(
        "--event-id",
        action="append",
        dest="event_ids",
        help="Captured SHA-256 event ID; repeat to replay multiple events.",
    )
    parser.add_argument("--repository-id", default="demo", help="GitLab repository identity.")
    parser.add_argument("--dry-run", action="store_true", help="Map events without graph mutation.")
    golden = parser.add_mutually_exclusive_group()
    golden.add_argument("--golden", help="Compare post-replay logical output to this JSON file.")
    golden.add_argument("--write-golden", help="Write post-replay logical output to this JSON file.")
    args = parser.parse_args(argv)

    store = create_store()
    try:
        result = replay_captured_events(
            store,
            data_root(),
            source_system=args.source_system,
            event_ids=args.event_ids,
            dry_run=args.dry_run,
            repository_id=args.repository_id,
        )
        output = logical_graph_output(store)
        if args.write_golden:
            destination = Path(args.write_golden)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            result["golden_written"] = str(destination.resolve())
        if args.golden:
            expected = json.loads(Path(args.golden).read_text(encoding="utf-8"))
            result["golden_diff"] = logical_output_diff(expected, output)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("golden_diff", {"equivalent": True})["equivalent"] else 1
    finally:
        store.close()


if __name__ == "__main__":
    sys.exit(main())
