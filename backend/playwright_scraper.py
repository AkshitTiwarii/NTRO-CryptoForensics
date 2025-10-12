"""
Playwright-based web scraper with JavaScript rendering support
Supports Surface Web, Dark Web (.onion via Tor), and Deep Web (.i2p)
"""

import os
import re
import logging
from typing import Dict, List
from datetime import datetime, timezone
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import asyncio
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlaywrightScraper:
    """Web scraper using Playwright for JavaScript-enabled sites"""
    
    # Cryptocurrency address patterns
    CRYPTO_PATTERNS = {
        'BITCOIN': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|bc1[a-z0-9]{39,59}\b',
        'ETHEREUM': r'\b0x[a-fA-F0-9]{40}\b',
        'LITECOIN': r'\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b|ltc1[a-z0-9]{39,59}\b',
        'DOGECOIN': r'\bD{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}\b',
        'RIPPLE': r'\br[a-zA-Z0-9]{24,34}\b',
        'MONERO': r'\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b',
        'DASH': r'\bX[1-9A-HJ-NP-Za-km-z]{33}\b',
        'ZCASH': r'\bt1[a-zA-Z0-9]{33}\b'
    }
    
    def __init__(self):
        """Initialize Playwright scraper"""
        logger.info("🎭 Playwright Scraper initialized (JavaScript enabled)")
    
    def detect_web_type(self, url: str) -> str:
        """Detect if URL is surface, dark, or deep web"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        if '.onion' in domain:
            return 'dark'
        elif '.i2p' in domain:
            return 'deep'
        else:
            return 'surface'
    
    def extract_addresses(self, text: str) -> List[Dict]:
        """Extract cryptocurrency addresses from text"""
        addresses = []
        seen = set()
        
        for crypto_type, pattern in self.CRYPTO_PATTERNS.items():
            matches = re.findall(pattern, text)
            for address in matches:
                if address not in seen and len(address) >= 26:
                    seen.add(address)
                    addresses.append({
                        'address': address,
                        'currency': crypto_type,  # Use 'currency' not 'crypto_type'
                        'category': 'discovered',
                        'discovered_at': datetime.now(timezone.utc).isoformat(),
                        'source': 'playwright_scraper'
                    })
        
        return addresses
    
    async def scrape_url(self, url: str, use_proxy: bool = False, 
                   proxy_host: str = None, proxy_port: int = None,
                   timeout: int = 30000) -> Dict:
        """
        Scrape a URL with JavaScript rendering (ASYNC)
        
        Args:
            url: URL to scrape
            use_proxy: Enable proxy (for Tor/I2P)
            proxy_host: Proxy server (e.g., '127.0.0.1')
            proxy_port: Proxy port (e.g., 9150 for Tor, 4444 for I2P)
            timeout: Page load timeout in milliseconds
            
        Returns:
            Dict with success status, addresses found, and metadata
        """
        web_type = self.detect_web_type(url)
        
        # Auto-detect proxy settings for dark/deep web
        if web_type == 'dark' and not proxy_host:
            proxy_host = '127.0.0.1'
            proxy_port = 9150  # Tor Browser default SOCKS port
            use_proxy = True
            logger.info(f"🧅 Using Tor proxy ({proxy_host}:{proxy_port})")
        elif web_type == 'deep' and not proxy_host:
            proxy_host = '127.0.0.1'
            proxy_port = 4444  # I2P default HTTP proxy port
            use_proxy = True
            logger.info(f"🌊 Using I2P proxy ({proxy_host}:{proxy_port})")
        
        logger.info(f"🌐 Scraping {web_type.upper()} WEB: {url}")
        
        try:
            # Use async_playwright for compatibility with asyncio
            async with async_playwright() as p:
                # Launch browser with proxy if needed
                browser_args = {
                    'headless': True,
                    'args': [
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ]
                }
                
                if use_proxy and proxy_host and proxy_port:
                    browser_args['proxy'] = {
                        'server': f'{proxy_host}:{proxy_port}'
                    }
                
                browser = await p.chromium.launch(**browser_args)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                # Navigate and wait for network idle
                logger.info(f"⏳ Loading page (timeout: {timeout}ms)...")
                await page.goto(url, timeout=timeout, wait_until='networkidle')
                
                # Wait for dynamic content
                await page.wait_for_timeout(2000)  # 2 seconds for JavaScript execution
                
                # Get full page content (after JavaScript rendering)
                content = await page.content()
                text = await page.inner_text('body')
                
                logger.info(f"✅ Page loaded - {len(text)} characters")
                
                # Extract addresses
                addresses = self.extract_addresses(text)
                
                # Cleanup
                await browser.close()
                
                logger.info(f"🎯 Found {len(addresses)} addresses")
                
                return {
                    'success': True,
                    'url': url,
                    'web_type': web_type,
                    'addresses_found': len(addresses),
                    'addresses': addresses,
                    'scraped_at': datetime.now(timezone.utc).isoformat()
                }
                
        except PlaywrightTimeout:
            error_msg = f"Timeout loading {url} (exceeded {timeout}ms)"
            logger.error(f"⏰ {error_msg}")
            return {
                'success': False,
                'url': url,
                'error': error_msg,
                'addresses_found': 0
            }
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Error scraping {url}: {error_msg}")
            return {
                'success': False,
                'url': url,
                'error': error_msg,
                'addresses_found': 0
            }
    
    async def scrape_seed(self, seed: Dict, use_proxy: bool = False) -> Dict:
        """
        Scrape a seed source (ASYNC)
        
        Args:
            seed: Seed dictionary with 'url', 'name', etc.
            use_proxy: Enable proxy for dark/deep web
            
        Returns:
            Dict with scraping results
        """
        url = seed.get('url')
        if not url:
            return {
                'success': False,
                'error': 'No URL provided in seed',
                'addresses_found': 0
            }
        
        # Auto-enable proxy for .onion and .i2p domains
        web_type = self.detect_web_type(url)
        if web_type in ['dark', 'deep']:
            use_proxy = True
        
        # Scrape the URL
        result = await self.scrape_url(url, use_proxy=use_proxy)
        
        # Add seed metadata
        result['seed_name'] = seed.get('name', 'Unknown')
        result['seed_id'] = seed.get('_id')
        
        return result


# CLI Testing
if __name__ == "__main__":
    import asyncio
    
    async def test_scraper():
        scraper = PlaywrightScraper()
        
        # Test surface web
        print("\n🌐 Testing Surface Web (Reddit)...")
        result = await scraper.scrape_url("https://old.reddit.com/r/Bitcoin/new/", use_proxy=False)
        print(f"Result: {result['success']}, Found: {result.get('addresses_found', 0)} addresses")
        if result.get('addresses'):
            print(f"Sample: {result['addresses'][0]}")
        
        # Test dark web (requires Tor Browser running)
        print("\n🧅 Testing Dark Web (.onion)...")
        print("Note: This requires Tor Browser running on port 9150")
        result = await scraper.scrape_url(
            "http://darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion",
            use_proxy=True
        )
        print(f"Result: {result['success']}, Error: {result.get('error', 'None')}")
    
    # Run async test
    asyncio.run(test_scraper())
