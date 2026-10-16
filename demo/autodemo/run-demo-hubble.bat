@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run-demo-hubble.ps1"
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" echo Hubble enterprise demonstration failed. Review the error above.
pause
exit /b %RESULT%
