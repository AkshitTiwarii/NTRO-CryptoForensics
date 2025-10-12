@echo off
echo Starting NTRO CryptoForensics System...
echo.

echo 1. Starting Backend Server...
cd /d "C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend"
start "Backend Server" cmd /k "python server.py"

echo.
echo 2. Starting Frontend Server...
cd /d "C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\frontend"
start "Frontend Server" cmd /k "npm start"

echo.
echo System is starting...
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause