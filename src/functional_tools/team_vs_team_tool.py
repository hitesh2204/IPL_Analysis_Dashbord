import pandas as pd

# 🧠 GENAI FUNCTION — Used by LangChain Agent
def get_team_vs_team_summary(team1: str, team2: str, ipl: pd.DataFrame) -> str:
    matches = ipl[((ipl['Team1'] == team1) & (ipl['Team2'] == team2)) |
                  ((ipl['Team1'] == team2) & (ipl['Team2'] == team1))]

    if matches.empty:
        return f"No head-to-head records found between {team1} and {team2}."

    total_matches = matches['ID'].nunique()
    team1_wins = matches[matches['WinningTeam'] == team1]['ID'].nunique()
    team2_wins = matches[matches['WinningTeam'] == team2]['ID'].nunique()

    top_batsmen_df = matches.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(5)
    top_batsmen_text = "\n".join([f"{i+1}. {name} ({runs} runs)" for i, (name, runs) in enumerate(top_batsmen_df.items())])

    dismissals = matches[matches['isWicketDelivery'] == 1]
    top_bowlers_df = dismissals[dismissals['player_out'].notnull()].groupby('bowler')['player_out'].count().sort_values(ascending=False).head(5)
    top_bowlers_text = "\n".join([f"{i+1}. {name} ({wkts} wickets)" for i, (name, wkts) in enumerate(top_bowlers_df.items())])

    highest_score = matches.groupby('ID')['total_run'].sum().max()

    match_scores = matches.groupby(['ID', 'batter'])['batsman_run'].sum().reset_index()
    top_individual = match_scores.sort_values(by='batsman_run', ascending=False).iloc[0]
    best_batsman = top_individual['batter']
    best_score = top_individual['batsman_run']

    summary = (
        f"🏏 Head-to-Head: {team1} vs {team2}\n\n"
        f"• Total Matches: {total_matches}\n"
        f"• {team1} Wins: {team1_wins}\n"
        f"• {team2} Wins: {team2_wins}\n"
        f"• Highest Team Score: {highest_score} runs\n"
        f"• Best Individual Score: {best_batsman} ({best_score} runs)\n\n"
        f"🔥 Top 5 Batsmen:\n{top_batsmen_text}\n\n"
        f"🎯 Top 5 Bowlers:\n{top_bowlers_text}"
    )

    return summary