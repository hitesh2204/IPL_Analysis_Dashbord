# 🧠 GENAI FUNCTION — Used by LangChain Agent
def get_leaderboard_summary(query: str, ipl_df) -> str:
    query = query.lower()

    # Extract season if available
    import re
    season_match = re.search(r'\b(20\d{2})\b', query)
    season = int(season_match.group(1)) if season_match else None

    filtered_df = ipl_df[ipl_df["Season"] == season] if season else ipl_df

    if "bat" in query or "run" in query:
        top_batsmen = (
            filtered_df.groupby("batter")["batsman_run"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        result = "🏏 Top Batsmen:\n"
        for i, (player, runs) in enumerate(top_batsmen.items(), 1):
            result += f"{i}. {player}: {runs} runs\n"

    elif "bowl" in query or "wicket" in query:
        wickets_df = filtered_df[filtered_df["isWicketDelivery"] == 1]
        top_bowlers = (
            wickets_df.groupby("bowler")["player_out"]
            .count()
            .sort_values(ascending=False)
            .head(10)
        )
        result = "🎯 Top Bowlers:\n"
        for i, (player, wkts) in enumerate(top_bowlers.items(), 1):
            result += f"{i}. {player}: {wkts} wickets\n"

    else:
        result = "Please mention 'batting' or 'bowling' in your query."

    return result