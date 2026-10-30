@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Reconstruction de la premiere etape avec journalisation et RunOnce.
rem Pas de mot de passe, autologon ni redemarrage force.
set "ROOT=C:\ProgramData\EndpointDeployment"
set "LOGS=%ROOT%\Logs"
set "STATE=%ROOT%\State"
if not exist "%LOGS%" mkdir "%LOGS%"
if not exist "%STATE%" mkdir "%STATE%"
if exist "%STATE%\stage01.ok" exit /b 0

echo [%DATE% %TIME%] Stage 01 demarree>>"%LOGS%\stage01.log"
call "%ROOT%\Scripts\installpackages-example.cmd" >>"%LOGS%\stage01.log" 2>&1
if errorlevel 1 (
  echo [FAIL] Installation des premiers paquets>>"%LOGS%\stage01.log"
  exit /b 10
)
rem HKLM RunOnce se declenche lors du prochain logon administrateur :
rem il ne suffit pas de redemarrer sans ouvrir de session.
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce" ^
 /v EndpointStage02 /t REG_SZ ^
 /d "%ROOT%\Scripts\stage-02.cmd" /f >>"%LOGS%\stage01.log" 2>&1
if errorlevel 1 exit /b 11
>"%STATE%\stage01.ok" echo stage01-success
echo [INFO] Phase suivante enregistree; connexion admin requise.>>"%LOGS%\stage01.log"
endlocal & exit /b 0
