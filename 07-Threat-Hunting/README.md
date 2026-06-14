# Phase 7: Threat Hunting 🔍

## Proactive Searching for Hidden Threats

This phase covers threat hunting methodology and advanced search techniques.

---

## ⏱️ Time Estimate: 1.5-2 hours

---

## 📋 Prerequisites

✅ Phases 1-6 complete
✅ Events flowing into Splunk
✅ Detection rules created
✅ Comfortable with searches

---

## 🎯 Learning Objectives

After this phase:
- ✅ Understand threat hunting methodology
- ✅ Create hunting hypotheses
- ✅ Write advanced searches
- ✅ Correlate events across sources
- ✅ Identify suspicious patterns

---

## 🎲 Threat Hunting Methodology

### The Hunting Loop:

```
1. HYPOTHESIS
   "Attackers might be using PowerShell for lateral movement"
        ↓
2. INVESTIGATION
   Search for PowerShell with network activity
        ↓
3. ENRICHMENT
   Add IP reputation, domain info, user context
        ↓
4. ANALYSIS
   Determine if legitimate or malicious
        ↓
5. OUTCOME
   Create alert, escalate to incident, or close
```

---

## 🔎 Hunting Query 1: Unauthorized Admin Access

**Hypothesis**: Attackers might be using stolen credentials to access admin accounts

```
Search:
index=security EventCode=4624 logon_type=3 user=*admin*
| stats count, earliest, latest by src_ip, user
| where count > 5
```

**What to look for**:
- Admin logins from unusual times
- Admin logins from unexpected IPs
- Multiple admin accounts same source

---

## 🔎 Hunting Query 2: Persistence Mechanisms

**Hypothesis**: Attackers create backdoors using registry

```
Search:
index=windows EventID=13 TargetObject=*\\Run\\*
| stats count by Computer, TargetObject
| where count > 2
```

**What to look for**:
- New entries in Windows Run registry
- Entries with suspicious program names
- Registry changes outside business hours

---

## 🔎 Hunting Query 3: Credential Dumping Attempts

**Hypothesis**: Attackers accessing LSASS to dump credentials

```
Search:
index=windows EventID=10 TargetImage=*lsass.exe*
| stats count, earliest, latest by Computer, SourceImage
| where count > 1
```

**What to look for**:
- Multiple processes accessing LSASS
- Access from suspicious executables
- Access from non-standard locations

---

## 🔎 Hunting Query 4: Lateral Movement

**Hypothesis**: Attackers moving to other systems via SMB

```
Search:
index=windows EventID=3 DestinationPort=445
| stats dc(DestinationIp) as unique_targets by Computer
| where unique_targets > 10
```

**What to look for**:
- Single system connecting to many others
- Connections at odd times
- Connections to admin shares

---

## 🔎 Hunting Query 5: Data Exfiltration

**Hypothesis**: Attackers stealing data via unusual protocols

```
Search:
index=windows EventID=3 DestinationPort=443
| stats bytes_out by DestinationIp, Computer
| where bytes_out > 1000000
```

**What to look for**:
- Large outbound HTTPS transfers
- Connections to known C&C IPs
- Unusual destination countries

---

## 🔎 Hunting Query 6: Process Injection

**Hypothesis**: Attackers injecting code into legitimate processes

```
Search:
index=windows EventID=8
| stats count by Computer, TargetImage, SourceImage
| where count > 2
```

**What to look for**:
- One process creating threads in another
- Injection from non-standard locations
- Multiple targets from same source

---

## 🔎 Hunting Query 7: Command Line Obfuscation

**Hypothesis**: Attackers hiding commands with encoding

```
Search:
index=windows EventID=1 
(CommandLine=*base64* 
OR CommandLine=*cmd /c* 
OR CommandLine=*powershell -enc*
OR CommandLine=*echo*|*cmd*)
| stats count by Computer, CommandLine
```

**What to look for**:
- Base64 encoded commands
- Multi-layer command execution
- Encoded PowerShell scripts

---

## 🔎 Hunting Query 8: Scheduled Task Creation

**Hypothesis**: Attackers creating persistence via scheduled tasks

```
Search:
index=windows EventID=600
| stats count by Computer, TaskName
| where count > 5
```

**What to look for**:
- New scheduled tasks
- Tasks with suspicious names
- Tasks running at odd intervals

---

## 📋 Hunting Investigation Checklist

When you find suspicious activity:

- ✅ Who? (User, computer, IP address)
- ✅ What? (Type of activity, commands, data)
- ✅ When? (Date, time, duration)
- ✅ Where? (Source, destination, geography)
- ✅ Why? (Legitimate or malicious?)
- ✅ Frequency? (One-time or repeated?)
- ✅ Related? (Connect to other events?)

---

## 🎯 Hunting Tips

1. **Start with Baselines**
   - What's normal in your environment?
   - Document expected activity
   - Hunt for deviations

2. **Use Time-Based Analysis**
   - Business hours vs. after-hours
   - Day vs. night
   - Weekday vs. weekend

3. **Correlation is Key**
   - Don't hunt in isolation
   - Link events together
   - Follow the chain of events

4. **Think Like Attacker**
   - What would they do next?
   - What persistence mechanisms?
   - How would they hide?

5. **Document Everything**
   - Save searches
   - Document findings
   - Create repeatable hunts

---

## ✅ Phase 7 Verification Checklist

- ✅ Can write hunting queries
- ✅ Can identify suspicious patterns
- ✅ Can correlate events
- ✅ Created hunting hypotheses
- ✅ Understand anomaly detection
- ✅ Know how to investigate
- ✅ Saved multiple hunting searches

---

## 📄 Files in This Phase

See `07-Threat-Hunting/` for:
- `hunting-queries.txt` - Pre-built hunting searches
- `hunting-hypotheses.md` - Hypothesis templates
- `hunting-checklist.md` - Investigation checklist

---

## 🎓 What You Learned

✅ Threat hunting methodology
✅ Hypothesis-driven investigations
✅ Advanced Splunk searches
✅ Event correlation
✅ Anomaly identification
✅ Investigation techniques

---

## ↩️ Next Phase

Phase 8: MITRE ATT&CK Mapping

Time to map detections to industry framework! 🗺️