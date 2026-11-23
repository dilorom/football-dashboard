import pandas as pd
from stats import player_table

def test_counts_goals_and_xg():
    fake = pd.DataFrame({
        "player": ["A", "A", "B"],
        "shot_outcome": ["Goal", "Saved", "Goal"],
        "shot_statsbomb_xg": [0.5, 0.2, 0.1],
    })
    table = player_table(fake).set_index("player")
    assert table.loc["A", "shots"] == 2
    assert table.loc["A", "goals"] == 1
    assert table.loc["A", "xg"] == 0.7
    assert table.loc["B", "goals_minus_xg"] == 0.9