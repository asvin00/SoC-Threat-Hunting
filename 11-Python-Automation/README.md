# Phase 11: Python Automation 🐍

## Automate Security Tasks with Python Scripts

This phase covers creating Python scripts for security automation.

---

## ⏱️ Time Estimate: 1.5-2 hours

---

## 📋 Prerequisites

✅ Phases 1-10 complete
✅ Python 3.8+ installed on Ubuntu
✅ pip installed
✅ Splunk running and accessible
✅ Comfortable with Python basics

---

## 🎯 Learning Objectives

After this phase:
- ✅ Write Python scripts for security tasks
- ✅ Integrate with Splunk API
- ✅ Automate network scanning
- ✅ Generate test logs
- ✅ Enrich data with threat intelligence

---

## 📦 Install Dependencies

```bash
# On Ubuntu terminal

sudo apt install python3-pip -y

pip3 install requests
pip3 install python-nmap
pip3 install paramiko
pip3 install requests-toolbelt

# Verify
python3 --version
pip3 list | grep requests
```

---

## 🔧 Script 1: Nmap-Splunk Integration

**Purpose**: Automated Nmap scanning with Splunk integration

### File: `nmap-splunk-integration.py`

```python
#!/usr/bin/env python3
import subprocess
import json
import requests
from datetime import datetime

SPLUNK_HOST = "192.168.56.10"
SPLUNK_PORT = 8000
SPLUNK_USER = "admin"
SPLUNK_PASS = "Splunk@123"
TARGET = "192.168.56.20"

def run_nmap_scan(target):
    """Run Nmap scan and return results"""
    print(f"[*] Starting Nmap scan on {target}")
    cmd = f"nmap -sV -p 1-1000 {target} -oX -"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def send_to_splunk(data):
    """Send scan results to Splunk"""
    url = f"https://{SPLUNK_HOST}:{SPLUNK_PORT}/services/receivers/simple"
    auth = (SPLUNK_USER, SPLUNK_PASS)
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "event": data,
        "sourcetype": "nmap_scan",
        "source": "automated_scanner",
        "index": "security"
    }
    
    try:
        response = requests.post(url, json=payload, auth=auth, verify=False)
        if response.status_code == 200:
            print("✓ Data sent to Splunk successfully")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

def main():
    print(f"[*] Automated Nmap Splunk Integration")
    print(f"[*] Target: {TARGET}")
    print(f"[*] Splunk: {SPLUNK_HOST}:{SPLUNK_PORT}")
    print()
    
    # Run scan
    scan_result = run_nmap_scan(TARGET)
    
    # Send to Splunk
    send_to_splunk(scan_result)
    
    print("[✓] Automation complete")

if __name__ == "__main__":
    main()
```

### Usage:

```bash
chmod +x /home/socadmin/nmap-splunk-integration.py
python3 /home/socadmin/nmap-splunk-integration.py
```

---

## 🔧 Script 2: Log Generator

**Purpose**: Generate test security logs

### File: `log-generator.py`

```python
#!/usr/bin/env python3
import random
import time
from datetime import datetime

USERS = ["admin", "user1", "user2", "guest", "service"]
IPS = [
    "192.168.1.100",
    "192.168.1.101",
    "10.0.0.1",
    "10.0.0.2",
    "203.0.113.1"
]
EVENT_CODES = {
    "4624": "Successful Logon",
    "4625": "Failed Logon",
    "4720": "User Account Created",
    "4728": "User Added to Group"
}

def generate_security_event():
    """Generate random security event"""
    event_id = random.choice(list(EVENT_CODES.keys()))
    user = random.choice(USERS)
    source_ip = random.choice(IPS)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    event = {
        "timestamp": timestamp,
        "EventID": event_id,
        "EventName": EVENT_CODES[event_id],
        "User": user,
        "SourceIP": source_ip,
        "Computer": "DESKTOP-ABC123",
        "Description": f"{EVENT_CODES[event_id]} for user {user} from {source_ip}"
    }
    
    return event

def main():
    print("[*] Security Event Log Generator")
    print()
    
    for i in range(100):
        event = generate_security_event()
        print(f"[{i+1}] {event['timestamp']} - {event['EventName']} - User: {event['User']} - IP: {event['SourceIP']}")
        time.sleep(0.1)
    
    print("\n[✓] Generated 100 test events")

if __name__ == "__main__":
    main()
```

