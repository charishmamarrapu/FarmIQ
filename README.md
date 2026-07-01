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

## How to Run Locally
1. Clone the repo
2. Create virtual environment: `python -m venv farmiq_env`
3. Activate: `farmiq_env\Scripts\activate`
4. Install: `pip install -r requirements.txt`
5. Add API keys to `.env` file
6. Run pipeline: `python src/rag/build_pipeline.py`
7. Run app: `streamlit run src/ui/app.py`

## Data Sources
See `docs/DATA_SOURCES.md` for full list