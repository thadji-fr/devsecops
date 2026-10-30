# Reconstitution documentaire en lecture seule.
# La presence d'un paquet ne prouve pas, seule, la correction d'une CVE.
$ErrorActionPreference = 'Stop'
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    throw 'Chocolatey non disponible sur cet hote.'
}
$wanted = @('7zip.install', 'firefox', 'thunderbird', 'irfanview')
$lines = & choco list --limit-output 2>&1
if ($LASTEXITCODE -ne 0) { throw "Inventaire Chocolatey en echec : $lines" }
$found = @{}
foreach ($line in $lines) {
    if ($line -match '^([^|]+)\|(.+)$') {
        $found[$matches[1].ToLowerInvariant()] = $matches[2]
    }
}
$wanted | ForEach-Object {
    [pscustomobject]@{
        Package = $_
        Version = $found[$_]
        Present = $found.ContainsKey($_)
    }
} | Format-Table -AutoSize
# Verifier les options de choco list selon la version de Chocolatey.
