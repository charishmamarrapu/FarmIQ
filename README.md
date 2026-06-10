# FarmIQ 🌾
Multi-agent agricultural advisory system for farmers in AP and Telangana.

## Project Overview
FarmIQ uses RAG over government crop data, weather patterns, and mandi 
prices to give farmers real, actionable decisions.

## Target Users
- Small and medium farmers in Krishna, Guntur, West Godavari, Kurnool
- Agricultural extension officers
- Agri-input retailers

## Agents
- Crop Advisory Agent
- Market Price Agent
- Weather Impact Agent
- Pest & Disease Agent

## Tech Stack
- LLM: Gemini 2.5 Flash / GPT-4o-mini
- RAG: LangChain
- Vector Store: ChromaDB
- Frontend: Streamlit

## Team
- Charishma Marrapu (Team Leader) - RAG Pipeline
- Gurrala Sri Likhitha - Data Collection
- V.S. Hasini Reddy - Testing & Integration

## How to Run
1. Clone the repo
2. Create virtual environment: `python -m venv farmiq_env`
3. Activate: `farmiq_env\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Run pipeline: `python src/rag/build_pipeline.py`
6. Test retrieval: `python src/rag/test_retrieval.py`

## Data Sources
See `docs/DATA_SOURCES.md` for full list