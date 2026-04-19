# 🎧 Model Card: TempoWave AI

## 1. Model Name

TempoWave AI: An AI DJ for Harmonic Playlist Generation

---

## 2. Intended Use

TempoWave AI is designed to generate ordered playlists from a local music dataset using genre, mood, harmonic compatibility, BPM flow, energy, and valence. Its purpose is not just to recommend individual songs, but to build a full sequence that feels more coherent from one track to the next.

The system is intended for classroom and portfolio demonstration as a specialized applied AI project. It is best suited for users who want a simple, explainable playlist generator based on structured music metadata rather than a large commercial recommendation platform.

The expected use case is narrow and controlled: the user selects a genre, a mood, and a number of songs, and the system returns a no-repeat playlist from that exact bucket. It is not designed for open-ended music discovery, personalization from listening history, or real-time streaming.

---

## 3. How the Model Works

TempoWave AI uses a constrained playlist-planning workflow rather than a general-purpose machine learning model. It begins by loading songs from a local CSV file, validating the request, and filtering the dataset by exact genre and exact mood so that all candidates come from a clearly defined pool.

After filtering, the system selects a first song based on mood-aware logic and then repeatedly scores the remaining candidates. Each transition is evaluated using Camelot compatibility, BPM closeness, energy flow, and valence alignment. The highest-scoring next song is added to the playlist, and the process repeats until the requested number of songs has been reached.

Once the playlist is complete, the system generates transition explanations and can export the result to CSV. It also supports a lightweight verbose mode that shows intermediate steps such as filtering, scoring, picking the next song, and building the playlist, which helps make the system more explainable and easier to review.

---

## 4. Data

The dataset is stored in `data/songs.csv` and currently contains 145 songs. Each row includes the following fields: `song_id`, `title`, `artist`, `genre`, `mood_tag`, `bpm`, `musical_key`, `camelot_key`, `energy`, and `valence`.

The data was curated specifically for this project and organized around three genres and three moods: Rap, EDM, and Pop, crossed with Workout, Chill, and Vibe. This structure allows the system to operate on well-defined candidate buckets and makes testing more predictable.

A limitation of the dataset is that some BPM and key values were manually approximated for less common songs. In addition, the dataset does not include listening history, lyrical themes, artist relationships, popularity, or raw audio features, so the system’s view of musical fit is intentionally narrow and metadata-driven.

---

## 5. Strengths

One of TempoWave AI’s main strengths is that it solves a more interesting problem than simple recommendation ranking: playlist sequencing. Instead of only asking which songs match a user’s preferences, it also asks which songs flow together in a musically sensible order.

The system is also strong in explainability. Because the playlist is built from transparent rules such as exact filtering, harmonic compatibility, BPM closeness, and energy/valence movement, the results are easier to understand and defend than black-box outputs. The verbose mode strengthens this further by showing intermediate decision steps.

Another strength is reproducibility. The project runs locally from a CSV file, has clear guardrails, includes automated tests, and supports a repeatable evaluation script. That makes it easier to demo, review, and validate than a more complex system that depends on external APIs or hidden data sources.

---

## 6. Limitations and Bias

TempoWave AI is limited by the scope and quality of its dataset. Because the system only works with the songs present in `songs.csv`, it cannot generalize beyond that catalog, and it may produce weaker results when a selected bucket has less stylistic variety than others.

The system also simplifies music preference into a small set of structured features. Real playlist quality depends on more than genre, mood, key, BPM, energy, and valence. Factors such as lyrics, artist familiarity, cultural context, nostalgia, production style, and personal listening history are all missing, which means the system can only approximate musical fit.

There is also potential bias in the curated metadata itself. Since some feature values were manually selected or estimated, those choices can influence how the system ranks transitions. In that sense, the playlist logic is only as strong as the assumptions built into the dataset and scoring rules.

---

## 7. Evaluation

I evaluated TempoWave AI using three main methods: direct manual review of playlist quality, automated pytest tests, and a scripted evaluation run with predefined scenarios. This allowed me to check both whether the system behaved correctly and whether the outputs felt musically reasonable.

The final test suite passed 78 out of 78 tests. These tests covered key behaviors such as exact filtering, request validation, harmonic compatibility logic, playlist length correctness, no-repeat construction, mood-aware opening song selection, and interactive input handling such as case-insensitive genre and mood input plus re-prompting on invalid entries. I also ran an evaluation script that generated multiple demo playlists and separately tested invalid inputs to confirm that the guardrails blocked unsupported genre, mood, and count requests.

What stood out most during evaluation was that the system performed best when the mood constraints and dataset bucket were well matched. The evaluation also helped reveal smaller polish issues, such as terminal table formatting for long artist names, which I fixed so the output would be cleaner and more professional for demo and review purposes.

---

## 8. Future Work

The clearest next improvement would be to expand the dataset and increase stylistic diversity within each genre-mood bucket. That would give the planner more candidate variety and reduce the chance that a playlist feels too tightly constrained by a small pool.

Another strong improvement would be to enrich the metadata. Features such as subgenre, vocal/instrumental tags, release era, intensity curves, or more nuanced emotional labels could help the system generate transitions that feel even more intentional and musically coherent.

A longer-term version of the project could also improve the output experience by adding a lightweight front end, stronger explanation formatting, and more advanced sequencing strategies. However, for this project, I deliberately kept the scope local, modular, and explainable rather than expanding into external APIs or streaming integrations.

## 9. Misuse Risks and Mitigations

TempoWave AI could be misused if someone presents its playlists as objectively “correct” or as a substitute for real listener preference. In reality, the system is a constrained playlist generator based on curated metadata and scoring rules, not a universal music-quality judge or a personalized commercial recommendation engine.

To reduce that risk, the project is documented clearly as a classroom and portfolio system with a narrow intended use. It also uses guardrails, exact filtering, and explainable transitions so that users can see how results were produced instead of treating them as black-box outputs.

---

## 10. AI Collaboration Notes

AI was helpful during this project when it assisted with implementation structure and debugging workflow. One especially helpful contribution was speeding up the transition from planning to modular code by helping scaffold files for filtering, harmonic scoring, guardrails, playlist planning, and tests in a consistent structure.

One flawed suggestion from AI was output formatting that initially looked acceptable in theory but broke alignment when artist names became too long in the evaluation table. That issue had to be caught through human review and then corrected by truncating long text fields so the CLI output stayed clean and readable.

What surprised me most during testing was that reliability was not only about logic correctness, but also about presentation quality. The system’s core behavior worked, but smaller issues like formatting and edge-case messaging still mattered because they affected how trustworthy and professional the final output felt.

---

## 11. Personal Reflection

This project taught me that recommendation and sequencing are related but different problems. My earlier project focused on matching songs to preferences, but TempoWave AI pushed me to think more deeply about flow, transition quality, and how a system can build a coherent experience instead of just a ranked list.

One of the most interesting things I discovered was how useful constrained logic can be when it is paired with good structure and testing. Even without a large external model, the system still feels meaningfully “AI-like” because it performs a specialized task, makes step-by-step decisions, and produces explainable results.

This project also changed how I think about music apps and AI systems more broadly. It showed me that a strong applied AI project does not need to be huge or overly complex; it needs to be focused, testable, understandable, and intentional in how it turns data into decisions.