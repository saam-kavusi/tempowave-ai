"""
TempoWave AI — Evaluation Script

Runs three predefined playlist requests (demo cases) and one guardrail
failure test, then prints a clean summary report.

Run from the repo root:
    python evaluation/run_eval.py
"""

import os
import sys

# Ensure the repo root is on sys.path so `src` imports resolve.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import DATA_PATH
from src.data_loader import load_songs
from src.filters import filter_songs
from src.guardrails import validate_request, validate_pool, GuardrailError
from src.planner import build_playlist
from src.harmonic import camelot_score


# ── Evaluation cases ───────────────────────────────────────────────

DEMO_CASES = [
    {"genre": "Rap", "mood": "Workout", "count": 10},
    {"genre": "EDM", "mood": "Chill",   "count": 5},
    {"genre": "Pop", "mood": "Vibe",    "count": 15},
]

GUARDRAIL_CASES = [
    ("Jazz",   "Workout", 10),  # invalid genre
    ("Rap",    "Party",   10),  # invalid mood
    ("EDM",    "Chill",   20),  # invalid count
]


# ── Metrics ────────────────────────────────────────────────────────

def avg_transition_score(playlist: list[tuple]) -> float:
    """Average transition score across songs 2–N (song 1 has no predecessor)."""
    scores = [score for _, score, _ in playlist[1:]]
    return sum(scores) / len(scores) if scores else 0.0


def harmonic_compat_pct(playlist: list[tuple]) -> float:
    """Percentage of adjacent pairs with harmonic score >= 0.8."""
    songs = [s for s, _, _ in playlist]
    if len(songs) <= 1:
        return 100.0
    compatible = sum(
        1 for i in range(1, len(songs))
        if camelot_score(songs[i - 1].camelot_key, songs[i].camelot_key) >= 0.8
    )
    return compatible / (len(songs) - 1) * 100


def energy_flow_summary(playlist: list[tuple], mood: str) -> str:
    """Describe how energy moves through the playlist."""
    energies = [s.energy for s, _, _ in playlist]
    if mood == "Workout":
        non_drops = sum(1 for i in range(1, len(energies)) if energies[i] >= energies[i - 1])
        return f"{non_drops}/{len(energies) - 1} transitions maintain or rise"
    elif mood == "Chill":
        smooth = sum(1 for i in range(1, len(energies)) if abs(energies[i] - energies[i - 1]) <= 2)
        return f"{smooth}/{len(energies) - 1} transitions within ±2 energy"
    else:
        return f"range {min(energies):.0f}–{max(energies):.0f} (Vibe)"


# ── Runner ─────────────────────────────────────────────────────────

def _trunc(text: str, width: int) -> str:
    """Truncate `text` to `width` characters, appending '…' if clipped."""
    if len(text) <= width:
        return text
    return text[: width - 1] + "…"


def run_demo_cases(all_songs: list) -> None:
    bar = "=" * 62

    for case in DEMO_CASES:
        genre, mood, count = case["genre"], case["mood"], case["count"]
        print(f"\n{bar}")
        print(f"  CASE: {genre} / {mood} / {count} songs")
        print(bar)

        try:
            validate_request(genre, mood, count)
            pool = filter_songs(all_songs, genre, mood)
            validate_pool(pool, count, genre, mood)
        except GuardrailError as e:
            print(f"  [GUARDRAIL] {e}")
            continue

        playlist = build_playlist(pool, mood, count, verbose=False)

        avg  = avg_transition_score(playlist)
        compat = harmonic_compat_pct(playlist)
        flow   = energy_flow_summary(playlist, mood)

        print(f"  Pool size       : {len(pool)} songs available")
        print(f"  Avg transition  : {avg:.3f} / 1.000")
        print(f"  Harmonic compat : {compat:.0f}% of pairs ≥ 0.8")
        print(f"  Energy flow     : {flow}")
        print()
        print(f"  {'#':>3}  {'Score':>7}  {'Title':<35}  {'Artist':<25}  E  BPM  Key")
        print(f"  {'-'*3}  {'-'*7}  {'-'*35}  {'-'*25}  -  ---  ---")
        for i, (song, score, _) in enumerate(playlist, start=1):
            score_str = "[open]" if i == 1 else f"{score:.3f}"
            title  = _trunc(song.title,  35)
            artist = _trunc(song.artist, 25)
            print(
                f"  {i:>3}  {score_str:>7}  {title:<35}  {artist:<25}"
                f"  {song.energy:.0f}  {song.bpm:>3.0f}  {song.camelot_key}"
            )


def run_guardrail_cases() -> None:
    print(f"\n{'=' * 62}")
    print("  GUARDRAIL TESTS")
    print(f"{'=' * 62}")
    for genre, mood, count in GUARDRAIL_CASES:
        try:
            validate_request(genre, mood, count)
            print(f"  {genre}/{mood}/{count:<3} : (no error — unexpected)")
        except GuardrailError as e:
            print(f"  {genre}/{mood}/{count:<3} : BLOCKED → {e}")


# ── Main ───────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 62)
    print("  TempoWave AI — Evaluation Run")
    print("=" * 62)

    all_songs = load_songs(DATA_PATH)
    print(f"\n  Dataset loaded: {len(all_songs)} songs from '{DATA_PATH}'")

    run_demo_cases(all_songs)
    run_guardrail_cases()

    print(f"\n{'=' * 62}")
    print("  Evaluation complete.")
    print("=" * 62)


if __name__ == "__main__":
    main()
