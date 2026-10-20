"""Run source-registry CRUD QA against a disposable in-process API."""

from __future__ import annotations

import os
import secrets
import tempfile
import time

from fastapi.testclient import TestClient

from qa.bench import check, exit_code, write_evidence


def run() -> list[dict]:
    source_id = "qa-" + secrets.token_hex(10)
    token = secrets.token_urlsafe(32)
    keys = ("EOIP_DATA_DIR", "EOIP_GRAPH_BACKEND", "EOIP_API_TOKEN", "REVA_ENABLED")
    before = {key: os.environ.get(key) for key in keys}
    results: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="eoip-qa-source-") as root:
        os.environ.update({"EOIP_DATA_DIR": root, "EOIP_GRAPH_BACKEND": "memory", "EOIP_API_TOKEN": token, "REVA_ENABLED": "false"})
        try:
            from apps.api.main import create_app

            with TestClient(create_app()) as client:
                headers = {"Authorization": f"Bearer {token}"}
                payload = {"source_id": source_id, "source_type": "local_files", "name": "QA disposable source"}
                created = False
                deleted = False

                def probe(name: str, method: str, path: str, expected: int, *, body: dict | None = None, predicate=None) -> None:
                    nonlocal created, deleted
                    started = time.perf_counter()
                    response = client.request(method, path, headers=headers, json=body)
                    elapsed = round((time.perf_counter() - started) * 1000, 1)
                    valid = response.status_code == expected and len(response.content) < 1_000_000 and token.encode() not in response.content
                    if valid and predicate:
                        try:
                            valid = bool(predicate(response.json()))
                        except (ValueError, TypeError):
                            valid = False
                    if name == "Create source" and response.status_code == 201:
                        created = True
                    if name == "Delete source" and response.status_code == 204:
                        deleted = True
                    results.append(check(name, valid, f"HTTP {response.status_code}; expected {expected}; {elapsed} ms; {len(response.content)} bytes"))

                try:
                    probe("Create source", "POST", "/api/v1/sources", 201, body=payload, predicate=lambda data: data["source_id"] == source_id)
                    probe("Read source", "GET", f"/api/v1/sources/{source_id}", 200, predicate=lambda data: data["source_id"] == source_id)
                    probe("Reject duplicate", "POST", "/api/v1/sources", 409, body=payload)
                    probe("Rename source", "PATCH", f"/api/v1/sources/{source_id}", 200, body={"name": "QA renamed source"}, predicate=lambda data: data["name"] == "QA renamed source")
                    probe("List source", "GET", "/api/v1/sources", 200, predicate=lambda data: any(item["source_id"] == source_id for item in data))
                    probe("Delete source", "DELETE", f"/api/v1/sources/{source_id}", 204)
                    probe("Deleted source is absent", "GET", f"/api/v1/sources/{source_id}", 404)
                finally:
                    if created and not deleted:
                        try:
                            cleanup = client.delete(f"/api/v1/sources/{source_id}", headers=headers)
                            results.append(check("Failure cleanup", cleanup.status_code in {204, 404}, f"HTTP {cleanup.status_code}"))
                        except Exception as exc:  # noqa: BLE001
                            results.append(check("Failure cleanup", False, f"Cleanup raised {type(exc).__name__}"))
        except Exception as exc:  # noqa: BLE001
            results.append(check("Disposable source workflow", False, f"Workflow raised {type(exc).__name__}"))
        finally:
            for key, value in before.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
    return results


def main() -> int:
    checks = run()
    output = write_evidence("source-workflow", checks, {"disposable_in_memory_api": True, "expected_steps": 7})
    for item in checks:
        print(f"{item['status'].upper():7} {item['name']}: {item['detail']}")
    print(f"Evidence: {output}")
    return exit_code(checks)


if __name__ == "__main__":
    raise SystemExit(main())
