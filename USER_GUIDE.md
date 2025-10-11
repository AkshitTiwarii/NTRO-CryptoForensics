# 📖 NTRO CryptoForensics - Complete User Guide

## 🎯 Overview
This system helps law enforcement track cryptocurrency addresses across the web by:
1. **Scraping** websites to find crypto addresses
2. **Storing** them in a database
3. **Analyzing** patterns and risks
4. **Visualizing** connections between addresses

---

## 📂 Menu Options Explained (Left Sidebar)

### 1️⃣ **Dashboard** 📊
**What it does:** Shows an overview of your entire system
**You'll see:**
- Total addresses collected
- High-risk addresses (score above 70)
- Monitored wallets on watchlist
- Recent updates in last 24 hours
- Charts showing cryptocurrency distribution
- Category breakdown (scams, darknet, etc.)

**When to use:** First thing after login to see overall status

---

### 2️⃣ **Address Registry** 🔍
**What it does:** Search and browse all cryptocurrency addresses you've collected
**You'll see:**
- Complete list of all scraped addresses
- Details: Type (BTC/ETH/etc), Category, Risk Score, Balance
- Search bar to find specific addresses
- Filter by crypto type or category

**How to view scraped data HERE:**
1. Click "Address Registry" in sidebar
2. You'll see a table with all addresses found by scraping
3. Click on any address to see full details
4. Use search box to find specific wallets

**Example:** After scraping BitcoinTalk forums, all Bitcoin addresses found will appear in this list.

---

### 3️⃣ **Register Address** ➕
**What it does:** Manually add a cryptocurrency address to the database
**You'll see:** Form with fields:
- Address (the actual wallet address)
- Cryptocurrency Type (Bitcoin, Ethereum, etc.)
- Category (Scam, Darknet Market, Ransomware, etc.)
- Risk Score (0-100)
- Notes/Tags

**When to use:** 
- You found an address during manual investigation
- Informant provides a suspicious wallet
- Need to add known scam addresses

---

### 4️⃣ **OSINT Scraper** 🕸️
**What it does:** Scrape deep web/.onion sites for crypto addresses
**You'll see:**
- Manual scraper interface
- URL input field
- Deep web toggle (.onion support)
- Results showing extracted addresses

**When to use:**
- Investigating specific dark web marketplaces
- One-off scraping of a suspicious forum
- Testing if a site contains crypto addresses

**How it works:**
1. Enter URL (e.g., `http://darkmarketxyz.onion`)
2. Enable "Deep Web" if it's a .onion site
3. Click "Scrape"
4. Addresses found will be saved to Address Registry

---

### 5️⃣ **Seed Manager** 🌱 **[MOST IMPORTANT FOR AUTO-SCRAPING]**
**What it does:** Manage automated scraping sources (seed URLs)
**You'll see:**
- List of 10 pre-configured websites to scrape
- Statistics: Total Seeds, Active Seeds, Addresses Found, Success Rate
- Each seed shows:
  - Name (e.g., "BitcoinTalk - Marketplace")
  - URL
  - Category (forum/medium/high priority)
  - Scraping frequency (daily/weekly)
  - Last crawled timestamp
  - Play button (▶) to manually trigger scrape
  - Toggle to enable/disable
  - Delete button (🗑️)

**How to view scraped data from seeds:**
1. Look at "Addresses Found" column - shows how many addresses each seed discovered
2. Click the **Play button (▶)** to scrape that seed right now
3. Wait for completion message (e.g., "Found 5 addresses")
4. Go to **Address Registry** to see the newly found addresses
5. Each address will have metadata showing which seed found it

**Pre-configured Seeds:**
1. **BitcoinTalk - Marketplace** (forum, High priority, daily)
   - Bitcoin marketplace discussions
   
2. **BitcoinTalk - Scam Accusations** (forum, Medium, daily)
   - Forum for reporting Bitcoin scams
   
3. **Reddit - r/Bitcoin** (forum, Medium, daily)
   - Bitcoin subreddit discussions
   
4. **Blockchain.info - Recent Transactions** (blockchain, High, hourly)
   - Live Bitcoin transactions
   
5. **Etherscan - Recent Transactions** (blockchain, High, hourly)
   - Live Ethereum transactions
   
6. **GitHub - Cryptocurrency Projects** (code, Low, weekly)
   - Developer crypto addresses
   
7. **Twitter - Crypto Scam Alerts** (social, Medium, daily)
   - Scam warnings with addresses
   
