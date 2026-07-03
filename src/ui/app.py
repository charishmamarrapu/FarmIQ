import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agents.orchestrator import Orchestrator

# ── Load API Keys from Streamlit Secrets ────────────
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    os.environ["OPENWEATHER_API_KEY"] = st.secrets["OPENWEATHER_API_KEY"]
except:
    pass  # Falls back to .env file locally

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

# ── Sidebar ──────────────────────────────────────────
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

# ── Main Title ───────────────────────────────────────
st.title("🌾 FarmIQ — Agricultural Advisory System")
st.markdown(
    "AI-powered advice for farmers in "
    "Andhra Pradesh and Telangana"
)
st.markdown("---")

# ── Tabs ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌾 Crop Advisory",
    "💰 Market Price",
    "🌤️ Weather Alert",
    "🐛 Pest & Disease",
    "🏛️ Govt Schemes",
    "🌱 Fertilizer Calc"
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
        placeholder="Example: What is the best crop "
                    "to grow in Kharif season?",
        height=100
    )

    if st.button("Get Crop Advice 🌾", key="crop_btn"):
        if crop_question:
            with st.spinner(
                "Getting advice from agricultural documents..."
            ):
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
            "Banana", "Mango", "Coconut",
            "Soybean", "Sesame", "Castor",
            "Pearl Millet", "Finger Millet",
            "Black Pepper", "Cashew", "Coffee",
            "Cardamom", "Areca Nut"
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

                # Price Chart
                st.subheader("📊 Historical Price Trend")
                import pandas as pd
                price_data = pd.DataFrame({
                    "Month": [
                        "Jan", "Feb", "Mar", "Apr",
                        "May", "Jun", "Jul", "Aug",
                        "Sep", "Oct", "Nov", "Dec"
                    ],
                    "Price (₹/Quintal)": [
                        1800, 1850, 1900, 1780,
                        1820, 1950, 2000, 1980,
                        1870, 1760, 1800, 1900
                    ]
                })
                st.line_chart(
                    price_data.set_index("Month")
                )
                st.caption(
                    "Note: Chart shows indicative historical "
                    "price trend. Actual prices vary by market."
                )

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
            "Tomato", "Onion", "Brinjal", "Okra",
            "Banana", "Mango", "Coconut",
            "Soybean", "Sesame", "Castor",
            "Pearl Millet", "Finger Millet",
            "Black Pepper", "Cashew", "Coffee",
            "Cardamom", "Areca Nut"
        ]
    )

    if st.button("Get Weather Alert 🌤️", key="weather_btn"):
        with st.spinner("Fetching live weather forecast..."):
            try:
                orch = load_orchestrator()
                answer = orch.route(
                    "What is the weather forecast "
                    "and impact on my crop?",
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
        "Describe symptoms or upload a photo of "
        "your affected crop to get diagnosis and "
        "treatment advice."
    )

    pest_crop = st.selectbox(
        "Select Affected Crop",
        [
            "Paddy", "Cotton", "Maize", "Groundnut",
            "Sunflower", "Redgram", "Blackgram",
            "Greengram", "Jowar", "Bajra", "Wheat",
            "Sugarcane", "Turmeric", "Chilli",
            "Tomato", "Onion", "Brinjal", "Okra",
            "Banana", "Mango", "Coconut",
            "Soybean", "Sesame", "Castor", "Ragi"
        ]
    )

    # Input method selection
    input_method = st.radio(
        "How would you like to describe the problem?",
        ["📝 Describe Symptoms", "📷 Upload Photo"]
    )

    if input_method == "📝 Describe Symptoms":
        symptoms = st.text_area(
            "Describe the symptoms you see:",
            placeholder="Example: Leaves are turning "
                        "yellow and curling at the edges",
            height=100
        )

        if st.button("Identify Pest/Disease 🐛",
                     key="pest_btn"):
            if symptoms:
                with st.spinner(
                    "Analyzing symptoms from pest "
                    "management documents..."
                ):
                    try:
                        orch = load_orchestrator()
                        answer = orch.route(
                            f"pest disease symptoms {symptoms}",
                            language=language,
                            crop=pest_crop,
                            symptoms=symptoms
                        )
                        st.success(
                            "✅ Pest/Disease Analysis Ready!"
                        )
                        st.markdown(answer)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning(
                    "Please describe the symptoms first!"
                )

    else:  # Upload Photo
        uploaded_image = st.file_uploader(
            "Upload a photo of your affected crop",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo showing "
                 "the affected leaves, stems or fruits"
        )

        if uploaded_image is not None:
            # Show uploaded image
            from PIL import Image
            image = Image.open(uploaded_image)
            image_resized = image.resize((400, 300))
            st.image(
                image_resized,
                caption="Uploaded crop photo",
                width=400
            )

            # Ask farmer to describe what they see
            st.markdown("**What do you see in the photo?**")
            col1, col2 = st.columns(2)

            with col1:
                color_change = st.multiselect(
                    "Color changes on leaves/stems:",
                    ["Yellow leaves", "Brown spots",
                     "Black spots", "White patches",
                     "Purple discoloration", "Wilting",
                     "Curling leaves", "Dried leaves"]
                )

            with col2:
                other_symptoms = st.multiselect(
                    "Other symptoms visible:",
                    ["Holes in leaves", "Sticky substance",
                     "Insects visible", "Web on plants",
                     "Rotting stems", "Stunted growth",
                     "Falling leaves", "Damaged fruits"]
                )

            if st.button(
                "Analyze Photo 📷",
                key="photo_btn"
            ):
                with st.spinner(
                    "Analyzing your crop photo..."
                ):
                    try:
                        # Combine visual observations
                        image_description = (
                            f"Color changes: "
                            f"{', '.join(color_change) if color_change else 'None'}. "
                            f"Other symptoms: "
                            f"{', '.join(other_symptoms) if other_symptoms else 'None'}"
                        )

                        # Use pest agent directly
                        from agents.pest_disease_agent import PestDiseaseAgent
                        agent = PestDiseaseAgent()
                        answer = agent.analyze_image(
                            pest_crop,
                            image_description,
                            language
                        )

                        st.success("✅ Photo Analysis Ready!")
                        st.markdown(answer)

                    except Exception as e:
                        st.error(f"Error: {e}")

