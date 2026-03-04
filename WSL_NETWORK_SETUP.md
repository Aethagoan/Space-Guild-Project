# Space Guild - WSL Network Setup for LAN Access

This guide explains how to make Space Guild accessible over your local network when running in WSL2.

## The Problem

WSL2 uses a virtualized network adapter with its own IP address. When you run servers in WSL2, they're only accessible from within WSL and from Windows localhost by default. To access them from other devices on your LAN, you need to set up port forwarding.

## Quick Setup (Recommended)

### 1. Run the Setup Script

**In Windows PowerShell (Run as Administrator):**

```powershell
cd C:\Users\xefin\Desktop\Projects\SpaceGuild
.\setup_wsl_network.ps1
```

This script will:
- Detect your WSL IP address
- Detect your Windows LAN IP address
- Set up port forwarding from Windows to WSL
- Configure Windows Firewall
- Display instructions for accessing the game

### 2. Start Your Servers in WSL

```bash
# Start backend
cd SpaceGuildBack
python program.py

# In another terminal, start frontend
cd SpaceGuildWeb
python -m http.server 8080
```

### 3. Access from Other Devices

The script will show you the URL to use. It will look like:
```
http://192.168.1.100:8080/game.html
```

Use this URL from any device on your local network (phones, tablets, other computers).

## Manual Setup

If you prefer to set up manually:

### 1. Get WSL IP Address

In WSL:
```bash
hostname -I
```
Example output: `172.20.10.5`

### 2. Set Up Port Forwarding

In Windows PowerShell (as Administrator):
```powershell
# Replace 172.20.10.5 with your actual WSL IP
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=172.20.10.5
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=172.20.10.5
```

### 3. Configure Windows Firewall

In Windows PowerShell (as Administrator):
```powershell
New-NetFirewallRule -DisplayName "Space Guild Backend (WSL)" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
New-NetFirewallRule -DisplayName "Space Guild Frontend (WSL)" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

### 4. Get Your Windows LAN IP

In Windows PowerShell:
```powershell
ipconfig
```
Look for "IPv4 Address" under your network adapter (usually Ethernet or Wi-Fi).

## Troubleshooting

### Port Forwarding Not Working

Check current port forwarding rules:
```powershell
netsh interface portproxy show v4tov4
```

### WSL IP Changed

WSL IP addresses can change when WSL restarts. If the game stops working:
1. Run `setup_wsl_network.ps1` again as Administrator
2. The script will detect the new WSL IP and update the port forwarding

### Firewall Blocking Connections

Check Windows Firewall rules:
```powershell
Get-NetFirewallRule -DisplayName "Space Guild*"
```

### Can't Access from Other Devices

1. Make sure both devices are on the same network
2. Try pinging your Windows machine from the other device
3. Temporarily disable Windows Firewall to test if it's the issue
4. Check that your router isn't blocking local network communication

## Cleanup

To remove port forwarding and firewall rules:

```powershell
cd C:\Users\xefin\Desktop\Projects\SpaceGuild
.\cleanup_wsl_network.ps1
```

Or manually:
```powershell
# Remove port forwarding
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0
netsh interface portproxy delete v4tov4 listenport=8080 listenaddress=0.0.0.0

# Remove firewall rules
Remove-NetFirewallRule -DisplayName "Space Guild Backend (WSL)"
Remove-NetFirewallRule -DisplayName "Space Guild Frontend (WSL)"
```

## Alternative: WSL Mirrored Mode (Windows 11 22H2+)

If you're on a recent version of Windows 11, you can enable WSL mirrored networking mode which eliminates the need for port forwarding.

Create/edit `C:\Users\xefin\.wslconfig`:
```ini
[wsl2]
networkingMode=mirrored
```

Then restart WSL:
```powershell
wsl --shutdown
```

With mirrored mode, WSL will use the same network interface as Windows, so no port forwarding is needed.

## Notes

- Port forwarding rules persist across reboots
- WSL IP can change, requiring you to run the setup script again
- The frontend (`api.js`) has been configured to auto-detect the backend URL
- Both servers must be running in WSL for this to work
