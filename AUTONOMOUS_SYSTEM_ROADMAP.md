# 🤖 AUTONOMOUS OSINT SYSTEM ROADMAP
## Converting Manual Scraper → Fully Autonomous Cryptocurrency Intelligence Platform

---

## 🎯 Executive Summary

**Current State**: Manual URL-driven scraper (proof-of-concept)  
**Target State**: Autonomous 24/7 OSINT pipeline with discovery, scheduling, enrichment, clustering, and alerting  
**Gap**: 70% of NTRO requirements missing  
**Timeline**: 4-8 weeks MVP, 12 weeks full production system  

---

## 📊 Current Capabilities Assessment

### ✅ What You Have (30% Complete)

1. **Frontend Skeleton**
   - Address Registry UI (search/filter interface)
   - Manual OSINT Scraper (single URL input)
   - Recent Jobs placeholder (no real data)
   - Blockchair Analysis interface (excellent!)

2. **Backend Foundation**
   - FastAPI server with JWT auth
   - `crypto_collector.py` (surface web scraping)
   - `ml_categorizer.py` (11-category classification)
   - `blockchair_api.py` (41 blockchain support)
   - In-memory storage (test mode)

3. **Data Collection**
   - Regex patterns for 7 cryptocurrencies
   - Basic PII extraction (email, phone, name)
   - BeautifulSoup HTML parsing
   - Single-URL scraping capability

### ❌ What's Missing (70% Incomplete)

| Component | Status | Impact |
|-----------|--------|--------|
| **Autonomous Discovery** | 0% | 🔴 CRITICAL - Core requirement |
| **Seed Management** | 0% | 🔴 CRITICAL - No source lists |
| **Scheduler/Orchestration** | 0% | 🔴 CRITICAL - No automation |
| **Deep/Dark Web Access** | 0% | 🔴 CRITICAL - 15% of eval weight |
| **Distributed Crawling** | 0% | 🟡 HIGH - Scalability issue |
| **Auto-Enrichment** | 20% | 🟡 HIGH - Partial Blockchair |
| **Alerting System** | 0% | 🟡 MEDIUM - Reactive capability |
| **Graph Database** | 0% | 🟡 MEDIUM - Clustering limited |
| **Credibility Scoring** | 0% | 🟢 LOW - Quality control |
| **Legal/Audit Framework** | 0% | 🟢 LOW - Compliance gap |

---

## 🏗️ Target Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                          │
├─────────────────────────────────────────────────────────────────┤
│  Dashboard │ Seed Manager │ Job Monitor │ Watchlists │ Alerts   │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                         │
├─────────────────────────────────────────────────────────────────┤
│  Auth │ Rate Limiting │ Request Routing │ WebSocket (live feed) │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Celery Workers │ Beat Scheduler │ Task Queue (Redis/RabbitMQ)  │
│  Job Dispatcher │ Priority Queue │ Dead Letter Queue            │
└────┬───────┬────────────────────────────────────────────────────┘
     │       │
     │       └──────────────────┐
     │                          │
┌────▼──────────────┐  ┌────────▼───────────┐  ┌─────────────────┐
│  INGESTION LAYER  │  │ ENRICHMENT LAYER   │  │ ANALYTICS LAYER │
├───────────────────┤  ├────────────────────┤  ├─────────────────┤
│ Scrapy Cluster    │  │ Blockchain APIs    │  │ ML Categorizer  │
│ Tor Browser Pool  │  │ Address Validator  │  │ Risk Scoring    │
│ Puppeteer/Selenium│  │ PII Extractor (NLP)│  │ Graph Clustering│
│ Image OCR         │  │ Geo-IP Lookup      │  │ Pattern Analysis│
│ Forum Crawlers    │  │ WHOIS/DNS Lookup   │  │ Anomaly Detector│
└─────────┬─────────┘  └────────┬───────────┘  └────────┬────────┘
          │                     │                       │
          └─────────────────────┼───────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                      STORAGE LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│ PostgreSQL      │ ElasticSearch  │ Neo4j Graph DB │ Redis Cache │
│ (Metadata)      │ (Full-text)    │ (Relationships)│ (Sessions)  │
│                 │                │                 │             │
│ S3/MinIO        │ MongoDB        │ InfluxDB       │ Prometheus  │
│ (Raw HTML/imgs) │ (Unstructured) │ (Time-series)  │ (Metrics)   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Implementation Roadmap

### **PHASE 1: MVP Autonomous System** (4-8 weeks)

#### Week 1-2: Seed Management & Scheduler

**Backend Components**:

