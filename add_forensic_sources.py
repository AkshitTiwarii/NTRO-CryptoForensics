#!/usr/bin/env python3
"""
Add Real Deep/Dark Web Sources for Cryptocurrency Forensics
This adds legitimate forensic sources focusing on cryptocurrency investigations
"""

import asyncio
import requests
import json

def add_forensic_sources():
    """Add real deep/dark web sources for cryptocurrency forensics"""
    
    print("🕵️ ADDING REAL FORENSIC CRYPTOCURRENCY SOURCES")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000/api"
    
    # Real forensic sources that contain cryptocurrency addresses
    forensic_sources = [
        {
            "name": "Bitcoin Abuse Database",
            "url": "https://www.bitcoinabuse.com/reports",
            "description": "🚨 Database of Bitcoin addresses used in criminal activities",
            "category": "forensic",
            "priority": 1,
            "frequency": "hourly",
            "deep_web": False,
            "enabled": True
        },
        {
            "name": "Cryptocurrency Investigations",
            "url": "https://www.elliptic.co/blog",
            "description": "🔍 Professional cryptocurrency investigation reports",
            "category": "forensic",
            "priority": 2,
            "frequency": "daily",
            "deep_web": False,
            "enabled": True
        },
        {
            "name": "Blockchain Investigation Reports",
            "url": "https://www.chainalysis.com/blog",
            "description": "📊 Blockchain analysis and investigation reports",
            "category": "forensic",
            "priority": 2,
            "frequency": "daily", 
            "deep_web": False,
            "enabled": True
        },
        {
            "name": "Crypto Crime Reports",
            "url": "https://ciphertrace.com/cryptocurrency-crime-and-anti-money-laundering-report",
            "description": "💰 Cryptocurrency crime and AML investigation reports",
            "category": "forensic",
            "priority": 3,
            "frequency": "weekly",
            "deep_web": False,
            "enabled": True
        },
        {
            "name": "OFAC Sanctions List",
            "url": "https://home.treasury.gov/policy-issues/financial-sanctions/specially-designated-nationals-and-blocked-persons-list-sdn-human-readable-lists",
            "description": "🏛️ US Treasury sanctioned cryptocurrency addresses",
            "category": "government",
            "priority": 1,
            "frequency": "weekly",
            "deep_web": False,
            "enabled": True
        },
        {
            "name": "FBI IC3 Crypto Reports",
            "url": "https://www.ic3.gov/Media/Y2023/PSA231215",
            "description": "🏛️ FBI Internet Crime Complaint Center crypto reports",
            "category": "government",
            "priority": 2,
            "frequency": "weekly",
            "deep_web": False,
            "enabled": True
        },
        {
            "name": "DarkWeb Forums (Sample)",
            "url": "dread.onion",  # Note: This is a placeholder for demo
            "description": "🕸️ Deep web forum discussions about cryptocurrency",
            "category": "darkweb",
            "priority": 4,
            "frequency": "daily",
            "deep_web": True,
            "enabled": False  # Disabled by default for safety
        },
        {
            "name": "Tor Network Analysis",
            "url": "i2p-forums.example",  # Note: This is a placeholder for demo
            "description": "🧅 I2P network cryptocurrency discussions",
            "category": "deepweb",
            "priority": 5,
            "frequency": "weekly",
            "deep_web": True,
            "enabled": False  # Disabled by default for safety
        }
    ]
    
    # Add each source
    added_count = 0
    for source in forensic_sources:
        try:
            print(f"📋 Adding: {source['name']}")
            
            response = requests.post(f"{base_url}/seeds", json=source)
            
            if response.status_code == 200:
                print(f"✅ Added: {source['name']}")
                added_count += 1
            else:
                print(f"⚠️ Warning: {source['name']} - {response.status_code}")
                
        except Exception as e:
            print(f"❌ Failed to add {source['name']}: {e}")
    
    print(f"\n✅ Added {added_count} new forensic sources!")
    print("\n🔍 FORENSIC CAPABILITIES:")
    print("✅ Surface Web: Professional investigation reports")
    print("✅ Government Sources: Official sanctions and warnings")
    print("⚠️ Deep Web: Sample sources (disabled for safety)")
    print("⚠️ Dark Web: Sample sources (disabled for safety)")
    print("\n📊 The system now focuses on REAL cryptocurrency forensic data!")

if __name__ == "__main__":
    add_forensic_sources()