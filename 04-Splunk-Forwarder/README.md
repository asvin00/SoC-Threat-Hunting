# Phase 4: Splunk Universal Forwarder 📤

## Install & Configure Log Forwarding Agent

This phase installs the Splunk forwarder on Windows to send logs to Splunk.

---

## ⏱️ Time Estimate: 45 minutes

---

## 📋 Prerequisites

✅ Windows VM running (192.168.56.20)
✅ Sysmon installed (Phase 3)
✅ Splunk running on Ubuntu (192.168.56.10)
✅ Admin access to Windows
✅ Network connectivity (ping 192.168.56.10 from Windows)

---

## 🎯 Learning Objectives

After this phase:
- ✅ Download Universal Forwarder
- ✅ Install forwarder on Windows
- ✅ Configure log inputs
- ✅ Configure Splunk output
- ✅ Verify logs flowing to Splunk

---

## 🚀 Step-by-Step Installation

### STEP 1: Test Network Connectivity

```powershell
# Open PowerShell on Windows

ping 192.168.56.10

# Expected:
# Reply from 192.168.56.10: bytes=32 time=5ms TTL=64
```

If ping fails, fix Windows network (see Phase 1 troubleshooting).

---

### STEP 2: Download Universal Forwarder

```
1. Open Firefox on Windows
2. Go to: https://www.splunk.com/en_us/download/universal-forwarder.html
3. Download: "Windows 64-bit" (.msi file)
4. Save to: C:\Users\admin\Downloads
5. File: splunk-9.x.x-windows-64-release.msi (~400 MB)
```

**Time**: ~10-15 minutes

---

### STEP 3: Install Universal Forwarder

```
1. Navigate to: C:\Users\admin\Downloads
2. Double-click: splunk-xxx-windows-64-release.msi
3. Click "Next"
4. Accept license agreement
5. Click "Next"

When asked for Splunk server:
  Receiving indexer: 192.168.56.10:9997
  
When asked for username/password:
  Username: admin
  Password: Splunk@123
  
6. Click "Next" → "Finish"
7. Wait for installation (~5 minutes)
```

---

### STEP 4: Verify Forwarder Service

```powershell
# Open PowerShell (Admin)

Get-Service SplunkForwarder

# Expected output:
Status   Name                DisplayName
------   ----                -----------
Running  SplunkForwarder     SplunkForwarder
```

If not running:
```powershell
Start-Service SplunkForwarder
```

---

### STEP 5: Configure Data Inputs

```powershell
# Open PowerShell (Admin)

cd "C:\Program Files\SplunkUniversalForwarder\bin"

# Add forward server
.\splunk.exe add forward-server 192.168.56.10:9997 \
  -auth admin:Splunk@123
```

---

### STEP 6: Monitor Windows Security Log

```powershell
# In same PowerShell window:

.\splunk.exe add monitor "C:\Windows\System32\winevt\Logs\Security.evtx" \
  -index security \
  -auth admin:Splunk@123
```

---

### STEP 7: Monitor Windows Application Log (Sysmon)

```powershell
.\splunk.exe add monitor "C:\Windows\System32\winevt\Logs\Application.evtx" \
  -index windows \
  -auth admin:Splunk@123
```

---

### STEP 8: Monitor Windows System Log

```powershell
.\splunk.exe add monitor "C:\Windows\System32\winevt\Logs\System.evtx" \
  -index windows \
  -auth admin:Splunk@123
```

---

### STEP 9: Restart Forwarder Service

```powershell
Restart-Service SplunkForwarder

# Wait 30 seconds

Get-Service SplunkForwarder
# Should show: Running
```

---

### STEP 10: Verify Data Flow in Splunk

**On Ubuntu (Splunk Server)**:

```
1. Open Splunk Web: https://localhost:8000
2. Click "Search & Reporting"
3. In search box, enter:
   index=security OR index=windows
4. Click search (or press Enter)
5. Wait 1-2 minutes
6. Refresh search
7. Should show events arriving from Windows!
```

---

## 📊 Verify Events Arriving

**Method 1: Count Events**
```
Search: index=security OR index=windows | stats count

Expected: count > 0 (should show events)
```

**Method 2: View by Index**
```
Search: index=security | head 10

Should show security events with:
- EventID: 4624, 4625, etc.
- User, Computer, Source IP
```

**Method 3: View Sysmon Events**
```
Search: index=windows EventID=1

Should show process creation events
```

---

## ✅ Phase 4 Verification Checklist

- ☐ Universal Forwarder downloaded (~400 MB)
- ☐ Forwarder installed on Windows
- ☐ Forward-server configured: 192.168.56.10:9997
- ☐ SplunkForwarder service running
- ☐ Security.evtx monitored (index=security)
- ☐ Application.evtx monitored (index=windows)
- ☐ System.evtx monitored (index=windows)
- ☐ Events visible in Splunk (index=security OR index=windows)
- ☐ Process events visible (EventID=1)
- ☐ Security events visible (EventID=4624, 4625)

---

## 🔧 Troubleshooting

### Forwarder not sending logs
```
✅ Verify network: ping 192.168.56.10 from Windows
✅ Check service: Get-Service SplunkForwarder
✅ Restart service: Restart-Service SplunkForwarder
✅ Wait 2 minutes
✅ Refresh Splunk search
```

### Port 9997 not reachable
```powershell
# Test from Windows:
Test-NetConnection 192.168.56.10 -Port 9997

# Should show: TcpTestSucceeded : True

# If fails, check Splunk firewall on Ubuntu:
sudo ufw allow 9997
```

### Can't find log files
```bash
# Verify on Windows:
dir "C:\Windows\System32\winevt\Logs\Security.evtx"

# Must return: Security.evtx file exists
```

---

## 📁 Configuration Files

See `04-Splunk-Forwarder/` for:
- `forwarder-install.ps1` - PowerShell install script
- `inputs.conf` - Log input configuration
- `outputs.conf` - Output configuration

---

## 🎓 What You Learned

✅ Universal Forwarder installation
✅ Data input configuration
✅ Index routing
✅ Encryption and authentication
✅ Service management on Windows
✅ Log verification in Splunk

---

## ↪️ Next Phase

Phase 5: Log Analysis

Time to search and analyze logs! 🔍