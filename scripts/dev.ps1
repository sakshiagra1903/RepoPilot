$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
if (!(Test-Path (Join-Path $Backend ".env"))) { Copy-Item (Join-Path $Backend ".env.example") (Join-Path $Backend ".env") }
if (!(Test-Path (Join-Path $Backend ".venv"))) { py -3.12 -m venv (Join-Path $Backend ".venv") }
$Py = Join-Path $Backend ".venv\Scripts\python.exe"
& $Py -m pip install --upgrade pip
& $Py -m pip install -r (Join-Path $Backend "requirements.txt")
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Backend'; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload"
Set-Location $Frontend
if (!(Test-Path "node_modules")) { npm install }
Write-Host "Starting RepoPilot frontend at http://localhost:5173" -ForegroundColor Yellow
npm run dev
