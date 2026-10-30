@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Post-installation : applications, profil optionnel, pilotes (si fournis).
rem Reconstitution anonymisee de la deuxieme vague Windows 10/11.
set "ROOT=C:\ProgramData\EndpointDeployment"
set "LOGS=%ROOT%\Logs"
set "STATE=%ROOT%\State"
if not exist "%LOGS%" mkdir "%LOGS%"
if not exist "%STATE%" mkdir "%STATE%"
if exist "%STATE%\stage02.ok" exit /b 0
if not exist "%STATE%\stage01.ok" exit /b 20
where choco.exe >nul 2>&1
if errorlevel 1 exit /b 127

echo [%DATE% %TIME%] Stage02 BEGIN>>"%LOGS%\stage02.log"
choco upgrade irfanview -y --no-progress --params="/desktop=1 /assoc=1 /group=1" >>"%LOGS%\stage02.log" 2>&1
if errorlevel 1 exit /b 21
choco upgrade irfanviewplugins -y --no-progress >>"%LOGS%\stage02.log" 2>&1
if errorlevel 1 exit /b 22

rem Anciennement selection par parametres reseau : ici profil explicite.
if /I "%DEPLOY_PROFILE%"=="lab" (
 call "%ROOT%\Scripts\profile-apps-example.cmd" >>"%LOGS%\stage02.log" 2>&1
 if errorlevel 1 exit /b 23
)

rem Salt Minion est installe pendant la preparation Windows 11.
rem La configuration du Salt Master (adresse, certificats, cle) est
rem separee de ce script public pour proteger l'environnement d'origine.
choco install saltminion --yes --no-progress >>"%LOGS%\stage02.log" 2>&1
if errorlevel 1 exit /b 25

rem Extraction de pilotes + dpinst64.exe observee dans la chaine source.
rem Le binaire et les pilotes ne sont jamais distribues dans ce depot.
if exist "%ROOT%\Drivers\dpinst64.exe" (
 pushd "%ROOT%\Drivers"
 start "" /wait dpinst64.exe /q /f /se >>"%LOGS%\stage02.log" 2>&1
 if errorlevel 1 (
  popd
  exit /b 24
 )
 popd
) else (
 echo [SKIP] Pilotes absents du laboratoire>>"%LOGS%\stage02.log"
)
>"%STATE%\stage02.ok" echo stage02-success
echo [%DATE% %TIME%] Stage02 END>>"%LOGS%\stage02.log"
endlocal & exit /b 0