8. **Pastebin - Recent Pastes** (leak, High, hourly)
   - Data leaks with crypto addresses
   
9. **Dark Web Market Monitor** (darknet, High, daily)
   - .onion marketplace monitoring
   
10. **Ransomware Tracker** (security, High, daily)
    - Known ransomware payment addresses

**How autonomous scraping works:**
- Every seed has a schedule (hourly/daily/weekly)
- Backend automatically scrapes them
- Requires Redis + Celery workers (currently in demo mode)

---

### 6️⃣ **Network Graph** 🕸️
**What it does:** Visualize connections between crypto addresses
**You'll see:**
- Interactive graph/network diagram
- Nodes = cryptocurrency addresses
- Lines = transactions/connections between them
- Clustering of related addresses

**When to use:**
- Investigating money laundering networks
- Tracking ransomware payment flows
- Finding connected scam operations

**Example:** If Address A sent money to Address B, you'll see them connected.

---

### 7️⃣ **Analytics** 📈
**What it does:** Statistical analysis and trends
**You'll see:**
- Category distribution (pie chart)
- Cryptocurrency type breakdown
- Risk score distribution
- Timeline of address discoveries
- Top categories by count

**When to use:**
- Monthly reports to management
- Understanding which threat types are most common
- Identifying trends (e.g., increase in ransomware)

---

### 8️⃣ **Alerts & Watchlists** 🔔
**What it does:** Monitor specific addresses for activity
**You'll see:**
- List of monitored addresses
- Alert rules (e.g., "notify if balance changes")
- Notification history
- Risk threshold settings

**When to use:**
- Monitoring known criminal wallets
- Tracking addresses under investigation
- Getting alerts when targets move money

**Example:** Add a ransomware payment address to get notified when funds are withdrawn.

---

### 9️⃣ **Data Export** 📥
**What it does:** Generate reports in CSV/JSON format
**You'll see:**
- Export options (CSV, JSON, Excel)
- Filter options (date range, category, crypto type)
- Download buttons

**When to use:**
- Creating evidence for court cases
- Sharing data with other agencies
- Backup of investigation data
- Analysis in Excel/other tools

---

## 🔄 Complete Workflow: From Scraping to Viewing Data

### **Scenario: Finding addresses from a scam forum**

1. **Navigate to Seed Manager**
   - Click "Seed Manager" in sidebar
   
2. **Trigger a scrape**
   - Find "BitcoinTalk - Scam Accusations" seed
   - Click the **Play button (▶)**
   - Wait for message: "Scraping completed! Found 8 addresses"
   
3. **View the results**
   - Click "Address Registry" in sidebar
   - You'll see 8 new addresses in the list
   - They'll be tagged with category "scam"
   
4. **Investigate specific address**
   - Click on any address row
   - Modal popup shows:
     * Full wallet address
     * Balance (if available from blockchain API)
     * Risk score
     * Category
     * When it was discovered
     * Which seed found it
     * Transaction history
     
5. **Add to watchlist (optional)**
   - From address details, click "Add to Watchlist"
   - Set alert rules
   - Get notified of changes

6. **Export for reporting**
   - Go to "Data Export"
   - Select date range: "Last 24 hours"
   - Choose format: CSV
   - Click "Export"
   - Share with team

---

## 🚀 Quick Start Guide

### **First Time Using the System:**

1. **Login**
   - Username: `admin`
   - Password: `admin123`

2. **Check Dashboard**
   - See current statistics (will be 0 if fresh install)

3. **Run Your First Scrape**
   - Go to "Seed Manager"
   - Click Play (▶) on "BitcoinTalk - Marketplace"
   - Wait 10-30 seconds
   - See "Addresses Found" number increase

4. **View Results**
   - Go to "Address Registry"
   - Browse all discovered addresses
   - Click any address to see details

5. **Manually Add an Address**
   - Go to "Register Address"
   - Fill in:
     * Address: `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` (example)
     * Type: Bitcoin
     * Category: Scam
     * Risk Score: 85
     * Notes: "Reported by victim on 12/10/2025"
   - Click "Submit"

6. **Check Analytics**
   - Go to "Analytics"
   - See charts showing your data

---

## ❓ Why You Can't See Data

### **Possible Reasons:**

1. **No Scraping Done Yet**
   - Solution: Go to Seed Manager → Click Play button on any seed
   
2. **Database Empty (Fresh Install)**
   - Solution: MongoDB was just started, no historical data exists
   - Fix: Run manual scrapes to populate database
   
