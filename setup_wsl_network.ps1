# Space Guild - WSL Port Forwarding Setup
# Run this script as Administrator in PowerShell

Write-Host "Space Guild WSL Network Setup" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Get WSL IP address
Write-Host "[*] Getting WSL IP address..." -ForegroundColor Yellow
$wslIP = wsl hostname -I
$wslIP = $wslIP.Trim()
Write-Host "    WSL IP: $wslIP" -ForegroundColor Green

# Get Windows host IP address
Write-Host "[*] Getting Windows IP address..." -ForegroundColor Yellow
$windowsIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*WSL*" -and $_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"} | Select-Object -First 1).IPAddress
Write-Host "    Windows IP: $windowsIP" -ForegroundColor Green
Write-Host ""

# Remove existing port forwarding rules if they exist
Write-Host "[*] Removing old port forwarding rules (if any)..." -ForegroundColor Yellow
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0 2>$null
netsh interface portproxy delete v4tov4 listenport=8080 listenaddress=0.0.0.0 2>$null

# Add port forwarding rules
Write-Host "[*] Setting up port forwarding..." -ForegroundColor Yellow
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=$wslIP
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=$wslIP
Write-Host "    Port 8000 (Backend): Windows -> WSL" -ForegroundColor Green
Write-Host "    Port 8080 (Frontend): Windows -> WSL" -ForegroundColor Green
Write-Host ""

# Configure Windows Firewall
Write-Host "[*] Configuring Windows Firewall..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "Space Guild Backend (WSL)" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow -ErrorAction SilentlyContinue 2>$null
New-NetFirewallRule -DisplayName "Space Guild Frontend (WSL)" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow -ErrorAction SilentlyContinue 2>$null
Write-Host "    Firewall rules created" -ForegroundColor Green
Write-Host ""

# Display current port forwarding rules
Write-Host "[*] Current port forwarding rules:" -ForegroundColor Yellow
netsh interface portproxy show v4tov4
Write-Host ""

# Show access instructions
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access Space Guild from other devices:" -ForegroundColor Yellow
Write-Host "  http://$windowsIP:8080/game.html" -ForegroundColor White
Write-Host ""
Write-Host "From this computer (Windows):" -ForegroundColor Yellow
Write-Host "  http://localhost:8080/game.html" -ForegroundColor White
Write-Host "  http://$windowsIP:8080/game.html" -ForegroundColor White
Write-Host ""
Write-Host "Note: You need to run this script again if WSL restarts" -ForegroundColor Red
Write-Host "or the WSL IP address changes." -ForegroundColor Red
Write-Host ""
