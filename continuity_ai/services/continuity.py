"""ContinuityAI — deterministic demo service.

Runs without external API keys so the project works out of the box for portfolio viewers.
Swap analyze_frame_pair() for the Claude Vision version in production (see README).
"""
from __future__ import annotations
import hashlib
import random
from dataclasses import dataclass, asdict, field


ERROR_TEMPLATES = [
    ('prop_state',       'high',   'Coffee cup moved from right hand to left hand across cut', True,
     'Rotoscope cup to original position in Frame B'),
    ('prop_state',       'high',   'Whiskey glass fill level jumps from 40% to 80% across dialogue cut', True,
     'Digital paint to match fill level'),
    ('lighting',         'medium', 'Shadow direction inconsistent with established sun position (~40 degrees off)', True,
     'Relight pass to match previous shot direction'),
    ('lighting',         'low',    'Subtle color cast shift between wide and close-up coverage', True,
     'Color grade correction'),
    ('costume',          'medium', 'Jacket lapel folded differently across the cut', False,
     'Reshoot flagged; otherwise accept as drift'),
    ('background_extra', 'high',   'Background extra reappears in frame after exiting earlier in the same take', True,
     'Paint out extra in Frame B or composite clean plate'),
    ('makeup',           'high',   'Wound makeup missing on actor left arm in reverse angle', True,
     'Compositing restore wound detail'),
    ('environmental',    'medium', 'Rain visible on window in close-up, absent in matching wide shot', True,
     'Add digital rain layer to wide or remove from close-up'),
    ('screen_direction', 'medium', 'Character exits frame left then enters frame left in next shot (crosses the line)', False,
     'Editorial decision: accept or flip shot'),
    ('other',            'low',    'Minor hair drift across multi-day shoot detectable frame-by-frame', False,
     'Acceptable continuity drift'),
]


@dataclass
class ContinuityError:
    type: str
    severity: str
    description: str
    fixable: bool
    fix_suggestion: str


@dataclass
class ShotAnalysis:
    shot_index: int
    timecode_a: str
    timecode_b: str
    match_score: int
    errors: list = field(default_factory=list)
    summary: str = ''
    auto_fixable_count: int = 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d['errors'] = [asdict(e) if not isinstance(e, dict) else e for e in self.errors]
        d['high_count'] = sum(1 for e in self.errors if (e.severity if not isinstance(e, dict) else e['severity']) == 'high')
        d['medium_count'] = sum(1 for e in self.errors if (e.severity if not isinstance(e, dict) else e['severity']) == 'medium')
        d['low_count'] = sum(1 for e in self.errors if (e.severity if not isinstance(e, dict) else e['severity']) == 'low')
        return d


def _seed_from(text: str) -> int:
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


def _tc(shot_index: int, variant: str) -> str:
    """Generate SMPTE-style timecode for demo display."""
    total_sec = shot_index * 8 + (12 if variant == 'B' else 0)
    return f'01:{total_sec // 60:02d}:{total_sec % 60:02d}:{0 if variant == "A" else 12:02d}'


def analyze_frame_pair(frame_a_desc: str, frame_b_desc: str, shot_index: int = 0) -> dict:
    """Deterministic analysis of a described frame pair.

    Uses descriptions as seeds to produce consistent results across runs.
    Swap for Claude Vision API in production (see README).
    """
    combined = f'{frame_a_desc}|{frame_b_desc}|{shot_index}'
    rng = random.Random(_seed_from(combined))

    n_errors = rng.choices([0, 1, 2, 3], weights=[3, 4, 2, 1])[0]
    base_score = 95 - (n_errors * 12) - rng.randint(0, 8)
    base_score = max(25, min(98, base_score))

    errors = []
    chosen = rng.sample(ERROR_TEMPLATES, min(n_errors, len(ERROR_TEMPLATES)))
    for e_type, sev, desc, fixable, fix in chosen:
        errors.append(ContinuityError(
            type=e_type,
            severity=sev,
            description=desc,
            fixable=fixable,
            fix_suggestion=fix,
        ))

    high_errors = [e for e in errors if e.severity == 'high']
    if high_errors:
        summary = f'{len(high_errors)} high-severity error(s) detected — priority for VFX patch queue.'
    elif errors:
        summary = f'{len(errors)} minor continuity drift(s) detected — manageable in edit.'
    else:
        summary = 'Clean shot pair — no continuity errors detected.'

    analysis = ShotAnalysis(
        shot_index=shot_index,
        timecode_a=_tc(shot_index, 'A'),
        timecode_b=_tc(shot_index, 'B'),
        match_score=base_score,
        errors=errors,
        summary=summary,
        auto_fixable_count=sum(1 for e in errors if e.fixable),
    )
    return analysis.to_dict()


def classify_episode(shot_analyses: list) -> dict:
    """Aggregate per-shot analyses into an episode-level report."""
    total_errors = sum(len(s['errors']) for s in shot_analyses)
    high = sum(s['high_count'] for s in shot_analyses)
    medium = sum(s['medium_count'] for s in shot_analyses)
    low = sum(s['low_count'] for s in shot_analyses)
    fixable = sum(s['auto_fixable_count'] for s in shot_analyses)
    avg_score = sum(s['match_score'] for s in shot_analyses) / max(len(shot_analyses), 1)

    type_counts = {}
    for s in shot_analyses:
        for e in s['errors']:
            type_counts[e['type']] = type_counts.get(e['type'], 0) + 1

    priority = [s['shot_index'] for s in shot_analyses if s['high_count'] > 0 or s['match_score'] < 60]

    return {
        'total_shots': len(shot_analyses),
        'total_errors': total_errors,
        'high_errors': high,
        'medium_errors': medium,
        'low_errors': low,
        'auto_fixable': fixable,
        'avg_match_score': round(avg_score, 1),
        'priority_shots': priority,
        'error_type_breakdown': type_counts,
        'estimated_hours_saved': len(shot_analyses) * 0.5,
        'cost_savings_estimate': len(shot_analyses) * 0.5 * 200,
        'shots': shot_analyses,
    }


def build_demo_report() -> dict:
    """Build a rich demo report with 10 pre-analyzed shot pairs for the UI."""
    demo_descriptions = [
        ('Actor at desk with coffee cup in right hand, morning light',       'Same actor, coffee cup now in left hand'),
        ('Wide exterior establishing shot of suburban street, sunny',         'Same street moments later, slight shadow shift'),
        ('Medium shot of dinner table with full wine glass',                 'Same table, wine glass noticeably lower'),
        ('Close-up of character face during dialogue, neutral expression',    'Same character in reverse angle, matching expression'),
        ('Interior bar scene, patron in background wearing red jacket',       'Same bar, background patron now appears to the left'),
        ('Character bleeding from cut on left arm, close-up',                 'Reverse angle of same character, wound not visible on arm'),
        ('Office window showing heavy rain outside, tight shot',              'Wide shot of same office, no rain visible through window'),
        ('Hero walks exit frame left, action sequence',                       'Next shot, hero enters frame left — continuity crossed'),
        ('Candle lit on table, flame vertical, half burned',                  'Same candle later, noticeably shorter'),
        ('Car parked on street, clean windshield',                            'Same car, windshield now has water droplets'),
    ]

    shots = []
    for i, (a, b) in enumerate(demo_descriptions):
        shots.append(analyze_frame_pair(a, b, i))

    report = classify_episode(shots)
    report['generated_for'] = 'ContinuityAI Demo Episode'
    return report
