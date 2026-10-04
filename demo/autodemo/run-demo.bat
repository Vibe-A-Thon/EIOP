@echo off
REM EOIP Automated Demo Runner - Meridian Financial Services
REM Launches the Python demo runner with configurable modes.

setlocal

REM Resolve project root (two levels up from this batch file).
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%..\.." || exit /b 1
set "PROJECT_ROOT=%CD%"
popd

REM Default values.
set "MODE=full"
set "VERBOSE=--verbose"
set "OUTPUT_FILE="
set "DATA_DIR="
set "PYTHON="

:parse_args
if "%~1"=="" goto :find_python
if /i "%~1"=="--mode" (
    if "%~2"=="" goto :invalid_args
    set "MODE=%~2"
    shift
    shift
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
REM Try the project virtual environment first, then system Python.
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
echo   EOIP Automated Demo - Meridian Financial Services
echo   Mode: %MODE%
echo   Python: %PYTHON%
echo   Root: %PROJECT_ROOT%
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
    "%PYTHON%" -X utf8 -m demo.autodemo.runner --mode "%MODE%" %VERBOSE% --output "%OUTPUT_FILE%" --data-dir "%DATA_DIR%"
) else if defined OUTPUT_FILE (
    "%PYTHON%" -X utf8 -m demo.autodemo.runner --mode "%MODE%" %VERBOSE% --output "%OUTPUT_FILE%"
) else if defined DATA_DIR (
    "%PYTHON%" -X utf8 -m demo.autodemo.runner --mode "%MODE%" %VERBOSE% --data-dir "%DATA_DIR%"
) else (
    "%PYTHON%" -X utf8 -m demo.autodemo.runner --mode "%MODE%" %VERBOSE%
)
set "EXIT_CODE=%ERRORLEVEL%"
popd

if not "%EXIT_CODE%"=="0" (
    echo.
    echo Demo completed with failures. Exit code: %EXIT_CODE%
) else (
    echo.
    echo Demo completed successfully.
)
exit /b %EXIT_CODE%

:invalid_args
echo.
echo Run run-demo.bat --help for usage.
exit /b 2

:show_help
echo.
echo EOIP Automated Demo Runner
echo.
echo Usage: run-demo.bat [options]
echo.
echo Modes:
echo   full       Run both manual (PAY) and pipeline (FRD) ingestion
echo              plus code-graph, crawler, RAG, agents, and LAYA.
echo   manual     Run manual ingestion only (Payment Gateway / PAY).
echo   pipeline   Run pipeline ingestion only (Fraud Detection / FRD).
echo.
echo Options:
echo   --mode MODE       Set mode to full, manual, or pipeline.
echo   --quiet           Suppress verbose output.
echo   --output FILE     Write JSON results to a file.
echo   --data-dir DIR    Store raw captures and DLQ files in this directory.
echo   --help, -h        Show this help.
echo.
echo The launcher starts Docker Desktop services, opens the web UI, then runs
echo the automated console validation.
echo.
echo Examples:
echo   run-demo.bat
echo   run-demo.bat manual
echo   run-demo.bat --mode pipeline --quiet
echo   run-demo.bat --output "C:\temp\results.json"
echo   run-demo.bat manual --data-dir "C:\temp\eoip-demo-data"
echo.
exit /b 0
