# 🔧 Fix Vercel 404 Error - Deployment Configuration

## ❌ Problem

You're seeing a **404 NOT_FOUND** error because Vercel deployed from the wrong directory. Your frontend code is in `CryptoData/frontend`, but Vercel looked in the root directory.

---

## ✅ Solution: Configure Root Directory

### **Option 1: Via Vercel Dashboard (Easiest)**

1. **Go to your Vercel project:**
   - Visit: https://vercel.com/akshittiwarii/projects
   - Click on your deployed project

2. **Go to Settings:**
   - Click **"Settings"** tab at the top
   - Scroll to **"Build & Development Settings"**

3. **Set Root Directory:**
   - Find **"Root Directory"** setting
   - Click **"Edit"**
   - Enter: `frontend` (or `CryptoData/frontend` if that doesn't work)
   - Click **"Save"**

4. **Redeploy:**
   - Go to **"Deployments"** tab
   - Click **"..."** on the latest deployment
   - Click **"Redeploy"**
   - Check **"Use existing Build Cache"** = OFF
   - Click **"Redeploy"**

---

### **Option 2: Delete & Redeploy with Correct Settings**

If Option 1 doesn't work, delete and recreate:

1. **Delete the current deployment:**
   - Go to Settings → General
   - Scroll to bottom → "Delete Project"
   - Type project name to confirm

2. **Create new deployment with correct settings:**
   - Go to: https://vercel.com/new
   - Import your GitHub repo: `AkshitTiwarii/NTRO-CryptoForensics`
   - **IMPORTANT:** Set these correctly:
     - **Root Directory:** `frontend` ← CRITICAL!
     - **Framework Preset:** Create React App
     - **Build Command:** `npm run build` or leave default
     - **Output Directory:** `build` or leave default
     - **Install Command:** `npm install --legacy-peer-deps`

3. **Add environment variable (optional for now):**
   - Click "Environment Variables"
   - Name: `REACT_APP_BACKEND_URL`
   - Value: `http://localhost:8000` (for testing) or your Railway backend URL later
   - Click "Add"

4. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)

---

### **Option 3: Using Vercel CLI**

```powershell
# Navigate to frontend directory
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\frontend

# Install Vercel CLI (if not installed)
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (this will use the correct directory)
vercel --prod
```

---

## 🔍 Verify Settings

Before redeploying, make sure your Vercel project has these settings:

### **Build & Development Settings:**
```
Framework Preset:    Create React App
Build Command:       npm run build
Output Directory:    build
Install Command:     npm install --legacy-peer-deps
Root Directory:      frontend  ← MUST BE SET!
```

### **Environment Variables (Optional):**
```
REACT_APP_BACKEND_URL = http://localhost:8000
```

---

## 📊 Why This Happened

Your repository structure is:
```
NTRO-CryptoForensics/
├── frontend/          ← React app is HERE
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vercel.json
├── backend/           ← Python backend
├── README.md
└── ...other files
```

**Problem:** Vercel deployed from the root (`NTRO-CryptoForensics/`) which has no `package.json`, `src/`, or `build/` directory.

**Solution:** Tell Vercel to use the `frontend/` subdirectory as the root.

---

## ✅ Expected Result After Fix

After redeploying with correct settings, you should see:

1. **Build Log:**
   ```
   ✓ Installing dependencies
   ✓ Building project
   ✓ Detected Create React App
   ✓ Build completed
   ```

2. **Deployment URL:**
   - Opens to your landing page (NTRO branding)
   - No 404 error
   - Can see "Admin Login" button
   - Theme toggle works

3. **Files served:**
   - `index.html` loads correctly
   - JavaScript bundles load
   - CSS loads
   - Images/assets load

---

## 🚨 Quick Fix Checklist

- [ ] Go to Vercel project settings
- [ ] Set Root Directory to `frontend`
- [ ] Set Install Command to `npm install --legacy-peer-deps`
- [ ] Framework should auto-detect as "Create React App"
- [ ] Redeploy with cleared cache
- [ ] Verify deployment URL loads landing page
- [ ] Check browser console for any errors (F12)

---

## 📞 Still Getting 404?

If you still see 404 after setting Root Directory:

### **Check 1: Verify Root Directory**
```
Settings → Build & Development Settings → Root Directory
Should show: frontend
```

### **Check 2: Check Build Logs**
- Go to Deployments tab
- Click on latest deployment
- Check "Building" logs for errors
- Look for "npm install" and "npm run build" success

### **Check 3: Verify Build Output**
Build logs should show:
```
Creating an optimized production build...
Compiled successfully.
File sizes after gzip:
  50 KB  build/static/js/main.xxxxx.js
  2 KB   build/static/css/main.xxxxx.css
```

### **Check 4: Test Locally First**
```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\frontend
npm run build
npx serve -s build
```
Open http://localhost:3000 - if this works, Vercel should work too.

---

## 🎯 Alternative: Create Separate Frontend Repo

If you keep having issues, you can create a separate repo just for the frontend:

1. **Create new repo:** `NTRO-CryptoForensics-Frontend`
2. **Copy only frontend folder**
3. **Deploy that repo** (no need to set Root Directory)

But try the Root Directory fix first - it's easier!

---

## 📝 Summary

**The Fix:** Set **Root Directory** to `frontend` in Vercel project settings, then redeploy.

**Why:** Vercel needs to know your app is in a subdirectory, not the root.

**Next:** After frontend works, deploy backend to Railway separately.
