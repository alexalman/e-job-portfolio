# Deploy to Vercel — 3-Minute Guide

> I can't deploy from inside Claude directly (no auth to your Vercel account), but these three files make it a single command on your machine.

## Option A: One-command deploy (recommended)

If you already have Node.js installed:

```bash
cd e-job-portfolio
npm install -g vercel   # one-time: install the Vercel CLI
vercel login            # one-time: opens your browser to log in
./deploy-vercel.sh      # deploys a preview URL
```

To deploy to production (your actual domain):
```bash
./deploy-vercel.sh --prod
```

That's it. Vercel will output a URL like `e-job-portfolio-xxxxx.vercel.app`.

## Option B: GitHub → Vercel auto-deploy (best long-term)

This is the setup I'd actually recommend — every `git push` auto-deploys:

1. Push the portfolio to GitHub first:
   ```bash
   cd e-job-portfolio
   ./deploy.sh
   ```

2. Go to https://vercel.com/new

3. Click **"Import Git Repository"**

4. Select `alexalman/e-job-portfolio`

5. Leave all defaults (Vercel auto-detects the `vercel.json` config)

6. Click **"Deploy"**

Done. Takes ~30 seconds. Every future push to `main` auto-deploys.

## What's included in `vercel.json`

The config file I created gives you **clean URLs** for each project:

| URL | Goes to |
|-----|---------|
| `alexalman.com/` | Portfolio landing page |
| `alexalman.com/continuity` | ContinuityAI demo |
| `alexalman.com/discovery` | Discovery Feed AI |
| `alexalman.com/animation` | GenAI Animation Incubator |
| `alexalman.com/orchestration` | Enterprise AI Orchestration |
| `alexalman.com/ad-studio` | Streaming Ad Creative Studio |
| `alexalman.com/live-ads` | Live Ads Engine |
| `alexalman.com/rec-engine` | Unified Rec Engine |

Much cleaner than `/continuity_ai/apps/web/index.html` for your resume and cover letters.

## Custom domain (optional but worth it)

After deploy, in the Vercel dashboard:

1. Project Settings → Domains
2. Add your domain (e.g. `alexalman.ai`)
3. Vercel shows you the DNS records to add at your registrar
4. Usually works within ~5 minutes

Domains like `alexalman.ai` are $70/year and read much better in a cover letter than `alexalman.github.io/e-job-portfolio/`.

## What `.vercelignore` excludes

The Python backends don't deploy to Vercel (Vercel serves static sites). That's fine — every UI has a fallback mode so demos work on the deployed site. The backends only run locally when you want to show real API calls during an interview.

## Troubleshooting

**"vercel: command not found" after install**
```bash
# Fix PATH, then retry
export PATH="$PATH:$(npm config get prefix)/bin"
```

**"Permission denied" on deploy-vercel.sh**
```bash
chmod +x deploy-vercel.sh
```

**"Build failed"**
Not possible — this is a pure static site with no build step. If you see this, check that `vercel.json` is at the repo root (not inside a subfolder).

## After deploy — update your resume & cover letters

Replace every instance of:
- `alexalman.github.io/e-job-portfolio` → `alexalman.com` (or whatever domain you picked)
- The portfolio URL in the header of `resume.txt`
- The portfolio URLs in all 3 cover letter templates

Then you're ready to apply.
