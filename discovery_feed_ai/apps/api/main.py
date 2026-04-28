from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fastapi import FastAPI, Query
from pydantic import BaseModel
from services.recs import feed, watch

app = FastAPI(title='Discovery Feed AI')
class WatchReq(BaseModel): title: str
@app.get('/')
def root(): return {'message':'Discovery Feed AI is running.'}
@app.get('/feed')
def get_feed(q: str | None = Query(None), k: int = 10): return {'results': feed(q, k)}
@app.post('/watch')
def do_watch(req: WatchReq): return watch(req.title)
