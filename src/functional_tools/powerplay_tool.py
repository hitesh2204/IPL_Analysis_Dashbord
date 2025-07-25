# src/functional_tools/powerplay_summary.py

import pandas as pd
import re
from src.data_loader import load_ipl_data
from src.utils import normalize_team_name


def get_powerplay_summary(query: str, ipl_df) -> str:
    """
    Input format: 'Team Name, Season' or just 'Team Name'
    Example: 'Mumbai Indians, 2020' or 'RCB'
    """
    # Parse team and optional season
    parts = [p.strip() for p in query.split(",")]
    team = normalize_team_name(parts[0])
    season = int(parts[1]) if len(parts) > 1 and re.match(r"\d{4}", parts[1]) else None

    # Filter Powerplay data (overs 1 to 6)
    df = ipl_df.copy()
    df = df[df["overs"].between(1, 6)]
    df = df[df["BattingTeam"].str.lower() == team.lower()]
    if season:
        df = df[df["Season"] == season]

    if df.empty:
        return f"No powerplay data found for {team} in {season if season else 'all seasons'}."

    total_runs = df["total_run"].sum()
    total_balls = len(df)
    wickets = df["isWicketDelivery"].sum()
    strike_rate = round((total_runs / total_balls) * 100, 2) if total_balls > 0 else 0

    return (
        f"📊 Powerplay Summary for {team} ({season if season else 'All Seasons'}):\n"
        f"- 🏏 Total Runs: {total_runs}\n"
        f"- ❌ Wickets Lost: {int(wickets)}\n"
        f"- ⚡ Strike Rate: {strike_rate}"
    )

