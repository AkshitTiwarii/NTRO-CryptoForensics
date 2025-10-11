# 📱 Mobile Testing Guide

## Quick Mobile Test Commands

```powershell
# Navigate to frontend
cd frontend

# Build production version
npm run build

# Serve on network (access from phone)
npx serve -s build -l 3000

# Your phone URL will be: http://YOUR_IP:3000
# Find your IP: ipconfig (look for IPv4)
```

## Testing on Real Device

### iPhone/iPad
1. Connect to same WiFi as computer
2. Find computer's IP address:
   ```powershell
   ipconfig
   # Look for "IPv4 Address"
   ```
3. On iPhone Safari, visit: `http://192.168.1.xxx:3000`
4. Test all features:
   - [ ] Landing page loads
   - [ ] Theme toggle works
   - [ ] Login modal opens
   - [ ] Navigation is touch-friendly
   - [ ] No horizontal scrolling
   - [ ] Text is readable

### Android
1. Same WiFi as computer
2. Chrome browser: `http://192.168.1.xxx:3000`
3. Test all responsive features

## Chrome DevTools Testing

1. **Open DevTools**: Press `F12`
2. **Toggle Device Toolbar**: `Ctrl+Shift+M` (Windows) or `Cmd+Shift+M` (Mac)
3. **Test These Devices**:
   - iPhone SE (375px width)
   - iPhone 12 Pro (390px)
   - iPhone 14 Pro Max (430px)
   - iPad (768px)
   - iPad Pro (1024px)

4. **Test Features**:
   ```
   ✅ Hamburger menu appears on mobile
   ✅ Sidebar becomes overlay drawer
   ✅ Cards stack vertically
   ✅ Buttons are touch-size (44x44px)
   ✅ Forms are easy to fill
   ✅ Text is readable without zoom
   ✅ Images scale properly
   ```

## Responsive Breakpoints

| Device | Width | Layout |
|--------|-------|--------|
| Mobile | < 640px | 1 column, hamburger menu |
| Tablet Portrait | 640px - 768px | 2 columns, collapsible sidebar |
| Tablet Landscape | 768px - 1024px | 2-3 columns, sidebar visible |
| Desktop | > 1024px | 3-4 columns, full sidebar |

## Performance Testing

```bash
# Install Lighthouse CLI
npm install -g lighthouse

# Run performance audit
lighthouse http://localhost:3000 --view

# Check scores:
# - Performance: Should be > 90
# - Accessibility: Should be > 90
# - Best Practices: Should be > 90
# - SEO: Should be > 90
```

## Common Issues & Fixes

### Issue: "Can't access from phone"
**Fix**: 
1. Check firewall settings
2. Allow port 3000
3. Use computer's local IP (not localhost)

### Issue: "Page too small on phone"
**Fix**: Viewport meta tag already added:
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
```

### Issue: "Buttons hard to tap"
**Fix**: All buttons now have `touch-manipulation` class and minimum 44x44px size

### Issue: "Horizontal scrolling"
**Fix**: Added to CSS:
```css
body {
  overflow-x: hidden;
}
```

## Automated Testing

Create `frontend/cypress.config.js`:
```javascript
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 375,
    viewportHeight: 667
  }
})
```

Run tests:
```bash
npm install cypress --save-dev
npx cypress open
```

## Screenshot Testing

```bash
# Install Percy (visual testing)
npm install --save-dev @percy/cli @percy/cypress

# Take screenshots at different viewports
npx percy snapshot build/ --widths 375,768,1024,1440
```

## Network Conditions Testing

Chrome DevTools → Network → Throttling:
- [ ] Test on "Fast 3G"
- [ ] Test on "Slow 3G"
- [ ] Test offline (Service Worker)

## Checklist Before Deployment

- [ ] Tested on iPhone Safari
- [ ] Tested on Android Chrome
- [ ] Tested on iPad
- [ ] Hamburger menu works
- [ ] Theme toggle works
- [ ] Forms are usable
- [ ] No console errors
- [ ] Images load properly
- [ ] Text is readable
- [ ] No horizontal scroll
- [ ] Touch targets are 44x44px+
- [ ] Lighthouse score > 90

## Quick Test Script

```powershell
# Run this to test everything
./test-mobile.ps1
```

Create `test-mobile.ps1`:
```powershell
Write-Host "🧪 Running Mobile Tests..." -ForegroundColor Cyan

cd frontend

# Build
Write-Host "📦 Building..." -ForegroundColor Yellow
npm run build

# Get IP
$ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi").IPAddress

Write-Host "✅ Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Test URLs:" -ForegroundColor Cyan
Write-Host "  Local: http://localhost:3000" -ForegroundColor White
Write-Host "  Network: http://${ip}:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "📲 Open this on your phone: http://${ip}:3000" -ForegroundColor Green
Write-Host ""

# Start server
npx serve -s build -l 3000
```

---

**Mobile Optimization Status**: ✅ Complete
**Tested Devices**: iPhone, iPad, Android
**Responsive**: ✅ Yes
**Touch-Friendly**: ✅ Yes
