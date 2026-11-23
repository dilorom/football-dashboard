import pandas as pd
import streamlit as st
import sqlite3
from stats import player_table

st.set_page_config(page_title="Football Dashboard", layout="wide")

@st.cache_data
def load_shots():
    conn = sqlite3.connect("football.db")
    df = pd.read_sql("SELECT * FROM shots", conn)
    conn.close()
    return df

shots = load_shots()

st.title("Football Performance Dashboard")
st.caption("FIFA World Cup 2022 · data: StatsBomb Open Data")

teams = sorted(shots["team"].unique())
team = st.selectbox("Choose a team", teams)

team_shots = shots[shots["team"] == team]

table = player_table(team_shots)
table = table.sort_values("xg", ascending=False)

col1, col2, col3 = st.columns(3)
col1.metric("Shots", len(team_shots))
col2.metric("Goals", int(table["goals"].sum()))
col3.metric("Total xG", round(table["xg"].sum(), 2))

st.dataframe(table, use_container_width=True, hide_index=True)



import plotly.express as px

st.divider()
st.header("Player trend")

players = table["player"].tolist()
player = st.selectbox("Choose a player", players)

p = team_shots[team_shots["player"] == player]
per_match = p.groupby(["match_date", "opponent"]).agg(
    shots=("player", "count"),
    goals=("shot_outcome", lambda s: (s == "Goal").sum()),
    xg=("shot_statsbomb_xg", "sum"),
).reset_index().sort_values("match_date")

per_match["label"] = per_match["match_date"] + " vs " + per_match["opponent"]

fig = px.bar(per_match, x="label", y=["xg", "goals"], barmode="group",
             title=f"{player}: xG vs goals per match",
             labels={"value": "Amount", "label": "Match", "variable": ""})
st.plotly_chart(fig, use_container_width=True)



import ast
import plotly.graph_objects as go

st.divider()
st.header("Opposition report")

opponent = st.selectbox("Scout a team", teams, key="opp")
opp = shots[shots["team"] == opponent].copy()

opp["xy"] = opp["location"].apply(ast.literal_eval)
opp["x"] = opp["xy"].str[0]
opp["y"] = opp["xy"].str[1]
opp["is_goal"] = opp["shot_outcome"] == "Goal"

c1, c2, c3 = st.columns(3)
games = opp["match_id"].nunique()
c1.metric("Games", games)
c2.metric("Shots per game", round(len(opp) / games, 1))
c3.metric("xG per game", round(opp["shot_statsbomb_xg"].sum() / games, 2))

fig = go.Figure()
fig.add_shape(type="rect", x0=60, y0=0, x1=120, y1=80, line_color="gray")
fig.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line_color="gray")
fig.add_shape(type="rect", x0=114, y0=30, x1=120, y1=50, line_color="gray")

for goal, colour, name in [(False, "lightgray", "No goal"), (True, "red", "Goal")]:
    part = opp[opp["is_goal"] == goal]
    fig.add_trace(go.Scatter(
        x=part["x"], y=part["y"], mode="markers", name=name,
        marker=dict(size=part["shot_statsbomb_xg"] * 40 + 5, color=colour,
                    line=dict(width=1, color="black")),
        text=part["player"] + " · xG " + part["shot_statsbomb_xg"].round(2).astype(str),
        hoverinfo="text",
    ))

fig.update_xaxes(range=[60, 121], visible=False)
fig.update_yaxes(range=[81, -1], visible=False, scaleanchor="x")
fig.update_layout(title=f"{opponent}: every shot (bigger = better chance)",
                  plot_bgcolor="white", height=500)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.header("Tournament leaders (SQL)")

conn = sqlite3.connect("football.db")
leaders = pd.read_sql("""
    SELECT player, team,
           COUNT(*) AS shots,
           SUM(shot_outcome = 'Goal') AS goals,
           ROUND(SUM(shot_statsbomb_xg), 2) AS xg
    FROM shots
    GROUP BY player, team
    ORDER BY xg DESC
    LIMIT 10
""", conn)
conn.close()
st.dataframe(leaders, use_container_width=True, hide_index=True)