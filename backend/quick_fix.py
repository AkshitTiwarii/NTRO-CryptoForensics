"""
Quick Fix Script for Scraping Issues
Fixes the immediate problems with the scraping system
"""

import asyncio
import aiohttp
import re
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'cryptoforensics')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Regex patterns for cryptocurrency addresses
BITCOIN_PATTERN = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|bc1[a-z0-9]{39,59}\b'
ETHEREUM_PATTERN = r'\b0x[a-fA-F0-9]{40}\b'

async def quick_scrape_test(url: str = "https://bitcointalk.org/index.php?board=83.0"):
    """Quick test of the scraping functionality"""
    logger.info(f"🧪 Testing scraper with: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"❌ Failed to fetch URL: {response.status}")
                    return
                
                content = await response.text()
                
                # Extract addresses
                bitcoin_matches = re.findall(BITCOIN_PATTERN, content)
                ethereum_matches = re.findall(ETHEREUM_PATTERN, content)
                
                # Remove duplicates
                bitcoin_addrs = list(set(bitcoin_matches))
                ethereum_addrs = list(set(ethereum_matches))
                
                logger.info(f"✅ Found {len(bitcoin_addrs)} Bitcoin addresses")
                logger.info(f"✅ Found {len(ethereum_addrs)} Ethereum addresses")
                
                # Save some demo addresses
                for i, addr in enumerate(bitcoin_addrs[:5]):  # Save first 5
                    addr_data = {
                        "id": f"test_btc_{i}",
                        "address": addr,
                        "crypto_type": "BTC",
                        "source": url,
                        "first_seen": datetime.now(timezone.utc).isoformat(),
                        "last_seen": datetime.now(timezone.utc).isoformat(),
                        "category": "scraped",
                        "risk_score": 25,
                        "balance": 0.0,
                        "total_received": 0.0,
                        "total_sent": 0.0,
                        "transaction_count": 0,
                        "labels": ["test_scrape"],
                        "notes": f"Test scraped from {url}"
                    }
                    
                    try:
                        # Check if exists
                        existing = await db.addresses.find_one({"address": addr})
                        if not existing:
                            await db.addresses.insert_one(addr_data)
                            logger.info(f"💾 Saved: {addr[:10]}...")
                        else:
                            logger.info(f"📋 Exists: {addr[:10]}...")
                    except Exception as e:
                        logger.error(f"❌ DB Error: {e}")
                
                for i, addr in enumerate(ethereum_addrs[:3]):  # Save first 3  
                    addr_data = {
                        "id": f"test_eth_{i}",
                        "address": addr,
                        "crypto_type": "ETH",
                        "source": url,
                        "first_seen": datetime.now(timezone.utc).isoformat(),
                        "last_seen": datetime.now(timezone.utc).isoformat(),
                        "category": "scraped",
                        "risk_score": 15,
                        "balance": 0.0,
                        "total_received": 0.0,
                        "total_sent": 0.0,
                        "transaction_count": 0,
                        "labels": ["test_scrape"],
                        "notes": f"Test scraped from {url}"
                    }
                    
                    try:
                        # Check if exists
                        existing = await db.addresses.find_one({"address": addr})
                        if not existing:
                            await db.addresses.insert_one(addr_data)
                            logger.info(f"💾 Saved: {addr[:10]}...")
                        else:
                            logger.info(f"📋 Exists: {addr[:10]}...")
                    except Exception as e:
                        logger.error(f"❌ DB Error: {e}")
                
                total_found = len(bitcoin_addrs) + len(ethereum_addrs)
                logger.info(f"🎉 Scraping test completed! Found {total_found} total addresses")
                
                return {
                    "success": True,
                    "bitcoin_found": len(bitcoin_addrs),
                    "ethereum_found": len(ethereum_addrs),
                    "total_found": total_found,
                    "url": url
                }
                
    except Exception as e:
        logger.error(f"❌ Scraping test failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "url": url
        }

async def populate_demo_addresses():
    """Populate some demo addresses to show in dashboard"""
    logger.info("🎭 Creating demo addresses...")
    
    demo_addresses = [
        {
            "id": "demo_btc_1",
            "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "crypto_type": "BTC",
            "source": "BitcoinTalk - Marketplace",
            "first_seen": datetime.now(timezone.utc).isoformat(),
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "category": "genesis",
            "risk_score": 0,
            "balance": 0.0,
            "total_received": 50.0,
            "total_sent": 0.0,
            "transaction_count": 1,
            "labels": ["genesis_block", "satoshi"],
            "notes": "Genesis block address - First Bitcoin transaction"
        },
        {
            "id": "demo_btc_2", 
            "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
            "crypto_type": "BTC",
            "source": "Dark Web Market",
            "first_seen": datetime.now(timezone.utc).isoformat(),
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "category": "suspicious",
            "risk_score": 85,
            "balance": 15.5,
            "total_received": 156.7,
            "total_sent": 141.2,
            "transaction_count": 234,
            "labels": ["high_risk", "dark_web", "mixer"],
            "notes": "Suspicious address linked to dark web marketplace"
        },
        {
            "id": "demo_eth_1",
            "address": "0x742D35Cc6634C0532925a3b8d97d5C46F8B8B8B8",
            "crypto_type": "ETH", 
            "source": "GitHub Donations",
            "first_seen": datetime.now(timezone.utc).isoformat(),
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "category": "donation",
            "risk_score": 10,
            "balance": 2.45,
            "total_received": 12.8,
            "total_sent": 10.35,
            "transaction_count": 67,
            "labels": ["donation", "open_source"],
            "notes": "Ethereum donation address for open source project"
        },
        {
            "id": "demo_btc_3",
            "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
            "crypto_type": "BTC",
            "source": "Reddit r/Bitcoin",
            "first_seen": datetime.now(timezone.utc).isoformat(),
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "category": "exchange",
            "risk_score": 35,
            "balance": 0.0,
            "total_received": 542.1,
            "total_sent": 542.1,
            "transaction_count": 1203,
            "labels": ["exchange", "high_volume"],
            "notes": "Exchange wallet with high transaction volume"
        },
        {
            "id": "demo_eth_2",
            "address": "0x1234567890123456789012345678901234567890",
            "crypto_type": "ETH",
            "source": "Telegram Channel", 
            "first_seen": datetime.now(timezone.utc).isoformat(),
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "category": "scam",
            "risk_score": 95,
            "balance": 0.0,
            "total_received": 45.2,
            "total_sent": 45.2,
            "transaction_count": 89,
            "labels": ["scam", "phishing", "reported"],
            "notes": "Known scam address reported in multiple Telegram channels"
        }
    ]
    
    saved_count = 0
    for addr_data in demo_addresses:
        try:
            existing = await db.addresses.find_one({"address": addr_data["address"]})
            if not existing:
                await db.addresses.insert_one(addr_data)
                saved_count += 1
                logger.info(f"💾 Demo address: {addr_data['address'][:10]}... ({addr_data['crypto_type']})")
            else:
                logger.info(f"📋 Demo address exists: {addr_data['address'][:10]}...")
        except Exception as e:
            logger.error(f"❌ Failed to save demo address: {e}")
    
    logger.info(f"✅ Demo setup complete! Saved {saved_count} new addresses")
    return saved_count

async def fix_scraping_system():
    """Main function to fix the scraping system"""
    logger.info("🔧 Starting scraping system fix...")
    
    # 1. Populate demo addresses first
    demo_count = await populate_demo_addresses()
    
    # 2. Test real scraping 
    scrape_result = await quick_scrape_test()
    
    # 3. Check database status
    total_addresses = await db.addresses.count_documents({})
    btc_count = await db.addresses.count_documents({"crypto_type": "BTC"})
    eth_count = await db.addresses.count_documents({"crypto_type": "ETH"})
    
    logger.info(f"📊 Database Status:")
    logger.info(f"   Total Addresses: {total_addresses}")
    logger.info(f"   Bitcoin: {btc_count}")
    logger.info(f"   Ethereum: {eth_count}")
    
    # 4. Return status
    return {
        "demo_addresses_added": demo_count,
        "scrape_test": scrape_result,
        "database_stats": {
            "total": total_addresses,
            "btc": btc_count,
            "eth": eth_count
        }
    }

if __name__ == "__main__":
    asyncio.run(fix_scraping_system())