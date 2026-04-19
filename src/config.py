"""Central configuration for TempoWave AI."""

DATA_PATH = "data/songs.csv"

VALID_GENRES = ["Rap", "EDM", "Pop"]
VALID_MOODS = ["Workout", "Vibe", "Chill"]
VALID_COUNTS = [5, 10, 15]

# Composite transition-scoring weights per mood.
# All four weights in each row must sum to 1.0.
MOOD_WEIGHTS = {
    "Workout": {
        "harmonic": 0.15,
        "bpm":      0.30,
        "energy":   0.45,
        "valence":  0.10,
    },
    "Chill": {
        "harmonic": 0.40,
        "bpm":      0.20,
        "energy":   0.25,
        "valence":  0.15,
    },
    "Vibe": {
        "harmonic": 0.30,
        "bpm":      0.25,
        "energy":   0.25,
        "valence":  0.20,
    },
}
