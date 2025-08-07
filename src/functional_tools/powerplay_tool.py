# src/functional_tools/powerplay_summary.py

import pandas as pd
import re
from src.data_loader import load_ipl_data
from src.utils import normalize_team_name


def get_powerplay_summary(entity_name: str, ipl_df: pd.DataFrame, season: int = None) -> str:
    """
    Calculates batting/bowling stats for overs 1–6 (Powerplay) for teams or players.

    Parameters:
    - entity_name (str): Exact team or player name (no normalization here)
    - ipl_df (pd.DataFrame): IPL dataset
    - season (int, optional): Season year

    Returns:
    - str: Summary stats
    """
    df = ipl_df.copy()
    df = df[df["overs"].between(1, 6)]  # Filter to powerplay overs

    # Filter by season if provided
    if season:
        df = df[df["Season"] == season]

    all_teams = df["BattingTeam"].unique().tolist() + df["BowlingTeam"].unique().tolist()
    all_players = df["batter"].unique().tolist() + df["bowler"].unique().tolist()

    if entity_name in all_teams:
        entity_type = "team"
    elif entity_name in all_players:
        entity_type = "player"
    else:
        return f"❌ No data found for '{entity_name}'"

    if entity_type == "team":
        # Batting stats
        bat_df = df[df["BattingTeam"] == entity_name]
        runs = bat_df["total_run"].sum()
        balls = len(bat_df)
        wickets = bat_df["isWicketDelivery"].sum()
        strike_rate = round((runs / balls) * 100, 2) if balls else 0

        # Bowling stats
        bowl_df = df[df["BowlingTeam"] == entity_name]
        overs_bowled = len(bowl_df) / 6
        runs_conceded = bowl_df["total_run"].sum()
        wickets_taken = bowl_df["isWicketDelivery"].sum()
        economy = round(runs_conceded / overs_bowled, 2) if overs_bowled else 0

        return (
            f"📊 Powerplay Stats for **{entity_name}** ({season or 'All Seasons'})\n\n"
            f"**Batting:** Runs: {runs}, Wickets Lost: {wickets}, SR: {strike_rate}\n"
            f"**Bowling:** Overs: {overs_bowled:.1f}, Wickets Taken: {wickets_taken}, Economy: {economy}"
        )

    else:  # Player
        bat_df = df[df["batter"] == entity_name]
        runs = bat_df["batsman_run"].sum()
        balls = len(bat_df)
        strike_rate = round((runs / balls) * 100, 2) if balls else 0
        wickets_lost = bat_df["isWicketDelivery"].sum()

        bowl_df = df[df["bowler"] == entity_name]
        overs_bowled = len(bowl_df) / 6
        runs_conceded = bowl_df["total_run"].sum()
        wickets_taken = bowl_df["isWicketDelivery"].sum()
        economy = round(runs_conceded / overs_bowled, 2) if overs_bowled else 0

        return (
            f"📊 Powerplay Stats for **{entity_name}** ({season or 'All Seasons'})\n\n"
            f"**Batting:** Runs: {runs}, Wickets Lost: {wickets_lost}, SR: {strike_rate}\n"
            f"**Bowling:** Overs: {overs_bowled:.1f}, Wickets Taken: {wickets_taken}, Economy: {economy}"
        )