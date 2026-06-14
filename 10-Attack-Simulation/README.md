# Phase 10: Attack Simulation 🎯

## Validate Detection Rules with Simulated Attacks

This phase involves simulating real-world attacks to test your detection rules.

---

## ⏱️ Time Estimate: 1-1.5 hours

---

## 📋 Prerequisites

✅ Phases 1-9 complete
✅ Detection rules created
✅ Dashboards deployed
✅ All three VMs running
✅ Network connectivity verified

---

## 🎯 Learning Objectives

After this phase:
- ✅ Simulate brute-force attacks
- ✅ Simulate network reconnaissance
- ✅ Simulate process execution
- ✅ Trigger detection rules
- ✅ Validate detection effectiveness
- ✅ Understand false positives

---

## 🚀 Attack Simulation 1: Brute Force (Kali → Windows)

**Goal**: Generate failed login events to trigger detection rule

### From Kali Linux:

```bash
# Install Hydra (if not already installed)
sudo apt install hydra -y

# Create password list
echo -e "password1\npassword2\nwrongpass" > /tmp/wordlist.txt

# Run brute-force attack
hydra -l admin -P /tmp/wordlist.txt 192.168.56.20 smb -v

# Expected output:
# [139][smb] host: 192.168.56.20   login: admin   password: (wrong passwords)
# Multiple connection attempts
```

### Verify in Splunk:

```
1. Go to Splunk Web
2. Search: index=security EventCode=4625 | stats count
3. Should show: count > 5 (multiple failed logins)
4. Check Dashboard: Alert should trigger
```

**Screenshot concept:**
```
┌─ Splunk Dashboard ─────────────────────────┐
│                                            │
│ 🔴 ALERT: Brute Force Detected             │
│ ├─ Source IP: 192.168.56.30               │
│ ├─ Failed Attempts: 8                      │
│ ├─ Target: admin (192.168.56.20)          │
│ └─ Time: 2025-06-14 12:30:45              │
│                                            │
│ [Details] [Investigate] [Close]            │
└────────────────────────────────────────────┘
```

---

## 🚀 Attack Simulation 2: Network Scan (Kali → Windows)

**Goal**: Generate network events and reconnaissance indicators

### From Kali Linux:

```bash
# Install Nmap (if not already installed)
sudo apt install nmap -y

# Run network scan
nmap -sV -p 1-10000 192.168.56.20 -v

# Expected output:
# Nmap scan report for 192.168.56.20
# PORT      STATE SERVICE
# 445/tcp   open  microsoft-ds
# 3389/tcp  open  ms-wbt-server
# Multiple ports showing open services
```

### Verify in Splunk:

```
1. Search: index=windows EventID=3 DestinationPort=445
2. Should show: Network connections on SMB port
3. Search: index=windows EventID=3 | stats dc(DestinationPort) by Computer
4. Should show: Multiple ports connected
```

---

## 🚀 Attack Simulation 3: Process Execution (Windows)

**Goal**: Create process execution events for detection

### On Windows (PowerShell as Admin):

```powershell
# Generate process execution events
Get-Process
ipconfig /all
systeminfo
whoami
net user
net view

# Generate PowerShell events
powershell.exe -Command "Get-ChildItem C:\\"
powershell.exe -Command "Get-Process | Out-File C:\\temp.txt"

# Generate cmd execution
cmd.exe /c "ipconfig /all"
```

### Verify in Splunk:

```
1. Search: index=windows EventID=1 Image=*powershell.exe*
2. Should show: Multiple PowerShell executions
3. Search: index=windows EventID=1 CommandLine=*whoami*
4. Should show: Process with whoami command
```

---

## 🚀 Attack Simulation 4: Registry Modification (Windows)

**Goal**: Create persistence indicator

### On Windows (PowerShell as Admin):

```powershell
# Create registry entry (simulating persistence)
New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "TestKey" -Value "C:\\test.exe" -Force

# Modify registry
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "TestKey" -Value "C:\\malware.exe"

# View registry
Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
```

### Verify in Splunk:

```
1. Search: index=windows EventID=13 TargetObject=*\\Run\\*
2. Should show: Registry modifications
3. Look for: TestKey, malware.exe
```

---

## 🚀 Attack Simulation 5: Data Exfiltration (Kali)

**Goal**: Simulate outbound data transfer

### From Kali Linux:

```bash
# Start simple HTTP server to simulate C&C
cd /tmp
python3 -m http.server 8888 &

# From Windows, download large file
# (Simulate data exfiltration)

# You can also use:
curl http://192.168.56.30:8888/largefile -o output.bin
```

### Verify in Splunk:

```
1. Search: index=windows EventID=3 DestinationIp=192.168.56.30
2. Should show: Connections to Kali
3. Look for: Port 8888
```

---

## ✅ Detection Validation Checklist

**After each simulation:**

- ✅ Events appear in Splunk within 1 minute
- ✅ Detection rule triggers alert
- ✅ Alert appears on dashboard
- ✅ Can see raw event data
- ✅ Can follow event chain
- ✅ Can identify threat actor actions

---

## 📊 Detection Effectiveness Report

| Attack Type | Detection Rule | Triggered | Time-to-Alert | False Positives |
|------------|----------------|-----------|---------------|-----------------|
| Brute Force | Rule 1 | ✅ Yes | 30 sec | Low |
| Network Recon | Rule 4 | ✅ Yes | 15 sec | Medium |
| Process Exec | Rule 2 | ✅ Yes | 5 sec | High |
| Registry Mod | (need rule) | ❌ No | N/A | N/A |
| Credential Dump | Rule 5 | ✅ Yes | 10 sec | Low |
| Lateral Move | Rule 6 | ✅ Yes | 20 sec | Low |

**Overall Detection Rate: 83%**

---

## 🎯 Create Incident from Simulation

**For each attack:**

```
1. Record start time of attack
2. Run attack simulation
3. Note when alert triggers
4. Calculate time-to-detection
5. Document findings:
   - What was detected
   - What was missed
   - False positives generated
   - Improvement areas
```

---

## ✅ Phase 10 Verification Checklist

- ✅ Brute-force attack simulated
- ✅ Network scan simulated
- ✅ Process execution events generated
- ✅ Registry modifications created
- ✅ All events visible in Splunk
- ✅ Detection rules triggered by attacks
- ✅ Alerts appeared on dashboard
- ✅ Time-to-detection measured
- ✅ False positives identified
- ✅ Detection effectiveness documented

---

## 📁 Files in This Phase

See `10-Attack-Simulation/` for:
- `brute-force-simulation.sh` - Hydra script
- `nmap-scan-simulation.sh` - Network scan script
- `process-execution-test.ps1` - Process generation script
- `validation-checklist.md` - Testing checklist

---

## 🎓 What You Learned

✅ Attack simulation techniques
✅ Detection validation methods
✅ Time-to-detection measurement
✅ False positive identification
✅ Effectiveness assessment
✅ Incident creation

---

## ⬅️ Next Phase

Phase 11: Python Automation

Time to automate security tasks! 🐍