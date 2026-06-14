# Phase 9: Dashboards 📊

## Create Real-Time Security Dashboards

This phase covers building interactive security dashboards.

---

## ⏱️ Time Estimate: 1.5-2 hours

---

## 📋 Prerequisites

✅ Phases 1-8 complete
✅ Detection rules created
✅ Data flowing into Splunk
✅ Familiar with Splunk UI

---

## 🎯 Learning Objectives

After this phase:
- ✅ Create 3 comprehensive dashboards
- ✅ Understand dashboard components
- ✅ Add visualizations
- ✅ Configure real-time updates
- ✅ Create executive reports

---

## 🎨 Dashboard 1: SOC Overview

**Purpose**: Executive-level security status

### Panel 1: Total Events (24hrs)
```
Search: index=* | stats count
Visualization: Single Value
Color: Green (if normal), Red (if high)
```

### Panel 2: Events by Index
```
Search: index=* | stats count by index
Visualization: Pie Chart
Shows: Proportion of events per index
```

### Panel 3: Events Timeline
```
Search: index=* | timechart count
Visualization: Line Chart
Shows: Events per hour over 24 hours
```

### Panel 4: Top 10 Users
```
Search: index=security | stats count by User | top 10
Visualization: Bar Chart
Shows: Most active users
```

### Panel 5: Top 10 Source IPs
```
Search: index=security | stats count by SourceIP | top 10
Visualization: Table
Shows: IPs with most events
```

### Panel 6: Alert Status
```
Search: index=main name=alert_fired | stats count
Visualization: Single Value
Color: Red if > 10 alerts
```

---

## 🎯 Dashboard 2: Threat Hunting

**Purpose**: Detailed investigation dashboard

### Panel 1: Suspicious Process Execution
```
Search: index=windows EventID=1 (Image=*cmd.exe* OR Image=*powershell.exe*)
Visualization: Table
Fields: Computer, Image, CommandLine, User, TimeCreated
```

### Panel 2: Network Connections (Top 20)
```
Search: index=windows EventID=3 | stats count by DestinationIp | sort - count | head 20
Visualization: Table
Shows: Top destination IPs
```

### Panel 3: Registry Modifications
```
Search: index=windows EventID=13 | stats count by TargetObject | sort - count | head 20
Visualization: Table
Shows: Most modified registry keys
```

### Panel 4: Failed Logins by Source IP
```
Search: index=security EventCode=4625 | timechart count by SourceIP limit=10
Visualization: Line Chart
Shows: Trends of failed logins by IP
```

### Panel 5: Process Access to LSASS
```
Search: index=windows EventID=10 TargetImage=*lsass.exe* | stats count by Computer, SourceImage
Visualization: Table
Shows: Processes accessing LSASS
```

### Panel 6: Lateral Movement Indicators
```
Search: index=windows EventID=3 (DestinationPort=445 OR DestinationPort=139) | stats dc(DestinationIp) by Computer
Visualization: Table
Shows: Computers connecting to multiple hosts
```

---

## 📈 Dashboard 3: Security Metrics

**Purpose**: KPI and compliance tracking

### Panel 1: Login Success Rate
```
Search: index=security (EventCode=4624 OR EventCode=4625) 
        | stats count(eval(EventCode=4624)) as successful, count(eval(EventCode=4625)) as failed
        | eval success_rate=round((successful/(successful+failed))*100,2)
Visualization: Gauge
Range: 0-100%
Color: Green > 90%, Yellow 70-90%, Red < 70%
```

### Panel 2: Top 10 Failing Accounts
```
Search: index=security EventCode=4625 | stats count by TargetUserName | sort - count | head 10
Visualization: Bar Chart
Shows: Accounts with most failed logins
```

### Panel 3: Security Events Trend
```
Search: index=security EventCode=4625 OR EventCode=4720 | timechart count by EventCode
Visualization: Line Chart
Shows: Trends over time
```

### Panel 4: Alerts Triggered
```
Search: index=main name=*alert* | stats count by name | sort - count
Visualization: Bar Chart
Shows: Most frequently triggered alerts
```

### Panel 5: Detection Rule Performance
```
Search: index=main name=*alert* | stats count as triggered_count by name
Visualization: Table with columns:
  - Alert Name
  - Triggered Count
  - Last Triggered
```

### Panel 6: Event Volume Forecast
```
Search: index=security | timechart count | predict count future_timespan=24
Visualization: Line Chart
Shows: Predicted events for next 24 hours
```

---

## 🖱️ How to Create Dashboard in Splunk

### Method 1: From Search Result
```
1. Run search
2. Results appear
3. Click "Visualizations" tab
4. Select visualization type
5. Click "Save As" → "Dashboard Panel"
6. Name: "Panel Name"
7. Dashboard: "Create New"
8. Dashboard Name: "Dashboard Title"
9. Click "Save"
```

### Method 2: Create Blank Dashboard
```
1. Click "Dashboards" (top menu)
2. Click "Create New Dashboard"
3. Name: "Dashboard Name"
4. Owner: "Private"
5. Click "Create Dashboard"
6. Click "Edit" button
7. Click "Add Panel"
8. Enter search or select existing panel
9. Click "Add Panel"
10. Click "Save"
```

---

## 📊 Dashboard Refresh Settings

```
1. Open Dashboard
2. Click settings icon (gear)
3. Refresh: "Every 30 seconds" (for real-time)
4. Time Range: "Last 24 hours"
5. Click "Apply"
```

---

## ✅ Phase 9 Verification Checklist

- ✅ SOC Overview dashboard created (6 panels)
- ✅ Threat Hunting dashboard created (6 panels)
- ✅ Security Metrics dashboard created (6 panels)
- ✅ All panels showing data
- ✅ Dashboards refreshing in real-time
- ✅ Can modify dashboard layouts
- ✅ Understand panel types
- ✅ Time ranges configured
- ✅ Saved as private dashboards

---

## 📄 Files in This Phase

See `09-Dashboards/` for:
- `soc-overview-dashboard.json` - SOC Overview definition
- `threat-hunting-dashboard.json` - Threat Hunting definition
- `security-metrics-dashboard.json` - Metrics definition
- `dashboard-installation.md` - Import instructions

---

## 🎓 What You Learned

✅ Dashboard design principles
✅ Visualization selection
✅ Real-time monitoring
✅ KPI tracking
✅ Executive reporting
✅ Dashboard customization

---

## ↩️ Next Phase

Phase 10: Attack Simulation

Time to test your detections! 🎯