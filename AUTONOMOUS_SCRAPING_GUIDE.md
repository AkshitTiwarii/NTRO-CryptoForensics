# 🚀 Autonomous Scraping Setup Guide

## Overview
Enable **autonomous scraping** where the system automatically scrapes all enabled seeds every hour without manual intervention.

## 🎯 What You Get

### Automated Tasks:
- ⏰ **Hourly Scraping**: All enabled seeds scraped automatically
- 🔄 **Address Enrichment**: Every 30 minutes
- 🔔 **Watchlist Alerts**: Every 15 minutes
- 🧹 **Cleanup**: Daily at 2 AM

## 📋 Setup Steps

### Option 1: Automated Setup (Recommended)

```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData
.\setup_redis.ps1
```

This will:
1. Install Redis via Chocolatey
2. Install Python dependencies (redis, celery)
3. Start Redis server
4. Test connection
5. Show you next steps

### Option 2: Manual Setup

1. **Install Chocolatey** (if not installed):
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

2. **Install Redis**:
```powershell
choco install redis-64 -y
```

3. **Install Python packages**:
```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
pip install redis celery
```

4. **Start Redis**:
```powershell
redis-server
```

## 🎮 Running the System

### Quick Start (All Services):
```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData
.\start_all.ps1
```

This opens 5 terminal windows:
1. **Backend Server** (FastAPI on port 8000)
2. **Celery Worker** (Processes scraping jobs)
3. **Celery Beat** (Scheduler for autonomous scraping)
4. **Frontend** (React on port 3000)
5. **MongoDB** (Should already be running)

### Manual Start (Step by Step):

**Terminal 1 - Backend:**
```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
python server.py
```

**Terminal 2 - Celery Worker:**
```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
celery -A celery_app worker --loglevel=info --pool=solo
```

**Terminal 3 - Celery Beat (Scheduler):**
```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
celery -A celery_app beat --loglevel=info
```

**Terminal 4 - Frontend:**
```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\frontend
npm start
```

## 📊 How It Works

### Architecture:
```
User → Frontend → Backend API
                      ↓
              Manual Scrape → Celery Worker → Scraper → MongoDB
                      ↓
              Celery Beat (Scheduler)
                      ↓
              Autonomous Scrape (hourly) → Celery Worker → MongoDB
```

### Schedule (Configured in `celery_app.py`):

```python
# Autonomous scraping - every hour
'autonomous-scraping-hourly': {
    'schedule': crontab(minute=0),  # Top of every hour
}

# Address enrichment - every 30 minutes
'enrichment-every-30min': {
    'schedule': crontab(minute='*/30'),
}

# Watchlist alerts - every 15 minutes
'check-watchlists-every-15min': {
    'schedule': crontab(minute='*/15'),
}

# Cleanup old jobs - daily at 2 AM
'cleanup-old-jobs-daily': {
    'schedule': crontab(hour=2, minute=0),
}
```

## 🎯 Using the System

1. **Enable Seeds**:
   - Go to http://localhost:3000
   - Navigate: Scraping → Seed Manager
   - Toggle ON the seeds you want to scrape
   - Seeds marked 🧅 (dark web) require Tor Browser running

2. **Manual Scrape** (Optional):
   - Click the ▶️ Play button on any seed
   - Results appear immediately

3. **Autonomous Scraping**:
   - Enabled seeds will scrape automatically every hour
   - Check logs in Celery Beat terminal
   - View addresses in: Addresses → Search Registry

## 🔍 Monitoring

### Check if services are running:

**Redis:**
```powershell
redis-cli ping
# Should respond: PONG
```

**Celery Worker:**
```powershell
celery -A celery_app inspect active
```

**Celery Beat Schedule:**
```powershell
celery -A celery_app inspect scheduled
```

### Logs to watch:

- **Backend Server**: Shows API requests, scraping starts
- **Celery Worker**: Shows scraping progress, addresses found
- **Celery Beat**: Shows when scheduled tasks trigger
- **Frontend**: Hot reload, compilation errors

## ⚠️ Troubleshooting

### "Redis connection failed"
- Make sure Redis is running: `Get-Process redis-server`
- Start Redis: `redis-server` or `Start-Service Redis`

### "Celery worker not responding"
- Check if worker is running
- Restart worker terminal
- Check for Python errors in worker log

### "No autonomous scraping happening"
- Check Celery Beat is running
- Look for schedule logs in Beat terminal
- Verify seeds are ENABLED (toggle ON)

### "ImportError: No module named 'celery'"
```powershell
pip install redis celery
```

## 🎛️ Configuration

### Change scraping frequency:

Edit `backend/celery_app.py`:

```python
# Every 30 minutes instead of hourly:
'autonomous-scraping-hourly': {
    'schedule': crontab(minute='*/30'),
}

# Every 6 hours:
'autonomous-scraping-hourly': {
    'schedule': crontab(minute=0, hour='*/6'),
}
```

### Add new scheduled tasks:

```python
'my-new-task': {
    'task': 'tasks.my_task_function',
    'schedule': crontab(minute='*/10'),  # Every 10 minutes
}
```

## 🚦 System Status

When everything is running correctly, you should see:

✅ 5 terminal windows open
✅ Backend: "INFO: Uvicorn running on http://0.0.0.0:8000"
✅ Worker: "celery@COMPUTERNAME ready"
✅ Beat: "Scheduler: Sending due task autonomous-scraping-hourly"
✅ Frontend: "webpack compiled successfully"
✅ MongoDB: Running on port 27017

## 📈 Performance

- **Synchronous scraping**: 5-10 seconds per seed
- **Dark web scraping**: 30-60 seconds per seed (Tor is slow)
- **Background mode**: Multiple seeds scraped in parallel
- **Memory usage**: ~200-500MB total

## 🎓 Next Steps

1. Run `setup_redis.ps1` to install everything
2. Run `start_all.ps1` to start all services
3. Open http://localhost:3000
4. Enable seeds in Seed Manager
5. Watch autonomous scraping happen every hour!

---

**Questions?** Check the Celery logs for detailed information about what's happening.
