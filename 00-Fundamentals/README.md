# Phase 0: Fundamentals 📚

## Essential Concepts for SOC & Threat Hunting

This phase covers foundational concepts you need before starting the project.

---

## 🎯 Learning Objectives

After this phase, you will understand:
- What a SOC (Security Operations Center) is
- What a SIEM (Security Information & Event Management) tool does
- How Splunk works
- What Sysmon is and why it's useful
- What threat hunting means
- How detection rules work

---

## 📖 Key Concepts

### 1. SOC (Security Operations Center)

**Definition**: A team of security professionals working 24/7 to monitor, detect, investigate, and respond to security incidents.

**What they do**:
- Monitor security alerts in real-time
- Investigate suspicious activities
- Respond to security incidents
- Track threats and trends
- Create detection rules
- Maintain security infrastructure

**Typical SOC Structure**:
```
SOC Manager
├── Tier 1 Analysts (Alert monitoring)
├── Tier 2 Analysts (Investigation)
├── Tier 3 Engineers (Tools & Automation)
└── Incident Response Team
```

**Skills Needed**:
- SIEM administration
- Log analysis
- Threat intelligence
- Incident response
- Network security
- System administration

---

### 2. SIEM (Security Information & Event Management)

**Definition**: Software that collects security logs from all systems, centralizes them, analyzes them, and helps find security problems.

**Key Functions**:
1. **Collection** - Gather logs from hundreds/thousands of devices
2. **Normalization** - Convert different log formats to standard format
3. **Indexing** - Make logs searchable
4. **Analysis** - Find patterns and anomalies
5. **Alerting** - Notify when suspicious activities detected
6. **Reporting** - Generate compliance and security reports

**Why you need a SIEM**:
- One machine alone can't monitor everything
- Too much data to analyze manually
- Need real-time alerts
- Compliance requirements (HIPAA, PCI-DSS, etc.)
- Find attacks before they cause damage

**Popular SIEM Tools**:
- Splunk (market leader) - what we're using
- IBM QRadar
- ArcSight
- Elasticsearch Stack
- Azure Sentinel
- Sumo Logic

---

### 3. Splunk

**What is it?**: A powerful SIEM platform that processes massive amounts of machine data.

**Core Components**:
- **Forwarder** - Collects logs from endpoints
- **Indexer** - Stores and indexes logs
- **Search Head** - User interface for searching logs
- **Apps** - Specialized tools for specific use cases

**How Splunk Works**:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Endpoints   │───▶│   Forwarder  │───▶│   Indexer    │
│ (Windows,    │    │ (Collects    │    │ (Stores &    │
│  Linux,      │    │  logs)       │    │  Indexes)    │
│  Network     │    └──────────────┘    └──────┬───────┘
│  Devices)    │                               │
└──────────────┘                               │
                                               ▼
                                        ┌──────────────┐
                                        │ Search Head  │
                                        │ (Web UI)     │
                                        │ (Analysis)   │
                                        └──────────────┘
```

**Splunk in 3 Steps**:
1. **Ingest** - Collect logs from everywhere
2. **Index** - Make logs searchable and fast
3. **Investigate** - Search and analyze to find threats

---

### 4. Sysmon (System Monitor)

**What is it?**: A Windows system service and driver that monitors detailed system activity.

**What it tracks**:
- Process execution (what programs run)
- Network connections (what systems connect to)
- Registry modifications (system configuration changes)
- File creation (what files are created)
- Process access (one process accessing another)
- Image loading (DLL/library loading)

**Why it's important**:
- Windows doesn't log detailed process information by default
- Sysmon fills this gap
- Can detect malware by watching abnormal behavior
- Creates Event ID logs that Splunk can analyze

**Example Event**:
```
Event: Process Creation
EventID: 1
Parent Process: explorer.exe
Process: powershell.exe
Command Line: powershell.exe -Command "Get-Process"
User: Domain\admin
Timestamp: 2025-06-14 10:30:45.123
Computer: DESKTOP-ABC123
```

---

### 5. Threat Hunting

**Definition**: Proactively searching for attackers who have already breached the network, rather than waiting for alerts.

**Key Differences**:
- **Detection**: Reactive (waits for alerts)
- **Hunting**: Proactive (searches for threats)

**Threat Hunting Process**:

```
1. Hypothesis: "Attackers might be using PowerShell for commands"
       ↓
2. Search: index=windows powershell.exe CommandLine=*whoami*
       ↓
3. Investigate: Check if legitimate or malicious
       ↓
4. Validate: Confirm it's an actual threat
       ↓
