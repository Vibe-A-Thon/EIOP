@echo off
REM EOIP Manual Ingestion Demo - Payment Gateway (PAY)
REM Demonstrates manual ingestion of all PAY-domain source systems,
REM graph construction, traversal, validation, and quality metrics.

setlocal

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%..\.." || exit /b 1
set "PROJECT_ROOT=%CD%"
popd

set "VERBOSE=--verbose"
set "OUTPUT_FILE="
set "DATA_DIR="
set "PYTHON="
set "DRY_RUN="

:parse_args
if "%~1"=="" goto :find_python
if /i "%~1"=="--dry-run" (
    set "DRY_RUN=1"
    shift
    goto :parse_args
)
if /i "%~1"=="--quiet" (
    set "VERBOSE="
    shift
    goto :parse_args
)
if /i "%~1"=="--output" (
    if "%~2"=="" goto :invalid_args
    set "OUTPUT_FILE=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--data-dir" (
    if "%~2"=="" goto :invalid_args
    set "DATA_DIR=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--help" goto :show_help
if /i "%~1"=="-h" goto :show_help
echo ERROR: Unknown argument "%~1".
goto :invalid_args

:find_python
if defined DRY_RUN goto :dry_run
if exist "%PROJECT_ROOT%\.venv\Scripts\python.exe" (
    set "PYTHON=%PROJECT_ROOT%\.venv\Scripts\python.exe"
) else (
    where python >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python not found. Install Python 3.11+ or create a .venv.
        exit /b 1
    )
    set "PYTHON=python"
)

echo.
echo ==============================================================
echo   EOIP Manual Ingestion Demo - Payment Gateway (PAY)
echo   Meridian Financial Services
echo   -----------------------------------------------------------
echo   Demonstrates:
echo     - Multi-source manual ingestion (Rally, Jira, GitLab,
echo       ServiceNow, Confluence, qTest, Kibana, Grafana,
echo       Datadog, Figma, API Portal, Code Graph, Crawler)
echo     - Graph construction and Jira deep ingestion
echo     - Graph traversal (impact, path, neighborhood)
echo     - Validation and quality metrics
echo   -----------------------------------------------------------
echo   Python: %PYTHON%
echo   Root:   %PROJECT_ROOT%
echo ==============================================================
echo.

echo Starting Docker Desktop services and waiting for health checks...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PROJECT_ROOT%\scripts\docker.ps1" up
if errorlevel 1 (
    echo.
    echo ERROR: EOIP could not be started. Review the Docker output above.
    exit /b 1
)

echo Opening the EOIP web application...
start "" "http://localhost:8080/app"

pushd "%PROJECT_ROOT%" || exit /b 1
if defined OUTPUT_FILE if defined DATA_DIR (
    "%PYTHON%" -X utf8 -m demo.autodemo.runner --mode manual %VERBOSE% --output "%OUTPUT_FILE%" --data-dir "%DATA_DIR%"
) else if defined OUTPUT_FILE (
    "%PYTHON%" -X utf8 -m demo.autodemo.runner --mode manual %VERBOSE% --output "%OUTPUT_FILE%"
) else if defined DATA_DIR (
    "%PYTHON%" -X utf8 -m demo.autodemo.runner --mode manual %VERBOSE% --data-dir "%DATA_DIR%"
) else (
    "%PYTHON%" -X utf8 -m demo.autodemo.runner --mode manual %VERBOSE%
)
set "EXIT_CODE=%ERRORLEVEL%"
popd

if not "%EXIT_CODE%"=="0" (
    echo.
    echo Manual ingestion demo completed with failures. Exit code: %EXIT_CODE%
) else (
    echo.
    echo Manual ingestion demo completed successfully.
)
exit /b %EXIT_CODE%

:dry_run
echo DRY RUN: mode=manual; normal execution starts Docker, opens web UI,
echo and runs PAY-domain manual ingestion with graph verification.
exit /b 0

:invalid_args
echo.
echo Run run-demo-manual.bat --help for usage.
exit /b 2

:show_help
echo.
echo EOIP Manual Ingestion Demo - Payment Gateway (PAY)
echo.
echo Usage: run-demo-manual.bat [options]
echo.
echo Runs the manual ingestion demo for the Payment Gateway (PAY) domain.
echo This ingests all 13 source system JSON files from the manual/ folder,
echo constructs the knowledge graph, and verifies traversals and quality.
echo.
echo Source Systems Demonstrated:
echo   Rally         Portfolio epics, features, user stories, defects
echo   Jira          Issues with full cross-references (MRs, CHGs, TCs)
echo   GitLab        Merge requests and CI/CD pipelines
echo   ServiceNow    Changes, incidents, and problems
echo   Confluence    Wiki pages (architecture, runbooks, schemas)
echo   qTest         Test suites, test cases, and test runs
echo   Kibana        Dashboards, index patterns, saved searches
echo   Grafana       Dashboards, alert rules, datasources
echo   Datadog       Dashboards and monitors
echo   Figma         Design files, pages, and components
echo   API Portal    Services and API endpoints
echo   Code Graph    Repository code structure and dependencies
echo   Crawler       Crawled internal portal pages
echo.
echo Options:
echo   --quiet           Suppress verbose output.
echo   --output FILE     Write JSON results to a file.
echo   --data-dir DIR    Store raw captures and DLQ files in this directory.
echo   --help, -h        Show this help.
echo   --dry-run         Print plan without starting services.
echo.
echo Examples:
echo   run-demo-manual.bat
echo   run-demo-manual.bat --quiet
echo   run-demo-manual.bat --output "C:\temp\manual-results.json"
echo.
exit /b 0
