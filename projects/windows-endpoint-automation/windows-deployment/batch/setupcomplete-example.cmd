@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Reconstruction de SetupComplete. La copie initiale des scripts est
rem indispensable et doit etre effectuee par un staging distinct.
set "ROOT=C:\ProgramData\EndpointDeployment"
set "LOGS=%ROOT%\Logs"
if not exist "%LOGS%" mkdir "%LOGS%"
if not exist "%ROOT%\Scripts\stage-01.cmd" (
  echo [FAIL] stage-01 introuvable>>"%LOGS%\setupcomplete.log"
  exit /b 2
)
echo [%DATE% %TIME%] BEGIN SetupComplete>>"%LOGS%\setupcomplete.log"
call "%ROOT%\Scripts\stage-01.cmd" >>"%LOGS%\setupcomplete.log" 2>&1
set "RC=%ERRORLEVEL%"
echo [%DATE% %TIME%] END SetupComplete RC=%RC%>>"%LOGS%\setupcomplete.log"
endlocal & exit /b %RC%
