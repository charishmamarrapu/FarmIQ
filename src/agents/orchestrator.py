import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.crop_advisory_agent import CropAdvisoryAgent
from agents.market_price_agent import MarketPriceAgent
from agents.weather_agent import WeatherAgent
from agents.pest_disease_agent import PestDiseaseAgent
from agents.scheme_agent import SchemeAgent

class Orchestrator:
    def __init__(self):
        print("Loading all agents...")
        self.crop_agent    = CropAdvisoryAgent()
        self.market_agent  = MarketPriceAgent()
        self.weather_agent = WeatherAgent()
        self.pest_agent    = PestDiseaseAgent()
        self.scheme_agent  = SchemeAgent()
        print("✅ All 5 agents ready!")

    def route(self, query: str, language: str = "English", **kwargs):
        """Decides which agent to call based on query"""
        query_lower = query.lower()

        if any(word in query_lower for word in
               ["scheme", "eligib", "pm-kisan", "pmfby",
                "subsidy", "benefit", "government",
                "insurance", "kisan"]):
            print("→ Routing to Scheme Agent 🏛️")
            return self.scheme_agent.ask(
                kwargs.get("land_size", "2"),
                kwargs.get("income", "50000"),
                kwargs.get("district", "Guntur"),
                language
            )

        elif any(word in query_lower for word in
                 ["price", "sell", "mandi", "market",
                  "rate", "cost", "buy"]):
            print("→ Routing to Market Price Agent 💰")
            return self.market_agent.ask(
                kwargs.get("crop", "paddy"),
                kwargs.get("district", "Guntur"),
                language
            )

        elif any(word in query_lower for word in
                 ["weather", "rain", "flood", "drought",
                  "temperature", "forecast", "climate"]):
            print("→ Routing to Weather Agent 🌤️")
            return self.weather_agent.ask(
                kwargs.get("crop", "paddy"),
                kwargs.get("district", "Guntur"),
                language
            )

        elif any(word in query_lower for word in
                 ["pest", "disease", "yellow", "spots",
                  "wilt", "insect", "fungus", "symptom",
                  "leaves", "curling", "damage"]):
            print("→ Routing to Pest and Disease Agent 🐛")
            return self.pest_agent.ask(
                kwargs.get("crop", "paddy"),
                kwargs.get("symptoms", query),
                language
            )

        else:
            print("→ Routing to Crop Advisory Agent 🌾")
            return self.crop_agent.ask(query, language)


# Test all 5 agents
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