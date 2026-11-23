import pandas as pd

def player_table(shots):
    table = shots.groupby("player").agg(
        shots=("player", "count"),
        goals=("shot_outcome", lambda s: (s == "Goal").sum()),
        xg=("shot_statsbomb_xg", "sum"),
    ).reset_index()
    table["xg"] = table["xg"].round(2)
    table["goals_minus_xg"] = (table["goals"] - table["xg"]).round(2)
    return table.sort_values("xg", ascending=False)