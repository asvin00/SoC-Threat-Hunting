# Phase 2: Splunk Installation 🔧

## Install and Configure Splunk Enterprise SIEM

This phase involves downloading, installing, and configuring Splunk on Ubuntu.

---

## ⏱️ Time Estimate: 1-1.5 hours

---

## 📋 Prerequisites

✅ Ubuntu VM running (192.168.56.10)
✅ Internet connection
✅ ~10GB free disk space
✅ Terminal access with sudo privileges

---

## 🎯 Learning Objectives

After this phase:
- ✅ Download Splunk Enterprise
- ✅ Install Splunk service
- ✅ Configure receiving port (9997)
- ✅ Create indexes (security, windows)
- ✅ Access Splunk Web UI
- ✅ Enable boot-start

---

## 🚀 Step-by-Step Installation

### STEP 1: Update Ubuntu System

```bash
# Open Terminal on Ubuntu VM

sudo apt update
sudo apt upgrade -y
```

**Time**: ~5-10 minutes

---

### STEP 2: Download Splunk Enterprise

```bash
# Open Firefox
# Go to: https://www.splunk.com/en_us/download/splunk-enterprise.html

# Click "Free Download"
# Select:
#   Operating System: Linux
#   Architecture: 64-bit
#   Format: .tgz

# Click Download
# Save to ~/Downloads
```

**File**: splunk-9.x.x-linux-2.6_64-release.tgz (~435 MB)
**Time**: ~5-15 minutes (depends on internet)

---

### STEP 3: Move Splunk to /opt

```bash
# Open Terminal

cd /opt
sudo mv ~/Downloads/splunk*.tgz /opt/

# Verify
ls -lh /opt/splunk*.tgz
# Should show: ~435 MB file
```

---

### STEP 4: Extract Splunk

```bash
sudo tar -xzf /opt/splunk*.tgz -C /opt/

# Wait 2-3 minutes for extraction

# Verify
ls -la /opt/splunk/ | head -10
# Should show directories: bin, etc, lib, share, etc.
```

---

### STEP 5: Create Splunk User

```bash
sudo useradd -m -d /opt/splunk splunk
```

---

### STEP 6: Set Permissions

```bash
sudo chown -R splunk:splunk /opt/splunk/
```

---

### STEP 7: Start Splunk (Accept License)

```bash
sudo -u splunk /opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt

# Wait 5-10 minutes
# You'll see output:
#   Splunk> All in one. All in one.
#   Checking prerequisites...
#   Creating default configurations...
#   Starting splunkd...
#   Waiting for web server...
#   The Splunk web interface is at https://localhost:8000
```

---

### STEP 8: Verify Splunk Running

```bash
sudo -u splunk /opt/splunk/bin/splunk status

# Expected output:
# splunkd is running.
# Installed apps:
#   [list of apps]
```

---

### STEP 9: Access Splunk Web UI

```bash
# Open Firefox on Ubuntu
# Go to: https://localhost:8000

# Click "Advanced" → "Proceed anyway" (self-signed cert warning)
# You should see: Splunk login page
```

---

### STEP 10: Create Initial Admin User

```bash
# Back in Terminal:

sudo -u splunk /opt/splunk/bin/splunk add user admin \
  -password Splunk@123 \
  -role admin \
  -auth admin:changeme

# Press Enter when prompted
```

---

### STEP 11: Login to Splunk

```
Go back to Splunk Web (https://localhost:8000)

Username: admin
Password: Splunk@123

Click "Sign In"

You should see: Splunk dashboard
```

---

### STEP 12: Create "security" Index

```
1. Click Settings (top right)
2. Click "Indexes"
3. Click "New Index"
4. Index Name: security
5. Max raw size: 10000
6. Click "Save"
```

---

### STEP 13: Create "windows" Index

```
1. Click Settings
2. Click "Indexes"
3. Click "New Index"
4. Index Name: windows
5. Max raw size: 10000
6. Click "Save"
```

---

### STEP 14: Configure Receiving Port

```
1. Click Settings
2. Click "Forwarding and receiving"
3. Click "Configure receiving"
4. Click "New Receiving Port"
5. Listen on port: 9997
6. Click "Save"

Expected: Port 9997 configured successfully
```

---

### STEP 15: Enable Boot-Start

```bash
# In Terminal:

sudo /opt/splunk/bin/splunk enable boot-start \
  -auth admin:Splunk@123

# Verify:
sudo systemctl status splunk

# Expected: Active: active (running)
```

---

## ✅ Phase 2 Verification Checklist

- ☐ Splunk downloaded (~435 MB)
- ☐ Splunk extracted to /opt/splunk/
- ☐ Splunk user created
- ☐ Permissions set correctly
- ☐ Splunk service running
- ☐ Can access https://localhost:8000
- ☐ Can login with admin/Splunk@123
- ☐ Index "security" created
- ☐ Index "windows" created
- ☐ Receiving port 9997 configured
- ☐ Boot-start enabled
- ☐ Systemctl shows "Active: active"

---

## 🆘 Troubleshooting

### Splunk won't start
```bash
# Check disk space
df -h /

# Check logs
tail -100 /opt/splunk/var/log/splunk/splunkd.log

# Restart
sudo systemctl restart splunk

# Wait 2 minutes
sudo -u splunk /opt/splunk/bin/splunk status
```

### Can't access web UI
```bash
# Verify service running
sudo systemctl status splunk

# Check port listening
sudo netstat -tuln | grep 8000

# Restart Splunk
sudo systemctl restart splunk
```

### Firewall blocking
```bash
# Check firewall
sudo ufw status

# Allow ports
sudo ufw allow 8000
sudo ufw allow 9997
sudo ufw reload
```

---

## 📁 Configuration Files

See `02-Splunk-Installation/` directory for:
- `inputs.conf` - Data input configuration
- `outputs.conf` - Output configuration
- `indexes.conf` - Index definitions

---

## 🎓 What You Learned

✅ Splunk installation process
✅ Service configuration
✅ Index creation
✅ Receiving port setup
✅ Web UI access
✅ Boot-start configuration

---

## ⏭️ Next Phase

Phase 3: Sysmon Installation

Time to install Windows monitoring agent! 🚀