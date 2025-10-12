#!/usr/bin/env python3
"""Direct AI Engine Test"""
import asyncio
import sys
sys.path.append('C:\\Users\\akshi\\OneDrive\\Desktop\\PROJECTS\\Cryptodata\\CryptoData\\backend')

from ai_analysis_engine import crypto_ai

async def test_ai():
    print("🧪 Testing AI Analysis Engine...")
    
    # Test address
    test_address = {
        "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "crypto_type": "BTC",
        "risk_score": 85,
        "category": "darknet",
        "tags": ["suspicious", "high-value"]
    }
    
    print(f"\n📊 Analyzing: {test_address['address']}")
    print(f"   Risk Score: {test_address['risk_score']}")
    print(f"   Category: {test_address['category']}")
    
    try:
        result = await crypto_ai.analyze_address(test_address)
        print(f"\n✅ Analysis Complete!")
        print(f"   Risk Score: {result.risk_score}/100")
        print(f"   Confidence: {result.confidence}%")
        print(f"   Findings: {len(result.findings)}")
        if result.findings:
            print(f"\n📋 Sample Finding:")
            print(f"   {result.findings[0]}")
    except Exception as e:
        print(f"\n❌ Analysis Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ai())
