import pandas as pd
from src.data_loader import load_ipl_data

ipl = load_ipl_data()

def get_filtered_leaderboard(stat: str, top_n=5, season=None, phase=None, entity_type="player", venue=None):
    df = ipl.copy()

    # Season filter
    if season:
        df = df[df["Season"] == int(season)]

    # Venue filter
    if venue:
        df = df[df["Venue"].str.lower() == venue.lower()]

    # Phase filter
    if phase:
        if phase.lower() == "powerplay":
            df = df[df["overs"].between(1, 6)]
        elif phase.lower() == "middle":
            df = df[df["overs"].between(7, 15)]
        elif phase.lower() == "death":
            df = df[df["overs"].between(16, 20)]

    if entity_type == "player":
        group_col = "batter"
    elif entity_type == "team":
        group_col = "BattingTeam"
    else:
        return "Entity type must be 'player' or 'team'."

    if stat.lower() == "strike rate":
        runs = df.groupby(group_col)["batsman_run"].sum()
        balls = df.groupby(group_col).size()
        sr = (runs / balls) * 100
        result = sr.sort_values(ascending=False).head(top_n).reset_index(name="strike_rate")

    elif stat.lower() == "win %":
        matches = df.groupby(group_col)["ID"].nunique()
        wins = df[df["WinningTeam"] == df[group_col]].groupby(group_col)["ID"].nunique()
        win_pct = (wins / matches) * 100
        result = win_pct.sort_values(ascending=False).head(top_n).reset_index(name="win_percentage")

    else:
        return f"Stat '{stat}' not supported yet."

    return result.to_string(index=False)
