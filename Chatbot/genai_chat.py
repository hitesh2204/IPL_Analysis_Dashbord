import streamlit as st
from Chatbot.agent import run_ipl_agent

def genai_chat_tab():
    st.title("🤖 IPL GenAI Assistant")
    st.markdown("Ask anything about players, teams, venues, or IPL stats!")

    query = st.text_input("🗣️ Your Question", placeholder="e.g., How many runs did Virat Kohli score in 2016 IPL?")

    if query:
        prompt = (
            f"You are an intelligent,smart IPL expert analyst. Based on available functional tools and CSV RAG data, "
            f"answer the following query:\n\n"
            f"\"{query}\"\n\n"
            f"Only gives proper and exact answer what user asked in there query.Do not include any extra information by yourself base on observation data gives proper, genuine answer.."
        )

        with st.spinner("Thinking..."):
            response = run_ipl_agent(prompt)
            st.write(response, unsafe_allow_html=True)
