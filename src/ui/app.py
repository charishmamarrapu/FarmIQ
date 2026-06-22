import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agents.orchestrator import Orchestrator

# ── Page Configuration ──────────────────────────────
st.set_page_config(
    page_title="FarmIQ - Agricultural Advisory",
    page_icon="🌾",
    layout="wide"
)

# ── Load Orchestrator Once ───────────────────────────
@st.cache_resource
def load_orchestrator():
    return Orchestrator()

# ── Language Toggle ──────────────────────────────────
st.sidebar.title("🌾 FarmIQ")
st.sidebar.markdown("Multi-Agent Agricultural Advisory System")
st.sidebar.markdown("---")

language = st.sidebar.radio(
    "Select Language / భాష ఎంచుకోండి",
    ["English", "Telugu"]
)

district = st.sidebar.selectbox(
    "Select Your District",
    [
        "Guntur", "Krishna", "West Godavari",
        "East Godavari", "Kurnool", "Nellore",
        "Visakhapatnam", "Vizianagaram",
        "Srikakulam", "Prakasam", "Chittoor",
        "Kadapa", "Anantapur", "Eluru",
        "Bapatla", "Palnadu", "NTR District",
        "Sri Potti Sriramulu Nellore",
        "Alluri Sitharama Raju", "Anakapalli",
        "Kakinada", "Konaseema",
        "Sri Sathya Sai", "Tirupati",

        # Telangana Districts
        "Warangal", "Karimnagar", "Khammam",
        "Nizamabad", "Hyderabad", "Medchal",
        "Rangareddy", "Sangareddy", "Siddipet",
        "Nalgonda", "Suryapet", "Mahbubnagar",
        "Nagarkurnool", "Wanaparthy", "Jogulamba",
        "Gadwal", "Narayanpet", "Mahabubabad",
        "Bhadradri Kothagudem", "Mulugu",
        "Jayashankar Bhupalpally", "Peddapalli",
        "Jagtial", "Rajanna Sircilla", "Kamareddy",
        "Nirmal", "Adilabad", "Kumuram Bheem",
        "Mancherial", "Asifabad", "Medak",
        "Vikarabad", "Yadadri Bhuvanagiri",
        "Jangaon", "Hanamkonda"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Team 5 — FarmIQ**")
st.sidebar.markdown("Charishma | Likhitha | Hasini")

# ── Main Title ───────────────────────────────────────
st.title("🌾 FarmIQ — Agricultural Advisory System")
st.markdown(
    "AI-powered advice for farmers in Andhra Pradesh and Telangana"
)
st.markdown("---")

# ── Tabs ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🌾 Crop Advisory",
    "💰 Market Price",
    "🌤️ Weather Alert",
    "🐛 Pest & Disease"
])

# ── TAB 1: Crop Advisory ─────────────────────────────
with tab1:
    st.header("🌾 Crop Advisory")
    st.markdown(
        "Get expert advice on crops, fertilizers, "
        "irrigation and cultivation practices."
    )

    crop_question = st.text_area(
        "Ask your crop question:",
        placeholder="Example: What is the best crop to grow in Kharif season?",
        height=100
    )

    if st.button("Get Crop Advice 🌾", key="crop_btn"):
        if crop_question:
            with st.spinner("Getting advice from agricultural documents..."):
                try:
                    orch = load_orchestrator()
                    answer = orch.route(
                        crop_question,
                        language=language,
                        district=district
                    )
                    st.success("✅ Advisory Ready!")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please type your question first!")

# ── TAB 2: Market Price ──────────────────────────────
with tab2:
    st.header("💰 Market Price Advisory")
    st.markdown(
        "Check current mandi prices and get "
        "sell or hold recommendations."
    )

    crop_name = st.selectbox(
        "Select Your Crop",
        [
            "Paddy", "Cotton", "Maize", "Groundnut",
            "Sunflower", "Redgram", "Blackgram",
            "Greengram", "Jowar", "Bajra", "Wheat",
            "Sugarcane", "Turmeric", "Chilli",
            "Tomato", "Onion", "Brinjal", "Okra",
            "Banana", "Mango", "Coconut"
        ]
    )

    if st.button("Check Market Price 💰", key="market_btn"):
        with st.spinner("Fetching market price data..."):
            try:
                orch = load_orchestrator()
                answer = orch.route(
                    f"What is the current price of {crop_name}?",
                    language=language,
                    crop=crop_name,
                    district=district
                )
                st.success("✅ Price Advisory Ready!")
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error: {e}")

# ── TAB 3: Weather Alert ─────────────────────────────
with tab3:
    st.header("🌤️ Weather Alert")
    st.markdown(
        "Get weather forecast and crop protection "
        "advice for your district."
    )

    weather_crop = st.selectbox(
        "Select Your Crop for Weather Advisory",
        [
            "Paddy", "Cotton", "Maize", "Groundnut",
            "Sunflower", "Redgram", "Blackgram",
            "Greengram", "Jowar", "Bajra", "Wheat",
            "Sugarcane", "Turmeric", "Chilli",
            "Tomata", "Onion", "Brinjal", "Okra",
            "Banana", "Mango", "Coconut"
        ]
    )

    if st.button("Get Weather Alert 🌤️", key="weather_btn"):
        with st.spinner("Fetching live weather forecast..."):
            try:
                orch = load_orchestrator()
                answer = orch.route(
                    f"What is the weather forecast and impact on my crop?",
                    language=language,
                    crop=weather_crop,
                    district=district
                )
                st.success("✅ Weather Advisory Ready!")
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error: {e}")

# ── TAB 4: Pest & Disease ────────────────────────────
with tab4:
    st.header("🐛 Pest & Disease Identifier")
    st.markdown(
        "Describe your crop symptoms and get "
        "pest or disease identification with treatment advice."
    )

    pest_crop = st.selectbox(
        "Select Affected Crop",
        [
            "Paddy", "Cotton", "Maize", "Groundnut",
            "Sunflower", "Redgram", "Blackgram",
            "Greengram", "Jowar", "Bajra", "Wheat", 
            "Sugarcane", "Turmeric", "Chilli", 
            "Tomato", "Onion", "Brinjal", "Okra", 
            "Banana", "Mango", "Coconut"
        ]
    )

    symptoms = st.text_area(
        "Describe the symptoms you see:",
        placeholder="Example: Leaves are turning yellow and curling at the edges",
        height=100
    )

    if st.button("Identify Pest/Disease 🐛", key="pest_btn"):
        if symptoms:
            with st.spinner("Analyzing symptoms from pest management documents..."):
                try:
                    orch = load_orchestrator()
                    answer = orch.route(
                        f"pest disease symptoms {symptoms}",
                        language=language,
                        crop=pest_crop,
                        symptoms=symptoms
                    )
                    st.success("✅ Pest/Disease Analysis Ready!")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please describe the symptoms first!")