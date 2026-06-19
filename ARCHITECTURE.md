# 🏗️ SOC & Threat Hunting Platform - Architecture

## System Architecture Overview

### Network Topology

```
┌────────────────────────────────────────────────────────────────┐
│                 HOST MACHINE (Your Computer)                   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            VirtualBox Environment                        │   │
│  │         Network: 192.168.56.0/24 (Host-Only)           │   │
│  │                                                          │   │
│  │  ┌──────────────────────┐    ┌────────��────────────┐   │   │
│  │  │   UBUNTU 26.04       │    │   WINDOWS 11        │   │   │
│  │  │   192.168.56.10      │◄───│   192.168.56.20     │   │   │
│  │  │                      │    │                     │   │   │
│  │  │  ┌────────────────┐  │    │  ┌─────────────────┐│   │   │
│  │  │  │  Splunk SIEM   │  │    │  │ Sysmon          ││   │   │
│  │  │  │  Port 8000     │  │    │  │ (Monitoring)    ││   │   │
│  │  │  │                │  │    │  │                 ││   │   │
│  │  │  │  Indexes:      │  │    │  │ Splunk          ││   │   │
│  │  │  │  • security    │  │    │  │ Forwarder       ││   │   │
│  │  │  │  • windows     │  │    │  │ (Forwarding)    ││   │   │
│  │  │  │  • main        │  │    │  │ Port 9997 →     ││   │   │
│  │  │  │  • sysmon      │  │    │  │ 192.168.56.10   ││   │   │
│  │  │  │                │  │    │  │ 9997            ││   │   │
│  │  │  │  Receiving:    │  │    │  │                 ││   │   │
│  │  │  │  Port 9997     │  │    │  └─────────────────┘│   │   │
│  │  │  └────────────────┘  │    │                     │   │   │
│  │  │  ┌────────────────┐  │    │  Security Logs:     │   │   │
│  │  │  │  Web UI        │  │    │  • Event IDs        │   │   │
│  │  │  │  Port 8000     │  │    │  • Sysmon Events    │   │   │
│  │  │  │  (Analysis)    │  │    │  • Process Create   │   │   │
│  │  │  └────────────────┘  │    │  • Network Conn     │   │   │
│  │  │                      │    │  • File Operations  │   │   │
│  │  └──────────────────────┘    └─────────────────────┘   │   │
│  │         ▲                                                 │   │
│  │         │                                                 │   │
│  │  ┌──────┴──────────────────┐                            │   │
│  │  │   KALI LINUX            │                            │   │
│  │  │   192.168.56.30         │                            │   │
│  │  │                         │                            │   │
│  │  │  • Nmap (scanning)      │                            │   │
│  │  │  • Hydra (brute force)  │                            │   │
│  │  │  • Metasploit (attacks) │                            │   │
│  │  │  • Attack Simulation    │                            │   │
│  │  └─────────────────────────┘                            │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Architecture

### Log Collection Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│              ENDPOINT (Windows 192.168.56.20)                │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           SECURITY EVENT GENERATION                 │    │
│  │                                                     │    │
│  │  • Process Execution (cmd.exe, PowerShell)        │    │
│  │  • Network Connections (SMB, RDP, DNS)            │    │
│  │  • File Operations (Creation, Modification)       │    │
│  │  • Registry Changes (Persistence Mechanisms)      │    │
│  │  • Login Attempts (Success/Failure)               │    │
│  │  • Account Changes (New users, group changes)     │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            SYSMON MONITORING                        │    │
│  │  (Detailed endpoint activity tracking)             │    │
│  │                                                     │    │
│  │  Event Types:                                       │    │
│  │  • EventID 1: Process Create                       │    │
│  │  • EventID 3: Network Connection                   │    │
│  │  • EventID 5: Process Terminated                   │    │
│  │  • EventID 8: CreateRemoteThread                   │    │
│  │  • EventID 10: ProcessAccess (LSASS)              │    │
│  │  • EventID 11: FileCreate                          │    │
│  │  • EventID 13: RegistrySet                         │    │
│  │  • EventID 21: WmiEvent                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         WINDOWS EVENT LOGS                          │    │
│  │  (Centralized event log storage)                   │    │
│  │                                                     │    │
│  │  • Security.evtx (10,000+ events/day)             │    │
│  │  • Application.evtx (Sysmon events)               │    │
│  │  • System.evtx (System events)                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │     SPLUNK UNIVERSAL FORWARDER                      │    │
│  │  (Log collection & transmission agent)             │    │
│  │                                                     │    │
│  │  Function: Collect → Transform → Forward           │    │
│  │  Inputs:                                            │    │
│  │  • C:\Windows\System32\winevt\Logs\Security.evtx  │    │
│  │  • C:\Windows\System32\winevt\Logs\Application.evtx│   │
│  │  • C:\Windows\System32\winevt\Logs\System.evtx    │    │
│  │                                                     │    │
│  │  Connection: TCP 9997 to 192.168.56.10            │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                   Network Transmission
                   TCP 9997 (encrypted)
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│          SPLUNK INDEXER (Ubuntu 192.168.56.10)                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │      SPLUNK RECEIVING AGENT (Port 9997)              │    │
│  │  (Accepts incoming log streams)                      │    │
│  └──────────────────────────────────────────────────────┘    │
│                            │                                  │
│                            ▼                                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │       DATA PARSING & INDEXING                        │    │
│  │                                                      │    │
│  │  • Parse raw log data                              │    │
│  │  • Extract fields (host, source, sourcetype)       │    │
│  │  • Timestamp normalization                         │    │
│  │  • Field extraction                                │    │
│  └──────────────────────────────────────────────────────┘    │
│                            │                                  │
│                            ▼                                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         INDEX STORAGE (/opt/splunk/var/lib)         │    │
│  │                                                      │    │
│  │  Index: "security"                                 │    │
│  │  • Size: ~5GB (adjustable)                         │    │
│  │  • Retention: 30 days (default)                    │    │
│  │  • Event count: ~10,000/day                        │    │
│  │                                                      │    │
│  │  Index: "windows"                                  │    │
│  │  • Size: ~3GB                                       │    │
│  │  • Retention: 30 days                              │    │
│  │  • Event count: ~5,000/day                         │    │
│  │                                                      │    │
│  │  Index: "main"                                     │    │
│  │  • Default internal index                          │    │
│  └──────────────────────────────────────────────────────┘    │
│                            │                                  │
│                            ▼                                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         SPLUNK SEARCH INTERFACE                      │    │
│  │  (Web UI on Port 8000)                              │    │
│  │                                                      │    │
│  │  Access: https://192.168.56.10:8000                │    │
│  │  Capabilities:                                      │    │
│  │  • Real-time search                                │    │
│  │  • Alert creation                                  │    │
│  │  • Dashboard building                              │    │
│  │  • Report generation                               │    │
│  │  • Data visualization                              │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Detection Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                  INCOMING EVENTS                            │
│          (From Splunk indexed data)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           DETECTION RULES ENGINE                           │
│  (6 Detection Rules running continuously)                 │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────┬───────┼────────┬─────┬──────────┐
        │    │       │        │     │          │
        ▼    ▼       ▼        ▼     ▼          ▼
    ┌──────┐ ┌─────┐ ┌────────┐ ┌────┐ ┌──────┐ ┌──────────┐
    │Rule1 │ │Rule2│ │Rule 3  │ │Rule4 │ │Rule5 │ │Rule 6    │
    └──┬───┘ └──┬──┘ └───┬────┘ └───┬─┘ └──┬───┘ └────┬─────┘
       │        │        │          │       │          │
   Brute  Power  │    Network  Credential  Lateral
   Force  Shell  │    Recon    Dumping     Movement
            Cmd  │
                 │
          Suspicious
          Processes
                 │
        ┌────────┴──────────┐
        │                   │
        ▼                   ▼
    ┌─────────────┐   ┌──────────────┐
    │ ALERT       │   │ LOGGING      │
    │ TRIGGERED   │   │ (No Alert)   │
    └──────┬──────┘   └──────────────┘
           │
           ▼
    ┌────────────────────┐
    │ ALERTING ENGINE    │
    │ (Send Notification)│
    │ • Email            │
    │ • Dashboard Highlight
    │ • Incident Ticket  │
    └────────────────────┘
```