1. **Seed Manager Service** (`backend/seed_manager.py`)
```python
class SeedManager:
    def __init__(self):
        self.seeds = []  # Seed sources
        
    def add_seed(self, url: str, category: str, priority: int, frequency: str):
        """Add a seed source to the autonomous crawler"""
        seed = {
            "url": url,
            "category": category,  # forum, market, news, pastebin
            "priority": priority,  # 1=critical, 2=high, 3=medium, 4=low
            "frequency": frequency,  # hourly, daily, weekly
            "enabled": True,
            "last_crawled": None,
            "success_rate": 1.0,
            "addresses_found": 0
        }
        self.seeds.append(seed)
        return seed
    
    def get_due_seeds(self):
        """Get seeds that need to be crawled based on schedule"""
        now = datetime.now()
        due_seeds = []
        for seed in self.seeds:
            if not seed["enabled"]:
                continue
            if not seed["last_crawled"]:
                due_seeds.append(seed)
                continue
            # Check if frequency interval has passed
            if self._is_due(seed["last_crawled"], seed["frequency"]):
                due_seeds.append(seed)
        return sorted(due_seeds, key=lambda x: x["priority"])
    
    def _is_due(self, last_crawled, frequency):
        """Check if enough time has passed for next crawl"""
        delta = datetime.now() - last_crawled
        if frequency == "hourly":
            return delta.total_seconds() > 3600
        elif frequency == "daily":
            return delta.days >= 1
        elif frequency == "weekly":
            return delta.days >= 7
        return False
```

2. **Celery Task Queue** (`backend/celery_app.py`)
```python
from celery import Celery
from celery.schedules import crontab

app = Celery('ntro_crypto', 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'autonomous-scraping-every-hour': {
        'task': 'tasks.autonomous_scrape',
        'schedule': crontab(minute=0),  # Every hour
    },
    'enrichment-every-30min': {
        'task': 'tasks.enrich_addresses',
        'schedule': crontab(minute='*/30'),
    },
    'cleanup-old-jobs': {
        'task': 'tasks.cleanup',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}

@app.task(name='tasks.autonomous_scrape')
def autonomous_scrape():
    """Main autonomous scraping task"""
    seed_manager = SeedManager()
    due_seeds = seed_manager.get_due_seeds()
    
    for seed in due_seeds:
        # Create scraping job
        job_id = create_scraping_job(seed)
        # Dispatch to worker
        scrape_seed.delay(job_id, seed)
    
    return f"Dispatched {len(due_seeds)} scraping jobs"

@app.task(name='tasks.scrape_seed')
def scrape_seed(job_id, seed):
    """Individual seed scraping task"""
    collector = CryptocurrencyAddressCollector()
    
    try:
        # Scrape the seed URL
        results = collector.scrape_surface_web([seed["url"]])
        
        # Extract addresses
        addresses = []
        for result in results:
            addrs = collector.extract_addresses(result["content"])
            addresses.extend(addrs)
        
        # Auto-enrich each address
        for addr in addresses:
            enrich_address.delay(addr, seed["url"])
        
        # Update seed stats
        update_seed_stats(seed, success=True, count=len(addresses))
        
        return f"Job {job_id}: Found {len(addresses)} addresses"
        
    except Exception as e:
        update_seed_stats(seed, success=False)
        raise

@app.task(name='tasks.enrich_address')
def enrich_address(address_data, source_url):
    """Auto-enrichment: blockchain lookup + ML categorization"""
    blockchair = BlockchairAPI()
    categorizer = AddressCategorizer()
    
    # Get blockchain data
    blockchain_data = blockchair.get_address_info(
        address_data["address"], 
        address_data["crypto_type"]
    )
    
    # Categorize
    category_result = categorizer.categorize_address({
        **address_data,
        "blockchain_data": blockchain_data
    })
    
    # Store enriched address
    store_address({
        **address_data,
        "blockchain_data": blockchain_data,
        "category": category_result["category"],
        "risk_score": category_result["risk_score"],
        "source_url": source_url,
        "discovered_at": datetime.now()
    })
    
    # Check watchlist alerts
    check_watchlist_alerts(address_data["address"])
```

