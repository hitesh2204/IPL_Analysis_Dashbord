from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from Chatbot.llm import load_llm

load_dotenv()

VECTOR_STORE_PATH = "ipl_dataset/vectorstore"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_rag_tool(llm):
    # Load embeddings + vectorstore
    embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore = FAISS.load_local(
        VECTOR_STORE_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    # ✅ RetrievalQA with custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type="refine",
        return_source_documents=True,
        input_key="query"
    )
    return qa_chain
