"""Filters the song pool by genre and mood."""

from src.models import Song


def filter_songs(songs: list[Song], genre: str, mood: str) -> list[Song]:
    """
    Return songs that exactly match the requested genre and mood_tag.
    Comparison is case-insensitive to tolerate minor data inconsistencies.
    """
    genre_lower = genre.lower()
    mood_lower = mood.lower()
    return [
        s for s in songs
        if s.genre.lower() == genre_lower and s.mood_tag.lower() == mood_lower
    ]
