# ContinuityAI — Vision-LLM Post-Production Continuity Detection

> The same class of problem Netflix paid $600M to solve (InterPositive acquisition, March 2026).

Scans consecutive film frames to detect continuity errors across seven categories — props, lighting, costume, background extras, makeup, environmental match, and screen direction — and queues auto-fixable issues for the VFX pipeline.

## Run

```bash
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port 8006
```

Then open `apps/web/index.html` in your browser.

## Endpoints

- `GET /demo/report` — returns a full pre-analyzed 10-shot demo episode
- `POST /analyze/pair` — body `{frame_a_desc, frame_b_desc, shot_index}` — analyzes a single frame pair
- `GET /health` — service health

## Architecture

```
Frame pair descriptions (or video)
  │
  ▼
services/continuity.py      Deterministic demo analyzer
                            (swap for Claude Vision in production)
  │
  ▼
classify_episode()          Aggregate → priority shots, VFX queue
  │
  ▼
apps/web/index.html         Interactive shot list + error panel
```

## Production upgrade path

The demo service (`services/continuity.py`) uses a deterministic seeded analyzer so the portfolio works out of the box. In production, swap `analyze_frame_pair()` for the Claude Vision API version (see commented reference implementation in the file).

## Relevance

Netflix acquired InterPositive (Ben Affleck's AI post-production startup) for up to $600M in March 2026 to solve automated continuity supervision. This project independently demonstrates the same pipeline architecture — the engineering chops required for Netflix Inkubator and Disney/Paramount GenAI teams.
