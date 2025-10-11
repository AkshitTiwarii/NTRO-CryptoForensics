"""
Real Cryptocurrency Address Scraper
Scrapes actual websites for Bitcoin and Ethereum addresses
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

# Regex patterns for cryptocurrency addresses
BITCOIN_PATTERN = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|bc1[a-z0-9]{39,59}\b'
ETHEREUM_PATTERN = r'\b0x[a-fA-F0-9]{40}\b'

class RealScraper:
    """Real web scraper for cryptocurrency addresses"""
    
    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_addresses(self, text: str) -> Dict[str, List[str]]:
        """Extract cryptocurrency addresses from text"""
        bitcoin_addresses = list(set(re.findall(BITCOIN_PATTERN, text)))
        ethereum_addresses = list(set(re.findall(ETHEREUM_PATTERN, text)))
        
        # Filter out common false positives
        bitcoin_addresses = [addr for addr in bitcoin_addresses if self.is_valid_bitcoin(addr)]
        ethereum_addresses = [addr for addr in ethereum_addresses if self.is_valid_ethereum(addr)]
        
        return {
            'bitcoin': bitcoin_addresses,
            'ethereum': ethereum_addresses
        }
    
    def is_valid_bitcoin(self, address: str) -> bool:
        """Basic validation for Bitcoin addresses"""
        if len(address) < 26 or len(address) > 62:
            return False
        # Exclude common false positives
        if address.startswith('111111') or address.endswith('00000'):
            return False
        return True
    
    def is_valid_ethereum(self, address: str) -> bool:
        """Basic validation for Ethereum addresses"""
        if len(address) != 42:  # 0x + 40 hex chars
            return False
        # Check if it's all zeros or ones (common placeholders)
        if address[2:] == '0' * 40 or address[2:] == '1' * 40:
            return False
        return True
    
    def scrape_url(self, url: str, seed_name: str = None, use_proxy: bool = False) -> Dict:
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
                # Tor Browser uses port 9150, Tor Expert Bundle uses port 9050
                # Try both ports
                proxies = {
                    'http': 'socks5h://127.0.0.1:9150',  # Tor Browser default
                    'https': 'socks5h://127.0.0.1:9150'
                }
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
                proxies = {
                    'http': 'http://127.0.0.1:4444',
                    'https': 'http://127.0.0.1:4444'
                }
                logger.info(f"🕸️ Using I2P proxy for: {url}")
            else:
                # Surface web - no proxy needed
                proxies = None
            
            # Make request with or without proxy
            for attempt in range(self.max_retries):
                try:
                    response = self.session.get(
                        url, 
                        timeout=self.timeout if not proxies else self.timeout * 2,  # Longer timeout for Tor/I2P
                        verify=True if not proxies else False,  # Don't verify SSL for .onion
                        proxies=proxies
                    )
                    response.raise_for_status()
                    break
                except requests.RequestException as e:
                    if attempt == self.max_retries - 1:
                        raise
                    time.sleep(2 ** attempt)  # Exponential backoff
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
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
            
        except requests.Timeout:
            error = f"Timeout after {self.timeout}s"
            logger.error(f"❌ {error}: {url}")
        except requests.RequestException as e:
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
    
    def scrape_seed(self, seed: Dict, use_proxy: bool = False) -> Dict:
        """Scrape a seed source
        
        Args:
            seed: Seed configuration dictionary
            use_proxy: Whether to use Tor/I2P proxy for .onion/.i2p sites
        """
        result = self.scrape_url(seed['url'], seed.get('name'), use_proxy=use_proxy)
        
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
