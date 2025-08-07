import pandas as pd
from src.data_loader import load_ipl_data

ipl = load_ipl_data()

def get_record_finder(record_type: str, season=None, match_type=None, phase=None, venue=None):
    df = ipl.copy()

    # Filter season
    if season:
        df = df[df["Season"] == int(season)]

    # Filter by match type
    if match_type:
        match_type = match_type.lower()
        if match_type == "final":
            df = df[df["MatchType"].str.lower() == "final"]
        elif match_type == "playoffs":
            df = df[df["MatchType"].str.lower().isin(["qualifier 1", "qualifier 2", "eliminator", "final"])]

    # Filter by venue
    if venue:
        df = df[df["Venue"].str.lower() == venue.lower()]

    # Filter by phase
    if phase:
        if phase.lower() == "powerplay":
            df = df[df["overs"].between(1, 6)]
        elif phase.lower() == "middle":
            df = df[df["overs"].between(7, 15)]
        elif phase.lower() == "death":
            df = df[df["overs"].between(16, 20)]

    # Record logic
    if record_type.lower() == "fastest fifty":
        scores = df.groupby(["ID", "batter"])["batsman_run"].cumsum()
        fifty_balls = df[scores >= 50].groupby(["ID", "batter"]).first().reset_index()
        result = fifty_balls.sort_values("ball_number").head(5)

    elif record_type.lower() == "highest score":
        result = df.groupby(["ID", "batter"])["batsman_run"].sum().reset_index()
        result = result.sort_values("batsman_run", ascending=False).head(5)

    elif record_type.lower() == "best bowling":
        result = df[df["isWicketDelivery"] == 1].groupby(["ID", "bowler"])["player_out"].count().reset_index(name="wickets")
        result = result.sort_values("wickets", ascending=False).head(5)

    else:
        return f"Record type '{record_type}' not supported yet."

    return result.to_string(index=False)