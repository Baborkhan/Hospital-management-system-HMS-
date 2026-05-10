# 🔐 MedFind — Django Gmail OTP System Setup Guide
# All 12 Points Implemented & Production Ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## ✅ CHECKLIST — 12/12 Points
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Point 1  — Django project e OTP app (otp_auth/) create korা হয়েছে
✅ Point 2  — Gmail SMTP + App Password configured (settings.py)
✅ Point 3  — EmailOTP model: email, otp, created_at, expires_at, is_used
✅ Point 4  — generate_otp() — random.SystemRandom() দিয়ে 6-digit secure OTP
✅ Point 5  — Send OTP API: POST /api/v1/accounts/send-otp/ (generate+save+email send)
✅ Point 6  — Verify OTP API: POST /api/v1/accounts/verify-otp/ (match + expiry check)
✅ Point 7  — Expiry exactly 2 minutes (server-side, timezone-aware)
✅ Point 8  — Verify হলে সাথেসাথে is_used=True (invalidated, reuse impossible)
✅ Point 9  — Resend OTP API: POST /api/v1/accounts/resend-otp/ (old OTP cancel → new OTP)
✅ Point 10 — Rate limit: 60 seconds-এ 1টা OTP (429 Too Many Requests response)
✅ Point 11 — Input validation: email format regex + 6-digit OTP check (frontend + backend)
✅ Point 12 — URLs connected + frontend login.html এ email input, Send button, OTP input সব আছে

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 📁 নতুন ফাইল Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

backend/
  otp_auth/
    __init__.py
    apps.py           ← Django app config
    models.py         ← EmailOTP model (Point 3)
    services.py       ← generate_otp, send_otp, verify_otp (Points 4,5,6,7,8,9,10,11)
    views.py          ← SendOTPView, VerifyOTPView, ResendOTPView (Points 5,6,9)
    urls.py           ← URL routes (Point 12)
    admin.py          ← Django Admin এ OTP দেখা যাবে
    migrations/
      0001_initial.py ← Database table তৈরি

  medfind_project/
    settings.py       ← otp_auth added + Gmail SMTP config (Points 1,2)
    urls.py           ← /api/v1/accounts/ route added (Point 12)

  .env.example        ← Gmail credentials template

frontend/
  pages/
    login.html        ← Real API calls, no fake fallback (Point 12)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 🚀 SETUP — Step by Step
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### STEP 1 — Gmail App Password বানাও
────────────────────────────────────────
1. browser এ যাও: https://myaccount.google.com/security
2. "2-Step Verification" → ON করো (যদি না থাকে)
3. Search bar এ type করো: "App passwords"
4. "Select app" → "Mail"  |  "Select device" → "Other" → "MedFind" লিখো
5. "Generate" click করো
6. 16-character password দেখাবে (e.g.: abcd efgh ijkl mnop)
7. এই password টা copy করে রাখো

### STEP 2 — .env ফাইল তৈরি করো
────────────────────────────────────────
backend/ folder-এ  .env  নামে ফাইল বানাও:

    SECRET_KEY=medfind-super-secret-key-change-this-2026
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

    EMAIL_HOST_USER=তোমার_gmail@gmail.com
    EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop

⚠️ NOTE: EMAIL_HOST_PASSWORD = Gmail App Password (account password না!)
⚠️ NOTE: .env ফাইলে space সহ paste করো — Gmail দেখায় 4-4 group এ

### STEP 3 — Dependencies Install করো
────────────────────────────────────────
    cd backend
    pip install -r requirements.txt

### STEP 4 — Database Migration চালাও
────────────────────────────────────────
    cd backend
    python manage.py migrate

এটা mf_email_otp table তৈরি করবে।

### STEP 5 — Server চালু করো
────────────────────────────────────────
    cd backend
    python manage.py runserver

### STEP 6 — Test করো
────────────────────────────────────────
Browser এ login.html খোলো → OTP tab → email দাও → Send OTP click করো
→ তোমার Gmail inbox-এ OTP code আসবে real time!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 🌐 API Endpoints
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POST  http://127.0.0.1:8000/api/v1/accounts/send-otp/
      Body: {"email": "user@gmail.com"}
      Response: {"success": true, "message": "OTP sent..."}

POST  http://127.0.0.1:8000/api/v1/accounts/verify-otp/
      Body: {"email": "user@gmail.com", "otp": "123456"}
      Response: {"success": true, "message": "OTP verified successfully."}

POST  http://127.0.0.1:8000/api/v1/accounts/resend-otp/
      Body: {"email": "user@gmail.com"}
      Response: {"success": true, "message": "OTP sent..."}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 🔒 Security Features
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Server-side expiry — OTP expires exactly 2 minutes after generation
• Immediate invalidation — verified OTP instantly marked is_used=True
• Rate limiting — 1 OTP per 60 seconds per email (spam protection)
• Brute-force guard — 5 wrong attempts → OTP auto-invalidated
• Old OTP cancel — resend করলে পুরানো OTP instantly blocked
• Secure random — random.SystemRandom() (OS-level entropy)
• Input validation — both frontend JS + backend Python check করে

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## ❓ Common Problems & Fixes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "SMTPAuthenticationError" বা "Username and Password not accepted"
   ✅ Fix: App Password ঠিকমতো copy হয়নি। Step 1 আবার করো।
          Gmail account password দিলে কাজ করবে না — App Password লাগবে।

❌ "Failed to send OTP email"
   ✅ Fix: .env ফাইলে EMAIL_HOST_USER এবং EMAIL_HOST_PASSWORD দুটোই দিয়েছো কিনা চেক করো।

❌ "No OTP found" during verify
   ✅ Fix: OTP আগেই expire হয়ে গেছে (2 min)। আবার Send OTP চাপো।

❌ "Please wait X seconds"
   ✅ Fix: Rate limit hit হয়েছে। 60 seconds পরে আবার চেষ্টা করো।

❌ Backend not found / Network error
   ✅ Fix: python manage.py runserver চালু আছে কিনা দেখো (port 8000)।
