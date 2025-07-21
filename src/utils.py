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


def render_overview_carousel():
    st.markdown("## 🏏 IPL Insights Overview")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("IPL-Insights-by-Hitesh")
    with col2:
        st.image(Image.open("image-video/hitu.jpeg"), width=120)

    st.title(":red[IPL]:green[-]:blue[Analysis] :sunglasses:")

    # ✅ Intro image
    #intro_img = "image-video/IPL1-2024-Squad.jpg"
    #if os.path.exists(intro_img):
        #st.image(Image.open(intro_img), caption='All IPL Teams & Captains')


    # ✅ Slideshow Section (Rotating Player Images)
    st.markdown("### 🖼️ IPL Stars - Auto Slideshow")

    image_folder = "image-video/carousel"
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith((".jpg", ".jpeg", ".png"))])
    image_paths = [os.path.join(image_folder, f) for f in image_files]

    if image_paths:
        if "img_index" not in st.session_state:
            st.session_state.img_index = 0

        current_img = Image.open(image_paths[st.session_state.img_index])
        st.image(current_img, use_column_width=True, caption=image_files[st.session_state.img_index])

        time.sleep(2)
        st.session_state.img_index = (st.session_state.img_index + 1) % len(image_paths)
        st.experimental_rerun()
    else:
        st.warning("No slideshow images found!")

    
    # ✅ Autoplay Video (🎥)
    video_path = "image-video/ipl_video.mp4"
    if os.path.exists(video_path):
        autoplay_video("image-video/ipl_video.mp4")
    else:
        st.warning("⚠️ IPL video not found!")

    st.balloons()