import pandas as pd
import streamlit as st
from logger import setup_logger

logger = setup_logger()

@st.cache_data
def load_ipl_data():
    try:
        logger.info("Starting to load IPL datasets...")

        match_df = pd.read_csv("ipl_dataset/crick_ipl.csv")
        logger.info("Loaded match-level data.")

        ball_df = pd.read_csv("ipl_dataset/crick_ipl_ball.csv")
        logger.info("Loaded ball-by-ball data.")

        merged = ball_df.merge(match_df, on='ID')
        logger.info("Successfully merged ball and match data.")


        ipl_df = pd.read_csv("ipl_dataset/final_ipl.csv", encoding='ISO-8859-1')
        logger.info("Loaded final IPL summary data.")

        logger.info(" IPL data loading completed successfully.")
        return ipl_df

    except FileNotFoundError as fnf_error:
        logger.error(f"🚫 File not found: {fnf_error}")
        st.error("Some IPL data files are missing. Please check the 'ipl_dataset' folder.")
        return pd.DataFrame()  # or raise if appropriate

    except Exception as e:
        logger.exception(f"Error while loading IPL data: {str(e)}")
        st.error("An unexpected error occurred while loading data.")
        return pd.DataFrame()  # or raise if appropriate
