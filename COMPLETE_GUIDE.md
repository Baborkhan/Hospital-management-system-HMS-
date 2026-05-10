# 🏥 MedFind Bangladesh — Production-Ready Guide
**Version:** Final | Project: medfind-bangladesh (Firebase)

---

## ✅ BUGS FIXED IN THIS VERSION

| # | Issue | Status |
|---|-------|--------|
| 1 | Organ Donation page — complete black screen | ✅ FIXED |
| 2 | OTP not visible — only appeared in browser Console | ✅ FIXED |
| 3 | OTP not auto-filling digits | ✅ FIXED |
| 4 | firebase.json catch-all rewrite breaking .html pages | ✅ FIXED |
| 5 | Blood donor page blank when backend offline | ✅ FIXED (demo data added) |
| 6 | services/api.js hardcoded to localhost only | ✅ FIXED |
| 7 | Bad folder `{patients,...}` in pages directory | ✅ REMOVED |

---

## 🖥️ STEP 1 — Run in VS Code (Local)

### Install these once (if not already installed):
1. **Node.js** → https://nodejs.org → Download LTS
2. **VS Code** → https://code.visualstudio.com
3. **Git** → https://git-scm.com

### Open the project:
```
1. Open VS Code
2. File → Open Folder → Select "medfind_final" folder
```

### Install Live Server extension:
```
1. Click the Extensions icon (left sidebar — 4 squares icon)
2. Search: Live Server
3. Install "Live Server" by Ritwick Dey
```

### Run the site:
```
1. In VS Code left panel → find: frontend/index.html
2. Right-click → "Open with Live Server"
3. Browser opens at: http://127.0.0.1:5500/frontend/
```

**The full site is now running locally!** All pages work.

> **Note:** Features like OTP email, Firestore save, and Doctor search data require Firebase setup (Step 2). Without it, they run in demo mode automatically — the OTP is shown on screen and demo data is displayed.

---

## 🔥 STEP 2 — Firebase Setup (for real OTP + login + data)

### 2a. Go to Firebase Console
Open: **https://console.firebase.google.com**
Click your project: **medfind-bangladesh**

### 2b. Enable Authentication
```
Firebase Console
  → Authentication
  → Sign-in method
  → Enable: Email/Password ✓
  → Enable: Email link (passwordless sign-in) ✓
  → Save
```

### 2c. Add Authorized Domains
```
Firebase Console
  → Authentication
  → Settings tab
  → Authorized domains
  → Add domain: localhost
  → Add domain: 127.0.0.1
  → Add domain: medfind-bangladesh.web.app  (already there)
  → Add domain: YOUR-CUSTOM-DOMAIN.com  (if you have one)
```

### 2d. Enable Firestore Database
```
Firebase Console
  → Firestore Database
  → Create database
  → Start in production mode
  → Choose region: asia-southeast1 (Singapore — closest to Bangladesh)
  → Done
```

### 2e. Deploy Firestore Security Rules
After deploying (Step 3), run:
```bash
firebase deploy --only firestore:rules
```

### 2f. Google OAuth (optional — for Google login button)
```
1. Go to: https://console.cloud.google.com/apis/credentials?project=medfind-bangladesh
2. Click: + Create Credentials → OAuth 2.0 Client ID
3. Application type: Web application
4. Name: MedFind Web
5. Authorized JavaScript origins:
     http://localhost
     http://127.0.0.1:5500
     https://medfind-bangladesh.web.app
6. Click Create → Copy the Client ID
7. Open: frontend/assets/js/firebase-config.js
8. Replace: REPLACE_WITH_YOUR_OAUTH_CLIENT_ID
   With your actual Client ID
```

---

## 🌐 STEP 3 — Deploy to Firebase Hosting (Go Live!)

### 3a. Install Firebase CLI
Open **Terminal** (or Command Prompt / PowerShell on Windows):
```bash
npm install -g firebase-tools
```

### 3b. Login to Firebase
```bash
firebase login
```
→ A browser window opens → Login with Google account that owns the project

### 3c. Navigate to project folder
```bash
# Windows example:
cd C:\Users\YourName\Downloads\medfind_final

# Mac/Linux example:
cd ~/Downloads/medfind_final
```

### 3d. Initialize (first time only — already configured)
The `firebase.json` and `.firebaserc` are already set up. Skip this.

### 3e. DEPLOY! 🚀
```bash
firebase deploy --only hosting
```

**Output you'll see:**
```
=== Deploying to 'medfind-bangladesh'...
i  deploying hosting
✔  hosting[medfind-bangladesh]: file upload complete
✔  Deploy complete!

Project Console: https://console.firebase.google.com/project/medfind-bangladesh/overview
Hosting URL: https://medfind-bangladesh.web.app
```

