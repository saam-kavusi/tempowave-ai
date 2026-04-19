"""Generates human-readable transition explanations for a playlist."""

from src.models import Song
from src.harmonic import camelot_score


def _direction(a: float, b: float) -> str:
    if b > a:
        return "↑"
    if b < a:
        return "↓"
    return "→"


def explain_transition(prev: Song, current: Song, position: int) -> str:
    """Return a multi-line explanation for the transition prev → current."""
    h = camelot_score(prev.camelot_key, current.camelot_key)
    bpm_diff = abs(prev.bpm - current.bpm)

    if h == 1.0:
        key_note = "perfect key match"
    elif h >= 0.8:
        key_note = "harmonically compatible"
    elif h >= 0.5:
        key_note = "moderate compatibility"
    else:
        key_note = "best option available"

    lines = [
        f"  [{position:2d}] \"{current.title}\" — {current.artist}",
        f"       Key:    {prev.camelot_key} → {current.camelot_key}  ({key_note})",
        f"       BPM:    {prev.bpm:.0f} {_direction(prev.bpm, current.bpm)} "
        f"{current.bpm:.0f}  (diff {bpm_diff:.0f})",
        f"       Energy: {prev.energy:.0f} {_direction(prev.energy, current.energy)} "
        f"{current.energy:.0f}",
        f"       Valence:{prev.valence:.0f} {_direction(prev.valence, current.valence)} "
        f"{current.valence:.0f}",
    ]
    return "\n".join(lines)


def explain_playlist(playlist: list[tuple]) -> str:
    """
    Generate a full annotated explanation for every transition in the playlist.

    `playlist` is a list of (Song, score, reason) tuples as returned by build_playlist.
    """
    songs = [s for s, _, _ in playlist]
    lines = [
        f"  [ 1] \"{songs[0].title}\" — {songs[0].artist}  (opening track)",
        f"       Energy: {songs[0].energy:.0f}  BPM: {songs[0].bpm:.0f}  "
        f"Key: {songs[0].camelot_key}",
    ]
    for i in range(1, len(songs)):
        lines.append(explain_transition(songs[i - 1], songs[i], i + 1))
    return "\n".join(lines)
