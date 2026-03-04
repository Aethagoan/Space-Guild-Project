# Space Guild - WSL Port Forwarding Cleanup
# Run this script as Administrator in PowerShell to remove port forwarding

Write-Host "Space Guild WSL Network Cleanup" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

# Remove port forwarding rules
Write-Host "[*] Removing port forwarding rules..." -ForegroundColor Yellow
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0
netsh interface portproxy delete v4tov4 listenport=8080 listenaddress=0.0.0.0
Write-Host "    Port forwarding removed" -ForegroundColor Green
Write-Host ""

# Remove firewall rules
Write-Host "[*] Removing firewall rules..." -ForegroundColor Yellow
Remove-NetFirewallRule -DisplayName "Space Guild Backend (WSL)" -ErrorAction SilentlyContinue
Remove-NetFirewallRule -DisplayName "Space Guild Frontend (WSL)" -ErrorAction SilentlyContinue
Write-Host "    Firewall rules removed" -ForegroundColor Green
Write-Host ""

Write-Host "Cleanup complete!" -ForegroundColor Green
