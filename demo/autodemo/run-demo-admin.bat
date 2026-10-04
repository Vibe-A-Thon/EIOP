@echo off
REM EOIP Administration Demo
REM Demonstrates platform administration capabilities including
REM graph health, schema inspection, connector catalog, ingestion,
REM export, gap coverage, evidence manifests, and trust states.

setlocal

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%..\.." || exit /b 1
set "PROJECT_ROOT=%CD%"
popd

set "VERBOSE=--verbose"
set "OUTPUT_FILE="
set "PYTHON="
set "DRY_RUN="
set "SKIP_INGEST="

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
if /i "%~1"=="--skip-ingest" (
    set "SKIP_INGEST=--skip-ingest"
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
echo   EOIP Administration Demo
echo   Meridian Financial Services
echo   -----------------------------------------------------------
echo   Demonstrates:
echo     - Graph health status and statistics
echo     - Ontology schema inspection
echo     - Connector catalog and capabilities
echo     - Single and batch JSON ingestion
echo     - Graph export (GraphML, JSON-LD)
echo     - Gap requirements coverage analysis
echo     - Evidence manifest generation
echo     - Test intelligence mappings
echo     - Knowledge firewall inspection
echo     - Trust state taxonomy
echo     - Graph validation and quality scoring
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

echo Opening the EOIP admin interface...
start "" "http://localhost:8080/admin"

pushd "%PROJECT_ROOT%" || exit /b 1
if defined OUTPUT_FILE (
    "%PYTHON%" -X utf8 -m demo.autodemo.admin_runner %VERBOSE% %SKIP_INGEST% --output "%OUTPUT_FILE%"
) else (
    "%PYTHON%" -X utf8 -m demo.autodemo.admin_runner %VERBOSE% %SKIP_INGEST%
)
set "EXIT_CODE=%ERRORLEVEL%"
popd

if not "%EXIT_CODE%"=="0" (
    echo.
    echo Administration demo completed with failures. Exit code: %EXIT_CODE%
) else (
    echo.
    echo Administration demo completed successfully.
)
exit /b %EXIT_CODE%

:dry_run
echo DRY RUN: admin demo; normal execution starts Docker, opens admin UI,
echo and runs administration capability demonstrations via the live API.
exit /b 0

:invalid_args
echo.
echo Run run-demo-admin.bat --help for usage.
exit /b 2

:show_help
echo.
echo EOIP Administration Demo
echo.
echo Usage: run-demo-admin.bat [options]
echo.
echo Runs the administration capabilities demo against the live EOIP API
echo at localhost:8000. Demonstrates graph management, schema inspection,
echo connector catalog, ingestion, export, gap coverage, evidence manifests,
echo test intelligence, knowledge firewall, and trust state features.
echo.
echo Administration Capabilities Demonstrated:
echo   1. Graph Health         Current graph statistics and status
echo   2. Schema Inspection    Ontology vertex/edge schema listing
echo   3. Connector Catalog    Available connectors and their capabilities
echo   4. Single Ingestion     Upload one source JSON file
echo   5. Batch Ingestion      Upload multiple source files at once
echo   6. Export Formats        List available graph export formats
echo   7. Graph Export         Export graph in GraphML format
echo   8. Gap Coverage         Requirements gap analysis
echo   9. Evidence Manifests   Generate compliance evidence
echo  10. Test Intelligence    Test-to-requirement mappings
echo  11. Knowledge Firewall   Data access and trust boundaries
echo  12. Trust States         Trust state taxonomy and transitions
echo.
echo Options:
echo   --quiet           Suppress verbose output.
echo   --skip-ingest     Skip ingestion steps (use pre-loaded data).
echo   --output FILE     Write JSON results to a file.
echo   --help, -h        Show this help.
echo   --dry-run         Print plan without starting services.
echo.
echo Examples:
echo   run-demo-admin.bat
echo   run-demo-admin.bat --skip-ingest
echo   run-demo-admin.bat --output "C:\temp\admin-results.json"
echo.
exit /b 0
