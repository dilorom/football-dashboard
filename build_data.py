import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from statsbombpy import sb

matches = sb.matches(competition_id=43, season_id=106)
all_shots = []

for i, match in matches.iterrows():
    print(f"Loading {i + 1}/{len(matches)}: {match['home_team']} vs {match['away_team']}")
    events = sb.events(match_id=match["match_id"])
    shots = events[(events["type"] == "Shot") & (events["period"] < 5)]
    shots = shots[["match_id", "minute", "team", "player", "shot_outcome", "shot_statsbomb_xg", "location"]].copy()
    shots["match_date"] = match["match_date"]
    shots["opponent"] = shots["team"].apply(
        lambda t: match["away_team"] if t == match["home_team"] else match["home_team"]
    )
    all_shots.append(shots)

data = pd.concat(all_shots)
data.to_csv("shots.csv", index=False)
print("Saved", len(data), "shots to shots.csv")