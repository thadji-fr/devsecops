$ErrorActionPreference = 'Stop'
# Exemple fictif de packaging MSI. Aucun installateur ni secret fourni.
$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$msis = @(Get-ChildItem -LiteralPath $toolsDir -Filter '*.msi' -File)
if ($msis.Count -ne 1) {
    throw "Un seul MSI autorise doit etre place dans tools. Presents : $($msis.Count)."
}
$expected = $env:PORTFOLIO_MSI_SHA256
if ($expected -notmatch '^[0-9a-fA-F]{64}$') {
    throw 'PORTFOLIO_MSI_SHA256 doit contenir une empreinte SHA-256 de confiance.'
}
$actual = (Get-FileHash -LiteralPath $msis[0].FullName -Algorithm SHA256).Hash
if ($actual -ine $expected) {
    throw 'Integrite du MSI : empreinte incorrecte.'
}
$packageArgs = @{
    packageName    = 'portfolio-msi-example'
    fileType       = 'msi'
    file           = $msis[0].FullName
    silentArgs     = '/qn /norestart'
    validExitCodes = @(0, 1641, 3010)
}
Install-ChocolateyInstallPackage @packageArgs
