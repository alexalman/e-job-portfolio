# Pluto + Paramount Unified Recommendation & Conversion Engine

A working prototype that simulates a shared free-to-paid recommendation layer.
It takes a user profile, recommends titles across free and premium catalogs,
and generates upgrade prompts and churn-risk signals.

## Run

```bash
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port 8004
```

Open `apps/web/index.html` in your browser.
