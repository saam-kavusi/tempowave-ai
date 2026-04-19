# TempoWave AI: An AI DJ for Harmonic Playlist Generation

## Title and Summary
TempoWave AI is an applied AI system that generates ordered playlists from a local music dataset using harmonic compatibility, BPM flow, energy/valence sequencing, and mood-specific rules. Instead of only recommending songs independently, it builds a complete no-repeat playlist designed to flow smoothly from one track to the next.

This project extends my earlier CodePath Module 3 project, **Music Recommender Simulation**. The original project focused on loading songs from a CSV file and ranking individual tracks based on user preferences such as genre, mood, and related music features. Its main goal was to simulate a recommendation engine for matching songs, while TempoWave AI expands that idea into full playlist construction and transition planning.

This project matters because playlist quality depends not only on what songs are chosen, but also on how they are sequenced. TempoWave AI approaches that problem as a structured AI task by combining constrained filtering, scoring logic, explainable transitions, and exportable results into one end-to-end system.

## Architecture Overview
TempoWave AI is organized as a modular pipeline that moves from user input to filtering, sequencing, explanation, and output. The system begins by loading a local CSV dataset, validating the request, and filtering songs by exact genre and exact mood so that playlist generation stays tightly constrained and consistent.

After filtering, the core AI logic selects the first song and then repeatedly scores the remaining candidates using Camelot compatibility, BPM closeness, energy, and valence. The system chooses the best next song, adds it to the playlist, and repeats this process until the requested number of songs has been reached.

Once the playlist is complete, TempoWave AI generates transition explanations and exports the final result to CSV. The architecture also includes guardrails to safely handle invalid requests or insufficient candidate pools, making the overall system easier to trust and reproduce.

![TempoWave AI System Architecture](assets/system_architecture.png)

## Setup Instructions
To run TempoWave AI, first clone the repository and enter the project folder. The project is designed to be lightweight and reproducible, using a local CSV dataset instead of requiring external APIs or authentication.

Create a virtual environment, activate it, and install the dependencies listed in `requirements.txt`. After setup, the main entry point can be run directly from the terminal, and the same environment can also be used to run the test suite and evaluation script.

This setup is intentionally simple so that another developer, recruiter, or instructor can run the project without guessing what to install or configure. Keeping the system local also makes it easier to demonstrate reliably in a portfolio setting.

```bash
git clone https://github.com/saam-kavusi/tempowave-ai.git
cd tempowave-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
python -m pytest
python evaluation/run_eval.py

```

## Sample Interactions
TempoWave AI accepts three inputs: Genre, Mood, and Number of Songs. The system then filters the dataset, checks that enough matching songs exist, builds an ordered playlist, explains key transitions, and exports the result.

The examples below are included to show how the system behaves across different playlist styles. These runs demonstrate that the same core pipeline can produce different sequencing behavior depending on whether the user selects Workout, Chill, or Vibe.

Example 1

Input

Genre: Rap
Mood: Workout
Number of Songs: 5

Output

[Add final generated playlist here]
[Add 1–2 transition explanations here]
Example 2

Input

Genre: EDM
Mood: Chill
Number of Songs: 10

Output

[Add final generated playlist here]
[Add 1–2 transition explanations here]
Example 3

Input

Genre: Pop
Mood: Vibe
Number of Songs: 15

Output

[Add final generated playlist here]
[Add 1–2 transition explanations here]

## Design Decisions
TempoWave AI was designed to stay focused, reproducible, and realistic by using a local CSV dataset instead of relying on external APIs or streaming integrations. I chose curated music features such as BPM, Camelot key, energy, and valence so the system could produce musically informed playlist sequencing while remaining explainable and manageable within project scope.

## Testing Summary
TempoWave AI includes guardrails, unit tests, and an evaluation script to verify that the system behaves reliably across different inputs. The testing focuses on core behaviors such as exact filtering, request validation, harmonic compatibility logic, no-repeat playlist construction, and safe handling of insufficient-song cases.

## Reflection
This project taught me how to turn a simpler recommendation prototype into a more complete applied AI system with clearer structure, stronger constraints, and more explainable outputs. It also reinforced the importance of balancing ambition with practicality by building something specialized, testable, and polished enough to present professionally in a portfolio.