---

## 🔧 Script 3: Threat Intelligence Enrichment

**Purpose**: Enrich logs with threat intelligence data

### File: `threat-intel-enrichment.py`

```python
#!/usr/bin/env python3
import json
import requests

# Simple threat intel database (in production, use real APIs)
THREAT_IPS = {
    "203.0.113.1": {"reputation": "malicious", "threat_level": "high", "category": "C&C"},
    "203.0.113.2": {"reputation": "suspicious", "threat_level": "medium", "category": "Botnet"}
}

def check_ip_reputation(ip):
    """Check if IP has known threats"""
    if ip in THREAT_IPS:
        return THREAT_IPS[ip]
    return {"reputation": "clean", "threat_level": "low", "category": "N/A"}

def enrich_event(event):
    """Add threat intelligence to event"""
    source_ip = event.get("SourceIP", "")
    destination_ip = event.get("DestinationIP", "")
    
    # Check source IP
    source_intel = check_ip_reputation(source_ip)
    event["source_threat_level"] = source_intel["threat_level"]
    event["source_reputation"] = source_intel["reputation"]
    
    # Check destination IP
    dest_intel = check_ip_reputation(destination_ip)
    event["dest_threat_level"] = dest_intel["threat_level"]
    event["dest_reputation"] = dest_intel["reputation"]
    
    return event

def main():
    print("[*] Threat Intelligence Enrichment")
    print()
    
    # Sample events
    events = [
        {"SourceIP": "203.0.113.1", "DestinationIP": "192.168.1.100", "EventID": "4624"},
        {"SourceIP": "10.0.0.1", "DestinationIP": "192.168.1.101", "EventID": "4625"},
        {"SourceIP": "203.0.113.2", "DestinationIP": "192.168.1.102", "EventID": "4720"}
    ]
    
    for event in events:
        enriched = enrich_event(event)
        print(f"[+] Event enriched:")
        print(f"    Source: {enriched['SourceIP']} - Threat: {enriched['source_threat_level']}")
        print(f"    Destination: {enriched['DestinationIP']} - Threat: {enriched['dest_threat_level']}")
        print()
    
    print("[✓] Enrichment complete")

if __name__ == "__main__":
    main()
```

---

## 📦 Requirements File

### File: `requirements.txt`

```
requests>=2.28.0
python-nmap>=0.0.1
paramiko>=3.0.0
requests-toolbelt>=0.9.1
```

### Install all dependencies:

```bash
pip3 install -r requirements.txt
```

---

## 🎯 Schedule Automation with Cron

```bash
# Edit cron table
crontab -e

# Add automated scan every hour
0 * * * * /home/socadmin/nmap-splunk-integration.py

# Run log generator every 30 minutes
*/30 * * * * python3 /home/socadmin/log-generator.py

# Check cron jobs
crontab -l
```

---

## ✅ Phase 11 Verification Checklist

- ✅ Python 3.8+ installed
- ✅ Dependencies installed (requests, nmap, etc.)
- ✅ nmap-splunk-integration.py created and working
- ✅ log-generator.py creates test events
- ✅ threat-intel-enrichment.py enriches data
- ✅ Scripts are executable
- ✅ Can run scripts manually
- ✅ Cron jobs scheduled
- ✅ Automation working end-to-end

---

## 📁 Files in This Phase

See `11-Python-Automation/` for:
- `nmap-splunk-integration.py` - Network scanning automation
- `log-generator.py` - Test log generation
- `threat-intel-enrichment.py` - Intelligence enrichment
- `requirements.txt` - Python dependencies
- `setup-automation.md` - Setup instructions

---

## 🎓 What You Learned

✅ Python script development
✅ API integration (Splunk)
✅ Automation scripting
✅ Scheduled tasks with cron
✅ Data enrichment
✅ Security tool integration

---

## ⬅️ Next Phase

Phase 12: Final Project

Time to wrap it all up! 🎉