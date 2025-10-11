# 🚀 Quick Start: Enable Autonomous Scraping

## What is Autonomous Scraping?

Instead of manually clicking "Play" on each seed, the system will **automatically scrape all enabled seeds every hour** in the background.

## 📋 Setup (One-time)

### Step 1: Install Redis + Celery

Open PowerShell as **Administrator** and run:

```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData
.\setup_redis.ps1
```

This installs:
- ✅ Redis (message broker)
- ✅ Celery (task queue)
- ✅ Python dependencies

Takes ~5 minutes.

### Step 2: Start All Services

```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData
.\start_all.ps1
```

This opens **5 terminal windows**:
1. Backend Server
2. Celery Worker
3. Celery Beat (Scheduler)
4. Frontend
5. (MongoDB should already be running)

## 🎯 How to Use

1. **Open the app**: http://localhost:3000

2. **Enable seeds**:
   - Go to: Scraping → Seed Manager
   - Toggle ON the seeds you want
   - Dark web seeds (🧅) require Tor Browser

3. **Sit back and relax!**
   - Seeds scrape automatically every hour
   - New addresses appear in the database
   - No manual work needed!

## ⏰ Automatic Schedule

- **Every Hour (on the hour)**: Scrape all enabled seeds
- **Every 30 minutes**: Enrich addresses with blockchain data
- **Every 15 minutes**: Check watchlist alerts
- **Daily at 2 AM**: Cleanup old jobs

## 🔍 Check Status

Run this anytime to see what's running:

```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData
.\check_status.ps1
```

## 📊 Difference: Manual vs Autonomous

### Manual Mode (Before):
- ❌ Click Play on each seed
- ❌ Wait for results
- ❌ Repeat every time you want data
- ❌ No scraping when you're away

### Autonomous Mode (After):
- ✅ Enable seed once
- ✅ Scrapes automatically every hour
- ✅ Runs in background
- ✅ Scrapes 24/7 even when you're asleep!

## 🎮 Quick Commands

```powershell
# Setup (one-time)
.\setup_redis.ps1

# Start everything
.\start_all.ps1

# Check status
.\check_status.ps1

# Stop everything (close all terminal windows)
```

## ⚠️ Important Notes

1. **Keep terminals open**: Don't close the 5 terminal windows
2. **Tor for dark web**: Keep Tor Browser running for 🧅 seeds
3. **MongoDB must be running**: Start it before `start_all.ps1`
4. **First scrape**: Might take up to 1 hour (wait for top of hour)

## 🎯 Next Steps

1. **Run `setup_redis.ps1`** (one-time setup)
2. **Run `start_all.ps1`** (every time you use the system)
3. **Enable seeds** in the UI
4. **Wait 1 hour** for first automatic scrape
5. **Check results** in Addresses → Search Registry

## 🏆 Benefits

- 📈 **24/7 data collection**
- 🔄 **Always up-to-date**
- 💤 **Works while you sleep**
- 🎯 **Set it and forget it**
- 📊 **More data = better analysis**

---

**Ready to go?** Run `.\setup_redis.ps1` now!
