"""
Cryptocurrency Address Collection Module
Multi-source scraping for crypto addresses from surface, deep, and dark web
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CryptocurrencyAddressCollector:
    """Main collector for cryptocurrency addresses from multiple sources"""
    
    def __init__(self):
        self.sources = {
            'surface_web': [
                'https://blockchain.com/explorer',
                'https://www.blockchain.com/btc/address/',
                'https://etherscan.io/',
            ],
            'blockchain_apis': [
                'https://blockchain.info/rawaddr/',
                'https://api.etherscan.io/api',
            ]
        }
        
        # Cryptocurrency regex patterns
        self.crypto_patterns = {
            'bitcoin': r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-z0-9]{39,59}',
            'ethereum': r'0x[a-fA-F0-9]{40}',
            'litecoin': r'[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}',
            'bitcoin_cash': r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bitcoincash:[a-z0-9]{41,42}',
            'monero': r'4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}',
            'ripple': r'r[0-9a-zA-Z]{24,34}',
            'dogecoin': r'D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}'
        }
        
        # PII extraction patterns
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
        }
    
    async def scrape_surface_web(self, url: str) -> List[Dict]:
        """Scrape cryptocurrency addresses from surface web sources"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to fetch {url}: {response.status}")
                        return []
                    
                    content = await response.text()
                    
                    # Extract addresses
                    addresses = self.extract_addresses(content)
                    
                    # Extract PII
                    pii_data = self.extract_pii(content)
                    
                    results = []
                    for addr, crypto_type in addresses:
                        results.append({
                            'address': addr,
                            'crypto_type': crypto_type,
                            'source_url': url,
                            'source_type': 'surface_web',
                            'timestamp': datetime.utcnow().isoformat(),
                            'pii_data': pii_data,
                            'context': self.extract_context(content, addr)
                        })
                    
                    return results
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout scraping {url}")
            return []
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return []
    
    def extract_addresses(self, text: str) -> List[tuple]:
        """Extract cryptocurrency addresses using regex patterns"""
        addresses = []
        
        for crypto_type, pattern in self.crypto_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                addresses.append((match, crypto_type))
        
        # Remove duplicates
        return list(set(addresses))
    
    def extract_pii(self, text: str) -> Dict:
        """Extract Personally Identifiable Information"""
        pii_data = {}
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                pii_data[pii_type] = list(set(matches))[:5]  # Limit to 5 matches
        
        return pii_data
    
    def extract_context(self, text: str, address: str, window: int = 200) -> str:
        """Extract context around the address"""
        try:
            idx = text.find(address)
            if idx == -1:
                return ""
            
            start = max(0, idx - window)
            end = min(len(text), idx + len(address) + window)
            
            context = text[start:end]
            # Clean up context
            context = ' '.join(context.split())
            
            return context
        except Exception:
            return ""
    
    def detect_crypto_type(self, address: str) -> str:
        """Detect cryptocurrency type from address format"""
        for crypto_type, pattern in self.crypto_patterns.items():
            if re.match(pattern, address):
                return crypto_type
        return 'unknown'
    
    async def fetch_blockchain_data(self, address: str, crypto_type: str) -> Dict:
        """Fetch transaction data from blockchain APIs"""
        try:
            if crypto_type == 'bitcoin':
                return await self.fetch_btc_data(address)
            elif crypto_type == 'ethereum':
                return await self.fetch_eth_data(address)
            else:
                return {}
        except Exception as e:
            logger.error(f"Error fetching blockchain data: {e}")
            return {}
    
    async def fetch_btc_data(self, address: str) -> Dict:
        """Fetch Bitcoin address info from blockchain.info API"""
        try:
            url = f"https://blockchain.info/rawaddr/{address}?limit=10"
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'balance': data.get('final_balance', 0) / 100000000,
                            'tx_count': data.get('n_tx', 0),
                            'total_received': data.get('total_received', 0) / 100000000,
                            'total_sent': data.get('total_sent', 0) / 100000000,
                        }
        except Exception as e:
            logger.error(f"Error fetching BTC data: {e}")
        
        return {}
    
    async def fetch_eth_data(self, address: str) -> Dict:
        """Fetch Ethereum address info from Etherscan API"""
        # Note: Requires API key in production
        try:
            url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest"
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('status') == '1':
                            balance_wei = int(data.get('result', 0))
                            balance_eth = balance_wei / 1e18
                            return {
                                'balance': balance_eth,
                                'currency': 'ETH'
                            }
        except Exception as e:
            logger.error(f"Error fetching ETH data: {e}")
        
        return {}
    
    def calculate_risk_score(self, address_data: Dict) -> float:
        """Calculate initial risk score based on available data"""
        risk_score = 0.0
        
        # High transaction volume indicates potential money laundering
        tx_count = address_data.get('tx_count', 0)
        if tx_count > 1000:
            risk_score += 0.3
        elif tx_count > 100:
            risk_score += 0.2
        
        # Context-based risk
        context = address_data.get('context', '').lower()
        risky_keywords = ['ransomware', 'darknet', 'laundering', 'illegal', 'stolen', 'hack']
        
        for keyword in risky_keywords:
            if keyword in context:
                risk_score += 0.2
                break
        
        # Source type risk
        if address_data.get('source_type') == 'dark_web':
            risk_score += 0.3
        
        # PII correlation risk
        if address_data.get('pii_data'):
            risk_score += 0.1
        
        return min(risk_score, 1.0)
    
    def categorize_address(self, address_data: Dict) -> str:
        """Simple rule-based categorization"""
        context = address_data.get('context', '').lower()
        
        category_keywords = {
            'ransomware': ['ransomware', 'ransom', 'wannacry', 'locky'],
            'darknet_market': ['darknet', 'dark web', 'marketplace', 'silk road'],
            'money_laundering': ['laundering', 'mixer', 'tumbler', 'mixing'],
            'fraud_scam': ['scam', 'fraud', 'phishing', 'ponzi'],
            'exchange': ['exchange', 'coinbase', 'binance', 'kraken'],
            'mining': ['mining', 'pool', 'miner'],
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in context:
                    return category
        
        return 'unknown'


class ScraperJobManager:
    """Manage scraping jobs and their status"""
    
    def __init__(self):
        self.jobs = {}
        self.collector = CryptocurrencyAddressCollector()
    
    async def start_scraping_job(self, job_config: Dict) -> str:
        """Start a new scraping job"""
        import uuid
        
        job_id = str(uuid.uuid4())
        
        job = {
            'id': job_id,
            'status': 'running',
            'config': job_config,
            'started_at': datetime.utcnow().isoformat(),
            'addresses_found': 0,
            'sources_scraped': 0,
            'errors': []
        }
        
        self.jobs[job_id] = job
        
        # Start scraping in background
        asyncio.create_task(self._run_scraping_job(job_id, job_config))
        
        return job_id
    
    async def _run_scraping_job(self, job_id: str, config: Dict):
        """Execute the scraping job"""
        job = self.jobs[job_id]
        
        try:
            sources = config.get('sources', [])
            all_addresses = []
            
            for source in sources:
                try:
                    addresses = await self.collector.scrape_surface_web(source)
                    all_addresses.extend(addresses)
                    job['sources_scraped'] += 1
                except Exception as e:
                    job['errors'].append(f"Error with {source}: {str(e)}")
            
            job['addresses_found'] = len(all_addresses)
            job['results'] = all_addresses
            job['status'] = 'completed'
            job['completed_at'] = datetime.utcnow().isoformat()
            
        except Exception as e:
            job['status'] = 'failed'
            job['error'] = str(e)
            logger.error(f"Job {job_id} failed: {e}")
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get status of a scraping job"""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all scraping jobs"""
        return list(self.jobs.values())
