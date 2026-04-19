"""Composite transition scoring for playlist sequencing."""

from src.models import Song
from src.harmonic import camelot_score
from src.config import MOOD_WEIGHTS


def bpm_score(bpm1: float, bpm2: float) -> float:
    """
    Score BPM closeness on [0.0, 1.0].
    0 BPM difference → 1.0; 40+ BPM difference → 0.0.
    """
    diff = abs(bpm1 - bpm2)
    return max(0.0, 1.0 - diff / 40.0)


def energy_transition_score(current: float, candidate: float, mood: str) -> float:
    """
    Score an energy transition based on mood intent.

    - Workout: rewards rising/maintaining energy; penalises drops
    - Chill:   rewards smooth flow (small deltas in either direction)
    - Vibe:    rewards moderate movement; penalises large jumps
    """
    diff = candidate - current      # positive = going up
    abs_diff = abs(diff)

    if mood == "Workout":
        if diff >= 0:
            return 1.0
        # Drops are penalised: -1 → 0.75, -2 → 0.50, -4 → 0.0
        return max(0.0, 1.0 + diff / 4.0)

    elif mood == "Chill":
        # Any delta up to 5 is acceptable; beyond that tails off
        return max(0.0, 1.0 - abs_diff / 5.0)

    else:  # Vibe
        return max(0.0, 1.0 - abs_diff / 7.0)


def valence_score(valence1: float, valence2: float) -> float:
    """
    Score valence smoothness on [0.0, 1.0].
    Prefers small valence jumps between consecutive songs.
    """
    diff = abs(valence1 - valence2)
    return max(0.0, 1.0 - diff / 9.0)


def score_transition(current: Song, candidate: Song, mood: str) -> float:
    """
    Compute a weighted composite score for the transition current → candidate.

    Returns a float in [0.0, 1.0]. Higher is a better follow-on song.
    Weights are drawn from MOOD_WEIGHTS[mood].
    """
    w = MOOD_WEIGHTS[mood]

    h = camelot_score(current.camelot_key, candidate.camelot_key)
    b = bpm_score(current.bpm, candidate.bpm)
    e = energy_transition_score(current.energy, candidate.energy, mood)
    v = valence_score(current.valence, candidate.valence)

    return w["harmonic"] * h + w["bpm"] * b + w["energy"] * e + w["valence"] * v
