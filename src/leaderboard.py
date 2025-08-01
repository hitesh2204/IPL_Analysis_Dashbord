import pandas as pd
import streamlit as st
import altair as alt
from logger import setup_logger

logger = setup_logger()

def leaderboard_dashboard(ipl, season=None):
    try:
        st.markdown("## 🏆 IPL Leaderboard Dashboard")

        # 🎯 Season filtering
        available_seasons = sorted(ipl["Season"].dropna().unique())
        logger.info("Available seasons extracted successfully.")

        # If season is passed (from agent), use it — else show selector
        if season and season in available_seasons:
            selected_season = season
            logger.info(f"Season selected from agent: {selected_season}")
        else:
            selected_season = st.selectbox("📅 Select Season", available_seasons)
            logger.info(f"Season selected by user: {selected_season}")

        # Filter data
        season_df = ipl[ipl["Season"] == selected_season]

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏏 Top Run Scorers", "🎯 Top Wicket Takers", "💥 Most Sixes",
            "🎯 Most Fours", "🚀 Best Strike Rate", "🛡️ Best Economy"
        ])

        # 1️⃣ Top Run Scorers
        with tab1:
            try:
                top_runs = season_df.groupby("batter")["batsman_run"].sum().sort_values(ascending=False).head(10).reset_index()
                chart = alt.Chart(top_runs).mark_bar(color="#3498DB").encode(
                    x=alt.X("batsman_run:Q", title="Runs"),
                    y=alt.Y("batter:N", sort='-x', title="Batsman"),
                    tooltip=["batter", "batsman_run"]
                ).properties(title=f"🏏 Top Run Scorers - {selected_season}", height=450)
                st.altair_chart(chart, use_container_width=True)
            except Exception as e:
                logger.exception("Failed to generate Top Run Scorers chart.")
                st.error("Error loading Top Run Scorers.")

        # 2️⃣ Top Wicket Takers
        with tab2:
            try:
                top_wickets = season_df[season_df['player_out'].notna()].groupby("bowler")["player_out"].count().sort_values(ascending=False).head(10).reset_index()
                chart = alt.Chart(top_wickets).mark_bar(color="#E74C3C").encode(
                    x=alt.X("player_out:Q", title="Wickets"),
                    y=alt.Y("bowler:N", sort='-x', title="Bowler"),
                    tooltip=["bowler", "player_out"]
                ).properties(title=f"🎯 Most Wickets - {selected_season}", height=450)
                st.altair_chart(chart, use_container_width=True)
            except Exception as e:
                logger.exception("Failed to generate Top Wicket Takers chart.")
                st.error("Error loading Wicket Takers.")

        # 3️⃣ Most Sixes
        with tab3:
            try:
                sixes = season_df[season_df['batsman_run'] == 6].groupby("batter").size().sort_values(ascending=False).head(10).reset_index(name='sixes')
                chart = alt.Chart(sixes).mark_bar(color="#9B59B6").encode(
                    x=alt.X("sixes:Q", title="Sixes"),
                    y=alt.Y("batter:N", sort='-x'),
                    tooltip=["batter", "sixes"]
                ).properties(title=f"💥 Most Sixes - {selected_season}", height=450)
                st.altair_chart(chart, use_container_width=True)
            except Exception as e:
                logger.exception("Failed to generate Most Sixes chart.")
                st.error("Error loading Most Sixes.")

        # 4️⃣ Most Fours
        with tab4:
            try:
                fours = season_df[season_df['batsman_run'] == 4].groupby("batter").size().sort_values(ascending=False).head(10).reset_index(name='fours')
                chart = alt.Chart(fours).mark_bar(color="#F39C12").encode(
                    x=alt.X("fours:Q", title="Fours"),
                    y=alt.Y("batter:N", sort='-x'),
                    tooltip=["batter", "fours"]
                ).properties(title=f"🎯 Most Fours - {selected_season}", height=450)
                st.altair_chart(chart, use_container_width=True)
            except Exception as e:
                logger.exception("Failed to generate Most Fours chart.")
                st.error("Error loading Most Fours.")

        # 5️⃣ Best Strike Rate
        with tab5:
            try:
                balls = season_df.groupby("batter")["ballnumber"].count()
                runs = season_df.groupby("batter")["batsman_run"].sum()
                strike_rate_df = pd.DataFrame({
                    "batter": runs.index,
                    "runs": runs.values,
                    "balls": balls.values,
                    "strike_rate": (runs.values / balls.values) * 100
                })
                filtered = strike_rate_df[strike_rate_df["balls"] > 100].sort_values("strike_rate", ascending=False).head(10)
                st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
            except Exception as e:
                logger.exception("Failed to calculate Best Strike Rate.")
                st.error("Error calculating Strike Rate.")

        # 6️⃣ Best Economy
        with tab6:
            try:
                total_runs = season_df.groupby("bowler")["batsman_run"].sum()
                total_balls = season_df.groupby("bowler")["ballnumber"].count()
                economy_df = pd.DataFrame({
                    "bowler": total_runs.index,
                    "runs_conceded": total_runs.values,
                    "balls": total_balls.values,
                    "economy": total_runs.values / (total_balls.values / 6)
                })
                filtered = economy_df[economy_df["balls"] > 100].sort_values("economy").head(10)
                st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
            except Exception as e:
                logger.exception("Failed to calculate Best Economy.")
                st.error("Error calculating Economy.")
    except Exception as e:
        logger.exception("An error occurred in leaderboard_dashboard.")
        st.error("Something went wrong while loading the dashboard.")
