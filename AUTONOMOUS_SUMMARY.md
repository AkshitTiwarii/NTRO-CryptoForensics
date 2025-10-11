# 🎯 Autonomous Scraping - Everything You Need

## 📁 New Files Created

1. **setup_redis.ps1** - One-time setup script
   - Installs Redis + Celery
   - Tests connection
   - Shows next steps

2. **start_all.ps1** - Start all services
   - Runs 5 services in separate terminals
   - Backend + Worker + Beat + Frontend + Redis

3. **check_status.ps1** - Health check
   - Shows what's running
   - Tests connections
   - Diagnoses issues

4. **AUTONOMOUS_SCRAPING_GUIDE.md** - Complete documentation
   - Architecture details
   - Configuration options
   - Troubleshooting guide

5. **QUICK_START_AUTONOMOUS.md** - Quick reference
   - Simple step-by-step
   - For beginners

## 🔄 Code Changes

### backend/server.py
- ✅ Re-enabled Celery import (with fallback)
- ✅ Smart detection: Use Celery if available, otherwise sync
- ✅ No errors if Redis not installed
- ✅ Works both ways: manual OR autonomous

## 🎮 How to Use (3 Steps)

### Step 1: Setup (One-time - 5 minutes)
```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData
.\setup_redis.ps1
```

### Step 2: Start (Every time you use the system)
```powershell
.\start_all.ps1
```

### Step 3: Enable Seeds
- Open http://localhost:3000
- Scraping → Seed Manager
- Toggle ON the seeds you want
- Done! Scrapes automatically every hour

## 📊 What Happens Automatically

```
Top of Every Hour (e.g., 3:00, 4:00, 5:00...):
├── Celery Beat triggers "autonomous-scraping-hourly"
├── Celery Worker picks up the task
├── Scraper visits all ENABLED seeds
├── Extracts Bitcoin/Ethereum addresses
├── Saves to MongoDB
└── Updates seed statistics

Every 30 Minutes:
└── Enriches addresses (blockchain data)

Every 15 Minutes:
└── Checks watchlist alerts

Daily at 2 AM:
└── Cleans up old job records
```

## 🎯 Current vs New

### Current System (Manual):
```
You → Click Play → Scraper → Addresses
```
**Problem**: You have to be there, manual work

### New System (Autonomous):
```
Celery Beat → Scheduled Task → Worker → Scraper → Addresses
            (every hour)      (background)
```
**Benefit**: Runs 24/7, no manual work!

## ⚡ Terminal Windows

When you run `start_all.ps1`, you'll see **5 windows**:

1. **Backend Server** (Blue)
   ```
   INFO: Uvicorn running on http://0.0.0.0:8000
   ✅ Celery tasks loaded - Autonomous scraping enabled
   ```

2. **Celery Worker** (Green)
   ```
   celery@YOURPC ready
   Tasks: autonomous_scrape, enrich_pending_addresses...
   ```

3. **Celery Beat** (Yellow)
   ```
   Scheduler: Sending due task autonomous-scraping-hourly
   ```

4. **Frontend** (Cyan)
   ```
   webpack compiled successfully
   ```

5. **Redis** (Hidden, background process)

## 🔍 Monitoring

### Check if autonomous scraping is working:

1. **Look at Celery Beat window**:
   ```
   [2025-10-12 15:00:00] autonomous-scraping-hourly sent
   ```

2. **Look at Celery Worker window**:
   ```
   [autonomous_scrape] Scraping seed: BitcoinTalk - Marketplace
   [autonomous_scrape] Found 15 addresses
   ```

3. **Check the UI**:
   - Addresses → Search Registry
   - "Last Crawled" timestamp updates
   - "Addresses Found" counter increases

## 🎓 Pro Tips

1. **Keep windows minimized** - They need to stay open but don't need to be visible

2. **Enable good seeds first** - Start with BitcoinTalk, Reddit, GitHub

3. **Dark web needs Tor** - Keep Tor Browser running for 🧅 seeds

4. **First scrape timing** - If you enable seeds at 3:15 PM, first scrape is at 4:00 PM

5. **Check logs for errors** - Worker window shows if a seed fails

## 🚨 Troubleshooting

### "Redis connection failed"
```powershell
# Start Redis manually
redis-server
```

### "Celery worker not responding"
- Close worker window
- Run again: `celery -A celery_app worker --pool=solo --loglevel=info`

### "No autonomous scraping"
- Check Celery Beat window is open
- Look for "Sending due task" messages
- Verify seeds are ENABLED (toggle ON)

### "Module not found"
```powershell
pip install redis celery
```

## 📈 Expected Results

After 1 hour of running:
- ✅ First autonomous scrape completed
- ✅ Addresses in database
- ✅ Seed stats updated
- ✅ "Last Crawled" shows recent time

After 24 hours:
- ✅ 24 autonomous scrapes completed
- ✅ Hundreds (or thousands) of addresses
- ✅ Continuous data growth
- ✅ No manual work!

## 🎯 Summary

**Old Way**: Manual clicking, limited data
**New Way**: 24/7 autonomous collection, massive dataset

**Setup Time**: 5 minutes (one-time)
**Daily Effort**: Just keep terminals open
**Result**: Continuous cryptocurrency intelligence gathering

---

## ✅ Ready to Start?

```powershell
# 1. Setup (one-time)
.\setup_redis.ps1

# 2. Start all services
.\start_all.ps1

# 3. Open browser
# http://localhost:3000

# 4. Enable seeds
# Scraping → Seed Manager → Toggle ON

# 5. Wait 1 hour for magic! ✨
```

**Questions?** Check `AUTONOMOUS_SCRAPING_GUIDE.md` for detailed docs!