# ── TAB 5: Government Schemes ────────────────────────
with tab5:
    st.header("🏛️ Government Scheme Finder")
    st.markdown(
        "Find out which government schemes "
        "you are eligible for based on your details."
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

    if st.button(
        "Check Scheme Eligibility 🏛️",
        key="scheme_btn"
    ):
        with st.spinner("Checking government schemes..."):
            try:
                orch = load_orchestrator()
                answer = orch.route(
                    "government scheme eligibility",
                    language=language,
                    district=district,
                    land_size=str(land_size),
                    income=str(income)
                )
                st.success("✅ Scheme Information Ready!")
                st.markdown(answer)

                # Scheme Cards
                st.subheader("📋 Major Schemes to Check")
                col1, col2 = st.columns(2)
                with col1:
                    st.info(
                        "**PM-KISAN**\n\n"
                        "Rs 6,000 per year income "
                        "support for all landholding farmers"
                    )
                    st.info(
                        "**PMFBY**\n\n"
                        "Crop insurance against natural "
                        "calamities, pests and diseases"
                    )
                with col2:
                    st.info(
                        "**PM Kisan Maan Dhan Yojana**\n\n"
                        "Rs 3,000 monthly pension for "
                        "small and marginal farmers"
                    )
                    st.info(
                        "**Kisan Credit Card**\n\n"
                        "Easy credit access for crop "
                        "production and allied activities"
                    )

            except Exception as e:
                st.error(f"Error: {e}")

# ── TAB 6: Fertilizer Calculator ─────────────────────
with tab6:
    st.header("🌱 Fertilizer Calculator")
    st.markdown(
        "Calculate the optimal fertilizer quantity "
        "and cost for your crop and land size."
    )

    col1, col2 = st.columns(2)

    with col1:
        fert_crop = st.selectbox(
            "Select Your Crop",
            [
                "Paddy", "Cotton", "Maize", "Groundnut",
                "Sunflower", "Redgram", "Blackgram",
                "Greengram", "Jowar", "Bajra", "Wheat",
                "Sugarcane", "Turmeric", "Chilli",
                "Tomato", "Onion", "Brinjal", "Okra",
                "Banana", "Mango", "Coconut",
                "Soybean", "Sesame", "Castor", "Ragi"
            ],
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
            ]
        )
        st.info(
            "💡 **Tip:** Select the correct soil type "
            "for accurate fertilizer recommendations"
        )

    if st.button(
        "Calculate Fertilizer 🌱",
        key="fert_btn"
    ):
        with st.spinner(
            "Calculating optimal fertilizer plan..."
        ):
            try:
                orch = load_orchestrator()
                answer = orch.route(
                    "fertilizer recommendation",
                    language=language,
                    crop=fert_crop,
                    land_size=str(fert_land),
                    soil_type=soil_type,
                    district=district
                )
                st.success("✅ Fertilizer Plan Ready!")
                st.markdown(answer)

                # Summary cards
                st.subheader("📊 Key Nutrients for Plants")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(
                        "**Nitrogen (N)**\n\n"
                        "Promotes leaf and stem growth. "
                        "Source: Urea, DAP"
                    )
                with col2:
                    st.info(
                        "**Phosphorus (P)**\n\n"
                        "Promotes root growth. "
                        "Source: SSP, DAP"
                    )
                with col3:
                    st.info(
                        "**Potassium (K)**\n\n"
                        "Promotes fruit quality. "
                        "Source: MOP, SOP"
                    )

            except Exception as e:
                st.error(f"Error: {e}")