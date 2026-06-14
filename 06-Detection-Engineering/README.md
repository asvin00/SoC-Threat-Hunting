# Phase 6: Detection Engineering 🚨

## Create Automated Detection Rules

This phase covers creating detection rules to automatically find threats.

---

## ⏱️ Time Estimate: 1.5-2 hours

---

## 📋 Prerequisites

✅ Splunk running and indexed logs (Phase 5)
✅ Familiar with Splunk searches
✅ Splunk admin access
✅ Understanding of threat patterns

---

## 🎯 Learning Objectives

After this phase:
- ✅ Create 6 detection rules
- ✅ Configure alerts
- ✅ Set thresholds
- ✅ Map to MITRE ATT&CK
- ✅ Trigger alerts manually

---

## 🔔 6 Detection Rules

### RULE 1: Brute Force Detection

**Threat**: Multiple failed login attempts = potential password guessing

```
Search Query:
index=security EventCode=4625 
| stats count by src_ip 
| where count > 5
```

**Configuration**:
- **Name**: Brute Force Attempt Detected
- **Alert Type**: Real-time
- **Threshold**: count > 5 in 5 minutes
- **Action**: Send email alert
- **MITRE**: T1110 (Brute Force)

**Why it works**:
- EventCode 4625 = failed login
- 5+ failures from same IP = suspicious
- Could indicate password attack

---

### RULE 2: PowerShell Abuse Detection

**Threat**: PowerShell used by attackers for command execution

```
Search Query:
index=windows EventID=1 Image=*powershell.exe* 
| stats count by Computer
```

**Configuration**:
- **Name**: PowerShell Execution Detected
- **Alert Type**: Real-time
- **Threshold**: Any execution (count > 0)
- **Action**: Log and dashboard highlight
- **MITRE**: T1059.001 (Command and Scripting Interpreter - PowerShell)

**Why it works**:
- EventID 1 = process creation
- PowerShell = common attack vector
- Flag for analysis

---

### RULE 3: Suspicious Command Line Execution

**Threat**: Specific commands often used by attackers

```
Search Query:
index=windows EventID=1 
(CommandLine=*net user* 
 OR CommandLine=*wget* 
 OR CommandLine=*curl* 
 OR CommandLine=*whoami*
 OR CommandLine=*systeminfo*)
```

**Configuration**:
- **Name**: Suspicious Command Line Detected
- **Alert Type**: Real-time
- **Threshold**: Any match
- **Action**: Alert and ticket creation
- **MITRE**: T1087 (Account Discovery)

**Why it works**:
- Attackers run specific commands to gather info
- Tools like wget, curl used to download malware
- Commands like whoami, systeminfo for reconnaissance

---

### RULE 4: Network Reconnaissance Detection

**Threat**: Scanning activity indicates active reconnaissance

```
Search Query:
index=windows EventID=3 
(DestinationPort=53 
 OR DestinationPort=445 
 OR DestinationPort=139 
 OR DestinationPort=3389)
```

**Configuration**:
- **Name**: Suspicious Network Connection Detected
- **Alert Type**: Real-time
- **Threshold**: Any connection to suspicious ports
- **Action**: Alert
- **MITRE**: T1046 (Network Service Discovery)

**Why it works**:
- Port 53 = DNS (data exfiltration)
- Port 445 = SMB (lateral movement)
- Port 139 = NetBIOS (network scanning)
- Port 3389 = RDP (remote access)

---

### RULE 5: Credential Dumping Detection

**Threat**: Process accessing LSASS = potential credential theft

```
Search Query:
index=windows EventID=10 
TargetImage=*lsass.exe* 
SourceImage!=*winlogon.exe*
```

**Configuration**:
- **Name**: Credential Dumping Attempt Detected
- **Alert Type**: Real-time
- **Threshold**: Any unauthorized access to LSASS
- **Action**: Critical alert
- **MITRE**: T1003 (OS Credential Dumping)

**Why it works**:
- EventID 10 = process access
- LSASS = stores Windows passwords
- Access (except from winlogon) = suspicious

---

### RULE 6: Lateral Movement Detection

**Threat**: Connections to multiple systems = lateral movement

```
Search Query:
index=windows EventID=3 
(DestinationPort=445 OR DestinationPort=139 OR DestinationPort=3389)
| stats dc(DestinationIp) as unique_ips by ComputerName
| where unique_ips > 3
```

**Configuration**:
- **Name**: Lateral Movement Detected
- **Alert Type**: Real-time
- **Threshold**: 3+ unique IPs from same computer
- **Action**: Critical alert
- **MITRE**: T1021 (Remote Services)

**Why it works**:
- Attacker connects to multiple systems
- SMB/RDP = lateral movement protocols
- Multiple connections = suspicious behavior

---

## 🔧 How to Create Alert in Splunk

```
1. Enter search query
2. Click "Search" button
3. Wait for results
4. Click "Save As" → "Alert"
5. Fill in:
   - Alert name
   - Alert type: "Real-time" or "Scheduled"
   - Trigger: "Always" or custom condition
   - Trigger throttle: 5 minutes (prevent spam)
6. Add action:
   - Email
   - Webhook
   - Custom script
7. Click "Save"
```

---

## ✅ Phase 6 Verification Checklist

- ☐ Rule 1: Brute Force Detection created
- ☐ Rule 2: PowerShell Detection created
- ☐ Rule 3: Suspicious Command Detection created
- ☐ Rule 4: Network Recon Detection created
- ☐ Rule 5: Credential Dumping Detection created
- ☐ Rule 6: Lateral Movement Detection created
- ☐ All rules searchable from Alerts menu
- ☐ Alert actions configured
- ☐ Can manually trigger each alert
- ☐ Understand MITRE mapping for each rule

---

## 📁 Detection Rule Files

See `06-Detection-Engineering/` for:
- `detection-rules.json` - All rules in JSON format
- `rules/` directory:
  - `brute-force-detection.json`
  - `powershell-abuse.json`
  - `suspicious-processes.json`
  - `network-reconnaissance.json`
  - `credential-dumping.json`
  - `lateral-movement.json`

---

## 🎓 What You Learned

✅ Detection rule creation
✅ Alert configuration
✅ Threshold tuning
✅ MITRE ATT&CK mapping
✅ False positive management
✅ Trigger actions

---

## ↪️ Next Phase

Phase 7: Threat Hunting

Time to proactively hunt for threats! 🔍