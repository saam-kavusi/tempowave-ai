"""Exports a finished playlist to a timestamped CSV file."""

import csv
import os
from datetime import datetime

from src.models import Song


def export_playlist(
    playlist: list[tuple],
    genre: str,
    mood: str,
    output_dir: str = "output",
) -> str:
    """
    Write the playlist to a CSV file inside `output_dir`.

    `playlist` is a list of (Song, transition_score, reason) tuples.
    Returns the path of the written file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"playlist_{genre}_{mood}_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "position", "song_id", "title", "artist",
            "genre", "mood_tag", "bpm", "musical_key", "camelot_key",
            "energy", "valence", "transition_score", "reason",
        ])
        for position, (song, score, reason) in enumerate(playlist, start=1):
            writer.writerow([
                position,
                song.song_id,
                song.title,
                song.artist,
                song.genre,
                song.mood_tag,
                f"{song.bpm:.1f}",
                song.musical_key,
                song.camelot_key,
                song.energy,
                song.valence,
                f"{score:.4f}",
                reason,
            ])

    return filepath
