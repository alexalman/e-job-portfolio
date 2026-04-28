from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fastapi import FastAPI
from pydantic import BaseModel
from services.pipeline import run_pipeline

app = FastAPI(title='GenAI Animation Incubator')
BASE_DIR = Path(__file__).resolve().parents[2] / 'outputs'

class GenerateReq(BaseModel): prompt: str

@app.get('/')
def root(): return {'message':'GenAI Animation Incubator is running.'}
@app.post('/generate')
def generate(req: GenerateReq): return run_pipeline(req.prompt, BASE_DIR)