---

## Component Details

### 1. **Ubuntu Splunk Server** (192.168.56.10)

**Role**: Central SIEM and data aggregation

**Specifications**:
- OS: Ubuntu 26.04 LTS
- RAM: 4GB allocated
- CPU: 2 cores
- Disk: 50GB virtual drive
- Splunk Version: Enterprise (free)

**Services**:
- Splunk daemon (splunkd) - Port 8089
- Splunk web UI - Port 8000
- Receiving port - Port 9997 (incoming logs)

**Indexes**:
- `security` - Windows security events (failed logins, account changes)
- `windows` - Sysmon events (process, network, file operations)
- `main` - Internal Splunk logs

**Key Directories**:
```
/opt/splunk/
├── bin/               # Splunk executables
├── etc/
│   ├── apps/         # Applications and configs
│   ├── system/       # System configurations
│   └── users/        # User configurations
├── var/
│   ├── log/          # Splunk logs
│   └── lib/          # Index storage (raw data)
└── share/            # UI assets
```

---

### 2. **Windows Endpoint** (192.168.56.20)

**Role**: Data source and attack target

**Specifications**:
- OS: Windows 11
- RAM: 2GB allocated
- CPU: 2 cores
- Disk: 60GB virtual drive

**Security Software**:
- **Sysmon** - System monitoring (detailed event tracking)
- **Splunk Universal Forwarder** - Log forwarding agent
- Windows Security Event Log - Native security logging

