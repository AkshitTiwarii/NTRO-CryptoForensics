# 🎯 Quick Reference: Where is My Data?

## ❓ The Problem
**"I scraped websites but I can't see the data anywhere!"**

## ✅ The Solution
All scraped cryptocurrency addresses appear in: **📂 Address Registry**

---

## 📍 Step-by-Step: View Scraped Data

### **Method 1: After Automated Scraping**
```
1. Click "Seed Manager" (left sidebar)
2. Click Play button (▶) on any seed
3. Wait for "Scraping completed! Found X addresses"
4. Click "Address Registry" (left sidebar)  ← YOUR DATA IS HERE
5. See table with all found addresses
```

### **Method 2: View All Addresses**
```
1. Click "Address Registry" directly
2. Browse complete list of all addresses
3. Click any row to see full details
4. Use search box to filter
```

---

## 📊 Menu Structure (Simple)

```
├── 📊 Dashboard (Overview - shows counts)
├── 📂 Address Registry  ← ALL DATA APPEARS HERE! 
├── ➕ Register Address (Manually add addresses)
├── 🕸️ OSINT Scraper (One-off manual scraping)
├── 🌱 Seed Manager (Automatic scraping - click Play ▶)
├── 🕸️ Network Graph (Visual connections)
├── 📈 Analytics (Charts and stats)
├── 🔔 Alerts & Watchlists (Monitoring)
└── 📥 Data Export (Download CSV/JSON)
```

---

## 🔄 Data Flow Diagram

```
[Seed Manager] → Click Play (▶)
       ↓
[Backend Scrapes Website]
       ↓
[Finds Crypto Addresses]
       ↓
[Saves to MongoDB Database]
       ↓
[📂 Address Registry Shows Results]  ← VIEW HERE
```

---

## 🎯 What Each Menu Does (1-Line Summary)

| Menu | Purpose | See Data Here? |
|------|---------|----------------|
| Dashboard | Overview stats | ❌ Shows counts only |
| **Address Registry** | **Browse all addresses** | ✅ **YES - MAIN DATA VIEW** |
| Register Address | Add addresses manually | ❌ Input form only |
| OSINT Scraper | Manual one-off scraping | ⚠️ Shows results, but saves to Address Registry |
| Seed Manager | Auto-scraping setup | ⚠️ Shows stats, data appears in Address Registry |
| Network Graph | Visual network map | ✅ YES - but visual only |
| Analytics | Charts and trends | ✅ YES - but summarized |
| Alerts | Monitoring specific addresses | ⚠️ Watchlist only |
| Data Export | Download files | ❌ Export function only |

---

## 💡 Why Dashboard Shows "0"

**Dashboard shows:**
- **Total Addresses:** 0
- **High Risk:** 0  
- **Watchlist:** 0
- **24h Updates:** 0

**Reason:** Database is empty (fresh MongoDB install)

**Fix:**
1. Go to Seed Manager
2. Click Play (▶) on "BitcoinTalk - Marketplace"
3. Wait for completion
4. Refresh Dashboard → Numbers will update
5. Go to Address Registry → See actual addresses

---

## 🚀 Your First Task (3 Minutes)

### **Goal: Get data showing in the system**

1. **Open Seed Manager**
   - Left sidebar → Click "Seed Manager"

2. **Trigger a scrape**
   - Find "BitcoinTalk - Marketplace" (first seed)
   - Click the **Play button (▶)** on the right
   - Wait 10-30 seconds

3. **Check results**
   - Message appears: "Scraping completed! Found X addresses"
   - Note the number (e.g., "Found 8 addresses")

4. **View the data**
   - Left sidebar → Click **"Address Registry"**
   - YOU WILL SEE A TABLE WITH ADDRESSES
   - Each row = one cryptocurrency address found

5. **Explore details**
   - Click on any row in the table
   - Popup shows full details:
     * Wallet address
     * Type (Bitcoin/Ethereum/etc)
     * Category (scam/marketplace/etc)
     * Risk score
     * Balance (if available)
     * When found
     * Which seed discovered it

6. **Check Dashboard**
   - Go back to Dashboard
   - "Total Addresses" will show the count
   - Charts will populate

**Done! You now have data in the system.**