3. **Database Schema Updates** (`backend/database.py`)
```python
# PostgreSQL schema for autonomous operations

CREATE TABLE seeds (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    category VARCHAR(50),
    priority INTEGER DEFAULT 3,
    frequency VARCHAR(20),
    enabled BOOLEAN DEFAULT TRUE,
    last_crawled TIMESTAMP,
    next_crawl TIMESTAMP,
    success_rate FLOAT DEFAULT 1.0,
    addresses_found INTEGER DEFAULT 0,
    credibility_score FLOAT DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE scraping_jobs (
    id UUID PRIMARY KEY,
    seed_id INTEGER REFERENCES seeds(id),
    status VARCHAR(20),  -- pending, running, completed, failed
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    addresses_found INTEGER,
    pages_crawled INTEGER,
    errors TEXT[],
    worker_id VARCHAR(100)
);

CREATE TABLE watchlists (
    id SERIAL PRIMARY KEY,
    address VARCHAR(100) NOT NULL,
    crypto_type VARCHAR(20),
    alert_threshold FLOAT,
    alert_types TEXT[],  -- ['new_transaction', 'balance_change', 'large_transfer']
    notification_channels TEXT[],  -- ['email', 'webhook', 'sms']
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    watchlist_id INTEGER REFERENCES watchlists(id),
    alert_type VARCHAR(50),
    severity VARCHAR(20),  -- critical, high, medium, low
    message TEXT,
    data JSONB,
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Frontend Components**:

1. **Seed Manager UI** (`frontend/src/components/SeedManager.jsx`)
```javascript
function SeedManager() {
  const [seeds, setSeeds] = useState([]);
  const [newSeed, setNewSeed] = useState({
    url: '',
    category: 'forum',
    priority: 3,
    frequency: 'daily'
  });

  const addSeed = async () => {
    await axios.post('/api/seeds', newSeed);
    loadSeeds();
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">
          Add Seed Source
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="https://bitcointalk.org/index.php?board=83.0"
            value={newSeed.url}
            onChange={(e) => setNewSeed({...newSeed, url: e.target.value})}
            className="px-3 py-2 bg-slate-950 text-slate-100 rounded border border-slate-800"
          />
          
          <select
            value={newSeed.category}
            onChange={(e) => setNewSeed({...newSeed, category: e.target.value})}
            className="px-3 py-2 bg-slate-950 text-slate-100 rounded border border-slate-800"
          >
            <option value="forum">Forum</option>
            <option value="market">Darknet Market</option>
            <option value="news">News Site</option>
            <option value="pastebin">Pastebin</option>
            <option value="social">Social Media</option>
          </select>
          
          <select
            value={newSeed.frequency}
            onChange={(e) => setNewSeed({...newSeed, frequency: e.target.value})}
            className="px-3 py-2 bg-slate-950 text-slate-100 rounded border border-slate-800"
          >
            <option value="hourly">Hourly</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
          </select>
          
          <button
            onClick={addSeed}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
          >
            Add Seed
          </button>
        </div>
      </div>

      {/* Seed List */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">
          Active Seeds ({seeds.length})
        </h3>
        
        <div className="space-y-3">
          {seeds.map(seed => (
            <SeedItem key={seed.id} seed={seed} onToggle={toggleSeed} />
          ))}
        </div>
      </div>
    </div>
  );
}
```

2. **Job Monitor UI** (`frontend/src/components/JobMonitor.jsx`)
```javascript
function JobMonitor() {
  const [jobs, setJobs] = useState([]);
  const [liveStats, setLiveStats] = useState({
    running: 0,
    queued: 0,
    completed_today: 0,
    addresses_found_today: 0
  });

  // WebSocket for live updates
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/job-monitor');
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      setJobs(prev => updateJobs(prev, update));
      setLiveStats(update.stats);
    };
    return () => ws.close();
  }, []);

  return (
    <div className="space-y-6">
      {/* Live Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard label="Running Jobs" value={liveStats.running} color="blue" />
        <StatCard label="Queued Jobs" value={liveStats.queued} color="yellow" />
        <StatCard label="Completed Today" value={liveStats.completed_today} color="green" />
        <StatCard label="Addresses Found" value={liveStats.addresses_found_today} color="purple" />
      </div>

      {/* Recent Jobs */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">
          Recent Scraping Jobs
        </h3>
        
        <div className="space-y-3">
          {jobs.map(job => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      </div>
    </div>
  );
}
```

**Deliverables Week 1-2**:
- ✅ Celery + Redis task queue operational
- ✅ Seed Manager backend + frontend
- ✅ Hourly autonomous scraping working
- ✅ Job Monitor with live updates
- ✅ PostgreSQL schema migrated from in-memory

---

#### Week 3-4: Deep/Dark Web Integration

**Backend Components**:

1. **Tor Scraper** (`backend/tor_scraper.py`)
```python
import requests
from stem import Signal
from stem.control import Controller

class TorScraper:
    def __init__(self):
        self.session = requests.session()
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        })
    
    def renew_connection(self):
        """Get new Tor circuit"""
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            time.sleep(controller.get_newnym_wait())
    
    async def scrape_onion_site(self, url: str, max_retries=3):
        """Scrape .onion darknet site"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    return {
                        "url": url,
                        "content": response.text,
                        "status_code": response.status_code,
                        "scraped_at": datetime.now()
                    }
                else:
                    # Renew Tor circuit and retry
                    self.renew_connection()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                self.renew_connection()
        
        return None
    
    def scrape_darknet_market(self, market_url: str):
        """Scrape darknet marketplace"""
        # Login if credentials available
        # Navigate to crypto addresses section
        # Extract vendor addresses, escrow addresses
        pass

# Known darknet market seeds (archived/historical)
DARKNET_SEEDS = [
    "http://alphabay...onion/crypto",  # AlphaBay (historical)
    "http://silkroad...onion/vendors",  # Silk Road archives
    # Add more from public OSINT sources
]
```

2. **Puppeteer JS Renderer** (`backend/js_renderer.py`)
```python
import asyncio
from pyppeteer import launch

class JavaScriptRenderer:
    def __init__(self, use_tor=False):
        self.browser = None
        self.use_tor = use_tor
    
    async def init_browser(self):
        """Initialize headless browser"""
        args = ['--no-sandbox', '--disable-setuid-sandbox']
        if self.use_tor:
            args.append('--proxy-server=socks5://127.0.0.1:9050')
        
        self.browser = await launch(
            headless=True,
            args=args
        )
    
    async def render_page(self, url: str):
        """Render JavaScript-heavy page"""
        if not self.browser:
            await self.init_browser()
        
        page = await self.browser.newPage()
        await page.setUserAgent('Mozilla/5.0...')
        
        await page.goto(url, {'waitUntil': 'networkidle0'})
        content = await page.content()
        
        await page.close()
        return content
```

3. **Forum Crawler** (`backend/forum_crawler.py`)
```python
class ForumCrawler:
    """Specialized crawler for forums (BitcoinTalk, Reddit, etc.)"""
    
    def __init__(self):
        self.visited_threads = set()
    
    async def crawl_bitcointalk(self, board_url: str):
        """Crawl BitcoinTalk board"""
        # Get all thread URLs from board
        threads = self.get_thread_urls(board_url)
        
        addresses_found = []
        for thread_url in threads:
            if thread_url in self.visited_threads:
                continue
            
            # Scrape thread
            posts = self.scrape_thread(thread_url)
            
            # Extract addresses + context
            for post in posts:
                addrs = self.extract_addresses_with_context(post)
                addresses_found.extend(addrs)
            
            self.visited_threads.add(thread_url)
        
        return addresses_found
    
    def extract_addresses_with_context(self, post):
        """Extract addresses with surrounding text for categorization"""
        # Find crypto addresses
        # Grab 100 characters before/after for context
        # Extract author info (PII)
        pass
```

**Frontend Updates**:

1. **Add Deep Web Toggle to Seed Manager**
```javascript
<div className="flex items-center gap-2">
  <input
    type="checkbox"
    checked={newSeed.deep_web}
    onChange={(e) => setNewSeed({...newSeed, deep_web: e.target.checked})}
  />
  <label className="text-sm text-slate-300">Deep Web Source (.onion)</label>
</div>
```

2. **Tor Status Indicator**
```javascript
<div className="flex items-center gap-2 text-sm">
  <div className={`h-2 w-2 rounded-full ${torStatus === 'connected' ? 'bg-green-400' : 'bg-red-400'}`} />
  <span className="text-slate-400">
    Tor: {torStatus === 'connected' ? 'Connected' : 'Disconnected'}
  </span>
</div>
```

**Deliverables Week 3-4**:
- ✅ Tor integration with circuit renewal
- ✅ Puppeteer JS rendering for dynamic sites
- ✅ Forum crawler for BitcoinTalk, Reddit
- ✅ Deep web seed support in UI
- ✅ Proxy rotation for surface web

---

#### Week 5-6: Auto-Enrichment & Alerting

**Backend Components**:

1. **Enhanced Enrichment Pipeline** (`backend/enrichment_pipeline.py`)
```python
class EnrichmentPipeline:
    def __init__(self):
        self.blockchair = BlockchairAPI()
        self.categorizer = AddressCategorizer()
        self.pii_extractor = PIIExtractor()  # spaCy NER
    
    async def enrich_address(self, address_data):
        """Full enrichment: blockchain + ML + PII + geo"""
        
        # 1. Blockchain data
        blockchain_data = await self.blockchair.get_address_info(
            address_data["address"],
            address_data["crypto_type"]
        )
        
        # 2. ML categorization
        category_result = self.categorizer.categorize_address({
            **address_data,
            "blockchain_data": blockchain_data
        })
        
        # 3. PII extraction from context
        pii_data = self.pii_extractor.extract(address_data.get("context", ""))
        
        # 4. Geo-IP if available
        geo_data = None
        if pii_data.get("ip_address"):
            geo_data = await self.lookup_geoip(pii_data["ip_address"])
        
        # 5. WHOIS/DNS for domains
        domain_data = None
        if pii_data.get("domain"):
            domain_data = await self.whois_lookup(pii_data["domain"])
        
        return {
            **address_data,
            "blockchain_data": blockchain_data,
            "category": category_result["category"],
            "risk_score": category_result["risk_score"],
            "confidence": category_result["confidence"],
            "pii": pii_data,
            "geo": geo_data,
            "domain_info": domain_data,
            "enriched_at": datetime.now()
        }

class PIIExtractor:
    """Advanced PII extraction using spaCy NER"""
    
    def __init__(self):
        import spacy
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract(self, text: str):
        """Extract PII entities"""
        doc = self.nlp(text)
        
        pii = {
            "persons": [],
            "organizations": [],
            "locations": [],
            "emails": [],
            "phones": [],
            "ip_addresses": [],
            "domains": []
        }
        
        # Named entities
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                pii["persons"].append(ent.text)
            elif ent.label_ == "ORG":
                pii["organizations"].append(ent.text)
            elif ent.label_ == "GPE":
                pii["locations"].append(ent.text)
        
        # Regex patterns
        import re
        pii["emails"] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        pii["ip_addresses"] = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        
        return pii
```

2. **Watchlist & Alerting System** (`backend/alerting.py`)
```python
class AlertingSystem:
    def __init__(self):
        self.watchlists = []
    
    def add_to_watchlist(self, address: str, alert_config: dict):
        """Add address to watchlist"""
        watchlist = {
            "address": address,
            "alert_types": alert_config.get("alert_types", ["new_transaction"]),
            "threshold": alert_config.get("threshold", None),
            "channels": alert_config.get("channels", ["email"]),
            "created_at": datetime.now()
        }
        self.watchlists.append(watchlist)
        return watchlist
    
    async def check_alerts(self, address: str):
        """Check if address matches any watchlist conditions"""
        watchlist_items = [w for w in self.watchlists if w["address"] == address]
        
        for item in watchlist_items:
            # Get latest blockchain data
            blockchain_data = await self.blockchair.get_address_info(address, "bitcoin")
            
            # Check conditions
            alerts = []
            
            if "new_transaction" in item["alert_types"]:
                if self.has_new_transactions(address, blockchain_data):
                    alerts.append({
                        "type": "new_transaction",
                        "severity": "medium",
                        "message": f"New transaction detected for {address}"
                    })
            
            if "large_transfer" in item["alert_types"]:
                if self.has_large_transfer(blockchain_data, item["threshold"]):
                    alerts.append({
                        "type": "large_transfer",
                        "severity": "high",
                        "message": f"Large transfer detected: {blockchain_data['latest_tx_value']} BTC"
                    })
            
            # Send alerts via configured channels
            for alert in alerts:
                await self.send_alert(alert, item["channels"])
        
        return alerts
    
    async def send_alert(self, alert, channels):
        """Send alert via configured channels"""
        if "email" in channels:
            await self.send_email_alert(alert)
        if "webhook" in channels:
            await self.send_webhook_alert(alert)
        if "sms" in channels:
            await self.send_sms_alert(alert)
```

**Frontend Components**:

1. **Watchlist Manager UI**
```javascript
function WatchlistManager() {
  const [watchlists, setWatchlists] = useState([]);
  const [newWatchlist, setNewWatchlist] = useState({
    address: '',
    alert_types: ['new_transaction', 'large_transfer'],
    threshold: 10,  // BTC
    channels: ['email']
  });

  return (
    <div className="space-y-6">
      {/* Add to Watchlist Form */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">
          Add to Watchlist
        </h3>
        
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Bitcoin address to monitor"
            value={newWatchlist.address}
            onChange={(e) => setNewWatchlist({...newWatchlist, address: e.target.value})}
            className="w-full px-3 py-2 bg-slate-950 text-slate-100 rounded border border-slate-800 font-mono"
          />
          
          <div>
            <label className="text-sm text-slate-400 mb-2 block">Alert Conditions</label>
            <div className="space-y-2">
              <CheckboxOption 
                label="New Transaction" 
                checked={newWatchlist.alert_types.includes('new_transaction')}
                onChange={(checked) => toggleAlertType('new_transaction', checked)}
              />
              <CheckboxOption 
                label="Large Transfer (>10 BTC)" 
                checked={newWatchlist.alert_types.includes('large_transfer')}
                onChange={(checked) => toggleAlertType('large_transfer', checked)}
              />
              <CheckboxOption 
                label="Balance Change" 
                checked={newWatchlist.alert_types.includes('balance_change')}
                onChange={(checked) => toggleAlertType('balance_change', checked)}
              />
            </div>
          </div>
          
          <button
            onClick={addToWatchlist}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
          >
            Add to Watchlist
          </button>
        </div>
      </div>

      {/* Active Watchlists */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">
          Active Watchlists ({watchlists.length})
        </h3>
        
        <div className="space-y-3">
          {watchlists.map(w => (
            <WatchlistItem key={w.id} watchlist={w} />
          ))}
        </div>
      </div>
    </div>
  );
}
```

2. **Alerts Dashboard**
```javascript
function AlertsDashboard() {
  const [alerts, setAlerts] = useState([]);
  
  // WebSocket for live alerts
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/alerts');
    ws.onmessage = (event) => {
      const newAlert = JSON.parse(event.data);
      setAlerts(prev => [newAlert, ...prev]);
      // Show browser notification
      showNotification(newAlert);
    };
    return () => ws.close();
  }, []);

  return (
    <div className="space-y-4">
      {alerts.map(alert => (
        <AlertCard 
          key={alert.id} 
          alert={alert}
          onAcknowledge={() => acknowledgeAlert(alert.id)}
        />
      ))}
    </div>
  );
}
```

**Deliverables Week 5-6**:
- ✅ spaCy NER for advanced PII extraction
- ✅ Auto-enrichment pipeline (blockchain + ML + PII + geo)
- ✅ Watchlist system backend + frontend
- ✅ Real-time alerting via WebSocket
- ✅ Email/webhook alert notifications

---

#### Week 7-8: Distributed Crawling & Graph DB

**Backend Components**:

1. **Scrapy-Redis Distributed Crawler** (`backend/scrapy_cluster/`)
```python
# settings.py
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://localhost:6379'

# crypto_spider.py
import scrapy
from scrapy_redis.spiders import RedisSpider

class CryptoSpider(RedisSpider):
    name = 'crypto_spider'
    redis_key = 'crypto:start_urls'
    
    def parse(self, response):
        # Extract crypto addresses
        addresses = self.extract_addresses(response.text)
        
        for addr in addresses:
            yield {
                'address': addr['address'],
                'crypto_type': addr['type'],
                'context': addr['context'],
                'source_url': response.url,
                'discovered_at': datetime.now().isoformat()
            }
        
        # Follow links
        for href in response.css('a::attr(href)').getall():
            if self.should_follow(href):
                yield response.follow(href, self.parse)
```

2. **Neo4j Graph Database** (`backend/graph_db.py`)
```python
from neo4j import GraphDatabase

class CryptoGraphDB:
    def __init__(self, uri="bolt://localhost:7687"):
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    
    def create_address_node(self, address_data):
        """Create cryptocurrency address node"""
        with self.driver.session() as session:
            session.run(
                """
                MERGE (a:Address {address: $address})
                SET a.crypto_type = $crypto_type,
                    a.category = $category,
                    a.risk_score = $risk_score,
                    a.balance = $balance
                """,
                address=address_data["address"],
                crypto_type=address_data["crypto_type"],
                category=address_data["category"],
                risk_score=address_data["risk_score"],
                balance=address_data.get("blockchain_data", {}).get("balance", 0)
            )
    
    def create_transaction_edge(self, from_addr, to_addr, amount, timestamp):
        """Create transaction relationship"""
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Address {address: $from_addr})
                MATCH (b:Address {address: $to_addr})
                MERGE (a)-[t:TRANSACTED {timestamp: $timestamp}]->(b)
                SET t.amount = $amount
                """,
                from_addr=from_addr,
                to_addr=to_addr,
                amount=amount,
                timestamp=timestamp
            )
    
    def find_clusters(self, address, max_depth=3):
        """Find related addresses via transaction graph"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH path = (a:Address {address: $address})-[:TRANSACTED*1..$max_depth]-(related:Address)
                RETURN related.address as address, 
                       related.risk_score as risk_score,
                       length(path) as distance
                ORDER BY distance
                """,
                address=address,
                max_depth=max_depth
            )
            return [record.data() for record in result]
