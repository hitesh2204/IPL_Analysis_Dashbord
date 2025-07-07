import streamlit as st

# 🏏 2. Bar Chart: Distribution of run types (0s, 1s, 2s, 4s, 6s)
def plot_run_distribution(duel_df):
    if duel_df.empty:
        return
    run_counts = duel_df['batsman_run'].value_counts().sort_index()
    st.write("🏏 Run Type Distribution")
    st.bar_chart(run_counts)

# 📈 3. Line Chart: Ball-by-ball progression of runs scored in the duel
def plot_ball_timeline(duel_df):
    if duel_df.empty:
        return
    st.write("📈 Ball-by-Ball Runs Timeline")
    st.line_chart(duel_df['batsman_run'].reset_index(drop=True))
