# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