**Sysmon Installation**:
```
C:\Sysmon\sysmon.exe -accepteula -i sysmonconfig-export.xml
```

**Forwarder Installation**:
```
C:\Program Files\SplunkUniversalForwarder\bin\splunk forward-server 192.168.56.10:9997
```

**Event Sources**:
- Windows Security Event Log (Event Viewer)
- Sysmon Event Log (Application log)
- Process execution logs
- Network connection logs

---

### 3. **Kali Linux** (192.168.56.30)

**Role**: Attack simulation and security testing

**Specifications**:
- OS: Kali Linux
- RAM: 2GB allocated
- CPU: 2 cores
- Disk: Imported from VirtualBox OVA

**Tools Included**:
- **Nmap** - Network scanning and discovery
- **Hydra** - Brute-force password cracking
- **Metasploit** - Exploitation framework
- Network utilities (ping, netstat, etc.)

**Attack Simulation Examples**:
```bash
# Brute-force simulation
hydra -l admin -P wordlist.txt 192.168.56.20 smb

# Network scanning
nmap -sV -p 1-10000 192.168.56.20

# Process monitoring
watch -n 1 netstat -ano
```

---

## Data Processing Pipeline

### Step 1: Event Generation (Windows)
- Sysmon monitors all process execution, network connections, registry changes
- Windows logs all security events (logon attempts, account changes, etc.)
- Events written to Windows Event Log in real-time

### Step 2: Log Collection (Splunk Forwarder)
- Forwarder reads new events from Windows Event Log
- Transforms events to plain text format
- Sends via TLS/SSL to Splunk receiving port
- Retry logic for failed connections

### Step 3: Event Reception (Splunk Indexer)
- Splunk listening agent on port 9997
- Receives and verifies incoming data
- Extracts source, host, sourcetype metadata
- Performs initial parsing

### Step 4: Indexing & Storage
- Splunk parses raw events
- Extracts fields (timestamp, EventID, User, Computer, etc.)
- Creates searchable index files
- Stores raw event data for retrieval
- Maintains index metadata

### Step 5: Search & Analysis
- User submits SPL (Splunk Processing Language) search query
- Splunk searches indexes matching the query
- Returns matching events in real-time
- User performs correlation and analysis

### Step 6: Detection & Alerting
- Detection rules run on incoming data
- Rules evaluate patterns (e.g., >5 failed logins in 5 min)
- Matching events trigger alerts
- Alerts create tickets or send notifications

---

## Security Event Mappings

### Windows Event IDs

| Event ID | Event Name | Source | Importance |
|----------|-----------|--------|------------|
| 4624 | Successful logon | Security | Medium |
| 4625 | Failed logon | Security | High |
| 4628 | Account group membership changed | Security | Medium |
| 4630 | Account deleted | Security | High |
| 4720 | User account created | Security | High |
| 4722 | User account enabled | Security | Medium |
| 4723 | Password change attempt | Security | Low |
| 4728 | Member added to security group | Security | High |

### Sysmon Event IDs

| Event ID | Event Name | Use Case |
|----------|-----------|----------|
| 1 | Process created | Detect malware execution |
| 3 | Network connection | Detect C&C communication |
| 5 | Process terminated | Monitor process lifecycle |
| 8 | Remote thread creation | Detect code injection |
| 10 | Process access | Detect credential dumping (LSASS) |
| 11 | File created | Detect file drops |
| 13 | Registry value set | Detect persistence mechanisms |
| 21 | WmiEvent | Detect WMI exploitation |

---

## Performance Specifications

### Event Volume
- Windows Security Events: ~10,000-15,000/day
- Sysmon Events: ~50,000-100,000/day
- Total Daily: ~60,000-115,000 events

### Storage Requirements
- Security Index: 5GB (30-day retention)
- Windows Index: 3GB (30-day retention)
- Total: ~8GB for indexes

### Processing Capacity
- Splunk can handle ~10,000 events/second (EPS)
- This lab generates ~1-2 events/second normally
- Capable of handling attack simulations with 100+ EPS

---
