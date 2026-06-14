#!/usr/bin/env python3
# threat-intel-enrichment.py
# Enriches logs with threat intelligence

import json

# Simple threat intel database
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
