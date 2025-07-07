import streamlit as st
from PIL import Image

def render_header():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 🏏 <span style='color:#FF4B4B'>IPL Insights by Hitesh</span>", unsafe_allow_html=True)
    with col2:
        st.image("image-video/hitu.jpeg", width=80)

    st.markdown("##### 🎯 Analyze Teams, Duels, and Trends — all in one place!")

def sidebar_menu():
    st.sidebar.image("image-video/hitu.jpeg", width=100)
    st.sidebar.markdown("## 📂 Navigation")
    return st.sidebar.selectbox("Select Analysis", [
        "🏠 Overview", "🧢 Team Analysis", "⚔️ Player vs Bowler Duel"
    ])
