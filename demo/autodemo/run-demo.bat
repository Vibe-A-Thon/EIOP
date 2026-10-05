@echo off
setlocal
set "NO_PAUSE="
for %%A in (%*) do (
    if /i "%%~A"=="--no-pause" set "NO_PAUSE=1"
    if /i "%%~A"=="--dry-run" set "NO_PAUSE=1"
    if /i "%%~A"=="--help" set "NO_PAUSE=1"
    if /i "%%~A"=="-h" set "NO_PAUSE=1"
)
where.exe node >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is required. Install the repository-supported Node.js runtime.
    set "RESULT=1"
    goto :finished
)
node "%~dp0launch-demo.js" %*
set "RESULT=%ERRORLEVEL%"
:finished
echo.
if not "%RESULT%"=="0" echo Demo failed. Review the error and receipt above.
if not defined NO_PAUSE pause
exit /b %RESULT%
