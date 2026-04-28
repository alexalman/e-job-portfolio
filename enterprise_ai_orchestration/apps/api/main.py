from __future__ import annotations
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fastapi import FastAPI
from pydantic import BaseModel
from services.core import AgentRouter, ToolRegistry, RAG, WorkflowEngine, summariser, reverse, clean_text, word_count

app = FastAPI(title='Enterprise AI Orchestration')
router = AgentRouter(); router.register('summariser', summariser); router.register('reverse', reverse)
tools = ToolRegistry(); tools.register('clean_text', clean_text); tools.register('word_count', word_count)
rag = RAG(json.loads((Path(__file__).resolve().parents[2] / 'data' / 'docs.json').read_text()))
engine = WorkflowEngine(router, tools)

class DocsReq(BaseModel): documents: list
class QueryReq(BaseModel): query: str; top_k: int = 3
class WorkflowReq(BaseModel): workflow: str

@app.get('/')
def root(): return {'message':'Enterprise AI Orchestration is running.'}
@app.post('/rag/index')
def index(req: DocsReq): rag.index(req.documents); return {'indexed': len(req.documents)}
@app.post('/rag/query')
def query(req: QueryReq): return rag.query(req.query, req.top_k)
@app.post('/workflow/run')
def run(req: WorkflowReq): return {'context': engine.run(req.workflow)}
@app.get('/history')
def history(): return engine.history
