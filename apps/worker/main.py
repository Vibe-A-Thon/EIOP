"""Single durable filesystem worker; interrupted jobs replay idempotently."""

import json
import logging
import os
import signal
import time
from pathlib import Path
from threading import Thread
from uuid import uuid4

import httpx
from eoip.audit.sink import AuditSink
from eoip.connectors.errors import ConnectorError
from eoip.connectors.gitlab_json import GitLabJsonConnector
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.connectors.registry import SourceRegistry
from eoip.contracts.audit import AuditEvent
from eoip.contracts.source_event import utc_now_iso
from eoip.demo import load_demo
from eoip.graph.consumers import run_default_consumers
from eoip.ingestion.github import GitHubIngestionService, run_registered_github_operation
from eoip.ingestion.gitlab import GitLabIngestionService
from eoip.ingestion.gitlab_rest import GitLabTemporalIngestionService, run_registered_gitlab_operation
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.ingestion.jira_rest import JiraTemporalIngestionService, run_registered_jira_operation
from eoip.ingestion.replay import replay_captured_events
from eoip.ingestion.source_sync import run_configured_source_sync, run_registered_source_operation
from eoip.jobs import JobQueue, write_json
from eoip.observability import configure_json_logging
from eoip.runtime import create_store, data_root

logger = logging.getLogger("eoip.worker")
running = True


