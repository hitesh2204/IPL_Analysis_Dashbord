import streamlit as st
from Chatbot.agent import run_ipl_agent

def genai_chat_tab():
    st.title("🤖 IPL GenAI Assistant")
    st.markdown("Ask anything about players, teams, venues, or IPL stats!")

    query = st.text_input(
        "🗣️ Your Question",
        placeholder="e.g., How many runs did Virat Kohli score in 2016 IPL?"
    )

    if query:
        # 🔑 Simple prompt version
        prompt = f"Answer the following IPL query using the available tools and CSV knowledge base: {query}"

        with st.spinner("⚡ Analyzing your query..."):
            response = run_ipl_agent(prompt)
            st.write(response, unsafe_allow_html=True)
