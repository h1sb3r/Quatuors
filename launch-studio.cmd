@echo off
setlocal

set "PORT=8081"
set "ROOT=C:\IA\Quatuors"
set "LISTENING_PID="

for /f "tokens=5" %%P in ('netstat -ano ^| findstr /R /C:":%PORT% .*LISTENING"') do (
    set "LISTENING_PID=%%P"
    goto :open_browser
)

start "Quatuors Studio Server (8081)" powershell -NoExit -ExecutionPolicy Bypass -Command "Set-Location -LiteralPath '%ROOT%'; if (Get-Command py -ErrorAction SilentlyContinue) { py server.py %PORT% } elseif (Get-Command python -ErrorAction SilentlyContinue) { python server.py %PORT% } else { Write-Host 'Python introuvable'; Read-Host 'Appuyez sur Entree pour fermer' }"
timeout /t 2 /nobreak >nul

:open_browser
start "" "http://localhost:%PORT%/studio.html"

endlocal
