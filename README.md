# 🏏 IPL GenAI Assistant

## 📌 Project Introduction

Traditional cricket websites provide rich statistics about leagues and matches, but they lack a **chat-based Q&A system**.  
For example, users cannot directly ask:

👉 “Who scored the fastest fifty at Wankhede in 2016?”  

This project fills that gap by building a **RAG-based GenAI application** that combines:  

- **Manual Analysis Dashboards** → Interactive tables & graphs for IPL stats.  
- **GenAI Chat Assistant** → Natural language Q&A powered by LLM + RAG.  

---

## 🔎 Features

### 1️⃣ Manual Analysis Dashboards  

Users can explore IPL history through structured, interactive analysis:  

- 📊 **Overall IPL Analysis** → Teams, winners, historical trends.  
- 🏏 **Team Analysis** → Select team → drill down into player stats (batting, bowling, vs opponents).  
- 👥 **Player Summary** → Career-wise details in table + graph format.  
- ⚔️ **Player vs Bowler** → Head-to-head records.  
- 🆚 **Team vs Team** → Comparative match history.  
- 🏆 **Leaderboards** → Top performers by season.  
- 🏟️ **Venue Analysis** → Matches, top performers, 4s/6s by venue.  
- 🔄 **Player Comparison** → Compare two players’ stats.  
- 🎯 **Tournament Summary** → Season champions, top batsmen & bowlers.  

👉 These are deterministic, structured functions ensuring accuracy.  

---

### 2️⃣ GenAI Chat Assistant  

A conversational agent that answers simple, tricky, and complex IPL queries.  

**Hybrid Design**  
- ✅ Structured queries → handled by **function tools** (e.g., player summary, venue analysis).  
- ✅ Unstructured queries → handled by **RAG over 15 curated CSVs**.  

**Data Preparation**  
- Extracted IPL dataset from Kaggle.  
- Created 15 specialized CSVs (batting stats, bowling stats, boundaries, partnerships, playoffs, venues, etc.).  
- Generated embeddings using OpenAI `text-embedding-3-large`.  
- Stored in **FAISS vector database** for semantic retrieval.  

**Query Flow**  
1. User enters query → e.g., *“How many sixes did Rohit Sharma hit in 2017?”*  
2. Tool Router decides:  
   - Structured → Use Python function.  
   - Unstructured → Use RAG.  
3. Selected tool executes → sends result to LLM → generates human-readable answer.  
4. Response displayed in chatbot UI.  

---

## ⚙️ Tech Stack & Architecture  

- **LLM & Embeddings** → OpenAI GPT models (`text-embedding-3-large`).  
- **Framework** → LangChain (tool routing, RAG pipeline).  
- **Database** → FAISS (vector store for embeddings).  
- **Frontend/UI** → Streamlit.  
- **Backend Logic** → Python tools for structured queries.  

**System Flow**  

```text
User Query
   ↓
LangChain Agent
   ↓
╔══════════════════════════════════════╗
║ Is this query suitable for a function? ║
╚══════════════════════════════════════╝
   ↓ Yes                          ↓ No
[Tool Calling]                 [RAG]
  → functions.py                → vectorstore
     (stats/graphs)               (semantic text retrieval)
         ↓                          ↓
     Combine + Answer        Combine + Answer
                ↓
      Streamlit UI (chat + graphs)
```

---

## 🚀 Future Enhancements  

- ⚡ Add FastAPI backend for production-ready APIs.  
- 📱 Deploy as a web/mobile app for wider accessibility.  
- 📊 Expand dataset to include live IPL feeds for real-time insights.  

---

## 📂 Final Folder Structure – GenAI IPL App  

```text
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
│       ├── batting_phase_stats.csv
│       ├── bolwer_vs_team_season_venue.csv
│       ├── bowling_phase_stats.csv
│       ├── match_highlights.csv
│       ├── player_boundary_season.csv
│       ├── player_boundary_stats.csv
│       ├── player_partnership_records.csv
│       ├── player_role.csv
│       ├── player_stats.csv
│       ├── player_vs_team_season_venue.csv
│       ├── playoff_stats.csv
│       ├── season_summary_final.csv
│       ├── team_records_season.csv
│       ├── team_vs_team_powerplay_stats.csv
│       ├── team_vs_team_season.csv
│       └── venue_stats_season.csv
│
├── ipl_player/                   # Player images
│
├── RAG_helper/                   # Helpers for RAG pipelines
│   ├── batsman_team_phase_season.py
│   ├── batting_phase_stats.py
│   ├── boundry_stats.py
│   ├── bowler_phase_team_season.py
│   ├── bowler_vs_team.py
│   ├── bowling_phase_stat.py
│   ├── match_highligths.py
│   ├── player_boundry_stats.py
│   ├── player_stats.py
│   ├── player_vs_team.py
│   ├── playoff_stats.py
│   ├── powerplay_stats.py
│   ├── retriever.py              # CSV/text loader and retriever setup
│   ├── season_summary.py
│   ├── team_records.py
│   ├── team_vs_team.py
│   ├── venue_stats.py
│   └── retriever.py
│
├── src/                          # 🔧 Core IPL business logic
│   ├── functional_tool/          # Structured tool logic
│   │   ├── pair_stats_tools.py
│   │   ├── phase_wise_tool.py
│   │   ├── player_summary_tool.py
│   │   └── rag_csv_tool.py
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
```

---
