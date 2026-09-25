# Pre-render course PDFs to <pdf-name>_pages\page-NNN.png (incremental: unchanged pages are reused).
# Optional convenience; /ingest-course renders on demand with the same tool.
param(
    [int]$Dpi = 220
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Renderer = Join-Path $Root "tools\render_pdf.py"

$sourceFolders = @(
    (Join-Path $Root "materials\lectures"),
    (Join-Path $Root "materials\review")
)

foreach ($folder in $sourceFolders) {
    Get-ChildItem -Path $folder -Filter *.pdf -File -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host ""
        Write-Host "Rendering $($_.FullName)"
        py -3.11 $Renderer render $_.FullName --dpi $Dpi
    }
}

# Handwritten/scanned notes need more resolution.
Get-ChildItem -Path (Join-Path $Root "materials\notes") -Filter *.pdf -File -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host ""
    Write-Host "Rendering $($_.FullName) at 300 DPI"
    py -3.11 $Renderer render $_.FullName --dpi 300
}
