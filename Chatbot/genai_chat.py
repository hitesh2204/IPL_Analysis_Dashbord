import streamlit as st
from Chatbot.agent import run_ipl_agent

def genai_chat_tab():
    st.title("🤖 IPL GenAI Assistant")
    st.markdown("Ask anything about players, teams, venues, or IPL stats!")

    query = st.text_input("🗣️ Your Question", placeholder="e.g., How many runs did Virat Kohli score?")
    
    if query:
        with st.spinner("Thinking..."):
            response = run_ipl_agent(query)
            st.success(response)
