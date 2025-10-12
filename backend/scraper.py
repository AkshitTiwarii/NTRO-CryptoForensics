"""
Real Cryptocurrency Address Scraper
Scrapes actual websites for Bitcoin and Ethereum addresses
"""

import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, urlparse
import ssl

logger = logging.getLogger(__name__)

# Regex patterns for cryptocurrency addresses
BITCOIN_PATTERN = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|bc1[a-z0-9]{39,59}\b'
ETHEREUM_PATTERN = r'\b0x[a-fA-F0-9]{40}\b'

class RealScraper:
    """Real web scraper for cryptocurrency addresses"""
    
    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries
        # Use async session
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    def extract_addresses(self, text: str) -> Dict[str, List[str]]:
        """Extract cryptocurrency addresses from text"""
        results = {}
        
        # Enhanced patterns for better detection
        patterns = {
            'bitcoin': [
                r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',  # Legacy P2PKH/P2SH
                r'\bbc1[a-z0-9]{39,59}\b',                # Bech32
                r'\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b'  # Litecoin (often found together)
            ],
            'ethereum': [
                r'\b0x[a-fA-F0-9]{40}\b'                  # Ethereum addresses
            ]
        }
        
        for crypto_type, pattern_list in patterns.items():
            addresses = set()
            for pattern in pattern_list:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if self.is_valid_address(match, crypto_type):
                        addresses.add(match)
            results[crypto_type] = list(addresses)
        
        return results
    
    def is_valid_address(self, address: str, crypto_type: str) -> bool:
        """Enhanced address validation"""
        if crypto_type == 'bitcoin':
            return self.is_valid_bitcoin(address)
        elif crypto_type == 'ethereum':
            return self.is_valid_ethereum(address)
        return False
    
    def is_valid_bitcoin(self, address: str) -> bool:
        """Enhanced validation for Bitcoin addresses"""
        if len(address) < 26 or len(address) > 62:
            return False
        # Exclude common false positives and test addresses
        invalid_patterns = [
            '111111', '000000', '123456', 'abcdef',
            '1111111111111111111111', '0000000000000000000000'
        ]
        for pattern in invalid_patterns:
            if pattern in address.lower():
                return False
        # Check for reasonable character distribution (not all same character)
        if len(set(address)) < 5:
            return False
        return True
    
    def is_valid_ethereum(self, address: str) -> bool:
        """Enhanced validation for Ethereum addresses"""
        if len(address) != 42:  # 0x + 40 hex chars
            return False
        hex_part = address[2:].lower()
        # Check if it's all zeros, ones, or other obvious placeholders
        invalid_patterns = ['0' * 40, '1' * 40, 'f' * 40, 'a' * 40, '123456789' * 4]
        if hex_part in invalid_patterns:
            return False
        # Check for reasonable character distribution
        if len(set(hex_part)) < 6:
            return False
        return True
    
    async def scrape_url(self, url: str, seed_name: str = None, use_proxy: bool = False) -> Dict:
        """Scrape a single URL for cryptocurrency addresses
        
        Args:
            url: URL to scrape
            seed_name: Name of the seed source
            use_proxy: Whether to use Tor/I2P proxy (for .onion/.i2p sites)
        """
        logger.info(f"🌐 Scraping: {url}")
        
        addresses_found = []
        error = None
        
        try:
            # Handle Tor .onion sites (for NTRO authorized use)
            if '.onion' in url:
                if not use_proxy:
                    logger.warning(f"⚠️ Tor site detected: {url}. Requires Tor proxy configuration.")
                    return {
                        'url': url,
                        'addresses': [],
                        'error': 'Tor SOCKS5 proxy not configured. Run setup_tor.ps1 script',
                        'success': False
                    }
                # Use Tor SOCKS5 proxy
                connector = aiohttp.TCPConnector(ssl=False)
                logger.info(f"🧅 Using Tor proxy for: {url}")
            
            # Handle I2P .i2p sites (for NTRO authorized use)
            elif '.i2p' in url:
                if not use_proxy:
                    logger.warning(f"⚠️ I2P site detected: {url}. Requires I2P router.")
                    return {
                        'url': url,
                        'addresses': [],
                        'error': 'I2P HTTP proxy not configured. See I2P_SETUP_GUIDE.md',
                        'success': False
                    }
                # Use I2P HTTP proxy
                connector = aiohttp.TCPConnector(ssl=False)
                logger.info(f"🕸️ Using I2P proxy for: {url}")
            else:
                # Surface web - default connector
                connector = aiohttp.TCPConnector(ssl=ssl.create_default_context())
            
            # Create headers
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            # Make request with retry logic
            for attempt in range(self.max_retries):
                try:
                    timeout = aiohttp.ClientTimeout(total=self.timeout if not '.onion' in url and not '.i2p' in url else self.timeout * 2)
                    
                    async with aiohttp.ClientSession(connector=connector, headers=headers, timeout=timeout) as session:
                        async with session.get(url) as response:
                            if response.status != 200:
                                raise aiohttp.ClientResponseError(
                                    request_info=response.request_info,
                                    history=response.history,
                                    status=response.status
                                )
                            
                            # Get the content
                            content = await response.text()
                            break
                            
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    if attempt == self.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract text from various elements
            text_content = soup.get_text(separator=' ')
            
            # Also check code blocks specifically (common in forums/GitHub)
            code_blocks = soup.find_all(['code', 'pre', 'div'], class_=re.compile(r'code|pre|snippet'))
            for block in code_blocks:
                text_content += ' ' + block.get_text()
            
            # Extract addresses
            extracted = self.extract_addresses(text_content)
            
            # Format addresses for MongoDB
            for btc_addr in extracted['bitcoin']:
                addresses_found.append({
                    'address': btc_addr,
                    'currency': 'BTC',
                    'source': seed_name or url,
                    'first_seen': datetime.now(timezone.utc),
                    'last_seen': datetime.now(timezone.utc),
                    'category': 'unknown',
                    'risk_score': 0.0,
                    'balance': 0.0,
                    'total_received': 0.0,
                    'total_sent': 0.0,
                    'transaction_count': 0,
                    'labels': [],
                    'notes': f'Scraped from {url}'
                })
            
            for eth_addr in extracted['ethereum']:
                addresses_found.append({
                    'address': eth_addr,
                    'currency': 'ETH',
                    'source': seed_name or url,
                    'first_seen': datetime.now(timezone.utc),
                    'last_seen': datetime.now(timezone.utc),
                    'category': 'unknown',
                    'risk_score': 0.0,
                    'balance': 0.0,
                    'total_received': 0.0,
                    'total_sent': 0.0,
                    'transaction_count': 0,
                    'labels': [],
                    'notes': f'Scraped from {url}'
                })
            
            logger.info(f"✅ Found {len(addresses_found)} addresses from {url}")
            
            return {
                'url': url,
                'addresses': addresses_found,
                'error': None,
                'success': True,
                'stats': {
                    'bitcoin': len(extracted['bitcoin']),
                    'ethereum': len(extracted['ethereum']),
                    'total': len(addresses_found)
                }
            }
            
        except asyncio.TimeoutError:
            error = f"Timeout after {self.timeout}s"
            logger.error(f"❌ {error}: {url}")
        except aiohttp.ClientError as e:
            error = f"Request failed: {str(e)}"
            logger.error(f"❌ {error}")
        except Exception as e:
            error = f"Scraping error: {str(e)}"
            logger.error(f"❌ {error}")
        
        return {
            'url': url,
            'addresses': [],
            'error': error,
            'success': False
        }
    
    async def scrape_seed(self, seed: Dict, use_proxy: bool = False) -> Dict:
        """Scrape a seed source
        
        Args:
            seed: Seed configuration dictionary
            use_proxy: Whether to use Tor/I2P proxy for .onion/.i2p sites
        """
        result = await self.scrape_url(seed['url'], seed.get('name'), use_proxy=use_proxy)
        
        return {
            'seed_id': seed['id'],
            'seed_name': seed['name'],
            'url': seed['url'],
            'addresses_found': result['addresses'],
            'count': len(result['addresses']),
            'success': result['success'],
            'error': result.get('error'),
            'timestamp': datetime.now(timezone.utc)
        }


