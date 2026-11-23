# Football Performance Dashboard

A coach-facing dashboard for player development and opposition analysis,
built with Python, Streamlit, Plotly, pandas and SQLite.
Data: FIFA World Cup 2022 from StatsBomb Open Data.

## Why I built it
(2–3 sentences: your EdgeLog story, helping coaches see progress and weak points.)

## Features
- Squad overview: shots, goals, xG and goals minus xG per player
- Player trend: xG vs goals, match by match
- Opposition report: shot map and per-game averages
- Tournament leaders: written in SQL

## How to run
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build_data.py
python make_db.py
streamlit run app.py

## Tests
python -m pytest