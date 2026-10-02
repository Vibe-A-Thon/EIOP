"""Single durable filesystem worker; interrupted jobs replay idempotently."""

import json
import logging
import os
import signal
import time
from threading import Thread

import httpx
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.contracts.source_event import utc_now_iso
from eoip.demo import load_demo
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.jobs import JobQueue, write_json
from eoip.runtime import create_store, data_root

logger = logging.getLogger("eoip.worker")
running = True


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)

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
                logger.error("job=%s retry=%s type=%s", job["job_id"], attempts, type(exc).__name__)
            except Exception as exc:  # noqa: BLE001 - persist unexpected job failures and keep the worker alive
                logger.error("job=%s failed type=%s", job["job_id"], type(exc).__name__)
                job.update(status="FAILED", error=type(exc).__name__, finished_at=utc_now_iso())
            write_json(path, job)
            logger.info("job=%s status=%s", job["job_id"], job["status"])
        time.sleep(2)
    store.close()


if __name__ == "__main__":
    main()
