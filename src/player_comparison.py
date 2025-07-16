import streamlit as st
import pandas as pd
from src.utils import get_image_path
import re

## Streamlit UI function for player comparison.
def player_detailed_comparison(ipl, bat1=None, bat2=None, bowl1=None, bowl2=None):
    st.header("⚖️ Player Career Comparison", divider='rainbow')
    tab1, tab2 = st.tabs(["🧢 Batsman Comparison", "🎯 Bowler Comparison"])

    # ---------------------- 🧢 Batsman Comparison --------------------------
    with tab1:
        col1, col2 = st.columns(2)
        p1 = bat1 if bat1 else col1.selectbox("Select Batsman 1", sorted(ipl['batter'].unique()), key="bat1")
        p2 = bat2 if bat2 else col2.selectbox("Select Batsman 2", sorted(ipl['batter'].unique()), key="bat2")

        if p1 == p2:
            st.warning("Please select two different batsmen.")
            return

        df1 = ipl[ipl['batter'] == p1]
        df2 = ipl[ipl['batter'] == p2]

        def get_batsman_stats(df, player):
            total_runs = df['batsman_run'].sum()
            balls = df.shape[0]
            fours = df[df['batsman_run'] == 4].shape[0]
            sixes = df[df['batsman_run'] == 6].shape[0]
            innings = df['ID'].nunique()
            strike_rate = (total_runs / balls) * 100 if balls > 0 else 0
            fifties = df.groupby('ID')['batsman_run'].sum()
            num_50s = fifties[(fifties >= 50) & (fifties < 100)].count()
            num_100s = fifties[fifties >= 100].count()
            return {
                "player": player,
                "innings": innings,
                "runs": total_runs,
                "strike_rate": round(strike_rate, 2),
                "fours": fours,
                "sixes": sixes,
                "50s": num_50s,
                "100s": num_100s
            }

        stats1 = get_batsman_stats(df1, p1)
        stats2 = get_batsman_stats(df2, p2)

        st.markdown("### 📊 Batsman Stats Side-by-Side")
        c1, c2 = st.columns(2)
        for col, stats in zip([c1, c2], [stats1, stats2]):
            with col:
                img_path = get_image_path(stats["player"])
                if img_path:
                    st.image(img_path, width=120, caption=stats["player"])
                st.metric("Matches", stats["innings"])
                st.metric("Runs", stats["runs"])
                st.metric("Strike Rate", stats["strike_rate"])
                st.metric("Fours", stats["fours"])
                st.metric("Sixes", stats["sixes"])
                st.metric("50s", stats["50s"])
                st.metric("100s", stats["100s"])

    # ---------------------- 🎯 Bowler Comparison --------------------------
    with tab2:
        col1, col2 = st.columns(2)
        p1 = bowl1 if bowl1 else col1.selectbox("Select Bowler 1", sorted(ipl['bowler'].unique()), key="bowl1")
        p2 = bowl2 if bowl2 else col2.selectbox("Select Bowler 2", sorted(ipl['bowler'].unique()), key="bowl2")

        if p1 == p2:
            st.warning("Please select two different bowlers.")
            return

        df1 = ipl[ipl['bowler'] == p1]
        df2 = ipl[ipl['bowler'] == p2]

        def get_bowler_stats(df, player):
            innings = df['ID'].nunique()
            balls = df['ballnumber'].count()
            overs = balls / 6
            runs_conceded = df['batsman_run'].sum()
            wickets = df[df['isWicketDelivery'] == 1].shape[0]
            economy = (runs_conceded / overs) if overs > 0 else 0
            five_wkts = df[df['isWicketDelivery'] == 1].groupby('ID').size()
            five_wkts = five_wkts[five_wkts >= 5].count()

            return {
                "player": player,
                "innings": innings,
                "overs": round(overs, 1),
                "wickets": wickets,
                "economy": round(economy, 2),
                "5w_hauls": five_wkts
            }

        stats1 = get_bowler_stats(df1, p1)
        stats2 = get_bowler_stats(df2, p2)

        st.markdown("### 📊 Bowler Stats Side-by-Side")
        c1, c2 = st.columns(2)
        for col, stats in zip([c1, c2], [stats1, stats2]):
            with col:
                img_path = get_image_path(stats["player"])
                if img_path:
                    st.image(img_path, width=120, caption=stats["player"])
                st.metric("Matches", stats["innings"])
                st.metric("Overs", stats["overs"])
                st.metric("Wickets", stats["wickets"])
                st.metric("Economy", stats["economy"])
                st.metric("5 Wicket Hauls", stats["5w_hauls"])


# 🧠 GENAI FUNCTION — Used by LangChain Agent
def get_player_comparison(player_query: str, ipl_df) -> str:

    # Extract player names
    players = re.split(r",|\s+and\s+|\s+vs\s+", player_query, flags=re.IGNORECASE)
    players = [p.strip() for p in players if p.strip()]
    
    if len(players) < 2:
        return "❌ Please provide at least two player names to compare, like 'Kohli, Rohit and Dhoni'."

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
        five_wkts = dismissals.groupby("ID")["player_out"].count()
        five_wkt_hauls = (five_wkts >= 5).sum()

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
