"""Tests for src/harmonic.py"""

import pytest
from src.harmonic import camelot_score, _parse_camelot


# ── _parse_camelot ─────────────────────────────────────────────────

def test_parse_valid_major():
    assert _parse_camelot("8B") == (8, "B")

def test_parse_valid_minor():
    assert _parse_camelot("3A") == (3, "A")

def test_parse_boundary_low():
    assert _parse_camelot("1B") == (1, "B")

def test_parse_boundary_high():
    assert _parse_camelot("12A") == (12, "A")

def test_parse_empty_returns_none():
    assert _parse_camelot("") is None

def test_parse_single_char_returns_none():
    assert _parse_camelot("A") is None

def test_parse_invalid_letter_returns_none():
    assert _parse_camelot("8C") is None

def test_parse_out_of_range_returns_none():
    assert _parse_camelot("13A") is None


# ── camelot_score ──────────────────────────────────────────────────

def test_same_key_major():
    assert camelot_score("8B", "8B") == 1.0

def test_same_key_minor():
    assert camelot_score("3A", "3A") == 1.0

def test_adjacent_up_same_mode():
    assert camelot_score("8B", "9B") == 0.8

def test_adjacent_down_same_mode():
    assert camelot_score("8B", "7B") == 0.8

def test_relative_major_minor_swap():
    assert camelot_score("8A", "8B") == 0.8
    assert camelot_score("8B", "8A") == 0.8

def test_two_steps_same_mode():
    assert camelot_score("8B", "10B") == 0.5
    assert camelot_score("8B", "6B") == 0.5

def test_incompatible_returns_low_score():
    assert camelot_score("1A", "7B") == 0.1

def test_wraparound_12_to_1():
    # 12B and 1B are adjacent on the wheel
    assert camelot_score("12B", "1B") == 0.8
    assert camelot_score("1B", "12B") == 0.8

def test_wraparound_1_to_12():
    assert camelot_score("1A", "12A") == 0.8

def test_empty_key_fallback():
    assert camelot_score("", "8B") == 0.1
    assert camelot_score("8B", "") == 0.1

def test_both_empty_fallback():
    assert camelot_score("", "") == 0.1
