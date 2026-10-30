@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Les scripts initiaux faisaient des installations conditionnelles.
rem Le profil de demonstration ne reproduit aucun sous-reseau.
if /I not "%DEPLOY_PROFILE%"=="lab" exit /b 0
where choco.exe >nul 2>&1
if errorlevel 1 exit /b 127
echo [INFO] Profil laboratoire : installation complementaire
choco upgrade ltspice --yes --no-progress
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" exit /b %RC%
endlocal & exit /b 0
