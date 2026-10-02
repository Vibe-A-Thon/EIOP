import argparse
import logging
from uuid import uuid4

from eoip.contracts.audit import AuditEvent
from eoip.observability import configure_json_logging, log_audit_event
from eoip.runtime import create_store, data_root
from eoip.snapshot import restore

if __name__ == "__main__":
    configure_json_logging()
    logger = logging.getLogger("eoip.restore")
    correlation_id = str(uuid4())
    parser = argparse.ArgumentParser(description="Restore into an empty, isolated EOIP deployment")
    parser.add_argument("source")
    args = parser.parse_args()
    store = create_store()
    try:
        result = restore(store, data_root(), args.source)
        log_audit_event(
            logger,
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="restore",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="success",
                safe_summary=f"Graph restore completed with {result['vertices']} vertices and {result['edges']} edges",
            ),
            operation="restore",
        )
        print(result)
    except Exception as exc:
        log_audit_event(
            logger,
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="restore",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="failure",
                reason_code=type(exc).__name__,
                safe_summary="Graph restore failed",
            ),
            operation="restore",
        )
        raise
    finally:
        store.close()
