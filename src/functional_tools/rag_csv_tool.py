from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

VECTOR_STORE_PATH = "ipl_dataset/vectorstore"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def get_rag_tool():
    embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore = FAISS.load_local(
        VECTOR_STORE_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=st.session_state.llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff"
    )

    return qa_chain
