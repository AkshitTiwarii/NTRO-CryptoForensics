# 🎯 Landing Page & Authentication System

## Overview

The NTRO CryptoForensics platform now features a **professional landing page** that showcases the system's capabilities before requiring authentication.

## Features

### 🏠 Landing Page

1. **Hero Section**
   - Eye-catching gradient background
   - NTRO branding with badge
   - Clear value proposition
   - Quick stats (24/7 scraping, 3 web layers, etc.)

2. **Problem Statement**
   - 4 critical issues explained:
     * Dark Web Crime
     * Money Laundering
     * Terrorism Financing
     * Data Fragmentation

3. **Solution Features**
   - Multi-layer web scraping (Surface/Dark/Deep)
   - Centralized intelligence database
   - Autonomous 24/7 operation
   - Network graph analysis
   - Watchlist monitoring
     * Advanced search capabilities

4. **Technology Stack**
   - Frontend: React 19, TailwindCSS, shadcn/ui
   - Backend: Python FastAPI, MongoDB, Redis + Celery
   - Scraping: BeautifulSoup4, Tor SOCKS5, I2P Proxy
   - Security: JWT Auth, bcrypt, HTTPS/TLS

5. **Admin Login Modal**
   - Secure authentication
   - Clean UI matching overall theme
   - Demo credentials displayed

### 🔐 Authentication Flow

```
User Visit → Landing Page → Click "Admin Login" → Login Modal → Dashboard
                                                         ↓
                                                   Invalid credentials → Error message
                                                         ↓
                                                   Valid credentials → Save token → Redirect
```

### 🎨 Design Theme

- **Colors**: Dark theme with gradient accents (blue, purple, pink)
- **Components**: Consistent with dashboard (same card/button styles)
- **Typography**: Bold headlines, clear hierarchy
- **Animations**: Subtle pulse effects, smooth transitions

## Usage

### For Users:

1. **Visit**: Open http://localhost:3000
2. **Explore**: Read about features and capabilities
3. **Login**: Click "Admin Login" button
4. **Credentials**: Use demo credentials (admin / admin123)
5. **Access**: Dashboard opens after successful authentication

### Demo Credentials:

```
Username: admin
Password: admin123
```

## File Structure

```
frontend/src/
├── components/
│   └── LandingPage.jsx     # New landing page component
├── App.js                   # Updated with landing page logic
└── ...
```

## Key Changes

### App.js Updates:

1. **Import LandingPage component**
   ```javascript
   import LandingPage from "./components/LandingPage";
   ```

2. **Add 'landing' to AUTH_VIEWS**
   ```javascript
   const AUTH_VIEWS = new Set(["login", "signup", "landing"]);
   ```

3. **Default view changed**
   ```javascript
   const [view, setView] = useState(token ? "dashboard" : "landing");
   ```

4. **Logout redirects to landing**
   ```javascript
   const logout = () => {
     // ... clear storage ...
     setView("landing");
   };
   ```

5. **Conditional rendering**
   ```javascript
   if (view === 'landing') {
     return <LandingPage onLogin={handleLoginSuccess} />;
   }
   ```

### LandingPage.jsx Features:

- **Responsive design**: Works on mobile/tablet/desktop
- **Smooth scrolling**: "Learn More" button scrolls to features
- **Modal login**: Overlay authentication without leaving page
- **API integration**: Calls backend `/api/auth/login` endpoint
- **Error handling**: Shows connection/credential errors
- **Loading states**: Spinner during authentication

## Backend Integration

The landing page uses the existing backend auth endpoint:

```
POST http://localhost:8000/api/auth/login
Body: { "username": "admin", "password": "admin123" }
Response: { "token": "jwt_token", "user": { ... } }
```

On successful login:
- Token stored in `localStorage` as `auth_token`
- User data stored as `user`
- Redirects to dashboard

## Customization

### Change Hero Text:

Edit `LandingPage.jsx`:
```javascript
<h1 className="text-6xl font-bold text-white mb-6">
  Your Custom Title
</h1>
```

### Modify Problem Statements:

Update the problem cards in the "Critical Issues" section.

### Add New Features:

Extend the features grid with new cards:
```javascript
<Card className="bg-gray-900 border-gray-700">
  <CardHeader>
    <YourIcon className="w-12 h-12 text-color-400 mb-4" />
    <CardTitle>Feature Name</CardTitle>
    <CardDescription>Description...</CardDescription>
  </CardHeader>
</Card>
```

### Change Color Scheme:

Modify gradient colors:
```javascript
// Current: blue → purple → pink
bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400

// Example: green → teal → blue
bg-gradient-to-r from-green-400 via-teal-400 to-blue-400
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Demo Credentials**: Change `admin/admin123` in production
2. **HTTPS Required**: Use SSL/TLS in production environment
3. **Token Storage**: Consider more secure storage than localStorage
4. **Rate Limiting**: Add login attempt limits to prevent brute force
5. **Authorization**: Landing page is public, but all data endpoints require auth

## Testing

### Manual Testing:

1. **Landing Page Load**
   ```
   ✓ Page loads without errors
   ✓ All sections render correctly
   ✓ Gradients and animations work
   ```

2. **Login Flow**
   ```
   ✓ Click "Admin Login" opens modal
   ✓ Enter credentials
   ✓ Submit form
   ✓ Token saved to localStorage
   ✓ Redirect to dashboard
   ```

3. **Error Handling**
   ```
   ✓ Invalid credentials show error
   ✓ Backend offline shows connection error
   ✓ Close modal (X button) works
   ```

4. **Logout Flow**
   ```
   ✓ Click logout in dashboard
   ✓ Token cleared
   ✓ Redirect to landing page
   ```

## Benefits

✅ **Professional First Impression**: Clean, modern landing page
✅ **Information Before Commitment**: Users learn about features first
✅ **Clear Value Proposition**: Solves specific problems for NTRO
✅ **Seamless Authentication**: Integrated login without page reload
✅ **Consistent Branding**: Matches dashboard theme
✅ **Mobile-Friendly**: Responsive design for all devices

## Next Steps

1. ✅ Landing page created
2. ✅ Authentication integrated
3. ⏳ Optional: Add more sections (team, testimonials, contact)
4. ⏳ Optional: Add registration flow (if needed)
5. ⏳ Optional: Add password reset functionality
6. ⏳ Production: Change demo credentials, enable HTTPS

---

**Ready to use!** Just start the frontend and visit http://localhost:3000 to see the new landing page! 🚀
