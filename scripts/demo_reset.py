"""Reset and reload the demo environment.

Usage: python -m scripts.demo_reset [--data-dir /data]
Clears the graph, re-bootstraps schema and meta-graph, then loads demo fixtures.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "packages"))

from eoip.audit.sink import AuditSink
from eoip.contracts.audit import AuditEvent
from eoip.demo import load_demo
from eoip.runtime import create_store, data_root


def main():
    parser = argparse.ArgumentParser(description="Reset demo environment")
    parser.add_argument("--data-dir", type=Path, default=None)
    args = parser.parse_args()
    data = args.data_dir or data_root()

    print(f"[demo_reset] data_dir={data}")
    audit = AuditSink(data / "audit")
    correlation_id = str(uuid4())

    for subdir in ["raw", "dlq", "state", "audit"]:
        d = data / subdir
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

    store = create_store()
    try:
        store.clear()
        print("[demo_reset] graph cleared")
    except RuntimeError:
        print("[demo_reset] graph clear not supported by backend; continuing with upsert")

    store.ensure_schema({})
    print("[demo_reset] schema bootstrapped")

    result = load_demo(store, str(data))
    print(f"[demo_reset] demo loaded: {json.dumps(result, indent=2)}")

    audit.emit(
        AuditEvent(
            audit_id=str(uuid4()),
            event_type="demo_reset",
            actor="admin",
            correlation_id=correlation_id,
            outcome="success",
            safe_summary=f"Demo reset: {result['jira']['records_accepted']} Jira + {result['git']['files']} files",
        ),
    )
    print("[demo_reset] complete")


if __name__ == "__main__":
    main()
