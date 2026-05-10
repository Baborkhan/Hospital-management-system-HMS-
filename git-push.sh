#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  MedFind Bangladesh — Git Auto-Push & Deploy Script
#  Usage: ./git-push.sh "your commit message"
#  Or:    ./git-push.sh   (auto-generates timestamped message)
# ═══════════════════════════════════════════════════════════

set -e

MSG="${1:-Auto-update: $(date '+%Y-%m-%d %H:%M')}"
BRANCH="main"
REPO="https://github.com/Baborkhan/MedFind-Bangladesh-AI-Healthcare-Platform"

echo "╔══════════════════════════════════════════╗"
echo "║   MedFind Bangladesh — Auto Deploy       ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "📝 Commit: $MSG"
echo "🌿 Branch: $BRANCH"
echo ""

# Ensure we're on main
git checkout $BRANCH 2>/dev/null || git checkout -b $BRANCH

# Stage all changes
git add -A

# Check if anything to commit
if git diff --cached --quiet; then
  echo "✅ Nothing to commit — working tree clean."
  echo ""
  echo "🌐 Live site: https://medfind-bangladesh.web.app"
  echo "⚙️  Backend:   https://medfind-bangladesh-ai-healthcare-platform.onrender.com"
  exit 0
fi

# Show what's being committed
echo "📦 Files changed:"
git diff --cached --name-status | head -20
echo ""

# Commit
git commit -m "$MSG"

# Push
git push origin $BRANCH

echo ""
echo "════════════════════════════════════════"
echo "✅ Pushed to GitHub!"
echo "🚀 GitHub Actions will auto-deploy:"
echo "   → Render backend (~2 min)"  
echo "   → Firebase frontend (~1 min)"
echo ""
echo "📊 Monitor: $REPO/actions"
echo "🌐 Live:    https://medfind-bangladesh.web.app"
echo "════════════════════════════════════════"
