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
            print("[✓] Data sent to Splunk successfully")
            return True
        else:
            print(f"[✗] Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"[✗] Exception: {e}")
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
