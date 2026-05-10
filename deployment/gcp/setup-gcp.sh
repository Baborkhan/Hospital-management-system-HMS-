#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
#  MedFind — Google Cloud One-Time Setup Script
#  Run this ONCE before first deployment.
#  Prerequisites: gcloud CLI installed + logged in (gcloud auth login)
# ═══════════════════════════════════════════════════════════════════════
set -e

# ──────────────────────────────────────────────────────────────────────
# CONFIGURATION — Change these values
# ──────────────────────────────────────────────────────────────────────
PROJECT_ID="medfind-bd"               # Your GCP Project ID
REGION="asia-southeast1"              # Singapore (closest to Bangladesh)
DB_INSTANCE="medfind-db"
DB_NAME="medfind"
DB_USER="medfind_user"
DB_PASSWORD="$(openssl rand -base64 32)"   # Auto-generate strong password
GITHUB_REPO="YOUR_GITHUB_USERNAME/medfind" # e.g. baborkhan/medfind

echo "╔════════════════════════════════════════════╗"
echo "║   MedFind — Google Cloud Setup             ║"
echo "╚════════════════════════════════════════════╝"
echo "Project: $PROJECT_ID | Region: $REGION"
echo ""

# ── 1. Set project ──────────────────────────────────────────────────
gcloud config set project "$PROJECT_ID"

# ── 2. Enable required APIs ─────────────────────────────────────────
echo "📡 Enabling Google Cloud APIs..."
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  firebase.googleapis.com \
  cloudbuild.googleapis.com \
  iam.googleapis.com \
  --quiet

echo "✅ APIs enabled"

# ── 3. Create Artifact Registry repo ───────────────────────────────
echo "🗂️  Creating Docker registry..."
gcloud artifacts repositories create medfind \
  --repository-format=docker \
  --location="$REGION" \
  --description="MedFind Docker Images" \
  --quiet 2>/dev/null || echo "  (registry already exists)"
echo "✅ Registry ready"

# ── 4. Create Cloud SQL PostgreSQL instance ─────────────────────────
echo "🗄️  Creating PostgreSQL database..."
gcloud sql instances create "$DB_INSTANCE" \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region="$REGION" \
  --storage-type=SSD \
  --storage-size=10GB \
  --backup-start-time=02:00 \
  --enable-bin-log \
  --quiet 2>/dev/null || echo "  (DB instance already exists)"

gcloud sql databases create "$DB_NAME" --instance="$DB_INSTANCE" --quiet 2>/dev/null || true
gcloud sql users create "$DB_USER" --instance="$DB_INSTANCE" --password="$DB_PASSWORD" --quiet 2>/dev/null || true
echo "✅ PostgreSQL ready"
echo "   DB Password (save this!): $DB_PASSWORD"

# ── 5. Create Service Account for Cloud Run ─────────────────────────
echo "🔑 Creating service account..."
gcloud iam service-accounts create medfind-sa \
  --display-name="MedFind Service Account" \
  --quiet 2>/dev/null || echo "  (SA already exists)"

SA_EMAIL="medfind-sa@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/cloudsql.client" --quiet

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/secretmanager.secretAccessor" --quiet

echo "✅ Service account ready: $SA_EMAIL"

# ── 6. Store secrets in Secret Manager ─────────────────────────────
echo "🔒 Setting up Secret Manager..."
echo "  Enter your secrets (they will be stored securely):"

create_secret() {
  local name="$1"
  local value="$2"
  echo -n "$value" | gcloud secrets create "$name" --data-file=- --quiet 2>/dev/null || \
  echo -n "$value" | gcloud secrets versions add "$name" --data-file=- --quiet
  gcloud secrets add-iam-policy-binding "$name" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/secretmanager.secretAccessor" --quiet
}

# Auto-generate a strong SECRET_KEY
SECRET_KEY="$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")"
create_secret "medfind-secret-key" "$SECRET_KEY"
create_secret "medfind-db-password" "$DB_PASSWORD"

echo ""
echo "  ⚠️  Enter your API keys (press Enter for each):"
read -rp "  ANTHROPIC_API_KEY: " ANTHROPIC_KEY
create_secret "medfind-anthropic-key" "$ANTHROPIC_KEY"

read -rp "  SSLCOMMERZ_STORE_ID: " SSL_ID
create_secret "medfind-ssl-store-id" "$SSL_ID"

read -rp "  SSLCOMMERZ_STORE_PASS: " SSL_PASS
create_secret "medfind-ssl-store-pass" "$SSL_PASS"

read -rp "  REDIS_URL (leave blank to skip): " REDIS_URL
if [ -n "$REDIS_URL" ]; then
  create_secret "medfind-redis-url" "$REDIS_URL"
fi

echo "✅ Secrets stored in Secret Manager"

# ── 7. Workload Identity for GitHub Actions ─────────────────────────
echo "🔗 Setting up Workload Identity for GitHub Actions..."
POOL_NAME="medfind-github-pool"
PROVIDER_NAME="medfind-github-provider"

gcloud iam workload-identity-pools create "$POOL_NAME" \
  --location="global" \
  --display-name="MedFind GitHub Pool" \
  --quiet 2>/dev/null || echo "  (pool already exists)"

gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_NAME" \
  --location="global" \
  --workload-identity-pool="$POOL_NAME" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --quiet 2>/dev/null || echo "  (provider already exists)"

POOL_ID=$(gcloud iam workload-identity-pools describe "$POOL_NAME" \
  --location="global" --format="value(name)")

gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${POOL_ID}/attribute.repository/${GITHUB_REPO}" \
  --quiet

PROVIDER_ID=$(gcloud iam workload-identity-pools providers describe "$PROVIDER_NAME" \
  --location="global" \
  --workload-identity-pool="$POOL_NAME" \
  --format="value(name)")

echo "✅ Workload Identity configured"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   ADD THESE TO GITHUB REPOSITORY SECRETS                  ║"
echo "║   Settings → Secrets and variables → Actions              ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ GCP_WORKLOAD_IDENTITY_PROVIDER = $PROVIDER_ID"
echo "║ GCP_SERVICE_ACCOUNT            = $SA_EMAIL"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ Google Cloud setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add GitHub secrets above"
echo "  2. git push origin main → auto-deploy starts"
echo "  3. After deploy: firebase hosting:channel:open live"
