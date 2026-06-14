# Phase 8: MITRE ATT&CK Mapping 🗺️

## Align Detections with Industry Framework

This phase covers mapping detections to MITRE ATT&CK framework.

---

## ⏱️ Time Estimate: 1 hour

---

## 📋 Prerequisites

✅ Phases 1-7 complete
✅ Detection rules created
✅ Understand threat hunting
✅ Familiar with attacks

---

## 🎯 Learning Objectives

After this phase:
- ✅ Understand MITRE ATT&CK framework
- ✅ Map detections to techniques
- ✅ Identify detection gaps
- ✅ Understand threat actor tactics
- ✅ Create coverage analysis

---

## 📚 MITRE ATT&CK Framework Overview

### What is MITRE ATT&CK?

A globally-accessible knowledge base of adversary tactics and techniques based on real-world observations.

### Structure:

```
TACTIC (What goal?)
  └─ TECHNIQUE (How to achieve it?)
      └─ SUB-TECHNIQUE (Specific method)
```

---

## 🎭 13 Tactics (Attack Phases)

```
1. RECONNAISSANCE
   └─ T1598 - Phishing for Information
   └─ T1592 - Gather Victim Host Information

2. RESOURCE DEVELOPMENT
   └─ T1586 - Compromise Accounts
   └─ T1583 - Acquire Infrastructure

3. INITIAL ACCESS
   └─ T1200 - Hardware Additions
   └─ T1566 - Phishing

4. EXECUTION
   └─ T1059 - Command and Scripting Interpreter
   └─ T1203 - Exploitation for Client Execution

5. PERSISTENCE
   └─ T1547 - Boot or Logon Autostart Execution
   └─ T1547.001 - Registry Run Keys

6. PRIVILEGE ESCALATION
   └─ T1548 - Abuse Elevation Control Mechanism
   └─ T1548.003 - Sudo and Sudo Caching

7. DEFENSE EVASION
   └─ T1197 - BITS Jobs
   └─ T1036 - Masquerading

8. CREDENTIAL ACCESS
   └─ T1110 - Brute Force
   └─ T1003 - OS Credential Dumping

9. DISCOVERY
   └─ T1580 - Cloud Infrastructure Discovery
   └─ T1538 - Cloud Service Discovery

10. LATERAL MOVEMENT
    └─ T1570 - Lateral Tool Transfer
    └─ T1021 - Remote Services

11. COLLECTION
    └─ T1557 - Man-in-the-Middle
    └─ T1123 - Audio Capture

12. COMMAND & CONTROL
    └─ T1071 - Application Layer Protocol
    └─ T1092 - Communication Through Removable Media

13. EXFILTRATION
    └─ T1041 - Exfiltration Over C2 Channel
    └─ T1020 - Automated Exfiltration

14. IMPACT
    └─ T1531 - Account Access Removal
    └─ T1485 - Data Destruction
```

---

## 🔗 Detection Rules to MITRE Mapping

### Rule 1: Brute Force Detection
```
Rule: index=security EventCode=4625 | stats count by src_ip | where count > 5
  ↓
Tactic: Credential Access
Technique: T1110 - Brute Force
Sub-technique: T1110.001 - Password Guessing
Severity: High
```

### Rule 2: PowerShell Abuse Detection
```
Rule: index=windows EventID=1 Image=*powershell.exe*
  ↓
Tactic: Execution
Technique: T1059 - Command and Scripting Interpreter
Sub-technique: T1059.001 - PowerShell
Severity: Medium
```

### Rule 3: Suspicious Command Execution
```
Rule: index=windows EventID=1 CommandLine=*net user*
  ↓
Tactic: Discovery
Technique: T1087 - Account Discovery
Severity: Medium
```

### Rule 4: Network Reconnaissance
```
Rule: index=windows EventID=3 DestinationPort=445
  ↓
Tactic: Lateral Movement
Technique: T1021 - Remote Services
Sub-technique: T1021.002 - SMB/Windows Admin Shares
Severity: High
```

### Rule 5: Credential Dumping
```
Rule: index=windows EventID=10 TargetImage=*lsass.exe*
  ↓
Tactic: Credential Access
Technique: T1003 - OS Credential Dumping
Sub-technique: T1003.001 - LSASS Memory
Severity: Critical
```

### Rule 6: Lateral Movement
```
Rule: index=windows EventID=3 DestinationPort=445 | stats dc(DestinationIp) by Computer | where dc > 3
  ↓
Tactic: Lateral Movement
Technique: T1570 - Lateral Tool Transfer
Severity: High
```

---

## 📊 Detection Coverage Analysis

### Coverage by Tactic:

```
Tactic                    | Covered | Detection Rule
──────────────────────────┼─────────┼──────────────────────────
RECONNAISSANCE           | ❌ No   | Need network scanning detection
RESOURCE DEVELOPMENT     | ❌ No   | Need account compromise detection
INITIAL ACCESS           | ❌ No   | Need email/phishing detection
EXECUTION                | ✅ Yes  | PowerShell detection (Rule 2)
PERSISTENCE              | ⚠️ Partial | Registry monitoring only
PRIVILEGE ESCALATION     | ❌ No   | Need UAC bypass detection
DEFENSE EVASION          | ⚠️ Partial | Limited coverage
CREDENTIAL ACCESS        | ✅ Yes  | Brute Force (Rule 1), Credential Dumping (Rule 5)
DISCOVERY                | ✅ Yes  | Command execution (Rule 3)
LATERAL MOVEMENT         | ✅ Yes  | Network connections (Rule 4, 6)
COLLECTION               | ❌ No   | Need data exfiltration detection
COMMAND & CONTROL        | ❌ No   | Need C2 communication detection
EXFILTRATION             | ❌ No   | Need data exfiltration detection
IMPACT                   | ❌ No   | Need destructive action detection
```

**Current Coverage: 42%** (6 out of 14 tactics)

---

## 🎯 Detection Gap Analysis

### Recommended Additional Detections:

1. **PERSISTENCE** - Registry Run Keys
   ```
   index=windows EventID=13 TargetObject=*\\Run\\*
   ```

2. **PRIVILEGE ESCALATION** - Scheduled Task Creation
   ```
   index=windows EventID=600
   ```

3. **DEFENSE EVASION** - Windows Defender Disable
   ```
   index=windows EventID=1 CommandLine=*Set-MpPreference*
   ```

4. **COLLECTION** - Screen Capture
   ```
   index=windows EventID=1 CommandLine=*screenshot*
   ```

5. **EXFILTRATION** - Large Data Transfer
   ```
   index=windows EventID=3 BytesSent > 1000000
   ```

---

## 📈 MITRE Navigator

**Visualize Coverage**:

1. Go to: https://mitre-attack.github.io/attack-navigator/
2. Upload detection mapping
3. View heatmap of covered techniques
4. Identify gaps

---

## ✅ Phase 8 Verification Checklist

- ✅ Understand 14 MITRE tactics
- ✅ Know 6+ techniques
- ✅ Mapped all detection rules to techniques
- ✅ Identified coverage gaps
- ✅ Know current coverage %
- ✅ Can create coverage report

---

## 📄 Files in This Phase

See `08-Mitre-Mapping/` for:
- `mitre-mapping.json` - Mapping data
- `mitre-coverage.md` - Coverage analysis
- `mitre-dashboard.json` - Dashboard definition

---

## 🎓 What You Learned

✅ MITRE ATT&CK framework
✅ Tactic and technique mapping
✅ Detection coverage analysis
✅ Gap identification
✅ Prioritization of detections

---

## ↩️ Next Phase

Phase 9: Dashboards

Time to visualize your data! 📊