```

**Frontend Components**:

1. **Graph Visualization** (`frontend/src/components/GraphView.jsx`)
```javascript
import Cytoscape from 'cytoscape';

function GraphView({ address }) {
  const cyRef = useRef(null);
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });

  useEffect(() => {
    // Fetch graph data from Neo4j
    axios.get(`/api/graph/clusters/${address}`).then(res => {
      setGraphData(res.data);
      renderGraph(res.data);
    });
  }, [address]);

  const renderGraph = (data) => {
    const cy = Cytoscape({
      container: cyRef.current,
      elements: [
        ...data.nodes.map(n => ({ data: { id: n.address, label: n.address.substr(0, 8), risk: n.risk_score } })),
        ...data.edges.map(e => ({ data: { source: e.from, target: e.to } }))
      ],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': (ele) => ele.data('risk') > 70 ? '#f87171' : '#94a3b8',
            'label': 'data(label)'
          }
        }
      ],
      layout: { name: 'cose' }
    });
  };

  return <div ref={cyRef} className="w-full h-[600px] bg-slate-950 rounded" />;
}
```

**Deliverables Week 7-8**:
- ✅ Scrapy-Redis distributed crawling
- ✅ Neo4j graph database integration
- ✅ Transaction graph analysis
- ✅ Interactive graph visualization (Cytoscape.js)
- ✅ Cluster detection algorithms

---

### **PHASE 2: Production Hardening** (Weeks 9-12)

#### Week 9-10: Scalability & Performance

1. **Load Balancing & Horizontal Scaling**
   - Nginx reverse proxy
   - Multiple FastAPI instances
   - Redis Cluster for caching
   - PostgreSQL read replicas

2. **Performance Optimization**
   - ElasticSearch for full-text search
   - Redis caching layer
   - Database query optimization
   - Celery worker autoscaling

3. **Monitoring & Observability**
   - Prometheus metrics
   - Grafana dashboards
   - ELK stack for logging
   - Sentry error tracking

#### Week 11: Legal, Security & Compliance

1. **Legal Framework**
   - robots.txt compliance checker
   - Terms of Service violation detector
   - Rate limiting per site
   - Legal approval workflow for sensitive sources

2. **Security Hardening**
   - PII encryption at rest (AES-256)
   - Role-based access control (RBAC)
   - Audit logging (who accessed what, when)
   - API key rotation
   - SQL injection prevention
   - XSS protection

3. **Data Retention Policies**
   - Configurable retention periods
   - Automated data purging
   - GDPR-compliant data export
   - Right to be forgotten implementation

#### Week 12: Testing & Deployment

1. **Testing**
   - Unit tests (pytest)
   - Integration tests
   - Load testing (Locust)
   - Security testing (OWASP ZAP)

2. **Deployment**
   - Docker Compose for development
   - Kubernetes manifests for production
   - CI/CD pipeline (GitHub Actions)
   - Blue-green deployment

3. **Documentation**
   - API documentation (OpenAPI/Swagger)
   - User manual for NTRO analysts
   - Admin guide for deployment
   - Incident response playbook

---

## 🎯 MVP Feature Checklist (8-Week Target)

### **Core Autonomous Features** ✅

- [ ] **Seed Management**
  - [ ] Add/edit/delete seeds
  - [ ] Priority levels (1-4)
  - [ ] Frequency scheduling (hourly/daily/weekly)
  - [ ] Enable/disable seeds
  - [ ] Credibility scoring

- [ ] **Autonomous Scraping**
  - [ ] Celery task queue
  - [ ] Hourly scheduled scraping
  - [ ] Distributed Scrapy workers
  - [ ] Job status tracking
  - [ ] Error handling & retries

- [ ] **Deep/Dark Web**
  - [ ] Tor integration
  - [ ] .onion site support
  - [ ] Circuit renewal
  - [ ] Puppeteer JS rendering
  - [ ] Forum crawlers (BitcoinTalk, Reddit)

- [ ] **Auto-Enrichment**
  - [ ] Blockchain API lookups
  - [ ] ML categorization
  - [ ] spaCy NER for PII
  - [ ] Geo-IP resolution
  - [ ] WHOIS/DNS lookup

- [ ] **Alerting**
  - [ ] Watchlist management
  - [ ] Alert conditions (new tx, large transfer, balance change)
  - [ ] WebSocket live alerts
  - [ ] Email notifications
  - [ ] Webhook integrations

- [ ] **Graph Analysis**
  - [ ] Neo4j integration
  - [ ] Transaction graph
  - [ ] Cluster detection
  - [ ] Interactive visualization

### **Infrastructure** ✅

- [ ] **Databases**
  - [ ] PostgreSQL (addresses, jobs, seeds)
  - [ ] Redis (cache, task queue)
  - [ ] Neo4j (transaction graph)
  - [ ] ElasticSearch (full-text search)

- [ ] **Queue & Scheduler**
  - [ ] Celery workers
  - [ ] Celery Beat scheduler
  - [ ] Dead letter queue
  - [ ] Priority queue

- [ ] **Monitoring**
  - [ ] Prometheus metrics
  - [ ] Grafana dashboards
  - [ ] Error tracking
  - [ ] Performance profiling

### **Frontend** ✅

- [ ] **New Views**
  - [ ] Seed Manager
  - [ ] Job Monitor (live updates)
  - [ ] Watchlist Manager
  - [ ] Alerts Dashboard
  - [ ] Graph Visualization

- [ ] **Enhancements**
  - [ ] WebSocket real-time updates
  - [ ] Autonomous mode toggle
  - [ ] Tor status indicator
  - [ ] Live job stats

---

## 📊 Success Metrics

### **Autonomous Operation**
- ✅ **24/7 Uptime**: System runs continuously without manual intervention
- ✅ **Seeds Crawled**: >100 seeds scheduled and crawled automatically
- ✅ **Discovery Rate**: >1,000 addresses/day discovered autonomously
- ✅ **Enrichment Rate**: >90% of discovered addresses auto-enriched within 1 hour

### **Deep Web Coverage**
- ✅ **Tor Connectivity**: 99%+ uptime on Tor circuit
- ✅ **.onion Sites**: >20 darknet markets/forums monitored
- ✅ **JS Rendering**: >95% success rate on dynamic sites

### **Alert Responsiveness**
- ✅ **Alert Latency**: <5 minutes from event to notification
- ✅ **False Positive Rate**: <10% for watchlist alerts
- ✅ **Notification Delivery**: >99% email/webhook delivery success

### **Scalability**
- ✅ **Concurrent Jobs**: >50 scraping jobs running simultaneously
- ✅ **Throughput**: >10,000 pages/hour crawled
- ✅ **Database Performance**: <100ms query latency (p95)

---

## 🚨 Critical Success Factors

### **For SIH Demo (4-Week Target)**

1. **Show Autonomous Operation**
   - Live demo of seeds being crawled automatically (not manual)
   - Job Monitor showing recent autonomous jobs with stats
   - Seed Manager with 10+ pre-configured seeds running

2. **Demonstrate Deep Web**
   - Tor status indicator showing "Connected"
   - At least 3 .onion seeds configured
   - Screenshots/video of successful darknet scraping

3. **Prove Auto-Enrichment**
   - Show newly discovered address → auto-enriched → categorized → stored
   - <1 minute end-to-end latency
   - ML categorization confidence scores visible

4. **Working Alerts**
   - Add address to watchlist in demo
   - Trigger alert (simulate new transaction)
   - Show real-time alert notification

### **Technical Priorities**

**Week 1-2**: Seed Manager + Celery + Autonomous scraping (CRITICAL)
**Week 3-4**: Tor integration + .onion scraping (HIGH - 15% eval weight)
**Week 5-6**: Auto-enrichment + Alerting (HIGH - differentiator)
**Week 7-8**: Graph DB + Visualization (MEDIUM - impressive but not required)

### **Demo Day Strategy**

**5-Minute Pitch**:
1. Problem: Manual investigation doesn't scale
2. Solution: **Autonomous** 24/7 OSINT pipeline
3. Live Demo:
   - Show Job Monitor with autonomous jobs running
   - Navigate to Seed Manager → show 20+ active seeds
   - Click "Analytics" → show addresses discovered **today** (auto-enriched)
   - Watchlist → trigger alert → show real-time notification
4. Deep Web: Show Tor indicator + .onion seeds configured
5. Impact: "Discovered 5,000 addresses this week, fully autonomous, zero manual intervention"

---

## 💡 Quick Wins for Next 48 Hours

### **Immediate Actions** (Can be done this weekend)

1. **Install Dependencies**
```bash
# Redis (task queue)
# Windows: https://github.com/microsoftarchive/redis/releases
# Run: redis-server

