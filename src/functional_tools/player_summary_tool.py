import pandas as pd
from src.data_loader import load_ipl_data

# 🧠 GENAI FUNCTION — Used by LangChain Agent
def get_player_summary(player_name: str) -> str:
    ipl = load_ipl_data()

    player_df = ipl[ipl['batter'] == player_name]
    bowler_df = ipl[ipl['bowler'] == player_name]
    full_df = pd.concat([player_df, bowler_df]).drop_duplicates()

    if player_df.empty and bowler_df.empty:
        return f"No data found for {player_name}."

    total_runs = player_df['batsman_run'].sum()
    total_balls = player_df.shape[0]
    total_fours = player_df[player_df['batsman_run'] == 4].shape[0]
    total_sixes = player_df[player_df['batsman_run'] == 6].shape[0]
    total_outs = ipl[ipl['player_out'] == player_name].shape[0]
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0

    match_runs = player_df.groupby('ID')['batsman_run'].sum()
    highest_score = match_runs.max() if not match_runs.empty else 0
    fifties = match_runs[(match_runs >= 50) & (match_runs < 100)].count()
    hundreds = match_runs[match_runs >= 100].count()

    summary = f"📊 **IPL Career Summary of {player_name}**\n\n"
    summary += f"🏏 Batting:\n"
    summary += f"- Total Runs: {total_runs}\n"
    summary += f"- Balls Faced: {total_balls}\n"
    summary += f"- 4s: {total_fours}, 6s: {total_sixes}\n"
    summary += f"- Strike Rate: {strike_rate:.2f}\n"
    summary += f"- Highest Score: {highest_score}\n"
    summary += f"- 50s: {fifties}, 100s: {hundreds}\n"
    summary += f"- Dismissals: {total_outs}\n"

    dismissals = bowler_df[bowler_df['isWicketDelivery'] == 1]
    total_wickets = dismissals['player_out'].notnull().sum()
    best_bowling_df = dismissals.groupby('ID')['player_out'].count()
    best_bowling = best_bowling_df.max() if not best_bowling_df.empty else 0

    if not bowler_df.empty and total_wickets > 0:
        summary += f"\n🎯 Bowling:\n"
        summary += f"- Total Wickets: {total_wickets}\n"
        summary += f"- Best Bowling (Match): {best_bowling} Wickets\n"
    else:
        summary += "\n🎯 Bowling:\n- No bowling data available.\n"

    return summary