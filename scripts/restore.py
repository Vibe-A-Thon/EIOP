import argparse
from pathlib import Path
from uuid import uuid4
from zipfile import is_zipfile

from eoip.audit.sink import AuditSink
from eoip.contracts.audit import AuditEvent
from eoip.observability import configure_json_logging
from eoip.recovery_bundle import MAX_BYTES, restore_bundle
from eoip.runtime import create_store, data_root
from eoip.snapshot import restore

if __name__ == "__main__":
    configure_json_logging()
    correlation_id = str(uuid4())
    parser = argparse.ArgumentParser(description="Restore into an empty, isolated EOIP deployment")
    parser.add_argument("source")
    parser.add_argument("--config-dir", help="Empty configuration target for a recovery bundle")
    parser.add_argument("--model-dir", help="Empty Ollama models target for a recovery bundle")
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    args = parser.parse_args()
    bundle = Path(args.source).suffix.lower() == ".zip" or is_zipfile(args.source)
    if bundle and (not args.config_dir or not args.model_dir):
        parser.error("Bundle restore requires explicit --config-dir and --model-dir empty targets")
    audit_sink = AuditSink(data_root() / "audit")
    store = create_store()
    try:
        audit_sink.emit(
            AuditEvent(
                audit_id=str(uuid4()),
                event_type="restore_intent",
                actor="local-operator",
                correlation_id=correlation_id,
                outcome="authorized",
                safe_summary="Restore operation accepted for execution",
            ),
            operation="restore",
        )
        result = (
            restore_bundle(
                store, data_root(), args.source, config_dir=args.config_dir,
                model_dir=args.model_dir, max_bytes=args.max_bytes,
            ) if bundle else restore(store, data_root(), args.source)
        )
        audit_sink.emit(
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
        audit_sink.emit(
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
