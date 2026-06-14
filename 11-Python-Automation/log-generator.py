#!/usr/bin/env python3
# log-generator.py
# Generates test security logs

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
