$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "Starting Claude Code in ChemStudy..."
claude
