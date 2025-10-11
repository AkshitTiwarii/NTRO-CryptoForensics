# 🌐 Web Types & Application Flow Guide

## 🔍 Understanding Web Types in the Application

Your NTRO CryptoForensics system now supports scraping from **three different web layers**:

### 1. 🌐 **Surface Web** (Standard Internet)
- **Examples**: BitcoinTalk, Reddit, Pastebin, GitHub, CoinDesk
- **Access**: Direct browser access, no special tools needed
- **Protocol**: HTTP or HTTPS
- **Badge Color**: 
  - 🌐 Green = HTTPS (encrypted)
  - 🌐 Blue = HTTP (unencrypted)
- **Current Seeds**: 10 surface web sources enabled

### 2. 🧅 **Dark Web** (Tor Network - .onion sites)
- **Examples**: Darknet markets, ransomware portals, mixing services
- **Access**: Requires Tor Browser or Tor proxy
- **Protocol**: .onion domains
- **Badge Color**: 🧅 Purple
- **Security Level**: HIGH - anonymous, encrypted routing
- **Current Seeds**: 4 Tor sources added (3 enabled, 1 disabled)

### 3. 🕸️ **Deep Web** (I2P Network - .i2p sites)
- **Examples**: Private forums, anonymous trading
- **Access**: Requires I2P router
- **Protocol**: .i2p domains  
- **Badge Color**: 🕸️ Indigo
- **Security Level**: MEDIUM-HIGH - decentralized anonymous network
- **Current Seeds**: 2 I2P sources added

---

## 📊 Complete Application Flow

### **Phase 1: Setup & Scraping** 🔄

```
1. Backend Running (port 8000)
   ├── MongoDB Connected
   ├── Seeds Loaded (16 total)
   └── API Ready

2. Frontend Running (port 3000)
   ├── React App
   └── Connected to Backend

3. Navigate: Scraping → Seed Manager
   ├── View all seed sources
   ├── See web type badges (🌐 🧅 🕸️)
   └── Click Play button on any seed
```

### **Phase 2: Scraping Process** ⚡

```
Click Play Button
   ↓
Button shows spinning loader (⏳)
   ↓
Backend scrapes the source
   ↓
Finds cryptocurrency addresses
   ↓
Stores in MongoDB (collection: addresses)
   ↓
Returns count: "Found X addresses"
   ↓
Success message appears:
   "✅ Scraping 'Seed Name' completed! 
    Found 24 addresses. 
    → Go to 'Addresses' menu to view them."
   ↓
Stats auto-refresh (1 second delay)
   ↓
Loading clears (2 second delay)
```

### **Phase 3: View Results** 👀

```
Navigate: Addresses → Search Registry
   ↓
View table of all addresses
   ├── Address (BTC/ETH)
   ├── Risk Score
   ├── First Seen
   ├── Last Seen
   ├── Balance
   ├── Transaction Count
   └── Source (e.g., "BitcoinTalk - Marketplace")
   ↓
Click on any address row
   ↓
View detailed profile
```

### **Phase 4: Network Analysis** 🔗

```
Navigate: Network Graph
   ↓
Select an address from dropdown
   ↓
View visual connections:
   ├── Incoming transactions
   ├── Outgoing transactions  
   ├── Related addresses
   └── Transaction clusters
```

### **Phase 5: Analytics** 📈

```
Navigate: Analytics
   ↓
View charts & trends:
   ├── Risk Distribution
   ├── Transaction Timeline
   ├── Address Categories
   ├── Balance Distribution
   └── Activity Heatmap
```

---

## 🎯 Finding Your Scraped Data

### **Problem**: "Where are my 24 scraped addresses?"

### **Solution**:

1. **Click** `Addresses` in top menu
2. **Select** "Search Registry" tab (default)
3. **See** table with all addresses
4. **Filter** by:
   - Source: "BitcoinTalk - Marketplace"
   - Risk Score: High/Medium/Low
   - Date Range: Last 7 days
   - Currency: BTC or ETH

### **Quick Stats**:
- **Dashboard** → Overview cards show total addresses
- **Scraping → Stats** → Shows addresses found per seed
- **Analytics** → Charts show distribution

---

## 🔧 Current Seed Sources (16 Total)

### Surface Web (10 sources) 🌐
1. ✅ BitcoinTalk - Marketplace (forum, daily)
2. ✅ BitcoinTalk - Scam Accusations (forum, daily)
3. ✅ Reddit r/Bitcoin (social, daily)
4. ✅ Reddit r/CryptoCurrency (social, daily)
5. ✅ Pastebin Bitcoin Search (pastebin, hourly)
6. ✅ Paste.ee Bitcoin (pastebin, daily)
7. ✅ CoinDesk - Crime Tag (news, daily)
8. ✅ Cointelegraph - Hacks (news, daily)
9. ✅ GitHub Bitcoin Address Search (code, weekly)
10. ❌ Twitter Bitcoin Scam Search (social, disabled)

### Dark Web - Tor (4 sources) 🧅
11. ✅ Dark Market Forum (market, daily, priority 1)
12. ✅ Ransomware Payment Portal (forum, hourly, priority 1)
13. ✅ BTC Mixer Service (market, daily, priority 2)
14. ❌ Silk Road Vendors (market, disabled)

### Deep Web - I2P (2 sources) 🕸️
15. ✅ Crypto Trade Market (market, daily, priority 2)
16. ✅ Anonymous BTC Forum (forum, weekly, priority 3)

---

## 🚀 How to Test Different Web Types

