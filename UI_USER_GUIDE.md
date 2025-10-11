# 🎨 NTRO CryptoForensics - New UI Guide

## Theme System

### ✨ Features
- **Pure Black/White Design** - No more bluish colors!
- **One-Click Theme Toggle** - Switch between dark and light modes instantly
- **Auto-Save Preference** - Your choice is remembered
- **System Integration** - Respects your OS dark mode setting

### 🔄 How to Switch Themes

#### On Login Page:
- Look for the floating button in the **top-right corner**
- Click the **Moon icon** 🌙 to switch to dark mode
- Click the **Sun icon** ☀️ to switch to light mode

#### After Login:
- Find the theme toggle in the **header** (top-right)
- Shows "Light Mode" button in dark mode
- Shows "Dark Mode" button in light mode

### 🎨 Color Schemes

#### ⚪ Light Mode
```
Background: Pure White (#FFFFFF)
Text: Pure Black (#000000)
Cards: White with subtle borders
Sidebar: White background
Active Items: Black background, white text
```

#### ⚫ Dark Mode  
```
Background: Pure Black (#000000)
Text: Pure White (#FFFFFF)
Cards: Near-black with light borders
Sidebar: Black background
Active Items: White background, black text
```

### 🔐 Login Credentials
```
Username: admin
Password: admin123
```

### 📱 UI Components

#### Navigation Sidebar
- **Collapsed**: Click ✕ icon (only icons visible)
- **Expanded**: Click ☰ icon (full labels + descriptions)
- **Active Page**: Highlighted in primary color (black/white inverted)

#### Dashboard Cards
- **Total Seeds**: Shows configured sources
- **Active Seeds**: Currently enabled crawlers
- **Addresses Found**: Total wallet addresses
- **Success Rate**: Scraping success percentage

#### Seed Manager
- **Add Seed**: ➕ button (top right)
- **Enable/Disable**: Toggle switch per seed
- **Manual Trigger**: ▶ Play button
- **Delete**: 🗑️ Trash icon
- **Auto-refresh**: Every 10 seconds

### 🎯 Navigation Menu
1. **Dashboard** - Overview & KPIs
2. **Address Registry** - Search wallets
3. **Register Address** - Manual entry
4. **OSINT Scraper** - Web harvesting
5. **Seed Manager** - Autonomous sources ⭐
6. **Network Graph** - Entity clustering
7. **Analytics** - Category trends
8. **Alerts & Watchlists** - Notifications
9. **Data Export** - CSV/JSON reports

### ⚡ Quick Actions

#### From Dashboard:
- View all addresses
- Start manual scrape
- Check recent jobs
- Review analytics

#### From Seed Manager:
- Add new source
- Enable/disable seeds
- Trigger manual crawl
- View statistics

### 🔔 Status Indicators

#### Seed Status:
- **Green Globe** 🌐 - Active and enabled
- **Gray Globe** - Disabled
- **Progress Badge** - Crawling in progress

#### Success Rate:
- **100%** - All jobs successful
- **<100%** - Some failures detected

#### Last Crawled:
- **"Never"** - New seed, not yet run
- **Time ago** - Last execution time

### 🎨 Category Badges
- **Ransomware**: Red (High risk: 90)
- **Darknet Market**: Orange (High risk: 80)
- **Mixer**: Purple (Medium-High: 70)
- **Scam**: Amber (Medium-High: 75)
- **Gambling**: Pink (Medium: 50)
- **Exchange**: Blue (Low: 20)
- **Mining**: Green (Very low: 10)
- **Legitimate**: Dark green (Very low: 5)
- **Unknown**: Gray (Unclassified)

### 📊 Dashboard Statistics

#### Key Metrics:
- **Total Addresses**: All wallets in database
- **High Risk**: Risk score ≥ 70
- **Watched**: Addresses with alerts enabled
- **BTC/ETH/Other**: Breakdown by blockchain

#### Charts:
- Category distribution (pie chart)
- Blockchain distribution (bar chart)
- Risk score trends (line chart)

### 🛠️ Advanced Features

#### Network Graph:
- Visualize transaction flows
- Identify clusters
- Entity relationships

#### Alerts & Watchlists:
- Real-time notifications
- Custom alert conditions
- Email/webhook integration

#### Data Export:
- CSV format for Excel
- JSON format for APIs
- Filtered exports
- Bulk downloads

### 🔒 Security Features
- JWT token authentication
- Session persistence
- Auto-logout on token expiry
- Secure API communication

### 💡 Tips & Tricks

1. **Fast Navigation**: Use keyboard shortcuts (coming soon)
2. **Bulk Actions**: Select multiple addresses for batch operations
3. **Filter Results**: Use search and category filters
4. **Sort Columns**: Click column headers to sort
5. **Expand Details**: Click address cards for full info

### 🐛 Troubleshooting

#### Theme not changing?
- Refresh the page (F5)
- Clear browser cache
- Check browser console for errors

#### Login issues?
- Use: admin / admin123
- Check backend is running (port 8000)
- Verify network connectivity

#### Seed Manager not loading?
- Check backend API connectivity
- Verify token is valid
- Check browser console

### 📞 Support
- Backend URL: http://localhost:8000
- Frontend URL: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

**Made with ❤️ for NTRO - National Technical Research Organisation**
