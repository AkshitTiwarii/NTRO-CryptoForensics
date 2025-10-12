"""
Test Scraping with Real API Calls
Tests the actual scraping endpoints
"""

import requests
import json
import time

API_BASE = "http://localhost:8000/api"

def test_scraping():
    """Test the scraping system"""
    print("🧪 Testing NTRO-CryptoForensics Scraping System")
    
    # 1. Check if seeds exist
    print("\n📋 Checking seeds...")
    try:
        response = requests.get(f"{API_BASE}/seeds")
        if response.status_code == 200:
            seeds = response.json()
            print(f"✅ Found {len(seeds['seeds'])} seeds")
            
            # Find an enabled seed to test
            enabled_seeds = [s for s in seeds['seeds'] if s['enabled']]
            if enabled_seeds:
                test_seed = enabled_seeds[0]
                print(f"🎯 Testing with seed: {test_seed['name']}")
                
                # 2. Trigger scraping
                print(f"\n🚀 Triggering scrape for seed ID {test_seed['id']}...")
                scrape_response = requests.post(f"{API_BASE}/seeds/{test_seed['id']}/scrape")
                
                if scrape_response.status_code == 200:
                    result = scrape_response.json()
                    print("✅ Scraping completed!")
                    print(f"   Addresses found: {result.get('addresses_found', 0)}")
                    print(f"   Total extracted: {result.get('total_extracted', 0)}")
                    print(f"   Success: {result.get('success', False)}")
                    print(f"   URL: {result.get('url', 'N/A')}")
                    
                    if result.get('error'):
                        print(f"   Error: {result['error']}")
                else:
                    print(f"❌ Scraping failed: {scrape_response.status_code}")
                    print(f"   Response: {scrape_response.text}")
                
                # 3. Check updated stats
                print("\n📊 Checking updated seed stats...")
                time.sleep(2)  # Wait for stats to update
                stats_response = requests.get(f"{API_BASE}/seeds/stats")
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    print(f"   Total addresses found: {stats.get('total_addresses_found', 0)}")
                    print(f"   Active seeds: {stats.get('enabled_seeds', 0)}")
                
                # 4. Check addresses in database
                print("\n📬 Checking addresses...")
                try:
                    # This endpoint might not exist, but let's try
                    addr_response = requests.get(f"{API_BASE}/addresses")
                    if addr_response.status_code == 200:
                        addresses = addr_response.json()
                        print(f"   Total addresses in DB: {len(addresses)}")
                    else:
                        print(f"   Addresses endpoint not available: {addr_response.status_code}")
                except:
                    print("   Could not check addresses endpoint")
                
            else:
                print("❌ No enabled seeds found for testing")
        else:
            print(f"❌ Failed to get seeds: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_scraping()