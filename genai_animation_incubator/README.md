# GenAI Animation Incubator

## Run
```bash
pip install -r requirements.txt
uvicorn apps.api.main:app --reload --port 8005
```

Use `POST /generate` with a prompt to produce a script, shot list, and placeholder animatic frames.
