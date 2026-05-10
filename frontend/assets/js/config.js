/**
 * MedFind Bangladesh — Frontend Configuration v3.0
 * ══════════════════════════════════════════════════
 *
 * HOW AI WORKS (no key needed for users):
 *   Browser → Django /api/v1/ai/chat/ → Anthropic (key stays on server)
 *
 * FOR LOCAL DEV WITHOUT DJANGO:
 *   Set ANTHROPIC_KEY below with your sk-ant-... key
 *   OR run Django: cd backend && python manage.py runserver
 *
 * FOR PRODUCTION:
 *   1. Set ANTHROPIC_API_KEY in your .env file
 *   2. Update PRODUCTION_API_URL to your deployed backend URL
 *   3. Leave ANTHROPIC_KEY empty here
 */
(function () {
  const isLocal =
    location.hostname === 'localhost' || location.hostname === '127.0.0.1';

  // ── PRODUCTION BACKEND URL (update after deploy) ──────────
<<<<<<< HEAD
  const PRODUCTION_API_URL = 'https://medfind-bangladesh-ai-healthcare-platform.onrender.com/api/v1';
=======
  const PRODUCTION_API_URL = 'https://medfind-backend-CHANGE-THIS.a.run.app/api/v1';
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
  // ──────────────────────────────────────────────────────────

  // ── LOCAL DEV ONLY: set your Anthropic key here if Django is not running
  // ⚠️  NEVER commit a real key to git. Leave empty in production.
  const DEV_ANTHROPIC_KEY = '';   // e.g. 'sk-ant-api03-...'  (local dev only)
  // ──────────────────────────────────────────────────────────

  window.MEDFIND_CONFIG = {
    API_BASE:         isLocal ? 'http://127.0.0.1:8000/api/v1' : PRODUCTION_API_URL,
    ANTHROPIC_KEY:    isLocal ? DEV_ANTHROPIC_KEY : '',
    GOOGLE_CLIENT_ID: window.MEDFIND_GOOGLE_CLIENT_ID || '',
    FIREBASE:         window.MEDFIND_FIREBASE || {},
    VERSION:          '3.0',
    ENV:              isLocal ? 'development' : 'production',
    AUTH_PROVIDER:    'firebase',
  };

  if (isLocal) {
    console.log('%c🏥 MedFind v3.0 — Development Mode', 'color:#14b8a6;font-weight:bold;font-size:14px');
    console.log('%c📡 API Base:',   'color:#93c5fd;font-weight:600', window.MEDFIND_CONFIG.API_BASE);
    console.log('%c🤖 AI Proxy:',   'color:#93c5fd;font-weight:600', window.MEDFIND_CONFIG.API_BASE + '/ai/chat/');
    if (DEV_ANTHROPIC_KEY) {
      console.log('%c🔑 Dev key set (direct mode)', 'color:#fbbf24;font-weight:600');
    } else {
      console.log('%c⚡ Start Django for AI: python manage.py runserver', 'color:#f87171;font-weight:600');
    }
  }
})();
