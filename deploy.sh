#!/usr/bin/env bash
# deploy.sh — quickly push this portfolio to your GitHub repo
#
# Usage:
#   ./deploy.sh                              # push to origin main
#   ./deploy.sh "custom commit message"      # push with custom message

set -e

MSG="${1:-feat: full portfolio with 7 projects and polished UIs}"

# Check we are in a git repo
if [ ! -d .git ]; then
  echo "→ Initializing git repo..."
  git init
  git remote add origin https://github.com/alexalman/e-job-portfolio.git
fi

# Check remote is configured
if ! git remote -v | grep -q "alexalman/e-job-portfolio"; then
  echo "→ Adding remote..."
  git remote add origin https://github.com/alexalman/e-job-portfolio.git 2>/dev/null || \
    git remote set-url origin https://github.com/alexalman/e-job-portfolio.git
fi

# Stage, commit, push
git add -A
git status --short

echo ""
echo "→ Committing: $MSG"
git commit -m "$MSG" || echo "  (nothing to commit)"

echo ""
echo "→ Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✓ Done. View at:"
echo "  https://github.com/alexalman/e-job-portfolio"
echo ""
echo "To enable GitHub Pages (portfolio live preview):"
echo "  1. https://github.com/alexalman/e-job-portfolio/settings/pages"
echo "  2. Source: Deploy from branch → main → / (root)"
echo "  3. Save — site available at https://alexalman.github.io/e-job-portfolio/"
