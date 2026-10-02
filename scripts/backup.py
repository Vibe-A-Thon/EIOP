import argparse
import logging
from datetime import UTC, datetime
from uuid import uuid4

from eoip.contracts.audit import AuditEvent
from eoip.observability import configure_json_logging, log_audit_event
from eoip.runtime import create_store, data_root
from eoip.snapshot import backup

if __name__ == "__main__":
    configure_json_logging()
    logger = logging.getLogger("eoip.backup")
    correlation_id = str(uuid4())
    parser = argparse.ArgumentParser(description="Export a quiescent EOIP graph and raw evidence")
    parser.add_argument("--output")
    args = parser.parse_args()
    destination = args.output or str(
        data_root() / "backups" / f"eoip-{datetime.now(UTC):%Y%m%dT%H%M%SZ}.json"
    )
    store = create_store()
    try:
        result = backup(store, data_root(), destination)
        log_audit_event(
            logger,
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
        log_audit_event(
            logger,
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
