import pandas as pd
from src.utils import normalize_team_name

def get_playoff_performance(player_or_team_name: str, df: pd.DataFrame) -> str:
    playoff_keywords = ['Qualifier 1', 'Eliminator', 'Final',' Semi Final', 'Semi Final', 'Qualifier 2', '3rd Place Play-Off']

    # Normalize team/player name
    player_or_team_name_normalized = normalize_team_name(player_or_team_name)
    
    # Filter playoff matches
    playoff_df = df[df["MatchNumber"].str.contains('|'.join(playoff_keywords), case=False, na=False)]

    # Check if input is team or player based on occurrence
    is_team = player_or_team_name_normalized in df['BattingTeam'].unique() or player_or_team_name_normalized in df['Team1'].unique()

    result = f"📊 **Playoff Performance for {player_or_team_name_normalized}**\n"

    if is_team:
        team_df = playoff_df[
            (playoff_df["BattingTeam"] == player_or_team_name_normalized) | 
            (playoff_df["Team1"] == player_or_team_name_normalized) |
            (playoff_df["Team2"] == player_or_team_name_normalized)
        ]
        matches_played = team_df["ID"].nunique()
        wins = team_df[team_df["WinningTeam"] == player_or_team_name_normalized]["ID"].nunique()
        losses = matches_played - wins

        result += f"\n🏏 Team Stats:\n- Matches: {matches_played}\n- Wins: {wins}\n- Losses: {losses}"

    else:
        # Player Batting
        batting_df = playoff_df[playoff_df["batter"] == player_or_team_name_normalized]
        runs = batting_df["batsman_run"].sum()
        balls = batting_df.shape[0]
        dismissals = batting_df[batting_df["player_out"] == player_or_team_name_normalized].shape[0]

        # Player Bowling
        bowling_df = playoff_df[playoff_df["bowler"] == player_or_team_name_normalized]
        balls_bowled = bowling_df.shape[0]
        runs_conceded = bowling_df["total_run"].sum()
        wickets = bowling_df[bowling_df["isWicketDelivery"] == 1].shape[0]

        result += f"\n\n🟢 **Batting:**\n- Runs: {runs}\n- Balls: {balls}\n- Dismissals: {dismissals}"
        result += f"\n\n🔵 **Bowling:**\n- Balls Bowled: {balls_bowled}\n- Runs Conceded: {runs_conceded}\n- Wickets: {wickets}"

    return result
