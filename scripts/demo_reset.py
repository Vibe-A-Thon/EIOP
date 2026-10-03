"""Reset and reload the demo environment.

Usage: python -m scripts.demo_reset --confirm [--data-dir /data]
Clears the graph, re-bootstraps schema and meta-graph, then loads demo fixtures.
Only for backends that permit deletion; HugeGraph requires a disposable deployment.
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


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="Reset demo environment")
    parser.add_argument("--data-dir", type=Path, default=None)
    parser.add_argument("--confirm", action="store_true", help="Confirm deletion of demo graph and evidence")
    args = parser.parse_args(argv)
    if not args.confirm:
        parser.error("--confirm is required; reset deletes graph, raw evidence, DLQ and state")
    data = args.data_dir or data_root()

    print(f"[demo_reset] data_dir={data}")
    audit = AuditSink(data / "audit")
    correlation_id = str(uuid4())

    store = create_store()
    try:
        audit.emit(
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="demo_reset_intent",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="authorized",
                safe_summary="Confirmed demo reset accepted for execution",
            ),
        )
        store.clear()
        print("[demo_reset] graph cleared")
        for subdir in ["raw", "dlq", "state"]:
            d = data / subdir
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True, exist_ok=True)

        store.ensure_schema({})
        result = load_demo(store, str(data))
        print(f"[demo_reset] demo loaded: {json.dumps(result, indent=2)}")
        audit.emit(
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="demo_reset",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="success",
                safe_summary=f"Demo reset: {result['jira']['records_accepted']} Jira + {result['git']['files']} files",
            ),
        )
    except Exception as exc:
        audit.emit(
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="demo_reset",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="failure",
                reason_code=type(exc).__name__,
                safe_summary="Demo reset failed; inspect the operation error before retrying",
            ),
        )
        raise
    finally:
        store.close()
    print("[demo_reset] complete")


if __name__ == "__main__":
    main()
