"""Unit tests for Phase 7 WP 7.1: Scale and Polish (5 tasks).

Requirements:
- S-01: Frontend KGR completion (WebGL rendering, layout worker, visual query builder)
- S-02: Performance benchmarks (load testing at 50K+ nodes, query latency, memory profiling)
- S-03: CI/CD pipeline (automated test + lint + build + deploy workflows)
- S-04: Developer documentation (API docs, architecture guides, tutorial)
- S-05: Security hardening (OWASP Top 10 audit, dependency scanning, secrets detection)
"""

from __future__ import annotations

from pathlib import Path
import pytest

from eoip.ci.pipeline import (
    STAGE_LINT,
    STAGE_SCHEMA,
    STAGE_SECURITY,
    STAGE_ORDER,
    KGCIReport,
    run_pipeline,
)
from eoip.graph.benchmark import BenchmarkHarness
from eoip.graph.memory import MemoryGraphStore
from eoip.security.hardening import SecurityHardeningScanner


@pytest.mark.req("S-01")
def test_s_01_frontend_kgr_completion():
    # Verify WebGL renderer, layout worker, and visual query builder modules exist and are valid
    webgl_file = Path("apps/web/src/kgr/rendering/WebGLGraphRenderer.js")
    worker_file = Path("apps/web/src/kgr/workers/layoutWorker.js")
    builder_file = Path("apps/web/src/kgr/components/VisualQueryBuilder.jsx")

    assert webgl_file.exists()
    assert worker_file.exists()
    assert builder_file.exists()

    webgl_content = webgl_file.read_text(encoding="utf-8")
    assert "WebGLGraphRenderer" in webgl_content
    assert "nodeCapacity" in webgl_content

    builder_content = builder_file.read_text(encoding="utf-8")
    assert "VisualQueryBuilder" in builder_content
    assert "MATCH" in builder_content


@pytest.mark.req("S-02")
def test_s_02_performance_benchmarks():
    store = MemoryGraphStore()
    benchmark = BenchmarkHarness()


    # 1. Benchmark at 50K+ nodes target
    scale_res = benchmark.run_large_scale_benchmark(store, target_nodes=50_000)
    assert scale_res["target_scale_nodes"] == 50_000
    assert scale_res["target_50k_kpi_met"] is True
    assert scale_res["measured_throughput_ops_sec"] > 1000.0

    # 2. Memory profiling
    mem_res = benchmark.run_memory_profiling(store)
    assert mem_res["memory_per_50k_nodes_mb"] > 0
    assert mem_res["status"] == "HEALTHY"

    # 3. Query latency baselines
    lat_res = benchmark.run_query_latency_baselines(store, queries=50)
    assert lat_res["p95_ms"] < 50.0
    assert lat_res["sla_p95_below_50ms"] is True


@pytest.mark.req("S-03")
def test_s_03_cicd_pipeline():
    # Verify GitHub Actions workflow exists
    ci_workflow = Path(".github/workflows/ci.yml")
    assert ci_workflow.exists()
    ci_text = ci_workflow.read_text(encoding="utf-8")
    assert "lint-and-validate" in ci_text
    assert "test" in ci_text
    assert "build-and-package" in ci_text

    # Verify python KG CI pipeline stages
    assert STAGE_LINT in STAGE_ORDER
    assert STAGE_SCHEMA in STAGE_ORDER
    assert STAGE_SECURITY in STAGE_ORDER

    # Run offline pipeline in report-only mode
    report = run_pipeline(fail_on="never")
    assert isinstance(report, KGCIReport)
    assert len(report.stages) >= 2



@pytest.mark.req("S-04")
def test_s_04_developer_documentation():
    docs_dir = Path("docs")
    getting_started = docs_dir / "getting-started.md"
    arch_guide = docs_dir / "architecture-guide.md"
    api_ref = docs_dir / "api-reference.md"

    assert getting_started.exists()
    assert arch_guide.exists()
    assert api_ref.exists()

    assert "Prerequisites" in getting_started.read_text(encoding="utf-8")
    assert "Architecture Overview" in arch_guide.read_text(encoding="utf-8")
    assert "Core REST API Endpoints" in api_ref.read_text(encoding="utf-8")


@pytest.mark.req("S-05")
def test_s_05_security_hardening():
    scanner = SecurityHardeningScanner()

    # 1. Secret detection
    leaked_code = 'const apiKey = "abcdef1234567890abcdef1234567890";'
    secret_findings = scanner.scan_for_secrets(leaked_code, "test.js")
    assert len(secret_findings) >= 1
    assert secret_findings[0].category == "SECRET_LEAK"

    # 2. OWASP Top 10 API configuration check
    endpoints = [
        {"path": "/api/v1/admin/users", "auth_required": False, "cors_origin": "*"},
        {"path": "/health", "auth_required": False, "cors_origin": "https://app.corp"},
    ]
    owasp_findings = scanner.audit_owasp_top_10(endpoints)
    assert len(owasp_findings) >= 2

    # 3. Dependency vulnerability check
    deps = [
        {"name": "log4j", "version": "1.2.17"},
        {"name": "safe-lib", "version": "2.0.0"},
    ]
    cve_findings = scanner.audit_dependencies(deps)
    assert len(cve_findings) == 1
    assert "CVE-2021-44228" in cve_findings[0].description

    # 4. Overall posture report
    report = scanner.generate_security_posture_report(endpoints, deps, leaked_code)
    assert "security_score" in report
    assert report["total_findings"] >= 4
