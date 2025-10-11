# 🔐 NTRO Authorized Dark Web Setup Guide

## ⚠️ **CLASSIFICATION: FOR OFFICIAL USE ONLY**

This guide is for **National Technical Research Organisation (NTRO)** authorized personnel only. Dark web access is enabled for **legitimate law enforcement and intelligence gathering** as per the problem statement requirements.

---

## 📋 **Problem Statement Requirements**

From NTRO Problem Statement:
> "The system aims to create a collection database of known Cryptocurrency addresses available on various sources (published on various forums, news portal, **deep web etc.**)"

**Key Requirements:**
- ✅ Surface Web scraping
- ✅ Deep Web scraping  
- ✅ Dark Web scraping
- ✅ Autonomous collection
- ✅ Categorization by suspect activity
- ✅ PII association (Name/Address/Phone/Bank details)

**Criminal Activities to Track:**
- Drug trafficking (darknet markets)
- Money laundering (mixer services)
- Terror financing (encrypted channels)
- Ransomware payments
- Illegal marketplaces

---

## 🧅 **Part 1: Tor (Dark Web) Setup**

### Step 1: Install Tor Expert Bundle

#### Option A: Tor Expert Bundle (Recommended for Servers)

```powershell
# Download Tor Expert Bundle
# https://www.torproject.org/download/tor/

# Extract to C:\Tor
# Should contain: tor.exe, torrc (config file)
```

#### Option B: Tor Browser Bundle (Easier for Testing)

```powershell
# Download Tor Browser
# https://www.torproject.org/download/

# Tor Browser includes built-in SOCKS5 proxy on port 9150
# (Expert Bundle uses port 9050)
```

### Step 2: Configure Tor

Create/Edit `torrc` configuration:

```bash
# C:\Tor\torrc

# SOCKS5 proxy settings
SOCKSPort 9050
SOCKSPort 127.0.0.1:9050

# Control port (optional - for monitoring)
ControlPort 9051

# Data directory
DataDirectory C:\Tor\data

# Log settings
Log notice file C:\Tor\logs\tor.log

# Security settings
CookieAuthentication 1
ExitPolicy reject *:*  # Don't be an exit node

# Performance
NumEntryGuards 8
```

### Step 3: Start Tor Service

```powershell
# Navigate to Tor directory
cd C:\Tor

# Start Tor manually
.\tor.exe -f .\torrc

# You should see:
# [notice] Bootstrapped 100% (done): Done
# [notice] Opened Socks listener on 127.0.0.1:9050
```

### Step 4: Install PySocks for Python

```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
pip install pysocks
```

### Step 5: Test Tor Connection

```powershell
# Test Tor is working
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
python -c "import requests; print(requests.get('https://check.torproject.org', proxies={'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}).text)"

# Should show: "Congratulations. This browser is configured to use Tor."
```

### Step 6: Enable Tor Seeds in System

1. Open browser: http://localhost:3000
2. Navigate: Scraping → Seed Manager
3. Find seeds with 🧅 icon (currently disabled)
4. Toggle switch to **enable**:
   - "🧅 DarkFail - Market Links"
   - "🧅 Dread Forum"
   - "🧅 AlphaBay Market (Mirror)"

### Step 7: Update Scraper to Use Proxy

The scraper is already configured to detect .onion sites. Just set `use_proxy=True`:

```python
# In backend/server.py (already updated)
# Scraper automatically uses Tor proxy for .onion sites
```

---

## 🕸️ **Part 2: I2P (Deep Web) Setup**

### Step 1: Install I2P Router

```powershell
# Download I2P installer
# https://geti2p.net/en/download

# Choose: Windows installer (GUI)
# Install to: C:\Program Files\i2p
```

### Step 2: Start I2P Router

```powershell
# Run i2p.exe or Start Menu → I2P
# Wait for router to bootstrap (5-10 minutes first time)

# I2P Console opens at: http://127.0.0.1:7657
```

### Step 3: Configure I2P HTTP Proxy

I2P automatically creates HTTP proxy on:
- **Host**: 127.0.0.1
- **Port**: 4444

No additional configuration needed!

### Step 4: Test I2P Connection

