"""Tests for src/planner.py"""

import pytest
from src.models import Song
from src.planner import build_playlist, _select_first_song


def make_song(song_id: int, energy: float, bpm: float = 120.0,
              camelot: str = "8B", valence: float = 5.0) -> Song:
    return Song(
        song_id=song_id,
        title=f"Song {song_id}",
        artist=f"Artist {song_id}",
        genre="Rap",
        mood_tag="Workout",
        bpm=bpm,
        musical_key="C Major",
        camelot_key=camelot,
        energy=energy,
        valence=valence,
    )


# 19 distinct songs with ascending energy 1–19
SONGS = [make_song(i, energy=float(i), bpm=100.0 + i * 2) for i in range(1, 20)]


# ── build_playlist ─────────────────────────────────────────────────

def test_playlist_correct_count():
    result = build_playlist(SONGS, "Workout", 5)
    assert len(result) == 5


def test_playlist_count_10():
    result = build_playlist(SONGS, "Chill", 10)
    assert len(result) == 10


def test_no_repeated_songs():
    result = build_playlist(SONGS, "Vibe", 10)
    ids = [s.song_id for s, _, _ in result]
    assert len(ids) == len(set(ids)), "Playlist contains duplicate songs"


def test_returns_correct_tuple_types():
    result = build_playlist(SONGS, "Workout", 5)
    for song, score, reason in result:
        assert isinstance(song, Song)
        assert isinstance(score, float)
        assert isinstance(reason, str)


def test_first_song_score_is_1():
    result = build_playlist(SONGS, "Workout", 5)
    _, first_score, _ = result[0]
    assert first_score == 1.0


def test_all_songs_valid_for_mood():
    for mood in ["Workout", "Chill", "Vibe"]:
        result = build_playlist(SONGS, mood, 5)
        assert len(result) == 5


# ── _select_first_song ─────────────────────────────────────────────

def test_workout_opens_highest_energy():
    first = _select_first_song(SONGS, "Workout")
    assert first.energy == max(s.energy for s in SONGS)


def test_chill_opens_low_energy():
    first = _select_first_song(SONGS, "Chill")
    assert first.energy <= 3.0


def test_vibe_opens_near_median():
    first = _select_first_song(SONGS, "Vibe")
    energies = sorted(s.energy for s in SONGS)
    median = energies[len(energies) // 2]
    # Should be within 2 units of the median
    assert abs(first.energy - median) <= 2.0
