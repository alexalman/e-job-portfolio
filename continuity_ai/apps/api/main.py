from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from services.continuity import analyze_frame_pair, classify_episode, build_demo_report

app = FastAPI(title='ContinuityAI')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


class FramePairReq(BaseModel):
    frame_a_desc: str
    frame_b_desc: str
    shot_index: int = 0


@app.get('/')
def root():
    return {'message': 'ContinuityAI is running.'}


@app.post('/analyze/pair')
def analyze_pair(req: FramePairReq):
    """Analyze a single shot pair by description. Used by the web demo UI."""
    return analyze_frame_pair(req.frame_a_desc, req.frame_b_desc, req.shot_index)


@app.get('/demo/report')
def demo_report():
    """Return a full pre-analyzed demo episode report for the UI."""
    return build_demo_report()


@app.get('/health')
def health():
    return {'status': 'ok', 'model': 'deterministic-demo'}
