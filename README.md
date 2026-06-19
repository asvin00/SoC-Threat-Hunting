# 🛡️ SOC & Threat Hunting Platform Using Splunk

## Complete Educational Cybersecurity Project

A **fully functional Security Operations Center (SOC)** simulation platform built with Splunk SIEM for learning SIEM operations, threat detection, and incident investigation.

---

## 📋 Project Overview

This project demonstrates real-world SOC operations by building a complete security monitoring environment with:

- **Centralized Log Collection** - Splunk SIEM aggregating logs from Windows endpoints
- **Endpoint Monitoring** - Sysmon tracking process execution, network connections, and file operations
- **Real-time Detection** - 6+ detection rules for common attack patterns
- **Threat Hunting** - Proactive searching for hidden attackers
- **MITRE ATT&CK Mapping** - Aligning detections with industry framework
- **Security Automation** - Python scripts for continuous scanning and integration
- **Interactive Dashboards** - Real-time security visibility

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   NETWORK: 192.168.56.0/24                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌────────────────────────┐   │
│  │ Ubuntu-Splunk    │         │  Windows-Endpoint      │   │
│  │ 192.168.56.10    │◄────────│  192.168.56.20         │   │
│  │                  │ (logs)  │                        │   │
│  │ • Splunk SIEM    │         │ • Sysmon               │   │
│  │ • Port 8000      │         │ • Universal Forwarder  │   │
│  │ • Indexes:       │         │ • Port 9997            │   │
│  │   - security     │         │                        │   │
│  │   - windows      │         │ Sends logs every 30s   │   │
│  │   - main         │         │                        │   │
│  └──────────────────┘         └────────────────────────┘   │
│         ▲                                                    │
│         │ (searches/analysis)                               │
│         │                                                    │
│  ┌──────┴──────────┐                                        │
│  │ Kali-Attacker   │                                        │
│  │ 192.168.56.30   │                                        │
│  │                 │                                        │
│  │ • Nmap scans    │                                        │
│  │ • Attack sims   │                                        │
│  │ • Pen testing   │                                        │
│  └─────────────────┘                                        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
SoC-Threat-Hunting/
├── README.md                          # This file
├── ARCHITECTURE.md                    # Detailed architecture
│
├── 📂 00-Fundamentals/
│   ├── README.md                     # Concepts guide
│   └── concepts-glossary.md          # Definitions
│
├── 📂 01-Environment-Setup/
│   ├── README.md
│   ├── vm-setup-checklist.md
│   ├── ubuntu-netplan-config.yaml
│   ├── windows-network-setup.ps1
│   └── kali-network-setup.sh
│
├── 📂 02-Splunk-Installation/
│   ├── README.md
│   ├── splunk-install.sh
│   ├── inputs.conf
│   ├── outputs.conf
│   └── indexes.conf
│
├── 📂 03-Sysmon-Installation/
│   ├── README.md
│   ├── sysmonconfig-export.xml
│   └── sysmon-install.ps1
│
├── 📂 04-Splunk-Forwarder/
│   ├── README.md
│   ├── forwarder-install.ps1
│   ├── inputs.conf
│   └── outputs.conf
│
├── 📂 05-Log-Analysis/
│   ├── README.md
│   ├── basic-searches.txt
│   └── search-macros.conf
│
├── 📂 06-Detection-Engineering/
│   ├── README.md
│   ├── detection-rules.json
│   └── rules/
│
├── 📂 07-Threat-Hunting/
│   ├── README.md
│   └── hunting-queries.txt
│
├── 📂 08-Mitre-Mapping/
│   ├── README.md
│   └── mitre-mapping.json
│
├── 📂 09-Dashboards/
│   ├── README.md
│   ├── soc-overview-dashboard.json
│   └── threat-hunting-dashboard.json
│
├── 📂 10-Attack-Simulation/
│   ├── README.md
│   └── brute-force-simulation.sh
│
├── 📂 11-Python-Automation/
│   ├── README.md
│   ├── nmap-splunk-integration.py
│   └── requirements.txt
|
├── 📂 Configuration-Files/
│   ├── network-configs/
│   ├── splunk-configs/
│   └── endpoint-configs/
│
├── 📂 Documentation/
│   ├── ARCHITECTURE.md
│   ├── SETUP-GUIDE.md
│   ├── TROUBLESHOOTING.md
│ 
└── LICENSE
```

---
---

## 📞 Support

1. Check **[TROUBLESHOOTING.md](Documentation/TROUBLESHOOTING.md)**
2. Review phase-specific README file

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

**Status: Complete & Ready for Deployment** ✅

*All materials needed to build a professional SOC lab for learning cybersecurity operations.*