# Celery
pip install celery redis

# Tor Browser
# Download: https://www.torproject.org/download/
# Configure SOCKS5 proxy on port 9050
```

2. **Create Celery Worker** (2 hours)
- Copy code from Week 1-2 section above
- Create `backend/celery_app.py`
- Create `backend/tasks.py`
- Run: `celery -A celery_app worker --loglevel=info`

3. **Seed Manager Backend** (3 hours)
- Create `backend/seed_manager.py`
- Add `/api/seeds` endpoints to `test_server.py`
- Test with Postman

4. **Seed Manager Frontend** (3 hours)
- Create `frontend/src/components/SeedManager.jsx`
- Add to App.js navigation
- Test adding/viewing seeds

**Total Time**: 8-10 hours = **1 weekend sprint** to have autonomous scraping working!

---

## 🎓 Learning Resources

### **Celery & Task Queues**
- [Celery Documentation](https://docs.celeryproject.org/)
- [Redis Quick Start](https://redis.io/topics/quickstart)

### **Distributed Crawling**
- [Scrapy-Redis Guide](https://github.com/rmax/scrapy-redis)
- [Scrapy Best Practices](https://docs.scrapy.org/en/latest/topics/practices.html)

### **Tor Integration**
- [Stem (Tor Controller)](https://stem.torproject.org/)
- [Tor Configuration](https://2019.www.torproject.org/docs/tor-manual.html)

### **Graph Databases**
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [Cytoscape.js Documentation](https://js.cytoscape.org/)

---

## 🏆 Final Thoughts

Your current system is a **strong foundation** (30% complete) with excellent components:
- Blockchair API (world-class blockchain data)
- ML categorization (11 categories)
- Professional UI/UX

But to win SIH and meet NTRO's requirements, you need **autonomous operation**:
- Continuous scraping without manual intervention
- Deep web monitoring via Tor
- Auto-enrichment pipeline
- Real-time alerting

**The good news**: 70% of the missing functionality is **orchestration and plumbing**, not advanced algorithms. You already have the hard parts (Blockchair, ML, frontend).

**Focus on Week 1-4 roadmap** above. If you execute Weeks 1-2 (Seed Manager + Celery), you'll have a working autonomous system to demo. Add Weeks 3-4 (Tor) and you'll have a **winning differentiator**.

**You can do this! The architecture is clear, the code examples are provided, and the timeline is realistic. Go build the autonomous system NTRO needs! 🚀**

---

**Document Version**: 1.0  
**Created**: October 12, 2025  
**Estimated Implementation**: 4-8 weeks MVP, 12 weeks production  
**Priority**: 🔴 CRITICAL - Core SIH requirement
