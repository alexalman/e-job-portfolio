# Streaming Ad Creative Studio

A lightweight working prototype for generating ad concepts, scripts, storyboards,
and AI-style campaign summaries from a single campaign brief. It uses deterministic
Python logic and a FastAPI backend so it runs locally without external APIs.

## Run

```bash
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port 8002
```

Open `apps/web/index.html` in your browser.

## Features
- campaign brief form
- generates 3 ad concepts
- creates 6s / 15s / 30s scripts
- creates clickable storyboard cards
- generates a mock campaign performance summary
