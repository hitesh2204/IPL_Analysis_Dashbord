def get_tournament_summary(season: str, ipl_df) -> str:
    try:
        season = int(season.strip())
        season_df = ipl_df[ipl_df["Season"] == season]

        if season_df.empty:
            return f"No data found for the {season} IPL season."

        total_matches = season_df["ID"].nunique()
        venues = season_df["Venue"].value_counts()
        most_used_venue = venues.idxmax() if not venues.empty else "Unknown"

        # Final match (last match of the season)
        final_match = season_df.sort_values("ID").dropna(subset=["WinningTeam"]).iloc[-1]
        winner = final_match["WinningTeam"]
        teams_in_final = [final_match["Team1"], final_match["Team2"]]
        runner_up = teams_in_final[0] if teams_in_final[1] == winner else teams_in_final[1]

        # Orange Cap (most runs)
        top_batsman_stats = (
            season_df.groupby("batter")["batsman_run"].sum().sort_values(ascending=False)
        )
        top_batsman = top_batsman_stats.index[0]
        top_batsman_runs = top_batsman_stats.values[0]

        # Purple Cap (most wickets)
        top_bowler_stats = (
            season_df[season_df["isWicketDelivery"] == 1]
            .groupby("bowler")["player_out"]
            .count()
            .sort_values(ascending=False)
        )
        top_bowler = top_bowler_stats.index[0]
        top_bowler_wkts = top_bowler_stats.values[0]

        summary = f"""📅 IPL {season} Summary:

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
