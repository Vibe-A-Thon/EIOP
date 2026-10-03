"""Run the versioned EOIP graph benchmark and emit an evidence report.

Examples:
    python -m scripts.benchmark --run smoke --store memory
    python -m scripts.benchmark --run full --store configured --prepare-configured

``--prepare-configured`` is intentionally guarded: the configured graph must
be empty. Use it only with an isolated HugeGraph deployment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

import httpx
from eoip.contracts.query_plan import QueryPlan
from eoip.query.executor import QueryExecutor

from scripts.benchmark_data import SCALES, build_store, store_stats

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "config" / "benchmarks" / "mvp-v1.json"


def percentile(values: list[float], pct: float) -> float:
    """Nearest-rank percentile, suitable for published latency summaries."""
    if not values:
        return 0.0
    if pct < 0 or pct > 100:
        raise ValueError("percentile must be between 0 and 100")
    ordered = sorted(values)
    rank = max(1, math.ceil((pct / 100.0) * len(ordered)))
    return ordered[min(rank, len(ordered)) - 1]


def load_manifest(path: str | Path = DEFAULT_MANIFEST) -> dict:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"schema_version", "manifest_id", "dataset", "runs", "workloads"}
    missing = required - document.keys()
    if missing:
        raise ValueError(f"benchmark manifest missing fields: {sorted(missing)}")
    if document["schema_version"] != "eoip-benchmark-manifest/v1":
        raise ValueError("unsupported benchmark manifest schema")
    return document


def _total_memory_bytes() -> int | None:
    if os.name == "nt":
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("length", ctypes.c_ulong),
                    ("memory_load", ctypes.c_ulong),
                    ("total_physical", ctypes.c_ulonglong),
                    ("available_physical", ctypes.c_ulonglong),
                    ("total_page_file", ctypes.c_ulonglong),
                    ("available_page_file", ctypes.c_ulonglong),
                    ("total_virtual", ctypes.c_ulonglong),
                    ("available_virtual", ctypes.c_ulonglong),
                    ("available_extended_virtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.length = ctypes.sizeof(status)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return int(status.total_physical)
        except (AttributeError, OSError):
            return None
    try:
        return int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES"))
    except (AttributeError, OSError, ValueError):
        return None


def _peak_rss_bytes() -> int | None:
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            class ProcessMemoryCounters(ctypes.Structure):
                _fields_ = [
                    ("cb", wintypes.DWORD),
                    ("page_fault_count", wintypes.DWORD),
                    ("peak_working_set_size", ctypes.c_size_t),
                    ("working_set_size", ctypes.c_size_t),
                    ("quota_peak_paged_pool_usage", ctypes.c_size_t),
                    ("quota_paged_pool_usage", ctypes.c_size_t),
                    ("quota_peak_non_paged_pool_usage", ctypes.c_size_t),
                    ("quota_non_paged_pool_usage", ctypes.c_size_t),
                    ("pagefile_usage", ctypes.c_size_t),
                    ("peak_pagefile_usage", ctypes.c_size_t),
                ]

            counters = ProcessMemoryCounters()
            counters.cb = ctypes.sizeof(counters)
            get_process = ctypes.windll.kernel32.GetCurrentProcess
            get_process.restype = wintypes.HANDLE
            get_memory = ctypes.windll.psapi.GetProcessMemoryInfo
            get_memory.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(ProcessMemoryCounters),
                wintypes.DWORD,
            ]
            get_memory.restype = wintypes.BOOL
            if get_memory(get_process(), ctypes.byref(counters), counters.cb):
                return int(counters.peak_working_set_size)
        except (AttributeError, OSError):
            return None
        return None
    try:
        import resource

        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(value if sys.platform == "darwin" else value * 1024)
    except (ImportError, OSError, ValueError):
        return None


def hardware_profile(path: Path = PROJECT_ROOT) -> dict:
    disk = shutil.disk_usage(path)
    return {
        "os": platform.platform(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "cpu_model": platform.processor() or "not reported by operating system",
        "cpu_logical_cores": os.cpu_count(),
        "memory_total_bytes": _total_memory_bytes(),
        "storage_type": os.getenv("EOIP_BENCHMARK_STORAGE_TYPE", "not declared"),
        "storage_total_bytes": disk.total,
        "storage_free_bytes_at_start": disk.free,
        "containerized": Path("/.dockerenv").exists(),
    }


def _software_revision() -> dict:
    declared_revision = os.getenv("EOIP_BUILD_REVISION")
    declared_dirty = os.getenv("EOIP_BUILD_DIRTY")
    if declared_revision:
        return {
            "eoip_git_revision": declared_revision,
            "working_tree_dirty": (
                declared_dirty.casefold() in {"1", "true", "yes"}
                if declared_dirty is not None
                else None
            ),
            "source_fingerprint_sha256": _source_fingerprint(),
        }
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout
        return {
            "eoip_git_revision": revision,
            "working_tree_dirty": bool(status.strip()),
            "source_fingerprint_sha256": _source_fingerprint(),
        }
    except (OSError, subprocess.SubprocessError):
        return {
            "eoip_git_revision": "unknown",
            "working_tree_dirty": None,
            "source_fingerprint_sha256": _source_fingerprint(),
        }


def _source_fingerprint() -> str:
    """Hash execution-relevant source/configuration available to the runner."""
    digest = hashlib.sha256()
    roots = ["apps", "config", "deploy", "packages", "schemas", "scripts"]
    paths = [PROJECT_ROOT / name for name in roots]
    paths.extend(PROJECT_ROOT / name for name in ("pyproject.toml", "uv.lock"))
    files = []
    excluded_directories = {
        ".git",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "test-results",
    }
    for path in paths:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for directory, directory_names, file_names in os.walk(path):
                directory_names[:] = sorted(
                    name for name in directory_names if name not in excluded_directories
                )
                files.extend(
                    Path(directory) / name
                    for name in file_names
                    if Path(name).suffix
                    in {
                        ".css",
                        ".html",
                        ".js",
                        ".json",
                        ".lock",
                        ".py",
                        ".toml",
                        ".yml",
                        ".yaml",
                    }
                )
    for path in sorted(files, key=lambda item: item.relative_to(PROJECT_ROOT).as_posix()):
        relative = path.relative_to(PROJECT_ROOT).as_posix().encode()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        contents = path.read_bytes()
        digest.update(len(contents).to_bytes(8, "big"))
        digest.update(contents)
    return digest.hexdigest()


def _measure(operation: Callable[[], object], warmups: int, samples: int) -> dict:
    for _ in range(warmups):
        operation()
    latencies = []
    started = time.perf_counter()
    for _ in range(samples):
        sample_started = time.perf_counter_ns()
        operation()
        latencies.append((time.perf_counter_ns() - sample_started) / 1_000_000.0)
    duration = time.perf_counter() - started
    return {
        "samples": samples,
        "warmups": warmups,
        "latency_ms": {
            "min": round(min(latencies), 3),
            "p50": round(percentile(latencies, 50), 3),
            "p95": round(percentile(latencies, 95), 3),
            "p99": round(percentile(latencies, 99), 3),
            "max": round(max(latencies), 3),
        },
        "throughput_operations_per_second": round(samples / duration, 3) if duration else 0.0,
    }


def _query_operation(store, intent: str) -> Callable[[], object]:
    executor = QueryExecutor(store)
    plans = {
        "SEARCH": QueryPlan(
            intent="SEARCH",
            anchors=["BENCH-42"],
            max_depth=1,
            result_limit=25,
            evidence_mode="NONE",
        ),
        "PATH": QueryPlan(
            intent="PATH",
            anchors=["urn:bench:symbol:0", "urn:bench:symbol:5"],
            relationship_allowlist=["DEPENDS_ON"],
            max_depth=8,
            result_limit=100,
            evidence_mode="SUMMARY",
        ),
        "IMPACT": QueryPlan(
            intent="IMPACT",
            anchors=["urn:bench:item:0"],
            max_depth=2,
            result_limit=100,
            evidence_mode="SUMMARY",
        ),
    }
    plan = plans[intent]
    return lambda: executor.execute(plan)


def _api_operation(api_url: str, token: str) -> tuple[httpx.Client, Callable[[], object]]:
    client = httpx.Client(
        base_url=api_url.rstrip("/"),
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
        trust_env=False,
    )
    payload = {
        "intent": "SEARCH",
        "anchors": ["BENCH-42"],
        "max_depth": 1,
        "result_limit": 25,
        "evidence_mode": "NONE",
    }

    def operation():
        response = client.post("/api/v1/query", json=payload)
        response.raise_for_status()
        return response.json()

    return client, operation


def run_benchmark(
    manifest: dict,
    *,
    run_name: str = "smoke",
    backend: str = "memory",
    prepare_configured: bool = False,
    samples: int | None = None,
    warmups: int | None = None,
    api_url: str | None = None,
    api_token: str | None = None,
    batch_size: int | None = None,
) -> dict:
    if run_name not in manifest["runs"]:
        raise ValueError(f"unknown benchmark run: {run_name}")
    scale = manifest["dataset"]["profiles"][run_name]
    if scale not in SCALES:
        raise ValueError(f"manifest references unknown dataset profile: {scale}")
    seed = int(manifest["dataset"]["seed"])
    run_config = manifest["runs"][run_name]
    effective_batch_size = int(
        batch_size if batch_size is not None else manifest.get("bulk_batch_size", 500)
    )
    if not 1 <= effective_batch_size <= 1000:
        raise ValueError("bulk batch size must be between 1 and 1000")
    sample_count = samples if samples is not None else int(run_config["samples"])
    warmup_count = warmups if warmups is not None else int(run_config["warmups"])
    if sample_count < 1 or warmup_count < 0:
        raise ValueError("samples must be positive and warmups must be non-negative")

    resource_started = {
        "process_cpu_seconds": time.process_time(),
        "peak_rss_bytes": _peak_rss_bytes(),
        "storage_free_bytes": shutil.disk_usage(PROJECT_ROOT).free,
    }
    preparation_started = time.perf_counter()
    load_details = {"mode": "in-process-upsert"}
    if backend == "memory":
        store = build_store(scale, seed)
    elif backend == "configured":
        from eoip.runtime import create_store

        store = create_store()
        store.ensure_schema({})
        if prepare_configured:
            if store.count_vertices() or store.count_edges():
                raise RuntimeError(
                    "--prepare-configured requires an empty graph; use an isolated deployment"
                )
            source = build_store(scale, seed)
            source_vertices = source.find_vertices(limit=1_000_000, include_deleted=True)
            source_edges = source.find_edges(limit=1_000_000, include_historical=True)
            load_details = store.bulk_load(
                source_vertices,
                source_edges,
                batch_size=effective_batch_size,
            )
        elif store.get_vertex_by_canonical_id("urn:bench:item:0") is None:
            raise RuntimeError(
                "configured graph does not contain the benchmark dataset; prepare an isolated graph first"
            )
    else:
        raise ValueError(f"unknown store backend: {backend}")
    preparation_seconds = time.perf_counter() - preparation_started
    stats = store_stats(store, scale, seed)

    results = []
    api_client = None
    try:
        for workload in manifest["workloads"]:
            kind = workload["kind"]
            if kind == "store_lookup":
                operation = lambda: store.get_vertex_by_canonical_id("urn:bench:item:42")
            elif kind == "query_plan":
                operation = _query_operation(store, workload["intent"])
            elif kind == "http_api":
                if not api_url:
                    results.append(
                        {
                            "id": workload["id"],
                            "status": "skipped",
                            "reason": "--api-url was not supplied",
                            "target_p95_ms": workload["target_p95_ms"],
                        }
                    )
                    continue
                if not api_token:
                    raise ValueError("an API token is required when --api-url is supplied")
                api_client, operation = _api_operation(api_url, api_token)
            else:
                raise ValueError(f"unknown workload kind: {kind}")
            target = float(workload["target_p95_ms"])
            try:
                measurement = _measure(operation, warmup_count, sample_count)
            except Exception as exc:  # noqa: BLE001 - failures belong in the evidence report
                results.append(
                    {
                        "id": workload["id"],
                        "kind": kind,
                        "target_p95_ms": target,
                        "status": "failed",
                        "error": {"type": type(exc).__name__, "message": str(exc)},
                    }
                )
                continue
            measurement.update(
                {
                    "id": workload["id"],
                    "kind": kind,
                    "target_p95_ms": target,
                    "status": "passed" if measurement["latency_ms"]["p95"] <= target else "failed",
                }
            )
            results.append(measurement)
    finally:
        if api_client is not None:
            api_client.close()
        close = getattr(store, "close", None)
        if callable(close):
            close()

    resource_finished = {
        "process_cpu_seconds": time.process_time(),
        "peak_rss_bytes": _peak_rss_bytes(),
        "storage_free_bytes": shutil.disk_usage(PROJECT_ROOT).free,
    }
    mutations = stats["vertices"] + stats["edges"]
    preparation = {
        "duration_seconds": round(preparation_seconds, 3),
        "logical_mutations": mutations,
        "logical_mutations_per_second": (
            round(mutations / preparation_seconds, 3) if preparation_seconds else 0.0
        ),
        **load_details,
    }
    measured = [item for item in results if item["status"] != "skipped"]
    return {
        "schema_version": "eoip-benchmark-result/v1",
        "created_at": datetime.now(UTC).isoformat(),
        "requirement": manifest.get("requirement", "NFR-PERF-001"),
        "manifest": {
            "id": manifest["manifest_id"],
            "schema_version": manifest["schema_version"],
            "path": DEFAULT_MANIFEST.relative_to(PROJECT_ROOT).as_posix(),
        },
        "software": _software_revision(),
        "backend": backend,
        "run": run_name,
        "dataset": stats,
        "hardware": hardware_profile(),
        "configuration": {
            "samples": sample_count,
            "warmups": warmup_count,
            "api_url": api_url,
            "hugegraph_url": os.getenv("EOIP_HUGEGRAPH_URL") if backend == "configured" else None,
            "bulk_batch_size": effective_batch_size if backend == "configured" else None,
        },
        "preparation": preparation,
        "workloads": results,
        "resources": {
            "client_process_cpu_seconds": round(
                resource_finished["process_cpu_seconds"] - resource_started["process_cpu_seconds"], 3
            ),
            "client_peak_rss_bytes": resource_finished["peak_rss_bytes"],
            "storage_bytes_consumed": max(
                0, resource_started["storage_free_bytes"] - resource_finished["storage_free_bytes"]
            ),
            "scope": "benchmark client process; server/container metrics require external collection",
        },
        "status": "passed" if measured and all(item["status"] == "passed" for item in measured) else "failed",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--run", choices=["smoke", "full"], default="smoke")
    parser.add_argument("--store", choices=["memory", "configured"], default="memory")
    parser.add_argument("--prepare-configured", action="store_true")
    parser.add_argument("--samples", type=int)
    parser.add_argument("--warmups", type=int)
    parser.add_argument("--api-url")
    parser.add_argument("--api-token-env", default="EOIP_API_TOKEN")
    parser.add_argument(
        "--batch-size",
        type=int,
        help="Override the versioned manifest's bulk_batch_size",
    )
    parser.add_argument("--output", help="Optional JSON result path")
    args = parser.parse_args(argv)

    if args.prepare_configured and args.store != "configured":
        parser.error("--prepare-configured requires --store configured")
    token = os.getenv(args.api_token_env) if args.api_url else None
    report = run_benchmark(
        load_manifest(args.manifest),
        run_name=args.run,
        backend=args.store,
        prepare_configured=args.prepare_configured,
        samples=args.samples,
        warmups=args.warmups,
        api_url=args.api_url,
        api_token=token,
        batch_size=args.batch_size,
    )
    rendered = json.dumps(report, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
        print(f"benchmark report written to {destination}", file=sys.stderr)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
