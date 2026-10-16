@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%..\.." || exit /b 1
set "PROJECT_ROOT=%CD%"
set "DEMO_ARGS="
set "NO_PAUSE="
set "DRY_RUN="
set "EXIT_CODE=0"

:parse_args
if "%~1"=="" goto :args_parsed
if /i "%~1"=="--dry-run" (
    set "DRY_RUN=1"
    set "DEMO_ARGS=%DEMO_ARGS% --dry-run"
    shift
    goto :parse_args
)
if /i "%~1"=="--no-pause" (
    set "NO_PAUSE=1"
    set "DEMO_ARGS=%DEMO_ARGS% --no-pause"
    shift
    goto :parse_args
)
if /i "%~1"=="--help" goto :show_help
if /i "%~1"=="-h" goto :show_help
echo ERROR: Unknown argument "%~1".
set "EXIT_CODE=2"
goto :finish

:args_parsed
if defined DRY_RUN goto :run_demo

echo.
echo ==============================================================
echo   EOIP Context 0.1.0 - Visible VS Code Live Demo
echo   Workspace source extension; live API and MCP services
echo ==============================================================
echo.

if not defined EOIP_API_URL set "EOIP_API_URL=http://localhost:8000"
if not defined EOIP_MCP_URL set "EOIP_MCP_URL=http://localhost:8001/mcp"

echo Starting Docker Desktop services (API + MCP)...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PROJECT_ROOT%\scripts\docker.ps1" up
if errorlevel 1 (
    echo ERROR: EOIP could not be started. Review the Docker output above.
    set "EXIT_CODE=1"
    goto :finish
)

echo.
echo Waiting up to 60 seconds for API and MCP readiness...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$api=$env:EOIP_API_URL; $mcp=[Uri]$env:EOIP_MCP_URL; for($i=0; $i -lt 30; $i++){ try { Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 -Uri ($api.TrimEnd('/') + '/health/ready') | Out-Null; Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 -Uri ($mcp.GetLeftPart([UriPartial]::Authority) + '/health/live') | Out-Null; exit 0 } catch { Start-Sleep -Seconds 2 } }; exit 1"
if errorlevel 1 (
    echo ERROR: EOIP API or MCP did not become healthy within 60 seconds.
    echo Check Docker service logs and the EOIP_API_URL / EOIP_MCP_URL configuration.
    set "EXIT_CODE=1"
    goto :finish
)

:run_demo
echo.
echo Launching the visible EOIP VS Code demo...
node "%PROJECT_ROOT%\demo\autodemo\vscode-demo.js"%DEMO_ARGS%
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
    echo.
    echo VS Code live demo failed with exit code %EXIT_CODE%.
) else (
    echo.
    echo VS Code live demo finished. The JSON receipt is under test-results\.
)
goto :finish

:finish
if not defined NO_PAUSE (
    echo.
    echo Exit code: %EXIT_CODE%
    pause
)
popd
endlocal & exit /b %EXIT_CODE%

:show_help
echo.
echo EOIP Context 0.1.0 visible VS Code live demo
echo Usage: run-demo-vscode.bat [--dry-run] [--no-pause] [--help]
echo.
echo Default behavior starts local API/MCP services, then runs the workspace
echo source extension in a disposable visible VS Code development host. It
echo requires the intent-to-runtime and knowledge-provenance demo scenarios to
echo already be ingested and ready. This launcher does not preload graph data.
echo.
echo Live coverage: NLQ SEARCH, PATH, IMPACT, NEIGHBORHOOD, LINEAGE and
echo TRACEABILITY; plus all 11 read-only MCP tools supported by the extension.
echo.
echo Options:
echo   --dry-run   Print the planned coverage without starting services.
echo   --no-pause  Do not hold VS Code between steps or pause the console.
echo   --help      Show this help.
echo.
set "NO_PAUSE=1"
set "EXIT_CODE=0"
goto :finish
