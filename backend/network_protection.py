# Network Protection & Proxy Configuration for Autonomous Scraping
# This file provides IP rotation, proxy management, and anti-ban mechanisms

from typing import List, Optional, Dict
import random
import time
import logging
from datetime import datetime, timedelta
from stem import Signal
from stem.control import Controller
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class ProxyRotator:
    """
    Manages proxy rotation to prevent IP bans
    Supports: Tor, SOCKS5, HTTP proxies, VPN integration
    """
    
    def __init__(self):
        self.tor_enabled = False
        self.proxy_list = []
        self.current_proxy_index = 0
        self.failed_proxies = set()
        self.request_counts = {}  # Track requests per proxy
        self.last_rotation = {}   # Track last rotation time
        
        # Load proxies from config
        self._load_proxy_list()
        
        # Try to connect to Tor
        self._init_tor()
    
    def _init_tor(self):
        """Initialize Tor connection if available"""
        try:
            # Test Tor SOCKS proxy
            session = requests.Session()
            session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            response = session.get('https://check.torproject.org/', timeout=10)
            if 'Congratulations' in response.text:
                self.tor_enabled = True
                logger.info("✓ Tor connection active - IP protection enabled")
            else:
                logger.warning("⚠ Tor not properly configured")
        except Exception as e:
            logger.warning(f"⚠ Tor not available: {e}")
            logger.info("Continuing with proxy rotation only")
    
    def _load_proxy_list(self):
        """
        Load proxy list from configuration
        Add your own proxies here or load from external source
        """
        # Example proxy list (replace with your own)
        self.proxy_list = [
            # Free proxy lists (not recommended for production)
            # Use paid proxy services like:
            # - Bright Data (formerly Luminati)
            # - Oxylabs
            # - Smartproxy
            # - IPRoyal
            
            # Example format:
            # {'http': 'http://user:pass@proxy1.example.com:8080', 'https': 'http://user:pass@proxy1.example.com:8080'},
            # {'http': 'socks5://user:pass@proxy2.example.com:1080', 'https': 'socks5://user:pass@proxy2.example.com:1080'},
        ]
        
        if self.proxy_list:
            logger.info(f"Loaded {len(self.proxy_list)} proxy servers")
        else:
            logger.warning("No proxies configured - using direct connection")
    
    def get_proxy(self, force_tor: bool = False) -> Optional[Dict]:
        """
        Get next proxy in rotation
        
        Args:
            force_tor: Force use of Tor (for .onion sites or high-risk sources)
        
        Returns:
            Proxy configuration dict or None for direct connection
        """
        # Force Tor for .onion sites
        if force_tor:
            if self.tor_enabled:
                return {
                    'http': 'socks5h://127.0.0.1:9050',
                    'https': 'socks5h://127.0.0.1:9050'
                }
            else:
                logger.error("Tor requested but not available!")
                return None
        
        # Use proxy rotation if available
        if self.proxy_list:
            proxy = self._get_next_working_proxy()
            if proxy:
                return proxy
        
        # Fallback to Tor if enabled
        if self.tor_enabled:
            return {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
        
        # Direct connection (no proxy)
        return None
    
    def _get_next_working_proxy(self) -> Optional[Dict]:
        """Get next proxy that hasn't failed"""
        attempts = 0
        while attempts < len(self.proxy_list):
            proxy = self.proxy_list[self.current_proxy_index]
            proxy_key = str(self.current_proxy_index)
            
            # Check if proxy is in failed list
            if proxy_key not in self.failed_proxies:
                # Track usage
                self.request_counts[proxy_key] = self.request_counts.get(proxy_key, 0) + 1
                
                # Rotate to next proxy for next request
                self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
                
                return proxy
            
            # Move to next proxy
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
            attempts += 1
        
        # All proxies failed - reset and try again
        logger.warning("All proxies failed - resetting failed list")
        self.failed_proxies.clear()
        return self.proxy_list[0] if self.proxy_list else None
    
    def mark_proxy_failed(self, proxy: Dict):
        """Mark a proxy as failed"""
        for idx, p in enumerate(self.proxy_list):
            if p == proxy:
                self.failed_proxies.add(str(idx))
                logger.warning(f"Proxy {idx} marked as failed")
                break
    
    def renew_tor_circuit(self):
        """Renew Tor circuit to get new IP address"""
        if not self.tor_enabled:
            logger.warning("Tor not enabled - cannot renew circuit")
            return False
        
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()  # Use password if configured
                controller.signal(Signal.NEWNYM)
                time.sleep(controller.get_newnym_wait())
                logger.info("✓ Tor circuit renewed - new IP address")
                return True
        except Exception as e:
            logger.error(f"Failed to renew Tor circuit: {e}")
            logger.info("Hint: Enable ControlPort in torrc and set password")
            return False


class RateLimiter:
    """
    Intelligent rate limiting to avoid bans
    Implements:
    - Per-domain rate limits
    - Exponential backoff
    - Respectful crawl delays
    """
    
    def __init__(self):
        self.last_request = {}
        self.request_counts = {}
        self.backoff_delays = {}
        
        # Default rate limits (requests per minute)
        self.rate_limits = {
            'default': 30,           # 30 req/min = 1 every 2 seconds
            'bitcointalk.org': 20,   # More conservative for forums
            'reddit.com': 60,        # Reddit allows higher rates
            'pastebin.com': 10,      # Very conservative
            'github.com': 30,
            'twitter.com': 15,
            '.onion': 5,             # Very slow for Tor sites
        }
    
    def wait_if_needed(self, url: str):
        """Wait if necessary to respect rate limits"""
        domain = self._extract_domain(url)
        limit = self._get_rate_limit(domain)
        delay = 60.0 / limit  # Convert req/min to seconds between requests
        
        # Add backoff if domain has been problematic
        if domain in self.backoff_delays:
            delay *= self.backoff_delays[domain]
        
        # Check last request time
        if domain in self.last_request:
            elapsed = time.time() - self.last_request[domain]
            if elapsed < delay:
                wait_time = delay - elapsed
                logger.debug(f"Rate limiting {domain}: waiting {wait_time:.1f}s")
                time.sleep(wait_time)
        
        # Update last request time
        self.last_request[domain] = time.time()
        
        # Track request count
        self.request_counts[domain] = self.request_counts.get(domain, 0) + 1
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Check for .onion
        if '.onion' in domain:
            return '.onion'
        
        return domain
    
    def _get_rate_limit(self, domain: str) -> int:
        """Get rate limit for domain"""
        # Check exact match
        if domain in self.rate_limits:
            return self.rate_limits[domain]
        
        # Check partial matches
        for key, limit in self.rate_limits.items():
            if key in domain:
                return limit
        
        return self.rate_limits['default']
    
    def increase_backoff(self, url: str):
        """Increase backoff delay after error (429, 503, etc.)"""
        domain = self._extract_domain(url)
        current_backoff = self.backoff_delays.get(domain, 1.0)
        new_backoff = min(current_backoff * 2, 16.0)  # Max 16x slower
        self.backoff_delays[domain] = new_backoff
        logger.warning(f"Increased backoff for {domain}: {new_backoff}x slower")
    
    def reset_backoff(self, url: str):
        """Reset backoff after successful requests"""
        domain = self._extract_domain(url)
        if domain in self.backoff_delays:
            del self.backoff_delays[domain]
            logger.info(f"Reset backoff for {domain}")


class ProtectedScraper:
    """
    Scraper with built-in protection mechanisms:
    - Proxy rotation
    - Rate limiting
    - User-agent rotation
    - Retry logic
    - Anti-fingerprinting headers
    """
    
    def __init__(self):
        self.proxy_rotator = ProxyRotator()
        self.rate_limiter = RateLimiter()
        self.user_agents = self._load_user_agents()
        self.session = self._create_session()
    
    def _load_user_agents(self) -> List[str]:
        """Load realistic user agent strings"""
        return [
            # Chrome on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # Firefox on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            # Chrome on macOS
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # Firefox on Linux
            'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            # Edge on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        ]
    
    def _create_session(self) -> requests.Session:
        """Create session with retry logic"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def scrape(self, url: str, force_tor: bool = False, timeout: int = 30) -> Optional[str]:
        """
        Scrape URL with full protection
        
        Args:
            url: URL to scrape
            force_tor: Force Tor usage (.onion or high-risk)
            timeout: Request timeout
        
        Returns:
            HTML content or None on failure
        """
        # Check if .onion URL
        is_onion = '.onion' in url
        if is_onion:
            force_tor = True
        
        # Rate limiting
        self.rate_limiter.wait_if_needed(url)
        
        # Get proxy
        proxy = self.proxy_rotator.get_proxy(force_tor=force_tor)
        
        # Random user agent
        user_agent = random.choice(self.user_agents)
        
        # Anti-fingerprinting headers
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        try:
            logger.info(f"Scraping: {url} (Tor: {force_tor}, Proxy: {proxy is not None})")
            
            response = self.session.get(
                url,
                headers=headers,
                proxies=proxy,
                timeout=timeout,
                allow_redirects=True
            )
            
            response.raise_for_status()
            
            # Reset backoff on success
            self.rate_limiter.reset_backoff(url)
            
            logger.info(f"✓ Success: {url} ({len(response.text)} bytes)")
            return response.text
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [429, 503]:
                # Rate limited - increase backoff
                logger.warning(f"Rate limited on {url}: {e}")
                self.rate_limiter.increase_backoff(url)
                
                # Renew Tor circuit if using Tor
                if force_tor or proxy:
                    self.proxy_rotator.renew_tor_circuit()
            
            elif e.response.status_code in [403, 407]:
                # Proxy blocked
                logger.warning(f"Proxy blocked on {url}: {e}")
                if proxy:
                    self.proxy_rotator.mark_proxy_failed(proxy)
            
            logger.error(f"HTTP error on {url}: {e}")
            return None
            
        except requests.exceptions.ProxyError as e:
            logger.error(f"Proxy error on {url}: {e}")
            if proxy:
                self.proxy_rotator.mark_proxy_failed(proxy)
            return None
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None


# Global instances
proxy_rotator = ProxyRotator()
rate_limiter = RateLimiter()
protected_scraper = ProtectedScraper()


# Configuration for different platforms
PLATFORM_CONFIGS = {
    'telegram': {
        'rate_limit': 20,  # req/min
        'require_proxy': True,
        'rotate_after': 50,  # Rotate IP after N requests
    },
    'instagram': {
        'rate_limit': 15,
        'require_proxy': True,
        'rotate_after': 30,
    },
    'twitter': {
        'rate_limit': 15,
        'require_proxy': False,  # API has its own rate limits
        'rotate_after': 100,
    },
    'darknet': {
        'rate_limit': 5,
        'require_proxy': True,
        'force_tor': True,
        'rotate_after': 10,
    },
}
