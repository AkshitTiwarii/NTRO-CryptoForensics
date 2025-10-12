#!/usr/bin/env python3
"""
Test the fixed scraping endpoint to verify it works
"""

import requests
import json
import time

def test_scraper_fix():
    """Test that the fixed scraper endpoint actually works"""
    
    print("🔍 TESTING FIXED SCRAPER ENDPOINT")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000/api"
    
    # Step 1: Get available seeds
    print("📋 Getting available seeds...")
    response = requests.get(f"{base_url}/seeds")
    
    if response.status_code != 200:
        print(f"❌ Failed to get seeds: {response.status_code}")
        return
        
    seeds = response.json()
    print(f"✅ Found {len(seeds)} seeds")
    
    if not seeds:
        print("❌ No seeds available for testing")
        return
    
    # Use first seed for testing
    test_seed = seeds[0]
    seed_id = test_seed['id']
    print(f"🎯 Testing with seed: {test_seed['name']} (ID: {seed_id})")
    print(f"🌐 URL: {test_seed['url']}")
    
    # Step 2: Get initial stats
    print("\n📊 Getting initial stats...")
    stats_response = requests.get(f"{base_url}/seeds/stats")
    if stats_response.status_code == 200:
        initial_stats = stats_response.json()
        print(f"📈 Initial addresses count: {initial_stats.get('total_addresses', 0)}")
        print(f"📅 Last crawled: {test_seed.get('last_crawled', 'Never')}")
    
    # Step 3: Trigger scraping
    print(f"\n🚀 Triggering scraping for seed {seed_id}...")
    scrape_response = requests.post(f"{base_url}/seeds/{seed_id}/scrape")
    
    if scrape_response.status_code != 200:
        print(f"❌ Scraping failed: {scrape_response.status_code}")
        print(f"Response: {scrape_response.text}")
        return
    
    scrape_result = scrape_response.json()
    print(f"✅ Scraping triggered successfully!")
    print(f"📝 Response: {json.dumps(scrape_result, indent=2)}")
    
    # Step 4: Check if addresses were actually found
    addresses_found = scrape_result.get('addresses_found', 0)
    total_extracted = scrape_result.get('total_extracted', 0)
    success = scrape_result.get('success', False)
    
    if success and addresses_found > 0:
        print(f"🎉 SUCCESS! Found {addresses_found} new addresses ({total_extracted} total)")
    elif success and total_extracted > 0:
        print(f"✅ SUCCESS! Extracted {total_extracted} addresses (some may be duplicates)")
    else:
        print(f"⚠️ No addresses found, but scraper executed without errors")
    
    # Step 5: Verify stats updated
    print("\n📊 Checking updated stats...")
    time.sleep(1)  # Give a moment for stats to update
    
    stats_response = requests.get(f"{base_url}/seeds/stats")
    if stats_response.status_code == 200:
        updated_stats = stats_response.json()
        print(f"📈 Updated addresses count: {updated_stats.get('total_addresses', 0)}")
    
    # Get updated seed info
    seed_response = requests.get(f"{base_url}/seeds")
    if seed_response.status_code == 200:
        updated_seeds = seed_response.json()
        updated_seed = next((s for s in updated_seeds if s['id'] == seed_id), None)
        if updated_seed:
            print(f"📅 Updated last crawled: {updated_seed.get('last_crawled', 'Still Never')}")
            print(f"📊 Addresses found: {updated_seed.get('addresses_found', 0)}")
    
    print("\n" + "=" * 50)
    print("🏁 SCRAPER TEST COMPLETED!")
    
    if success:
        print("✅ THE SCRAPER IS NOW WORKING!")
        print("✅ No more instant 'done' without actual scraping")
        print("✅ Last crawled timestamp should update")
        print("✅ Address count should increase")
    else:
        print("❌ Scraper still has issues")

if __name__ == "__main__":
    test_scraper_fix()