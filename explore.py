import warnings
warnings.filterwarnings("ignore")

from statsbombpy import sb

matches = sb.matches(competition_id=43, season_id=106)
final = matches[matches["competition_stage"] == "Final"].iloc[0]
print(final["home_team"], final["home_score"], "-", final["away_score"], final["away_team"])

events = sb.events(match_id=final["match_id"])
print("Events in this match:", len(events))
print(events["type"].value_counts().head(10))

shots = events[events["type"] == "Shot"]
print(shots[["minute", "team", "player", "shot_outcome", "shot_statsbomb_xg"]].to_string())