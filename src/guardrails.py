"""Input validation and guardrails for TempoWave AI."""

from src.config import VALID_GENRES, VALID_MOODS, VALID_COUNTS
from src.models import Song


class GuardrailError(Exception):
    """Raised when a request fails a validation check."""


def validate_request(genre: str, mood: str, count: int) -> None:
    """
    Validate genre, mood, and count against allowed values.
    Raises GuardrailError with a clear message on failure.
    """
    if genre not in VALID_GENRES:
        raise GuardrailError(
            f"Invalid genre '{genre}'. Choose from: {', '.join(VALID_GENRES)}"
        )
    if mood not in VALID_MOODS:
        raise GuardrailError(
            f"Invalid mood '{mood}'. Choose from: {', '.join(VALID_MOODS)}"
        )
    if count not in VALID_COUNTS:
        raise GuardrailError(
            f"Invalid count '{count}'. Choose from: {VALID_COUNTS}"
        )


def validate_pool(songs: list[Song], count: int, genre: str, mood: str) -> None:
    """
    Confirm the filtered pool has at least `count` songs.
    Raises GuardrailError if not enough songs are available.
    """
    if len(songs) < count:
        raise GuardrailError(
            f"Not enough songs for {genre} / {mood}. "
            f"Requested {count}, but only {len(songs)} available in this bucket."
        )
