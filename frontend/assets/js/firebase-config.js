/**
 * MedFind — Firebase Configuration
 * Project: medfind-bangladesh
 * Last updated: 2026-05-01
 *
 * ✅ These keys are SAFE to expose in frontend code.
 *    Firebase Security Rules protect your data — not the config.
 *    Ref: https://firebase.google.com/docs/projects/api-keys
 */

const FIREBASE_CONFIG = {
  apiKey:            "AIzaSyCVUqudx4bX9LcRwleF2J9GMX7QYdSvXvA",
  authDomain:        "medfind-bangladesh.firebaseapp.com",
  projectId:         "medfind-bangladesh",
  storageBucket:     "medfind-bangladesh.firebasestorage.app",
  messagingSenderId: "497488341848",
  appId:             "1:497488341848:web:aa4fbafa844a0bdf2ad32d",
  measurementId:     "G-47DV6LQ5ZF"
};

/**
 * Google OAuth Client ID
 * ─────────────────────────────────────────────────────────────
 * Get from: Firebase Console → Authentication → Sign-in method
 *           → Google → Web SDK configuration → Web client ID
 *
 * Format: "497488341848-xxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com"
 *
 * NOTE: Google login via Firebase popup works WITHOUT this value.
 * This is only needed for One Tap / GIS button flows.
 * Leave as empty string until you get it from Firebase Console.
 */
const GOOGLE_CLIENT_ID = "";

// Export for use across auth modules
window.MEDFIND_FIREBASE     = FIREBASE_CONFIG;
window.MEDFIND_GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID;

// ── Runtime status log (dev only) ───────────────────────────
(function(){
  const isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
  if(isLocal){
    console.log('%c🔥 Firebase Config Loaded','color:#f59e0b;font-weight:bold;font-size:13px');
    console.log('%cProject: medfind-bangladesh','color:#34d399');
    console.log('%cApp ID: 1:497488341848:web:aa4fbafa844a0bdf2ad32d','color:#93c5fd');
    if(GOOGLE_CLIENT_ID.includes('REPLACE')){
      console.warn('%c⚠️ Google Client ID not set yet — Google login uses Firebase popup fallback','color:#fbbf24');
      console.info('%cGet it from: https://console.cloud.google.com/apis/credentials?project=medfind-bangladesh','color:#93c5fd');
    } else {
      console.log('%c✅ Google Client ID set','color:#34d399');
    }
  }
})();
