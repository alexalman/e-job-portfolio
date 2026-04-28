# Enterprise AI Orchestration

## Run
```bash
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port 8000
```

### Example endpoints
- `POST /rag/index`
- `POST /rag/query`
- `POST /workflow/run`
- `GET /history`
