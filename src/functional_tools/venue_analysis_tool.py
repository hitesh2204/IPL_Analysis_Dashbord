
# 🧠-GENAI FUNCTION — Used by LangChain Agent
def get_venue_summary(ipl, venue_query: str) -> str:
    venue = venue_query.strip()

    df = ipl[ipl['Venue'].str.lower() == venue.lower()]
    if df.empty:
        return f"No data found for venue '{venue}'."

    total_matches = df['ID'].nunique()

    # Innings-wise average scores
    first_innings = df[df['innings'] == 1].groupby('ID')['total_run'].sum()
    second_innings = df[df['innings'] == 2].groupby('ID')['total_run'].sum()
    avg_score_1 = first_innings.mean()
    avg_score_2 = second_innings.mean()

    # Total runs, 4s, and 6s
    total_runs = df['batsman_run'].sum()
    total_fours = df[df['batsman_run'] == 4].shape[0]
    total_sixes = df[df['batsman_run'] == 6].shape[0]

    # Match win analysis
    match_results = df.groupby('ID').agg({
        'BattingTeam': 'first',
        'WinningTeam': 'first',
        'innings': 'max'
    }).reset_index()
    bat_first_win = match_results[match_results['WinningTeam'] == match_results['BattingTeam']].shape[0]
    chase_win = total_matches - bat_first_win

    # Top 5 teams by win
    team_wins = df.groupby('WinningTeam')['ID'].nunique().sort_values(ascending=False).head(3)

    # Top 5 batsmen
    top_batsmen = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(5)

    # Top 5 bowlers
    top_bowlers = df[df['isWicketDelivery'] == 1].groupby('bowler')['player_out'].count().sort_values(ascending=False).head(5)

    return (
        f"🏟️ **Venue Summary: {venue}**\n\n"
        f"• Total Matches: {total_matches}\n"
        f"• Avg 1st Innings Score: {avg_score_1:.2f}\n"
        f"• Avg 2nd Innings Score: {avg_score_2:.2f}\n"
        f"• Total Runs Scored: {total_runs}\n"
        f"• Total Fours: {total_fours} | Total Sixes: {total_sixes}\n"
        f"• Bat First Wins: {bat_first_win} | Chasing Wins: {chase_win}\n\n"

        f"🏆 **Top Teams (by Wins)**:\n" +
        "\n".join([f"- {team}: {wins} wins" for team, wins in team_wins.items()]) + "\n\n"

        f"🔥 **Top 5 Batsmen at {venue}**:\n" +
        "\n".join([f"- {batsman}: {runs} runs" for batsman, runs in top_batsmen.items()]) + "\n\n"

        f"🎯 **Top 5 Bowlers at {venue}**:\n" +
        "\n".join([f"- {bowler}: {wkts} wickets" for bowler, wkts in top_bowlers.items()])
    )
