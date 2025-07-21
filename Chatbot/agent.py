# agent.py

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOllama  # ✅ Use local Ollama
from Chatbot.tool import all_tools  # ✅ Your custom tools

# ✅ Load environment variables
load_dotenv()

# ✅ Load Ollama LLaMA 3 model
llm = ChatOllama(model="llama3:8b-instruct-q4_0")  # You must have already run `ollama run mistral`

# ✅ Initialize LangChain Agent with your tools and LLaMA3
agent = initialize_agent(
    tools=all_tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# ✅ Function to expose agent to other modules
def run_ipl_agent(query: str) -> str:
    return agent.run(query)
