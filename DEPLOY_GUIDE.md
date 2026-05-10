# 🚀 MedFind — Google Deployment Guide
**Version:** 2.0 | Stack: Firebase Hosting + Google Cloud Run + Cloud SQL

---

## Architecture Overview

```
User Browser
     │
     ▼
Firebase Hosting (frontend)    ← medfind.com.bd
     │  /api/** → rewrites to ↓
     ▼
Google Cloud Run (backend)     ← Django + DRF
     │
     ├── Cloud SQL PostgreSQL  ← User, doctor, appointment data
     ├── MongoDB Atlas         ← Medical records, chat logs
     └── Secret Manager        ← All API keys & passwords
```

---

## STEP 1 — Prerequisites (Install these first)

```bash
# 1. Google Cloud CLI
curl https://sdk.cloud.google.com | bash
gcloud init

# 2. Firebase CLI
npm install -g firebase-tools
firebase login

# 3. Docker (for local testing)
# Install from: https://docs.docker.com/get-docker/
```

---

## STEP 2 — Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Click "New Project" → Name: **MedFind** → Project ID: **medfind-bd**
3. Enable Billing (required for Cloud Run)

---

## STEP 3 — Run One-Time GCP Setup

```bash
# Update PROJECT_ID and GITHUB_REPO in this file first!
nano deployment/gcp/setup-gcp.sh

# Then run:
bash deployment/gcp/setup-gcp.sh
```

This script will:
- Enable all required Google APIs
- Create Docker Artifact Registry
- Create PostgreSQL database (Cloud SQL)
- Store all secrets in Secret Manager
- Set up GitHub Actions authentication (Workload Identity)

At the end, it shows **2 values** — add them to GitHub Secrets.

---

## STEP 4 — Add GitHub Repository Secrets

Go to: `GitHub Repo → Settings → Secrets and variables → Actions`

| Secret Name | Value |
|---|---|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | (from setup script output) |
| `GCP_SERVICE_ACCOUNT` | `medfind-sa@medfind-bd.iam.gserviceaccount.com` |
| `FIREBASE_SERVICE_ACCOUNT` | (see Step 5) |

---

## STEP 5 — Set Up Firebase

```bash
# 1. Create Firebase project (use existing GCP project)
# Go to: https://console.firebase.google.com → Add project → Use existing → medfind-bd

# 2. Get service account JSON for GitHub Actions
# Firebase Console → Project Settings → Service accounts → Generate new private key
# Copy the JSON content → add as GitHub secret: FIREBASE_SERVICE_ACCOUNT

# 3. Initialize Firebase (run once locally)
firebase login
firebase init hosting
# → Use existing project: medfind-bd
# → Public directory: frontend
# → Single-page app: NO (we have our own 404.html)
```

---

## STEP 6 — First Deploy

```bash
# Push to main branch → GitHub Actions deploys automatically
git add .
git commit -m "Initial production deploy"
git push origin main
```

Watch deployment at: `GitHub Repo → Actions` tab

---

## STEP 7 — After First Deploy, Update API URL

```bash
# Get your Cloud Run URL
gcloud run services describe medfind-backend \
  --region=asia-southeast1 \
  --format="value(status.url)"
# Output: https://medfind-backend-abc123-as.a.run.app
```

Update `frontend/assets/js/config.js`:
```js
const PRODUCTION_API_URL = 'https://medfind-backend-abc123-as.a.run.app/api/v1';
```

Also update `firebase.json` → rewrites → `serviceId` if needed.

Then push again: `git push origin main`

---

## STEP 8 — Custom Domain

### Firebase (Frontend)
1. Firebase Console → Hosting → Add custom domain
2. Enter: `medfind.com.bd`
3. Add the DNS records it shows you (in your domain registrar)
4. HTTPS is automatic ✅

### Cloud Run (Backend)
```bash
gcloud run domain-mappings create \
  --service=medfind-backend \
  --domain=api.medfind.com.bd \
  --region=asia-southeast1
```

---

## STEP 9 — Verify Everything Works

```bash
# Test backend health
curl https://api.medfind.com.bd/api/v1/health/

# Test frontend
open https://medfind.com.bd
```

Checklist:
- [ ] Homepage loads
- [ ] Login works
- [ ] Doctor search works
- [ ] Appointment booking works
- [ ] Admin login works
- [ ] Mobile view works

---

## Costs (Estimated for Bangladesh-scale)

| Service | Free Tier | After Free |
|---|---|---|
| Firebase Hosting | 10 GB/month free | ~$0.026/GB |
| Cloud Run | 2M requests/month free | ~$0.40/million req |
| Cloud SQL (db-f1-micro) | ❌ | ~$7-10/month |
| Secret Manager | 6 active secrets free | Minimal |
| **Total (small scale)** | **~$7-10/month** | grows with traffic |

---

## Quick Rollback

```bash
# List previous versions
gcloud run revisions list --service=medfind-backend --region=asia-southeast1

# Rollback to a specific version
gcloud run services update-traffic medfind-backend \
  --to-revisions=REVISION_NAME=100 \
  --region=asia-southeast1
```

---

## Monitoring

- Cloud Run logs: https://console.cloud.google.com/run
- Error tracking: Add Sentry DSN to Secret Manager as `medfind-sentry-dsn`
- Uptime checks: Google Cloud Monitoring → Uptime checks → Create

