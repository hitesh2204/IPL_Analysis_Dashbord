import streamlit as st
import pandas as pd
from src.utils import get_image_path
from logger import setup_logger
import re

logger = setup_logger()

def player_detailed_comparison(ipl, bat1=None, bat2=None, bowl1=None, bowl2=None):
    try:
        st.header("⚖️ Player Career Comparison", divider='rainbow')
        tab1, tab2 = st.tabs(["🧢 Batsman Comparison", "🎯 Bowler Comparison"])

        # ---------------------- 🧢 Batsman Comparison --------------------------
        with tab1:
            try:
                col1, col2 = st.columns(2)
                p1 = bat1 if bat1 else col1.selectbox("Select Batsman 1", sorted(ipl['batter'].unique()), key="bat1")
                p2 = bat2 if bat2 else col2.selectbox("Select Batsman 2", sorted(ipl['batter'].unique()), key="bat2")

                logger.info(f"Selected batsmen: {p1} vs {p2}")

                if p1 == p2:
                    st.warning("Please select two different batsmen.")
                    logger.warning("Same batsman selected for both sides.")
                    return

                df1 = ipl[ipl['batter'] == p1]
                df2 = ipl[ipl['batter'] == p2]

                def get_batsman_stats(df, player):
                    try:
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
                    except Exception as e:
                        logger.exception(f"Error calculating stats for batsman {player}: {e}")
                        return {}

                stats1 = get_batsman_stats(df1, p1)
                stats2 = get_batsman_stats(df2, p2)

                st.markdown("### 📊 Batsman Stats Side-by-Side")
                c1, c2 = st.columns(2)
                for col, stats in zip([c1, c2], [stats1, stats2]):
                    with col:
                        img_path = get_image_path(stats.get("player", ""))
                        if img_path:
                            st.image(img_path, width=120, caption=stats["player"])
                        st.metric("Matches", stats.get("innings", 0))
                        st.metric("Runs", stats.get("runs", 0))
                        st.metric("Strike Rate", stats.get("strike_rate", 0.0))
                        st.metric("Fours", stats.get("fours", 0))
                        st.metric("Sixes", stats.get("sixes", 0))
                        st.metric("50s", stats.get("50s", 0))
                        st.metric("100s", stats.get("100s", 0))
            except Exception as e:
                logger.exception(f"Error in batsman comparison tab: {e}")
                st.error("An error occurred while comparing batsmen.")

        # ---------------------- 🎯 Bowler Comparison --------------------------
        with tab2:
            try:
                col1, col2 = st.columns(2)
                p1 = bowl1 if bowl1 else col1.selectbox("Select Bowler 1", sorted(ipl['bowler'].unique()), key="bowl1")
                p2 = bowl2 if bowl2 else col2.selectbox("Select Bowler 2", sorted(ipl['bowler'].unique()), key="bowl2")

                logger.info(f"Selected bowlers: {p1} vs {p2}")

                if p1 == p2:
                    st.warning("Please select two different bowlers.")
                    logger.warning("Same bowler selected for both sides.")
                    return

                df1 = ipl[ipl['bowler'] == p1]
                df2 = ipl[ipl['bowler'] == p2]

                def get_bowler_stats(df, player):
                    try:
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
                    except Exception as e:
                        logger.exception(f"Error calculating stats for bowler {player}: {e}")
                        return {}

                stats1 = get_bowler_stats(df1, p1)
                stats2 = get_bowler_stats(df2, p2)

                st.markdown("### 📊 Bowler Stats Side-by-Side")
                c1, c2 = st.columns(2)
                for col, stats in zip([c1, c2], [stats1, stats2]):
                    with col:
                        img_path = get_image_path(stats.get("player", ""))
                        if img_path:
                            st.image(img_path, width=120, caption=stats["player"])
                        st.metric("Matches", stats.get("innings", 0))
                        st.metric("Overs", stats.get("overs", 0.0))
                        st.metric("Wickets", stats.get("wickets", 0))
                        st.metric("Economy", stats.get("economy", 0.0))
                        st.metric("5 Wicket Hauls", stats.get("5w_hauls", 0))
            except Exception as e:
                logger.exception(f"Error in bowler comparison tab: {e}")
                st.error("An error occurred while comparing bowlers.")

    except Exception as e:
        logger.exception(f"Top-level error in player_detailed_comparison: {e}")
        st.error("Something went wrong while rendering the comparison.")
