import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import os
from PIL import Image

def team_vs_team_analysis(ipl, team1, team2):
    st.header(f"🤜 {team1} vs {team2} Analysis", divider="rainbow")

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

    # ✅ Filter matches between the 2 teams
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

    # 🥧 Pie chart + bar chart (side-by-side)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🥧 Win Distribution")
        win_counts = pd.Series({team1: team1_wins, team2: team2_wins})
        fig, ax = plt.subplots(figsize=(4.5, 4.5))  # Increased chart size
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
            color=alt.Color('BattingTeam:N')
        ).properties(height=320)
        st.altair_chart(chart, use_container_width=True)

    st.markdown("---")  # 👈 Added to reduce space before next section

    # 🔥 Top Batsmen in Rivalry
    top_batsmen = df[df['BattingTeam'].isin([team1, team2])] \
        .groupby('batter')['batsman_run'].sum() \
        .sort_values(ascending=False).head(5).reset_index()
    st.subheader("🔥 Top Batsmen")
    st.dataframe(top_batsmen)

    # 🎯 Top Bowlers in Rivalry
    top_bowlers = df[df['isWicketDelivery'] == 1] \
        .groupby('bowler')['player_out'].count() \
        .sort_values(ascending=False).head(5).reset_index()
    st.subheader("🎯 Top Bowlers")
    st.dataframe(top_bowlers)

    # 📈 Year-wise runs trend
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

    # ⚔️ Bonus: Strike Rate Comparison
    st.subheader("⚔️ Top Rivalry Batsman Strike Rates (min 30 balls)")
    strike_df = df.groupby('batter').agg(
        runs=('batsman_run', 'sum'),
        balls=('ballnumber', 'count')
    ).reset_index()
    strike_df = strike_df[strike_df['balls'] >= 30]
    strike_df['Strike Rate'] = (strike_df['runs'] / strike_df['balls']) * 100
    top_strike = strike_df.sort_values("Strike Rate", ascending=False).head(5)
    st.dataframe(top_strike)
