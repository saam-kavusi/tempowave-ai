from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []
        for song in self.songs:
            score = 0.0

            if song.mood.lower() == user.favorite_mood.lower():
                score += 5

            energy_diff = abs(song.energy - user.target_energy)
            score += max(0, 3 - energy_diff * 3)

            if song.genre.lower() == user.favorite_genre.lower():
                score += 2

            if user.likes_acoustic and song.acousticness >= 0.5:
                score += 1

            scored.append((score, song))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []

        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("matching mood")
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("matching genre")
        if abs(song.energy - user.target_energy) <= 0.2:
            reasons.append("similar energy")
        if user.likes_acoustic and song.acousticness >= 0.5:
            reasons.append("acoustic style")

        if not reasons:
            return "Recommended based on overall similarity."
        return "Recommended because of " + ", ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += 5
        reasons.append("matching mood")

    energy_diff = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = max(0, 3 - energy_diff * 3)
    score += energy_score
    if energy_score > 0:
        reasons.append("similar energy")

    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += 2
        reasons.append("matching genre")

    if user_prefs["likes_acoustic"] and song["acousticness"] >= 0.5:
        score += 1
        reasons.append("acoustic style")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "Recommended because of " + ", ".join(reasons) if reasons else "Recommended based on overall similarity."
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]