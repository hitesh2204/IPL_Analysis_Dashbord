# src/tournament_summary.py

import streamlit as st
import pandas as pd
from src.tournament_summary_data import tournament_summary
from logger import setup_logger

# Initialize logger
logger = setup_logger()

def tournament_summary_page():
    st.header("🏆 IPL Tournament Summary (2008 - 2025)", divider="rainbow")
    
    try:
        # Create DataFrame
        df = pd.DataFrame(tournament_summary).sort_values("Season", ascending=False)
        st.dataframe(df, use_container_width=True)
        st.markdown("You can sort columns, filter by year, or export as CSV if needed.")
        logger.info("Tournament summary page loaded successfully.")
    
    except Exception as e:
        logger.error(f"Error in tournament_summary_page: {e}", exc_info=True)
        st.error("Something went wrong while loading the tournament summary. Please try again later.")
