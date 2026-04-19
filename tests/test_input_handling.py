"""Tests for interactive input handling and CLI normalization (main.py)."""

import argparse
import pytest
from unittest.mock import patch

from main import GENRE_MAP, MOOD_MAP, _normalize_genre, _normalize_mood, _prompt_user


# ── GENRE_MAP canonical values ────────────────────────────────────

def test_genre_map_rap():
    assert GENRE_MAP["rap"] == "Rap"


def test_genre_map_edm():
    assert GENRE_MAP["edm"] == "EDM"


def test_genre_map_pop():
    assert GENRE_MAP["pop"] == "Pop"


# ── _normalize_genre ──────────────────────────────────────────────

def test_normalize_genre_lowercase():
    assert _normalize_genre("rap") == "Rap"
    assert _normalize_genre("edm") == "EDM"
    assert _normalize_genre("pop") == "Pop"


def test_normalize_genre_uppercase():
    assert _normalize_genre("RAP") == "Rap"
    assert _normalize_genre("EDM") == "EDM"
    assert _normalize_genre("POP") == "Pop"


def test_normalize_genre_mixed_case():
    assert _normalize_genre("Rap") == "Rap"
    assert _normalize_genre("Edm") == "EDM"


def test_normalize_genre_invalid_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        _normalize_genre("Jazz")


def test_normalize_genre_misspelled_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        _normalize_genre("rpa")


def test_normalize_genre_blank_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        _normalize_genre("")


def test_normalize_genre_symbols_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        _normalize_genre("@@@")


# ── MOOD_MAP canonical values ─────────────────────────────────────

def test_mood_map_workout():
    assert MOOD_MAP["workout"] == "Workout"


def test_mood_map_chill():
    assert MOOD_MAP["chill"] == "Chill"


def test_mood_map_vibe():
    assert MOOD_MAP["vibe"] == "Vibe"


# ── _normalize_mood ───────────────────────────────────────────────

def test_normalize_mood_lowercase():
    assert _normalize_mood("workout") == "Workout"
    assert _normalize_mood("chill") == "Chill"
    assert _normalize_mood("vibe") == "Vibe"


def test_normalize_mood_uppercase():
    assert _normalize_mood("WORKOUT") == "Workout"
    assert _normalize_mood("CHILL") == "Chill"
    assert _normalize_mood("VIBE") == "Vibe"


def test_normalize_mood_mixed_case():
    assert _normalize_mood("Chill") == "Chill"
    assert _normalize_mood("Vibe") == "Vibe"


def test_normalize_mood_invalid_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        _normalize_mood("Party")


def test_normalize_mood_misspelled_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        _normalize_mood("vibez")


def test_normalize_mood_blank_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        _normalize_mood("")


def test_normalize_mood_symbols_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        _normalize_mood("###")


# ── _prompt_user: happy path ──────────────────────────────────────

def test_prompt_user_valid_inputs_all_lowercase():
    """All-lowercase valid entries must normalize and be accepted first try."""
    with patch("builtins.input", side_effect=["rap", "chill", "5"]):
        genre, mood, count = _prompt_user()
    assert genre == "Rap"
    assert mood == "Chill"
    assert count == 5


def test_prompt_user_valid_inputs_uppercase():
    with patch("builtins.input", side_effect=["EDM", "VIBE", "10"]):
        genre, mood, count = _prompt_user()
    assert genre == "EDM"
    assert mood == "Vibe"
    assert count == 10


# ── _prompt_user: invalid genre retries ──────────────────────────

def test_prompt_user_invalid_genre_retries_then_accepts():
    """
    'rpa' must be rejected; genre loop re-asks; 'edm' accepted as EDM.
    Mood and count are only asked after genre succeeds.
    """
    inputs = ["rpa", "edm", "Chill", "5"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert genre == "EDM"
    assert mood == "Chill"
    assert count == 5


def test_prompt_user_blank_genre_retries():
    inputs = ["", "pop", "vibe", "15"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert genre == "Pop"


def test_prompt_user_symbol_genre_retries():
    inputs = ["@@@", "Rap", "Workout", "10"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert genre == "Rap"


# ── _prompt_user: invalid mood retries ───────────────────────────

def test_prompt_user_invalid_mood_retries_then_accepts():
    """
    'party' must be rejected; mood loop re-asks; 'chill' accepted.
    Genre must NOT be re-asked once it was accepted.
    """
    inputs = ["Rap", "party", "chill", "10"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert genre == "Rap"
    assert mood == "Chill"
    assert count == 10


def test_prompt_user_blank_mood_retries():
    inputs = ["edm", "", "vibe", "5"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert mood == "Vibe"


# ── _prompt_user: invalid count retries ──────────────────────────

def test_prompt_user_letters_at_count_retries():
    """Letters at count prompt must be rejected without crashing."""
    inputs = ["Rap", "Workout", "abc", "5"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert count == 5


def test_prompt_user_symbols_at_count_retries():
    """Symbols at count prompt must be rejected without crashing."""
    inputs = ["EDM", "Chill", "@#$", "10"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert count == 10


def test_prompt_user_out_of_range_count_retries():
    """Count outside [5, 10, 15] must be rejected and re-asked."""
    inputs = ["Pop", "Vibe", "1", "20", "15"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert count == 15


def test_prompt_user_blank_count_retries():
    """Blank count entry must be rejected without crashing."""
    inputs = ["Rap", "Workout", "", "5"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert count == 5


def test_prompt_user_full_invalid_sequence():
    """
    Full sequence from Flow 1 in the spec:
    rpa -> edm -> party -> chill -> @ -> 1 -> 5
    """
    inputs = ["rpa", "edm", "party", "chill", "@", "1", "5"]
    with patch("builtins.input", side_effect=inputs):
        genre, mood, count = _prompt_user()
    assert genre == "EDM"
    assert mood == "Chill"
    assert count == 5