3. **Redis Not Running (Autonomous Mode Disabled)**
   - Current Status: Demo mode - scraping returns simulated 0-15 addresses
   - Solution: For real data, install Redis (optional)
   - Impact: Manual scraping still works, just returns simulated counts
   
4. **Backend Not Connected**
   - Check: Backend logs show "MongoDB connected"
   - Fix: Ensure backend is running on port 8000

5. **Frontend Cache Issue**
   - Solution: Clear browser cache (Ctrl+Shift+Delete)
   - Hard refresh: Ctrl+F5

---

## 🔧 Current System Status

### ✅ **Working:**
- ✅ Login/Authentication
- ✅ Dashboard display
- ✅ MongoDB connected
- ✅ Theme toggle (Dark/Light)
- ✅ All menu navigation
- ✅ Manual address registration
- ✅ Seed Manager interface
- ✅ Demo mode scraping (simulated results)

### ⚠️ **Demo Mode (No Real Data Yet):**
- ⚠️ Scraping returns random 0-15 addresses (simulated)
- ⚠️ No real network requests to target websites
- ⚠️ Statistics show 0 because database is empty
- ⚠️ Need to run actual scrapes or manually add addresses

### 🚀 **To Get Real Data:**

**Option 1: Manual Address Entry (Immediate)**
1. Go to "Register Address"
2. Add 5-10 test addresses manually
3. Check "Address Registry" to see them
4. Dashboard will update with statistics

**Option 2: Install Redis for Real Scraping**
1. Redis already running in Docker ✅
2. Need to start Celery workers:
   ```powershell
   cd backend
   celery -A celery_app worker --loglevel=info --pool=solo
   ```
3. Scraping will fetch real addresses from websites
4. Database will populate automatically

**Option 3: Test with Sample Data**
- I can create a script to populate sample addresses for testing

---

## 📝 Understanding Each Data Field

### **Address Registry Columns:**

| Column | Meaning | Example |
|--------|---------|---------|
| **Address** | Cryptocurrency wallet address | `1A1zP1eP...` |
| **Type** | Blockchain (BTC/ETH/XMR/etc) | `Bitcoin` |
| **Category** | Threat classification | `Scam` |
| **Risk Score** | Danger level (0-100) | `85` |
| **Balance** | Current wallet balance | `0.0052 BTC` |
| **First Seen** | When address was discovered | `12/10/2025` |
| **Last Updated** | Last time info was refreshed | `12/10/2025 2:00 AM` |
| **Source** | How it was found | `BitcoinTalk Scraper` |

---

## 🎓 Training Scenarios

### **Exercise 1: Basic Scraping**
1. Open Seed Manager
2. Click Play on "BitcoinTalk - Marketplace"
3. Wait for completion
4. Go to Address Registry
5. Verify addresses appear
**Expected Result:** See new addresses in registry

### **Exercise 2: Manual Investigation**
1. Go to OSINT Scraper
2. Enter URL: `https://bitcointalk.org/index.php?board=83.0`
3. Click "Scrape"
4. Review extracted addresses
**Expected Result:** Manual scrape finds addresses

### **Exercise 3: Watchlist Setup**
1. Find a high-risk address in Address Registry
2. Click on it to open details
3. Click "Add to Watchlist"
4. Set alert threshold
5. Go to "Alerts & Watchlists" to verify
**Expected Result:** Address monitored for changes

---

## 🆘 Troubleshooting

### **"No data available" on Dashboard**
- Database is empty
- Run scrapes or manually add addresses

### **Scraping returns 0 addresses**
- Demo mode active (Redis not running)
- Or target website has no crypto addresses
- Check seed URL is valid

### **Can't see newly scraped addresses**
- Check Address Registry (not Dashboard)
- Refresh page (F5)
- Check backend logs for errors

### **Balance shows "Unknown"**
- Blockchain API limits reached
- Address has no transactions
- Network connectivity issue

---

## 📞 Need More Help?

**Quick Reference:**
- Login Page → Enter credentials
- Dashboard → Overview
- **Address Registry** → **VIEW ALL SCRAPED DATA HERE** ← **MAIN DATA VIEW**
- Seed Manager → Trigger scrapes with Play button
- Register Address → Add addresses manually

**Remember:** The **Address Registry** is where ALL scraped data appears!

---

**Last Updated:** October 12, 2025  
**Version:** 1.0  
**System Status:** Demo Mode Active (MongoDB connected, Redis optional)
