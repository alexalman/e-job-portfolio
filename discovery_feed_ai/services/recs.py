from __future__ import annotations
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CATALOG = json.loads((Path(__file__).resolve().parent.parent / 'data' / 'catalog.json').read_text())
V = TfidfVectorizer(stop_words='english')
M = V.fit_transform([x['title']+' '+x['synopsis']+' '+x['tags'] for x in CATALOG])
HISTORY = []

def feed(query: str | None = None, k: int = 10):
    q = query or (' '.join(HISTORY[-2:]) if HISTORY else 'family adventure')
    sims = cosine_similarity(V.transform([q]), M).flatten()
    ranked = sorted(list(enumerate(sims)), key=lambda x: x[1], reverse=True)[:k]
    out=[]
    for idx, score in ranked:
        item = dict(CATALOG[idx])
        item['score'] = round(float(score),3)
        item['explanation'] = f"Matched your search for '{query}'" if query else (f"Because you watched {HISTORY[-1]}" if HISTORY else 'Popular pick')
        out.append(item)
    return out

def watch(title: str):
    HISTORY.append(title)
    return {'history': HISTORY}
