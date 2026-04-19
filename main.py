#!/usr/bin/env python3
"""
TempoWave AI — CLI entry point.

Usage (interactive):
    python main.py

Usage (arguments):
    python main.py --genre Rap   --mood Workout --count 10
    python main.py --genre EDM   --mood Chill   --count 5  --verbose
    python main.py --genre Pop   --mood Vibe    --count 15 --no-export
"""

import argparse
import sys

from src.config import DATA_PATH, VALID_GENRES, VALID_MOODS, VALID_COUNTS
from src.data_loader import load_songs
from src.filters import filter_songs
from src.guardrails import validate_request, validate_pool, GuardrailError
from src.planner import build_playlist
from src.explainer import explain_playlist
from src.exporter import export_playlist


# ── Argument parsing ───────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TempoWave AI Playlist Generator")
    parser.add_argument("--genre",    choices=VALID_GENRES,      help="Music genre")
    parser.add_argument("--mood",     choices=VALID_MOODS,       help="Playlist mood")
    parser.add_argument("--count",    type=int, choices=VALID_COUNTS, help="Number of songs")
    parser.add_argument("--verbose",  action="store_true", help="Show step-by-step planning")
    parser.add_argument("--no-export", action="store_true", help="Skip CSV export")
    return parser.parse_args()


def _prompt_user() -> tuple[str, str, int]:
    """Interactive mode: prompt for genre, mood, and count."""
    print("\n=== TempoWave AI ===")
    print(f"Available genres : {', '.join(VALID_GENRES)}")
    genre = input("Genre           : ").strip()

    print(f"Available moods  : {', '.join(VALID_MOODS)}")
    mood = input("Mood            : ").strip()

    print(f"Song counts      : {VALID_COUNTS}")
    try:
        count = int(input("Number of songs : ").strip())
    except ValueError:
        print("[ERROR] Count must be a number.")
        sys.exit(1)

    return genre, mood, count


# ── Core pipeline ──────────────────────────────────────────────────

def run(
    genre: str,
    mood: str,
    count: int,
    verbose: bool = False,
    export: bool = True,
) -> list[tuple] | None:
    """
    Execute the full TempoWave pipeline.

    Steps:
      1. Load songs from CSV
      2. Validate request inputs
      3. Filter by genre + mood
      4. Validate pool size
      5. Build playlist (greedy, mood-aware)
      6. Display tracklist + transition explanations
      7. Export to CSV (optional)
    """

    # 1. Load
    all_songs = load_songs(DATA_PATH)
    if verbose:
        print(f"[LOAD]   {len(all_songs)} songs loaded from '{DATA_PATH}'")

    # 2. Validate request
    try:
        validate_request(genre, mood, count)
    except GuardrailError as e:
        print(f"\n[GUARDRAIL] {e}\n")
        return None

    # 3. Filter
    pool = filter_songs(all_songs, genre, mood)
    if verbose:
        print(f"[FILTER] {len(pool)} songs match {genre} / {mood}")

    # 4. Validate pool
    try:
        validate_pool(pool, count, genre, mood)
    except GuardrailError as e:
        print(f"\n[GUARDRAIL] {e}\n")
        return None

    # 5. Build
    playlist = build_playlist(pool, mood, count, verbose=verbose)

    # 6. Display tracklist
    bar = "=" * 58
    print(f"\n{bar}")
    print(f"  TempoWave AI  |  {genre}  ·  {mood}  ·  {count} songs")
    print(bar)
    for i, (song, score, _) in enumerate(playlist, start=1):
        score_tag = "[open]" if i == 1 else f"[{score:.3f}]"
        print(f"  {i:2d}. {score_tag:8s}  {song.title} — {song.artist}")
        print(f"            BPM {song.bpm:.0f}  |  key {song.camelot_key}"
              f"  |  energy {song.energy}  |  valence {song.valence}")

    # Transition explanations
    print(f"\n{bar}")
    print("  TRANSITION EXPLANATIONS")
    print(bar)
    print(explain_playlist(playlist))

    # 7. Export
    if export:
        path = export_playlist(playlist, genre, mood)
        print(f"\n[EXPORT] Playlist saved → {path}")

    print()
    return playlist


# ── Entry point ────────────────────────────────────────────────────

def main() -> None:
    args = _parse_args()

    if args.genre and args.mood and args.count:
        genre, mood, count = args.genre, args.mood, args.count
    else:
        genre, mood, count = _prompt_user()

    run(
        genre=genre,
        mood=mood,
        count=count,
        verbose=args.verbose,
        export=not args.no_export,
    )


if __name__ == "__main__":
    main()