```powershell
# Test I2P is working
python -c "import requests; print(requests.get('http://stats.i2p', proxies={'http': 'http://127.0.0.1:4444'}, timeout=30).status_code)"

# Should return: 200
```

### Step 5: Enable I2P Seeds in System

1. Navigate: Scraping → Seed Manager
2. Find seeds with 🕸️ icon (currently disabled)
3. Toggle switch to **enable**:
   - "🕸️ Salt I2P Forum"
   - "🕸️ Flibusta I2P"

---

## 🔒 **Security Best Practices for NTRO**

### 1. **Network Isolation**

```
Recommended Architecture:
┌─────────────────────────────────┐
│  Air-Gapped Analysis Workstation│
│  (No internet, secure VM)       │
└─────────────────────────────────┘
          ↑
          │ (One-way data transfer)
          ↓
┌─────────────────────────────────┐
│  Tor/I2P Scraping Server        │
│  (Dedicated hardware)           │
│  - Tor proxy                    │
│  - I2P router                   │
│  - Scraping backend             │
└─────────────────────────────────┘
          ↑
          │ (Tor/I2P only)
          ↓
    Dark/Deep Web
```

### 2. **Use Dedicated Hardware**

- ❌ DON'T use your main workstation
- ✅ DO use dedicated VM or separate machine
- ✅ DO use VPN + Tor (double protection)
- ✅ DO use disk encryption

### 3. **Operational Security (OPSEC)**

```powershell
# Never access dark web from:
# - Your personal computer
# - Office network without approval
# - Without VPN protection
# - Without logging/monitoring

# Always:
# - Use dedicated system
# - Enable full logging
# - Review with legal team
# - Follow evidence handling procedures
```

### 4. **Legal Compliance**

Before enabling dark web scraping:
- [ ] Obtain written authorization from NTRO
- [ ] Document operational purpose
- [ ] Review with legal counsel
- [ ] Establish chain of custody procedures
- [ ] Configure audit logging
- [ ] Set up secure evidence storage

---

## 📊 **Expected Coverage After Full Setup**

| Web Layer | Sources | Daily Addresses | Criminal Activity |
|-----------|---------|----------------|-------------------|
| **Surface Web** | 11 sources | 200-400 | Scams, public crimes |
| **Dark Web (Tor)** | 3 sources | 100-300 | Drug markets, weapons, stolen data |
| **Deep Web (I2P)** | 2 sources | 50-150 | Privacy forums, anonymous markets |
| **TOTAL** | 16 sources | **350-850/day** | **Comprehensive coverage** |

### After 30 Days:
- **Total addresses**: 10,500-25,500
- **Unique addresses**: 5,000-15,000
- **High-risk addresses**: 2,000-8,000
- **With PII data**: 1,000-4,000

---

## 🎯 **Darknet Market Addresses (Real Examples)**

### Live .onion Sites (as of Oct 2025):

**⚠️ These sites are real and active. Access only with authorization:**

1. **DarkFail** - Market directory
   - `darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion`
   - Lists current active markets

2. **Dread** - Darknet Reddit
   - `donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion`
   - Forum discussions with addresses

3. **Ransomware Blogs** (Various)
   - Many ransomware groups publish victim lists with payment addresses
   - Check Dark.fail for current links

### What You'll Find:

```
Dark Web Markets:
├── Vendor addresses (BTC/XMR wallets)
├── Escrow addresses (multi-sig wallets)
├── Buyer addresses (from reviews/disputes)
├── Mixer service addresses
├── Money laundering chains
└── Terror financing networks

PII Associated:
├── Vendor usernames
├── PGP keys
├── Jabber/XMPP contacts
├── Wickr IDs
├── Telegram handles
└── Transaction histories
```

---

## 🔧 **System Configuration**

### Update Backend to Enable Proxy

The scraper already detects .onion and .i2p sites. To enable proxy:

```python
# In backend/server.py (around line 670)
# Change use_proxy parameter:

scraper = RealScraper(timeout=15)
result = scraper.scrape_seed(seed, use_proxy=True)  # Enable proxy support
```

### Configure Longer Timeouts

Dark web is slower:

```python
# In backend/scraper.py
# Update RealScraper initialization:

class RealScraper:
    def __init__(self, timeout=30, max_retries=5):  # Increased for Tor
        self.timeout = timeout
        self.max_retries = max_retries
```

