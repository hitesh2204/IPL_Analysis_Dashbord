import streamlit as st
import pandas as pd
from src.utils import get_image_path # Optional
from src.data_loader import load_ipl_data

def player_summary_page(ipl):
    
    st.markdown("## 👤 Player Career Summary")

    selected_player = st.session_state.get('selected_player')

    # 🧠 If not from agent, show dropdown
    if not selected_player:
        players = sorted(ipl['batter'].unique())
        col1, col2 = st.columns([4, 1])
        with col1:
            selected_player = st.selectbox("Select Player", players)
        with col2:
            img = get_image_path(selected_player)
            if img:
                st.image(img, width=100)
    else:
        st.markdown(f"### 🏏 Stats for **{selected_player}**")
        img = get_image_path(selected_player)
        if img:
            st.image(img, width=120)

    # Rest of your logic stays exactly the same 👇
    player_df = ipl[ipl['batter'] == selected_player]
    bowler_df = ipl[ipl['bowler'] == selected_player]
    full_df = pd.concat([player_df, bowler_df]).drop_duplicates()

    if player_df.empty and bowler_df.empty:
        st.warning("No data found for this player.")
        return

    total_runs = player_df['batsman_run'].sum()
    total_balls = player_df.shape[0]
    total_fours = player_df[player_df['batsman_run'] == 4].shape[0]
    total_sixes = player_df[player_df['batsman_run'] == 6].shape[0]
    total_outs = ipl[ipl['player_out'] == selected_player].shape[0]
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0

    match_runs = player_df.groupby('ID')['batsman_run'].sum()
    highest_score = match_runs.max() if not match_runs.empty else 0
    fifties = match_runs[(match_runs >= 50) & (match_runs < 100)].count()
    hundreds = match_runs[match_runs >= 100].count()

    st.markdown("### 🏏 Batting Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Runs", total_runs)
    col2.metric("Balls Faced", total_balls)
    col3.metric("Strike Rate", f"{strike_rate:.2f}")
    col4, col5, col6 = st.columns(3)
    col4.metric("4s", total_fours)
    col5.metric("6s", total_sixes)
    col6.metric("Dismissals", total_outs)
    col7, col8, col9 = st.columns(3)
    col7.metric("Highest Score", highest_score)
    col8.metric("50s", fifties)
    col9.metric("100s", hundreds)

    dismissals = bowler_df[bowler_df['isWicketDelivery'] == 1]
    total_wickets = dismissals['player_out'].notnull().sum()
    best_bowling_df = dismissals.groupby('ID')['player_out'].count()
    best_bowling = best_bowling_df.max() if not best_bowling_df.empty else 0

    if not bowler_df.empty and total_wickets > 0:
        st.markdown("### 🎯 Bowling Stats")
        col_b1, col_b2 = st.columns(2)
        col_b1.metric("🏹 Total Wickets", total_wickets)
        col_b2.metric("🥇 Best Bowling (Match)", f"{best_bowling} Wkts")
    else:
        st.info("ℹ️ This player has no bowling data.")

    st.markdown("### 🧢 Teams Played For")
    batting_teams = ipl[ipl['batter'] == selected_player]['BattingTeam'].unique()
    bowling_teams = ipl[ipl['bowler'] == selected_player]['BowlingTeam'].unique()
    teams_played = sorted(set(batting_teams).union(set(bowling_teams)))
    st.write(", ".join(teams_played) if teams_played else "No teams found.")


    if not player_df.empty:
        st.markdown("### 📊 Season-wise Runs")
        season_wise = player_df.groupby('Season')['batsman_run'].sum().reset_index()
        st.bar_chart(season_wise.set_index("Season"))

#### Newly added function for Langchian Agent only.

# 🧠 GENAI FUNCTION — Used by LangChain Agent
def get_player_summary(player_name: str) -> str:
    ipl = load_ipl_data()

    player_df = ipl[ipl['batter'] == player_name]
    bowler_df = ipl[ipl['bowler'] == player_name]
    full_df = pd.concat([player_df, bowler_df]).drop_duplicates()

    if player_df.empty and bowler_df.empty:
        return f"No data found for {player_name}."

    total_runs = player_df['batsman_run'].sum()
    total_balls = player_df.shape[0]
    total_fours = player_df[player_df['batsman_run'] == 4].shape[0]
    total_sixes = player_df[player_df['batsman_run'] == 6].shape[0]
    total_outs = ipl[ipl['player_out'] == player_name].shape[0]
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0

    match_runs = player_df.groupby('ID')['batsman_run'].sum()
    highest_score = match_runs.max() if not match_runs.empty else 0
    fifties = match_runs[(match_runs >= 50) & (match_runs < 100)].count()
    hundreds = match_runs[match_runs >= 100].count()

    summary = f"📊 **IPL Career Summary of {player_name}**\n\n"
    summary += f"🏏 Batting:\n"
    summary += f"- Total Runs: {total_runs}\n"
    summary += f"- Balls Faced: {total_balls}\n"
    summary += f"- 4s: {total_fours}, 6s: {total_sixes}\n"
    summary += f"- Strike Rate: {strike_rate:.2f}\n"
    summary += f"- Highest Score: {highest_score}\n"
    summary += f"- 50s: {fifties}, 100s: {hundreds}\n"
    summary += f"- Dismissals: {total_outs}\n"

    dismissals = bowler_df[bowler_df['isWicketDelivery'] == 1]
    total_wickets = dismissals['player_out'].notnull().sum()
    best_bowling_df = dismissals.groupby('ID')['player_out'].count()
    best_bowling = best_bowling_df.max() if not best_bowling_df.empty else 0

    if not bowler_df.empty and total_wickets > 0:
        summary += f"\n🎯 Bowling:\n"
        summary += f"- Total Wickets: {total_wickets}\n"
        summary += f"- Best Bowling (Match): {best_bowling} Wickets\n"
    else:
        summary += "\n🎯 Bowling:\n- No bowling data available.\n"

    return summary