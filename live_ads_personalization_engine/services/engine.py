from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List

DATA = json.loads((Path(__file__).resolve().parent.parent / 'data' / 'ads.json').read_text())


def simulate_plan(segment: str, context: str, slots: int = 5) -> Dict:
    eligible = [a for a in DATA if a['segment'] == segment] or DATA
    plan: List[Dict] = []
    for i in range(1, slots + 1):
        ad = eligible[(i - 1) % len(eligible)]
        plan.append({
            'slot': i,
            'moment': f'{context} break {i}',
            'brand': ad['brand'],
            'creative': ad['creative'],
            'cta': ad['cta'],
            'rationale': f'Selected for {segment} during {context} based on contextual relevance and fatigue control.'
        })
    return {
        'segment': segment,
        'context': context,
        'slots': plan,
        'forecast': {
            'attention_index': '118',
            'predicted_recall': '31%',
            'frequency_cap': 2,
            'summary': f'This plan prioritizes relevance for {segment} while rotating creatives to reduce repetition during {context}.'
        }
    }
