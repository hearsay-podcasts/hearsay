#!/usr/bin/env pwsh

# Hearsay Development Startup Script for Windows
# This script starts the PostgreSQL database, backend API, and frontend server

Write-Host "Starting Hearsay Development Environment..." -ForegroundColor Cyan

# Check if Docker is running
try {
    docker ps > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Start PostgreSQL database using Docker Compose
Write-Host "`nStarting PostgreSQL database..." -ForegroundColor Yellow
docker compose up -d

# Function to cleanup processes on script exit
$backendProcess = $null
$frontendProcess = $null

$cleanup = {
    Write-Host "`nStopping all processes..." -ForegroundColor Yellow
    if ($backendProcess) { Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue }
    if ($frontendProcess) { Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue }
    Write-Host "All processes stopped." -ForegroundColor Green
}

# Register cleanup on script exit (Ctrl+C)
trap {
    & $cleanup
    exit
}

# Start Backend
Write-Host "`nStarting Backend (FastAPI)..." -ForegroundColor Yellow
$backendDir = Join-Path $PSScriptRoot "backend"
if (!(Test-Path $backendDir)) {
    Write-Host "Error: Backend directory not found at $backendDir" -ForegroundColor Red
    exit 1
}

$backendScript = {
    param($Path)
    Set-Location $Path
    uv run uvicorn app.main:app --reload
}

$backendProcess = Start-Job -ScriptBlock $backendScript -ArgumentList $backendDir
$backendJobId = $backendProcess.Id
Write-Host "Backend starting on http://localhost:8000" -ForegroundColor Green

# Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "`nStarting Frontend (SvelteKit)..." -ForegroundColor Yellow
$frontendDir = Join-Path $PSScriptRoot "web"
if (!(Test-Path $frontendDir)) {
    Write-Host "Error: Frontend directory not found at $frontendDir" -ForegroundColor Red
    exit 1
}

$frontendScript = {
    param($Path)
    Set-Location $Path
    pnpm dev
}

$frontendProcess = Start-Job -ScriptBlock $frontendScript -ArgumentList $frontendDir
Write-Host "Frontend starting on http://localhost:5173" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Hearsay Development Environment Started!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "Frontend:     http://localhost:5173" -ForegroundColor White
Write-Host "`nPress Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Keep script running and monitor jobs
try {
    while ($backendProcess.State -eq "Running" -and $frontendProcess.State -eq "Running") {
        Start-Sleep -Seconds 1

        # Check for job errors
        if ($backendProcess.State -eq "Failed") {
            Write-Host "`nBackend process failed!" -ForegroundColor Red
            Receive-Job -Job $backendProcess | Write-Host
            break
        }
        if ($frontendProcess.State -eq "Failed") {
            Write-Host "`nFrontend process failed!" -ForegroundColor Red
            Receive-Job -Job $frontendProcess | Write-Host
            break
        }
    }
} finally {
    & $cleanup
}
