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
        self.crop_agent = CropAdvisoryAgent()
        self.market_agent = MarketPriceAgent()
        self.weather_agent = WeatherAgent()
        self.pest_agent = PestDiseaseAgent()
        self.scheme_agent = SchemeAgent()
        self.fertilizer_agent = FertilizerAgent()
        print("✅ All 6 agents ready!")

    def route(self, query: str, language: str = "English", **kwargs):
        """Route query to correct agent using keyword scoring"""
        query_lower = query.lower()

        scores = {
            "fertilizer": 0,
            "scheme": 0,
            "market": 0,
            "weather": 0,
            "pest": 0,
            "crop": 0
        }

        # Fertilizer keywords
        for word in [
            "fertilizer", "npk", "nitrogen", "phosphorus", "potassium",
            "manure", "urea", "dap", "nutrient", "dose"
        ]:
            if word in query_lower:
                scores["fertilizer"] += 2

        # Scheme keywords
        for word in [
            "scheme", "eligible", "eligibility", "pm-kisan", "pmfby",
            "subsidy", "benefit", "government", "insurance", "kisan", "yojana"
        ]:
            if word in query_lower:
                scores["scheme"] += 2

        # Market keywords
        for word in [
            "price", "sell", "mandi", "market", "rate",
            "cost", "buy", "rupee", "quintal", "hold"
        ]:
            if word in query_lower:
                scores["market"] += 2

        # Weather keywords
        for word in [
            "weather", "rain", "flood", "drought", "temperature",
            "forecast", "climate", "humidity", "wind", "storm"
        ]:
            if word in query_lower:
                scores["weather"] += 2

        # Pest keywords
        for word in [
            "pest", "disease", "yellow", "spots", "wilt", "insect",
            "fungus", "symptom", "leaves", "curling", "damage",
            "attack", "infected", "dying"
        ]:
            if word in query_lower:
                scores["pest"] += 2

        # Crop keywords
        for word in [
            "crop", "grow", "plant", "harvest", "soil",
            "seed", "irrigation", "season", "yield", "sow",
            "kharif", "rabi"
        ]:
            if word in query_lower:
                scores["crop"] += 2

        best_agent = max(scores, key=scores.get)

        if scores[best_agent] == 0:
            best_agent = "crop"

        if best_agent == "fertilizer":
            print("→ Routing to Fertilizer Agent 🌱")
            try:
                land_size = float(kwargs.get("land_size", 2))
            except ValueError:
                land_size = 2.0

            return self.fertilizer_agent.ask(
                kwargs.get("crop", "paddy"),
                land_size,
                kwargs.get("soil_type", "Clay Loam"),
                kwargs.get("district", "Guntur"),
                language
            )

        elif best_agent == "scheme":
            print("→ Routing to Scheme Agent 🏛️")
            return self.scheme_agent.ask(
                kwargs.get("land_size", 2),
                kwargs.get("income", 50000),
                kwargs.get("district", "Guntur"),
                language
            )

        elif best_agent == "market":
            print("→ Routing to Market Price Agent 💰")
            return self.market_agent.ask(
                kwargs.get("crop", "paddy"),
                kwargs.get("district", "Guntur"),
                language
            )

        elif best_agent == "weather":
            print("→ Routing to Weather Agent 🌤️")
            return self.weather_agent.ask(
                kwargs.get("crop", "paddy"),
                kwargs.get("district", "Guntur"),
                language
            )

        elif best_agent == "pest":
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