"""Tests for src/filters.py"""

import pytest
from src.models import Song
from src.filters import filter_songs


def make_song(song_id: int, genre: str, mood: str) -> Song:
    return Song(
        song_id=song_id, title=f"Song {song_id}", artist="Test Artist",
        genre=genre, mood_tag=mood, bpm=120.0, musical_key="C Major",
        camelot_key="8B", energy=7.0, valence=5.0,
    )


SONGS = [
    make_song(1, "Rap", "Workout"),
    make_song(2, "Rap", "Chill"),
    make_song(3, "Rap", "Workout"),
    make_song(4, "EDM", "Workout"),
    make_song(5, "Pop", "Vibe"),
    make_song(6, "EDM", "Chill"),
]


def test_filter_returns_correct_songs():
    result = filter_songs(SONGS, "Rap", "Workout")
    assert len(result) == 2
    assert all(s.genre == "Rap" and s.mood_tag == "Workout" for s in result)


def test_filter_no_match_returns_empty():
    result = filter_songs(SONGS, "Pop", "Workout")
    assert result == []


def test_filter_single_match():
    result = filter_songs(SONGS, "Pop", "Vibe")
    assert len(result) == 1
    assert result[0].song_id == 5


def test_filter_edm_chill():
    result = filter_songs(SONGS, "EDM", "Chill")
    assert len(result) == 1
    assert result[0].song_id == 6


def test_filter_case_insensitive():
    result = filter_songs(SONGS, "rap", "workout")
    assert len(result) == 2


def test_filter_does_not_cross_genres():
    rap_songs = filter_songs(SONGS, "Rap", "Workout")
    assert all(s.genre == "Rap" for s in rap_songs)


def test_filter_empty_input():
    assert filter_songs([], "Rap", "Workout") == []
