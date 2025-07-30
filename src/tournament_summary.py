# src/tournament_summary.py
import streamlit as st
import pandas as pd
from src.tournament_summary_data import tournament_summary

## Streamlit UI for tournament summary.
def tournament_summary_page():
    st.header("🏆 IPL Tournament Summary (2008 - 2025)", divider="rainbow")
    
    df = pd.DataFrame(tournament_summary).sort_values("Season", ascending=False)
    
    st.dataframe(df, use_container_width=True)

    st.markdown("You can sort columns, filter by year, or export as CSV if needed.")



