"""Data models for TempoWave AI."""

from dataclasses import dataclass


@dataclass
class Song:
    """Represents one song loaded from songs.csv."""

    song_id: int
    title: str
    artist: str
    genre: str
    mood_tag: str
    bpm: float
    musical_key: str
    camelot_key: str
    energy: float   # 1–10 scale (curated)
    valence: float  # 1–10 scale (curated)
