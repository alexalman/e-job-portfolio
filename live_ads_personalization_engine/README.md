# Live Ads Personalization Engine

A working simulation of a live-event ad decision engine. It generates ad slot
plans for different audience segments and contexts, showing how creative variants
and pacing can change in real time.

## Run

```bash
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port 8003
```

Open `apps/web/index.html` in your browser.
