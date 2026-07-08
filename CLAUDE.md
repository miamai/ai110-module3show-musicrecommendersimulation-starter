# CLAUDE.md — Music Recommender Simulation

## Project Overview

A classroom content-based music recommender built in Python. Songs are scored against a user taste profile using weighted numeric and categorical features; the top-k scored songs become the recommendations.

**Run the app:**
```bash
python -m src.main
```

**Run tests:**
```bash
pytest
```

---

## Repository Layout

```
src/
  main.py          — CLI entry point; calls load_songs + recommend_songs
  recommender.py   — All core logic: dataclasses, scoring, ranking
data/
  songs.csv        — 10-song catalog (the full dataset)
tests/
  test_recommender.py — pytest suite targeting Song, UserProfile, Recommender
model_card.md      — Student reflection doc (not code)
ai_interactions.md — Stretch feature log (not code)
```

---

## Core Data Model

**`Song` dataclass** (`src/recommender.py`):

| Field | Type | Notes |
|---|---|---|
| `id` | int | 1–10 |
| `title` | str | |
| `artist` | str | |
| `genre` | str | pop, lofi, rock, ambient, jazz, synthwave, indie pop |
| `mood` | str | happy, chill, intense, relaxed, moody, focused |
| `energy` | float 0–1 | physical intensity |
| `tempo_bpm` | float | 60–152 BPM |
| `valence` | float 0–1 | brightness / positivity |
| `danceability` | float 0–1 | rhythmic suitability |
| `acousticness` | float 0–1 | organic vs. electronic |

**`UserProfile` dataclass** (`src/recommender.py`):

| Field | Type | Example |
|---|---|---|
| `favorite_genre` | str | `"pop"` |
| `favorite_mood` | str | `"happy"` |
| `target_energy` | float 0–1 | `0.8` |
| `likes_acoustic` | bool | `False` |

---

## Scoring Formula

`score_song()` returns a float in **[0.0, 1.0]** using three Tier 1 features:

```
energy_score  = 1 - |song.energy  - user.target_energy|
valence_score = 1 - |song.valence - user.target_valence|
mood_score    = 1  if song.mood == user.favorite_mood, else 0

score = (0.35 × energy_score) + (0.25 × valence_score) + (0.40 × mood_score)
```

Weight rationale: mood (0.40) is the most explicit user signal; energy (0.35) is the most perceptually obvious numeric gap; valence (0.25) adds emotional nuance.

The `recommend_songs()` function scores every song, sorts by score descending, and returns the top `k` as `(song_dict, score, explanation)` tuples.

---

## Implementation Status

All core functions are TODO stubs — this is intentional starter code:

| Function / Method | File | Status |
|---|---|---|
| `load_songs(csv_path)` | `src/recommender.py` | TODO |
| `score_song(user_prefs, song)` | `src/recommender.py` | TODO |
| `recommend_songs(user_prefs, songs, k)` | `src/recommender.py` | TODO |
| `Recommender.recommend(user, k)` | `src/recommender.py` | TODO |
| `Recommender.explain_recommendation(user, song)` | `src/recommender.py` | TODO |

`load_songs` should use `pandas.read_csv` and return a list of dicts (one per row). `score_song` should implement the formula above. `recommend_songs` should call `score_song` for every song and return sorted top-k.

---

## Test Contract

`tests/test_recommender.py` imports `Song`, `UserProfile`, and `Recommender` from `src.recommender`. Tests assert:

1. `recommend()` returns songs sorted by score — pop/happy song ranks above lofi/chill for a pop/happy/high-energy user profile.
2. `explain_recommendation()` returns a non-empty string.

Do not rename or move these classes — the test file imports them by name.

---

## Dependencies

```
pandas    — CSV loading
pytest    — test runner
streamlit — optional UI (not used in starter)
```