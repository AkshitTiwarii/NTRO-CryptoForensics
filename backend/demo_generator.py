"""
Demo Address Generator
Generates realistic cryptocurrency addresses for demonstration
"""

import random
import hashlib
import base58
import asyncio
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class DemoAddressGenerator:
    """Generate realistic demo cryptocurrency addresses"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    def generate_bitcoin_address(self) -> str:
        """Generate a realistic Bitcoin address"""
        # Generate random bytes for address
        private_key = random.randbytes(32)
        # Simple address generation (not cryptographically secure, just for demo)
        address_bytes = hashlib.sha256(private_key).digest()[:20]
        # Add version byte and checksum for P2PKH address
        versioned = b'\x00' + address_bytes
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        full_address = versioned + checksum
        return base58.b58encode(full_address).decode()
    
    def generate_ethereum_address(self) -> str:
        """Generate a realistic Ethereum address"""
        # Generate random 20 bytes for Ethereum address
        address_bytes = random.randbytes(20)
        return '0x' + address_bytes.hex()
    
    def generate_demo_addresses(self, count: int = 50) -> List[Dict]:
        """Generate demo addresses with realistic metadata"""
        addresses = []
        sources = [
            "BitcoinTalk - Marketplace", "Reddit r/Bitcoin", "GitHub Donations",
            "Pastebin Bitcoin Search", "CoinDesk - Crime Tag", "Dark Web Market",
            "Telegram Channel", "Discord Server", "Twitter Post", "Forum Discussion"
        ]
        
        categories = ["exchange", "mixer", "gambling", "mining", "donation", "personal", "merchant", "unknown"]
        
        for i in range(count):
            # Generate addresses (70% Bitcoin, 30% Ethereum)
            if random.random() < 0.7:
                address = self.generate_bitcoin_address()
                currency = "BTC"
            else:
                address = self.generate_ethereum_address()
                currency = "ETH"
            
            # Generate realistic metadata
            created_time = datetime.now(timezone.utc) - timedelta(
                days=random.randint(1, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            addr_data = {
                "id": f"demo_{i+1}",
                "address": address,
                "crypto_type": currency,
                "source": random.choice(sources),
                "first_seen": created_time.isoformat(),
                "last_seen": created_time.isoformat(),
                "category": random.choice(categories),
                "risk_score": random.randint(0, 100),
                "balance": round(random.uniform(0, 100), 8),
                "total_received": round(random.uniform(0, 1000), 8),
                "total_sent": round(random.uniform(0, 500), 8),
                "transaction_count": random.randint(1, 500),
                "labels": random.sample(["exchange", "mixer", "gambling", "scam", "donation", "cold_storage"], 
                                      random.randint(0, 3)),
                "notes": f"Demo address from {random.choice(sources)}",
                "source_type": "demo_generator"
            }
            
            addresses.append(addr_data)
        
        return addresses
    
    async def populate_demo_data(self, count: int = 50):
        """Populate database with demo addresses"""
        logger.info(f"🎭 Generating {count} demo addresses...")
        
        # Check if demo data already exists
        existing_count = await self.db.addresses.count_documents({"source_type": "demo_generator"})
        if existing_count > 0:
            logger.info(f"Demo data already exists ({existing_count} addresses). Skipping...")
            return existing_count
        
        # Generate demo addresses
        demo_addresses = self.generate_demo_addresses(count)
        
        # Insert into database
        if demo_addresses:
            result = await self.db.addresses.insert_many(demo_addresses)
            logger.info(f"✅ Inserted {len(result.inserted_ids)} demo addresses")
            return len(result.inserted_ids)
        
        return 0
    
    async def clear_demo_data(self):
        """Clear demo data from database"""
        result = await self.db.addresses.delete_many({"source_type": "demo_generator"})
        logger.info(f"🗑️ Cleared {result.deleted_count} demo addresses")
        return result.deleted_count

# Demo threat personas for intelligence correlation
DEMO_THREAT_PERSONAS = [
    {
        "persona_id": "threat_001",
        "primary_identifier": "CryptoLaunderer_X",
        "confidence_score": 0.85,
        "threat_level": "HIGH",
        "crypto_wallets": ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "0x742D35Cc6634C0532925a3b8d97d5C46F8B8B8B"],
        "email_addresses": ["suspicious@protonmail.com"],
        "telegram_handles": ["@cryptomixer_pro"],
        "attack_vectors": ["mixing_services", "chain_hopping", "privacy_coins"],
        "first_activity": "2023-01-15T10:30:00Z",
        "last_activity": "2024-10-01T15:45:00Z",
        "behavioral_patterns": {
            "transaction_timing": "late_night",
            "amount_patterns": "round_numbers",
            "mixing_preference": "tornado_cash"
        }
    },
    {
        "persona_id": "threat_002",
        "primary_identifier": "DarkMarket_Vendor",
        "confidence_score": 0.72,
        "threat_level": "CRITICAL",
        "crypto_wallets": ["bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", "0x8ba1f109551bD432803012645Hac136c22C"],
        "email_addresses": ["vendor123@tutanota.com"],
        "telegram_handles": ["@darkvendor", "@market_supplier"],
        "attack_vectors": ["drug_trafficking", "weapon_sales", "stolen_data"],
        "first_activity": "2022-08-20T09:15:00Z",
        "last_activity": "2024-09-28T20:30:00Z",
        "behavioral_patterns": {
            "transaction_timing": "random",
            "amount_patterns": "varied_small",
            "communication": "encrypted_channels"
        }
    },
    {
        "persona_id": "threat_003",
        "primary_identifier": "RansomwareGroup_Alpha",
        "confidence_score": 0.91,
        "threat_level": "CRITICAL",
        "crypto_wallets": ["1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2", "0x1234567890123456789012345678901234567890"],
        "email_addresses": ["payment@ransomgroup.dark"],
        "telegram_handles": ["@ransom_payments"],
        "attack_vectors": ["ransomware", "data_encryption", "extortion"],
        "first_activity": "2023-05-10T14:20:00Z",
        "last_activity": "2024-10-05T11:00:00Z",
        "behavioral_patterns": {
            "transaction_timing": "business_hours",
            "amount_patterns": "large_payments",
            "payment_method": "bitcoin_only"
        }
    }
]

async def populate_demo_threat_personas(db: AsyncIOMotorDatabase):
    """Populate database with demo threat personas"""
    existing_count = await db.threat_personas.count_documents({})
    if existing_count > 0:
        logger.info(f"Threat persona data already exists ({existing_count} personas). Skipping...")
        return existing_count
    
    if DEMO_THREAT_PERSONAS:
        result = await db.threat_personas.insert_many(DEMO_THREAT_PERSONAS)
        logger.info(f"✅ Inserted {len(result.inserted_ids)} demo threat personas")
        return len(result.inserted_ids)
    
    return 0

# Demo communication data
DEMO_COMMUNICATIONS = [
    {
        "id": "comm_001",
        "sender": "cryptolaunderer_x",
        "recipient": "money_mixer_pro",
        "platform": "telegram",
        "timestamp": "2024-10-01T15:30:00Z",
        "content_type": "text",
        "extracted_addresses": ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"],
        "risk_indicators": ["money_laundering", "mixing_service"]
    },
    {
        "id": "comm_002",
        "sender": "darkvendor123",
        "recipient": "customer_buyer",
        "platform": "dark_forum",
        "timestamp": "2024-09-28T20:15:00Z",
        "content_type": "encrypted",
        "extracted_addresses": ["bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"],
        "risk_indicators": ["illegal_marketplace", "drug_trafficking"]
    },
    {
        "id": "comm_003",
        "sender": "ransom_payment_bot",
        "recipient": "victim_company",
        "platform": "email",
        "timestamp": "2024-10-05T11:00:00Z",
        "content_type": "ransom_note",
        "extracted_addresses": ["1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"],
        "risk_indicators": ["ransomware", "extortion", "cybercrime"]
    }
]

async def populate_demo_communications(db: AsyncIOMotorDatabase):
    """Populate database with demo communications"""
    existing_count = await db.communications.count_documents({})
    if existing_count > 0:
        logger.info(f"Communication data already exists ({existing_count} records). Skipping...")
        return existing_count
    
    if DEMO_COMMUNICATIONS:
        result = await db.communications.insert_many(DEMO_COMMUNICATIONS)
        logger.info(f"✅ Inserted {len(result.inserted_ids)} demo communications")
        return len(result.inserted_ids)
    
    return 0

async def setup_complete_demo_environment(db: AsyncIOMotorDatabase):
    """Set up complete demo environment with all data types"""
    logger.info("🎭 Setting up complete demo environment...")
    
    # Generate demo addresses
    generator = DemoAddressGenerator(db)
    addresses_count = await generator.populate_demo_data(100)
    
    # Generate demo threat personas
    personas_count = await populate_demo_threat_personas(db)
    
    # Generate demo communications
    comms_count = await populate_demo_communications(db)
    
    logger.info(f"✅ Demo environment setup complete!")
    logger.info(f"   📊 Addresses: {addresses_count}")
    logger.info(f"   👤 Threat Personas: {personas_count}")
    logger.info(f"   💬 Communications: {comms_count}")
    
    return {
        "addresses": addresses_count,
        "threat_personas": personas_count,
        "communications": comms_count
    }

if __name__ == "__main__":
    import asyncio
    from motor.motor_asyncio import AsyncIOMotorClient
    import os
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'cryptoforensics')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    asyncio.run(setup_complete_demo_environment(db))