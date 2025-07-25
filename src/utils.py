import base64
import os
from PIL import Image
import streamlit as st
import time
import re

@st.cache_resource
def load_encoded_video(video_path):
    with open(video_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def autoplay_video(video_path):
    encoded = load_encoded_video(video_path)
    video_html = f"""
        <video width="700" autoplay loop muted controls>
            <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
        </video>
    """
    st.markdown(video_html, unsafe_allow_html=True)

def get_image_path(player_name, image_folder="IPL_Player"):
    filename = player_name.replace(" ", "_") + ".jpg"
    path = os.path.join(image_folder, filename)

    if os.path.exists(path):
        return path

    fallback = os.path.join(image_folder, "default_avatar.png")
    if os.path.exists(fallback):
        return fallback
    # 👇 Return a valid image object to prevent crashing
    return None

    
    # ✅ Autoplay Video (🎥)
    video_path = "image-video/ipl_video.mp4"
    if os.path.exists(video_path):
        autoplay_video("image-video/ipl_video.mp4")
    else:
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
    name_upper = name.strip().upper()
    return TEAM_NAME_ALIASES.get(name_upper, name)
