@echo off
REM EOIP VS Code Extension Demo
REM Demonstrates the EOIP VS Code plugin (eoip-context-0.1.0)
REM with NLQ (Natural Language Query) and MCP capabilities.

setlocal

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%..\.." || exit /b 1
set "PROJECT_ROOT=%CD%"
popd

set "PYTHON="
set "DRY_RUN="

:parse_args
if "%~1"=="" goto :find_python
if /i "%~1"=="--dry-run" (
    set "DRY_RUN=1"
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
echo   EOIP VS Code Extension Demo (eoip-context-0.1.0)
echo   Meridian Financial Services
echo   -----------------------------------------------------------
echo   Demonstrates:
echo     - NLQ impact analysis (natural language queries)
echo     - MCP handshake (Model Context Protocol connection)
echo     - MCP search (graph-aware code search)
echo     - MCP lineage (full traceability chains)
echo     - NLQ cross-domain queries (PAY + FRD)
echo     - NLQ compliance queries (PCI DSS, audit)
echo   -----------------------------------------------------------
echo   Root: %PROJECT_ROOT%
echo ==============================================================
echo.

echo Starting Docker Desktop services (API + MCP)...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PROJECT_ROOT%\scripts\docker.ps1" up
if errorlevel 1 (
    echo.
    echo ERROR: EOIP could not be started. Review the Docker output above.
    exit /b 1
)

echo.
echo Waiting for MCP server at localhost:8001...
:wait_mcp
powershell.exe -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8001/health' -TimeoutSec 5 -UseBasicParsing; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"
if errorlevel 1 (
    echo   MCP not ready yet, retrying in 3s...
    timeout /t 3 /nobreak >nul
    goto :wait_mcp
)
echo   MCP server is healthy.

echo.
echo Pre-loading demo data for VS Code scenarios...
pushd "%PROJECT_ROOT%" || exit /b 1
"%PYTHON%" -X utf8 -m demo.autodemo.runner --mode full --quiet
if errorlevel 1 (
    echo WARNING: Data pre-load had failures, but VS Code demo will continue.
)
popd

echo.
echo Launching VS Code extension demo...
node "%PROJECT_ROOT%\demo\autodemo\vscode-demo.js"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo.
    echo VS Code extension demo completed with failures. Exit code: %EXIT_CODE%
) else (
    echo.
    echo VS Code extension demo completed successfully.
)
exit /b %EXIT_CODE%

:dry_run
node "%PROJECT_ROOT%\demo\autodemo\vscode-demo.js" --dry-run
exit /b %ERRORLEVEL%

:invalid_args
echo.
echo Run run-demo-vscode.bat --help for usage.
exit /b 2

:show_help
echo.
echo EOIP VS Code Extension Demo (eoip-context-0.1.0)
echo.
echo Usage: run-demo-vscode.bat [options]
echo.
echo Launches an isolated VS Code instance with the EOIP extension loaded,
echo demonstrating Natural Language Query (NLQ) and Model Context Protocol
echo (MCP) capabilities against the live EOIP API and MCP servers.
echo.
echo Demo Steps:
echo   1. NLQ Impact      Natural language impact analysis query
echo   2. MCP Handshake   Establish MCP connection to localhost:8001
echo   3. MCP Search      Graph-aware code and artifact search
echo   4. MCP Lineage     Full requirement-to-deployment traceability
echo   5. NLQ Cross       Cross-domain query spanning PAY and FRD
echo   6. NLQ Compliance  Compliance and audit query (PCI DSS)
echo.
echo Prerequisites:
echo   - Node.js 18+ installed
echo   - VS Code 1.96.4 cached in apps/vscode-extension/.vscode-test/
echo   - Extension node_modules installed
echo   - EOIP API running at localhost:8000
echo   - EOIP MCP server running at localhost:8001
echo   - EOIP_API_TOKEN in environment or deploy/.env
echo.
echo Options:
echo   --help, -h        Show this help.
echo   --dry-run         Print plan without starting services.
echo.
echo Examples:
echo   run-demo-vscode.bat
echo   run-demo-vscode.bat --dry-run
echo.
exit /b 0
