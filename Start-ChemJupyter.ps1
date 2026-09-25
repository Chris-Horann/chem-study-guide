$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "Starting JupyterLab for ChemStudy..."
py -3.11 -m jupyterlab --port=8889 --IdentityProvider.token=CHEM_TOKEN --ip=127.0.0.1 --no-browser
