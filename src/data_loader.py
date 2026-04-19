"""Loads and cleans the song dataset from songs.csv."""

import csv
from src.models import Song


def load_songs(path: str) -> list[Song]:
    """
    Read songs.csv and return a list of Song objects.

    Strips leading/trailing whitespace from all string fields.
    Skips rows with empty genre or mood_tag (malformed data).
    """
    songs: list[Song] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            genre = row["genre"].strip()
            mood_tag = row["mood_tag"].strip()

            if not genre or not mood_tag:
                continue  # skip the 2 blank/malformed rows in the dataset

            try:
                songs.append(
                    Song(
                        song_id=int(row["song_id"]),
                        title=row["title"].strip(),
                        artist=row["artist"].strip(),
                        genre=genre,
                        mood_tag=mood_tag,
                        bpm=float(row["bpm"]),
                        musical_key=row["musical_key"].strip(),
                        camelot_key=row["camelot_key"].strip(),
                        energy=float(row["energy"]),
                        valence=float(row["valence"]),
                    )
                )
            except (ValueError, KeyError):
                continue  # skip rows with unparseable numeric fields

    return songs
