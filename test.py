import pandas as pd
import streamlit as st
from PIL import Image
import base64
import os

# Load Data
match_df = pd.read_csv("ipl_dataset//crick_ipl.csv")
ball_df = pd.read_csv("ipl_dataset//crick_ipl_ball.csv")
ipl = ball_df.merge(match_df, on='ID')

st.write("🧩 Columns:", ipl.columns.tolist())
