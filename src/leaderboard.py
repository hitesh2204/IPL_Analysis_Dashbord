import pandas as pd
import streamlit as st
import altair as alt

def leaderboard_dashboard(ipl, season=None):
    st.markdown("## 🏆 IPL Leaderboard Dashboard")

    # 🎯 Season filtering
    available_seasons = sorted(ipl["Season"].dropna().unique())

    # If season is passed (from agent), use it — else show selector
    if season and season in available_seasons:
        selected_season = season
    else:
        selected_season = st.selectbox("📅 Select Season", available_seasons)

    # Filter data for selected season
    season_df = ipl[ipl["Season"] == selected_season]

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏏 Top Run Scorers", "🎯 Top Wicket Takers", "💥 Most Sixes",
        "🎯 Most Fours", "🚀 Best Strike Rate", "🛡️ Best Economy"
    ])

    # 1️⃣ Top Run Scorers
    with tab1:
        top_runs = season_df.groupby("batter")["batsman_run"].sum().sort_values(ascending=False).head(10).reset_index()
        st.altair_chart(alt.Chart(top_runs).mark_bar(color="#3498DB").encode(
            x=alt.X("batsman_run:Q", title="Runs"),
            y=alt.Y("batter:N", sort='-x', title="Batsman"),
            tooltip=["batter", "batsman_run"]
        ).properties(title=f"🏏 Top Run Scorers - {selected_season}", height=450), use_container_width=True)

    # 2️⃣ Top Wicket Takers
    with tab2:
        top_wickets = season_df[season_df['player_out'].notna()].groupby("bowler")["player_out"].count().sort_values(ascending=False).head(10).reset_index()
        st.altair_chart(alt.Chart(top_wickets).mark_bar(color="#E74C3C").encode(
            x=alt.X("player_out:Q", title="Wickets"),
            y=alt.Y("bowler:N", sort='-x', title="Bowler"),
            tooltip=["bowler", "player_out"]
        ).properties(title=f"🎯 Most Wickets - {selected_season}", height=450), use_container_width=True)

    # 3️⃣ Most Sixes
    with tab3:
        sixes = season_df[season_df['batsman_run'] == 6].groupby("batter").size().sort_values(ascending=False).head(10).reset_index(name='sixes')
        st.altair_chart(alt.Chart(sixes).mark_bar(color="#9B59B6").encode(
            x=alt.X("sixes:Q", title="Sixes"),
            y=alt.Y("batter:N", sort='-x'),
            tooltip=["batter", "sixes"]
        ).properties(title=f"💥 Most Sixes - {selected_season}", height=450), use_container_width=True)

    # 4️⃣ Most Fours
    with tab4:
        fours = season_df[season_df['batsman_run'] == 4].groupby("batter").size().sort_values(ascending=False).head(10).reset_index(name='fours')
        st.altair_chart(alt.Chart(fours).mark_bar(color="#F39C12").encode(
            x=alt.X("fours:Q", title="Fours"),
            y=alt.Y("batter:N", sort='-x'),
            tooltip=["batter", "fours"]
        ).properties(title=f"🎯 Most Fours - {selected_season}", height=450), use_container_width=True)

    # 5️⃣ Best Strike Rate (min 100 balls)
    with tab5:
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

    # 6️⃣ Best Economy (min 100 balls)
    with tab6:
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
