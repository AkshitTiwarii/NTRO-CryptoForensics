"""
Improved Scraper for Better Address Detection
Uses better patterns and multiple techniques to find crypto addresses
"""

import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional
import ssl
import random

logger = logging.getLogger(__name__)

# Enhanced regex patterns for cryptocurrency addresses
CRYPTO_PATTERNS = {
    'BTC': [
        r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',  # Legacy addresses
        r'\bbc1[a-z0-9]{39,59}\b',                # Bech32 addresses
        r'\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b'  # Litecoin (often mixed)
    ],
    'ETH': [
        r'\b0x[a-fA-F0-9]{40}\b'                  # Ethereum addresses
    ]
}

class ImprovedScraper:
    """Enhanced scraper with better address detection"""
    
    def __init__(self, timeout=15):
        self.timeout = timeout
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    def extract_all_crypto_addresses(self, text: str) -> Dict[str, List[str]]:
        """Extract all types of crypto addresses from text"""
        results = {}
        
        for crypto_type, patterns in CRYPTO_PATTERNS.items():
            addresses = set()
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if self.validate_address(match, crypto_type):
                        addresses.add(match)
            
            results[crypto_type] = list(addresses)
        
        return results
    
    def validate_address(self, address: str, crypto_type: str) -> bool:
        """Basic validation for crypto addresses"""
        if crypto_type == 'BTC':
            # Check length and format
            if len(address) < 26 or len(address) > 62:
                return False
            # Exclude obvious fake addresses
            if address.startswith('111111') or address.endswith('00000'):
                return False
            if address.count('1') > 20 or address.count('0') > 20:
                return False
            return True
            
        elif crypto_type == 'ETH':
            # Ethereum addresses should be 42 characters (0x + 40 hex)
            if len(address) != 42:
                return False
            # Check if it's all zeros or ones (placeholders)
            hex_part = address[2:]
            if hex_part == '0' * 40 or hex_part == '1' * 40 or hex_part == 'f' * 40:
                return False
            return True
        
        return False
    
    async def scrape_url_improved(self, url: str, seed_name: str = None) -> Dict:
        """Improved scraping with better extraction techniques"""
        logger.info(f"🌐 Enhanced scraping: {url}")
        
        try:
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = aiohttp.TCPConnector(ssl=ssl.create_default_context())
            
            async with aiohttp.ClientSession(connector=connector, headers=headers, timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.warning(f"⚠️ HTTP {response.status} for {url}")
                        return self._error_result(url, f"HTTP {response.status}")
                    
                    content = await response.text()
                    
                    # Parse with BeautifulSoup
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract text from multiple sources
                    text_sources = []
                    
                    # 1. General page text
                    text_sources.append(soup.get_text(separator=' '))
                    
                    # 2. Code blocks (common in forums)
                    code_elements = soup.find_all(['code', 'pre', 'textarea', 'input'])
                    for elem in code_elements:
                        text_sources.append(elem.get_text())
                    
                    # 3. Specific containers that might have addresses
                    containers = soup.find_all(['div', 'span', 'p'], 
                                             class_=re.compile(r'address|wallet|payment|crypto|bitcoin|ethereum', re.I))
                    for container in containers:
                        text_sources.append(container.get_text())
                    
                    # 4. Check HTML attributes that might contain addresses
                    for elem in soup.find_all(attrs={'data-address': True}):
                        text_sources.append(elem.get('data-address', ''))
                    
                    for elem in soup.find_all(attrs={'value': True}):
                        value = elem.get('value', '')
                        if len(value) > 20:  # Likely an address
                            text_sources.append(value)
                    
                    # Combine all text sources
                    combined_text = ' '.join(text_sources)
                    
                    # Extract addresses
                    extracted = self.extract_all_crypto_addresses(combined_text)
                    
                    # Format for database
                    addresses_found = []
                    now = datetime.now(timezone.utc)
                    
                    for crypto_type, addresses in extracted.items():
                        for addr in addresses:
                            addr_data = {
                                'address': addr,
                                'currency': crypto_type,
                                'crypto_type': crypto_type,
                                'source': seed_name or url,
                                'first_seen': now,
                                'last_seen': now,
                                'category': 'scraped',
                                'risk_score': random.randint(10, 60),  # Random risk for demo
                                'balance': 0.0,
                                'total_received': 0.0,
                                'total_sent': 0.0,
                                'transaction_count': 0,
                                'labels': ['scraped', crypto_type.lower()],
                                'notes': f'Scraped from {url}',
                                'id': f"scraped_{crypto_type.lower()}_{hash(addr) % 100000}"
                            }
                            addresses_found.append(addr_data)
                    
                    total_found = len(addresses_found)
                    logger.info(f"✅ Enhanced scraping found {total_found} addresses from {url}")
                    
                    return {
                        'url': url,
                        'addresses': addresses_found,
                        'success': True,
                        'error': None,
                        'stats': {
                            'total': total_found,
                            **{crypto: len(addrs) for crypto, addrs in extracted.items()}
                        }
                    }
                    
        except asyncio.TimeoutError:
            error = f"Timeout after {self.timeout}s"
            logger.error(f"❌ {error}: {url}")
            return self._error_result(url, error)
            
        except aiohttp.ClientError as e:
            error = f"Connection error: {str(e)}"
            logger.error(f"❌ {error}")
            return self._error_result(url, error)
            
        except Exception as e:
            error = f"Scraping error: {str(e)}"
            logger.error(f"❌ {error}")
            return self._error_result(url, error)
    
    def _error_result(self, url: str, error: str) -> Dict:
        """Return error result structure"""
        return {
            'url': url,
            'addresses': [],
            'success': False,
            'error': error,
            'stats': {'total': 0}
        }

# Quick test sites with known addresses for demo
TEST_URLS = [
    "https://bitcoin.org/en/",  # Should have donation addresses
    "https://github.com/bitcoin/bitcoin",  # May have addresses in issues/code
    "https://bitcointalk.org/index.php?topic=1.0",  # Genesis thread
]

async def test_improved_scraper():
    """Test the improved scraper"""
    scraper = ImprovedScraper()
    
    # Test with a simpler URL first
    test_url = "https://bitcoin.org/en/"
    logger.info(f"🧪 Testing improved scraper with {test_url}")
    
    result = await scraper.scrape_url_improved(test_url, "Test Source")
    
    print(f"Success: {result['success']}")
    print(f"Addresses found: {len(result['addresses'])}")
    print(f"Stats: {result['stats']}")
    if result['error']:
        print(f"Error: {result['error']}")
    
    for addr in result['addresses'][:3]:  # Show first 3
        print(f"  {addr['currency']}: {addr['address']}")

if __name__ == "__main__":
    asyncio.run(test_improved_scraper())