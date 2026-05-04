$ErrorActionPreference = "Stop"

Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)

New-Item -ItemType Directory -Force -Path "secrets" | Out-Null

Write-Host "Place your Google OAuth desktop client JSON at:"
Write-Host "  secrets\google_oauth_client.json"
Write-Host ""
Write-Host "Then run:"
Write-Host "  python -m src.google_auth_setup"
Write-Host ""

python -m src.setup_check
