# Tor Scraper for Deep Web / Dark Web Sources
import requests
from stem import Signal
from stem.control import Controller
import logging
from typing import Optional
import time

logger = logging.getLogger(__name__)

class TorScraper:
    """Scraper for .onion sites via Tor network"""
    
    def __init__(self, tor_proxy='socks5h://127.0.0.1:9050', control_port=9051):
        self.tor_proxy = tor_proxy
        self.control_port = control_port
        self.session = requests.Session()
        self.session.proxies = {
            'http': self.tor_proxy,
            'https': self.tor_proxy
        }
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        })
        logger.info("TorScraper initialized")
    
    def renew_connection(self):
        """Renew Tor circuit to get new IP address"""
        try:
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                time.sleep(controller.get_newnym_wait())
                logger.info("Tor circuit renewed successfully")
        except Exception as e:
            logger.error(f"Failed to renew Tor circuit: {e}")
            logger.warning("Continuing with existing circuit...")
    
    def scrape_onion_site(self, url: str, timeout: int = 30, max_retries: int = 3) -> Optional[str]:
        """Scrape a .onion site through Tor"""
        logger.info(f"Scraping .onion site: {url}")
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                logger.info(f"Successfully scraped {url} ({len(response.text)} bytes)")
                return response.text
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout for {url}, attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    self.renew_connection()
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error scraping {url}: {e}")
                if attempt < max_retries - 1:
                    self.renew_connection()
                else:
                    return None
        
        return None
    
    def check_tor_connection(self) -> bool:
        """Verify Tor connection is working"""
        try:
            response = self.session.get('https://check.torproject.org/', timeout=10)
            if 'Congratulations' in response.text:
                logger.info("Tor connection verified")
                return True
            else:
                logger.warning("Tor connection check failed")
                return False
        except Exception as e:
            logger.error(f"Tor connection check error: {e}")
            return False


# Sample .onion seeds (for testing - use archived/research sites only)
SAMPLE_ONION_SEEDS = [
    {
        "url": "http://darknetlive.com/",  # News site (clearnet mirror)
        "category": "news",
        "priority": 2,
        "frequency": "daily",
        "name": "Darknet Live",
        "description": "Dark web news and market monitoring",
        "deep_web": False  # Clearnet version for testing
    },
    # Add actual .onion URLs only if legal and for research
]