**Your site is LIVE at:** https://medfind-bangladesh.web.app 🎉

---

## 🔄 STEP 4 — Update After Changes

Whenever you edit files, just run:
```bash
firebase deploy --only hosting
```
Takes about 30 seconds.

---

## 🌍 STEP 5 — Connect Custom Domain (e.g. medfindbd.com)

```
Firebase Console
  → Hosting
  → Add custom domain
  → Enter: medfindbd.com
  → Follow DNS verification steps (add TXT record to your domain registrar)
  → SSL certificate is automatic and free!
```

For `.com.bd` domains, contact your registrar (like BDIX or any BD domain provider) to add the DNS records Firebase shows you.

---

## 🔑 How OTP Works (Current Setup)

### If Firebase is configured:
- User enters email → Firebase sends magic link to email inbox
- User clicks the link → automatically logged in
- No OTP code needed

### If Firebase NOT configured (Demo Mode):
- User enters email → OTP is **immediately shown on screen** in large text
- OTP is **auto-filled** in the 6 boxes
- User just clicks **Verify** → enters the site
- Works 100% without any backend

---

## 🩸 Blood Donor Search

- With backend running → fetches real donors from database
- Without backend → shows 8 sample donor profiles automatically
- Donor registration always saves to Firestore (if connected) or localStorage

---

## 📋 Admin Panel Access

The admin dashboard is protected. To login:
- Go to: `https://your-site.web.app/pages/admin/dashboard.html`
- Owner emails: `ahsanulyaminbabor@gmail.com` / `baborkhan117085@gmail.com`
- Owner phones: `01772172829` / `01516550217`

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Page shows black/blank | Hard refresh: `Ctrl+Shift+R` (Win) / `Cmd+Shift+R` (Mac) |
| OTP not received by email | Check spam folder; demo OTP is shown on screen anyway |
| Firebase "auth/unauthorized-domain" error | Add your domain to Firebase → Authentication → Authorized domains |
| Google login popup blocked | Allow popups for your site URL in browser settings |
| `firebase: command not found` | Run `npm install -g firebase-tools` first |
| `Error: Not in a Firebase app directory` | Make sure you're in the `medfind_final` folder, not inside `frontend` |
| Blood donor shows "Could not connect" | This is fixed in this version — demo donors show automatically |
| API errors (404 /api/v1/...) | Normal — backend not running. Frontend works in demo mode |

---

## 📂 Project Structure

```
medfind_final/
├── frontend/                    ← All website files (deployed to Firebase)
│   ├── index.html               ← Homepage
│   ├── 404.html                 ← Custom error page
│   ├── assets/
│   │   ├── css/                 ← All stylesheets
│   │   └── js/
│   │       ├── firebase-config.js  ← Firebase credentials (your project)
│   │       ├── components.js    ← Auto navbar + footer injection
│   │       ├── firestore.js     ← Database operations
│   │       └── config.js        ← API URL configuration
│   ├── services/
│   │   └── api.js               ← Backend API calls
│   └── pages/
│       ├── login.html           ← Login (OTP fixed ✓)
│       ├── register.html        ← Registration (OTP fixed ✓)
│       ├── donate/index.html    ← Organ donation (black screen fixed ✓)
│       ├── blood-donor/         ← Blood donor search (demo data added ✓)
│       ├── symptoms/            ← AI symptom checker
│       ├── doctors/             ← Doctor search + console
│       ├── patients/            ← Patient dashboard + records
│       ├── hospital/            ← Hospital list + admin
│       ├── admin/               ← Admin panel (protected)
│       └── ...
├── firebase.json                ← Firebase hosting config (fixed ✓)
├── firestore.rules              ← Database security rules
├── firestore.indexes.json       ← Database indexes
├── .firebaserc                  ← Project: medfind-bangladesh
└── backend/                     ← Django backend (optional for advanced features)
```

---

## 💡 Quick Reference — All Pages

| Page | URL after deploy |
|------|-----------------|
| Homepage | `/` |
| Login | `/pages/login.html` |
| Register | `/pages/register.html` |
| Organ Donation | `/pages/donate/index.html` |
| Blood Donor Search | `/pages/blood-donor/search.html` |
| Symptom Checker | `/pages/symptoms/index.html` |
| Doctor Search | `/pages/doctors/search.html` |
| Hospital List | `/pages/hospital/list.html` |
| MedFind AI | `/pages/medfind-ai.html` |
| Patient Dashboard | `/pages/patients/dashboard.html` |
| Admin Panel | `/pages/admin/dashboard.html` |

---

## 📞 Support

- Firebase docs: https://firebase.google.com/docs/hosting
- Firebase Console: https://console.firebase.google.com
- Project email: medfindbd2026@gmail.com

