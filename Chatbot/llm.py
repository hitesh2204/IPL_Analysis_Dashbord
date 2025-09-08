from langchain_openai import ChatOpenAI  
from dotenv import load_dotenv

load_dotenv()

def load_llm():
    llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
    #api_key=os.getenv("OPENAI_API_KEY")
    )
    return llm


## gpt-4o-mini