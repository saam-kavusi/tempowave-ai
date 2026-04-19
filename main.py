#!/usr/bin/env python3
"""
TempoWave AI — CLI entry point.

Usage (interactive):
    python3 main.py

Usage (flags):
    python3 main.py --genre Rap   --mood Workout --count 10
    python3 main.py --genre EDM   --mood Chill   --count 5  --verbose
    python3 main.py --genre Pop   --mood Vibe    --count 15 --no-export

Genre and mood inputs are case-insensitive in both modes.
"""

import argparse

from src.config import DATA_PATH, VALID_GENRES, VALID_MOODS, VALID_COUNTS
from src.data_loader import load_songs
from src.filters import filter_songs
from src.guardrails import validate_request, validate_pool, GuardrailError
from src.planner import build_playlist
from src.explainer import explain_playlist
from src.exporter import export_playlist


# ── Normalization maps ─────────────────────────────────────────────
# Strip + lowercase the user input, then look up the canonical form.
# This avoids .title() producing "Edm" instead of "EDM".

GENRE_MAP = {
    "rap": "Rap",
    "edm": "EDM",
    "pop": "Pop",
}

MOOD_MAP = {
    "workout": "Workout",
    "chill":   "Chill",
    "vibe":    "Vibe",
}


# ── Argument-type helpers (used by argparse --genre / --mood) ──────

def _normalize_genre(value: str) -> str:
    """Normalize genre from CLI flag; raises ArgumentTypeError if invalid."""
    normalized = GENRE_MAP.get(value.strip().lower())
    if normalized is None:
        raise argparse.ArgumentTypeError(
            f"'{value}' is not valid. Choose from: {', '.join(VALID_GENRES)}"
        )
    return normalized


def _normalize_mood(value: str) -> str:
    """Normalize mood from CLI flag; raises ArgumentTypeError if invalid."""
    normalized = MOOD_MAP.get(value.strip().lower())
    if normalized is None:
        raise argparse.ArgumentTypeError(
            f"'{value}' is not valid. Choose from: {', '.join(VALID_MOODS)}"
        )
    return normalized


# ── Argument parsing ───────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TempoWave AI Playlist Generator")
    parser.add_argument("--genre",     type=_normalize_genre,          help="Music genre")
    parser.add_argument("--mood",      type=_normalize_mood,           help="Playlist mood")
    parser.add_argument("--count",     type=int, choices=VALID_COUNTS, help="Number of songs")
    parser.add_argument("--verbose",   action="store_true",            help="Show step-by-step planning")
    parser.add_argument("--no-export", action="store_true",            help="Skip CSV export")
    return parser.parse_args()


# ── Interactive prompt ─────────────────────────────────────────────

def _prompt_user() -> tuple[str, str, int]:
    """
    Interactive mode: re-prompt each field until a valid value is entered.
    Genre is locked in before mood is asked; mood is locked in before count.
    Never calls sys.exit — bad input just loops.
    """
    print("\n=== TempoWave AI ===")

    # ── Genre loop ────────────────────────────────────────────────
    genre: str | None = None
    while genre is None:
        print(f"Available genres : {', '.join(VALID_GENRES)}")
        raw = input("Genre           : ").strip()
        genre = GENRE_MAP.get(raw.lower())
        if genre is None:
            print(f"  ✗ '{raw}' is not valid. Choose from: {', '.join(VALID_GENRES)}")

    # ── Mood loop ─────────────────────────────────────────────────
    mood: str | None = None
    while mood is None:
        print(f"Available moods  : {', '.join(VALID_MOODS)}")
        raw = input("Mood            : ").strip()
        mood = MOOD_MAP.get(raw.lower())
        if mood is None:
            print(f"  ✗ '{raw}' is not valid. Choose from: {', '.join(VALID_MOODS)}")

    # ── Count loop ────────────────────────────────────────────────
    count_choices_str = ", ".join(str(c) for c in VALID_COUNTS)
    count: int | None = None
    while count is None:
        print(f"Song counts      : {VALID_COUNTS}")
        raw = input("Number of songs : ").strip()
        try:
            parsed = int(raw)
        except ValueError:
            print(f"  ✗ '{raw}' is not valid. Choose from: {count_choices_str}")
            continue
        if parsed in VALID_COUNTS:
            count = parsed
        else:
            print(f"  ✗ '{raw}' is not valid. Choose from: {count_choices_str}")

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
    for i, (song, _, _) in enumerate(playlist, start=1):
        print(f"  {i:2d}.  {song.title} — {song.artist}")
        print(f"        BPM {song.bpm:.0f}  |  key {song.camelot_key}"
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

    if args.genre is not None and args.mood is not None and args.count is not None:
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
