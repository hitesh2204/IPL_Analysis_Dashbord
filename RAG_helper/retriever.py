import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# === Configuration ===
DATA_FOLDER = "ipl_dataset//rag_knowledgebase"
VECTOR_STORE_PATH = "ipl_dataset/vectorstore"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# === Load embedding model ===
embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)

def load_and_process_csvs(data_folder: str):
    """
    Reads all CSV files in the folder and converts rows to text-based Documents.
    """
    documents = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            filepath = os.path.join(data_folder, filename)
            df = pd.read_csv(filepath)

            for i, row in df.iterrows():
                row_text = " | ".join(f"{col}: {row[col]}" for col in df.columns if pd.notnull(row[col]))
                metadata = {
                    "source": filename,
                    "row": i
                }
                documents.append(Document(page_content=row_text, metadata=metadata))
    
    return documents

def create_vectorstore():
    print("🔍 Loading CSVs and processing into documents...")
    docs = load_and_process_csvs(DATA_FOLDER)

    print(f"📄 Total documents created: {len(docs)}")

    print("🧱 Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    print(f"🧠 Total chunks after splitting: {len(split_docs)}")

    print("🚀 Generating embeddings and creating FAISS vectorstore...")
    vectorstore = FAISS.from_documents(split_docs, embedding_model)

    print(f"💾 Saving vectorstore to {VECTOR_STORE_PATH}...")
    vectorstore.save_local(VECTOR_STORE_PATH)

    print("✅ Vectorstore created and saved successfully.")

if __name__ == "__main__":
    create_vectorstore()
