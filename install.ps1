# Install the skills in this repo into the Claude Code personal skills directory.
# Usage (PowerShell): .\install.ps1
# ASCII-only on purpose: Windows PowerShell 5.1 reads UTF-8 without BOM as ANSI.
$ErrorActionPreference = "Stop"
$src = $PSScriptRoot
$dst = Join-Path $env:USERPROFILE ".claude\skills"
New-Item -ItemType Directory -Force -Path $dst | Out-Null

$skills = @(
    "weekly-kpi-email",
    "document-flow-audit",
    "rule-based-data-audit",
    "receivables-dashboard",
    "sales-performance-analysis",
    "business-review-deck"
)

foreach ($s in $skills) {
    $from = Join-Path $src $s
    if (-not (Test-Path $from)) { Write-Warning "Skip (missing): $s"; continue }
    $to = Join-Path $dst $s
    if (Test-Path $to) {
        Write-Host "Exists, overwriting: $to"
        Remove-Item $to -Recurse -Force
    }
    Copy-Item $from $to -Recurse
    Write-Host "Installed: $s"
}

Write-Host ""
Write-Host "Done. Run /reload-skills or restart Claude Code, then /skills." -ForegroundColor Green
