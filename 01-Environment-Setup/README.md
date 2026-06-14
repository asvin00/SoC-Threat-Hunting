# Phase 1: Environment Setup 🖥️

## Virtual Machine Configuration & Network Setup

This phase involves creating and configuring 3 virtual machines with proper networking.

---

## ⏱️ Time Estimate: 2-3 hours

---

## 📋 Prerequisites

✅ VirtualBox installed (6.1+)
✅ 8GB RAM minimum (16GB recommended)
✅ 100GB free disk space
✅ Downloaded ISO files:
  - Ubuntu 26.04 LTS (3-4 GB)
  - Windows 11 (5-6 GB)
  - Kali Linux VirtualBox (3-4 GB)

---

## 🎯 Learning Objectives

After this phase:
- ✅ Create 3 VirtualBox VMs
- ✅ Configure networking (Host-Only Adapter)
- ✅ Set static IPs
- ✅ Verify connectivity between VMs
- ✅ Create backups (snapshots)

---

## 📊 VM Specifications

### VM 1: Ubuntu Splunk Server
- **OS**: Ubuntu 26.04 LTS
- **IP**: 192.168.56.10
- **RAM**: 4GB
- **CPU**: 2 cores
- **Disk**: 50GB
- **Role**: SIEM (Splunk installation)

### VM 2: Windows Endpoint
- **OS**: Windows 11
- **IP**: 192.168.56.20
- **RAM**: 2GB
- **CPU**: 2 cores
- **Disk**: 60GB
- **Role**: Event source (Sysmon + Forwarder)

### VM 3: Kali Linux
- **OS**: Kali Linux
- **IP**: 192.168.56.30
- **RAM**: 2GB
- **CPU**: 2 cores
- **Disk**: Default (OVA import)
- **Role**: Attack simulator

---

## 🚀 Step-by-Step Setup

### STEP 1: Create Ubuntu VM

```bash
1. Open VirtualBox Manager
2. Click "New" button
3. Fill in:
   Name: Ubuntu-Splunk
   OS: Linux
   Version: Ubuntu (64-bit)
   Memory: 4096 MB
   CPU: 2 cores
   Disk: 50 GB (VDI)
4. Click "Create"
5. Select ISO: ubuntu-26.04-desktop-amd64.iso
6. Click "Start" to boot
```

**Installation Steps**:
```
1. Language: English
2. Keyboard: Your layout
3. Installation type: "Erase disk and install Ubuntu"
4. Timezone: Your location
5. Create account:
   Full Name: SOC Admin
   Computer name: ubuntu-soc
   Username: socadmin
   Password: Splunk@123
6. Wait 15-20 minutes
7. Restart when complete
```

**Verification**:
```bash
lsb_release -a
# Output: Ubuntu 26.04 LTS
```

---

### STEP 2: Configure Ubuntu Network

```bash
# Open Terminal: Ctrl+Alt+T

# Edit netplan configuration
sudo nano /etc/netplan/00-installer-config.yaml

# Replace all content with:
```

```yaml
network:
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 192.168.56.10/24
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
      routes:
        - to: 0.0.0.0/0
          via: 192.168.56.1
  version: 2
```

```bash
# Save: Ctrl+X → Y → Enter

# Apply configuration
sudo netplan apply

# Verify
ip addr show enp0s3 | grep "inet 192"
# Expected: inet 192.168.56.10/24
```

---

### STEP 3: Create Windows VM

```bash
1. Open VirtualBox Manager
2. Click "New"
3. Fill in:
   Name: Windows-Endpoint
   OS: Windows
   Version: Windows 11 (64-bit)
   Memory: 2048 MB
   CPU: 2 cores
   Disk: 60 GB (VDMK)
4. Configure Network BEFORE starting:
   Right-click VM → Settings → Network
   Adapter 1: Host-Only Adapter (vboxnet0)
   Promiscuous Mode: Allow All
   Click "OK"
5. Select Windows 11 ISO
6. Click "Start"
```

**Installation Steps**:
```
1. Language: English
2. Region: Your country
3. Keyboard: Your layout
4. Accept License
5. Installation type: Custom
6. Select Drive: Drive 0 Unallocated Space
7. Wait 20-30 minutes
8. Microsoft Account: Click "Offline account"
9. Create local account:
   Username: admin
   Password: Windows@123
10. Security questions: Answer 3 (any answers)
11. Complete setup
```

---

### STEP 4: Configure Windows Network

