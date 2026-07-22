from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import pandas as pd

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
    target_valence: float = 0.5
    likes_acoustic: bool = False

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores every song against the user profile and returns the top-k Song objects."""
        user_prefs = asdict(user)
        scored = [(song, score_song(user_prefs, asdict(song))) for song in self.songs]
        scored.sort(key=lambda pair: pair[1][0], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song matches the user profile."""
        _, reasons = score_song(asdict(user), asdict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts using pandas."""
    print(f"Loading songs from {csv_path}...")
    return pd.read_csv(csv_path).to_dict("records")

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences using the weighted energy/valence/mood recipe."""
    energy_score = 1 - abs(song["energy"] - user_prefs["target_energy"])
    valence_score = 1 - abs(song["valence"] - user_prefs["target_valence"])
    mood_match = song["mood"] == user_prefs["favorite_mood"]
    mood_score = 1.0 if mood_match else 0.0

    score = (0.35 * energy_score) + (0.25 * valence_score) + (0.40 * mood_score)

    reasons = [
        f"mood {'matches' if mood_match else 'differs'} ({song['mood']} vs {user_prefs['favorite_mood']})",
        f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f}",
        f"valence {song['valence']:.2f} vs target {user_prefs['target_valence']:.2f}",
    ]
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song against user_prefs and returns the top-k (song, score, explanation) tuples."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda triple: triple[1], reverse=True)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in scored[:k]]
