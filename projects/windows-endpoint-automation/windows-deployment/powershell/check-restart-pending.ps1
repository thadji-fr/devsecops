# Controle non destructif d'indicateurs de redemarrage Windows.
$ErrorActionPreference = 'Stop'
$paths = @(
  'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending',
  'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
)
$pending = @($paths | Where-Object { Test-Path -LiteralPath $_ })
$renames = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name 'PendingFileRenameOperations' -ErrorAction SilentlyContinue
[pscustomobject]@{
  RebootPending = ($pending.Count -gt 0 -or $null -ne $renames)
  Sources = ($pending -join ', ')
  CheckedAt = Get-Date
}
