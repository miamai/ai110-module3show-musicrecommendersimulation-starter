# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**MoodMatch 1.0**

---

## 2. Intended Use

MoodMatch is a classroom exploration of content-based recommendation, not a system for real users. Given one user profile (favorite genre, favorite mood, target energy, target valence, and whether they like acoustic music), it generates a ranked top-5 list of songs from an 18-song catalog. It assumes a listener's taste can be reduced to those five stated preferences, that a single mood label describes what they want right now, and that a numeric energy/valence target is a good stand-in for how a song actually feels.

---

## 3. How the Model Works

For every song in the catalog, MoodMatch checks three things: how close the song's energy is to what the listener asked for, how close its valence (brightness/positivity) is to what they asked for, and whether its mood label matches their favorite mood exactly. Those three checks are combined into one score, but not equally — mood match counts the most, energy closeness counts a bit less, and valence closeness counts the least. Every song gets scored this way, then they're sorted so the best matches float to the top and the top 5 get shown to the listener, along with a plain-English reason for each pick.

From the starter logic, I: (1) actually implemented the CSV loading using `pandas` instead of leaving it a stub, (2) added a `target_valence` preference (defaulting to a neutral 0.5) because the scoring formula needed it but the original starter profile didn't have it, and (3) built the "reasons" text so each recommendation explains itself instead of just showing a bare number.

---

## 4. Data

The catalog has 18 songs. The original starter file had 10, covering pop, lofi, rock, ambient, jazz, synthwave, and indie pop with moods like happy, chill, intense, relaxed, moody, and focused. I added 8 more songs to cover genres and moods that were completely missing: hip-hop, classical, folk, metal, R&B, electronic, country, and reggae, with moods like energetic, melancholic, nostalgic, aggressive, romantic, dreamy, uplifting, and carefree. Even after adding those, the catalog is unevenly distributed — pop and lofi each have 3+ songs while most of the new genres have exactly one — so results for niche tastes are less reliable than for pop/lofi listeners. The catalog also doesn't capture lyrics, language, listening history, or artist similarity, and `tempo_bpm` is stored for every song but never actually used in scoring.

---

## 5. Strengths

MoodMatch works best for listeners whose favorite mood clearly exists in the catalog. The "High-Energy Pop" and "Chill Lofi" experiment runs (see README) both produced tight, intuitive top-3 clusters — pop/happy tracks for the pop profile, lofi/chill and ambient tracks for the lofi profile — with no odd or out-of-place picks. The energy dimension also demonstrably drives ranking rather than just riding along on mood: flipping `target_energy` from 0.90 down to 0.30 (same mood-matching logic otherwise) flipped the entire top 3 from high-energy pop songs to low-energy lofi songs, which is exactly the behavior you'd want from that feature.

---

## 6. Limitations and Bias

Mood matching is all-or-nothing: `mood_score` is 1 or 0 with no partial credit, so if a user's `favorite_mood` isn't one of the catalog's exact mood labels (e.g. `"sad"`, which doesn't exist among the 18 songs), that 40%-weighted term is zero for every song and ranking silently collapses to energy/valence alone — the "Conflicting Signals" experiment (see README) shows this: the top result "Sunrise City" scores 0.56 purely on energy/valence, with no mood contribution at all. Genre and `likes_acoustic` are captured in the user profile but never used by `score_song` — the same "Conflicting Signals" run asked for `favorite_genre=classical` and `likes_acoustic=True`, yet every top-5 result was an electronic, non-acoustic pop/rock track, so the system can silently ignore two of five stated preferences without any warning to the user. The catalog is also unevenly distributed across genres: pop and lofi each have 3+ songs while classical, metal, R&B, folk, country, and reggae have exactly one, so users whose taste maps to a niche genre get a much smaller and less-tuned candidate pool than pop/lofi listeners — the system's apparent quality is really a function of how well-represented a taste is in the data, not how good the scoring logic is.

---

## 7. Evaluation

Tested five profiles total via `python -m src.main`: the starter pop/happy profile plus four experimental ones — High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial "Conflicting Signals" profile (`favorite_genre=classical, favorite_mood=sad, target_energy=0.90, likes_acoustic=True`). For each, I checked whether the top result's genre/mood matched intuition, whether nudging `target_energy`/`target_valence` shifted the ranking in the expected direction, and whether an intentionally broken/contradictory profile would crash the system or just quietly misbehave (it did the latter, not the former).

Comparisons:

- **High-Energy Pop vs. Chill Lofi**: flipping `target_energy` from 0.90 to 0.30 flips the entire top 3 from pop/happy tracks ("Sunrise City," "Rooftop Lights") to lofi/ambient chill tracks ("Library Rain," "Spacewalk Thoughts," "Midnight Coding") — confirms `energy_score` genuinely drives ranking, it isn't just riding on `mood_score`.
- **Deep Intense Rock vs. Conflicting Signals**: both profiles want `target_energy=0.90`, but Deep Intense Rock has a real catalog mood (`"intense"`) and surfaces "Storm Runner" (rock/intense, 0.95) as a clean mood-matching top pick, while Conflicting Signals' mood (`"sad"`) matches nothing, so its top pick ("Sunrise City," 0.56) is chosen on energy/valence alone — same energy target, very different reasoning behind the #1 result.
- **Deep Intense Rock internally**: "Storm Runner" (rock/intense, 0.95) beats "Iron Horizon" (metal/aggressive, 0.55) despite Iron Horizon having near-identical energy (0.97 vs 0.91) and closer-if-anything valence — the 0.40-weighted mood term is the entire reason for the 0.40-point gap, showing how much a single categorical mismatch can cost a taste-adjacent song.

What surprised me: the adversarial "Conflicting Signals" profile didn't produce an obviously broken or empty result — it returned five plausible-looking, reasonably-scored (0.49–0.56) songs. That's the concerning part: a user who typed in a genre/mood the system can't actually honor gets a confident-looking list anyway, with no signal that 2 of their 5 stated preferences (genre, acoustic) were silently ignored and their mood preference matched nothing in the catalog.

---

## 8. Future Work

If I kept developing this, I'd: (1) add a genre-match term to the scoring formula so `favorite_genre` actually influences ranking — right now it's collected from the user but never used, which the "Conflicting Signals" experiment exposed directly; (2) replace exact-string mood matching with a similarity or near-miss scale, so a mood like "uplifting" scores better than "aggressive" against a "happy" preference instead of scoring the same (both currently just fail the equality check); and (3) surface a coverage/confidence warning when a user's stated mood doesn't exist anywhere in the catalog, since right now the system returns a confident-looking top-5 even when it's silently ignoring most of what the user asked for.

---

## 9. Personal Reflection

The biggest learning moment for me was realizing how little math it actually takes for a recommendation to "feel" right — a weighted sum over three features, mostly leaning on one exact string match, is enough to reliably surface pop songs for a pop/happy listener and lofi songs for a chill listener.
