#!/usr/bin/env pwsh
# Quick restart script for backend server

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "    Restarting Backend Server" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Stop any running Python processes
Write-Host "[1/2] Stopping existing Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Start backend server
Write-Host "[2/2] Starting backend server..." -ForegroundColor Yellow
Set-Location "C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend"
python server.py
