from langchain.tools import tool
import pandas as pd
from src.utils import normalize_team_name

# 🔍 Core Logic Function
def get_player_vs_team_summary(player_name, team_name, season, df):
    """
    Returns batting and bowling summary of a given player against a specified team.
    
    Args:
        player_name (str): Name of the player (e.g., "Virat Kohli").
        team_name (str): Name of the opponent team (e.g., "Chennai Super Kings").
        season (int or None): IPL season year (e.g., 2020) or None for overall.
        df (pd.DataFrame): The IPL dataset.
    
    Returns:
        str: Formatted performance summary.
    """
    
    # ✅ Filter the dataset by season (if provided)
    if season:
        df = df[df['Season'] == season]

    # Batting Performance

    batting_df = df[(df['batter'] == player_name) & (df['BowlingTeam'] == team_name)]
    
    total_runs = batting_df['batsman_run'].sum()
    balls_faced = batting_df.shape[0]
    dismissals = batting_df[batting_df['player_out'] == player_name].shape[0]
    strike_rate = round((total_runs / balls_faced) * 100, 2) if balls_faced > 0 else "N/A"

    #  Bowling Performance
    bowling_df = df[(df['bowler'] == player_name) & (df['BattingTeam'] == team_name)]

    runs_conceded = bowling_df['total_run'].sum()
    wickets = bowling_df[bowling_df['isWicketDelivery'] == 1].shape[0]
    balls_bowled = bowling_df.shape[0]
    economy = round((runs_conceded / (balls_bowled / 6)), 2) if balls_bowled > 0 else "N/A"

    #  Format the Output
    
    season_str = f"{season}" if season else "Overall"

    summary = f"""
            📊 **Performance Summary of {player_name} vs {team_name}** ({season_str})

            🏏 **Batting Stats**
            - Runs Scored     : {total_runs}
            - Balls Faced     : {balls_faced}
            - Dismissals      : {dismissals}
            - Strike Rate     : {strike_rate}

            🎯 **Bowling Stats**
            - Runs Conceded   : {runs_conceded}
            - Balls Bowled    : {balls_bowled}
            - Wickets Taken   : {wickets}
            - Economy Rate    : {economy}
            """
    return summary