### Test Surface Web:
```
1. Go to: Scraping → Seed Manager
2. Find: BitcoinTalk - Marketplace
3. Badge shows: 🌐 Surface Web (HTTPS) [Green]
4. Click: Play button
5. Wait: Spinner shows loading
6. See: "Found X addresses → Go to Addresses"
7. Navigate: Addresses → Search Registry
```

### Test Dark Web (Demo):
```
1. Go to: Scraping → Seed Manager
2. Find: 🧅 Dark Market Forum (Tor)
3. Badge shows: 🧅 Dark Web (Tor) [Purple]
4. Click: Play button
5. Result: Demo scraping (no actual Tor connection)
6. Simulates finding addresses from darknet
```

### Test Deep Web (Demo):
```
1. Go to: Scraping → Seed Manager
2. Find: 🕸️ Crypto Trade Market (I2P)
3. Badge shows: 🕸️ Deep Web (I2P) [Indigo]
4. Click: Play button
5. Result: Demo scraping (no actual I2P connection)
6. Simulates finding addresses from I2P network
```

---

## ⚠️ Important Notes

### Demo Mode vs Production Mode:

**Current Mode**: DEMO (Redis/Celery not configured)
- Scraping runs synchronously
- Simulates finding 0-15 addresses per scrape
- No actual web requests to Tor/.onion or I2P/.i2p sites
- Updates stats immediately

**Production Mode**: (Requires Redis + Tor + I2P)
- Async task queue with Celery
- Real Tor connections for .onion sites
- Real I2P connections for .i2p sites
- Background scraping with job monitoring

### Security Warnings:

🧅 **Dark Web (Tor)**: 
- Real deployment requires Tor proxy/SOCKS5
- Illegal content warnings
- Law enforcement coordination required
- Use official Tor browser bundle

🕸️ **Deep Web (I2P)**:
- Requires I2P router installation
- Slower than Tor (garlic routing)
- Less content than Tor
- Good for forums/file sharing

---

## 🎨 Visual Indicators Guide

### Badge Colors:
- 🌐 **Green** = HTTPS (encrypted surface web)
- 🌐 **Blue** = HTTP (unencrypted surface web)
- 🧅 **Purple** = Tor dark web (.onion)
- 🕸️ **Indigo** = I2P deep web (.i2p)

### Priority Colors:
- 🔴 **Red** = Critical (priority 1) - Check hourly
- 🟠 **Orange** = High (priority 2) - Check daily
- 🟡 **Yellow** = Medium (priority 3) - Check daily
- 🔵 **Blue** = Low (priority 4) - Check weekly

### Category Colors:
- 🔵 **Blue** = Forum discussions
- 🟣 **Purple** = Social media
- 🟢 **Green** = News sites
- 🟠 **Orange** = Pastebin dumps
- 🔴 **Red** = Darknet markets
- ⚫ **Gray** = Code repositories

---

## 🔄 Refresh Instructions

After backend restart with new seeds:

1. **Hard Refresh Browser**: `Ctrl + Shift + R` (Windows)
2. **Or Clear Cache**: F12 → Application → Clear storage
3. **Navigate to**: Scraping → Seed Manager
4. **Verify**: You see 16 seeds (not just 10)
5. **Check**: Web type badges show 🌐 🧅 🕸️

---

## 📝 Quick Troubleshooting

### "I don't see the new seeds"
- **Solution**: Restart backend server (it loads seeds on startup)
- **Command**: Stop Python process, run `python server.py`

### "Play button doesn't show loading"
- **Solution**: Hard refresh browser (`Ctrl+Shift+R`)
- **Check**: Browser console for errors (F12)

### "Where are the addresses?"
- **Solution**: Click `Addresses` in top menu → Search Registry tab
- **Filter**: Use "Source" dropdown to find specific seed

### "Web type badges not showing"
- **Solution**: Hard refresh browser
- **Verify**: SeedManager.jsx has `getWebTypeInfo` function
- **Check**: Seeds have `deep_web` flag or `.onion`/`.i2p` in URL

---

## 🎓 Understanding the Complete Flow

```
📍 Start Here
   ↓
🔧 Scraping Menu
   ├── Seed Manager Tab (manage sources)
   └── Manual Scraper Tab (one-time scrapes)
   ↓
▶️ Click Play on Seed
   ↓
⏳ Loading Indicator (spinner)
   ↓
✅ Success Message
   ↓
📊 Stats Update Automatically
   ↓
📍 Navigate to Addresses
   ↓
🔍 Search Registry Tab
   ↓
📋 View Table of Addresses
   ↓
👁️ Click Row for Details
   ↓
🔗 Network Graph (visual connections)
   ↓
📈 Analytics (charts & trends)
   ↓
⚠️ Watchlist (monitoring)
   ↓
📥 Export (reports)
```

---

## 🎯 Next Steps

1. **Restart Backend** to load new diverse seeds
2. **Hard Refresh** browser (`Ctrl+Shift+R`)
3. **Navigate**: Scraping → Seed Manager
4. **Verify**: See 16 seeds with web type badges
5. **Test**: Click Play on different web types
6. **Navigate**: Addresses → Search Registry
7. **Explore**: Network Graph, Analytics, Watchlist

---

## 📞 Support

If you still have questions:
1. Check browser console (F12) for errors
2. Check backend logs for scraping status
3. Verify MongoDB connection (backend startup logs)
4. Review this guide's flow diagrams

**Goal**: Make it crystal clear where data flows and how to access it! 🚀
