# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This system is a **content-based recommender**: it scores every song in the catalog against a user's taste profile using the song's own attributes — no data from other users is needed.

### Song Features

Each `Song` stores ten attributes loaded from `data/songs.csv`:

| Attribute | Type | Description |
|---|---|---|
| `genre` | categorical | Broad style bucket (pop, lofi, rock, jazz, …) |
| `mood` | categorical | Emotional tone (happy, chill, intense, moody, …) |
| `energy` | float 0–1 | Physical intensity — low = calm, high = driving |
| `valence` | float 0–1 | Musical brightness — high = uplifting, low = dark |
| `tempo_bpm` | float | Beats per minute |
| `danceability` | float 0–1 | Rhythmic suitability for movement |
| `acousticness` | float 0–1 | Organic/natural vs. electronic sound |

### UserProfile

A `UserProfile` stores the user's stated preferences:

- `favorite_mood` — the mood they want right now (e.g. `"happy"`)
- `target_energy` — how intense they want the music (e.g. `0.8`)
- `target_valence` — how bright/positive they want the music (e.g. `0.8`, defaults to `0.5`)
- `favorite_genre` — their preferred genre (e.g. `"pop"`)
- `likes_acoustic` — whether they prefer acoustic over electronic sound

### Example Taste Profile

A concrete profile for an upbeat-pop workout listener:

```python
user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
    "target_valence": 0.80,
    "likes_acoustic": False,
}
```

Against the 18-song catalog, this profile should clearly separate high-energy/high-valence pop and happy tracks (e.g. "Sunrise City," "Gym Hero," "Rooftop Lights") from both intense-but-dark songs (e.g. "Iron Horizon" — high energy, low valence, wrong mood) and mellow songs (lofi, classical, ambient — low energy, wrong mood). See the real ranked output in [Sample Recommendation Output](#sample-recommendation-output).

### Scoring Rule (one song)

`score_song()` computes a match score in **[0.0, 1.0]** using three Tier 1 features with weighted combination:

```
energy_score  = 1 - |song.energy  - user.target_energy|
valence_score = 1 - |song.valence - user.target_valence|
mood_score    = 1  if song.mood == user.favorite_mood, else 0

score = (0.35 × energy_score) + (0.25 × valence_score) + (0.40 × mood_score)
```

Weights reflect intent strength: `mood` (0.40) is the user's most explicit request; `energy` (0.35) is the most perceptually obvious numeric difference; `valence` (0.25) adds emotional nuance.

### Ranking Rule (full catalog)

`recommend_songs()` applies the scoring rule to every song, then:

1. Sorts all `(song, score)` pairs by score descending
2. Returns the top `k` results (default `k = 5`)

```
User Profile ──► score_song(song_1) ──► 0.983
                 score_song(song_2) ──► 0.481   ──► sort ──► top-k ──► Recommendations
                 score_song(song_N) ──► 0.712
```

The scoring rule grades each song independently; the ranking rule makes the final comparative decision.

### Potential Biases

- **Mood is all-or-nothing.** Because `mood_score` is a strict boolean (1 or 0), a near-miss mood (e.g. "uplifting" or "carefree") scores no better than a totally opposite mood (e.g. "aggressive") — the system over-rewards exact mood labels over emotional similarity.
- **Genre isn't scored at all.** Two songs with identical energy/valence/mood but very different genres receive identical scores — the system may under-represent genre preference despite `favorite_genre` being part of the user profile.
- **`likes_acoustic` is unused.** It's captured on `UserProfile` but not yet factored into the Tier-1 formula — acoustic preference currently has no effect on ranking.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the starter profile (`favorite_genre=pop, favorite_mood=happy, target_energy=0.8, target_valence=0.8`):

```
Loading songs from data/songs.csv...

Top recommendations:

Rooftop Lights - Score: 0.98
Because: mood matches (happy vs happy); energy 0.76 vs target 0.80; valence 0.81 vs target 0.80

Sunrise City - Score: 0.98
Because: mood matches (happy vs happy); energy 0.82 vs target 0.80; valence 0.84 vs target 0.80

Gym Hero - Score: 0.55
Because: mood differs (intense vs happy); energy 0.93 vs target 0.80; valence 0.77 vs target 0.80

Concrete Jungle - Score: 0.54
Because: mood differs (energetic vs happy); energy 0.85 vs target 0.80; valence 0.62 vs target 0.80

Backroad Sundown - Score: 0.53
Because: mood differs (uplifting vs happy); energy 0.60 vs target 0.80; valence 0.80 vs target 0.80
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



