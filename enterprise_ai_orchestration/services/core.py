from __future__ import annotations
import json, re
from pathlib import Path
from typing import Any, Dict, List
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AgentRouter:
    def __init__(self): self.agents = {}
    def register(self, name, func): self.agents[name] = func
    def call(self, name, payload): return self.agents[name](payload)

class ToolRegistry:
    def __init__(self): self.tools = {}
    def register(self, name, func): self.tools[name] = func
    def call(self, name, **kwargs): return self.tools[name](**kwargs)

class RAG:
    def __init__(self, docs=None):
        self.docs = docs or []
        self.v = TfidfVectorizer(stop_words='english')
        self.m = None
        if self.docs: self.index(self.docs)
    def index(self, docs):
        self.docs = docs
        self.m = self.v.fit_transform([d['text'] for d in docs])
    def query(self, q, top_k=3):
        sims = cosine_similarity(self.v.transform([q]), self.m).flatten()
        ranked = sorted(list(enumerate(sims)), key=lambda x: x[1], reverse=True)[:top_k]
        docs = [dict(self.docs[i], score=round(float(s),3)) for i,s in ranked]
        summary = ' '.join([re.split(r'(?<=[.!?])\s+', d['text'])[0] for d in docs])
        return {'documents': docs, 'summary': summary}

class WorkflowEngine:
    def __init__(self, router, tools):
        self.router = router; self.tools = tools; self.history=[]
    def _resolve(self, value, ctx):
        if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
            return ctx.get(value[2:-2].strip(), value)
        return value
    def run(self, workflow_yaml: str):
        data = yaml.safe_load(workflow_yaml)
        ctx={}; trace=[]
        for step in data.get('steps', []):
            inputs = {k:self._resolve(v, ctx) for k,v in step.get('inputs', {}).items()}
            if step.get('agent'):
                result = self.router.call(step['agent'], inputs)
            else:
                result = self.tools.call(step['tool'], **inputs)
            if step.get('output'): ctx[step['output']] = result
            trace.append({'step': step.get('id'), 'result': result})
        self.history.append({'context': ctx, 'trace': trace})
        return ctx

def summariser(payload):
    text = payload.get('text','')
    return text[:140] + ('...' if len(text)>140 else '')

def reverse(payload): return payload.get('text','')[::-1]
def clean_text(text:str): return ' '.join(text.split())
def word_count(text:str): return len(text.split())