5. Escalate: Create alert or incident
```

**Common Hunting Scenarios**:
- Find all process injections (malware technique)
- Detect unusual network connections
- Identify credential access attempts
- Discover persistence mechanisms
- Track lateral movement patterns

---

### 6. Detection Rules

**What is it?**: Automated searches that run continuously to find specific security problems.

**Components of a Detection Rule**:
```
{
  "name": "Brute Force Detection",
  "search": "index=security EventCode=4625 | stats count by src_ip | where count > 5",
  "threshold": "count > 5 failed logins",
  "time_window": "5 minutes",
  "action": "Send email alert",
  "mitre_technique": "T1110 (Brute Force)"
}
```

**How it works**:
1. Rule searches for specific pattern
2. If pattern found, trigger threshold check
3. If threshold met, trigger alert
4. Alert sent to analyst or ticket system

---

### 7. Log Analysis Basics

**What are logs?**: Records of everything happening on a computer.

**Types of logs**:
- **Security Logs** - Login attempts, account changes, permissions
- **Application Logs** - Software errors, user actions
- **System Logs** - Hardware events, service starts/stops
- **Sysmon Logs** - Process, network, registry, file activity

**Log Format**:
```
2025-06-14 10:30:45.123 ComputerName EventCode=4625 User=admin \
  FailureReason=BadPassword SourceIP=192.168.1.100 \
  FailureCount=3
```

---

### 8. MITRE ATT&CK Framework

**What is it?**: A comprehensive list of tactics and techniques used by attackers.

**Structure**:
```
Tactic (Goal)        → Technique (Method)              → Sub-technique
Initial Access      → Phishing (T1566)                → Email attachment
Execution           → Command and Scripting (T1059)   → PowerShell
Persistence         → Registry Run Keys (T1547.001)   → Windows Run key
Privilege Escalation → Sudo caching (T1548.003)       → Sudo exploits
Defense Evasion     → Masquerading (T1036)            → Rename files
Discovery           → Network Service Scanning (T1046) → Nmap
Lateral Movement    → SMB (T1570)                     → Windows shares
Collection          → Screen Capture (T1113)          → Screenshot
Exfiltration        → Over C2 Channel (T1041)         → Data upload
Command & Control   → Remote Access Software (T1219)  → TeamViewer
Impact              → Data Destruction (T1485)        → Wiper malware
```

**Why it matters**:
- Standardized language for describing attacks
- Helps align detection rules with attacker techniques
- Useful for security assessments
- Helps prioritize defenses

---

## 🔄 Attack Kill Chain (Lockheed Martin)

Hackers follow this pattern:

```
1. RECONNAISSANCE
   └─ Attacker gathers information about target
   └─ DETECTION: Network scanning activity

2. WEAPONIZATION
   └─ Attacker creates malware or exploit code
   └─ DETECTION: Unusual file creation

3. DELIVERY
   └─ Attacker sends malware (email, USB, web)
   └─ DETECTION: Suspicious email, USB device

4. EXPLOITATION
   └─ Malware runs and exploits vulnerability
   └─ DETECTION: Process execution patterns

5. INSTALLATION
   └─ Attacker establishes persistence (backdoor)
   └─ DETECTION: Registry changes, scheduled tasks

6. COMMAND & CONTROL (C&C)
   └─ Attacker communicates with malware
   └─ DETECTION: Unusual network connections

7. ACTIONS ON OBJECTIVES
   └─ Attacker steals data, disrupts systems
   └─ DETECTION: Large data transfers, file deletion
```

---

## 📊 Common Security Terms

| Term | Definition | Example |
|------|-----------|----------|
| **Indicator of Compromise (IOC)** | Evidence of an attack | Malicious IP address, file hash |
| **Event** | Something happening on a system | Process execution, network connection |
| **Alert** | Notification of suspicious activity | Rule triggered: "Brute force detected" |
| **Incident** | Security event requiring response | Confirmed breach, data theft |
| **Artifact** | Data collected during investigation | Log files, memory dump |
| **Enrichment** | Adding context to data | IP reputation, geolocation |
| **Correlation** | Connecting related events | 100 systems compromised at same time |
| **Anomaly** | Deviation from normal behavior | Admin login at 3am from unknown IP |
| **False Positive** | Alert for non-threat activity | Blocked legitimate business process |
| **False Negative** | Missed actual threat | Attacker bypassed detection |

---

## 🎓 Preparation Checklist

Before starting Phase 1:

- ✅ Understand what a SOC does
- ✅ Know SIEM functions
- ✅ Understand Splunk's role
- ✅ Know what Sysmon monitors
- ✅ Understand threat hunting concept
- ✅ Familiar with detection rules
- ✅ Know kill chain phases
- ✅ Understand MITRE ATT&CK basics

---

## 🔗 Resources for Further Learning

### Official Documentation
- [Splunk Fundamentals](https://docs.splunk.com)
- [Sysmon Documentation](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [MITRE ATT&CK](https://attack.mitre.org)
- [Windows Event Log IDs](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/audit-events)

### Free Training
- Splunk Free Online Training
- SANS Cyber Academy
- Coursera Security specializations

### Books
- "The Cyber Threat Landscape" by SANS
- "Incident Response" by Erickson
- "The Art of Memory Forensics" by Ligh

---

## ✅ Phase 0 Summary

You now understand:
- ✅ SOC operations and structure
- ✅ SIEM purpose and functions
- ✅ How Splunk works
- ✅ Sysmon event monitoring
- ✅ Threat hunting methodology
- ✅ Detection rule concepts
- ✅ Kill chain and attack progression
- ✅ MITRE ATT&CK framework

---

**Next**: Start Phase 1 - Environment Setup

You're ready to build your SOC lab! 🚀