import argparse
from datetime import UTC, datetime
from uuid import uuid4

from eoip.audit.sink import AuditSink
from eoip.contracts.audit import AuditEvent
from eoip.observability import configure_json_logging
from eoip.runtime import create_store, data_root
from eoip.snapshot import backup

if __name__ == "__main__":
    configure_json_logging()
    correlation_id = str(uuid4())
    parser = argparse.ArgumentParser(description="Export a quiescent EOIP graph and raw evidence")
    parser.add_argument("--output")
    args = parser.parse_args()
    destination = args.output or str(
        data_root() / "backups" / f"eoip-{datetime.now(UTC):%Y%m%dT%H%M%SZ}.json"
    )
    audit_sink = AuditSink(data_root() / "audit")
    store = create_store()
    try:
        audit_sink.emit(
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="backup_intent",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="authorized",
                safe_summary="Backup operation accepted for execution",
            ),
            operation="backup",
        )
        result = backup(store, data_root(), destination)
        audit_sink.emit(
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="backup",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="success",
                safe_summary=f"Graph backup created with {result['vertices']} vertices and {result['edges']} edges",
            ),
            operation="backup",
        )
        print(result)
    except Exception as exc:
        audit_sink.emit(
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="backup",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="failure",
                reason_code=type(exc).__name__,
                safe_summary="Graph backup failed",
            ),
            operation="backup",
        )
        raise
    finally:
        store.close()
