#!/usr/bin/env python3
"""Test AI Analysis Endpoint"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("🔐 Step 1: Login...")
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "password": "admin123"
})

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ Login successful! Token: {token[:30]}...")

print("\n📊 Step 2: Get addresses...")
addresses_response = requests.get(f"{BASE_URL}/addresses", headers=headers)
if addresses_response.status_code != 200:
    print(f"❌ Failed to get addresses: {addresses_response.text}")
    exit(1)

addresses_data = addresses_response.json()
# Handle both list and dict response formats
if isinstance(addresses_data, list):
    addresses = addresses_data
elif isinstance(addresses_data, dict) and "addresses" in addresses_data:
    addresses = addresses_data["addresses"]
else:
    addresses = []
    
print(f"✅ Found {len(addresses)} addresses")

# Filter high-risk addresses
high_risk = [a for a in addresses if a.get("risk_score", 0) > 70]
print(f"🎯 Found {len(high_risk)} high-risk addresses (risk > 70)")

if not high_risk:
    print("⚠️  No high-risk addresses found. Please run scraping first or add test data.")
    print("   Try running: python add_high_risk_addresses.py")
    exit(0)

# Get first 2 high-risk addresses for testing
test_ids = [a["id"] for a in high_risk[:2]]
print(f"\n🧪 Step 3: Testing AI analysis with {len(test_ids)} addresses...")
print(f"   Address IDs: {test_ids}")

# Test the AI endpoint
ai_response = requests.post(
    f"{BASE_URL}/ai/analyze/bulk",
    headers=headers,
    json={"address_ids": test_ids}
)

print(f"\n📡 Response Status: {ai_response.status_code}")

if ai_response.status_code == 200:
    result = ai_response.json()
    print("✅ AI Analysis successful!")
    print(f"\n📊 Full Response:")
    print(f"   {json.dumps(result, indent=2)}")
    
    # Check both possible key names
    analysis_results = result.get('results') or result.get('analysis_results', [])
    
    print(f"\n📊 Results Summary:")
    print(f"   Total analyzed: {result.get('analyzed_count', len(analysis_results))}")
    
    for i, analysis in enumerate(analysis_results[:2], 1):
        print(f"\n   [{i}] Address: {analysis.get('address', 'N/A')[:30]}...")
        print(f"       Risk Score: {analysis.get('risk_score', 'N/A')}/100")
        print(f"       Confidence: {analysis.get('confidence', 'N/A')}%")
        if analysis.get('risk_factors'):
            print(f"       Risk Factors: {', '.join(analysis['risk_factors'][:3])}")
        if analysis.get('findings'):
            print(f"       Findings: {', '.join(analysis['findings'][:2])}")
else:
    print(f"❌ AI Analysis failed!")
    print(f"   Error: {ai_response.text}")
    
print("\n✨ Test complete!")
