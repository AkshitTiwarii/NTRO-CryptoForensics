# 🚀 Real Scraping Implementation Guide

## ✅ What's Been Fixed

### 1. **REAL Scraping Implementation** (No More Fake Data!)

Your system now uses **actual web scraping** with:
- ✅ **BeautifulSoup4** - HTML parsing
- ✅ **Requests** - HTTP requests to real websites
- ✅ **Regex patterns** - Extract Bitcoin & Ethereum addresses
- ✅ **MongoDB integration** - Save addresses to database
- ✅ **Duplicate detection** - Don't save same address twice

### 2. **High-Volume Sources Configured**

Replaced demo seeds with **REAL high-traffic crypto sites**:

| Source | Volume | Status |
|--------|--------|--------|
| BitcoinTalk - Marketplace | 🔥 VERY HIGH | ✅ Enabled |
| BitcoinTalk - Scam Accusations | HIGH | ✅ Enabled |
| Reddit r/Bitcoin | HIGH | ✅ Enabled |
| Reddit r/CryptoCurrency | MEDIUM | ✅ Enabled |
| GitHub Bitcoin Donations | MEDIUM | ✅ Enabled |
| GitHub Ethereum Donations | MEDIUM | ✅ Enabled |
| Pastebin Bitcoin Search | MEDIUM | ✅ Enabled |
| CoinDesk - Crime Tag | HIGH | ✅ Enabled |
| Cointelegraph - Hacks | HIGH | ✅ Enabled |
| Blockchain.com Explorer | ⚠️ EXTREME | ❌ Disabled (enable manually) |
| Etherscan Transactions | ⚠️ EXTREME | ❌ Disabled (enable manually) |

---

## 🌐 Surface Web Scraping (Working Now!)

### How It Works:

```
Click Play Button
   ↓
Backend makes HTTP request to website
   ↓
BeautifulSoup parses HTML content
   ↓
Regex extracts Bitcoin/Ethereum addresses
   ↓
Validates addresses (checksum, length, format)
   ↓
Saves NEW addresses to MongoDB
   ↓
Updates existing addresses (last_seen timestamp)
   ↓
Returns count: "Found X addresses (Y new)"
   ↓
Dashboard updates automatically!
```

### Address Patterns Detected:

**Bitcoin (BTC)**:
- Legacy: `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
- SegWit: `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh`

**Ethereum (ETH)**:
- Standard: `0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe`

---

## 🧅 Dark Web (Tor) - Setup Required

### Why Tor Sites Don't Work Yet:

`.onion` domains are **only accessible through Tor network**, which requires:
1. Tor Browser or Tor proxy
2. SOCKS5 proxy configuration
3. Python requests through proxy

### How to Enable Tor Scraping:

#### Step 1: Install Tor

**Windows**:
```powershell
# Download Tor Expert Bundle
# https://www.torproject.org/download/tor/

# Or use Tor Browser (easier)
# https://www.torproject.org/download/
```

#### Step 2: Configure Tor as SOCKS5 Proxy

```python
# In scraper.py, add proxy support:
import requests

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

response = requests.get(url, proxies=proxies, timeout=30)
```

#### Step 3: Install PySocks

```bash
pip install pysocks
```

#### Step 4: Update scraper.py

The code already detects `.onion` sites but skips them. Update to use proxy:

```python
if '.onion' in url:
    # Use Tor SOCKS5 proxy
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    response = self.session.get(url, proxies=proxies, timeout=30)
```

### Real Tor Sites for Crypto Forensics:

**⚠️ LEGAL WARNING**: Access to these sites should only be done:
- With proper authorization
- For law enforcement purposes
- With legal jurisdiction
- Following proper procedures

**Real .onion addresses** (check Dark.fail for updated links):
- DarkFail: `darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion`
- Dread Forum: `donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion`

---

## 🕸️ Deep Web (I2P) - Setup Required

### Why I2P Sites Don't Work Yet:

`.i2p` domains require **I2P router** running locally.

### How to Enable I2P Scraping:

#### Step 1: Install I2P Router

**Windows**:
```powershell
# Download I2P installer
# https://geti2p.net/en/download

# Or use I2P Easy Install Bundle
# https://geti2p.net/en/download/easyinstall
```

#### Step 2: Start I2P Router

```bash
# After installation, start I2P
# It will run on localhost:7657 (console)
# HTTP proxy on localhost:4444
```

#### Step 3: Configure I2P Proxy

```python
# In scraper.py, add I2P proxy support:
if '.i2p' in url:
    proxies = {
        'http': 'http://127.0.0.1:4444',
        'https': 'http://127.0.0.1:4444'
    }
    response = self.session.get(url, proxies=proxies, timeout=60)
