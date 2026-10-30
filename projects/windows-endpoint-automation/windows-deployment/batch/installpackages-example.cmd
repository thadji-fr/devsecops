@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Reconstitution de la premiere vague Windows 10/11.
rem Chocolatey doit etre preinstalle, configure et teste en laboratoire.
set "ROOT=C:\ProgramData\EndpointDeployment"
set "LOGS=%ROOT%\Logs"
set "STATE=%ROOT%\State"
if not exist "%LOGS%" mkdir "%LOGS%"
if not exist "%STATE%" mkdir "%STATE%"
where choco.exe >nul 2>&1
if errorlevel 1 (
 echo [FAIL] Chocolatey absent>>"%LOGS%\packages.log"
 exit /b 127
)
set "REBOOT_PENDING=0"
for %%P in (7zip.install firefox thunderbird) do (
 call :INSTALL "%%P"
 if errorlevel 1 exit /b 10
)
if "%REBOOT_PENDING%"=="1" >"%STATE%\reboot-required.txt" echo Reboot requis
echo [OK] Premiere vague terminee>>"%LOGS%\packages.log"
endlocal & exit /b 0

:INSTALL
echo [%DATE% %TIME%] Installation de %~1>>"%LOGS%\packages.log"
choco upgrade "%~1" --yes --no-progress >>"%LOGS%\packages.log" 2>&1
set "RC=%ERRORLEVEL%"
if "%RC%"=="0" exit /b 0
if "%RC%"=="3010" (
 echo [WARN] %~1 signale un redemarrage (3010)>>"%LOGS%\packages.log"
 set "REBOOT_PENDING=1"
 exit /b 0
)
echo [FAIL] %~1 retourne %RC%>>"%LOGS%\packages.log"
exit /b 1