# High-volume crypto sites for real scraping
RECOMMENDED_SOURCES = {
    'surface_web': [
        {
            'name': 'BitcoinTalk - Security & Legal',
            'url': 'https://bitcointalk.org/index.php?board=83.0',
            'category': 'forum',
            'description': 'Very high volume Bitcoin address discussions'
        },
        {
            'name': 'Reddit r/Bitcoin - New Posts',
            'url': 'https://old.reddit.com/r/Bitcoin/new/',
            'category': 'social',
            'description': 'Active Bitcoin community'
        },
        {
            'name': 'GitHub - Bitcoin Donations',
            'url': 'https://github.com/topics/bitcoin-donation',
            'category': 'code',
            'description': 'Open source projects with donation addresses'
        },
        {
            'name': 'Blockchain.com Explorer - Latest Blocks',
            'url': 'https://www.blockchain.com/explorer',
            'category': 'explorer',
            'description': 'Live blockchain transactions'
        },
        {
            'name': 'CoinDesk - Crime & Hacks',
            'url': 'https://www.coindesk.com/tag/crime/',
            'category': 'news',
            'description': 'News about crypto crime with addresses'
        },
        {
            'name': 'Etherscan - Latest Transactions',
            'url': 'https://etherscan.io/txs',
            'category': 'explorer',
            'description': 'Live Ethereum transactions'
        },
    ],
    'dark_web': [
        # Note: These require Tor SOCKS5 proxy configuration
        {
            'name': 'Dark Web Market (DEMO)',
            'url': 'http://example.onion',
            'category': 'market',
            'description': 'Requires Tor proxy - see setup guide',
            'requires': 'tor'
        }
    ],
    'deep_web': [
        # Note: These require I2P router
        {
            'name': 'I2P Forum (DEMO)',
            'url': 'http://example.i2p',
            'category': 'forum',
            'description': 'Requires I2P router - see setup guide',
            'requires': 'i2p'
        }
    ]
}