---

## 🔍 Understanding Seed Manager

### **What you see in Seed Manager:**

```
┌─────────────────────────────────────────────────────────┐
│ Total Seeds: 10    Active: 9    Addresses Found: 14     │
│ Success Rate: 100%                                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ BitcoinTalk - Marketplace         [forum] [High] [daily]│
│ https://bitcointalk.org/...                              │
│ Bitcoin marketplace discussions                          │
│                                                          │
│ Addresses Found: 14     Last Crawled: 12/10/2025 2:00am │
│ Total Crawls: 1         Success Rate: 100%               │
│                                                          │
│ [Toggle ON/OFF]  [▶ Play]  [🗑️ Delete]                  │
└─────────────────────────────────────────────────────────┘
```

### **What each button does:**

- **Toggle Switch:** Enable/disable automatic scheduled scraping
- **▶ Play Button:** Manually trigger scrape RIGHT NOW
- **🗑️ Delete:** Remove this seed from the system

### **"Addresses Found: 14"**
- This means this seed has discovered 14 addresses total
- To see those 14 addresses → Go to **Address Registry**

---

## 📝 Example Workflow

### **Scenario: Investigating a scam forum**

**Step 1: Setup**
- Seed: "BitcoinTalk - Scam Accusations"
- URL: https://bitcointalk.org/index.php?board=159.0
- Already pre-configured in Seed Manager

**Step 2: Scrape**
- Click Play (▶) button
- System scrapes the forum
- Finds 5 Bitcoin addresses mentioned in scam reports

**Step 3: View Data**
- Go to Address Registry
- See 5 new rows:
  ```
  1A1zP1... | Bitcoin | Scam | 85 | 0.0052 BTC | 12/10/2025
  3J98t1... | Bitcoin | Scam | 90 | 0.0000 BTC | 12/10/2025
  bc1qxy2... | Bitcoin | Scam | 75 | 0.0123 BTC | 12/10/2025
  (etc...)
  ```

**Step 4: Investigate**
- Click on row with highest risk score (90)
- See full details in popup
- Note: "Source: BitcoinTalk - Scam Accusations"

**Step 5: Action**
- Add high-risk address to watchlist
- Export to CSV for report
- Share with team

---

## 🆘 Still Can't See Data?

### **Checklist:**

- ✅ Backend running? (Check terminal - should show "MongoDB connected")
- ✅ MongoDB running? (Docker container `crypto-mongodb` active)
- ✅ Did you click Play button in Seed Manager?
- ✅ Did you wait for completion message?
- ✅ Are you looking in **Address Registry** (not Dashboard)?
- ✅ Did you refresh the page? (Press F5)

### **If still empty:**

**Option A: Add test data manually**
1. Go to "Register Address"
2. Add a test address:
   - Address: `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
   - Type: Bitcoin
   - Category: Test
   - Risk: 50
3. Go to Address Registry
4. You should see your test address

**Option B: Check backend logs**
- Look for errors in terminal where backend is running
- Should show: "Scraping completed successfully"

---

## 🎓 Summary

### **Key Points:**

1. **Scraped data appears in: Address Registry** (NOT Dashboard)
2. **Dashboard shows statistics** (counts, charts)
3. **Seed Manager triggers scraping** (Play button ▶)
4. **Address Registry shows actual data** (the table)
5. **Click rows for details** (popup with full info)

### **Data Flow:**
```
Seed Manager (▶ Play)
      ↓
   Scrape
      ↓
   Save to DB
      ↓
Address Registry (VIEW HERE!)
```

### **Most Important:**
> **📂 Address Registry = Where ALL your data lives**

---

**Need the full guide?** See `USER_GUIDE.md` for detailed explanations of every feature.

**Got it working?** Next steps:
- Set up automated scraping (requires Redis + Celery)
- Add addresses to watchlist
- Generate reports with Data Export
- Analyze patterns with Network Graph

---

**Quick Support:**
- Backend not running? → Start with `python server.py` in backend folder
- MongoDB not connected? → Start Docker: `docker start crypto-mongodb`
- Frontend not loading? → Start with `npm start` in frontend folder
- Still confused? → Read sections 1-5 of `USER_GUIDE.md`
