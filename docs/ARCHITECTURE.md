# FarmIQ Agent Architecture

## System Flow

Farmer Query (English/Telugu)
↓
Streamlit UI (6 Tabs)
↓
Orchestrator (Intent Detection)
↓
┌─────────────────────────────────────┐
│  price/mandi → Market Price Agent   │
│  weather/rain → Weather Agent       │
│  pest/disease → Pest Agent          │
│  scheme/kisan → Scheme Agent        │
│  fertilizer   → Fertilizer Agent    │
│  default      → Crop Advisory Agent │
└─────────────────────────────────────┘
↓
ChromaDB Similarity Search
(12,397 chunks from 10 PDFs + 2 CSVs)
↓
Groq llama-3.3-70b-versatile
(Generates grounded answer)
↓
Farmer gets clear advice ✅

## Agent Details

| Agent | Input | Data Source | Output |
|-------|-------|-------------|--------|
| Crop Advisory | Question + District | ICAR PDFs | Crop recommendations |
| Market Price | Crop + District | data.gov.in API + CSV | Price + sell/hold |
| Weather Impact | Crop + District | OpenWeatherMap API | Risk alerts |
| Pest & Disease | Crop + Symptoms | Pest management PDFs | Diagnosis + treatment |
| Govt Schemes | Land + Income | PM-KISAN/PMFBY PDFs | Eligibility info |
| Fertilizer Calc | Crop + Land + Soil | Agronomy PDFs | NPK quantities |

## Tech Stack
LLM          → Groq llama-3.3-70b-versatile
Embeddings   → HuggingFace all-MiniLM-L6-v2
Vector Store → ChromaDB (47MB)
RAG Framework→ LangChain
Frontend     → Streamlit
Deployment   → Streamlit Cloud