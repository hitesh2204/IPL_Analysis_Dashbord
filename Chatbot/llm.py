from langchain_openai import ChatOpenAI  
from dotenv import load_dotenv

load_dotenv()

def load_llm():
    llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    #temperature=0.7,  # Optional: Controls randomness
    #api_key=os.getenv("OPENAI_API_KEY")
    )
    return llm