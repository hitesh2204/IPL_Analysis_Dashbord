# src/tournament_summary.py
import streamlit as st
import pandas as pd
from src.tournament_summary_data import tournament_summary

## Streamlit UI for tournament summary.
def tournament_summary_page():
    st.header("🏆 IPL Tournament Summary (2008 - 2024)", divider="rainbow")
    
    df = pd.DataFrame(tournament_summary).sort_values("Season", ascending=False)
    
    st.dataframe(df, use_container_width=True)

    st.markdown("You can sort columns, filter by year, or export as CSV if needed.")

# 🧠-GENAI FUNCTION — Used by LangChain Agent
def get_tournament_summary(season: str, ipl_df) -> str:
    try:
        season = int(season.strip())
        season_df = ipl_df[ipl_df["Season"] == season]

        if season_df.empty:
            return f"No data found for the {season} IPL season."

        total_matches = season_df["ID"].nunique()
        winner = season_df["WinningTeam"].value_counts().idxmax()
        venues = season_df["Venue"].value_counts()
        most_used_venue = venues.idxmax() if not venues.empty else "Unknown"

        # Top batsman
        top_batsman = (
            season_df.groupby("batter")["batsman_run"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
            .index[0]
        )
        top_batsman_runs = (
            season_df.groupby("batter")["batsman_run"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
            .values[0]
        )

        # Top bowler
        top_bowler = (
            season_df[season_df["isWicketDelivery"] == 1]
            .groupby("bowler")["player_out"]
            .count()
            .sort_values(ascending=False)
            .head(1)
            .index[0]
        )
        top_bowler_wkts = (
            season_df[season_df["isWicketDelivery"] == 1]
            .groupby("bowler")["player_out"]
            .count()
            .sort_values(ascending=False)
            .head(1)
            .values[0]
        )

        summary = f"""📅 IPL {season} Summary:

                    🏆 Winner: {winner}
                    📊 Total Matches: {total_matches}
                    🏟️ Most Used Venue: {most_used_venue}

                    🧢 Orange Cap: {top_batsman} ({top_batsman_runs} runs)
                    🎯 Purple Cap: {top_bowler} ({top_bowler_wkts} wickets)
                """
        return summary

    except Exception as e:
        return f"Error in generating tournament summary: {str(e)}"