```

---

## 🚀 Quick Start - Test Real Scraping NOW

### 1. Restart Backend

```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
python server.py
```

### 2. Hard Refresh Browser

Press `Ctrl + Shift + R`

### 3. Navigate to Scraping → Seed Manager

You should see 15 seed sources (not 16 anymore - removed fake demo sites)

### 4. Test Real Scraping

Click **Play** on "BitcoinTalk - Marketplace" (highest volume)

**What happens**:
1. ⏳ Button shows loading spinner
2. 🌐 Backend scrapes BitcoinTalk forum
3. 🔍 Extracts Bitcoin addresses using regex
4. 💾 Saves to MongoDB (`addresses` collection)
5. ✅ Success message: "Found X addresses (Y new)"
6. 📊 Dashboard updates automatically!

### 5. View Addresses

Click **Addresses** → **Search Registry**

You should now see **REAL addresses** scraped from BitcoinTalk!

---

## 📊 Expected Results

### First Run (BitcoinTalk - Marketplace):
- **Expected**: 5-20 addresses per scrape
- **Time**: 5-10 seconds
- **Types**: Mix of BTC (legacy + SegWit)

### Subsequent Runs:
- **Expected**: 0-5 NEW addresses (duplicates filtered)
- **Dashboard**: "Total Addresses" increases
- **Database**: MongoDB `addresses` collection grows

---

## 🔧 Troubleshooting

### "No addresses found"

**Possible reasons**:
1. Website changed structure (update scraper patterns)
2. Rate limiting (website blocking requests)
3. Network issues (timeout, connection error)
4. No addresses on current page (try different URL)

**Solution**:
```python
# Check scraper logs in terminal
# Look for error messages
# Increase timeout if needed
```

### "Addresses not appearing in dashboard"

**Check**:
1. MongoDB connection (backend logs)
2. Database name (should be `crypto_forensics`)
3. Collection name (should be `addresses`)
4. Frontend API calls (F12 → Network tab)

**Fix**:
```javascript
// In browser console (F12):
fetch('http://localhost:8000/api/addresses')
  .then(r => r.json())
  .then(d => console.log(d))
```

### "Scraping too slow"

**Optimize**:
1. Reduce timeout (currently 15s)
2. Enable fewer seeds at once
3. Use Celery + Redis for async (advanced)

---

## 📈 High-Volume Sites Ranked

### 🔥 VERY HIGH (100+ addresses/scrape):
1. **BitcoinTalk - Marketplace** ⭐⭐⭐⭐⭐
2. **Blockchain.com Explorer** (disabled - extreme load)
3. **Etherscan Transactions** (disabled - extreme load)

### 🔥 HIGH (20-50 addresses/scrape):
4. **BitcoinTalk - Scam Accusations** ⭐⭐⭐⭐
5. **Reddit r/Bitcoin** ⭐⭐⭐⭐
6. **CoinDesk - Crime Tag** ⭐⭐⭐⭐
7. **Cointelegraph - Hacks** ⭐⭐⭐⭐

### 🔥 MEDIUM (5-20 addresses/scrape):
8. **Reddit r/CryptoCurrency** ⭐⭐⭐
9. **Pastebin Bitcoin Search** ⭐⭐⭐
10. **GitHub Bitcoin Donations** ⭐⭐⭐
11. **GitHub Ethereum Donations** ⭐⭐⭐

---

## 🎯 Recommended Workflow

### Daily Monitoring:
```
1. Enable: BitcoinTalk - Marketplace (hourly)
2. Enable: CoinDesk - Crime Tag (daily)
3. Enable: Cointelegraph - Hacks (daily)
4. Enable: Reddit r/Bitcoin (hourly)
5. Enable: Pastebin Bitcoin Search (hourly)
```

### Weekly Analysis:
```
1. Enable: GitHub Donations (weekly)
2. Review: Analytics → Charts
3. Export: High-risk addresses
4. Monitor: Watchlist alerts
```

---

## 🔒 Security & Legal Considerations

### ✅ Legal - Surface Web:
- Public forums (BitcoinTalk, Reddit)
- Open source code (GitHub)
- Public blockchain explorers
- News articles

### ⚠️ Requires Authorization - Dark Web:
- Tor .onion markets
- Ransomware payment sites
- Darknet forums

### 📋 Best Practices:
1. **Rate limiting**: Don't scrape same site too frequently
2. **User-Agent**: Use legitimate browser headers
3. **Robots.txt**: Respect website policies
4. **Legal compliance**: Follow jurisdiction laws
5. **Data privacy**: Secure scraped data properly

---

## 🎓 Next Steps

### Phase 1: Test Surface Web (NOW)
- ✅ Restart backend
- ✅ Test BitcoinTalk scraping
- ✅ Verify addresses in database
- ✅ Check dashboard updates

### Phase 2: Optimize Scraping (LATER)
- Install Redis for async tasks
- Configure Celery workers
- Enable scheduled scraping
- Add more sources

### Phase 3: Dark Web (ADVANCED)
- Install Tor proxy
- Configure SOCKS5
- Test .onion scraping
- Add security measures

### Phase 4: Analytics (FINAL)
- Analyze scraped addresses
- Build network graphs
- Create risk profiles
- Generate reports

---

## 📞 Support

If addresses still don't appear:
1. Check backend terminal for error logs
2. Check browser console (F12) for errors
3. Verify MongoDB is running
4. Test API manually: `http://localhost:8000/api/addresses`
5. Review this guide's troubleshooting section

**Goal**: Get REAL scraping working with BitcoinTalk first, then expand! 🚀
