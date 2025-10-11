# Celery Tasks for Autonomous Scraping
from celery_app import app
from seed_manager import seed_manager
from crypto_collector import CryptocurrencyAddressCollector
from ml_categorizer import AddressCategorizer
import logging
from datetime import datetime
import random

logger = logging.getLogger(__name__)

# Initialize components
collector = CryptocurrencyAddressCollector()
categorizer = AddressCategorizer()

@app.task(name='tasks.autonomous_scrape')
def autonomous_scrape():
    """Main autonomous scraping task - runs hourly"""
    logger.info("Starting autonomous scraping cycle...")
    
    # Get seeds that are due for crawling
    due_seeds = seed_manager.get_due_seeds()
    logger.info(f"Found {len(due_seeds)} seeds due for crawling")
    
    results = {
        "started_at": datetime.now().isoformat(),
        "seeds_processed": 0,
        "jobs_dispatched": 0,
        "errors": []
    }
    
    # Dispatch scraping jobs for each due seed
    for seed in due_seeds:
        try:
            job_id = f"job_{seed['id']}_{int(datetime.now().timestamp())}"
            scrape_seed.delay(job_id, seed)
            results["jobs_dispatched"] += 1
            results["seeds_processed"] += 1
        except Exception as e:
            logger.error(f"Error dispatching job for seed {seed['id']}: {e}")
            results["errors"].append(str(e))
    
    results["completed_at"] = datetime.now().isoformat()
    logger.info(f"Autonomous scraping cycle completed: {results}")
    return results


@app.task(name='tasks.scrape_seed', bind=True)
def scrape_seed(self, job_id: str, seed: dict):
    """Scrape a single seed source"""
    logger.info(f"Job {job_id}: Scraping seed {seed['name']} - {seed['url']}")
    
    job_result = {
        "job_id": job_id,
        "seed_id": seed['id'],
        "seed_url": seed['url'],
        "started_at": datetime.now().isoformat(),
        "addresses_found": 0,
        "status": "running",
        "worker_id": self.request.hostname
    }
    
    try:
        # Use PROTECTED scraper with proxy rotation and rate limiting
        from network_protection import protected_scraper
        
        # Force Tor for deep web sources
        force_tor = seed.get('deep_web', False)
        html = protected_scraper.scrape(seed['url'], force_tor=force_tor)
        
        if not html:
            raise Exception("Failed to fetch URL content")
        
        # Extract crypto addresses
        addresses = collector.extract_crypto_addresses(html)
        job_result["addresses_found"] = len(addresses)
        
        # Categorize addresses using ML
        categorized_addresses = []
        for addr in addresses:
            category, confidence = categorizer.categorize_address(addr)
            categorized_addresses.append({
                "address": addr,
                "category": category,
                "confidence": confidence,
                "source_url": seed['url'],
                "source_name": seed['name'],
                "discovered_at": datetime.now().isoformat()
            })
        
        # Trigger enrichment for high-value addresses
        for addr_data in categorized_addresses:
            if addr_data['confidence'] > 0.7:
                enrich_address.delay(addr_data)
        
        # Update seed statistics
        seed_manager.update_seed_stats(seed['id'], success=True, addresses_found=len(addresses))
        
        job_result["status"] = "completed"
        job_result["completed_at"] = datetime.now().isoformat()
        
        logger.info(f"Job {job_id}: Completed successfully - {len(addresses)} addresses found")
        
    except Exception as e:
        logger.error(f"Job {job_id}: Failed - {e}")
        job_result["status"] = "failed"
        job_result["error"] = str(e)
        job_result["completed_at"] = datetime.now().isoformat()
        seed_manager.update_seed_stats(seed['id'], success=False)
    
    return job_result


@app.task(name='tasks.enrich_address')
def enrich_address(address_data: dict):
    """Enrich a crypto address with additional intelligence"""
    logger.info(f"Enriching address: {address_data['address']}")
    
    try:
        # Blockchain analysis via Blockchair
        from blockchair_api import BlockchairAPI
        blockchair = BlockchairAPI()
        
        blockchain_type = "bitcoin"  # Detect from address format
        enrichment = blockchair.get_address_info(blockchain_type, address_data['address'])
        
        address_data['enrichment'] = {
            "balance_usd": enrichment.get('balance_usd', 0),
            "transaction_count": enrichment.get('transaction_count', 0),
            "first_seen": enrichment.get('first_transaction_time'),
            "last_seen": enrichment.get('last_transaction_time'),
            "total_received_usd": enrichment.get('received_usd', 0),
            "total_sent_usd": enrichment.get('spent_usd', 0),
        }
        
        # Risk scoring
        address_data['risk_score'] = calculate_risk_score(address_data)
        
        # Check against watchlists
        check_watchlist_match.delay(address_data)
        
        logger.info(f"Address enriched: {address_data['address']} (Risk: {address_data['risk_score']})")
        
    except Exception as e:
        logger.error(f"Enrichment failed for {address_data['address']}: {e}")
        address_data['enrichment_error'] = str(e)
    
    return address_data


@app.task(name='tasks.enrich_pending_addresses')
def enrich_pending_addresses():
    """Periodic task to enrich pending addresses (runs every 30 min)"""
    logger.info("Starting enrichment cycle for pending addresses...")
    
    # This would query database for addresses pending enrichment
    # For now, it's a placeholder
    
    return {"status": "completed", "enriched": 0}


@app.task(name='tasks.check_watchlist_alerts')
def check_watchlist_alerts():
    """Check for watchlist alerts (runs every 15 min)"""
    logger.info("Checking watchlists for alerts...")
    
    # Placeholder for watchlist checking logic
    # Would query database for watchlisted addresses and check for new activity
    
    return {"alerts_triggered": 0}


@app.task(name='tasks.check_watchlist_match')
def check_watchlist_match(address_data: dict):
    """Check if discovered address matches any watchlist"""
    # Placeholder for watchlist matching
    return address_data


@app.task(name='tasks.cleanup_old_jobs')
def cleanup_old_jobs():
    """Clean up old job records (runs daily)"""
    logger.info("Cleaning up old job records...")
    
    # Would delete jobs older than 30 days
    
    return {"cleaned": 0}


def calculate_risk_score(address_data: dict) -> int:
    """Calculate risk score 0-100"""
    score = 0
    
    # Category-based scoring
    category_scores = {
        "ransomware": 90,
        "darknet_market": 80,
        "mixer": 70,
        "scam": 75,
        "gambling": 50,
        "exchange": 20,
        "mining": 10,
        "legitimate": 5
    }
    score += category_scores.get(address_data.get('category', 'unknown'), 30)
    
    # Confidence adjustment
    confidence = address_data.get('confidence', 0)
    score = int(score * confidence)
    
    # Enrichment-based adjustments
    enrichment = address_data.get('enrichment', {})
    
    # High transaction volume
    if enrichment.get('transaction_count', 0) > 100:
        score += 10
    
    # Large balance
    if enrichment.get('balance_usd', 0) > 100000:
        score += 15
    
    # Recent activity
    from datetime import datetime, timedelta
    last_seen = enrichment.get('last_seen')
    if last_seen:
        try:
            last_seen_dt = datetime.fromisoformat(last_seen)
            if datetime.now() - last_seen_dt < timedelta(days=7):
                score += 5
        except:
            pass
    
    return min(score, 100)
