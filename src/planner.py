"""
Greedy playlist builder — the core AI algorithm of TempoWave.

Agentic workflow (observable via verbose=True):
  1. Load candidates (already filtered by genre + mood)
  2. Select opening song based on mood energy anchor
  3. Score every remaining candidate against the current last song
  4. Pick the highest-scoring candidate
  5. Append to playlist and remove from pool
  6. Repeat steps 3–5 until the requested count is reached
"""

from src.models import Song
from src.scoring import score_transition
from src.harmonic import camelot_score


# -------------------------------------------------------------------
# Opening song selection
# -------------------------------------------------------------------

def _select_first_song(candidates: list[Song], mood: str) -> Song:
    """
    Choose the opening song based on mood intent.

    - Workout: highest energy song (momentum from the start)
    - Chill:   lowest energy song that is still >= 2 (ease in gently)
    - Vibe:    song closest to the median energy (balanced anchor)
    """
    if mood == "Workout":
        return max(candidates, key=lambda s: s.energy)

    elif mood == "Chill":
        valid = [s for s in candidates if s.energy >= 2]
        pool = valid if valid else candidates
        return min(pool, key=lambda s: s.energy)

    else:  # Vibe
        sorted_energies = sorted(s.energy for s in candidates)
        median = sorted_energies[len(sorted_energies) // 2]
        return min(candidates, key=lambda s: abs(s.energy - median))


# -------------------------------------------------------------------
# Transition reason summary (used internally by planner)
# -------------------------------------------------------------------

def _build_reason(prev: Song, chosen: Song, mood: str) -> str:
    """Return a compact human-readable reason for choosing `chosen` after `prev`."""
    parts = []

    h = camelot_score(prev.camelot_key, chosen.camelot_key)
    if h >= 1.0:
        parts.append("same key")
    elif h >= 0.8:
        parts.append("compatible key")

    bpm_diff = abs(prev.bpm - chosen.bpm)
    if bpm_diff <= 5:
        parts.append("matching tempo")
    elif bpm_diff <= 15:
        parts.append("close tempo")

    energy_diff = chosen.energy - prev.energy
    if mood == "Workout" and energy_diff >= 0:
        parts.append("maintains/builds energy")
    elif mood == "Chill" and abs(energy_diff) <= 2:
        parts.append("smooth energy flow")
    elif mood == "Vibe":
        parts.append("balanced energy")

    return ", ".join(parts) if parts else "best available transition"


# -------------------------------------------------------------------
# Main playlist builder
# -------------------------------------------------------------------

def build_playlist(
    songs: list[Song],
    mood: str,
    count: int,
    verbose: bool = False,
) -> list[tuple[Song, float, str]]:
    """
    Build an ordered playlist of `count` songs using greedy scoring.

    Returns a list of (Song, transition_score, reason) tuples.
    The first entry always has score=1.0 (opening anchor).

    Set verbose=True to print step-by-step planning output.
    """
    if verbose:
        print(f"\n[PLANNER] Building {count}-song '{mood}' playlist "
              f"from {len(songs)} candidates")

    remaining = list(songs)
    playlist: list[tuple[Song, float, str]] = []

    # ── Step 1: opening song ──────────────────────────────────────
    first = _select_first_song(remaining, mood)
    remaining.remove(first)
    playlist.append((first, 1.0, "opening track — mood energy anchor"))

    if verbose:
        print(f"  [OPEN] '{first.title}' — {first.artist} "
              f"| energy={first.energy}  BPM={first.bpm:.0f}  key={first.camelot_key}")

    # ── Steps 2–N: greedy selection ───────────────────────────────
    while len(playlist) < count:
        current = playlist[-1][0]

        if verbose:
            print(f"\n  [SCORE] Evaluating {len(remaining)} candidates "
                  f"after '{current.title}'...")

        scored = sorted(
            remaining,
            key=lambda c: score_transition(current, c, mood),
            reverse=True,
        )
        best = scored[0]
        best_score = score_transition(current, best, mood)
        reason = _build_reason(current, best, mood)

        playlist.append((best, best_score, reason))
        remaining.remove(best)

        if verbose:
            print(f"  [PICK] '{best.title}' — {best.artist} "
                  f"| score={best_score:.3f}  energy={best.energy}  "
                  f"BPM={best.bpm:.0f}  key={best.camelot_key}")
            print(f"         reason: {reason}")

    if verbose:
        print(f"\n[PLANNER] Done — {count} songs selected.")

    return playlist
