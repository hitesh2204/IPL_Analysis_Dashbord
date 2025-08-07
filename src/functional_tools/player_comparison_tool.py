import re
import pandas as pd

def get_player_comparison(player1: str, player2: str, ipl_df) -> str:
    players = [player1.strip(), player2.strip()]

    result = "🧍‍♂️ **IPL Player Comparison**\n\n"

    for player in players:
        batting_df = ipl_df[ipl_df['batter'] == player]
        bowling_df = ipl_df[ipl_df['bowler'] == player]
        full_df = pd.concat([batting_df, bowling_df]).drop_duplicates()

        if full_df.empty:
            result += f"❌ No data available for **{player}**.\n\n"
            continue

        # Batting stats
        total_runs = batting_df['batsman_run'].sum()
        total_balls = batting_df.shape[0]
        strike_rate = (total_runs / total_balls) * 100 if total_balls else 0
        total_fours = batting_df[batting_df['batsman_run'] == 4].shape[0]
        total_sixes = batting_df[batting_df['batsman_run'] == 6].shape[0]
        match_runs = batting_df.groupby("ID")["batsman_run"].sum()
        fifties = match_runs[(match_runs >= 50) & (match_runs < 100)].count()
        hundreds = match_runs[match_runs >= 100].count()
        highest_score = match_runs.max() if not match_runs.empty else 0

        # Bowling stats
        dismissals = bowling_df[bowling_df["isWicketDelivery"] == 1]
        total_wickets = dismissals["player_out"].notnull().sum()
        best_bowling = dismissals.groupby("ID")["player_out"].count().max() if not dismissals.empty else 0
        five_wkt_hauls = (dismissals.groupby("ID")["player_out"].count() >= 5).sum()

        # Teams and matches
        teams = set(batting_df['BattingTeam'].dropna().unique()) | set(bowling_df['BowlingTeam'].dropna().unique())
        total_matches = full_df['ID'].nunique()

        result += (
            f"🔹 **{player}**\n"
            f"• Matches: {total_matches}\n"
            f"• Teams: {', '.join(teams) if teams else 'N/A'}\n\n"
            f"**Batting:**\n"
            f"→ Runs: {total_runs}, Balls: {total_balls}, SR: {strike_rate:.2f}\n"
            f"→ 4s: {total_fours}, 6s: {total_sixes}\n"
            f"→ Highest Score: {highest_score}, 50s: {fifties}, 100s: {hundreds}\n\n"
            f"**Bowling:**\n"
            f"→ Wickets: {total_wickets}, Best in Match: {best_bowling} wkts\n"
            f"→ 5-Wicket Hauls: {five_wkt_hauls}\n\n"
        )

    return result