def execute_job(store, root, job):
    """Execute one durable job using the same services as the synchronous test surface."""
    payload = job.get("payload") or {}
    if job["kind"] == "DEMO":
        return load_demo(store, root)
    if job["kind"] == "JIRA_JSON":
        connector = JiraJsonConnector.from_yaml("config/mappings/jira-mvp.yaml")
        service = JiraIngestionService(
            store, connector, FileEventCapture(root / "raw"), root / "dlq"
        )
        return service.ingest(payload["document"], dry_run=payload.get("dry_run", False))
    if job["kind"] == "GITLAB_JSON":
        service = GitLabIngestionService(
            store,
            payload.get("repository_id", "demo"),
            GitLabJsonConnector(),
            FileEventCapture(root / "raw"),
            root / "dlq",
        )
        return service.ingest(payload["document"], dry_run=payload.get("dry_run", False))
    if job["kind"] == "REPLAY":
        return replay_captured_events(
            store,
            root,
            source_system=payload["source_system"],
            event_ids=payload.get("event_ids"),
            dry_run=payload.get("dry_run", False),
            repository_id=payload.get("repository_id", "demo"),
        )
    if job["kind"] in {"CONFLUENCE", "SERVICENOW"}:
        return run_configured_source_sync(
            job["kind"].lower(),
            payload,
            store,
            str(root),
            job["correlation_id"],
        )
    if job["kind"] == "SOURCE_OPERATION":
        registry = SourceRegistry(root / "state" / "source-registry.json")
        entry = registry.get(payload["source_id"])
        if entry.source_type == "documents":
            from eoip.ingestion.files import run_registered_file_operation

            return run_registered_file_operation(
                entry, payload, store, str(root), job["correlation_id"]
            )
        if entry.source_type == "github":
            return run_registered_github_operation(
                entry, payload, store, str(root), job["correlation_id"]
            )
        if entry.source_type == "gitlab":
            return run_registered_gitlab_operation(
                entry, payload, store, str(root), job["correlation_id"]
            )
        if entry.source_type == "jira":
            return run_registered_jira_operation(
                entry, payload, store, str(root), job["correlation_id"]
            )
        return run_registered_source_operation(
            entry,
            payload,
            store,
            str(root),
            job["correlation_id"],
        )
    if job["kind"] == "SOURCE_WEBHOOK":
        registry = SourceRegistry(root / "state" / "source-registry.json")
        entry = registry.get(payload["source_id"])
        receipt_path = root / "receipts" / entry.source_id
        candidate = Path(payload["receipt_ref"]).resolve()
        if receipt_path.resolve() not in candidate.parents:
            raise ValueError("webhook receipt path escapes source receipt directory")
        receipt = json.loads(candidate.read_text(encoding="utf-8"))
        document = receipt["payload"]
        if entry.source_type == "jira":
            from eoip.connectors.config import connector_from_registry
            from eoip.connectors.jira import JiraConnector

            connector = connector_from_registry(entry, correlation_id=job["correlation_id"])
            if not isinstance(connector, JiraConnector):
                raise TypeError("registered Jira source did not create a Jira connector")
            try:
                service = JiraTemporalIngestionService(
                    store, connector, FileEventCapture(root / "raw"), root / "dlq"
                )
                return service.ingest(list(connector.handle_event(document)))
            finally:
                connector.close()
        if entry.source_type == "gitlab":
            from eoip.connectors.config import connector_from_registry
            from eoip.connectors.gitlab import GitLabConnector

            connector = connector_from_registry(entry, correlation_id=job["correlation_id"])
            if not isinstance(connector, GitLabConnector):
                raise TypeError("registered GitLab source did not create a GitLab connector")
            try:
                document["_event_name"] = receipt.get("metadata", {}).get("event_name")
                service = GitLabTemporalIngestionService(
                    store, connector, FileEventCapture(root / "raw"), root / "dlq"
                )
                return service.ingest(list(connector.handle_event(document)))
            finally:
                connector.close()
        if entry.source_type == "github":
            from eoip.connectors.config import connector_from_registry
            from eoip.connectors.github import GitHubConnector

            connector = connector_from_registry(entry, correlation_id=job["correlation_id"])
            if not isinstance(connector, GitHubConnector):
                raise TypeError("registered GitHub source did not create a GitHub connector")
            try:
                document["_event_name"] = receipt.get("metadata", {}).get("event_name")
                service = GitHubIngestionService(
                    store, connector, FileEventCapture(root / "raw"), root / "dlq"
                )
                return service.ingest(list(connector.handle_event(document)))
            finally:
                connector.close()
        raise ValueError("No webhook mapper is available for this source type")
    raise ValueError("Unknown job kind")


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
    audit_sink = AuditSink(root / "audit")

    def heartbeat():
        while running:
            write_json(root / "state/worker.json", {"status": "running", "timestamp": utc_now_iso()})
            time.sleep(10)

    Thread(target=heartbeat, daemon=True).start()
    queue = JobQueue(root)

    # Optional single-writer leader lease for multi-replica worker HA
    # (G2-DEPLOY-HA). Advisory filesystem lease: only the holder processes
    # jobs; others idle until the lease expires or is released.
    lease = None
    lease_path = os.getenv("EOIP_LEASE_PATH")
    if lease_path:
        from eoip.ha import LeaderLease

        lease = LeaderLease(
            lease_path,
            ttl_seconds=float(os.getenv("EOIP_LEASE_TTL_SECONDS", "30")),
        )
        if not lease.acquire():
            logger.warning(
                "worker.lease_contended",
                extra={
                    "event": "worker.lease_contended",
                    "operation": "startup",
                    "correlation_id": str(uuid4()),
                    "lease_path": lease_path,
                },
            )

    def ensure_leader():
        if lease is None:
            return True
        if lease.held:
            return lease.renew()
        return lease.acquire()

    if (
        os.getenv("EOIP_LOAD_DEMO", "true").lower() == "true"
        and ensure_leader()
        and not store.get_vertex_by_canonical_id("urn:eoip:code:repo:demo")
        and not any(j["kind"] == "DEMO" and j["status"] in {"PENDING", "RUNNING"} for j in queue.list())
    ):
        queue.submit("DEMO")
    while running:
        if not ensure_leader():
            time.sleep(2)
            continue
        for path in sorted(queue.root.glob("*.json")):
            job = json.loads(path.read_text())
            if job["status"] not in {"PENDING", "RUNNING"} or job.get("next_attempt", 0) > time.time():
                continue
            job.setdefault("correlation_id", str(uuid4()))
            job.update(status="RUNNING", started_at=utc_now_iso())
            write_json(path, job)
            try:
                result = execute_job(store, root, job)
                result["semantic_consumers"] = run_default_consumers(store, root)
                partial = result.get("run_status") == "PARTIAL" or any(
                    value.get("run_status") == "PARTIAL"
                    for value in result.values()
                    if isinstance(value, dict)
                )
                job.update(
                    status="PARTIAL" if partial else "SUCCEEDED", result=result, finished_at=utc_now_iso()
                )
            except ConnectorError as exc:
                attempts = job.get("attempts", 0) + 1
                retryable = exc.category in {
                    "timeout",
                    "transport_error",
                    "rate_limited",
                    "remote_error",
                }
                retry = retryable and attempts < 3
                job.update(
                    status="PENDING" if retry else "FAILED",
                    attempts=attempts,
                    next_attempt=time.time() + 2**attempts,
                    error=exc.category,
                    finished_at=None if retry else utc_now_iso(),
                )
                logger.error(
                    "job.connector_failed",
                    extra={
                        "event": "job.connector_failed",
                        "operation": job["kind"].lower(),
                        "correlation_id": exc.correlation_id,
                        "job_id": job["job_id"],
                        "source_system": exc.source_system,
                        "error_category": exc.category,
                        "attempt": attempts,
                    },
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
            audit_sink.emit(audit, operation="ingestion", job_id=job["job_id"])
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
    if lease is not None:
        lease.release()
    close = getattr(store, "close", None)
    if callable(close):
        close()
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
