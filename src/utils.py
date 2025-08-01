# utils/media_utils.py or wherever appropriate

import base64
import os
from PIL import Image
import streamlit as st
import time
import re
from core.logger import setup_logger

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
    'RCB': 'Royal Challengers Bangalore', 
    'ROYAL CHALLENGERS BANGALORE': 'Royal Challengers Bangalore',
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

def normalize_team_name(name):
    try:
        name_upper = name.strip().upper()
        normalized = TEAM_NAME_ALIASES.get(name_upper, name)
        logger.debug(f"Normalized team name: {name} → {normalized}")
        return normalized
    except Exception as e:
        logger.exception(f"Error normalizing team name: {name} | Error: {e}")
        return name
