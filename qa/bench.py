"""Read-only, evidence-producing non-functional QA bench."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from qa.postman.build_api_catalog import OUTPUT as API_CATALOG_PATH
from qa.postman.build_api_catalog import collection as api_catalog_collection
from qa.postman.build_collection import COLLECTION_PATH, ENVIRONMENT_PATH, collection, environment
from qa.postman.build_workflow import WORKFLOW_PATH
from qa.postman.build_workflow import collection as workflow_collection

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "qa" / "contracts" / "api-surface.json"
RESULT_ROOT = ROOT / "test-results" / "qa-bench"
TOKEN_ENV = ("QA_TOKEN", "EOIP_API_TOKEN")


def validated_base_url(value: str, allow_remote: bool = False) -> str:
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("A full HTTP(S) base URL is required")
    if parsed.username or parsed.password or parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise ValueError("Base URL cannot contain credentials, path, query, or fragment")
    if not allow_remote and (parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}):
        raise ValueError("Remote targets require --allow-remote")
    return value.rstrip("/")


def api_surface(document: dict) -> dict:
    if not isinstance(document.get("paths"), dict):
        raise TypeError("OpenAPI paths are missing")
    methods = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
    return {
        "schema_version": 1,
        "openapi": document.get("openapi"),
        "operations": [
            {"method": method.upper(), "path": path}
            for path, item in sorted(document["paths"].items())
            for method in sorted(item)
            if method in methods
        ],
    }


def offline_document() -> dict:
    # Build the application against a disposable store, never the user's configured data directory.
    with tempfile.TemporaryDirectory(prefix="eoip-qa-openapi-") as data_dir:
        old = {key: os.environ.get(key) for key in ("EOIP_GRAPH_BACKEND", "EOIP_DATA_DIR", "REVA_ENABLED", "EOIP_API_TOKEN", "EOIP_ASG_FILE")}
        os.environ.update({
            "EOIP_GRAPH_BACKEND": "memory",
            "EOIP_DATA_DIR": data_dir,
            "REVA_ENABLED": "false",
            "EOIP_API_TOKEN": "qa-disposable-token-for-contract-scan",
        })
        from qa._principal import provision

        os.environ.update(provision(data_dir, os.environ["EOIP_API_TOKEN"]))
        try:
            from apps.api.main import create_app
            return create_app().openapi()
        finally:
            for key, value in old.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_provenance() -> dict:
    try:
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=5, check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, timeout=10, check=True).stdout)
        return {"revision": revision, "worktree_dirty": dirty}
    except (OSError, subprocess.SubprocessError):
        return {"revision": None, "worktree_dirty": None}


def write_evidence(kind: str, checks: list[dict], metadata: dict, root: Path = RESULT_ROOT) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = root / f"{stamp}-{os.urandom(3).hex()}" / "summary.json"
    path.parent.mkdir(parents=True, exist_ok=False)
    status = "fail" if any(c["status"] == "fail" for c in checks) else (
        "blocked" if any(c["status"] == "blocked" for c in checks) else "pass"
    )
    payload = {
        "schema_version": 1,
        "suite": kind,
        "created_utc": datetime.now(UTC).isoformat(),
        "status": status,
        "checks": checks,
        "metadata": metadata,
        "repository": git_provenance(),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def exit_code(checks: list[dict]) -> int:
    if any(c["status"] == "fail" for c in checks):
        return 1
    if any(c["status"] == "blocked" for c in checks):
        return 2
    return 0


def check(name: str, ok: bool | None, detail: str) -> dict:
    return {"name": name, "status": "blocked" if ok is None else ("pass" if ok else "fail"), "detail": detail}


def offline_checks() -> list[dict]:
    document = offline_document()
    current = api_surface(document)
    checks = []
    if BASELINE.exists():
        pinned = json.loads(BASELINE.read_text(encoding="utf-8"))
        current_set = {(v["method"], v["path"]) for v in current["operations"]}
        pinned_set = {(v["method"], v["path"]) for v in pinned["operations"]}
        added, removed = sorted(current_set - pinned_set), sorted(pinned_set - current_set)
        checks.append(check("OpenAPI operation drift", not (added or removed), f"{len(current_set)} operations; added={added[:12]}; removed={removed[:12]}"))
    else:
        checks.append(check("OpenAPI operation drift", None, "Pinned baseline absent; run baseline --write and review the diff"))
    # FastAPI serves /openapi.json, but deliberately omits it from its own schema.
    expected = {("GET", path) for path in ("/health/ready", "/metrics", "/api/v1/auth/whoami", "/api/v1/admin/stats", "/api/v1/admin/system", "/api/v1/graph/backends", "/api/v1/query/templates", "/api/v1/reports/templates", "/api/v1/product/capabilities")}
    actual = {(v["method"], v["path"]) for v in current["operations"]}
    checks.append(check("QA probe endpoints", expected <= actual, f"{len(expected & actual)}/{len(expected)} expected operations available"))
    generated = collection()
    items = [item for group in generated["item"] for item in group["item"]]
    checks.append(check("Postman GET-only", bool(items) and all(item["request"]["method"] == "GET" for item in items), f"{len(items)} requests"))
    for path, expected_json in ((COLLECTION_PATH, generated), (ENVIRONMENT_PATH, environment())):
        actual_json = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        checks.append(check(f"Generated {path.name}", actual_json == expected_json, "Regenerate with python -m qa.postman.build_collection"))
    checks.append(check("No embedded Postman token", all(v["value"] == "" for v in generated["variable"] if v["key"] == "qaToken"), "Token comes from runtime environment"))
    workflow = workflow_collection()
    workflow_items = workflow["item"]
    checks.append(check("Disposable workflow artifact", WORKFLOW_PATH.exists() and json.loads(WORKFLOW_PATH.read_text(encoding="utf-8")) == workflow, "Regenerate with python -m qa.postman.build_workflow"))
    checks.append(check("Workflow operation allowlist", all(item["request"]["url"]["raw"].startswith("{{baseUrl}}/api/v1/sources") and item["request"]["method"] in {"GET", "POST", "PATCH", "DELETE"} for item in workflow_items), f"{len(workflow_items)} source-registry steps"))
    checks.append(check("Workflow locked by default", any(v["key"] == "qaDisposableTarget" and v["value"] == "false" for v in workflow["variable"]), "Bench-owned disposable runtime required"))
    catalog = api_catalog_collection(document)
    catalog_items = [item for group in catalog["item"] for item in group["item"]]
    checks.append(check("Complete API request blueprint", len(catalog_items) == len(current["operations"]), f"{len(catalog_items)} blueprints for {len(current['operations'])} operations"))
    checks.append(check("Catalog execution disabled", any("pm.execution.skipRequest();" in line for event in catalog["event"] for line in event["script"]["exec"]), "Collection-level hard stop required"))
    artifact = json.loads(API_CATALOG_PATH.read_text(encoding="utf-8")) if API_CATALOG_PATH.exists() else None
    checks.append(check("Generated complete API catalog", artifact == catalog, "Regenerate with python -m qa.postman.build_api_catalog"))
    return checks


def live_checks(base_url: str, token: str | None, timeout: float) -> list[dict]:
    probes = [
        ("Readiness", "/health/ready", None, 200),
        ("OpenAPI", "/openapi.json", None, 200),
        ("Metrics", "/metrics", None, 200),
        ("Whoami denied", "/api/v1/auth/whoami", None, 401),
        ("Invalid token denied", "/api/v1/auth/whoami", "invalid-qa-token", 401),
        ("Basic auth denied", "/api/v1/auth/whoami", "basic:Zm9vOmJhcg==", 401),
        ("Admin stats denied", "/api/v1/admin/stats", None, 401),
        ("Admin system denied", "/api/v1/admin/system", None, 401),
        ("Graph backends denied", "/api/v1/graph/backends", None, 401),
        ("Whoami authorized", "/api/v1/auth/whoami", token, 200),
        ("Admin stats authorized", "/api/v1/admin/stats", token, 200),
        ("System authorized", "/api/v1/admin/system", token, 200),
        ("Graph backends authorized", "/api/v1/graph/backends", token, 200),
        ("Query templates authorized", "/api/v1/query/templates", token, 200),
        ("Report templates authorized", "/api/v1/reports/templates", token, 200),
        ("Product capabilities authorized", "/api/v1/product/capabilities", token, 200),
        ("Unknown path authorized", "/api/v1/qa-nonexistent-route", token, 404),
    ]
    results = []
    with httpx.Client(timeout=timeout, follow_redirects=False, trust_env=False) as client:
        for name, path, credential, expected in probes:
            if credential is None and name.endswith("authorized"):
                results.append(check(name, None, "QA_TOKEN or EOIP_API_TOKEN is required"))
                continue
            headers = {"Accept": "application/json"}
            if credential:
                headers["Authorization"] = "Basic Zm9vOmJhcg==" if credential.startswith("basic:") else f"Bearer {credential}"
            started = time.perf_counter()
            try:
                response = client.get(base_url + path, headers=headers)
                elapsed = round((time.perf_counter() - started) * 1000, 1)
                size = len(response.content)
                ok = response.status_code == expected and size < 1_000_000
                if token and token.encode() in response.content:
                    ok = False
                results.append(check(name, ok, f"HTTP {response.status_code}; {elapsed} ms; {size} bytes; expected {expected}; correlation header={'present' if 'x-correlation-id' in response.headers else 'absent'}"))
            except httpx.RequestError as exc:
                results.append(check(name, False, f"Request failed: {type(exc).__name__}"))
    return results


def schema_checks(base_url: str, token: str | None, timeout: float) -> list[dict]:
    paths = ("/health/ready", "/api/v1/graph/backends", "/api/v1/query/templates", "/api/v1/reports/templates")
    if not token:
        return [check("Live JSON Schema", None, "QA_TOKEN or EOIP_API_TOKEN is required")]
    results = []
    with httpx.Client(timeout=timeout, follow_redirects=False, trust_env=False) as client:
        try:
            document_response = client.get(base_url + "/openapi.json")
            document_response.raise_for_status()
            document = document_response.json()
        except (httpx.HTTPError, ValueError) as exc:
            return [check("OpenAPI fetch", False, f"Could not read OpenAPI: {type(exc).__name__}")]
        for path in paths:
            name = f"GET {path} schema"
            schema = document.get("paths", {}).get(path, {}).get("get", {}).get("responses", {}).get("200", {}).get("content", {}).get("application/json", {}).get("schema")
            if not schema:
                results.append(check(name, None, "No usable 200 application/json schema published"))
                continue
            headers = {"Authorization": f"Bearer {token}"} if path != "/health/ready" else {}
            try:
                response = client.get(base_url + path, headers=headers)
                if response.status_code != 200 or len(response.content) >= 1_000_000:
                    results.append(check(name, False, f"HTTP {response.status_code}; {len(response.content)} bytes"))
                    continue
                if token.encode() in response.content:
                    results.append(check(name, False, "Access token echoed in response"))
                    continue
                root_schema = {"components": document.get("components", {}), "allOf": [schema]}
                Draft202012Validator(root_schema).validate(response.json())
                results.append(check(name, True, f"HTTP 200; {len(response.content)} bytes; schema validated"))
            except (httpx.HTTPError, ValueError, ValidationError, TypeError) as exc:
                results.append(check(name, False, f"Schema probe failed: {type(exc).__name__}"))
    return results


def newman_executable() -> str | None:
    binary = "newman.cmd" if os.name == "nt" else "newman"
    local = ROOT / "qa" / "postman" / "node_modules" / ".bin" / binary
    return str(local) if local.is_file() else shutil.which("newman")


def run_postman(base_url: str, token: str | None, allow_remote: bool, collection_path: Path = COLLECTION_PATH, disposable: bool = False) -> list[dict]:
    if not token:
        return [check("Newman", None, "QA_TOKEN or EOIP_API_TOKEN is required")]
    executable = newman_executable()
    if not executable:
        return [check("Newman", None, "newman executable is not installed")]
    runtime = environment()
    values = {v["key"]: v for v in runtime["values"]}
    values["baseUrl"]["value"] = base_url
    values["qaToken"]["value"] = token
    values["qaAllowRemote"]["value"] = "true" if allow_remote else "false"
    if disposable:
        runtime["values"].append({"key": "qaDisposableTarget", "value": "true", "enabled": True})
    with tempfile.TemporaryDirectory(prefix="eoip-qa-postman-") as tmp:
        env_path = Path(tmp) / "environment.json"
        env_path.write_text(json.dumps(runtime), encoding="utf-8")
        try:
            completed = subprocess.run(
                [executable, "run", str(collection_path), "-e", str(env_path), "--reporters", "cli"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, check=False,
            )
        except subprocess.TimeoutExpired:
            return [check("Newman", False, "Timed out after 120 seconds")]
    # Newman output may contain the target URL or response snippets; no raw output is retained.
    return [check("Newman", completed.returncode == 0, f"Exit code {completed.returncode}; raw output intentionally discarded")]


def run_workflow() -> list[dict]:
    if not newman_executable():
        return [check("Disposable workflow", None, "Newman unavailable")]
    with tempfile.TemporaryDirectory(prefix="eoip-qa-workflow-") as root:
        token = secrets.token_urlsafe(32)
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        base_url = f"http://127.0.0.1:{port}"
        env = os.environ.copy()
        env.update({"EOIP_GRAPH_BACKEND": "memory", "EOIP_DATA_DIR": root, "EOIP_API_TOKEN": token, "REVA_ENABLED": "false"})
        from qa._principal import provision

        env.update(provision(root, token))
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "apps.api.main:create_app", "--factory", "--host", "127.0.0.1", "--port", str(port)],
            cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        try:
            ready = False
            with httpx.Client(timeout=1.0, trust_env=False) as client:
                for _ in range(80):
                    if process.poll() is not None:
                        break
                    try:
                        ready = client.get(base_url + "/health/ready").status_code == 200
                    except httpx.RequestError:
                        pass
                    if ready:
                        break
                    time.sleep(0.25)
            if not ready:
                return [check("Disposable workflow", False, "Bench-owned API did not become ready")]
            schemas = schema_checks(base_url, token, 10.0)
            read_only = run_postman(base_url, token, False)
            workflow = run_postman(base_url, token, False, WORKFLOW_PATH, disposable=True)
            read_only[0]["name"] = "Postman read-only"
            workflow[0]["name"] = "Postman source CRUD"
            return schemas + read_only + workflow
        finally:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("offline", help="Pinned OpenAPI and Postman safety checks")
    baseline = sub.add_parser("baseline", help="Explicitly regenerate the review-required OpenAPI baseline")
    baseline.add_argument("--write", action="store_true", required=True)
    sub.add_parser("workflow", help="Run guarded Postman CRUD against a bench-owned disposable API")
    for name in ("live", "schema", "postman"):
        command = sub.add_parser(name, help="Run read-only probes against an isolated QA API")
        command.add_argument("--base-url", default="http://127.0.0.1:8000")
        command.add_argument("--allow-remote", action="store_true")
        if name in {"live", "schema"}:
            command.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args(argv)
    if args.command == "baseline":
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        baseline_data = api_surface(offline_document())
        BASELINE.write_text(json.dumps(baseline_data, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {BASELINE.relative_to(ROOT)} with {len(baseline_data['operations'])} operations; review git diff before accepting")
        return 0
    try:
        if args.command == "offline":
            checks = offline_checks()
            metadata = {"baseline_sha256": file_sha256(BASELINE) if BASELINE.exists() else None}
        elif args.command == "workflow":
            checks = run_workflow()
            metadata = {"disposable_in_memory_api": True}
        else:
            base_url = validated_base_url(args.base_url, args.allow_remote)
            token = next((os.environ[key] for key in TOKEN_ENV if os.environ.get(key)), None)
            if args.command in {"live", "schema"}:
                if args.timeout <= 0 or args.timeout > 60:
                    parser.error("--timeout must be between 0 and 60 seconds")
                checks = live_checks(base_url, token, args.timeout) if args.command == "live" else schema_checks(base_url, token, args.timeout)
            else:
                checks = run_postman(base_url, token, args.allow_remote)
            metadata = {"target": base_url, "token_configured": bool(token)}
        output = write_evidence(args.command, checks, metadata)
        for item in checks:
            print(f"{item['status'].upper():7} {item['name']}: {item['detail']}")
        print(f"Evidence: {output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}")
        return exit_code(checks)
    except (ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(f"QA bench configuration error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
