import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.crop_advisory_agent import CropAdvisoryAgent
from agents.market_price_agent import MarketPriceAgent
from agents.weather_agent import WeatherAgent
from agents.pest_disease_agent import PestDiseaseAgent
from agents.scheme_agent import SchemeAgent
from agents.fertilizer_agent import FertilizerAgent

class Orchestrator:
    def __init__(self):
        print("Loading all agents...")
        self.crop_agent    = CropAdvisoryAgent()
        self.market_agent  = MarketPriceAgent()
        self.weather_agent = WeatherAgent()
        self.pest_agent    = PestDiseaseAgent()
        self.scheme_agent  = SchemeAgent()
        self.fertilizer_agent = FertilizerAgent()
        print("✅ All 6 agents ready!")

    def route(self, query: str, language: str = "English", **kwargs):
        """Route query to correct agent using better intent detection"""
        query_lower = query.lower().strip()

    # Score each agent based on keyword relevance
        scores = {
            "fertilizer": 0,
            "scheme": 0,
            "market": 0,
            "weather": 0,
            "pest": 0,
            "crop": 0
        }

    # Fertilizer keywords
        fertilizer_words = [
            "fertilizer", "fertiliser", "npk", "nitrogen",
            "phosphorus", "potassium", "manure", "urea",
            "dap", "compost", "nutrient", "soil nutrient",
            "top dress", "basal dose", "micronutrient"
        ]

    # Scheme keywords
        scheme_words = [
            "scheme", "eligib", "pm-kisan", "pmfby",
            "subsidy", "benefit", "government", "insurance",
            "kisan", "yojana", "pension", "credit card",
            "ration", "welfare", "assistance"
        ]

    # Market keywords
        market_words = [
            "price", "sell", "mandi", "market", "rate",
            "cost", "buy", "quintal", "per kg", "profit",
            "sale", "trading", "wholesale", "retail"
        ]

    # Weather keywords
        weather_words = [
            "weather", "rain", "flood", "drought",
            "temperature", "forecast", "climate", "humid",
            "wind", "storm", "irrigation", "season"
        ]

    # Pest keywords
        pest_words = [
            "pest", "disease", "yellow", "spots", "wilt",
            "insect", "fungus", "symptom", "leaves", "curl",
            "damage", "rot", "blight", "virus", "bacteria",
            "infestation", "attack", "brown", "black spot"
        ]

    # Score each category
    for word in fertilizer_words:
        if word in query_lower:
            scores["fertilizer"] += 2
    for word in scheme_words:
        if word in query_lower:
            scores["scheme"] += 2
    for word in market_words:
        if word in query_lower:
            scores["market"] += 2
    for word in weather_words:
        if word in query_lower:
            scores["weather"] += 2
    for word in pest_words:
        if word in query_lower:
            scores["pest"] += 2

    # Default crop gets score 1 always
    scores["crop"] = 1

    # Find highest scoring agent
    best_agent = max(scores, key=scores.get)

    # Route to best agent
    if best_agent == "fertilizer" and scores["fertilizer"] > 0:
        print("→ Routing to Fertilizer Agent 🌱")
        return self.fertilizer_agent.ask(
            kwargs.get("crop", "paddy"),
            float(kwargs.get("land_size", "2")),
            kwargs.get("soil_type", "Clay Loam"),
            kwargs.get("district", "Guntur"),
            language
        )

    elif best_agent == "scheme" and scores["scheme"] > 0:
        print("→ Routing to Scheme Agent 🏛️")
        return self.scheme_agent.ask(
            kwargs.get("land_size", "2"),
            kwargs.get("income", "50000"),
            kwargs.get("district", "Guntur"),
            language
        )

    elif best_agent == "market" and scores["market"] > 0:
        print("→ Routing to Market Price Agent 💰")
        return self.market_agent.ask(
            kwargs.get("crop", "paddy"),
            kwargs.get("district", "Guntur"),
            language
        )

    elif best_agent == "weather" and scores["weather"] > 0:
        print("→ Routing to Weather Agent 🌤️")
        return self.weather_agent.ask(
            kwargs.get("crop", "paddy"),
            kwargs.get("district", "Guntur"),
            language
        )

    elif best_agent == "pest" and scores["pest"] > 0:
        print("→ Routing to Pest and Disease Agent 🐛")
        return self.pest_agent.ask(
            kwargs.get("crop", "paddy"),
            kwargs.get("symptoms", query),
            language
        )

    else:
        print("→ Routing to Crop Advisory Agent 🌾")
        return self.crop_agent.ask(
            query,
            language,
            district=kwargs.get("district", "Guntur")
        )


# Test all 6 agents
if __name__ == "__main__":
    orch = Orchestrator()

    print("\n" + "="*60)
    print("TEST 1 — Crop Advisory Agent")
    print("="*60)
    print(orch.route(
        "What are Kharif crops?",
        district="Guntur"
    ))

    print("\n" + "="*60)
    print("TEST 2 — Market Price Agent")
    print("="*60)
    print(orch.route(
        "What is the current price of paddy?",
        crop="Paddy",
        district="Krishna"
    ))

    print("\n" + "="*60)
    print("TEST 3 — Weather Agent")
    print("="*60)
    print(orch.route(
        "Will rain affect my cotton crop?",
        crop="Cotton",
        district="Guntur"
    ))

    print("\n" + "="*60)
    print("TEST 4 — Pest and Disease Agent")
    print("="*60)
    print(orch.route(
        "Yellow leaves on my tomato plant",
        crop="Tomato",
        symptoms="yellow leaves curling"
    ))

    print("\n" + "="*60)
    print("TEST 5 — Scheme Agent")
    print("="*60)
    print(orch.route(
        "Which government schemes am I eligible for?",
        district="Guntur",
        land_size="2",
        income="50000"
    ))