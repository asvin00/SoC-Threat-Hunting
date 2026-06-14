# Phase 3: Sysmon Installation 🔍

## Install Windows System Monitoring Agent

This phase installs Sysmon on Windows to capture detailed system events.

---

## ⏱️ Time Estimate: 30-45 minutes

---

## 📋 Prerequisites

✅ Windows VM running (192.168.56.20)
✅ Admin access to Windows
✅ Internet connection
✅ Administrator account

---

## 🎯 Learning Objectives

After this phase:
- ✅ Download Sysmon
- ✅ Download Sysmon configuration
- ✅ Install Sysmon with config
- ✅ Verify Sysmon running
- ✅ View Sysmon events

---

## 🚀 Step-by-Step Installation

### STEP 1: Download Sysmon

```
1. Open Firefox on Windows VM
2. Go to: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
3. Click "Download Sysmon" (sysmon.zip)
4. Save to: C:\Users\admin\Downloads
5. File size: ~2 MB
```

---

### STEP 2: Extract Sysmon

```
1. Open File Explorer
2. Navigate to: C:\Users\admin\Downloads
3. Right-click sysmon.zip → Extract All
4. Extract to: C:\Sysmon
5. Click Extract
```

---

### STEP 3: Download Sysmon Configuration

```
1. Open Firefox
2. Go to: https://github.com/SwiftOnSecurity/sysmon-config
3. Look for: sysmonconfig-export.xml (or download latest)
4. Save to: C:\Sysmon\
```

**What this config does**:
- Filters noisy events
- Focuses on suspicious activity
- Optimizes for security analysis

---

### STEP 4: Open Command Prompt (Admin)

```
1. Right-click Start menu
2. Select: Command Prompt (Admin)
   OR
3. Search for "cmd" → Right-click → Run as Administrator
```

---

### STEP 5: Navigate to Sysmon Directory

```bash
cd C:\Sysmon
dir

# Should show:
# sysmon.exe
# sysmonconfig-export.xml
# README (if included)
```

---

### STEP 6: Install Sysmon

```bash
sysmon.exe -accepteula -i sysmonconfig-export.xml

# Expected output:
# Sysmon installed.
# EventLog entry for Sysmon has been created.
# System monitoring started.
```

---

### STEP 7: Verify Sysmon Running

**Method 1: Task Manager**
```
1. Press Ctrl+Shift+Esc
2. Click "Processes" tab
3. Look for: sysmon.exe
4. Should show: "Running"
```

**Method 2: Command Prompt**
```bash
tasklist | find "sysmon"

# Expected: sysmon.exe [PID]
```

---

### STEP 8: Generate Test Events

```powershell
# Open PowerShell (Admin)

ipconfig /all
systeminfo
Get-Process
netstat -ano
whoami
```

These commands create Sysmon log entries.

---

### STEP 9: View Sysmon Events in Event Viewer

```
1. Press Windows+R
2. Type: eventvwr.msc
3. Click OK
4. Navigate to: Applications and Services Logs → Microsoft → Windows → Sysmon → Operational
5. You should see events with Event IDs:
   - 1 (Process Create)
   - 3 (Network Connection)
   - 8 (CreateRemoteThread)
   - etc.
```

---

## 📊 Sysmon Event IDs Reference

| Event ID | Event Name | Description |
|----------|-----------|-------------|
| 1 | Process created | When a process is started |
| 2 | A process changed a file creation time | File timestamp altered |
| 3 | Network connection detected | TCP/UDP connection |
| 4 | Sysmon service state changed | Sysmon started/stopped |
| 5 | Process terminated | Process ended |
| 6 | Driver loaded | Kernel driver loaded |
| 7 | Image loaded | DLL/library loaded |
| 8 | CreateRemoteThread detected | Code injection |
| 9 | RawAccessRead detected | Disk read |
| 10 | Process accessed | One process access another |
| 11 | File created | File written to disk |
| 12 | Registry object added/deleted | Registry key created |
| 13 | Registry value set | Registry value changed |
| 14 | Registry object renamed | Registry key renamed |
| 15 | FileStream detected | Alternate data stream |
| 17 | Pipe created | Named pipe |
| 18 | Pipe connected | Pipe connection |
| 19 | WmiEvent - WmiEventFilter | WMI event filter |
| 20 | WmiEvent - WmiEventConsumer | WMI event consumer |
| 21 | WmiEvent - WmiEventConsumerToFilter | WMI binding |
| 22 | DNSQuery detected | DNS query |
| 23 | FileExecutableDetected | Executable accessed |
| 24 | ClipboardChange detected | Clipboard data |
| 25 | ProcessTampering detected | Process tampering |
| 26 | HardLinkCreated | Hard link created |
| 27 | ObjectAce | Access control list |
| 28 | RawAccessThreadDetected | Raw access thread |

---

## ✅ Phase 3 Verification Checklist

- ☐ Sysmon downloaded to C:\Sysmon
- ☐ sysmonconfig-export.xml downloaded
- ☐ Sysmon installed: `sysmon.exe -accepteula -i sysmonconfig-export.xml`
- ☐ sysmon.exe showing in Task Manager
- ☐ sysmon.exe in tasklist output
- ☐ Event Viewer shows Sysmon → Operational
- ☐ Event IDs visible (1, 3, 8, etc.)
- ☐ Test commands generated events
- ☐ DNS query events showing (EventID 22)
- ☐ Process creation events showing (EventID 1)

---

## 🔧 Troubleshooting

### Sysmon not installed
```
✅ Verify you ran as Administrator
✅ Verify sysmonconfig-export.xml in same directory
✅ Check file permissions
✅ Try: sysmon.exe -? (to see help)
```

### Can't see Sysmon events
```
✅ Generate test events: ipconfig, systeminfo
✅ Wait 30 seconds
✅ Refresh Event Viewer
✅ Check correct event log: Sysmon → Operational
```

### Need to reinstall
```bash
# Uninstall first
sysmon.exe -u

# Then reinstall
sysmon.exe -accepteula -i sysmonconfig-export.xml
```

---

## 📁 Configuration Files

See `03-Sysmon-Installation/` for:
- `sysmonconfig-export.xml` - Sysmon configuration
- `sysmon-install.ps1` - PowerShell install script

---

## 🎓 What You Learned

✅ Sysmon installation process
✅ Sysmon event IDs and meanings
✅ Event Viewer navigation
✅ System monitoring basics
✅ Event generation for testing

---

## ↪️ Next Phase

Phase 4: Splunk Universal Forwarder

Time to connect Windows to Splunk! 🚀