"""Tests for src/guardrails.py"""

import pytest
from src.models import Song
from src.guardrails import validate_request, validate_pool, GuardrailError


def make_song(song_id: int) -> Song:
    return Song(
        song_id=song_id, title=f"Song {song_id}", artist="Test",
        genre="Rap", mood_tag="Workout", bpm=120.0, musical_key="C Major",
        camelot_key="8B", energy=7.0, valence=5.0,
    )


# ── validate_request ───────────────────────────────────────────────

def test_valid_request_does_not_raise():
    validate_request("Rap", "Workout", 10)  # must not raise
    validate_request("EDM", "Chill", 5)
    validate_request("Pop", "Vibe", 15)


def test_invalid_genre_raises():
    with pytest.raises(GuardrailError, match="genre"):
        validate_request("Jazz", "Workout", 10)


def test_invalid_mood_raises():
    with pytest.raises(GuardrailError, match="mood"):
        validate_request("Rap", "Party", 10)


def test_invalid_count_raises():
    with pytest.raises(GuardrailError, match="count"):
        validate_request("Rap", "Workout", 7)


def test_count_zero_raises():
    with pytest.raises(GuardrailError, match="count"):
        validate_request("EDM", "Vibe", 0)


# ── validate_pool ──────────────────────────────────────────────────

def test_pool_exact_count_passes():
    songs = [make_song(i) for i in range(5)]
    validate_pool(songs, 5, "Rap", "Workout")  # must not raise


def test_pool_more_than_enough_passes():
    songs = [make_song(i) for i in range(20)]
    validate_pool(songs, 10, "EDM", "Chill")


def test_pool_not_enough_raises():
    songs = [make_song(i) for i in range(3)]
    with pytest.raises(GuardrailError, match="Not enough"):
        validate_pool(songs, 5, "Rap", "Workout")


def test_pool_empty_raises():
    with pytest.raises(GuardrailError):
        validate_pool([], 5, "Pop", "Vibe")
