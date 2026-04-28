# e-job-portfolio — AI/ML Portfolio for Entertainment AI

> Seven working prototypes targeting Disney, Netflix, and Paramount roles.
> RAG, diffusion, vision-LLM, recommendation, and orchestration — each project has a runnable backend and a polished browser UI.

## Live preview

Open `index.html` in a browser to see the full portfolio landing page.
Each project card links directly to its interactive demo.

Every project UI includes a **static fallback** so demos work even without the backend running — perfect for GitHub Pages hosting.

## Projects

| # | Project | Stack | Port |
|---|---------|-------|------|
| 01 | [**ContinuityAI**](continuity_ai/) — flagship vision-LLM for continuity detection | FastAPI · Claude Vision | 8006 |
| 02 | [**Discovery Feed AI**](discovery_feed_ai/) — semantic post-binge recommender | TF-IDF · sklearn | 8001 |
| 03 | [**GenAI Animation Incubator**](genai_animation_incubator/) — prompt-to-animatic pipeline | Pillow · diffusion-ready | 8005 |
| 04 | [**Enterprise AI Orchestration**](enterprise_ai_orchestration/) — RAG + agents + tools + workflow | RAG · YAML workflows | 8000 |
| 05 | [**Ad Creative Studio**](streaming_ad_creative_studio/) — brief-to-campaign generator | FastAPI | 8002 |
| 06 | [**Live Ads Engine**](live_ads_personalization_engine/) — real-time slot planning | Segment ranking | 8003 |
| 07 | [**Unified Rec Engine**](pluto_paramount_unified_rec_engine/) — Pluto + Paramount+ bridge | TF-IDF · cosine | 8004 |

## Running locally

Every project follows the same pattern:

```bash
cd <project_name>
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port <port>
# Then open apps/web/index.html in your browser
```

For example, the flagship ContinuityAI:

```bash
cd continuity_ai
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port 8006
open apps/web/index.html
```

## Running all backends at once

```bash
# From repo root
for project in continuity_ai:8006 discovery_feed_ai:8001 genai_animation_incubator:8005 \
               enterprise_ai_orchestration:8000 streaming_ad_creative_studio:8002 \
               live_ads_personalization_engine:8003 pluto_paramount_unified_rec_engine:8004; do
  dir="${project%:*}"
  port="${project#*:}"
  (cd "$dir" && uvicorn apps.api.main:app --port "$port" &)
done
```

Then open `index.html` in your browser.

## Design system

All project UIs share a consistent visual language via `_shared/styles.css`:
- Dark editorial aesthetic — Fraunces serif + JetBrains Mono
- Distinctive accent color per project (gold, blue, violet, green, amber, red)
- Responsive grid layouts, semantic badges, score rings, typography scales

## Deployment to GitHub Pages

All UIs include static fallback data, so the landing page and project previews work directly on GitHub Pages without needing a backend running:

1. Push to `main` branch on GitHub
2. Settings → Pages → Deploy from `main` branch, root folder
3. Access at `https://alexalman.github.io/e-job-portfolio/`

Only live API interactions (running new queries against a backend) require local `uvicorn` servers.

## Background

10+ years of production ML — from EPAM Minsk and Yandex Moscow, to New York, now based in Los Angeles. Every project was built to demonstrate a specific engineering capability relevant to AI/ML roles at the three major studios.
