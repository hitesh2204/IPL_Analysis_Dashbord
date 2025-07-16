# agent.py

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from Chatbot.tool import all_tools  # ✅ Import your tools from tools.py

# ✅ Load environment variables
load_dotenv()

# ✅ Hugging Face Model Configuration
llm = HuggingFaceEndpoint( 
    repo_id="deepseek-ai/DeepSeek-R1",
    provider="together" )

model = ChatHuggingFace(llm=llm) 

# ✅ Initialize LangChain Agent with HF model
agent = initialize_agent(
    tools=all_tools,
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# ✅ Exposed method for chatbot
def run_ipl_agent(query: str) -> str:
    return agent.run(query)
