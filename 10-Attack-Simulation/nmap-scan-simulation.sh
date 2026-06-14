#!/bin/bash
# nmap-scan-simulation.sh
# Simulates network reconnaissance attack

echo "[*] Network Reconnaissance Simulation"
echo "[*] Target: 192.168.56.20"
echo ""

# Install nmap if needed
if ! command -v nmap &> /dev/null; then
    echo "[*] Installing nmap..."
    sudo apt install nmap -y
fi

echo "[*] Running Nmap scan..."
nmap -sV -p 1-10000 192.168.56.20 -v

echo ""
echo "[*] Port scan complete"
echo "[*] Check Splunk for network connection events (EventID=3)"
echo "[*] Search: index=windows EventID=3 DestinationPort=445"
