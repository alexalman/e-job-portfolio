from __future__ import annotations
from pathlib import Path
from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont
import uuid


def generate_script(prompt: str) -> str:
    return f"{prompt}. The main character enters a new world, faces a challenge, finds an unexpected ally, and ends with a visually memorable payoff."


def plan_shots(script: str) -> List[str]:
    parts = [p.strip() for p in script.split(',') if p.strip()]
    if not parts: parts = [script]
    return [f"Illustrate: {p}" for p in parts[:4]]


def make_frames(shots: List[str], out_dir: Path) -> List[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    paths=[]
    for i, shot in enumerate(shots, start=1):
        img = Image.new('RGB', (640, 360), (220 - i*20, 210, 245 - i*10))
        d = ImageDraw.Draw(img)
        d.text((20, 20), f"Shot {i}", fill=(10,10,10), font=font)
        d.text((20, 60), shot[:120], fill=(10,10,10), font=font)
        path = out_dir / f'frame_{i}.png'
        img.save(path)
        paths.append(str(path))
    return paths


def run_pipeline(prompt: str, base_dir: Path) -> Dict:
    run_id = str(uuid.uuid4())[:8]
    script = generate_script(prompt)
    shots = plan_shots(script)
    frames = make_frames(shots, base_dir / run_id)
    return {'run_id': run_id, 'script': script, 'shots': shots, 'frames': frames, 'note': 'Frames are placeholders designed for portfolio demos and can be replaced with diffusion outputs later.'}
