@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Exemple anonymise d'une source Chocolatey.
rem URL en .invalid, sans authentification ni donnees internes.
set "SOURCE_NAME=portfolio-demo"
set "SOURCE_URL=https://packages.example.invalid/chocolatey/"
where choco.exe >nul 2>&1
if errorlevel 1 exit /b 127
choco source list --limit-output
rem Ne pas supprimer les sources existantes sans validation.
choco source add --name="%SOURCE_NAME%" --source="%SOURCE_URL%" --priority=1
exit /b %ERRORLEVEL%
