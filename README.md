🏏 IPL GenAI Assistant

📌 Project Introduction

Traditional cricket websites provide rich statistics about leagues and matches, but lack a chat-based Q&A system.
For example, users cannot directly ask:
👉 “Who scored the fastest fifty at Wankhede in 2016?”
👉 “Compare Rohit Sharma and Virat Kohli in powerplays during 2017.”
👉 “Which bowler dismissed Dhoni most often in playoffs?”

This project bridges that gap by building a RAG-based GenAI application that combines:

📊 Manual Analysis Dashboards → Interactive tables & graphs for IPL stats

🤖 GenAI Chat Assistant → Natural language Q&A powered by LLM + RAG

🔎 Features
1️⃣ Manual Analysis Dashboards

Explore IPL history through structured, interactive analysis:

📊 Overall IPL Analysis → Teams, winners, historical trends

🏏 Team Analysis → Team-wise batting & bowling performance

👥 Player Summary → Career details with tables + graphs

⚔️ Player vs Bowler → Head-to-head records

🆚 Team vs Team → Comparative match history

🏆 Leaderboards → Season-wise top performers

🏟️ Venue Analysis → Matches, runs, wickets, 4s/6s by venue

🔄 Player Comparison → Compare two players side by side

🎯 Tournament Summary → Champions, orange/purple caps

👉 These are deterministic, structured functions ensuring accuracy.

2️⃣ GenAI Chat Assistant

A conversational agent that answers simple, tricky, and complex IPL queries.

✅ Structured queries → answered using Python functions/tools

✅ Unstructured queries → answered using RAG over 15 curated CSVs

⚙️ Tech Stack & Architecture

LLM & Embeddings → OpenAI GPT + text-embedding-3-large

Framework → LangChain (tool routing + RAG pipeline)

Database → FAISS (vector store for embeddings)

Frontend/UI → Streamlit

Backend Logic → Python tools for structured stats queries

Query Flow
User Query
   ↓
LangChain Agent
   ↓
╔══════════════════════════════════════╗
║ Is this query suitable for a function? ║
╚══════════════════════════════════════╝
   ↓ Yes                          ↓ No
[Tool Calling]                 [RAG Retrieval]
  → Structured functions         → FAISS vectorstore
     (stats/graphs)                 (semantic search)
         ↓                              ↓
     Combine + Answer            Combine + Answer
                ↓
      Streamlit UI (chat + graphs)

⚡ Setup & Installation
# Clone repo
git clone <your-repo-url>
cd ipl_genai_app

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run final_app.py

💬 Example Queries

Try asking:

“Who hit the most sixes at Eden Gardens in 2018?”

“Compare Kohli vs Rohit in powerplays.”

“Which team won the most playoffs at Wankhede?”

“Show me Dhoni’s boundary stats in 2012.”

🚀 Future Enhancements

⚡ Add FastAPI backend for production APIs

📱 Deploy as web + mobile app

📊 Expand dataset with live IPL feeds for real-time insights

📂 Final Folder Structure – GenAI IPL App
ipl_genai_app/
├── Chatbot/
│   ├── llm.py                    # Load OpenAI model
│   ├── agent.py                  # LangChain agent setup (tools + RAG)
│   ├── tools.py                  # Tool wrappers (calls your IPL functions)
│   └── gen_chat.py               # Chat interface where users ask queries
│
├── requirements.txt              # 📦 Dependencies
│
├── ipl_dataset/
│   ├── final_ipl.csv             # 🔢 Main IPL dataset
│   ├── player_info.csv           # 👤 Player profile data
│   ├── vectorstore/              # FAISS embeddings DB
│   └── rag_knowledgebase/        # CSVs for RAG (15 curated datasets)
│
├── ipl_player/                   # Player images
│
├── RAG_helper/                   # Helpers for RAG pipelines
│   ├── retriever.py              # CSV/text loader and retriever setup
│   └── (other RAG helper scripts for stats, matches, venues, etc.)
│
├── src/                          # 🔧 Core IPL business logic
│   ├── functional_tool/          # Structured tool logic
│   ├── player_summary.py
│   ├── team_vs_team.py
│   ├── venue_analysis.py
│   ├── overview.py
│   ├── tournament_summary.py
│   └── utils.py                  # Shared utilities
│
├── venue_images/                 # Venue thumbnails
│
└── final_app.py                  # Final Streamlit app entrypoint