# agent.py
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from Chatbot.llm import load_llm 
from Chatbot.tool import all_tools  

#  Load environment variables#
load_dotenv()

# Load gpt-4o model
llm = load_llm()

# ✅ Initialize LangChain Agent with your tools and LLaMA3
agent = initialize_agent(
    tools=all_tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True
)

# ✅ Function to expose agent to other modules
def run_ipl_agent(query: str) -> str:
    return agent.run(query)
