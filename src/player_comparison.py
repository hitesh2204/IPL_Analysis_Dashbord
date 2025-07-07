import streamlit as st
import pandas as pd
from src.utils import get_image_path

def player_detailed_comparison(ipl):
    st.header("⚖️ Player Career Comparison", divider='rainbow')

    tab1, tab2 = st.tabs(["🧢 Batsman Comparison", "🎯 Bowler Comparison"])

    # ---------------------- 🧢 Batsman Comparison --------------------------
    with tab1:
        col1, col2 = st.columns(2)
        p1 = col1.selectbox("Select Batsman 1", sorted(ipl['batter'].unique()), key="bat1")
        p2 = col2.selectbox("Select Batsman 2", sorted(ipl['batter'].unique()), key="bat2")

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
        p1 = col1.selectbox("Select Bowler 1", sorted(ipl['bowler'].unique()), key="bowl1")
        p2 = col2.selectbox("Select Bowler 2", sorted(ipl['bowler'].unique()), key="bowl2")

        df1 = ipl[ipl['bowler'] == p1]
        df2 = ipl[ipl['bowler'] == p2]

        def get_bowler_stats(df, player):
            innings = df['ID'].nunique()
            balls = df['ballnumber'].count()
            overs = balls / 6
            runs_conceded = df['batsman_run'].sum()
            wickets = df[df['isWicketDelivery'] == 1].shape[0]  # ✅ Corrected total wickets
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
                st.metric("Wickets", stats["wickets"])  # ✅ Now shows correctly
                st.metric("Economy", stats["economy"])
                st.metric("5 Wicket Hauls", stats["5w_hauls"])

