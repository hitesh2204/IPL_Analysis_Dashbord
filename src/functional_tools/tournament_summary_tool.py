import pandas as pd

def get_tournament_summary(season: str, ipl_df) -> str:
    try:
        # ✅ Case 1: Summary across all seasons
        if season.lower().strip() == "all":
            winners = (
                ipl_df.dropna(subset=["WinningTeam"])
                .sort_values(["Season", "Date"])
                .groupby("Season")
                .tail(1)[["Season", "WinningTeam"]]
            )
            return "🏆 IPL Winners by Season:\n" + "\n".join(
                [f"{int(row['Season'])}: {row['WinningTeam']}" for _, row in winners.iterrows()]
            )

        # ✅ Case 2: Single season summary
        season = int(season.strip())
        season_df = ipl_df[ipl_df["Season"] == season].copy()

        if season_df.empty:
            return f"No data found for the {season} IPL season."

        total_matches = season_df["ID"].nunique()

        # Most used venue
        venues = season_df["Venue"].value_counts()
        most_used_venue = venues.idxmax() if not venues.empty else "Unknown"

        # Convert to datetime safely
        season_df["Date"] = pd.to_datetime(season_df["Date"], errors="coerce")

        # ✅ Pick last match with a valid winner
        completed_matches = season_df.dropna(subset=["WinningTeam"])
        if completed_matches.empty:
            return f"IPL {season} season data is incomplete (no winner recorded)."

        final_match = completed_matches.sort_values("Date").iloc[-1]

        winner = final_match["WinningTeam"]
        teams_in_final = [final_match["Team1"], final_match["Team2"]]
        runner_up = teams_in_final[0] if teams_in_final[1] == winner else teams_in_final[1]

        # Orange Cap
        top_batsman_stats = (
            season_df.groupby("batter")["batsman_run"].sum().sort_values(ascending=False)
        )
        top_batsman = top_batsman_stats.index[0]
        top_batsman_runs = top_batsman_stats.values[0]

        # Purple Cap
        top_bowler_stats = (
            season_df[season_df["isWicketDelivery"] == 1]
            .groupby("bowler")["player_out"]
            .count()
            .sort_values(ascending=False)
        )
        top_bowler = top_bowler_stats.index[0]
        top_bowler_wkts = top_bowler_stats.values[0]

        summary = f"""IPL {season} Summary:

    Champion: {winner}
    Runner-Up: {runner_up}
    Total Matches: {total_matches}
    Final Venue: {final_match['Venue']}

    Orange Cap: {top_batsman} ({top_batsman_runs} runs)
    Purple Cap: {top_bowler} ({top_bowler_wkts} wickets)
"""
        return summary

    except Exception as e:
        return f"Error in generating tournament summary: {str(e)}"
