import sys
import os
import tempfile
from PIL import Image
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import Orchestrator


# ── Load API Keys from Streamlit Secrets ─────────────────────────
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    os.environ["OPENWEATHER_API_KEY"] = st.secrets["OPENWEATHER_API_KEY"]
except Exception:
    pass  # Falls back to .env file locally


# ── Page Configuration ───────────────────────────────────────────
st.set_page_config(
    page_title="FarmIQ - Agricultural Advisory",
    page_icon="🌾",
    layout="wide"
)

# ── Sidebar ──────────────────────────────────────────────────────
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
        # Andhra Pradesh Districts
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


# ── Main Title ───────────────────────────────────────────────────
st.title("🌾 FarmIQ — Agricultural Advisory System")
st.markdown(
    "AI-powered advice for farmers in Andhra Pradesh and Telangana"
)
st.markdown("---")


# ── Tabs ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌾 Crop Advisory",
    "💰 Market Price",
    "🌤️ Weather Alert",
    "🐛 Pest & Disease",
    "🏛️ Govt Schemes",
    "🌱 Fertilizer Calc"
])


# ── Common crop list ─────────────────────────────────────────────
COMMON_CROPS = [
    "Paddy", "Cotton", "Maize", "Groundnut",
    "Sunflower", "Redgram", "Blackgram",
    "Greengram", "Jowar", "Bajra", "Wheat",
    "Sugarcane", "Turmeric", "Chilli",
    "Tomato", "Onion", "Brinjal", "Okra",
    "Banana", "Mango", "Coconut",
    "Soybean", "Sesame", "Castor",
    "Pearl Millet", "Finger Millet",
    "Black Pepper", "Cashew", "Coffee",
    "Cardamom", "Areca Nut", "Ragi"
]


# ── TAB 1: Crop Advisory ─────────────────────────────────────────
with tab1:
    st.header("🌾 Crop Advisory")
    st.markdown(
        "Get expert advice on crops, fertilizers, irrigation, "
        "cultivation practices, and seasonal planning."
    )

    crop_question = st.text_area(
        "Ask your crop question:",
        placeholder="Example: What is the best crop to grow in Kharif season?",
        height=100
    )

    if st.button("Get Crop Advice 🌾", key="crop_btn"):
        if crop_question.strip():
            with st.spinner("Getting advice from agricultural documents..."):
                try:
                    orch = Orchestrator()
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


# ── TAB 2: Market Price ──────────────────────────────────────────
with tab2:
    st.header("💰 Market Price Advisory")
    st.markdown(
        "Check current mandi prices and get sell/hold recommendations."
    )

    crop_name = st.selectbox(
        "Select Your Crop",
        COMMON_CROPS,
        key="market_crop"
    )

    if st.button("Check Market Price 💰", key="market_btn"):
        with st.spinner("Fetching market price data..."):
            try:
                orch = Orchestrator()
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


# ── TAB 3: Weather Alert ─────────────────────────────────────────
with tab3:
    st.header("🌤️ Weather Alert")
    st.markdown(
        "Get weather forecast and crop protection advice for your district."
    )

    weather_crop = st.selectbox(
        "Select Your Crop for Weather Advisory",
        COMMON_CROPS,
        key="weather_crop"
    )

    if st.button("Get Weather Alert 🌤️", key="weather_btn"):
        with st.spinner("Fetching live weather forecast..."):
            try:
                orch = Orchestrator()
                answer = orch.route(
                    "What is the weather forecast and impact on my crop?",
                    language=language,
                    crop=weather_crop,
                    district=district
                )
                st.success("✅ Weather Advisory Ready!")
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error: {e}")


# ── TAB 4: Pest & Disease ────────────────────────────────────────
with tab4:
    st.header("🐛 Pest & Disease Identifier")
    st.markdown(
        "Describe symptoms or upload a crop photo to get diagnosis and treatment advice."
    )

    pest_crop = st.selectbox(
        "Select Affected Crop",
        COMMON_CROPS,
        key="pest_crop"
    )

    input_method = st.radio(
        "Choose Input Method",
        ["📝 Describe Symptoms", "📷 Upload Photo"],
        horizontal=True
    )

    # ── Option 1: Text symptoms ──────────────────────────────────
    if input_method == "📝 Describe Symptoms":
        symptoms = st.text_area(
            "Describe the symptoms you see:",
            placeholder="Example: Leaves are turning yellow and curling at the edges.",
            height=100
        )

        if st.button("Identify Pest / Disease 🐛", key="pest_btn"):
            if symptoms.strip():
                with st.spinner("Analyzing symptoms from pest management documents..."):
                    try:
                        orch = Orchestrator()
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

    # ── Option 2: Image upload ───────────────────────────────────
    else:
        uploaded_image = st.file_uploader(
            "Upload a photo of the affected crop",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo showing affected leaves, stems, or fruits.",
            key="pest_photo"
        )

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Crop Photo", width="stretch")

            st.markdown("### Optional: add visible symptoms for better accuracy")
            col1, col2 = st.columns(2)

            with col1:
                color_change = st.multiselect(
                    "Color changes on leaves/stems:",
                    [
                        "Yellow leaves", "Brown spots", "Black spots",
                        "White patches", "Purple discoloration",
                        "Wilting", "Curling leaves", "Dried leaves"
                    ],
                    key="color_change"
                )

            with col2:
                other_symptoms = st.multiselect(
                    "Other visible symptoms:",
                    [
                        "Holes in leaves", "Sticky substance", "Insects visible",
                        "Web on plants", "Rotting stems", "Stunted growth",
                        "Falling leaves", "Damaged fruits"
                    ],
                    key="other_symptoms"
                )

            if st.button("Analyze Photo 📷", key="photo_btn"):
                try:
                    extra_symptoms = []
                    
                    if color_change:
                        extra_symptoms.append("Color changes: " + ", ".join(color_change))

                    if other_symptoms:
                        extra_symptoms.append("Other symptoms: " + ", ".join(other_symptoms))

                    symptom_description = "\n".join(extra_symptoms).strip()

                    if not symptom_description:
                        st.warning("Please select at least one visible symptom from the image.")
                    else:
                        from agents.pest_disease_agent import PestDiseaseAgent

                        with st.spinner("Analyzing selected crop symptoms..."):
                            agent = PestDiseaseAgent()
                            answer = agent.ask(
                                crop=pest_crop,
                                symptoms=symptom_description,
                                language=language
                            )

                        st.success("✅ Photo-based Pest/Disease Advisory Ready!")
                        st.markdown("## 📝 Selected Symptoms")
                        st.write(symptom_description)

                        st.markdown("## 🌱 Advisory")
                        st.markdown(answer)

                except Exception as e:
                    st.error(f"Error while analyzing symptoms: {e}")

