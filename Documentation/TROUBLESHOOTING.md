# Frequently Asked Questions

## Installation Issues

### Q: VirtualBox won't start VMs
A: Check that virtualization is enabled in BIOS. For AMD: AMD-V, for Intel: VT-x

### Q: Splunk stuck on loading screen
A: Kill splunkd process and restart:
```bash
sudo killall splunkd
sudo systemctl restart splunk
```

### Q: Forwarder not sending logs
A: Verify connectivity:
```powershell
Test-NetConnection 192.168.56.10 -Port 9997
```

## Configuration Issues

### Q: No events appearing in Splunk
A: Check:
1. Forwarder service running
2. Receiving port 9997 configured
3. Log files exist on Windows
4. Time synchronized between systems

### Q: Detection rules not triggering
A: Verify:
1. Events actually in index
2. Rule syntax correct
3. Threshold met
4. Alert enabled

## Performance Issues

### Q: Splunk running slow
A: Check disk space and RAM usage:
```bash
df -h
free -h
```

### Q: High CPU usage
A: Reduce search frequency or disable unused searches

## Network Issues

### Q: VMs can't ping each other
A: Verify network adapter:
1. All on Host-Only (vboxnet0)
2. Correct IP range (192.168.56.x)
3. Firewall not blocking
