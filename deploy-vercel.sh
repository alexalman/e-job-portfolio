#!/usr/bin/env bash
# deploy-vercel.sh — Deploy the portfolio to Vercel
#
# Prerequisites (one-time setup on your machine):
#   1. Node.js 18+ installed:  node --version
#   2. Vercel CLI installed:   npm install -g vercel
#   3. Signed in to Vercel:    vercel login
#
# Usage:
#   ./deploy-vercel.sh                # preview deployment
#   ./deploy-vercel.sh --prod         # production deployment
#   ./deploy-vercel.sh --prod --yes   # production, skip confirmations

set -e

cd "$(dirname "$0")"

# ─── CHECK PREREQUISITES ──────────────────────────────────────────────────────
echo "→ Checking prerequisites..."

if ! command -v node >/dev/null 2>&1; then
  echo "✗ Node.js not installed. Install from https://nodejs.org/"
  exit 1
fi

if ! command -v vercel >/dev/null 2>&1; then
  echo "→ Vercel CLI not found. Installing globally..."
  npm install -g vercel
fi

# Check login status
if ! vercel whoami >/dev/null 2>&1; then
  echo "→ Not signed in to Vercel. Opening login..."
  vercel login
fi

ACCOUNT=$(vercel whoami 2>/dev/null || echo "unknown")
echo "✓ Signed in as: $ACCOUNT"

# ─── DEPLOY ───────────────────────────────────────────────────────────────────
echo ""
echo "→ Deploying e-job-portfolio to Vercel..."
echo ""

if [ "$1" = "--prod" ]; then
  if [ "$2" = "--yes" ]; then
    vercel --prod --yes
  else
    vercel --prod
  fi
else
  vercel
fi

echo ""
echo "─────────────────────────────────────────────────────────────────"
echo "✓ Deployment complete."
echo ""
echo "Next steps on Vercel dashboard (https://vercel.com/dashboard):"
echo "  1. Add a custom domain (e.g. alexalman.ai) in Project Settings → Domains"
echo "  2. Enable analytics in Project Settings → Analytics"
echo "  3. Connect GitHub for auto-deploy:"
echo "     Settings → Git → Connect → github.com/alexalman/e-job-portfolio"
echo ""
echo "Once GitHub is connected, every 'git push' auto-deploys."
echo "─────────────────────────────────────────────────────────────────"
