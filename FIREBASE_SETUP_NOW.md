# 🔥 Firebase Setup — করো এখনই (5 মিনিট)

firebase-config.js এ real values দেওয়া হয়েছে ✅
এখন শুধু Firebase Console-এ 3টা switch ON করতে হবে।

---

## Step 1 — Authentication Enable করো

এই link-এ যাও:
👉 https://console.firebase.google.com/project/medfind-bangladesh/authentication/providers

নিচের তিনটা Enable করো:

| Provider | Enable | Extra Setting |
|----------|--------|---------------|
| **Google** | ✅ ON | Support email দাও (তোমার Gmail) |
| **Email/Password** | ✅ ON | কিছু লাগবে না |
| **Email link (passwordless)** | ✅ ON | কিছু লাগবে না |

---

## Step 2 — Authorized Domains যোগ করো

এই link-এ যাও:
👉 https://console.firebase.google.com/project/medfind-bangladesh/authentication/settings

"Authorized domains" section → "Add domain" button → এগুলো যোগ করো:
- `localhost` (usually already there)
- `127.0.0.1`
- `medfind-bangladesh.web.app`
- `medfind-bangladesh.firebaseapp.com`
- তোমার custom domain (যদি থাকে)

---

## Step 3 — Google Client ID নাও (Optional but recommended)

👉 https://console.cloud.google.com/apis/credentials?project=medfind-bangladesh

"OAuth 2.0 Client IDs" section → Web client → Copy the Client ID
Format: `497488341848-xxxxxxxx.apps.googleusercontent.com`

এটা firebase-config.js এর GOOGLE_CLIENT_ID এ paste করো।

⚠️ ছাড়াও Google login কাজ করবে (Firebase popup দিয়ে) — optional।

---

## ✅ Test করো

1. VS Code → Live Server → login.html খোলো
2. "Continue with Google" click করো
3. Firebase popup আসবে → Google account select করো
4. Dashboard-এ redirect হবে → ✅ কাজ করছে!

Email OTP test:
1. register.html → যেকোনো email দাও
2. "Send OTP" click করো
3. ওই email-এ Firebase-এর email আসবে → link click করো → ✅

---

*এই ফাইলটা deploy-এর আগে delete করো (private info নেই, তবু clean রাখো)*
