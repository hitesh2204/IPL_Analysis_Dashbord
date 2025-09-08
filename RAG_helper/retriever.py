
import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# === Configuration ===
DATA_FOLDER = "IPL_Dataset/rag_knowledgebase"   # Folder containing all CSVs
VECTOR_STORE_PATH = "IPL_Dataset/vectorstore"
EMBEDDING_MODEL_NAME = "text-embedding-3-large"

# === Convert a single CSV into Documents (row-based) ===
def load_csv_as_docs(file_path: str):
    df = pd.read_csv(file_path)
    docs = []
    for _, row in df.iterrows():
        # Combine row into text, skip NaN values
        row_text = " | ".join([f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])])

        # Save row-level metadata
        metadata = {"source_file": os.path.basename(file_path)}
        for col in df.columns:
            val = row[col]
            if pd.notna(val):
                # Normalize metadata: lowercase strings, keep numbers as-is
                metadata[col] = str(val).strip().lower() if isinstance(val, str) else val

        docs.append(Document(page_content=row_text, metadata=metadata))
    return docs

# === Load all CSVs ===
def load_and_process_csvs():
    all_docs = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".csv"):
            file_path = os.path.join(DATA_FOLDER, file)
            all_docs.extend(load_csv_as_docs(file_path))
    return all_docs

# === Build & Save Vectorstore ===
def create_vectorstore():
    print("🔍 Loading CSVs and processing into documents...")
    documents = load_and_process_csvs()
    print(f"📄 Total documents created: {len(documents)}")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)

    print("🚀 Generating embeddings and creating FAISS vectorstore...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    print(f"💾 Saving vectorstore to {VECTOR_STORE_PATH}...")
    vectorstore.save_local(VECTOR_STORE_PATH)

    print(f"✅ Vectorstore created and saved at {VECTOR_STORE_PATH}")

if __name__ == "__main__":
    create_vectorstore()



