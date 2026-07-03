# FarmIQ 🌾
## Multi-Agent Agricultural Advisory System Using RAG

AI-powered advice for farmers in Andhra Pradesh 
and Telangana in Telugu and English.

## 🌐 Live Demo
https://farmiq-mw8pjyxyxvux4bblq4u6wd.streamlit.app/

## 📌 Project Overview
FarmIQ is a multi-agent system that retrieves from 
government agricultural data, mandi prices, soil health 
information, and weather forecasts to give farmers 
real, actionable decisions.

## 👥 Target Users
- Small and medium farmers in Krishna, Guntur, 
  West Godavari, and Kurnool districts
- Agricultural extension officers
- Agri-input retailers

## 🤖 Agents
| Agent | Function |
|-------|----------|
| Crop Advisory | Best crops by district and season |
| Market Price | Mandi prices and sell/hold advice |
| Weather Impact | Live forecast and crop risk alerts |
| Pest & Disease | Symptom diagnosis and treatment |
| Govt Schemes | PM-KISAN and PMFBY eligibility |
| Fertilizer Calc | NPK quantities and cost estimate |

## 🛠️ Tech Stack
- LLM: Groq llama-3.3-70b-versatile
- RAG Framework: LangChain
- Vector Store: ChromaDB (12,397 chunks)
- Embedding Model: HuggingFace all-MiniLM-L6-v2
- APIs: OpenWeatherMap, data.gov.in
- Frontend: Streamlit
- Deployment: Streamlit Cloud

## 📁 Project Structure
FarmIQ/
├── src/
│   ├── agents/
│   │   ├── crop_advisory_agent.py
│   │   ├── market_price_agent.py
│   │   ├── weather_agent.py
│   │   ├── pest_disease_agent.py
│   │   ├── scheme_agent.py
│   │   ├── fertilizer_agent.py
│   │   └── orchestrator.py
│   ├── rag/
│   │   ├── build_pipeline.py
│   │   ├── pdf_loader.py
│   │   ├── csv_loader.py
│   │   ├── vectorstore.py
│   │   ├── retriever.py
│   │   └── test_retrieval.py
│   ├── utils/
│   │   └── llm.py
│   └── ui/
│       └── app.py
├── data/
│   ├── pdfs/
│   └── csvs/
├── docs/
│   ├── DATA_SOURCES.md
│   ├── TESTING_REPORT_WEEK1.md
│   ├── TESTING_REPORT_WEEK2.md
│   └── TESTING_REPORT_WEEK3.md
└── vectorstore/

## 🚀 How to Run Locally
1. Clone the repo
2. Create virtual environment:
   python -m venv farmiq_env
3. Activate:
   farmiq_env\Scripts\activate
4. Install packages:
   pip install -r requirements.txt
5. Add API keys to .env file:
   GROQ_API_KEY=your_key
   OPENWEATHER_API_KEY=your_key
6. Run pipeline:
   python src/rag/build_pipeline.py
7. Run app:
   streamlit run src/ui/app.py

## 👨‍👩‍👧 Team 5
| Member | Role |
|--------|------|
| Charishma Marrapu (Lead) | RAG Pipeline + UI + Deployment |
| Gurrala Sri Likhitha | Data Collection + Market Agent |
| V.S. Hasini Reddy | Testing + Scheme Agent |

## 📊 Data Sources
See docs/DATA_SOURCES.md for complete list