
import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from Chatbot.llm import load_llm  # your LLM loader

load_dotenv()

VECTOR_STORE_PATH = "ipl_dataset/vectorstore"
EMBEDDING_MODEL = "text-embedding-3-large"

def get_rag_tool(llm):
    # Load embeddings
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    # Load the FAISS vectorstore
    vectorstore = FAISS.load_local(
        VECTOR_STORE_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    # Create RetrievalQA with custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 15}),
        chain_type="stuff",
        return_source_documents=True
    )
    return qa_chain

