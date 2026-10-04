@echo off
REM ═══════════════════════════════════════════════════════════════
REM  EOIP Automated Demo Runner — Meridian Financial Services
REM  Launches the Python demo runner with configurable modes
REM ═══════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

REM Resolve project root (two levels up from this bat file)
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%..\.."
set "PROJECT_ROOT=%CD%"
popd

REM Default values
set "MODE=full"
set "VERBOSE=--verbose"
set "OUTPUT="
set "PYTHON="

REM Parse arguments
:parse_args
if "%~1"=="" goto :find_python
if /i "%~1"=="--mode" (
    set "MODE=%~2"
    shift & shift
    goto :parse_args
)
if /i "%~1"=="manual" (
    set "MODE=manual"
    shift
    goto :parse_args
)
if /i "%~1"=="pipeline" (
    set "MODE=pipeline"
    shift
    goto :parse_args
)
if /i "%~1"=="full" (
    set "MODE=full"
    shift
    goto :parse_args
)
if /i "%~1"=="--quiet" (
    set "VERBOSE="
    shift
    goto :parse_args
)
if /i "%~1"=="--output" (
    set "OUTPUT=--output %~2"
    shift & shift
    goto :parse_args
)
if /i "%~1"=="--help" goto :show_help
if /i "%~1"=="-h" goto :show_help
shift
goto :parse_args

:find_python
REM Try venv first, then system Python
if exist "%PROJECT_ROOT%\.venv\Scripts\python.exe" (
    set "PYTHON=%PROJECT_ROOT%\.venv\Scripts\python.exe"
) else (
    where python >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON=python"
    ) else (
        echo ERROR: Python not found. Install Python 3.11+ or create a .venv.
        exit /b 1
    )
)

echo.
echo ══════════════════════════════════════════════════════════════
echo   EOIP Automated Demo — Meridian Financial Services
echo   Mode: %MODE%
echo   Python: %PYTHON%
echo   Root: %PROJECT_ROOT%
echo ══════════════════════════════════════════════════════════════
echo.

pushd "%PROJECT_ROOT%"
"%PYTHON%" -m demo.autodemo.runner --mode %MODE% %VERBOSE% %OUTPUT%
set "EXIT_CODE=%errorlevel%"
popd

if %EXIT_CODE% neq 0 (
    echo.
    echo Demo completed with failures. Exit code: %EXIT_CODE%
) else (
    echo.
    echo Demo completed successfully.
)

exit /b %EXIT_CODE%

:show_help
echo.
echo EOIP Automated Demo Runner
echo.
echo Usage: run-demo.bat [options]
echo.
echo Modes:
echo   full       Run both manual (PAY) and pipeline (FRD) ingestion
echo              plus code-graph, crawler, RAG, agents, LAYA (default)
echo   manual     Run manual ingestion only (Payment Gateway / PAY domain)
echo   pipeline   Run pipeline ingestion only (Fraud Detection / FRD domain)
echo.
echo Options:
echo   --mode MODE    Set mode (full, manual, pipeline)
echo   --quiet        Suppress verbose output
echo   --output FILE  Write JSON results to file
echo   --help, -h     Show this help
echo.
echo Examples:
echo   run-demo.bat                          Full demo, verbose
echo   run-demo.bat manual                   Manual ingestion only
echo   run-demo.bat --mode pipeline --quiet  Pipeline mode, quiet
echo   run-demo.bat --output results.json    Full demo, save results
echo.
exit /b 0
