"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

def main():
    songs = load_songs("../data/songs.csv")

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for song, score, explanation in recommendations:
        print(f"{song['title']} by {song['artist']} | Score: {score:.2f}")
        print(f"  {explanation}")

if __name__ == "__main__":
    main()
