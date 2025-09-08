# utils/media_utils.py or wherever appropriate

import base64
import os
from PIL import Image
import streamlit as st
import time
import re
import pandas as pd
from core.logger import setup_logger
from difflib import get_close_matches
from langchain_core.documents import Document

logger = setup_logger(__name__)

@st.cache_resource
def load_encoded_video(video_path):
    try:
        with open(video_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        logger.info(f"Loaded and encoded video: {video_path}")
        return encoded
    except FileNotFoundError:
        logger.error(f"Video file not found: {video_path}")
        st.error(f"Video file not found: {video_path}")
    except Exception as e:
        logger.exception(f"Unexpected error loading video: {e}")
        st.error("Unexpected error loading video.")
    return None

def autoplay_video(video_path):
    encoded = load_encoded_video(video_path)
    if encoded:
        try:
            video_html = f"""
                <video width="700" autoplay loop muted controls>
                    <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
                </video>
            """
            st.markdown(video_html, unsafe_allow_html=True)
            logger.info(f"Video autoplayed: {video_path}")
        except Exception as e:
            logger.exception(f"Error displaying video: {e}")
            st.error("Unable to play video.")
    else:
        logger.warning("Encoded video content is None.")

def get_image_path(player_name, image_folder="IPL_Player"):
    try:
        filename = player_name.replace(" ", "_") + ".jpg"
        path = os.path.join(image_folder, filename)

        if os.path.exists(path):
            logger.info(f"Found image for player: {player_name}")
            return path

        fallback = os.path.join(image_folder, "default_avatar.png")
        if os.path.exists(fallback):
            logger.warning(f"Using fallback image for player: {player_name}")
            return fallback
        
        logger.error(f"No image found for {player_name}, including fallback.")
        return None
    except Exception as e:
        logger.exception(f"Error retrieving image for player: {player_name} | Error: {e}")
        return None

# Optional autoplay setup logic if you want to move it here
def try_autoplay_video():
    video_path = "image-video/ipl_video.mp4"
    if os.path.exists(video_path):
        autoplay_video(video_path)
    else:
        logger.warning("⚠️ IPL video not found!")
        st.warning("⚠️ IPL video not found!")
    st.balloons()

TEAM_NAME_ALIASES = {
    'CSK': 'Chennai Super Kings', 
    'CHENNAI SUPER KINGS': 'Chennai Super Kings',
    'RCB': 'Royal Challengers Bengaluru', 
    'ROYAL CHALLENGERS BANGALURU': 'Royal Challengers Bengaluru',
    'MI': 'Mumbai Indians', 
    'MUMBAI INDIANS': 'Mumbai Indians',
    'KKR': 'Kolkata Knight Riders', 
    'KOLKATA KNIGHT RIDERS': 'Kolkata Knight Riders',
    'RR': 'Rajasthan Royals', 
    'RAJASTHAN ROYALS': 'Rajasthan Royals',
    'DC': 'Delhi Capitals', 
    'DELHI CAPITALS': 'Delhi Capitals',
    'PBKS': 'Punjab Kings', 
    'PUNJAB KINGS': 'Punjab Kings',
    'SRH': 'Sunrisers Hyderabad', 
    'SUNRISERS HYDERABAD': 'Sunrisers Hyderabad',
    'GL': 'Gujarat Lions', 
    'GUJARAT LIONS': 'Gujarat Lions',
    'GT': 'Gujarat Titans',
    'GUJARAT TITANS': 'Gujarat Titans',
    'LSG': 'Lucknow Super Giants', 
    'LUCKNOW SUPER GIANTS': 'Lucknow Super Giants',
    'PWI': 'Pune Warriors', 
    'PUNE WARRIORS': 'Pune Warriors',
    'RPS': 'Rising Pune Supergiant', 
    'RISING PUNE SUPERGIANT': 'Rising Pune Supergiant',
    'KTK': 'Kochi Tuskers Kerala', 
    'KOCHI TUSKERS KERALA': 'Kochi Tuskers Kerala',
    'DC_OLD': 'Deccan Chargers', 
    'DECCAN CHARGERS': 'Deccan Chargers'
}

## Normalize all teams name.
def normalize_team_name(name):
    try:
        name_upper = name.strip().upper()
        normalized = TEAM_NAME_ALIASES.get(name_upper, name)
        logger.debug(f"Normalized team name: {name} → {normalized}")
        return normalized
    except Exception as e:
        logger.exception(f"Error normalizing team name: {name} | Error: {e}")
        return name
    

### Fuzzy Player name

def get_normalized_player_name(user_input: str, player_names: list) -> str:
    """
    Fuzzy match user input to the closest player full name from dataset.
    """
    user_input = user_input.strip().lower()

    player_name_map = {name.lower(): name for name in player_names}
    lower_names = list(player_name_map.keys())

    matches = get_close_matches(user_input, lower_names, n=1, cutoff=0.6)

    if matches:
        matched_name = player_name_map[matches[0]]
        return matched_name
    else:
        return None

### normalized venue name

def normalize_venue_name(venue: str) -> str:
    """
    Normalize IPL venue names to handle variations and make queries more consistent.

    Args:
        venue (str): Raw venue name from dataset or user query.

    Returns:
        str: Normalized venue name (standardized).
    """
    if not venue:
        return ""

    venue = venue.strip().lower()

    # Mapping of common aliases / variations → standard names
    mapping = {
        "chinnaswamy": "M Chinnaswamy Stadium",
        "m chinnaswamy": "M Chinnaswamy Stadium",
        "is bindra": "Punjab Cricket Association IS Bindra Stadium",
        "mohali": "Punjab Cricket Association IS Bindra Stadium",
        "feroz shah kotla": "Feroz Shah Kotla",
        "arun jaitley": "Arun Jaitley Stadium",
        "wankhede": "Wankhede Stadium",
        "eden gardens": "Eden Gardens",
        "sawai mansingh": "Sawai Mansingh Stadium",
        "rajiv gandhi": "Rajiv Gandhi International Stadium",
        "ma chidambaram": "MA Chidambaram Stadium",
        "chepauk": "MA Chidambaram Stadium",
        "dy patil": "Dr DY Patil Sports Academy",
        "vidarbha": "Vidarbha Cricket Association Stadium, Jamtha",
        "nagpur": "Vidarbha Cricket Association Stadium, Jamtha",
        "hpca": "Himachal Pradesh Cricket Association Stadium",
        "dharamsala": "Himachal Pradesh Cricket Association Stadium",
        "nehru stadium": "Nehru Stadium",
        "holkar": "Holkar Cricket Stadium",
        "vdca": "ACA VDCA Cricket Stadium",
        "visakhapatnam": "ACA VDCA Cricket Stadium",
        "subrata roy": "Subrata Roy Sahara Stadium",
        "pune": "Maharashtra Cricket Association Stadium",
        "maharashtra cricket": "Maharashtra Cricket Association Stadium",
        "ekana": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
        "lucknow": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
        "barsapara": "Barsapara Cricket Stadium, Guwahati",
        "guwahati": "Barsapara Cricket Stadium, Guwahati",
        "mullanpur": "Maharaja Yadavindra Singh International Cricket Stadium",
    }

    # Try to find a match by keyword
    for key, standard in mapping.items():
        if re.search(rf"\b{key}\b", venue):
            return standard

    # If no mapping found, return title-cased version
    return venue.title()


# extract stats,win percentage,economy,average.
def extract_stat(query: str) -> str:
    stat_map = {
        "strike rate": ["strike rate", "sr"],
        "win %": ["win %", "win percentage", "winning %"],
        "average": ["average", "avg"],
        "economy": ["economy", "eco"]
    }

    for key, patterns in stat_map.items():
        if any(p in query.lower() for p in patterns):
            return key
    return None
