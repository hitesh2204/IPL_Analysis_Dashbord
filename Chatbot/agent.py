# agent.py
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI  
from Chatbot.tool import all_tools  

#  Load environment variables#
load_dotenv()

# Load Ollama LLaMA 3 model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    #temperature=0.7,  # Optional: Controls randomness
    #api_key=os.getenv("OPENAI_API_KEY")
)


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
