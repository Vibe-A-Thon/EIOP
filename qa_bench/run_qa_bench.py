#!/usr/bin/env python3
"""Unified QA Test Bench Orchestrator for KnowGridFlow / EOIP.

Usage:
  python qa_bench/run_qa_bench.py --suite api
  python qa_bench/run_qa_bench.py --suite selenium --headless
  python qa_bench/run_qa_bench.py --suite perf
  python qa_bench/run_qa_bench.py --suite all --report-html
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from qa_bench.config import (
    BACKEND_URL,
    FRONTEND_URL,
    REPORTS_DIR,
    SCREENSHOTS_DIR,
    DEFAULT_BROWSER,
    HEADLESS_MODE,
)


def check_server_reachable(url: str, timeout: float = 1.5) -> bool:
    """Check if a HTTP server responds at the given URL."""
    import urllib.parse
    import urllib.request

    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ("http", "https"):
        return False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "QA-Bench-Probe"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.status < 500
    except (urllib.error.URLError, OSError, TimeoutError):
        return False


def print_banner(suite: str, browser: str, headless: bool) -> None:
    print("\n" + "=" * 76)
    print("  KNOWGRIDFLOW / EOIP — ENTERPRISE QA AUTOMATION TEST BENCH")
    print("=" * 76)
    print(f"  Target Suite : {suite.upper()}")
    print(f"  Browser      : {browser} (headless={headless})")
    print(f"  Backend URL  : {BACKEND_URL}")
    print(f"  Frontend URL : {FRONTEND_URL}")
    print(f"  Reports Dir  : {REPORTS_DIR}")
    print("=" * 76 + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="KnowGridFlow QA Automation Test Bench Orchestrator")
    parser.add_argument(
        "--suite",
        choices=["all", "api", "selenium", "playwright", "perf", "e2e", "security", "chaos", "load"],
        default="api",
        help="Test suite to run (default: api)",
    )
    parser.add_argument(
        "--browser",
        choices=["chrome", "edge"],
        default=DEFAULT_BROWSER,
        help=f"Web browser for Selenium UI tests (default: {DEFAULT_BROWSER})",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=HEADLESS_MODE,
        help="Run browser in headless mode",
    )
    parser.add_argument(
        "--no-headless",
        action="store_false",
        dest="headless",
        help="Run browser in visible windowed mode",
    )
    parser.add_argument(
        "--report-html",
        action="store_true",
        help="Generate pytest HTML report in qa_bench/reports/",
    )
    parser.add_argument(
        "-k", "--filter",
        type=str,
        default="",
        help="Pytest substring expression filter (-k)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose pytest output",
    )

    args = parser.parse_args()

    # Set environment variables for child pytest execution
    os.environ["QA_BROWSER"] = args.browser
    os.environ["QA_HEADLESS"] = "true" if args.headless else "false"

    print_banner(args.suite, args.browser, args.headless)

    # Server liveness diagnostic
    backend_live = check_server_reachable(f"{BACKEND_URL}/health")
    frontend_live = check_server_reachable(FRONTEND_URL)

    print("[*] Pre-flight Server Diagnostics:")
    print(f"    Backend  ({BACKEND_URL}): {'[ONLINE]' if backend_live else '[OFFLINE - In-process TestClient fallback]'}")
    print(f"    Frontend ({FRONTEND_URL}): {'[ONLINE]' if frontend_live else '[OFFLINE]'}")

    if args.suite in ("selenium", "all") and not frontend_live:
        print("\n[WARNING] Frontend server is OFFLINE at http://localhost:3000.")
        print("          Selenium UI tests require the frontend dev server running:")
        print("          Run: npm --prefix frontend run dev\n")

    # Build pytest invocation arguments
    pytest_args = [sys.executable, "-m", "pytest"]

    if args.verbose:
        pytest_args.append("-v")
    else:
        pytest_args.append("-ra")

    if args.filter:
        pytest_args.extend(["-k", args.filter])

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.report_html:
        html_out = REPORTS_DIR / "qa_test_report.html"
        pytest_args.extend([f"--html={html_out}", "--self-contained-html"])

    # Suite mapping
    if args.suite == "playwright":
        npx_bin = shutil.which("npx") or "npx"
        playwright_cmd = [npx_bin, "playwright", "test", "--config", "qa_bench/playwright/playwright.config.ts"]
        if not args.headless:
            playwright_cmd.append("--headed")
        if args.filter:
            playwright_cmd.extend(["-g", args.filter])
        print(f"[*] Executing Playwright Command: {' '.join(playwright_cmd)}\n")
        t0 = time.perf_counter()
        res = subprocess.run(playwright_cmd, cwd=str(REPO_ROOT), shell=False, check=False)
        elapsed = time.perf_counter() - t0
        status_str = "SUCCESS (PASSED)" if res.returncode == 0 else f"FAILED (exit code {res.returncode})"
        print(f"\n  PLAYWRIGHT EXECUTION FINISHED: {status_str} in {elapsed:.2f}s\n")
        return res.returncode

    if args.suite == "load":
        from qa_bench.load_stress.stress_runner import run_stress_test
        run_stress_test(concurrency=10, duration_seconds=5)
        return 0

    if args.suite == "api":
        pytest_args.append("qa_bench/api_functional")
    elif args.suite == "selenium":
        pytest_args.append("qa_bench/selenium/tests")
    elif args.suite == "perf":
        pytest_args.append("qa_bench/performance_bench")
    elif args.suite == "security":
        pytest_args.append("qa_bench/security_dast")
    elif args.suite == "chaos":
        pytest_args.append("qa_bench/chaos_bench")
    elif args.suite == "e2e":
        pytest_args.append("qa_bench/e2e_workflows")
    elif args.suite == "all":
        pytest_args.extend(["qa_bench/api_functional", "qa_bench/security_dast", "qa_bench/chaos_bench", "qa_bench/e2e_workflows", "qa_bench/performance_bench"])

    print(f"[*] Executing Test Command: {' '.join(pytest_args)}\n")
    t0 = time.perf_counter()
    res = subprocess.run(pytest_args, cwd=str(REPO_ROOT), check=False)
    elapsed = time.perf_counter() - t0

    print("\n" + "=" * 76)
    status_str = "SUCCESS (PASSED)" if res.returncode == 0 else f"FAILED (exit code {res.returncode})"
    print(f"  QA BENCH EXECUTION FINISHED: {status_str} in {elapsed:.2f}s")
    print("=" * 76 + "\n")

    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