# ── TAB 5: Government Schemes ────────────────────────────────────
with tab5:
    st.header("🏛️ Government Scheme Finder")
    st.markdown(
        "Find government schemes you may be eligible for based on your farm details."
    )

    col1, col2 = st.columns(2)

    with col1:
        land_size = st.number_input(
            "Land Size (in acres)",
            min_value=0.1,
            max_value=100.0,
            value=2.0,
            step=0.5
        )

    with col2:
        income = st.number_input(
            "Annual Income (in Rupees)",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=5000
        )

    if st.button("Check Scheme Eligibility 🏛️", key="scheme_btn"):
        with st.spinner("Checking government schemes..."):
            try:
                orch = Orchestrator()
                answer = orch.route(
                    "government scheme eligibility",
                    language=language,
                    district=district,
                    land_size=land_size,
                    income=income
                )
                st.success("✅ Scheme Information Ready!")
                st.markdown(answer)

                st.subheader("📋 Major Schemes to Check")
                col1, col2 = st.columns(2)

                with col1:
                    st.info(
                        "**PM-KISAN**\n\n"
                        "₹6,000 per year income support for eligible landholding farmers."
                    )
                    st.info(
                        "**PMFBY**\n\n"
                        "Crop insurance against natural calamities, pests, and diseases."
                    )

                with col2:
                    st.info(
                        "**PM Kisan Maan Dhan Yojana**\n\n"
                        "₹3,000 monthly pension for eligible small and marginal farmers."
                    )
                    st.info(
                        "**Kisan Credit Card**\n\n"
                        "Easy credit access for crop production and allied activities."
                    )

            except Exception as e:
                st.error(f"Error: {e}")


# ── TAB 6: Fertilizer Calculator ─────────────────────────────────
with tab6:
    st.header("🌱 Fertilizer Calculator")
    st.markdown(
        "Calculate the optimal fertilizer quantity and cost for your crop and land size."
    )

    col1, col2 = st.columns(2)

    with col1:
        fert_crop = st.selectbox(
            "Select Your Crop",
            COMMON_CROPS,
            key="fert_crop"
        )
        fert_land = st.number_input(
            "Land Size (in acres)",
            min_value=0.5,
            max_value=100.0,
            value=2.0,
            step=0.5,
            key="fert_land"
        )

    with col2:
        soil_type = st.selectbox(
            "Select Soil Type",
            [
                "Clay Loam", "Sandy Loam", "Black Cotton Soil",
                "Red Soil", "Alluvial Soil", "Loamy Sand",
                "Silty Clay", "Sandy Clay Loam"
            ],
            key="soil_type"
        )
        st.info(
            "💡 Tip: Select the correct soil type for more accurate fertilizer recommendations."
        )

    if st.button("Calculate Fertilizer 🌱", key="fert_btn"):
        with st.spinner("Calculating optimal fertilizer plan..."):
            try:
                orch = Orchestrator()
                answer = orch.route(
                    "fertilizer recommendation",
                    language=language,
                    crop=fert_crop,
                    land_size=fert_land,
                    soil_type=soil_type,
                    district=district
                )
                st.success("✅ Fertilizer Plan Ready!")
                st.markdown(answer)

                st.subheader("📊 Key Nutrients for Plants")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.info(
                        "**Nitrogen (N)**\n\n"
                        "Promotes leaf and stem growth.\n\n"
                        "Common sources: Urea, DAP"
                    )

                with col2:
                    st.info(
                        "**Phosphorus (P)**\n\n"
                        "Promotes root growth and early crop establishment.\n\n"
                        "Common sources: SSP, DAP"
                    )

                with col3:
                    st.info(
                        "**Potassium (K)**\n\n"
                        "Improves plant strength, fruit quality, and stress tolerance.\n\n"
                        "Common sources: MOP, SOP"
                    )

            except Exception as e:
                st.error(f"Error: {e}")