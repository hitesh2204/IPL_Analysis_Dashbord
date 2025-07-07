import pandas as pd
import streamlit as st

@st.cache_data
def load_ipl_data():
    match_df = pd.read_csv("ipl_dataset/crick_ipl.csv")
    ball_df = pd.read_csv("ipl_dataset/crick_ipl_ball.csv")
    merged = ball_df.merge(match_df, on='ID')
    merged["BowlingTeam"] = merged.apply(
        lambda row: row["Team2"] if row["BattingTeam"] == row["Team1"] else row["Team1"], axis=1
    )
    return merged
