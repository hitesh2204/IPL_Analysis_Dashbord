import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import os
from PIL import Image

def team_vs_team_analysis(ipl, team1, team2):
    st.header(f"🤜 {team1} vs {team2} Analysis", divider="rainbow")

    logo1_path = f"image-video/{team1.replace(' ', '_').lower()}.jpeg"
    logo2_path = f"image-video/{team2.replace(' ', '_').lower()}.jpeg"

    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists(logo1_path):
            col1.image(Image.open(logo1_path), caption=team1, width=150)
    with col2:
        if os.path.exists(logo2_path):
            col2.image(Image.open(logo2_path), caption=team2, width=150)

    df = ipl[((ipl['Team1'] == team1) & (ipl['Team2'] == team2)) |
             ((ipl['Team1'] == team2) & (ipl['Team2'] == team1))]

    total_matches = df['ID'].nunique()
    st.subheader(f"📅 Total Matches Played: {total_matches}")

    win_df = df[['ID', 'WinningTeam']].drop_duplicates()
    team1_wins = win_df[win_df['WinningTeam'] == team1].shape[0]
    team2_wins = win_df[win_df['WinningTeam'] == team2].shape[0]

    col1, col2 = st.columns(2)
    col1.metric(f"{team1} Wins", team1_wins)
    col2.metric(f"{team2} Wins", team2_wins)

    win_counts = pd.Series({team1: team1_wins, team2: team2_wins})
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(win_counts, labels=win_counts.index, autopct='%1.1f%%', startangle=50, colors=['#3498DB', '#E74C3C'])
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader("🏏 Total Runs Scored")
    run_summary = df.groupby('BattingTeam')['total_run'].sum().reset_index()
    st.bar_chart(run_summary.set_index('BattingTeam'))

    top_batsmen = df[df['BattingTeam'].isin([team1, team2])] \
        .groupby('batter')['batsman_run'].sum() \
        .sort_values(ascending=False).head(5).reset_index()
    st.subheader("🔥 Top Batsmen")
    st.dataframe(top_batsmen)

    top_bowlers = df[df['isWicketDelivery'] == 1] \
        .groupby('bowler')['player_out'].count() \
        .sort_values(ascending=False).head(5).reset_index()
    st.subheader("🎯 Top Bowlers")
    st.dataframe(top_bowlers)

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

    st.subheader("⚔️ Top Rivalry Batsman Strike Rates (min 30 balls)")
    strike_df = df.groupby('batter').agg(
        runs=('batsman_run', 'sum'),
        balls=('ballnumber', 'count')
    ).reset_index()
    strike_df = strike_df[strike_df['balls'] >= 30]
    strike_df['Strike Rate'] = (strike_df['runs'] / strike_df['balls']) * 100
    top_strike = strike_df.sort_values("Strike Rate", ascending=False).head(5)
    st.dataframe(top_strike)


# 🧠 GENAI FUNCTION — Used by LangChain Agent
def get_team_vs_team_summary(team1: str, team2: str, ipl: pd.DataFrame) -> str:
    matches = ipl[((ipl['Team1'] == team1) & (ipl['Team2'] == team2)) |
                  ((ipl['Team1'] == team2) & (ipl['Team2'] == team1))]

    if matches.empty:
        return f"No head-to-head records found between {team1} and {team2}."

    total_matches = matches['ID'].nunique()
    team1_wins = matches[matches['WinningTeam'] == team1]['ID'].nunique()
    team2_wins = matches[matches['WinningTeam'] == team2]['ID'].nunique()

    top_batsmen_df = matches.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(5)
    top_batsmen_text = "\n".join([f"{i+1}. {name} ({runs} runs)" for i, (name, runs) in enumerate(top_batsmen_df.items())])

    dismissals = matches[matches['isWicketDelivery'] == 1]
    top_bowlers_df = dismissals[dismissals['player_out'].notnull()].groupby('bowler')['player_out'].count().sort_values(ascending=False).head(5)
    top_bowlers_text = "\n".join([f"{i+1}. {name} ({wkts} wickets)" for i, (name, wkts) in enumerate(top_bowlers_df.items())])

    highest_score = matches.groupby('ID')['total_run'].sum().max()

    match_scores = matches.groupby(['ID', 'batter'])['batsman_run'].sum().reset_index()
    top_individual = match_scores.sort_values(by='batsman_run', ascending=False).iloc[0]
    best_batsman = top_individual['batter']
    best_score = top_individual['batsman_run']

    summary = (
        f"🏏 Head-to-Head: {team1} vs {team2}\n\n"
        f"• Total Matches: {total_matches}\n"
        f"• {team1} Wins: {team1_wins}\n"
        f"• {team2} Wins: {team2_wins}\n"
        f"• Highest Team Score: {highest_score} runs\n"
        f"• Best Individual Score: {best_batsman} ({best_score} runs)\n\n"
        f"🔥 Top 5 Batsmen:\n{top_batsmen_text}\n\n"
        f"🎯 Top 5 Bowlers:\n{top_bowlers_text}"
    )

    return summary