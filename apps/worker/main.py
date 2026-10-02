"""Single durable filesystem worker; interrupted jobs replay idempotently."""

import json
import logging
import os
import signal
import time
from threading import Thread
from uuid import uuid4

import httpx
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.contracts.audit import AuditEvent
from eoip.contracts.source_event import utc_now_iso
from eoip.demo import load_demo
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.jobs import JobQueue, write_json
from eoip.observability import configure_json_logging, log_audit_event
from eoip.runtime import create_store, data_root

logger = logging.getLogger("eoip.worker")
running = True


def main():
    configure_json_logging()
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger.info(
        "worker.started",
        extra={
            "event": "worker.started",
            "operation": "startup",
            "correlation_id": str(uuid4()),
        },
    )

    def stop(*_):
        global running
        running = False

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    store, root = create_store(), data_root()

    def heartbeat():
        while running:
            write_json(root / "state/worker.json", {"status": "running", "timestamp": utc_now_iso()})
            time.sleep(10)

    Thread(target=heartbeat, daemon=True).start()
    queue = JobQueue(root)
    if (
        os.getenv("EOIP_LOAD_DEMO", "true").lower() == "true"
        and not store.get_vertex_by_canonical_id("urn:eoip:code:repo:demo")
        and not any(j["kind"] == "DEMO" and j["status"] in {"PENDING", "RUNNING"} for j in queue.list())
    ):
        queue.submit("DEMO")
    while running:
        for path in sorted(queue.root.glob("*.json")):
            job = json.loads(path.read_text())
            if job["status"] not in {"PENDING", "RUNNING"} or job.get("next_attempt", 0) > time.time():
                continue
            job.setdefault("correlation_id", str(uuid4()))
            job.update(status="RUNNING", started_at=utc_now_iso())
            write_json(path, job)
            try:
                if job["kind"] == "DEMO":
                    result = load_demo(store, root)
                elif job["kind"] == "JIRA_JSON":
                    connector = JiraJsonConnector.from_yaml("config/mappings/jira-mvp.yaml")
                    service = JiraIngestionService(
                        store, connector, FileEventCapture(root / "raw"), root / "dlq"
                    )
                    result = service.ingest(
                        job["payload"]["document"], dry_run=job["payload"].get("dry_run", False)
                    )
                else:
                    raise ValueError("Unknown job kind")
                partial = result.get("run_status") == "PARTIAL" or any(
                    value.get("run_status") == "PARTIAL"
                    for value in result.values()
                    if isinstance(value, dict)
                )
                job.update(
                    status="PARTIAL" if partial else "SUCCEEDED", result=result, finished_at=utc_now_iso()
                )
            except (httpx.HTTPError, OSError) as exc:
                attempts = job.get("attempts", 0) + 1
                job.update(
                    status="PENDING" if attempts < 3 else "FAILED",
                    attempts=attempts,
                    next_attempt=time.time() + 2**attempts,
                    error=type(exc).__name__,
                )
                logger.error(
                    "job.retry_scheduled",
                    extra={
                        "event": "job.retry_scheduled",
                        "operation": job["kind"].lower(),
                        "correlation_id": job["correlation_id"],
                        "job_id": job["job_id"],
                        "attempt": attempts,
                        "error_type": type(exc).__name__,
                    },
                )
            except Exception as exc:  # noqa: BLE001 - persist unexpected job failures and keep the worker alive
                logger.error(
                    "job.failed",
                    extra={
                        "event": "job.failed",
                        "operation": job["kind"].lower(),
                        "correlation_id": job["correlation_id"],
                        "job_id": job["job_id"],
                        "error_type": type(exc).__name__,
                    },
                )
                job.update(status="FAILED", error=type(exc).__name__, finished_at=utc_now_iso())
            write_json(path, job)
            audit = AuditEvent(
                audit_id=str(uuid4()),
                event_type="ingestion",
                actor="worker",
                correlation_id=job["correlation_id"],
                outcome="success" if job["status"] == "SUCCEEDED" else job["status"].lower(),
                reason_code=job.get("error"),
                safe_summary=f"{job['kind']} job completed with status {job['status']}",
            )
            log_audit_event(logger, audit, operation="ingestion", job_id=job["job_id"])
            logger.info(
                "job.completed",
                extra={
                    "event": "job.completed",
                    "operation": job["kind"].lower(),
                    "correlation_id": job["correlation_id"],
                    "job_id": job["job_id"],
                    "status_code": job["status"],
                },
            )
        time.sleep(2)
    store.close()
    logger.info(
        "worker.stopped",
        extra={
            "event": "worker.stopped",
            "operation": "shutdown",
            "correlation_id": str(uuid4()),
        },
    )


if __name__ == "__main__":
    main()
