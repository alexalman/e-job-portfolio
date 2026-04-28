from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CATALOG = json.loads((Path(__file__).resolve().parent.parent / 'data' / 'catalog.json').read_text())
VECTORIZER = TfidfVectorizer()
MATRIX = VECTORIZER.fit_transform([x['tags'] + ' ' + x['title'] for x in CATALOG])


def recommend(seed_interest: str, top_k: int = 4) -> Dict:
    q = VECTORIZER.transform([seed_interest])
    sims = cosine_similarity(q, MATRIX).flatten()
    ranked = sorted(list(enumerate(sims)), key=lambda x: x[1], reverse=True)[:top_k]
    results: List[Dict] = []
    has_premium = False
    for idx, score in ranked:
        item = dict(CATALOG[idx])
        item['score'] = round(float(score), 3)
        item['why'] = f"Matches your interest in {seed_interest}."
        if item['type'] == 'premium':
            has_premium = True
        results.append(item)
    upgrade = None
    if has_premium:
        upgrade = {
            'message': f'Upgrade to Paramount+ to unlock premium titles that best match {seed_interest}.',
            'offer': '7-day trial + premium recommendations',
        }
    churn = {
        'risk_level': 'medium' if 'sports' not in seed_interest.lower() else 'low',
        'reason': 'User is engaging with a narrow cluster of content; broaden recommendations with one premium bridge title.'
    }
    return {'interest': seed_interest, 'results': results, 'upgrade_prompt': upgrade, 'churn': churn}
