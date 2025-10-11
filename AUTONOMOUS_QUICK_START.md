# AUTONOMOUS SYSTEM QUICK START GUIDE

## 🚀 Getting Started with Autonomous Scraping

### Prerequisites Installed ✅
- Python 3.x
- Node.js & npm
- All Python dependencies (celery, redis, scrapy, etc.)

### Step 1: Install and Start Redis

**Option A: Download Redis for Windows**
1. Download from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`

**Option B: Use Docker** (Recommended)
```bash
docker run -d -p 6379:6379 --name redis redis:latest
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

### Step 2: Start Backend Server

```bash
cd backend
python server.py
```

Backend will run on: **http://localhost:8000**

### Step 3: Start Celery Worker

Open a new terminal in the `backend` folder:

```bash
cd backend
celery -A celery_app worker --loglevel=info --pool=solo
```

> **Note:** Use `--pool=solo` on Windows. On Linux/Mac you can omit this flag.

### Step 4: Start Celery Beat Scheduler

Open another new terminal in the `backend` folder:

```bash
cd backend
celery -A celery_app beat --loglevel=info
```

This runs the autonomous scraping schedule:
- **Every hour**: `autonomous_scrape` (collects addresses from due seeds)
- **Every 30 min**: `enrich_pending_addresses` (blockchain enrichment)
- **Every 15 min**: `check_watchlist_alerts` (alert monitoring)
- **Daily at 2 AM**: `cleanup_old_jobs` (housekeeping)

### Step 5: Start Frontend

```bash
cd frontend
npm start
```

Frontend will run on: **http://localhost:3000**

---

## 🎯 Using the Seed Manager

1. Navigate to **"Seed Manager"** in the sidebar
2. View **10 pre-configured seeds** (BitcoinTalk, Reddit, Pastebin, etc.)
3. Click **"Add Seed Source"** to add custom sources
4. Toggle seeds **ON/OFF** to enable/disable them
5. Click the **▶ Play button** to manually trigger a scrape
6. Monitor **statistics**: addresses found, success rate, last crawled

### Seed Configuration Options:
- **URL**: The website to scrape
- **Category**: forum, social, news, pastebin, market, code
- **Priority**: 1=Critical, 2=High, 3=Medium, 4=Low
- **Frequency**: hourly, daily, weekly
- **Deep Web**: Toggle ON for .onion Tor sites (requires Tor)

---

## 🧅 Optional: Tor Integration for Deep Web

### Install Tor Browser
1. Download: https://www.torproject.org/download/
2. Install and launch Tor Browser
3. Tor will run on port **9050** (SOCKS5 proxy)

### Configure Tor Control (Advanced)
Edit `torrc` file to enable control port:
```
ControlPort 9051
HashedControlPassword <your_hashed_password>
```

### Add .onion Seeds
In Seed Manager:
1. Add seed with `.onion` URL
2. Enable **"Deep Web Source"** toggle
3. Category: usually `market` or `forum`
4. Priority: **2 (High)** - rare sources

### Test Tor Connection
```python
from tor_scraper import TorScraper
tor = TorScraper()
print(tor.check_tor_connection())  # Should return True
```

---

## 📊 Monitoring Celery with Flower (Optional)

Flower provides a web UI to monitor Celery workers and tasks.

```bash
cd backend
celery -A celery_app flower --port=5555
```

Access Flower dashboard: **http://localhost:5555**

Features:
- Real-time worker status
- Task history and statistics
- Task execution timeline
- Worker resource usage

---

## 🔍 Testing Autonomous Scraping

### Test 1: Manual Trigger
1. Go to Seed Manager
2. Click ▶ on "BitcoinTalk - Marketplace" seed
3. Watch backend logs for scraping progress
4. Check addresses found count

### Test 2: Scheduled Trigger
1. Wait for the top of the hour (Celery Beat runs `autonomous_scrape`)
2. Check logs: "Starting autonomous scraping cycle..."
3. Verify seeds marked as "due" are scraped
4. Confirm addresses are extracted and categorized

### Test 3: Verify Enrichment
1. High-confidence addresses (>70%) auto-trigger enrichment
2. Enrichment calls Blockchair API
3. Adds: balance, transaction count, USD values
4. Calculates risk score (0-100)

---

## 📁 File Structure

```
CryptoData/
├── backend/
│   ├── server.py              # FastAPI server with /api/seeds endpoints
│   ├── celery_app.py          # Celery configuration + beat schedule
│   ├── tasks.py               # Autonomous scraping tasks
│   ├── seed_manager.py        # Seed management logic
│   ├── tor_scraper.py         # Tor/.onion scraping
│   ├── crypto_collector.py    # Address extraction
│   ├── ml_categorizer.py      # ML categorization
│   └── blockchair_api.py      # Blockchain intelligence
│
├── frontend/
│   └── src/
│       ├── App.js             # Main app with Seeds view
│       └── components/
│           └── SeedManager.jsx # Seed management UI
```

---

## 🐛 Troubleshooting

### Redis Connection Error
```
Error: Error 61 connecting to localhost:6379. Connection refused.
```
**Solution**: Start Redis server first (see Step 1)

### Celery Worker Not Starting
```
ERROR: No such transport: redis
```
**Solution**: Install redis package
```bash
pip install redis celery
```

### Import Errors in tasks.py
```
ModuleNotFoundError: No module named 'celery_app'
```
**Solution**: Make sure you're in the `backend` folder when starting Celery

### Tor Connection Failed
```
Error: Cannot connect to Tor proxy
```
**Solution**: 
1. Launch Tor Browser
2. Verify port 9050 is open
3. Test: `curl --socks5-hostname 127.0.0.1:9050 http://check.torproject.org/`

---

## 📈 Success Metrics

**System is working correctly when:**
- ✅ Redis responds to `ping` command
- ✅ Celery worker shows "ready" in logs
- ✅ Celery beat shows scheduled tasks
- ✅ Seed Manager UI loads 10 default seeds
- ✅ Manual scrape triggers successfully
- ✅ Addresses are found and categorized
- ✅ Hourly autonomous scraping runs automatically
- ✅ Statistics update (addresses found, success rate)

**Target Performance:**
- 🎯 **>1000 addresses/day** discovered autonomously
- 🎯 **>90% success rate** for enabled seeds
- 🎯 **<5 min** average scraping time per seed
- 🎯 **24/7 uptime** with Celery workers

---

## 🚨 Next Steps

1. **Add More Seeds**: Expand beyond 10 defaults
2. **Enable Tor**: Scrape .onion darknet markets
3. **PostgreSQL Migration**: Move from in-memory to persistent database
4. **Watchlist Alerts**: Set up email/webhook notifications
5. **Neo4j Graphs**: Add transaction graph analysis
6. **Distributed Scrapy**: Scale to multiple workers

---

## 📞 Support

For issues, check:
1. Backend logs: Look for errors in terminal running `server.py`
2. Celery logs: Check worker and beat terminals
3. Redis logs: Verify broker connectivity
4. Browser console: Frontend React errors

**Happy Autonomous Scraping! 🎉**
