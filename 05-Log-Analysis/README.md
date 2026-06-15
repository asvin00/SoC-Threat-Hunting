# Phase 5: Log Analysis 🔎

## Basic Splunk Searching and Analysis

This phase covers fundamental log searching and analysis techniques.

---

## ⏱️ Time Estimate: 1-1.5 hours

---

## 📋 Prerequisites

✅ Splunk running (Phase 2)
✅ Events flowing in (Phase 4)
✅ Can access Splunk Web
✅ Logged in as admin

---

## 🎯 Learning Objectives

After this phase:
- ✅ Write basic Splunk searches
- ✅ Filter by fields
- ✅ Understand field extraction
- ✅ Use stats and timechart
- ✅ Create basic searches

---

## 🚀 Basic Search Syntax

### Search 1: View All Events
```
index=security
```

**What it does**: Shows all events in security index
**Result**: ~1000+ events

---

### Search 2: Failed Logins
```
index=security EventCode=4625
```

**What it does**: Find failed login attempts
**Result**: Events with bad password, account locked, etc.

---

### Search 3: Process Execution
```
index=windows EventCode=1
```

**What it does**: Show all processes that executed
**Result**: Process creation events with Command Line

---

### Search 4: Network Connections
```
index=windows EventCode=3
```

**What it does**: Show network connections from endpoint
**Result**: TCP/UDP connections with IP and port

---

### Search 5: Registry Modifications
```
index=windows EventCode=13
```

**What it does**: Show registry value changes (persistence indicator)
**Result**: Registry path and values changed

---

## 📊 Stats and Analysis

### Count Events by User
```
index=security | stats count by User
```

**Result**:
```
User              count
admin             245
guest             12
system            1890
```

---

### Count by Event ID
```
index=security | stats count by EventCode
```

**Result**:
```
EventCode  count
4624       1200  (successful logon)
4625       45    (failed logon)
4628       12    (group membership)
```

---

### Top Process Names
```
index=windows EventID=1 | stats count by Image | top 10
```

**Result**: Most frequently executed processes

---

### Network Connections by Destination IP
```
index=windows EventID=3 | stats count by DestinationIp
```

**Result**: IPs most connected to

---

## 📈 Timechart (Timeline Analysis)

### Login Attempts Over Time
```
index=security | timechart count by EventCode
```

**Result**: Line graph showing events per hour

---

### Failed Logins by Hour
```
index=security EventCode=4625 | timechart count
```

**Result**: When most failed logins occurred

---

## 🔍 Advanced Filters

### Exclude System Processes
```
index=windows EventID=1 Image!=*system* Image!=*explorer.exe*
```

**Result**: Process events excluding system processes

---

### PowerShell Execution
```
index=windows EventID=1 Image=*powershell.exe*
```

**Result**: Only PowerShell process creation events

---

### Suspicious Command Lines
```
index=windows EventID=1 CommandLine=*wget* OR CommandLine=*curl* OR CommandLine=*whoami*
```

**Result**: Process execution with suspicious commands

---

### Unusual Source IPs
```
index=security EventCode=4624 SourceIP!=192.168.* SourceIP!=10.*
```

**Result**: Logins from non-internal IPs

---

## 💾 Save Searches

**To save a search**:
```
1. Enter search
2. Click search button
3. Click "Save As"
4. Enter name: "Failed Logins Analysis"
5. Owner: Private
6. Click "Save"
```

**To run saved search**:
```
1. Click "Searches" (top menu)
2. Find your saved search
3. Click to run
```

---

## 📋 Common Searches by Use Case

### Incident Response - User Login History
```
index=security user=admin | stats count, earliest, latest by EventCode
```

### Threat Hunting - Suspicious Processes
```
index=windows EventID=1 (Image=*cmd.exe* OR Image=*powershell.exe* OR Image=*regsvcs.exe*)
```

### Compliance - Account Changes
```
index=security EventCode=4720 OR EventCode=4722 OR EventCode=4723
```

### Performance - Top Talkers
```
index=windows EventID=3 | stats count by DestinationIp | sort - count | head 20
```

---

## ✅ Phase 5 Verification Checklist

- ☐ Can search index=security
- ☐ Can search index=windows
- ☐ Found failed login events (EventCode=4625)
- ☐ Found process creation events (EventID=1)
- ☐ Found network connection events (EventID=3)
- ☐ Stats working (count by User)
- ☐ Timechart working (events over time)
- ☐ Can save searches
- ☐ Can filter with WHERE clause
- ☐ Understand field names

---

## 📁 Search Files

See `05-Log-Analysis/` for:
- `basic-searches.txt` - Fundamental searches
- `search-macros.conf` - Reusable search macros
- `field-extractions.conf` - Field extraction rules

---

## 🎓 What You Learned

✅ Basic Splunk search syntax
✅ Field filtering
✅ Stats and aggregation
✅ Timeline analysis
✅ Search saving
✅ Event correlation

---

## ↪️ Next Phase

Phase 6: Detection Engineering

Time to create detection rules! 🚨