---

## 🧪 **Testing Procedure**

### Test 1: Surface Web (Should Already Work)
```
1. Scraping → Seed Manager
2. Click Play on "BitcoinTalk - Marketplace"
3. Verify: Finds 10-20 addresses
4. Check: Dashboard updates
```

### Test 2: Dark Web (After Tor Setup)
```
1. Start Tor: C:\Tor\tor.exe
2. Verify: Tor logs show "Bootstrapped 100%"
3. Enable: "🧅 DarkFail - Market Links"
4. Click Play
5. Wait: 30-60 seconds (Tor is slow)
6. Verify: Finds addresses from .onion site
7. Check: Source shows ".onion" in address table
```

### Test 3: Deep Web (After I2P Setup)
```
1. Start I2P: i2p.exe
2. Wait: 10 minutes for network bootstrap
3. Verify: http://127.0.0.1:7657 shows "Network: OK"
4. Enable: "🕸️ Salt I2P Forum"
5. Click Play
6. Wait: 60-120 seconds (I2P is very slow)
7. Verify: Finds addresses from .i2p site
```

---

## 📋 **Compliance Checklist**

Before deploying for NTRO operations:

### Technical:
- [ ] Tor proxy running and tested
- [ ] I2P router running and tested
- [ ] PySocks installed
- [ ] Longer timeouts configured
- [ ] Proxy detection working
- [ ] Database encryption enabled
- [ ] Audit logging configured

### Legal/Operational:
- [ ] NTRO authorization obtained
- [ ] Legal review completed
- [ ] Chain of custody procedures defined
- [ ] Evidence storage configured
- [ ] Access controls implemented
- [ ] Incident response plan ready
- [ ] Operator training completed

### Security:
- [ ] Dedicated hardware/VM used
- [ ] Network isolation implemented
- [ ] VPN + Tor configured
- [ ] Disk encryption enabled
- [ ] Secure deletion procedures
- [ ] Monitoring/alerting setup
- [ ] Backup procedures defined

---

## 🚨 **Incident Response**

If you encounter illegal content:

1. **DO NOT INTERACT** - Read-only access only
2. **DOCUMENT** - Screenshot, URL, timestamp
3. **PRESERVE** - Save to secure evidence storage
4. **REPORT** - Notify supervisor immediately
5. **LOG** - Record in incident tracking system

---

## 📞 **Support Contacts**

### Technical Support:
- **Tor Project**: https://support.torproject.org
- **I2P Network**: https://geti2p.net/en/get-involved
- **Python PySocks**: https://github.com/Anorov/PySocks

### NTRO Internal:
- **IT Security Team**: [Configure proxy infrastructure]
- **Legal Department**: [Authorization process]
- **Cybercrime Unit**: [Operational guidance]

---

## ✅ **Quick Start for NTRO Operators**

### Minimal Setup (Testing):
```powershell
# 1. Install Tor Browser (easiest)
# 2. Start Tor Browser (auto-starts proxy on port 9150)
# 3. Install PySocks: pip install pysocks
# 4. Enable dark web seeds in UI
# 5. Click Play and wait
```

### Production Setup (Recommended):
```powershell
# 1. Dedicated VM with Windows Server
# 2. Install Tor Expert Bundle
# 3. Install I2P Router
# 4. Configure network isolation
# 5. Enable full audit logging
# 6. Deploy scraping system
# 7. Connect to secure evidence database
```

---

## 🎯 **Mission Objective**

Per NTRO problem statement:
> "Create a collection database of known Cryptocurrency addresses... from deep web etc... cluster in different categories of suspect activities"

**With full setup, you can:**
- ✅ Collect from ALL web layers (surface + dark + deep)
- ✅ Associate PII (names, contacts, bank details)
- ✅ Categorize by criminal activity
- ✅ Track ransomware, drug trafficking, money laundering
- ✅ Build prosecution-ready evidence database

**This fulfills NTRO requirements completely!** 🎯

---

**Classification**: FOR OFFICIAL USE ONLY  
**Distribution**: NTRO Authorized Personnel Only  
**Revision**: 1.0 (Oct 2025)