```powershell
# Right-click Network icon → Advanced network options
# Click "Change adapter options"
# Right-click "Ethernet" → Properties
# Double-click "Internet Protocol Version 4 (TCP/IPv4)"

# Select "Use the following IP address"
# Enter:
IP Address: 192.168.56.20
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.56.1
Preferred DNS: 8.8.8.8
Alternate DNS: 8.8.4.4

# Click OK → OK

# Verify:
ipconfig /all
# Should show: IPv4 Address: 192.168.56.20
```

---

### STEP 5: Import Kali Linux

```bash
1. Download Kali VirtualBox OVA from:
   https://www.kali.org/get-kali/
   Download: Kali Linux (Bare Metal 64-bit)

2. In VirtualBox: File → Import Appliance

3. Select downloaded Kali OVA file

4. Review settings:
   Name: Kali-Attacker
   RAM: 2048 MB
   CPU: 2 cores
   Network: Host-Only (vboxnet0)

5. Click "Finish"

6. Start VM
```

**Default Kali Credentials**:
```
Username: kali
Password: kali
```

---

### STEP 6: Configure Kali Network

```bash
# Open Terminal

# Check interface name
ip link show
# Look for: eth0 or enp0s3

# Edit interfaces file
sudo nano /etc/network/interfaces

# Replace all with:
```

```bash
auto eth0
iface eth0 inet static
  address 192.168.56.30
  netmask 255.255.255.0
  gateway 192.168.56.1
  dns-nameservers 8.8.8.8 8.8.4.4
```

```bash
# Save: Ctrl+X → Y → Enter

# Restart network
sudo systemctl restart networking

# Verify
ip addr show eth0 | grep "inet 192"
# Expected: inet 192.168.56.30/24
```

---

## 🔗 Network Verification

### From Ubuntu Terminal:
```bash
ping -c 2 192.168.56.20  # Should reply from Windows
ping -c 2 192.168.56.30  # Should reply from Kali
```

### From Windows PowerShell:
```powershell
ping 192.168.56.10  # Should reply from Ubuntu
ping 192.168.56.30  # Should reply from Kali
```

### From Kali Terminal:
```bash
ping -c 2 192.168.56.10  # Should reply from Ubuntu
ping -c 2 192.168.56.20  # Should reply from Windows
```

**If Windows ping fails from Kali**:
```powershell
# On Windows (PowerShell as Admin):
netsh advfirewall firewall add rule name="Allow ICMP" dir=in action=allow protocol=icmpv4
```

---

## 💾 Create Snapshots

**For each VM - Right-click → Snapshots → Take Snapshot**

```
Ubuntu Snapshot: "Ubuntu-Clean-Install"
Windows Snapshot: "Windows-Clean-Install"
Kali Snapshot: "Kali-Clean-Install"
```

These snapshots allow you to restore if something breaks.

---

## ✅ Phase 1 Verification Checklist

- ☐ Ubuntu 26.04 installed
- ☐ Ubuntu IP: 192.168.56.10
- ☐ Windows 11 installed
- ☐ Windows IP: 192.168.56.20
- ☐ Kali Linux imported
- ☐ Kali IP: 192.168.56.30
- ☐ All VMs can ping each other (100% success)
- ☐ Snapshots created for all VMs
- ☐ All VMs run without major slowdown
- ☐ Disk space check: `df -h` shows sufficient space
- ☐ RAM usage: Total under 8GB

---

## 🆘 Troubleshooting

### Network not working
```
✅ Verify all VMs using Host-Only adapter (vboxnet0)
✅ Check IP addresses match 192.168.56.x/24
✅ Restart networking: sudo systemctl restart networking
✅ Check firewall: sudo ufw status
```

### VMs won't boot
```
✅ Check VirtualBox has enough RAM allocated
✅ Enable virtualization in BIOS
✅ Restart VirtualBox application
```

### Slow performance
```
✅ Reduce VM RAM/CPU if needed
✅ Use SSD for VM storage
✅ Run only 1-2 VMs at a time during testing
```

---

## 📁 Configuration Files

See `Configuration-Files/network-configs/` for:
- `ubuntu-netplan.yaml` - Ubuntu network config
- `windows-network.ps1` - Windows PowerShell script
- `kali-interfaces.conf` - Kali network config

---

## 🎓 What You Learned

✅ Virtual machine creation
✅ OS installation
✅ Static IP configuration
✅ Network connectivity
✅ VM snapshot backups

---

## ⏭️ Next Phase

Phase 2: Splunk Installation

Ready to install the SIEM? Let's go! 🚀