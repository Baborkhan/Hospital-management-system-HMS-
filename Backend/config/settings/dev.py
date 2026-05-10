from .base import *

DEBUG = True

# SQLite — no PostgreSQL setup needed for local dev
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Allow all origins in dev
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Email — print to console in dev (see emails in terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable Redis/Celery requirements in dev
CELERY_TASK_ALWAYS_EAGER = True

# Disable MongoDB requirements in dev
MONGODB_URI = None

# ── Channel Layers — use in-memory for dev (no Redis required) ──
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

