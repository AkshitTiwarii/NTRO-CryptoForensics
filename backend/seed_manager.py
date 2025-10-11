# Seed Manager - Manages autonomous crawling sources
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

class SeedManager:
    """Manages seed sources for autonomous crawling"""
    
    def __init__(self):
        self.seeds = []
        self._load_default_seeds()
    
    def _load_default_seeds(self):
        """Load pre-configured seed sources - REAL HIGH-VOLUME SITES"""
        default_seeds = [
            # ========== SURFACE WEB - HIGH VOLUME CRYPTO SITES ==========
            
            # Bitcoin Forums (VERY HIGH ADDRESS VOLUME)
            {
                "url": "https://bitcointalk.org/index.php?board=83.0",
                "category": "forum",
                "priority": 1,
                "frequency": "hourly",
                "enabled": True,
                "name": "BitcoinTalk - Marketplace",
                "description": "🔥 HIGHEST VOLUME - Marketplace with tons of BTC addresses"
            },
            {
                "url": "https://bitcointalk.org/index.php?board=159.0",
                "category": "forum",
                "priority": 2,
                "frequency": "daily",
                "enabled": True,
                "name": "BitcoinTalk - Scam Accusations",
                "description": "Reported scam addresses and fraudulent wallets"
            },
            
            # Reddit Crypto Communities (HIGH VOLUME)
            {
                "url": "https://old.reddit.com/r/Bitcoin/new/",
                "category": "social",
                "priority": 2,
                "frequency": "hourly",
                "enabled": True,
                "name": "Reddit r/Bitcoin",
                "description": "Active Bitcoin discussions with wallet addresses"
            },
            {
                "url": "https://old.reddit.com/r/CryptoCurrency/new/",
                "category": "social",
                "priority": 2,
                "frequency": "daily",
                "enabled": True,
                "name": "Reddit r/CryptoCurrency",
                "description": "Multi-crypto community with BTC/ETH addresses"
            },
            
            # GitHub Open Source (DONATION ADDRESSES)
            {
                "url": "https://github.com/topics/bitcoin-donation",
                "category": "code",
                "priority": 3,
                "frequency": "weekly",
                "enabled": True,
                "name": "GitHub Bitcoin Donations",
                "description": "Open source projects accepting Bitcoin donations"
            },
            {
                "url": "https://github.com/search?q=ethereum+donation&type=code",
                "category": "code",
                "priority": 3,
                "frequency": "weekly",
                "enabled": True,
                "name": "GitHub Ethereum Donations",
                "description": "Projects with Ethereum donation addresses"
            },
            
            # Pastebin Sites (LEAKED ADDRESSES, DUMPS)
            {
                "url": "https://pastebin.com/search?q=bitcoin+address",
                "category": "pastebin",
                "priority": 2,
                "frequency": "hourly",
                "enabled": True,
                "name": "Pastebin Bitcoin Search",
                "description": "Public pastes containing BTC addresses"
            },
            
            # Crypto News (CRIME & HACKS)
            {
                "url": "https://www.coindesk.com/tag/crime/",
                "category": "news",
                "priority": 1,
                "frequency": "daily",
                "enabled": True,
                "name": "CoinDesk - Crime Tag",
                "description": "Cryptocurrency crime news with involved addresses"
            },
            {
                "url": "https://cointelegraph.com/tags/hacks",
                "category": "news",
                "priority": 1,
                "frequency": "daily",
                "enabled": True,
                "name": "Cointelegraph - Hacks",
                "description": "Crypto hacking incidents with wallet addresses"
            },
            
            # Blockchain Explorers (LIVE TRANSACTIONS)
            {
                "url": "https://www.blockchain.com/explorer/blocks/btc",
                "category": "explorer",
                "priority": 2,
                "frequency": "hourly",
                "enabled": False,  # High load - enable manually
                "name": "Blockchain.com - Latest Blocks",
                "description": "⚠️ Live Bitcoin transactions (high volume)"
            },
            {
                "url": "https://etherscan.io/txs",
                "category": "explorer",
                "priority": 2,
                "frequency": "hourly",
                "enabled": False,  # High load - enable manually
                "name": "Etherscan - Latest Transactions",
                "description": "⚠️ Live Ethereum transactions (very high volume)"
            },
            
            # ========== DARK WEB (TOR .ONION SITES) ==========
            # For NTRO law enforcement use - requires Tor proxy setup
            # See TOR_SETUP_GUIDE.md for secure configuration
            
            {
                "url": "http://darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion",
                "category": "market",
                "priority": 1,
                "frequency": "daily",
                "enabled": False,  # Enable after Tor proxy configured
                "name": "🧅 DarkFail - Market Links",
                "description": "⚠️ REQUIRES TOR - Darknet market directory (NTRO authorized use only)",
                "deep_web": True
            },
            {
                "url": "http://donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion",
                "category": "forum",
                "priority": 1,
                "frequency": "daily",
                "enabled": False,  # Enable after Tor proxy configured
                "name": "🧅 Dread Forum",
                "description": "⚠️ REQUIRES TOR - Major darknet discussion forum (NTRO authorized use only)",
                "deep_web": True
            },
            {
                "url": "http://alphabaysplcnf3pix47f2oau5a2l3a6ik4qutcqxvpcdusj7mvbdmoad.onion",
                "category": "market",
                "priority": 1,
                "frequency": "daily",
                "enabled": False,  # Enable after Tor proxy configured
                "name": "🧅 AlphaBay Market (Mirror)",
                "description": "⚠️ REQUIRES TOR - Darknet marketplace addresses (NTRO authorized use only)",
                "deep_web": True
            },
            
            # ========== DEEP WEB (I2P NETWORK) ==========
            # For NTRO law enforcement use - requires I2P router
            # See I2P_SETUP_GUIDE.md for secure configuration
            
            {
                "url": "http://salt.i2p/",
                "category": "forum",
                "priority": 2,
                "frequency": "weekly",
                "enabled": False,  # Enable after I2P router configured
                "name": "🕸️ Salt I2P Forum",
                "description": "⚠️ REQUIRES I2P - Privacy-focused forum (NTRO authorized use only)"
            },
            {
                "url": "http://flibusta.i2p/",
                "category": "forum",
                "priority": 3,
                "frequency": "weekly",
                "enabled": False,  # Enable after I2P router configured
                "name": "🕸️ Flibusta I2P",
                "description": "⚠️ REQUIRES I2P - I2P content network (NTRO authorized use only)"
            },
        ]
        
        for seed in default_seeds:
            self.add_seed(**seed)
    
    def add_seed(self, url: str, category: str, priority: int, frequency: str, 
                 enabled: bool = True, name: str = None, description: str = None,
                 deep_web: bool = False) -> Dict:
        """Add a seed source to the autonomous crawler"""
        seed = {
            "id": len(self.seeds) + 1,
            "url": url,
            "category": category,  # forum, market, news, pastebin, social, code
            "priority": priority,  # 1=critical, 2=high, 3=medium, 4=low
            "frequency": frequency,  # hourly, daily, weekly
            "enabled": enabled,
            "name": name or url,
            "description": description or "",
            "deep_web": deep_web,  # Tor .onion site
            "last_crawled": None,
            "next_crawl": None,
            "success_rate": 1.0,
            "addresses_found": 0,
            "total_crawls": 0,
            "failed_crawls": 0,
            "credibility_score": 0.5,
            "created_at": datetime.now().isoformat()
        }
        self.seeds.append(seed)
        return seed
    
    def get_due_seeds(self) -> List[Dict]:
        """Get seeds that need to be crawled based on schedule"""
        now = datetime.now()
        due_seeds = []
        
        for seed in self.seeds:
            if not seed["enabled"]:
                continue
            
            # First crawl
            if not seed["last_crawled"]:
                due_seeds.append(seed)
                continue
            
            # Check if frequency interval has passed
            last_crawled = datetime.fromisoformat(seed["last_crawled"])
            if self._is_due(last_crawled, seed["frequency"]):
                due_seeds.append(seed)
        
        # Sort by priority (1 = highest)
        return sorted(due_seeds, key=lambda x: x["priority"])
    
    def _is_due(self, last_crawled: datetime, frequency: str) -> bool:
        """Check if enough time has passed for next crawl"""
        now = datetime.now()
        delta = now - last_crawled
        
        if frequency == "hourly":
            return delta.total_seconds() > 3600
        elif frequency == "daily":
            return delta.days >= 1
        elif frequency == "weekly":
            return delta.days >= 7
        
        return False
    
    def update_seed_stats(self, seed_id: int, success: bool, addresses_found: int = 0):
        """Update seed statistics after crawling"""
        for seed in self.seeds:
            if seed["id"] == seed_id:
                seed["last_crawled"] = datetime.now().isoformat()
                seed["total_crawls"] += 1
                
                if success:
                    seed["addresses_found"] += addresses_found
                else:
                    seed["failed_crawls"] += 1
                
                # Update success rate
                seed["success_rate"] = (seed["total_crawls"] - seed["failed_crawls"]) / seed["total_crawls"]
                
                # Update credibility score (based on success rate and addresses found)
                seed["credibility_score"] = (seed["success_rate"] * 0.6) + min(seed["addresses_found"] / 1000, 0.4)
                
                break
    
    def get_all_seeds(self) -> List[Dict]:
        """Get all seeds"""
        return self.seeds
    
    def get_seed_by_id(self, seed_id: int) -> Optional[Dict]:
        """Get seed by ID"""
        for seed in self.seeds:
            if seed["id"] == seed_id:
                return seed
        return None
    
    def toggle_seed(self, seed_id: int) -> bool:
        """Enable/disable a seed"""
        for seed in self.seeds:
            if seed["id"] == seed_id:
                seed["enabled"] = not seed["enabled"]
                return seed["enabled"]
        return False
    
    def delete_seed(self, seed_id: int) -> bool:
        """Delete a seed"""
        for i, seed in enumerate(self.seeds):
            if seed["id"] == seed_id:
                self.seeds.pop(i)
                return True
        return False

# Global seed manager instance
seed_manager = SeedManager()
