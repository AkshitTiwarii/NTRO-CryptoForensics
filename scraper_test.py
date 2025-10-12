#!/usr/bin/env python3
"""
Test web scraper with a proper HTML page
"""

import requests
import time

BASE_URL = "https://blockchain-sleuth-1.preview.emergentagent.com/api"
TOKEN = None

def get_auth_token():
    """Get authentication token"""
    global TOKEN
    login_data = {
        "username": "forensic_analyst_2025",
        "password": "SecureForensics@2025"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        TOKEN = data["token"]
        return True
    return False

def test_scraper_with_html():
    """Test scraper with HTML page that might contain crypto addresses"""
    if not TOKEN:
        print("❌ No authentication token")
        return False
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Use a test HTML page (Bitcoin.org homepage)
    test_url = "https://bitcoin.org"
    
    response = requests.post(f"{BASE_URL}/scraper/start", 
                           params={"target_url": test_url},
                           headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        job_id = data.get("job_id")
        print(f"✅ Scraper job started: {job_id}")
        
        # Wait for job to complete
        print("⏳ Waiting for scraper to complete...")
        time.sleep(5)
        
        # Check job status
        jobs_response = requests.get(f"{BASE_URL}/scraper/jobs", headers=headers)
        if jobs_response.status_code == 200:
            jobs = jobs_response.json()
            if jobs:
                latest_job = jobs[0]
                status = latest_job.get("status")
                addresses_found = latest_job.get("addresses_found", 0)
                error = latest_job.get("error")
                
                print(f"📊 Job Status: {status}")
                print(f"📍 Addresses Found: {addresses_found}")
                if error:
                    print(f"❌ Error: {error}")
                
                return status in ["completed", "running"]
        
    return False

if __name__ == "__main__":
    print("Testing Web Scraper with HTML page...")
    if get_auth_token():
        test_scraper_with_html()
    else:
        print("❌ Failed to authenticate")