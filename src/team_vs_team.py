import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import os
from PIL import Image

def team_vs_team_page(ipl):
    st.markdown("## 🤜 Team vs Team Analysis")

    # Get team names from data
    teams = sorted(set(ipl['Team1'].unique()).union(set(ipl['Team2'].unique())))

    # 🔄 Hybrid Mode: Use session_state input if set
    team1 = st.session_state.get("selected_team1")
    team2 = st.session_state.get("selected_team2")

    if not team1 or not team2:
        col1, col2 = st.columns(2)
        with col1:
            team1 = st.selectbox("Select Team 1", teams, key="team1_select")
        with col2:
            team2 = st.selectbox("Select Team 2", teams, key="team2_select")

    if team1 == team2:
        st.warning("Please select two different teams.")
        return

    # ✅ Show team logos side-by-side
    logo1_path = f"image-video/{team1.replace(' ', '_').lower()}.jpeg"
    logo2_path = f"image-video/{team2.replace(' ', '_').lower()}.jpeg"

    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists(logo1_path):
            col1.image(Image.open(logo1_path), caption=team1, width=150)
    with col2:
        if os.path.exists(logo2_path):
            col2.image(Image.open(logo2_path), caption=team2, width=150)

    # Filter matches between the two teams
    df = ipl[((ipl['Team1'] == team1) & (ipl['Team2'] == team2)) |
             ((ipl['Team1'] == team2) & (ipl['Team2'] == team1))]

    total_matches = df['ID'].nunique()
    st.subheader(f"📅 Total Matches Played: {total_matches}")

    # 🏆 Match wins
    win_df = df[['ID', 'WinningTeam']].drop_duplicates()
    team1_wins = win_df[win_df['WinningTeam'] == team1].shape[0]
    team2_wins = win_df[win_df['WinningTeam'] == team2].shape[0]

    col1, col2 = st.columns(2)
    col1.metric(f"{team1} Wins", team1_wins)
    col2.metric(f"{team2} Wins", team2_wins)

    # Pie + Bar chart
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🥧 Win Distribution")
        win_counts = pd.Series({team1: team1_wins, team2: team2_wins})
        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        ax.pie(win_counts, labels=win_counts.index, autopct='%1.1f%%',
               startangle=50, colors=['#3498DB', '#E74C3C'])
        ax.axis('equal')
        st.pyplot(fig)

    with col2:
        st.markdown("#### 🏏 Total Runs Scored")
        run_summary = df.groupby('BattingTeam')['total_run'].sum().reset_index()
        chart = alt.Chart(run_summary).mark_bar().encode(
            x=alt.X('BattingTeam:N', title='Team'),
            y=alt.Y('total_run:Q', title='Total Runs'),
            tooltip=['BattingTeam', 'total_run'],
            color='BattingTeam:N'
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

    # 🔥 Top Batsmen
    st.subheader("🔥 Top Batsmen")
    top_batsmen = df[df['BattingTeam'].isin([team1, team2])] \
        .groupby('batter')['batsman_run'].sum() \
        .sort_values(ascending=False).head(5).reset_index()
    st.dataframe(top_batsmen)

    # 🎯 Top Bowlers
    st.subheader("🎯 Top Bowlers")
    top_bowlers = df[df['isWicketDelivery'] == 1] \
        .groupby('bowler')['player_out'].count() \
        .sort_values(ascending=False).head(5).reset_index()
    st.dataframe(top_bowlers)

    # 📈 Year-wise run trend
    if 'Season' in df.columns:
        st.subheader("📊 Yearly Runs Trend")
        trend = df.groupby(['Season', 'BattingTeam'])['total_run'].sum().reset_index()
        chart = alt.Chart(trend).mark_line(point=True).encode(
            x='Season:O',
            y='total_run:Q',
            color='BattingTeam:N',
            tooltip=['Season', 'BattingTeam', 'total_run']
        ).properties(title="Yearly Runs Comparison", height=400)
        st.altair_chart(chart, use_container_width=True)

    # 🧠 Bonus: Strike Rate
    st.subheader("⚔️ Top Rivalry Batsman Strike Rates (min 30 balls)")
    strike_df = df.groupby('batter').agg(
        runs=('batsman_run', 'sum'),
        balls=('ballnumber', 'count')
    ).reset_index()
    strike_df = strike_df[strike_df['balls'] >= 30]
    strike_df['Strike Rate'] = (strike_df['runs'] / strike_df['balls']) * 100
    top_strike = strike_df.sort_values("Strike Rate", ascending=False).head(5)
    st.dataframe(top_strike)
