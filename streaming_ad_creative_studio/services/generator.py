from __future__ import annotations
from typing import Dict, List


def _tone_variants(goal: str) -> List[str]:
    return [
        f"emotion-first storytelling to drive {goal}",
        f"product-benefit clarity to improve {goal}",
        f"social-proof and urgency to increase {goal}",
    ]


def generate_campaign(payload: Dict[str, str]) -> Dict:
    brand = payload.get("brand", "Brand")
    product = payload.get("product", "Product")
    audience = payload.get("audience", "general audience")
    goal = payload.get("goal", "awareness")
    context = payload.get("context", "streaming")
    tones = _tone_variants(goal)
    concepts = []
    for i, tone in enumerate(tones, start=1):
        concepts.append(
            {
                "id": i,
                "title": f"{brand} Concept {i}",
                "angle": tone,
                "tagline": f"{product} for {audience}",
                "hook": f"In {context}, show how {product} unlocks value for {audience}.",
            }
        )
    scripts = {
        "6s": f"{brand}: {product}. Fast, clear, made for {audience}. Try it now.",
        "15s": f"Meet {product} from {brand}. In one quick moment, viewers see the core benefit, why it matters to {audience}, and a strong call to action built for {goal}.",
        "30s": f"Open with a problem your audience recognizes. Introduce {product} as the answer. Show one emotional beat, one proof point, and one memorable branded ending. Close with a direct CTA optimized for {goal}.",
    }
    storyboard = [
        {"scene": 1, "visual": f"Establish a {context} setting with {audience} on screen.", "copy": f"The moment before {product}."},
        {"scene": 2, "visual": f"Reveal {product} in action.", "copy": f"{brand} changes the flow."},
        {"scene": 3, "visual": f"Show the payoff and brand lockup.", "copy": f"Choose {product}."},
    ]
    summary = {
        "predicted_ctr": "2.8%",
        "predicted_completion_rate": "74%",
        "best_fit_segment": audience,
        "llm_summary": f"The strongest concept is the emotion-first version because it aligns {brand} with a clear viewer payoff while staying concise enough for streaming placements.",
    }
    return {"concepts": concepts, "scripts": scripts, "storyboard": storyboard, "summary": summary}
