# FIX: Unify 7 Projects on One Vercel Deployment

> Your Vercel dashboard shows 3 projects because Vercel either created separate projects per subfolder, or Root Directory is set wrong, or `vercel.json` was missing at first deploy.
> Here's the exact fix — takes 10 minutes.

---

## THE PROBLEM

When Vercel imported `github.com/alexalman/e-job-portfolio`, it likely:
1. Created **one project per folder** that has an `index.html` (hence "only 3 projects")
2. Or the initial deploy happened **before** `vercel.json` was committed
3. Or **Root Directory** was set to a subfolder instead of repo root

---

## THE FIX — 3 PHASES

### PHASE 1: Pull the updated files into your local repo

The files I just produced in this conversation include critical updates:

| File | What changed |
|------|--------------|
| `vercel.json` | Added explicit rewrites for all 7 projects with clean URLs |
| `index.html` | Cards now link to `/continuity`, `/discovery`, etc. (not nested paths) |
| All 7 project UIs | CSS paths changed from `../../../_shared/` to `/_shared/` (absolute) |
| All 7 project UIs | "Back to portfolio" links changed from `../../../index.html` to `/` |

On your local machine:

```bash
cd /path/to/your/e-job-portfolio
# Copy all updated files from Claude's outputs into this directory
# (index.html, vercel.json, and each project's apps/web/index.html)

git add -A
git commit -m "fix: unify all 7 projects under single Vercel deployment with clean URLs"
git push origin main
```

### PHASE 2: Clean up Vercel dashboard

Go to https://vercel.com/dashboard

**Delete any duplicate projects** — you should end up with only ONE project:

- ✅ Keep: The project named something like `e-job-portfolio` (connected to your repo root)
- ❌ Delete: Any project named after a subfolder (`discovery-feed-ai`, `continuity-ai`, `streaming-ad-creative-studio`, etc.)

To delete a project:
1. Click the project name
2. Settings (top right)
3. Scroll to bottom → "Delete Project"
4. Type the project name to confirm

### PHASE 3: Configure the surviving project correctly

Open your remaining `e-job-portfolio` Vercel project → Settings → **General**:

| Setting | Must be |
|---------|---------|
| **Framework Preset** | Other |
| **Root Directory** | `./` (or empty — it's the repo root) |
| **Build Command** | *(leave empty)* — override OFF |
| **Output Directory** | *(leave empty)* — override OFF |
| **Install Command** | *(leave empty)* — override OFF |
| **Node.js Version** | Default (20.x is fine) |

Save. Then trigger a redeploy:

1. Go to **Deployments** tab
2. Click the `⋯` menu on the latest deployment
3. Click **Redeploy**
4. **UNCHECK** "Use existing Build Cache"
5. Click **Redeploy**

Wait ~30 seconds for the build to finish.

---

## VERIFY IT WORKS

After the redeploy, visit your Vercel URL. You should see:

✅ The portfolio landing page with all 7 project cards
✅ Clicking each card opens that project at a clean URL like `/continuity`, `/discovery`, `/animation`
✅ Each project page has a working "← ALL PROJECTS" link back to the home
✅ All projects render with the consistent dark theme (Fraunces + JetBrains Mono)

Test each clean URL manually:
- `your-site.vercel.app/` → Landing page
- `your-site.vercel.app/continuity` → ContinuityAI
- `your-site.vercel.app/discovery` → Discovery Feed AI
- `your-site.vercel.app/animation` → GenAI Animation Incubator
- `your-site.vercel.app/orchestration` → Enterprise AI Orchestration
- `your-site.vercel.app/ad-studio` → Streaming Ad Creative Studio
- `your-site.vercel.app/live-ads` → Live Ads Engine
- `your-site.vercel.app/rec-engine` → Unified Rec Engine

---

## IF IT STILL DOESN'T WORK

Three most likely causes:

**1. Vercel is still building from an old cache**
→ Deployments → latest → ⋯ → Redeploy → UNCHECK "Use existing Build Cache"

**2. `vercel.json` is at the wrong path**
→ In your repo, `vercel.json` MUST be at the root (same level as `index.html`)
→ Run: `ls vercel.json` in the repo root — must return the filename

**3. Root Directory is still wrong**
→ Project Settings → General → Root Directory → must be `./` or empty, NOT `continuity_ai/` or any subfolder

If Vercel build logs show errors, screenshot them and I'll read them.

---

## BONUS: Custom domain setup

Once the unified deployment works, you can add a custom domain:

1. Project → Settings → Domains
2. Add `alexalman.ai` (buy from Namecheap, Cloudflare Registrar, or Porkbun — ~$70/year)
3. Vercel shows DNS records to add at your registrar
4. Propagates in ~5 minutes

Your cover letters now reference `alexalman.ai/continuity` instead of a long GitHub Pages URL. Much more credible.
